from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field
from app.core.simple_schemas import ProductoSimple

class CategoriaBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=100)
    descripcion: Optional[str] = Field(min_length=3, max_length=250)

class CategoriaCreate(CategoriaBase):
    categoria_padre_id: Optional[int] = None

class CategoriaUpdate(SQLModel):
    nombre: Optional[str] = Field(default=None, min_length=3, max_length=100)
    descripcion: Optional[str] = Field(default=None, min_length=3, max_length=250)
    categoria_padre_id: Optional[int] = None

class CategoriaSimple(SQLModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}

class CategoriaResponse(CategoriaBase):
    id: int
    categoria_padre_id: Optional[int] = None
    categoria_padre: Optional[CategoriaSimple] = None
    subcategorias: list[CategoriaSimple] = Field(default_factory=list)
    productos: list[ProductoSimple] = Field(default_factory=list)
    model_config = {"from_attributes": True}

class CategoriaList(SQLModel):
    data: List[CategoriaResponse]
    count: int

class CategoriaRead(CategoriaBase):
    id: int
    categoria_padre_id: Optional[int] = None
    subcategorias: list[CategoriaSimple] = Field(default_factory=list)

    model_config = {"from_attributes": True}

