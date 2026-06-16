from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File

from app.core.deps import require_role
from app.modules.uploads.schemas import CloudinaryResponse
from app.modules.uploads.service import UploadsService
from app.modules.usuarios.schemas import UsuarioPublico

router= APIRouter(prefix= "/api/v1/uploads", tags=["uploads"])

def get_uploads_service() -> UploadsService:
    return UploadsService()

@router.post("/imagen", response_model= CloudinaryResponse, status_code= 201)
async def upload_imagen(
    file: UploadFile = File(...),
    _admin: Annotated[UsuarioPublico, Depends(require_role(["ADMIN"]))] = None,
    svc: UploadsService= Depends(get_uploads_service)
):
    return await svc.upload(file)

@router.delete("/imagen/{public_id:path}", status_code=204)
def delete_imagen(
    public_id: str,
    _admin: Annotated[UsuarioPublico, Depends(require_role(["ADMIN"]))] = None,
    svc: UploadsService= Depends(get_uploads_service)
):
    svc.delete(public_id)
