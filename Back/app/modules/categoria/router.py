from typing import List, Annotated
from fastapi import APIRouter, HTTPException, Query, status
from app.modules.categoria.service import categoria_service

from app.modules.categoria.schema import CategoriaCreate, CategoriaList, CategoriaRead, CategoriaResponse, CategoriaUpdate

router = APIRouter(prefix="/categorias", tags=["categorias"])

@router.get("/", response_model=CategoriaList)
def listar_categorias(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100
):
    return categoria_service.listar_categorias(offset, limit)

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def get_categoria(categoria_id: int):
    return categoria_service.obtener_categoria_por_id(categoria_id)

@router.post("/", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED )
def crear_categoria(categoria: CategoriaCreate):
    return categoria_service.crear_categoria(categoria)

@router.put("/{categoria_id}", response_model=CategoriaRead)
def update_categoria(categoria_id: int, categoria: CategoriaUpdate):
    return categoria_service.actualizar_categoria(categoria_id, categoria)

@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categoria(categoria_id: int):
    return categoria_service.eliminar_categoria(categoria_id)