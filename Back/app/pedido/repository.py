

from sqlmodel import Session, select

from app.pedido.model import Pedido
from app.pedido.schema import PedidoCreate, PedidoList


class PedidoRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, pedido_id: int)-> Pedido:
        statement = select(Pedido).where(Pedido.id == pedido_id)
        return self.session.exec(statement).first()
    
    def get_all(self, offset: int = 0, limit: int = 100) -> list[Pedido]:
        statement = select(Pedido).offset(offset).limit(limit)
        return self.session.exec(statement).all()
    
    def get_by_usuario_id(self, usuario_id: int, offset: int = 0, limit: int = 100) -> list[Pedido]:
        statement = select(Pedido).where(Pedido.usuario_id == usuario_id).order_by(Pedido.id.desc()).offset(offset).limit(limit)
        return self.session.exec(statement).all()
    
    def get_by_estado(self, estado_codigo: str, offset: int = 0, limit: int = 100) -> list[Pedido]:
        statement = select(Pedido).where(Pedido.estado_codigo == estado_codigo).offset(offset).limit(limit)
        return self.session.exec(statement).all()
    
    def get_by_estado_by_usuario_id(self, usuario_id: int, estado_codigo: str, offset: int = 0, limit: int = 100) -> list[Pedido]:
        statement = select(Pedido).where(
            Pedido.usuario_id == usuario_id,
            Pedido.estado_codigo == estado_codigo
        ).offset(offset).limit(limit)
        return self.session.exec(statement).all()
    
    def create(self, pedido_data: dict) -> Pedido:
        pedido = Pedido(**pedido_data)
        self.session.add(pedido)
        self.session.flush()
        self.session.refresh(pedido)
        return pedido
    
    def update(self, pedido: Pedido) -> Pedido:
        self.session.add(pedido)
        self.session.flush()
        self.session.refresh(pedido)
        return pedido