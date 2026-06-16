from typing import Optional, List, TYPE_CHECKING

from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Relationship

from app.core.audit import AuditMixin
from app.core.models import ProductoCategoria

if TYPE_CHECKING:
    from app.modules.producto.model import Producto

class Categoria(AuditMixin, table = True):
    __tablename__ = "categorias"
    id: Optional[int] = Field (default=None, primary_key=True)
    nombre: str = Field (min_length=1, max_length=100, index=True, nullable=False)
    descripcion: Optional[str] = Field (default=None, max_length=255)
    disponible: bool = Field (default=True)
    categoria_padre_id: Optional[int] = Field(default=None, foreign_key="categorias.id")

    categoria_padre: Optional["Categoria"] = Relationship(
        back_populates="subcategorias",
        sa_relationship_kwargs={"remote_side": "Categoria.id"}
    )
    subcategorias: List["Categoria"] = Relationship(back_populates="categoria_padre")

    productos: List["Producto"] = Relationship(back_populates="categorias",
                link_model=ProductoCategoria)
