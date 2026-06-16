

from sqlmodel import select

from app.historialestadopedido.model import HistorialEstadoPedido


class HistorialEstadoPedidoRepository:
    
    def __init__(self, session):
        self.session = session

    def create(self, historial_pedido_estado):
        self.session.add(historial_pedido_estado)
        self.session.flush()
        self.session.refresh(historial_pedido_estado)
        return historial_pedido_estado
    
    def get_by_id(self, historial_pedido_estado_id):
        statement = select(HistorialEstadoPedido).where(HistorialEstadoPedido.id == historial_pedido_estado_id)
        return self.session.exec(statement).first()
    
    def get_by_pedido_id(self, pedido_id: int):
        historial = self.session.query(HistorialEstadoPedido).filter(
            HistorialEstadoPedido.pedido_id == pedido_id
        ).order_by(HistorialEstadoPedido.created_at).all()
        return historial