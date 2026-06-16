

from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.core.models import UsuarioRol

if TYPE_CHECKING:
    from app.modules.usuarios.model import Usuario


class Rol(SQLModel, table = True):

    __tablename__ = "roles"
    codigo : str = Field(max_length=20, nullable=False, primary_key=True)
    nombre : str = Field(unique=True, nullable=False, min_length=2, max_length=50)
    descripcion : Optional[str] = Field(min_length= 3, max_length= 100, default=None)

    usuarios : List["Usuario"] = Relationship(back_populates="roles",
                                    link_model=UsuarioRol,
                                    sa_relationship_kwargs={
                                        "primaryjoin": "UsuarioRol.rol_codigo==Rol.codigo",
                                        "secondaryjoin": "UsuarioRol.usuario_id==Usuario.id",
                                        "viewonly": True
                                    })