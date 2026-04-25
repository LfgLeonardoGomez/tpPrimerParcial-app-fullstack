from typing import Optional, List
from fastapi import HTTPException, status
from app.categoria.schema import CategoriaCreate, CategoriaList, CategoriaRead, CategoriaResponse, CategoriaUpdate
from app.categoria.model import Categoria
from app.core.uow import UnitOfWork

class CategoriaService:
    def crear_categoria(self, categoria: CategoriaCreate):
        with UnitOfWork() as uow:
            categoria_existente = uow.categorias.get_by_nombre(categoria.nombre)
            print(f"Categoria existente: {categoria_existente}")
            if categoria_existente:
                if categoria_existente.disponible:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Ya existe una categoría con ese nombre"
                        )
            
                categoria_existente.descripcion = categoria.descripcion
                categoria_existente.disponible = True
                print("Actualizando categoría existente:")
                uow.categorias.update(categoria_existente)
                return CategoriaRead.model_validate(categoria_existente)
            
            print("Creando nueva categoría:")
            nueva_categoria = Categoria(**categoria.model_dump())
            uow.categorias.create(nueva_categoria)
            return CategoriaRead.model_validate(nueva_categoria)

    def listar_categorias(self, offset : int = 0, limit : int = 100) -> CategoriaList:
        with UnitOfWork() as uow:
            categorias = uow.categorias.get_all(offset=offset, limit=limit)
            data = [CategoriaResponse.model_validate(cat) for cat in categorias]

            return CategoriaList(
                data=data,
                count=len(data)
        )




    def obtener_categoria_por_id(self, categoria_id: int) -> CategoriaResponse:
        with UnitOfWork() as uow:
            categoria = uow.categorias.get_by_id(categoria_id)
            if not categoria:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Categoría no encontrada"
                )
            return CategoriaResponse.model_validate(categoria)

    def actualizar_categoria(self, categoria_id: int, categoria: CategoriaUpdate) -> CategoriaRead:
        with UnitOfWork() as uow:
            categoria_existente = uow.categorias.get_by_id(categoria_id)
            if not categoria_existente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Categoría no encontrada"
                )
            for key, value in categoria.model_dump(exclude_unset=True).items():
                setattr(categoria_existente, key, value)
            uow.categorias.update(categoria_existente)
            return CategoriaRead.model_validate(categoria_existente)

    def eliminar_categoria(self, categoria_id: int) -> bool:
        with UnitOfWork() as uow:
            categoria = uow.categorias.get_by_id(categoria_id)
            if not categoria:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Categoría no encontrada"
                )
            
            uow.categorias.delete(categoria.id)
            
            return True


categoria_service = CategoriaService()