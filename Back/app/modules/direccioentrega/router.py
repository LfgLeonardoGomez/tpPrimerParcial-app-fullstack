from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.core.deps import get_current_active_user
from app.modules.direccioentrega.schema import (
    DireccionEntregaCreate,
    DireccionEntregaList,
    DireccionEntregaRead,
    DireccionEntregaUpdate,
)
from app.modules.direccioentrega.service import DireccionEntregaService
from app.modules.usuarios.model import Usuario


router = APIRouter(prefix="/direcciones", tags=["direcciones"])

service = DireccionEntregaService()


@router.get("/", response_model=DireccionEntregaList)
def listar_direcciones(
    current_user: Annotated[Usuario, Depends(get_current_active_user)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    return service.listar_direcciones(current_user.id, offset, limit)


@router.get("/{direccion_id}", response_model=DireccionEntregaRead)
def get_direccion(
    direccion_id: int,
    current_user: Annotated[Usuario, Depends(get_current_active_user)],
):
    return service.get_by_id(current_user.id, direccion_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=DireccionEntregaRead,
)
def crear_direccion(
    direccion: DireccionEntregaCreate,
    current_user: Annotated[Usuario, Depends(get_current_active_user)],
):
    return service.crear_direccion(current_user.id, direccion)


@router.put("/{direccion_id}", response_model=DireccionEntregaRead)
def actualizar_direccion(
    direccion_id: int,
    direccion: DireccionEntregaUpdate,
    current_user: Annotated[Usuario, Depends(get_current_active_user)],
):
    return service.actualizar_direccion(current_user.id, direccion_id, direccion)


@router.delete("/{direccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_direccion(
    direccion_id: int,
    current_user: Annotated[Usuario, Depends(get_current_active_user)],
):
    service.eliminar_direccion(current_user.id, direccion_id)
    return None


@router.put("/{direccion_id}/principal", response_model=DireccionEntregaRead)
def marcar_direccion_como_principal(
    direccion_id: int,
    current_user: Annotated[Usuario, Depends(get_current_active_user)],
):
    return service.actualizar_principal(current_user.id, direccion_id)