from typing import Optional

from sqlmodel import SQLModel, Field


class UsuarioBase(SQLModel):

    nombre : str = Field(nullable=False)
    apellido : str = Field(nullable=False)
    email: str
    celular : str = Field(max_length=20)


class UsuarioCreate(UsuarioBase):

    password: str = Field(min_length=8, max_length=72)

class UsuarioUpdate(SQLModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    celular: Optional[str] = None
    password: Optional[str] = None



class UsuarioRead(UsuarioBase):
    id: int
    roles: list[str] = Field(default_factory=list)
    disabled: bool
    
class UsuarioPublico(UsuarioBase):
    id: int
    roles: list[str] = Field(default_factory=list)
    disabled: bool

class UsuarioList(SQLModel):
    data: list[UsuarioPublico]
    count: int
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  