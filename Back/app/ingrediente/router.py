from typing import List, Annotated
from fastapi import HTTPException, Query, status, APIRouter
from app.ingrediente.service import IngredienteService
from app.ingrediente.schema import IngredienteCreate, IngredienteList, IngredienteRead, IngredienteResponse, IngredienteUpdate

router = APIRouter(prefix="/ingredientes", tags=["ingredientes"])

@router.get("/", response_model=IngredienteList)
def listar_ingredientes(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100
):
    return IngredienteService().listar_ingredientes(offset, limit)

@router.get("/{ingrediente_id}", response_model=IngredienteResponse)
def get_ingrediente(ingrediente_id: int):
    return IngredienteService().obtener_ingrediente_por_id(ingrediente_id)

@router.post("/", response_model=IngredienteRead, status_code=status.HTTP_201_CREATED)
def crear_ingrediente(ingrediente: IngredienteCreate):  
    return IngredienteService().crear_ingrediente(ingrediente)

@router.put("/{ingrediente_id}", response_model=IngredienteRead)
def update_ingrediente(ingrediente_id: int, ingrediente: IngredienteUpdate):
    return IngredienteService().actualizar_ingrediente(ingrediente_id, ingrediente)

@router.delete("/{ingrediente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingrediente(ingrediente_id: int):
    return IngredienteService().eliminar_ingrediente(ingrediente_id)
