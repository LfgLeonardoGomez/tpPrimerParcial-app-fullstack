
from datetime import datetime
from typing import Optional
from sqlmodel import BigInteger, SQLModel, Field

class Pago(SQLModel, table=True):

    __tablename__ = "pagos"
    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedidos.id", index=True)
    monto: float = Field(ge=0)
    estado: str =Field(max_length=20)

    mp_preference_id: Optional[str] = Field(default=None, max_length=255)
    mp_init_point: Optional[str] = Field(default=None, max_length=500)
    mp_payment_id: Optional[int] = Field(default=None, sa_type=BigInteger)
    mp_merchant_order_id: Optional[int] = Field(default=None, sa_type=BigInteger)
    mp_status: Optional[str] = Field(default=None, max_length=50)
    mp_status_detail: Optional[str] = Field(default=None, max_length=255)

    idempotency_key: str = Field(max_length=255, unique=True, index=True)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)