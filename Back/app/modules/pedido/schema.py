



from decimal import Decimal


from sqlmodel import Field, SQLModel

from app.detallepedido.model import DetallePedido
from app.detallepedido.schema import DetallePedidoCreate, DetallePedidoRead


class PedidoBase(SQLModel):
    
    direccion_id: int
    forma_pago_codigo: str
    descuento: Decimal
    notas: str | None = None

class PedidoCreate(PedidoBase):
    detalles: list[DetallePedidoCreate]

class PedidoPublic(PedidoBase):
    id: int
    usuario_id: int
    estado_codigo: str
    subtotal: Decimal
    costo_envio: Decimal
    total: Decimal

    model_config = {"from_attributes": True}

class PedidoRead(PedidoPublic):
    detalles: list[DetallePedidoRead] = []

class PedidoList(SQLModel):
    data: list[PedidoPublic]
    count: int

class PedidoEstadoUpdate(SQLModel):

    nuevo_estado: str = Field(min_length=1, max_length=50)
    motivo: str | None = Field(default=None, max_length=200)