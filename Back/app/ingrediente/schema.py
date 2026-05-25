from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.core.simple_schemas import ProductoSimple

class IngredienteBase(SQLModel):
    nombre: str = Field(min_length=3, max_length=100)
    descripcion: Optional[str] = Field(min_length=3, max_length=250)
    es_alergeno: bool = Field(default=False)

class IngredienteCreate(IngredienteBase):
    pass

class IngredienteUpdate(SQLModel):
    nombre: Optional[str] = Field(min_length=3, max_length=100)
    descripcion: Optional[str] = Field(min_length=3, max_length=250)
    es_alergeno: Optional[bool] = None

class IngredienteResponse(IngredienteBase):
    id: int
    disponible: bool = Field (default= True)
    productos: List[ProductoSimple] = Field(default_factory=list)

    model_config = {"from_attributes": True}

class IngredienteList(SQLModel):
    data: List[IngredienteResponse]
    count: int

class IngredienteRead(IngredienteBase):
    id: int
    disponible: bool = Field(default= True)
    model_config = {"from_attributes": True}
    