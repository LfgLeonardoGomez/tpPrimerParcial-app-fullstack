

from sqlmodel import SQLModel


class DireccionEntregaBase(SQLModel):
    alias: str
    linea_1: str
    linea_2: str
    ciudad: str
    provincia: str
    codigo_postal: str
    es_principal: bool

class DireccionEntregaCreate(DireccionEntregaBase):
    pass



class DireccionEntregaUpdate(SQLModel):
    alias: str | None = None
    linea_1: str | None = None
    linea_2: str | None = None
    ciudad: str | None = None
    provincia: str | None = None
    codigo_postal: str | None = None
    es_principal: bool | None = None

class DireccionEntregaRead(DireccionEntregaBase):
    id: int

class DireccionEntregaList(SQLModel):
    data: list[DireccionEntregaRead]
    count: int

