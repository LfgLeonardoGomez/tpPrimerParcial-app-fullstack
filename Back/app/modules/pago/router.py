import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse

from app.core.config import settings
from app.core.deps import get_current_active_user
from app.modules.pago.schema import ConfirmPagoRequest, PagoCreate, PagoEstadoResponse, PagoPublic
from app.modules.pago.service import PagoService
from app.modules.usuarios.model import Usuario

router = APIRouter(prefix="/pagos", tags=["Pagos"])

service = PagoService()
logger = logging.getLogger(__name__)

def get_pago_service() -> PagoService:
    return service


# =========================================================================
# Crear preferencia de pago (usuario autenticado)
# =========================================================================

@router.post("/create-preference", response_model=PagoPublic, status_code=status.HTTP_201_CREATED)
def create_preference(
    data: PagoCreate,
    current_user: Annotated[Usuario, Depends(get_current_active_user)],
    svc: PagoService = Depends(get_pago_service),
):
    return svc.crear_pago(data.pedido_id)


# =========================================================================
# Webhook — MercadoPago notifica aquí (público, sin auth)
# =========================================================================

@router.post("/webhook")
async def webhook(
    request: Request,
    svc: PagoService = Depends(get_pago_service),
):
    try:
        query_params = dict(request.query_params)
        if request.headers.get("content-type", "").startswith("application/json"):
            data = await request.json()
        else:
            data = dict(await request.form())
        return svc.procesar_webhook(data, query_params=query_params)
    except Exception as e:
        logger.exception("Error en webhook MP")
        return {"status": "error", "reason": str(e)}


# =========================================================================
# Confirmar estado del pago (polling manual)
# =========================================================================

@router.post("/confirm", response_model=PagoEstadoResponse)
def confirm_payment(
    data: ConfirmPagoRequest,
    svc: PagoService = Depends(get_pago_service),
):
    return svc.confirmar_pago(data.pedido_id, data.payment_id)


# =========================================================================
# Redirect — MercadoPago redirige al usuario aquí después del pago
# =========================================================================

@router.get("/redirect/{pedido_id}/{status}")
def redirect_after_pago(
    pedido_id: int,
    status: str,
    request: Request,
):
    frontend_url = settings.VITE_FRONTEND_URL or "http://localhost:5173"
    qs = request.url.query
    url = f"{frontend_url}/orders/{pedido_id}/{status}"
    if qs:
        url += f"?{qs}"
    return RedirectResponse(url=url)