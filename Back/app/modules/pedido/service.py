



from decimal import Decimal

from fastapi import HTTPException, status
import logging
from app.core.uow import UnitOfWork
from app.historialestadopedido.model import HistorialEstadoPedido
from app.modules.pedido.schema import PedidoCreate, PedidoList, PedidoPublic, PedidoRead
from app.modules.usuarios.model import Usuario

# Para que el logger en _emit_ws_events funcione
logger = logging.getLogger(__name__)
# =============================================================================
# NORMALIZACIÓN DE ESTADOS
# =============================================================================
#
# Unifica variaciones de entrada (inglés, mayúsculas, abreviaturas) a valores
# canónicos en minúsculas. Esto permite que el frontend envíe "Pendiente",
# "pending" o "PENDIENTE" y siempre se resuelva a "pendiente".
#
# Ejemplo de uso:
#   estado_db = "PENDIENTE"
#   estado_normalizado = ESTADOS.get(estado_db, estado_db)  # → "pendiente"
#
ESTADOS = {
    # Español
    "pendiente": "pendiente",
    "confirmado": "confirmado",
    "preparando": "preparando",
    "enviado": "enviado",
    "entregado": "entregado",
    "cancelado": "cancelado",
    # Inglés
    "pending": "pendiente",
    "confirmed": "confirmado",
    "shipped": "enviado",
    "delivered": "entregado",
    "cancelled": "cancelado",
    # Abreviaturas
    "en_prep": "preparando",
    "en_preparacion": "preparando",
    "en_camino": "listo",
    "listo": "listo",
    "ready": "listo",
    # Backward-compat (pedidos viejos en BD con estado enviado)
    "enviado": "listo",
}



# =============================================================================
# EVENTOS WebSocket
# =============================================================================
#
# Mapea cada estado destino al nombre del evento WebSocket que se envía
# al frontend. Los nombres siguen convención SCREAMING_SNAKE_CASE.
#
# Estos eventos son los que el frontend KDS escucha en socket.onmessage.
#
EVENTOS_WS = {
    "pendiente":  "NUEVO_PEDIDO",
    "confirmado": "PEDIDO_CONFIRMADO",
    "en_prep": "PEDIDO_EN_PREPARACION",
    "listo":      "PEDIDO_LISTO",
    "cancelado":  "PEDIDO_CANCELADO",
    "entregado":  "PEDIDO_ENTREGADO",
}

