from fastapi import HTTPException, status

from app.core.uow import UnitOfWork
from app.modules.direccioentrega.model import DireccionEntrega
from app.modules.direccioentrega.schema import (
    DireccionEntregaCreate,
    DireccionEntregaList,
    DireccionEntregaRead,
    DireccionEntregaUpdate,
)


class DireccionEntregaService:

    def crear_direccion(
        self,
        usuario_id: int,
        direccion: DireccionEntregaCreate,
    ) -> DireccionEntregaRead:
        with UnitOfWork() as uow:
            if uow.direcciones.get_by_alias_and_usuario_id(direccion.alias, usuario_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Este alias ya existe",
                )

            if not uow.usuarios.get_by_id(usuario_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No existe el usuario con el id {usuario_id}",
                )

            direccion_db = DireccionEntrega(
                **direccion.model_dump(),
                usuario_id=usuario_id,
            )

            direcciones_usuario = uow.direcciones.get_all_by_usuario_id(usuario_id)
            
            if len(direcciones_usuario.data) == 0:
                direccion_db.es_principal = True

            direccion_creada = uow.direcciones.create(direccion_db)
        
            if direccion_creada.es_principal:
                direccion_creada = uow.direcciones.actualizar_principal(direccion_creada.id)

            return DireccionEntregaRead.model_validate(direccion_creada)

    def listar_direcciones(
        self,
        usuario_id: int,
        offset: int = 0,
        limit: int = 10,
    ) -> DireccionEntregaList:
        with UnitOfWork() as uow:
            direcciones_db = uow.direcciones.get_all_by_usuario_id(usuario_id, offset, limit)

        

            data = [
                DireccionEntregaRead.model_validate(direccion)
                for direccion in direcciones_db.data
            ]

            return DireccionEntregaList(data=data, count=len(data))

    def get_by_id(
        self,
        usuario_id: int,
        direccion_id: int,
    ) -> DireccionEntregaRead:
        with UnitOfWork() as uow:
            direccion_db = self._get_direccion_del_usuario(
                uow,
                usuario_id,
                direccion_id,
            )

            return DireccionEntregaRead.model_validate(direccion_db)

    def actualizar_direccion(
        self,
        usuario_id: int,
        direccion_id: int,
        direccion: DireccionEntregaUpdate,
    ) -> DireccionEntregaRead:
        with UnitOfWork() as uow:
            direccion_db = self._get_direccion_del_usuario(
                uow,
                usuario_id,
                direccion_id,
            )

            for key, value in direccion.model_dump(exclude_unset=True).items():
                setattr(direccion_db, key, value)

            direccion_actualizada = uow.direcciones.update(
                direccion_id,
                direccion_db,
            )

            return DireccionEntregaRead.model_validate(direccion_actualizada)

    def actualizar_principal(
        self,
        usuario_id: int,
        direccion_id: int,
    ) -> DireccionEntregaRead:
        with UnitOfWork() as uow:
            self._get_direccion_del_usuario(
                uow,
                usuario_id,
                direccion_id,
            )

            direccion_actualizada = uow.direcciones.actualizar_principal(
                direccion_id,
            )

            return DireccionEntregaRead.model_validate(direccion_actualizada)

    def eliminar_direccion(
        self,
        usuario_id: int,
        direccion_id: int,
    ) -> None:
        with UnitOfWork() as uow:
            self._get_direccion_del_usuario(
                uow,
                usuario_id,
                direccion_id,
            )

            uow.direcciones.delete(direccion_id)

    def _get_direccion_del_usuario(
        self,
        uow: UnitOfWork,
        usuario_id: int,
        direccion_id: int,
    ) -> DireccionEntrega:
        direccion = uow.direcciones.get_by_id(direccion_id)

        if not direccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dirección no encontrada",
            )

        if direccion.usuario_id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tenés permiso para acceder a esta dirección",
            )

        return direccion


direccionEntrega_service = DireccionEntregaService()
