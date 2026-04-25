from sqlmodel import SQLModel

class CategoriaSimple(SQLModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}


class ProductoSimple(SQLModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}

class IngredienteSimple(SQLModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}