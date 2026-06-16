from sqlmodel import Session, select, desc

from app.modules.pago.model import Pago


class PagoRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, pago_id: int) -> Pago | None:
        statement = select(Pago).where(Pago.id == pago_id)
        return self.session.exec(statement).first()

    def get_by_mp_payment_id(self, mp_payment_id: int) -> Pago | None:
        statement = select(Pago).where(Pago.mp_payment_id == mp_payment_id)
        return self.session.exec(statement).first()

    def get_by_mp_merchant_order_id(self, mp_merchant_order_id: int) -> Pago | None:
        statement = select(Pago).where(Pago.mp_merchant_order_id == mp_merchant_order_id)
        return self.session.exec(statement).first()

    def get_ultimo_by_pedido(self, pedido_id: int) -> Pago | None:
        statement = (
            select(Pago)
            .where(Pago.pedido_id == pedido_id)
            .order_by(desc(Pago.created_at))
        )
        return self.session.exec(statement).first()

    def create(self, pago: Pago) -> Pago:
        self.session.add(pago)
        self.session.flush()
        self.session.refresh(pago)
        return pago

    def update(self, pago: Pago) -> Pago:
        self.session.add(pago)
        self.session.flush()
        self.session.refresh(pago)
        return pago