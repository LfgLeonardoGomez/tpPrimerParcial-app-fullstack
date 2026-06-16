
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class PagoBase(SQLModel):
    pass

class PagoCreate(SQLModel):
    pedido_id: int

class PagoPublic(SQLModel):

    id: int
    pedido_id: int
    monto: float
    estado: str
    mp_preference_id: Optional[str]
    mp_init_point: Optional[str]
    mp_status: Optional[str]
    created_at: datetime

class PagoEstadoResponse(SQLModel):
    pago_id: int
    pedido_id: int
    mp_status: str
    mp_payment_id: Optional[int]

class PagoUpdate(SQLModel):
    
    estado: Optional[str] = None
    mp_payment_id: Optional[int] = None
    mp_status: Optional[str] = None
    mp_status_detail: Optional[str] = None

class ConfirmPagoRequest(SQLModel):
    pedido_id: int
    payment_id: Optional[int]