from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column
if TYPE_CHECKING:
    from app.modules.pedido.model import Pedido

class DetallePedido(SQLModel, table = True):
    __tablename__ = "detalle_pedidos"
    pedido_id : int = Field (foreign_key="pedidos.id", primary_key=True)
    producto_id : int = Field (foreign_key="productos.id", primary_key=True)
    cantidad : int = Field (nullable = False, ge = 1)
    ##   snapshot  ##
    nombre_snapshot : str = Field (nullable = False, max_length = 200)
    precio_snapshot : float = Field (nullable = False, ge = 0)
    subtotal_snapshot : float = Field (nullable = False, ge = 0)
    personalizacion : list[list[int]] = Field(default_factory=list, sa_column = Column(JSONB, nullable = False))
    created_at : datetime = Field (default_factory=datetime.now, nullable = False)
    
    pedido: Optional["Pedido"] = Relationship(back_populates="detalles")