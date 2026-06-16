


from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.rol.model import Rol
from app.modules.usuarios.model import Usuario
from app.modules.usuarios.schemas import UsuarioCreate


class UsuarioRepository:

    def __init__(self, session: Session):
        self.session = session


    def get_by_id(self, usuario_id: int) -> Usuario:
        statement = select(Usuario).where(Usuario.id == usuario_id,
                            Usuario.disabled == False).options(selectinload(Usuario.roles)
                            )
        
        return self.session.exec(statement).first()
    
    def get_by_email(self, email: str) -> Usuario:
        statement = select(Usuario).where(Usuario.email == email, 
                            Usuario.disabled == False).options(selectinload(Usuario.roles)
                            )
        return self.session.exec(statement).first()
    

    def get_all(self, offset: int = 0, limit: int = 100) -> list[Usuario]:
        statement = select(Usuario).where(Usuario.disabled == False).offset(offset).limit(limit).options(selectinload(Usuario.roles)
                            )
        return self.session.exec(statement).all()
    

    def create(self, usuario: UsuarioCreate) -> Usuario:
        self.session.add(usuario)
        self.session.flush()
        self.session.refresh(usuario)
        return usuario
    

    def update(self, usuario: Usuario) -> Usuario:
        self.session.add(usuario)
        self.session.flush()
        self.session.refresh(usuario)
        return usuario
    

    def delete(self, usuario_id: int) -> None:
        usuario = self.get_by_id(usuario_id)
        if not usuario:
            raise ValueError(f"Usuario con id {usuario_id} no encontrado")
        usuario.disabled = True
        self.session.add(usuario)
        self.session.flush()
        self.session.refresh(usuario)
        return usuario
    
    def actualizar_roles(self, usuario: Usuario, roles: list[Rol]) -> Usuario:
        usuario.roles = roles
        self.session.add(usuario)
        self.session.flush()
        self.session.refresh(usuario)
        return usuario

    def get_by_id_including_disabled(self, usuario_id: int) -> Usuario | None:
        statement = select(Usuario).where(Usuario.id == usuario_id)
        return self.session.exec(statement).first()
