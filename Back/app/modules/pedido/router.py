


import json
import pathlib
from typing import Annotated

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from app.core.deps import get_current_active_user, require_role
from app.core.security import decode_access_token
from app.core.uow import UnitOfWork
from app.core.websocket import manager
from app.modules.pedido.schema import PedidoCreate, PedidoEstadoUpdate, PedidoList, PedidoPublic, PedidoRead
from app.modules.pedido.service import PedidoService
from fastapi import Depends, Response, status

from app.modules.usuarios.model import Usuario
from app.modules.usuarios.schemas import UsuarioPublico

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

# Roles autorizados para acceder a los endpoints de cocina/KDS
# Se incluyen variaciones en mayúsculas para robustez en comparación
COCINA_ROLES = ["cocina", "COCINA", "pedidos", "PEDIDOS", "admin", "ADMIN"]

# Roles que pueden gestionar pedidos (para WebSocket y FSM)
# Lista normalizada en minúsculas para lógica interna
STAFF_ROLES = ["admin", "pedidos", "cocina"]


service = PedidoService()

def get_pedido_service() -> PedidoService:
    return service

# crear

@router.post("/", response_model = PedidoRead, status_code= status.HTTP_201_CREATED)
async def crear_pedido(
    pedido: PedidoCreate,
    usuario: Annotated[Usuario, Depends(get_current_active_user)]
):
    result = service.crear_pedido(usuario.id, pedido)
    #  mode = json le dice a pydantic que convierta todo a tipso que JSON entiende
    data = result.model_dump(mode = 'json')
    await manager.broadcast_to_roles(["pedidos", "admin"], "NUEVO_PEDIDO", data)
    await manager.broadcast_to_order(result.id, "NUEVO_PEDIDO", data)

    return result



# traer pedidos de el usuario autenticado

@router.get("/pedidosdelusuario", response_model = PedidoList, status_code = status.HTTP_200_OK)
def traer_pedidos_por_cliente(
    usuario: Annotated[Usuario, Depends(get_current_active_user)]
):
    return service.traer_pedidos_por_cliente(usuario.id)

# traer todos los pedidos - solo admin

@router.get("/", response_model = PedidoList, status_code = status.HTTP_200_OK)
def traer_todos(admin: Annotated[Usuario, Depends(require_role(["ADMIN", "PEDIDOS"]))]):
    return service.traer_todos_los_pedidos()

# traer pedidos por estado

@router.get("/admin/estado/{estado}", response_model = PedidoList, status_code = status.HTTP_200_OK)
def traer_pedidos_por_estado(
    estado: str,
    admin: Annotated[Usuario,Depends(require_role(["ADMIN", "PEDIDOS"]))]
    ):
    return service.traer_pedidos_por_estado(estado)

# traer pedidos del cliente autenticado por estado

@router.get("/estado/{estado}", response_model = PedidoList, status_code = status.HTTP_200_OK)
def traer_pedidos_por_estado_del_usuario(
    estado: str,
    usuario: Annotated[Usuario, Depends(get_current_active_user)]
):
    return service.traer_pedidos_por_estado_por_cliente(usuario.id, estado)

# traer pedido por ID

@router.get("/{pedido_id}", response_model=PedidoRead, status_code=status.HTTP_200_OK)
def traer_pedido_por_id(
    pedido_id: int,
    usuario: Annotated[Usuario, Depends(get_current_active_user)]
):
    return service.traer_pedido_por_id(pedido_id, usuario)


# =============================================================================
# ENDPOINTS DEL DISPLAY DE COCINA (KDS)
# =============================================================================

@router.get("/cocina/pedidos", response_model=list[PedidoPublic])
def list_cocina_pedidos(
    _user: Annotated[UsuarioPublico, Depends(require_role(COCINA_ROLES))],
    svc: PedidoService = Depends(get_pedido_service),
) -> list[PedidoPublic]:
    """
    GET /api/v1/cocina/pedidos — Lista pedidos activos para la pantalla de cocina.

    Requiere: roles cocina, pedidos o admin.
    Filtra solo estados activos de cocina: "confirmado" o "preparando".
    Ordenados por antigüedad (ID ascendente).
    """
    return svc.list_cocina_pedidos()


