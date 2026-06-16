from typing import Optional, List
from fastapi import HTTPException, status
from app.modules.ingrediente.model import Ingrediente
from app.modules.ingrediente.schema import IngredienteCreate, IngredienteList, IngredienteRead, IngredienteResponse, IngredienteUpdate
from app.core.uow import UnitOfWork

class IngredienteService:
    def crear_ingrediente(self, ingrediente: IngredienteCreate):
        with UnitOfWork() as uow:
            ingrediente_existente = uow.ingredientes.get_by_nombre(ingrediente.nombre)

            if ingrediente_existente:
                if ingrediente_existente.disponible:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Ya existe un ingrediente con ese nombre"
                        )
            
                ingrediente_existente.descripcion = ingrediente.descripcion
                ingrediente_existente.es_alergeno = ingrediente.es_alergeno
                ingrediente_existente.disponible = True
                print("Actualizando ingrediente existente:")
                uow.ingredientes.update(ingrediente_existente)
                return IngredienteRead.model_validate(ingrediente_existente)

            nuevo_ingrediente = Ingrediente(**ingrediente.model_dump())
            uow.ingredientes.create(nuevo_ingrediente)
            return IngredienteRead.model_validate(nuevo_ingrediente)
        
    def listar_ingredientes(self, offset : int = 0, limit : int = 100) -> IngredienteList:
        with UnitOfWork() as uow:
            ingredientes = uow.ingredientes.get_all(offset=offset, limit=limit)
            data = [IngredienteResponse.model_validate(ing) for ing in ingredientes]
            return IngredienteList(data=data, count=len(data))
        
    def obtener_ingrediente_por_id(self, ingrediente_id: int) -> IngredienteResponse:
        with UnitOfWork() as uow:
            ingrediente = uow.ingredientes.get_by_id(ingrediente_id)
            if not ingrediente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ingrediente no encontrado"
                )
            return IngredienteResponse.model_validate(ingrediente)
        

    def actualizar_ingrediente(self, ingrediente_id: int, ingrediente: IngredienteUpdate) -> IngredienteRead:
        with UnitOfWork() as uow:
            ingrediente_existente = uow.ingredientes.get_by_id(ingrediente_id)
            if not ingrediente_existente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ingrediente no encontrado"
                )
            for key, value in ingrediente.model_dump(exclude_unset=True).items():
                setattr(ingrediente_existente, key, value)
            uow.ingredientes.update(ingrediente_existente)
            return IngredienteRead.model_validate(ingrediente_existente)
        

    def eliminar_ingrediente(self, ingrediente_id: int) -> IngredienteResponse:
        with UnitOfWork() as uow:
            ingrediente = uow.ingredientes.get_by_id(ingrediente_id)
            if not ingrediente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ingrediente no encontrado"
                )
            ingrediente.disponible = False
            uow.ingredientes.update(ingrediente)
            return IngredienteResponse.model_validate(ingrediente)
        
ingrediente_service = IngredienteService()