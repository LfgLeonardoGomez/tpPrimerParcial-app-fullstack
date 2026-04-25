from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field
from app.core.simple_schemas import ProductoSimple

class CategoriaBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=100)
    descripcion: Optional[str] = Field(min_length=3, max_length=250)

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(SQLModel):
    nombre: Optional[str] = Field(min_length=3, max_length=100)
    descripcion: Optional[str] = Field(min_length=3, max_length=250)

class CategoriaSimple(SQLModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}

class CategoriaResponse(CategoriaBase):
    id: int
    productos: list[ProductoSimple] = Field(default_factory=list)
    model_config = {"from_attributes": True}

class CategoriaList(SQLModel):
    data: List[CategoriaResponse]
    count: int

class CategoriaRead(CategoriaBase):
    id: int

    model_config = {"from_attributes": True}