# =============================================================================
# ENDPOINTS DE SERVICIO PARA FRONTENDS
# =============================================================================

CAJERO_ROLES = ["admin", "pedidos"]


@router.get("/cajero/pedidos", response_model=list[PedidoPublic])
def list_cajero_pedidos(
    _user: Annotated[UsuarioPublico, Depends(require_role(CAJERO_ROLES))],
    svc: PedidoService = Depends(get_pedido_service),
) -> list[PedidoPublic]:
    """GET /api/v1/cajero/pedidos — Lista todos los pedidos para el cajero."""
    return svc.traer_todos_los_pedidos()


@router.get("/cliente/mis-pedidos", response_model=PedidoList)
def list_cliente_pedidos(
    current_user: Annotated[UsuarioPublico, Depends(get_current_active_user)],
    svc: PedidoService = Depends(get_pedido_service),
) -> PedidoList:
    """GET /api/v1/cliente/mis-pedidos — Lista pedidos del usuario autenticado."""
    return svc.traer_pedidos_por_cliente(current_user.id)


# =============================================================================
# CAMBIO DE ESTADO (FSM — Finite State Machine)
# =============================================================================

@router.patch("/{pedido_id}/estado", response_model=PedidoPublic)
async def avanzar_pedido_estado(
    pedido_id: int,
    data: PedidoEstadoUpdate,
    current_user: Annotated[UsuarioPublico, Depends(require_role(COCINA_ROLES))],
    svc: PedidoService = Depends(get_pedido_service),
) -> PedidoPublic:
    """
    PATCH /api/v1/pedidos/{id}/estado — Avanza el estado de un pedido (FSM).

    Requiere: roles cocina, pedidos o admin.
    Valida la transición según la FSM + RBAC en un solo lookup.
    Emite eventos WebSocket a rooms relevantes después de persistir.

    Ejemplo de body:
        {"nuevo_estado": "confirmado", "motivo": "Pago verificado"}
    """
    return await svc.avanzar_estado(pedido_id, data.nuevo_estado, current_user, data.motivo)


# =============================================================================
# WEBSOCKET — CANAL BIDIRECCIONAL PARA TIEMPO REAL
# =============================================================================
#
# Este es el endpoint WebSocket principal del sistema.
#
# ─── PROTOCOLO ────────────────────────────────────────────────────────────────
#
# El protocolo sobre WebSocket es JSON bidireccional:
#
#   Cliente → Backend (acciones):
#     {"action": "subscribe-order",   "order_id": 5}
#     {"action": "unsubscribe-order", "order_id": 5}
#
#   Backend → Cliente (eventos):
#     {"event": "PEDIDO_CONFIRMADO",     "data": {...}}
#     {"event": "PEDIDO_EN_PREPARACION", "data": {...}}
#     {"event": "PEDIDO_EN_CAMINO",      "data": {...}}
#     {"event": "PEDIDO_CANCELADO",      "data": {...}}
#     {"event": "PEDIDO_ENTREGADO",      "data": {...}}
#     {"event": "SUBSCRIBED",            "data": {"order_id": 5}}
#     {"event": "ERROR",                 "data": {"detail": "..."}}
#
# ─── AUTENTICACIÓN ────────────────────────────────────────────────────────────
#
# El WebSocket NO soporta headers personalizados en el handshake desde el
# navegador (limitación del API WebSocket del browser). Por eso usamos
# cookies HttpOnly, que se envían automáticamente en el handshake:
#
#   1. El frontend primero hace login via REST: POST /api/v1/auth/token
#   2. El backend setea una cookie HttpOnly con el JWT
#   3. Al abrir el WebSocket, el browser envía la cookie automáticamente
#   4. El backend lee el JWT de la cookie y lo valida
#
# ─── SEGURIDAD ────────────────────────────────────────────────────────────────
#
#   - Solo usuarios activos pueden conectarse
#   - Los clientes (role:user) solo pueden suscribirse a pedidos propios
#   - La validación de propiedad se hace contra la BD (no confía en el cliente)
#   - Los códigos de cierre 1008 transmiten la razón del rechazo al frontend
#
# =============================================================================

