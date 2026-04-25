from typing import Optional, List
from fastapi import HTTPException, status
from app.producto.schema import ProductoCreate, ProductoList, ProductoRead, ProductoResponse, ProductoUpdate
from app.producto.model import Producto
from app.core.uow import UnitOfWork

class ProductoService:

    def crear_producto(self, producto: ProductoCreate):
        with UnitOfWork() as uow:
            producto_existente = uow.productos.get_by_nombre(producto.nombre)

            if producto_existente:
                if producto_existente.disponible:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Ya existe un producto con ese nombre"
                        )
            
                producto_existente.descripcion = producto.descripcion
                producto_existente.precio_base = producto.precio_base
                producto_existente.imagen_url = producto.imagen_url
                producto_existente.stock_cantidad = producto.stock_cantidad
                producto_existente.disponible = True
                print("Actualizando producto existente:")
                uow.productos.update(producto_existente)
                return ProductoRead.model_validate(producto_existente)

            nueva_producto = Producto(**producto.model_dump())
            uow.productos.create(nueva_producto)
            return ProductoRead.model_validate(nueva_producto)

    def listar_productos(self, offset : int = 0, limit : int = 100) -> ProductoList:
        with UnitOfWork() as uow:
            productos = uow.productos.get_all(offset=offset, limit=limit)
            data = [ProductoResponse.model_validate(prod) for prod in productos]
            return ProductoList(
                data=data,
                count=len(data)
            )

    def obtener_producto_por_id(self, producto_id: int) -> ProductoResponse:
        with UnitOfWork() as uow:
            producto = uow.productos.get_by_id(producto_id)
            if not producto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Producto no encontrado"
                )
            return ProductoResponse.model_validate(producto)
        
    def actualizar_producto(self, producto_id: int, producto: ProductoUpdate) -> ProductoRead:
        with UnitOfWork() as uow:
            producto_existente = uow.productos.get_by_id(producto_id)
            if not producto_existente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Producto no encontrado"
                )
            for key, value in producto.model_dump(exclude_unset=True).items():
                setattr(producto_existente, key, value)
            uow.productos.update(producto_existente)
            return ProductoRead.model_validate(producto_existente)
        
    def eliminar_producto(self, producto_id: int) -> bool:
        with UnitOfWork() as uow:
            producto = uow.productos.get_by_id(producto_id)
            if not producto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Producto no encontrado"
                )
            uow.productos.delete(producto.id)
            return True
        

    def actualizar_categorias_producto(self, producto_id: int, categorias: List[int]) -> ProductoRead:
        with UnitOfWork() as uow:
            producto = uow.productos.get_by_id(producto_id)
            if not producto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Producto no encontrado"
                )
            categorias_encontradas = []
            for categoria_id in categorias:
                categoria = uow.categorias.get_by_id(categoria_id)
                if not categoria:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Categoria con id {categoria_id} no encontrada"
                    )
                categorias_encontradas.append(categoria)

            producto_actualizado : Producto = uow.productos.update_categorias(producto, categorias_encontradas)
            return ProductoRead.model_validate(producto_actualizado)
        
    def actualizar_ingredientes_producto(self, producto_id: int, ingredientes: List[int]) -> ProductoRead:
        with UnitOfWork() as uow:
            producto = uow.productos.get_by_id(producto_id)
            if not producto:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Producto no encontrado"
                    )
            ingredientes_encontrados = []
            for ingrediente_id in ingredientes:
                    ingrediente = uow.ingredientes.get_by_id(ingrediente_id)
                    if not ingrediente:
                        raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Ingrediente no encontrado"
                    )
                    ingredientes_encontrados.append(ingrediente)

            producto_actualizado : Producto = uow.productos.update_ingredientes(producto, ingredientes_encontrados)
            return ProductoRead.model_validate(producto_actualizado)

producto_service = ProductoService()