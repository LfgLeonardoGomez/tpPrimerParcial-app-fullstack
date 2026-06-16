from datetime import UTC, datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey



if TYPE_CHECKING:
    from app.modules.pedido.model import Pedido
    from app.estadopedido.model import EstadoPedido
    from app.modules.usuarios.model import Usuario


class HistorialEstadoPedido(SQLModel, table=True):
    __tablename__ = "historial_estados_pedido"

    id: int | None = Field(primary_key=True)


    pedido_id: int = Field(foreign_key="pedidos.id")

    estado_desde: str = Field(foreign_key="estado_pedido.codigo", nullable=True, default= None)

    estado_hacia: str = Field(foreign_key="estado_pedido.codigo", nullable=False, default=None)   

    usuario_id: int = Field(foreign_key="usuarios.id",default=None, nullable=False)

    motivo: str | None = Field(nullable=True, default=None)

    created_at: datetime | None = Field(default_factory=lambda: datetime.now(UTC))


    pedido: Optional["Pedido"] = Relationship(back_populates="historial_estado")
    usuario: Optional["Usuario"] = Relationship(back_populates="historial_estados_pedido")
    
    desde: Optional["EstadoPedido"] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[HistorialEstadoPedido.estado_desde]",
            "lazy": "select"
        }
    )

    hacia: Optional["EstadoPedido"] = Relationship(
        sa_relationship_kwargs={
            "foreign_keys": "[HistorialEstadoPedido.estado_hacia]",
            "lazy": "select"
        }
    )