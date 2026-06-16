import logging
import uuid
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.uow import UnitOfWork
from app.pago.model import Pago
from app.pago.schema import PagoEstadoResponse, PagoPublic

logger = logging.getLogger(__name__)


class PagoService:
    # =========================================================================
    # CREAR PAGO (preferencia MP)
    # =========================================================================

    def crear_pago(self, pedido_id: int) -> PagoPublic:
        with UnitOfWork() as uow:
            pedido = uow.pedidos.get_by_id(pedido_id)
            if not pedido:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Pedido no encontrado"
                )

            if pedido.estado_codigo == "pagado":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El pedido ya está pagado"
                )

            if not settings.MP_ACCESS_TOKEN:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="MercadoPago no configurado. Configure MP_ACCESS_TOKEN"
                )
            
            ngrok_url = settings.NGROK_URL or "http://localhost:8000"
            back_urls = {
                "success": f"{ngrok_url}/pagos/redirect/{pedido_id}/success",
                "failure": f"{ngrok_url}/pagos/redirect/{pedido_id}/failure",
                "pending": f"{ngrok_url}/pagos/redirect/{pedido_id}/pending"
            }

            try:
                mp_data = self._crear_preferencia_mp(
                    monto=pedido.total,
                    titulo=f"Pedido #{pedido_id} - FoodStore",
                    pedido_id=pedido_id,
                    back_urls=back_urls
                )
            except Exception as e:
                logger.exception("Error creando preferencia MP")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error al crear preferencia MP: {str(e)}"
                )
            
            pago = Pago(
                pedido_id=pedido_id,
                monto=pedido.total,
                estado="pendiente",
                mp_preference_id=mp_data.get("preference_id"),
                mp_init_point=mp_data.get("init_point"),
                idempotency_key=str(uuid.uuid4())
            )
            pago = uow.pagos.create(pago)
            return PagoPublic.model_validate(pago)

    # =========================================================================
    # WEBHOOK (notificación de MP)
    # =========================================================================

    def procesar_webhook(self, data: dict, query_params: Optional[dict] = None) -> dict:
        logger.info("Webhook recibido: data=%s, qs=%s", data, query_params or {})

        if not data and query_params:
            data = query_params

        topic = data.get("type") or data.get("topic")
        data_id = data.get("data.id") or (data.get("data", {}) or {}).get("id")
        payment_id = data.get("id")

        if not data_id and query_params:
            data_id = query_params.get("data.id") or query_params.get("id")
        if not topic and query_params:
            topic = query_params.get("type") or query_params.get("topic")

        pago_mp_id = payment_id or data_id

        if not pago_mp_id:
            return {"status": "ignored", "reason": "No payment ID found"}
        if topic not in ["payment", "merchant_order"]:
            return {"status": "ignored", "reason": f"Unsupported topic: {topic}"}
        
        try:
            mp_info = self._consultar_pago_mp(int(pago_mp_id))
            estado_mp = mp_info.get("status")

            if estado_mp == "approved":
                nuevo_estado = "aprobado"
            elif estado_mp in ("rejected", "cancelled", "refunded", "charged_back"):
                nuevo_estado = "rechazado" 
            elif estado_mp in ("pending", "in_process", "authorized"):
                nuevo_estado = "pendiente"
            else:
                return {"status": "ignored", "reason": f"Unknown MP status: {estado_mp}"}
            
            with UnitOfWork() as uow:
                pago = uow.pagos.get_by_mp_payment_id(int(pago_mp_id))
                if not pago and mp_info.get("merchant_order_id"):
                    pago = uow.pagos.get_by_mp_merchant_order_id(
                        mp_info["merchant_order_id"]
                    )
                if not pago:
                    return {"status": "ignored", "reason": "Pago no encontrado"}
                if pago.estado != "pendiente":
                    return {"status": "already_processed", "estado": pago.estado}

                pago.mp_payment_id = int(pago_mp_id)
                pago.mp_status = estado_mp
                pago.mp_status_detail = mp_info.get("status_detail")
                pago.mp_merchant_order_id = mp_info.get("merchant_order_id")
                pago.estado = nuevo_estado
                pago.updated_at = datetime.now()
                uow.pagos.update(pago)

                if nuevo_estado == "aprobado":
                    pedido = uow.pedidos.get_by_id(pago.pedido_id)
                    if pedido:
                        pedido.estado_codigo = "pagado"
                        pedido.updated_at = datetime.now()
                        uow.pedidos.update(pedido)

            return {
                "status": "processed",
                "pago_id": pago.id,
                "estado": nuevo_estado,
                "pedido_id": pago.pedido_id
            }
        except Exception as e:
            logger.exception("Error procesando webhook MP")
            return {"status": "error", "reason": str(e)}

    # =========================================================================
    # CONFIRMAR PAGO (polling manual)
    # =========================================================================

    def confirmar_pago(self, pedido_id: int, payment_id: Optional[int] = None) -> PagoEstadoResponse:
        with UnitOfWork() as uow:
            pedido = uow.pedidos.get_by_id(pedido_id)
            if not pedido:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pedido no encontrado"
                )
            
            resolved_payment_id = payment_id
            if not resolved_payment_id:
                pago_local = uow.pagos.get_ultimo_by_pedido(pedido_id)
                if pago_local and pago_local.mp_payment_id:
                    resolved_payment_id = pago_local.mp_payment_id
            
            if not resolved_payment_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No se encontró un payment_id para confirmar"
                )
            
            try:
                mp_info = self._consultar_pago_mp(resolved_payment_id)
            except Exception as e:
                logger.exception("Error consultando MP")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error al consultar MercadoPago: {str(e)}"
                )
            
            estado_mp = mp_info.get("status")
            if estado_mp == "approved":
                nuevo_estado = "aprobado"
            elif estado_mp in ("rejected", "cancelled", "refunded", "charged_back"):
                nuevo_estado = "rechazado"
            else:
                nuevo_estado = "pendiente"

            pago = uow.pagos.get_by_mp_payment_id(resolved_payment_id)
            if not pago:
                pago = uow.pagos.get_ultimo_by_pedido(pedido_id)
            if not pago:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pago no encontrado"
                )
            
            pago.mp_payment_id = resolved_payment_id
            pago.mp_status = estado_mp
            pago.mp_status_detail = mp_info.get("status_detail")
            pago.mp_merchant_order_id = mp_info.get("merchant_order_id")
            pago.estado = nuevo_estado
            pago.updated_at = datetime.now()
            uow.pagos.update(pago)

            return PagoEstadoResponse(
                pago_id=pago.id,
                pedido_id=pago.pedido_id,
                mp_status=pago.mp_status,
                mp_payment_id=pago.mp_payment_id
            )

    # =========================================================================
    # INTEGRACIÓN CON MERCADOPAGO 
    # =========================================================================

    def _crear_preferencia_mp(self, monto: float, titulo: str, pedido_id: int, back_urls: dict) -> dict:
        
        import mercadopago

        sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)
        preference_data = {
            "items": [
                {
                    "title": titulo,
                    "quantity": 1,
                    "unit_price": float(monto),
                }
            ],
            "back_urls": back_urls,
            "external_reference": str(pedido_id),
            "auto_return": "approved",  # Si el pago es aprobado, redirige automáticamente a success
        }
        
        response = sdk.preference().create(preference_data)
        response_body = response.get("response", {})
        
        if not response_body or "id" not in response_body:
            raise RuntimeError(f"MercadoPago no devolvió preference_id: {response}")
        
        return {
            "preference_id": response_body["id"],
            "init_point": response_body["init_point"],
        }


    def _consultar_pago_mp(self, payment_id: int) -> dict:
    
        import mercadopago

        sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)
        response = sdk.payment().get(payment_id)
        response_body = response.get("response", {})
        
        if not response_body or "status" not in response_body:
            raise RuntimeError(f"MercadoPago no devolvió datos del pago: {response}")
        
        return {
            "status": response_body.get("status"),
            "status_detail": response_body.get("status_detail"),
            "merchant_order_id": response_body.get("order", {}).get("id"),
        }



pagoservice = PagoService()