@router.websocket("/cocina/ws")
async def websocket_endpoint(
    websocket: WebSocket,
):
    """
    WebSocket /api/v1/cocina/ws — Canal bidireccional autenticado para tiempo real.

    Flujo completo:
      1. Handshake: valida JWT desde cookie HttpOnly
      2. Conexión: une el socket a room de su rol
      3. Escucha: procesa suscripciones a pedidos específicos
      4. Desconexión: limpia todas las rooms del socket

    Arquitectura de rooms:
      - role:{rol}   → room del rol (cocina, pedidos, admin, user)
      - order:{id}   → room del pedido (solo para clientes)
    """

    # =========================================================================
    # PASO 1: EXTRAER TOKEN DE LA COOKIE HTTPONLY
    # =========================================================================
    # El browser envía automáticamente las cookies en el handshake WebSocket.
    # La cookie "access_token" contiene el JWT firmado.
    #
    # ¿Por qué cookie y no header?
    #   - El API WebSocket del navegador NO permite configurar headers
    #   - Las cookies HttpOnly no son accesibles desde JavaScript (protección XSS)
    #   - SameSite=lax previene ataques CSRF
    #
    token = websocket.cookies.get("access_token")

    if not token:
        # Sin token → rechazar con código 1008 (Policy Violation)
        # IMPORTANTE: debemos aceptar ANTES de close para que el cliente
        # reciba el código y la razón del rechazo
        await websocket.accept()
        await websocket.close(code=1008, reason="Token de autenticación requerido")
        return

    # =========================================================================
    # PASO 2: DECODIFICAR Y VALIDAR EL JWT
    # =========================================================================
    # decode_access_token() valida:
    #   - La firma HMAC (que no fue manipulado)
    #   - La expiración (exp claim)
    #   - Retorna el payload o None si es inválido
    #
    payload = decode_access_token(token)
    if not payload:
        await websocket.accept()
        await websocket.close(code=1008, reason="Token inválido o expirado")
        return

    # Extraer el "sub" (subject) del token — es el username
    email = payload.get("sub")
    if not email:
        await websocket.accept()
        await websocket.close(code=1008, reason="Token inválido")
        return

    # =========================================================================
    # PASO 3: VALIDAR USUARIO EN BASE DE DATOS
    # =========================================================================
    # Aunque el JWT sea válido, el usuario podría:
    #   - Haber sido eliminado de la BD
    #   - Haber sido desactivado (disabled=True)
    #
    # Siempre validamos contra la BD para tener la información más reciente.
    #
    # NOTA: Cualquier rol autenticado puede conectarse al WebSocket.
    # La diferenciación de roles se hace via rooms:
    #   - role:cocina  → recibe eventos de cocina
    #   - role:pedidos → recibe eventos de pedidos
    #   - role:user    → solo recibe eventos de sus pedidos específicos
    #
    #with Session(engine) as db_session:
    with UnitOfWork() as uow:
            user = uow.usuarios.get_by_email(email)
            if not user or user.disabled:
                await websocket.accept()
                await websocket.close(code=1008, reason="Usuario inválido o inactivo")
                return
            # Extraer valores primitivos DENTRO de la sesión antes de que se cierre.
            # Evita DetachedInstanceError al acceder a atributos fuera del bloque.
            user_roles = [r.codigo for r in user.roles]
            user_role = user_roles[0] if user_roles else "user"
            user_roles_upper = [r.upper().strip() for r in user_roles]
            user_id: int = user.id

    # =========================================================================
    # PASO 4: REGISTRAR EN EL CONNECTION MANAGER
    # =========================================================================
    from app.core.websocket import manager
    await manager.connect(websocket, role=user_role, user_id=user_id)

    # Unir al socket a todas las rooms de roles adicionales
    for rol in user_roles[1:]:
        manager._join_room(websocket, f"role:{rol.lower()}")

    # =========================================================================
    # PASO 5: BUCLE DE ESCUCHA DE MENSAJES
    # =========================================================================
    # El WebSocket queda en un bucle infinito procesando mensajes del cliente.
    #
    # Soporta dos acciones:
    #   - subscribe-order:   suscribirse a actualizaciones de un pedido
    #   - unsubscribe-order: desuscribirse de un pedido
    #
    # El bucle se rompe con WebSocketDisconnect (el cliente cerró la conexión)
    # o con cualquier otro error (se limpia la conexión).
    #
    try:
        while True:
            # Espera bloqueante: receive_text() se rompe cuando el cliente envía
            # un mensaje o cuando se desconecta (lanza WebSocketDisconnect)
            raw = await websocket.receive_text()

            # Parsear el mensaje JSON del cliente
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                # Mensaje malformado → ignorar y seguir escuchando
                continue

            action = msg.get("action")

            # ─── ACCIÓN: SUBSCRIBE-ORDER ──────────────────────────────────────
            # El cliente quiere suscribirse a las actualizaciones de un pedido.
            #
            # Para clientes (role:user):
            #   1. Valida que el pedido exista
            #   2. Valida que el pedido pertenezca al usuario
            #   3. Si es válido, une el socket a "order:{orderId}"
            #
            # Para staff (admin/pedidos/cocina):
            #   Se suscribe directamente (el staff puede ver cualquier pedido)
            #
            if action == "subscribe-order":
                order_id = msg.get("order_id")
                if not order_id or not isinstance(order_id, int):
                    continue

                # Validación de propiedad: solo para clientes (no staff)
                # Los staff pueden ver todos los pedidos
                if not any(r in ("ADMIN", "PEDIDOS", "COCINA") for r in user_roles_upper):
                    with UnitOfWork() as uow:
                        pedido = uow.pedidos.get_by_id(order_id)

                        # Validar que:
                        #   a. El pedido exista
                        #   b. El pedido pertenezca al usuario autenticado
                        if not pedido or pedido.usuario_id != user_id:
                            await websocket.send_json({
                                "event": "ERROR",
                                "data": {"detail": "No autorizado para este pedido"}
                            })
                            continue

                # Todo válido → unir el socket a la room del pedido
                manager.join_order_room(websocket, order_id)

                # Confirmar al cliente que se suscribió exitosamente
                await websocket.send_json({
                    "event": "SUBSCRIBED",
                    "data": {"order_id": order_id}
                })

            # ─── ACCIÓN: UNSUBSCRIBE-ORDER ────────────────────────────────────
            # El cliente deja de escuchar un pedido específico.
            #
            elif action == "unsubscribe-order":
                order_id = msg.get("order_id")
                if order_id and isinstance(order_id, int):
                    manager.leave_order_room(websocket, order_id)

    except WebSocketDisconnect:
        # El cliente cerró la conexión limpiamente
        manager.disconnect(websocket)
    except Exception:
        # Error inesperado → limpiar la conexión
        manager.disconnect(websocket)


@router.post("/{pedido_id}/cancelar", response_model=PedidoPublic)
async def cancelar_pedido_cliente(
    pedido_id: int,
    current_user: Annotated[UsuarioPublico, Depends(get_current_active_user)],
    svc: PedidoService = Depends(get_pedido_service),
) -> PedidoPublic:
    """
    Cancelación de pedido por el cliente.
    Solo permite cancelar pedidos propios en estado PENDIENTE o CONFIRMADO.
    """
    return await svc.cancelar_pedido_cliente(pedido_id, current_user)
