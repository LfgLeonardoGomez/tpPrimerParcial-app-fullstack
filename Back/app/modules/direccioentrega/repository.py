from sqlmodel import Session, select, update

from app.modules.direccioentrega.model import DireccionEntrega
from app.modules.direccioentrega.schema import DireccionEntregaCreate, DireccionEntregaList
from app.modules.usuarios.model import Usuario
from app.modules.usuarios.schemas import UsuarioRead


class DireccionEntregaRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, direccion_id: int) -> DireccionEntrega:
        statement = select(DireccionEntrega).where(DireccionEntrega.id==direccion_id,
                                DireccionEntrega.disabled==False)
        return self.session.exec(statement).first()
    
    
    def get_by_alias_and_usuario_id(self, alias: str, usuario_id: int) -> DireccionEntrega | None:
        statement = select(DireccionEntrega).where(DireccionEntrega.alias==alias,
                                DireccionEntrega.usuario_id==usuario_id,
                                DireccionEntrega.disabled==False)
        return self.session.exec(statement).first()
    
    def get_all(self, offset: int = 0, limit: int = 10) -> list[DireccionEntrega]:
        statement = select(DireccionEntrega).where(DireccionEntrega.disabled==False)
        return self.session.exec(statement)
    
    def create(self, direccion: DireccionEntregaCreate) -> DireccionEntrega:
        self.session.add(direccion)
        self.session.flush()
        self.session.refresh(direccion)
        return direccion
    
    def update(self, direccion_id: int, direccion: DireccionEntregaCreate) -> DireccionEntrega:
        # direccion_db = self.get_by_id(direccion_id)
        # if not direccion_db:
        #     raise ValueError(f"Direccion no encontrada para el id : {direccion_id}")
        
        # for key, value in direccion.model_dump(exclude_unset=True).items():
        #     setattr(direccion_db, key, value)

        self.session.add(direccion)
        self.session.flush()
        self.session.refresh(direccion)
        return direccion
    
    def actualizar_principal(self, direccion_id: int) -> None:
        direccion = self.get_by_id(direccion_id)
        if not direccion:
            raise ValueError(f"Direccion no encontrada para el id : {direccion_id}")
        
        self.session.exec(update(DireccionEntrega).where(DireccionEntrega.usuario_id==direccion.usuario_id)
                        .values(es_principal=False))
        
        direccion.es_principal = True

        self.session.add(direccion)
        self.session.flush()
        self.session.refresh(direccion)

        return direccion
    
    def delete(self, direccion_id: DireccionEntrega) -> None:
        direccion = self.get_by_id(direccion_id)
        if not direccion:
            raise ValueError(f"Direccion no encontrada para el id : {direccion_id}")
        
        direccion.disabled = True
        self.session.add(direccion)
        self.session.flush()
        self.session.refresh(direccion)
        return None
    
    def get_all_by_usuario_id(self,usuario_id: int,offset: int = 0,limit: int = 10,
    ) -> DireccionEntregaList:
        statement = (
            select(DireccionEntrega)
            .where(
                DireccionEntrega.usuario_id == usuario_id,
                DireccionEntrega.disabled == False,
            )
            .offset(offset)
            .limit(limit)
        )
        data = list(self.session.exec(statement).all())
        count = len(data)
        return DireccionEntregaList(data=data, count=count)

