

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.core.audit import AuditMixin
if TYPE_CHECKING:
    from app.modules.usuarios.model import Usuario
if TYPE_CHECKING:
    from app.modules.pedido.model import Pedido


class DireccionEntrega(AuditMixin, SQLModel, table = True):
    __tablename__ = "direcciones"
    id : int | None = Field(primary_key=True)

    usuario_id : int = Field(foreign_key = "usuarios.id", nullable=False)
    alias: str = Field(max_length=50)
    linea_1: str = Field(nullable=False)
    linea_2: str = Field()
    ciudad: str = Field(max_length=100, nullable=False)
    provincia: str = Field(max_length=100)
    codigo_postal: str = Field(max_length=10)
    es_principal: bool = Field(nullable=False, default=False)
    disabled: bool = Field(default=False)
    usuario: "Usuario" = Relationship(back_populates="direcciones")
    pedidos: list["Pedido"] = Relationship(back_populates="direccion")

