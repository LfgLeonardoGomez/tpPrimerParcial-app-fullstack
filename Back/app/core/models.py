from typing import Optional
from sqlmodel import Field, SQLModel

class ProductoCategoria(SQLModel, table=True):
    """Tabla intermedia para la relación muchos a muchos entre Productos y Categorías"""
    __tablename__ = "productos_categorias"
    
    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categorias.id", primary_key=True)


class ProductoIngrediente(SQLModel, table=True):
    """Tabla intermedia para la relación muchos a muchos entre Productos e Ingredientes"""
    __tablename__ = "productos_ingredientes"
    
    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    ingrediente_id: int = Field(foreign_key="ingredientes.id", primary_key=True)