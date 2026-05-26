from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field
from app.core.simple_schemas import CategoriaSimple, IngredienteSimple

class ProductoBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=250)
    precio_base: str = Field(min_length=1, max_length=50)
    imagen_url: Optional[str] = Field(default=None)
    stock_cantidad: Optional[int] = Field(default=0, ge=0)
    disponible: bool = Field(default=True)

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=250)
    precio_base: Optional[str] = Field(default=None, min_length=1, max_length=50)
    imagen_url: Optional[str] = Field(default=None)
    stock_cantidad: Optional[int] = Field(default=0, ge=0)
    disponible: Optional[bool] = None

class ProductoCategoriasUpdate(SQLModel):
    categorias: list[int] = Field(default_factory=list)

class ProductoIngredientesUpdate(SQLModel):
    ingredientes: list[int] = Field(default_factory=list)

class ProductoStockUpdate(SQLModel):
    stock_cantidad: Optional[int] = Field(default=None, ge=0)
    disponible: Optional[bool] = None
    
class ProductoSimple(SQLModel):
    id: int
    nombre: str
    stock_cantidad: int

    model_config = {"from_attributes": True}

class ProductoResponse(ProductoBase):
    id: int
    categorias: list[CategoriaSimple] = Field(default_factory=list)
    ingredientes: list[IngredienteSimple] = Field(default_factory=list)
    stock_cantidad: int
    model_config = {"from_attributes": True}

class ProductoList(SQLModel):
    data: List[ProductoResponse]
    count: int

class ProductoRead(ProductoBase):
    id: int
    stock_cantidad: int

    model_config = {"from_attributes": True}

