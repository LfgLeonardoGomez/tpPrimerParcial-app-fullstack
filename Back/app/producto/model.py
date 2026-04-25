from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

from app.core.audit import AuditMixin
from app.core.models import ProductoCategoria, ProductoIngrediente
from app.ingrediente.model import Ingrediente

if TYPE_CHECKING:
    from app.categoria.model import Categoria

class Producto(AuditMixin, table=True):
    __tablename__ = "productos"
    id: Optional[int] = Field (default=None, primary_key=True)
    nombre: str = Field (min_length=1, max_length=100, index=True, nullable=False)
    descripcion: Optional[str] = Field (default=None, min_length=3, max_length=255)
    precio_base: str = Field (min_length=1, max_length=50)
    imagen_url: Optional[str] = Field (default=None, max_length=500)
    stock_cantidad: Optional[int] = Field(default=0, ge=0, nullable=False)
    disponible: bool = Field (default=True)

    categorias: List["Categoria"] = Relationship(back_populates="productos",
                link_model=ProductoCategoria)
    
    ingredientes: list["Ingrediente"] = Relationship(back_populates="productos",
                link_model=ProductoIngrediente
)