ROLES_POR_TRANSICION = {
    "pendiente":  ["pedidos", "admin"],
    "confirmado": ["pedidos", "cocina", "admin"],
    "en_prep": ["cocina", "pedidos", "admin"],
    "listo":      ["pedidos", "admin"],   # Cajero recibe aviso para entregar
    "entregado":  ["pedidos", "admin"],
    "cancelado":  ["pedidos", "cocina", "admin"],
}
class PedidoService:



    def crear_pedido(self,usuario_id: int, pedido: PedidoCreate) -> PedidoRead:
        with UnitOfWork() as uow:

            existeusuario = uow.usuarios.get_by_id(usuario_id)
            if not existeusuario:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado",
                )
            
            existedireccion = uow.direcciones.get_by_id(pedido.direccion_id)
            if not existedireccion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Direccion no encontrada",
                )
            if existedireccion.usuario_id != usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La dirección no pertenece al usuario.",
                )
            existe_forma_pago = uow.formas_pago.get_forma_de_pago_by_codigo(pedido.forma_pago_codigo)
            
            if not existe_forma_pago:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Forma de pago no válida.",
                )
            
            if not pedido.detalles:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El pedido debe tener al menos un detalle.",
                )
            #      Creo el pedido primero para obtener el id
            pedido_db = uow.pedidos.create({
                "direccion_id": pedido.direccion_id,
                "forma_pago_codigo": pedido.forma_pago_codigo,
                "descuento": pedido.descuento,
                "notas": pedido.notas,
                "usuario_id": usuario_id,
                "estado_codigo": "PENDIENTE",
                "subtotal": Decimal("0"),
                "total": Decimal("0"),
                "costo_envio": Decimal("50.00"),
            })

            for detalle in pedido.detalles:
                producto = uow.productos.get_by_id(detalle.producto_id)
                if not producto:
                    raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto con id {detalle.producto_id} no encontrado",
    )
                
                if (producto.stock_cantidad < detalle.cantidad):
                    raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La cantidad excede el stock disponible",
                )
                
                producto.stock_cantidad -= detalle.cantidad
                uow.productos.update(producto)
                
                detalle_data = detalle.model_dump()
                detalle_data["pedido_id"] = pedido_db.id
                detalle_data["subtotal_snapshot"] = detalle_data["precio_snapshot"] * detalle_data["cantidad"]
                uow.detalles_pedido.create(detalle_data)

            #        Traigo de nuevo el pedido para actualizar los detalles
            pedido_db = uow.pedidos.get_by_id(pedido_db.id) 

            subtotal_pedido = sum(d.precio_snapshot * d.cantidad for d in pedido_db.detalles)
            total_pedido = Decimal(str(subtotal_pedido)) + pedido_db.costo_envio - pedido_db.descuento

            pedido_db.subtotal = subtotal_pedido
            pedido_db.total = total_pedido

            rta= uow.pedidos.update(pedido_db)

            uow.historialestadopedido.create(
            
            HistorialEstadoPedido(
            pedido_id=pedido_db.id,
            estado_desde=None,       # RN-02 — primera transición
            estado_hacia="PENDIENTE",
            usuario_id=usuario_id,
            motivo=None
            )
)

            return PedidoRead.model_validate(rta)
        
        #  traer los pedidos de un cliente,

    def traer_pedidos_por_cliente(self, cliente_id: int) -> PedidoList:
        with UnitOfWork() as uow:
            existecliente = uow.usuarios.get_by_id(cliente_id)
            if not existecliente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado",
                )
            
            data = uow.pedidos.get_by_usuario_id(cliente_id)
            count = len(data)

            return PedidoList(data=[PedidoPublic.model_validate(p) for p in data], count=count)
        
        
        #  traer todos los pedidos

    def traer_todos_los_pedidos(self) -> PedidoList:
        with UnitOfWork() as uow:
            data = uow.pedidos.get_all()
            count = len(data)

            return PedidoList(data=[PedidoPublic.model_validate(p) for p in data], count=count)

        #  traer pedidos por estado

    def traer_pedidos_por_estado(self, estado_codigo: str) -> PedidoList:
        with UnitOfWork() as uow:
            existeestado = uow.estadopedido.get_by_codigo(estado_codigo)
            if not existeestado:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Estado de pedido no encontrado",
                )
            data = uow.pedidos.get_by_estado(estado_codigo)
            count = len(data)

            return PedidoList(data=[PedidoPublic.model_validate(p) for p in data], count=count)
    
        #  traer pedidos de un cliente por estado,

    def traer_pedidos_por_estado_por_cliente(self, cliente_id: int, estado_codigo: str) -> PedidoList:
        with UnitOfWork() as uow:
            existecliente = uow.usuarios.get_by_id(cliente_id)
            if not existecliente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado",
                )
            existeestado = uow.estadopedido.get_by_codigo(estado_codigo)
            if not existeestado:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Estado de pedido no encontrado",
                )
            data = uow.pedidos.get_by_estado_by_usuario_id(cliente_id, estado_codigo)
            count = len(data)

            return PedidoList(data=[PedidoPublic.model_validate(p) for p in data], count=count)


        #  traer un pedido por id. 

    def traer_pedido_por_id(self, pedido_id: int, usuario: Usuario) -> PedidoRead:
        with UnitOfWork() as uow:
            pedido = uow.pedidos.get_by_id(pedido_id)
            if not pedido:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pedido no encontrado",
                )
            
            if not any(r.codigo in ["ADMIN", "PEDIDOS"] for r in usuario.roles) and pedido.usuario_id != usuario.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tenés permiso para ver este pedido.",
                )
        
            return PedidoRead.model_validate(pedido)
        
    def list_cocina_pedidos(self)-> list[PedidoPublic]:
        with UnitOfWork() as uow:
            pedidos = uow.pedidos.get_all()
            pedidos_cocina = [
                p for p in pedidos
                if p.estado_codigo.upper() in ("CONFIRMADO", "PREPARANDO", "EN_PREP", "EN_PREPARACION")
            ]
            pedidos_cocina.sort(key=lambda p:p.id or 0)
            result = [PedidoPublic.model_validate(p) for p in pedidos_cocina]

        return result



    # =========================================================================
    # EMISIÓN DE EVENTOS WebSocket
    # =========================================================================

    async def _emit_ws_events(
        self, pedido_id: int, destino: str, result: PedidoPublic
    ) -> None:
        """
        Emite eventos WebSocket a las rooms relevantes según el estado destino.

        Este método implementa la lógica de notificación selectiva:
          1. SIEMPRE emite a la room del pedido (order:{orderId})
             → El cliente que hizo el pedido recibe la actualización
          2. Emite a las rooms de los roles relevantes
             → El personal recibe solo lo que le compete

        El evento incluye el pedido completo serializado como diccionario,
        para que el frontend pueda actualizar su estado local sin hacer
        un fetch adicional a la API REST.

        Args:
            pedido_id: ID del pedido (para la room order:{id})
            destino:   Estado al que se transitionó (para mapear el evento)
            result:    PedidoPublic con los datos actualizados
        """
        from app.core.websocket import manager

        # Mapear estado destino → nombre del evento WebSocket
        # Si el estado no tiene evento asociado (ej: "pendiente"), no se emite
        destino_lower = destino.lower()
        event_type = EVENTOS_WS.get(destino_lower)
        if not event_type:
            return

        # Serializar el pedido a diccionario para enviar como JSON
        data = result.model_dump( mode= 'json')

        # ─── NOTIFICAR AL CLIENTE (room del pedido) ──────────────────────────
        # El cliente que hizo el pedido siempre recibe la actualización,
        # sin importar qué rol procesó el cambio.
        #
        # Ejemplo: si el pedido #5 pasó a "confirmado":
        #   broadcast_to_order(5, "PEDIDO_CONFIRMADO", pedido_data)
        #   → El socket del cliente en "order:5" recibe el evento
        #
        await manager.broadcast_to_order(pedido_id, event_type, data)

        # ─── NOTIFICAR A LOS ROLES RELEVANTES ───────────────────────────────
        # Cada transición notifica a los roles que necesitan saber el cambio.
        # La configuración está en ROLES_POR_TRANSICION.
        #
        # Ejemplo: si el pedido pasó a "confirmado":
        #   broadcast_to_roles(["pedidos", "cocina"], "PEDIDO_CONFIRMADO", data)
        #   → Los sockets en "role:pedidos" y "role:cocina" reciben el evento
        #   → Un socket que esté en ambas rooms solo recibe una vez (deduplicación)
        #
        roles_a_notificar = ROLES_POR_TRANSICION.get(destino_lower, [])
        if roles_a_notificar:
            await manager.broadcast_to_roles(roles_a_notificar, event_type, data)

        logger.info(
            f"WS emitido: {event_type} | pedido={pedido_id} | "
            f"roles={roles_a_notificar} | rooms_activas={manager.get_rooms_info()}"
        )

    async def avanzar_estado(
        self,
        pedido_id: int,
        nuevo_estado: str,
        current_user: Usuario,
        motivo: str | None = None,
    ) -> PedidoPublic:
        """
        Avanza el estado de un pedido usando la FSM del modelo y emite eventos WS.

        Flujo:
          1. Busca el pedido en la BD
          2. Valida permisos del usuario autenticado
          3. Delega la transición a pedido.cambiar_estado() (dominio)
          4. Persiste el historial de estado
          5. Emite eventos WebSocket a rooms relevantes
        """
        with UnitOfWork() as uow:
            pedido = uow.pedidos.get_by_id(pedido_id)
            if not pedido:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pedido no encontrado",
                )

            user_roles = [r.codigo for r in current_user.roles]
            # Solo staff o el dueño del pedido pueden avanzar el estado
            if not any(r in ["ADMIN", "PEDIDOS", "COCINA"] for r in user_roles) and pedido.usuario_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tenés permiso para modificar este pedido.",
                )

            # Delegar a la FSM del modelo
            estado_desde = pedido.cambiar_estado(nuevo_estado, user_roles, motivo)

            # Si el pedido se cancela, y el estado es pendiente o confirmado,
            # se recupera el stock

            if pedido.estado_codigo == "CANCELADO" and estado_desde in ("PENDIENTE", "CONFIRMADO"):
                for detalle in pedido.detalles:
                    producto = uow.productos.get_by_id(detalle.producto_id)
                    if producto:
                        producto.stock_cantidad += detalle.cantidad
                        uow.productos.update(producto)

                        
            # Registrar historial
            uow.historialestadopedido.create(
                HistorialEstadoPedido(
                    pedido_id=pedido.id,
                    estado_desde=estado_desde,
                    estado_hacia=pedido.estado_codigo,
                    usuario_id=current_user.id,
                    motivo=motivo,
                )
            )

            # Persistir cambios
            uow.pedidos.update(pedido)

            result = PedidoPublic.model_validate(pedido)
            estado_final = pedido.estado_codigo

        # Emitir eventos WS fuera del UoW para no bloquear la transacción
        await self._emit_ws_events(pedido_id, estado_final, result)
        return result
    
    async def cancelar_pedido_cliente(
        self,
        pedido_id: int,
        current_user: Usuario,
    ) -> PedidoPublic:
        """
        Cancela un pedido desde la vista del cliente.
        Valida ownership y estado (PENDIENTE o CONFIRMADO).
        """
        with UnitOfWork() as uow:
            pedido = uow.pedidos.get_by_id(pedido_id)
            if not pedido:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pedido no encontrado",
                )

            #  solo el dueño puede cancelar
            if pedido.usuario_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tenés permiso para cancelar este pedido.",
                )

            # solo PENDIENTE o CONFIRMADO
            estado_desde = pedido.estado_codigo
            if estado_desde not in ("PENDIENTE", "CONFIRMADO"):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Solo podés cancelar pedidos pendientes o confirmados. Estado actual: {estado_desde}",
                )

            
            pedido.estado_codigo = "CANCELADO"

            #  Recuperar stock
            for detalle in pedido.detalles:
                producto = uow.productos.get_by_id(detalle.producto_id)
                if producto:
                    producto.stock_cantidad += detalle.cantidad
                    uow.productos.update(producto)

            # Registrar historial
            uow.historialestadopedido.create(
                HistorialEstadoPedido(
                    pedido_id=pedido.id,
                    estado_desde=estado_desde,
                    estado_hacia="CANCELADO",
                    usuario_id=current_user.id,
                    motivo="Cancelado por el cliente",
                )
            )

            uow.pedidos.update(pedido)
            result = PedidoPublic.model_validate(pedido)
            estado_final = pedido.estado_codigo

        #  WebSocket (igual que avanzar_estado)
        await self._emit_ws_events(pedido_id, estado_final, result)
        return result

pedidoservice = PedidoService()