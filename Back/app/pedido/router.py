


from typing import Annotated

from fastapi import APIRouter

from app.core.deps import get_current_active_user, require_role
from app.pedido.schema import PedidoCreate, PedidoList, PedidoRead
from app.pedido.service import PedidoService
from fastapi import APIRouter, Depends, Response, status

from app.usuarios.model import Usuario

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

service = PedidoService()

# crear

@router.post("/", response_model = PedidoRead, status_code= status.HTTP_201_CREATED)
def crear_pedido(
    pedido: PedidoCreate,
    usuario: Annotated[Usuario, Depends(get_current_active_user)]
):
    return service.crear_pedido(usuario.id, pedido)

# traer pedidos de el usuario autenticado

@router.get("/pedidosdelusuario", response_model = PedidoList, status_code = status.HTTP_200_OK)
def traer_pedidos_por_cliente(
    usuario: Annotated[Usuario, Depends(get_current_active_user)]
):
    return service.traer_pedidos_por_cliente(usuario.id)

# traer todos los pedidos - solo admin

@router.get("/", response_model = PedidoList, status_code = status.HTTP_200_OK)
def traer_todos(admin: Annotated[Usuario, Depends(require_role(["ADMIN", "PEDIDOS"]))]):
    return service.traer_todos_los_pedidos()

# traer pedidos por estado

@router.get("/admin/estado/{estado}", response_model = PedidoList, status_code = status.HTTP_200_OK)
def traer_pedidos_por_estado(
    estado: str,
    admin: Annotated[Usuario,Depends(require_role(["ADMIN", "PEDIDOS"]))]
    ):
    return service.traer_pedidos_por_estado(estado)

# traer pedidos del cliente autenticado por estado

@router.get("/estado/{estado}", response_model = PedidoList, status_code = status.HTTP_200_OK)
def traer_pedidos_por_estado_del_usuario(
    estado: str,
    usuario: Annotated[Usuario, Depends(get_current_active_user)]
):
    return service.traer_pedidos_por_estado_por_cliente(usuario.id, estado)

# traer pedido por ID

@router.get("/{pedido_id}", response_model=PedidoRead, status_code=status.HTTP_200_OK)
def traer_pedido_por_id(
    pedido_id: int,
    usuario: Annotated[Usuario, Depends(get_current_active_user)]
):
    return service.traer_pedido_por_id(pedido_id, usuario)