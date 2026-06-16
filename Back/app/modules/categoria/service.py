from typing import Optional, List
from fastapi import HTTPException, status
from app.modules.categoria.schema import CategoriaCreate, CategoriaList, CategoriaRead, CategoriaResponse, CategoriaUpdate
from app.modules.categoria.model import Categoria
from app.core.uow import UnitOfWork

class CategoriaService:
    def crear_categoria(self, categoria: CategoriaCreate):
        with UnitOfWork() as uow:
            if categoria.categoria_padre_id is not None:
                padre = uow.categorias.get_by_id(categoria.categoria_padre_id)
                if not padre:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Categoría padre no encontrada"
                    )
                if padre.categoria_padre_id is not None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="La categoría padre no puede ser una subcategoría (solo se permite un nivel)"
                    )

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
                categoria_existente.categoria_padre_id = categoria.categoria_padre_id
                categoria_existente.disponible =True
                print("Actualizando categoría existente:")
                uow.categorias.update(categoria_existente)
                return CategoriaRead.model_validate(categoria_existente)
            
            print("Creando nueva categoría:")
            nueva_categoria = Categoria(**categoria.model_dump())
            uow.categorias.create(nueva_categoria)
            return CategoriaRead.model_validate(nueva_categoria)

    def listar_categorias(self, offset : int = 0, limit : int = 100) -> CategoriaList:
        with UnitOfWork() as uow:
            total = uow.categorias.count()
            categorias = uow.categorias.get_all(offset=offset, limit=limit)
            data = [CategoriaResponse.model_validate(cat) for cat in categorias]

            return CategoriaList(
                data=data,
                count=total)
        




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

            datos = categoria.model_dump(exclude_unset=True)

            if "categoria_padre_id" in datos:
                nuevo_padre_id = datos["categoria_padre_id"]
                if nuevo_padre_id is not None:
                    if nuevo_padre_id == categoria_id:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Una categoría no puede ser su propio padre"
                        )
                    padre = uow.categorias.get_by_id(nuevo_padre_id)
                    if not padre:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="Categoría padre no encontrada"
                        )
                    if padre.categoria_padre_id is not None:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="La categoría padre no puede ser una subcategoría"
                        )
                    if categoria_existente.subcategorias:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Una categoría con subcategorías no puede tener padre"
                        )

            for key, value in datos.items():
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
            
            # Soft delete en cascada de subcategorías
            for sub in categoria.subcategorias:
                sub.disponible = False
                uow.categorias.update(sub)
            
            uow.categorias.delete(categoria.id)
            
            return True


categoria_service = CategoriaService()