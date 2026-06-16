from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

from app.core.audit import AuditMixin
from app.core.models import ProductoIngrediente
if TYPE_CHECKING:
    from app.modules.producto.model import Producto

class Ingrediente(AuditMixin, table=True):
    __tablename__ = "ingredientes"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=1, max_length=100, index=True, nullable=False)
    descripcion: Optional[str] = Field(default=None, min_length=3, max_length=255)
    es_alergeno: bool = Field(default=False)
    disponible: bool = Field(default=True)
    productos: List["Producto"] = Relationship(back_populates="ingredientes", 
                link_model=ProductoIngrediente)
