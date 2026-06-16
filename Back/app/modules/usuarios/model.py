from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING, List, Optional


from app.core.audit import AuditMixin
from app.core.models import UsuarioRol
from app.historialestadopedido.model import HistorialEstadoPedido


if TYPE_CHECKING:
    from app.rol.model import Rol
if TYPE_CHECKING:
    from app.modules.direccioentrega.model import DireccionEntrega
if TYPE_CHECKING:
    from app.modules.pedido.model import Pedido

class Usuario (AuditMixin,SQLModel, table = True):
    __tablename__ = "usuarios"
    id:  int | None = Field(default=None, primary_key=True)
    nombre : str = Field(nullable=False)
    apellido : str = Field(nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    celular : str = Field(max_length=20)
    password_hashed: str = Field(nullable=False)
    disabled: bool = Field(default=False)

    roles: List["Rol"] = Relationship(back_populates= "usuarios",
                                    link_model=UsuarioRol,
                                    sa_relationship_kwargs={
                                        "primaryjoin": "UsuarioRol.usuario_id==Usuario.id",
                                        "secondaryjoin": "UsuarioRol.rol_codigo==Rol.codigo"
                                        
                                    })
    
    direcciones: list["DireccionEntrega"] = Relationship(
        back_populates="usuario"
    )

    historial_estados_pedido: list["HistorialEstadoPedido"] = Relationship(
        back_populates="usuario"
    )

    pedidos: list["Pedido"] = Relationship(back_populates="usuario")

