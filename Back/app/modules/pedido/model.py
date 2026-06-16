from decimal import Decimal

from fastapi import HTTPException, status
from sqlmodel import Field, Relationship, SQLModel

from app.detallepedido.model import DetallePedido
from app.modules.direccioentrega.model import DireccionEntrega
from app.historialestadopedido.model import HistorialEstadoPedido
from app.modules.usuarios.model import Usuario

TRANSICIONES_VALIDAS: dict[str, dict[str, set[str]]] = {
    "ADMIN": {
        "PENDIENTE": {"CONFIRMADO", "CANCELADO"},
        "CONFIRMADO": {"EN_PREP", "CANCELADO"},
        "EN_PREP": {"LISTO", "CANCELADO"},
        "LISTO": {"ENTREGADO", "CANCELADO"},
        "ENTREGADO": set(),
        "CANCELADO": set(),
    },
    "PEDIDOS": {
        "PENDIENTE": {"CONFIRMADO", "CANCELADO"},
        "CONFIRMADO": {"EN_PREP", "CANCELADO"},
        "EN_PREP": set(),
        "LISTO": {"ENTREGADO"},
        "ENTREGADO": set(),
        "CANCELADO": set(),
    },
    "COCINA": {
        "CONFIRMADO": {"EN_PREP"},
        "EN_PREP": {"LISTO"},
    },
}

ESTADOS_TERMINALES = {"ENTREGADO", "CANCELADO"}
ROLES_CANCELACION_EN_PREP = {"ADMIN", "PEDIDOS"}

class Pedido(SQLModel, table=True):
    __tablename__ = "pedidos"

    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id", nullable=False)
    direccion_id: int = Field(foreign_key="direcciones.id", nullable=False)
    estado_codigo: str = Field(foreign_key="estado_pedido.codigo", nullable=False)
    forma_pago_codigo: str = Field(foreign_key="forma_de_pago.codigo", nullable=False)
    
    #---------------------------------------#
    #     snpshot      #
    #---------------------------------------#
    subtotal: Decimal = Field(nullable=False)
    descuento: Decimal = Field(nullable=False, default=Decimal("0.00"))
    costo_envio: Decimal = Field(nullable=False, default=Decimal("50.00"))
    total: Decimal = Field(nullable=False, ge = 0)

    notas: str | None = Field(default=None)

    detalles: list["DetallePedido"] = Relationship(back_populates="pedido")
    usuario: "Usuario" = Relationship(back_populates="pedidos")
    direccion: "DireccionEntrega" = Relationship(back_populates="pedidos")
    historial_estado: list["HistorialEstadoPedido"] = Relationship(back_populates="pedido")


    def cambiar_estado(
        self,
        estado_hacia: str,
        roles: list[str],
        motivo: str | None = None,
    ) -> str | None:
        estado_desde = self.estado_codigo.upper() if self.estado_codigo else None
        estado_hacia = estado_hacia.upper()

        self._validar_transicion(
            estado_desde=estado_desde,
            estado_hacia=estado_hacia,
            roles=roles,
        )

        if estado_hacia == "CANCELADO" and not motivo:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El motivo es obligatorio para cancelar un pedido.",
            )

        self.estado_codigo = estado_hacia

        return estado_desde

    def _validar_transicion(
        self,
        estado_desde: str | None,
        estado_hacia: str,
        roles: list[str],
    ) -> None:
        if estado_desde in ESTADOS_TERMINALES:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El pedido está en estado terminal '{estado_desde}' y no puede cambiar.",
            )

        transiciones_permitidas = set()

        for rol in roles:
            transiciones_por_estado = TRANSICIONES_VALIDAS.get(rol, {})
            transiciones_permitidas |= transiciones_por_estado.get(estado_desde, set())

        if estado_hacia not in transiciones_permitidas:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Transición inválida: '{estado_desde}' → '{estado_hacia}'. "
                    f"Transiciones permitidas: {transiciones_permitidas}."
                ),
            )

        if (
            estado_desde == "PREPARANDO"
            and estado_hacia == "CANCELADO"
            and not any(r in ROLES_CANCELACION_EN_PREP for r in roles)
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Solo un administrador o pedidos puede cancelar un pedido en estado '{estado_desde}'.",
            )