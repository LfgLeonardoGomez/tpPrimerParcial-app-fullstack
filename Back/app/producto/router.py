from typing import List, Annotated
from fastapi import APIRouter,HTTPException, status, Query, Depends
from app.producto.service import ProductoService
from app.core.deps import require_role
from app.producto.schema import ProductoCategoriasUpdate, ProductoCreate, ProductoIngredientesUpdate, ProductoList, ProductoRead, ProductoResponse, ProductoStockUpdate, ProductoUpdate

router = APIRouter(prefix="/productos", tags=["productos"])

@router.get("/", response_model=ProductoList)
def listar_productos(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100
):
    return ProductoService().listar_productos(offset, limit)

@router.get("/{producto_id}", response_model=ProductoResponse)
def get_producto(producto_id: int):
    return ProductoService().obtener_producto_por_id(producto_id)

@router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate):  
    return ProductoService().crear_producto(producto)

@router.put("/{producto_id}", response_model=ProductoRead)
def update_producto(producto_id: int, producto: ProductoUpdate):
    return ProductoService().actualizar_producto(producto_id, producto)

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(producto_id: int):
    return ProductoService().eliminar_producto(producto_id)

@router.patch(
    "/{producto_id}/stock",
    response_model=ProductoRead,
    dependencies=[Depends(require_role(["ADMIN", "STOCK"]))]
)
def update_stock_producto(producto_id: int, data: ProductoStockUpdate):
    return ProductoService().actualizar_stock_producto(producto_id, data)

@router.put("/{producto_id}/categorias", response_model=ProductoRead)
def update_producto_categorias(producto_id: int, data: ProductoCategoriasUpdate):
    return ProductoService().actualizar_categorias_producto(producto_id, data.categorias)

@router.put("/{producto_id}/ingredientes", response_model=ProductoRead)
def update_producto_ingredientes(producto_id: int, data: ProductoIngredientesUpdate):
    return ProductoService().actualizar_ingredientes_producto(producto_id, data.ingredientes)