import asyncio
import cloudinary
import cloudinary.uploader
from fastapi import HTTPException, UploadFile, status

from app.core.config import settings
from app.modules.uploads.schemas import CloudinaryResponse

# Configuracion global
# Se ejecuta una vez al importar
# Las credenciales vienen del .env
cloudinary.config(
    cloud_name= settings.cloudinary_cloud_name,
    api_key= settings.cloudinary_api_key,
    api_secret= settings.cloudinary_api_secret,
    secure= True,
)

#Tipos permitidos y tamaño maximo del archivo
ALLOWED_MIME_TYPES= {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE_BYTES = 5 * 1024 * 1024 # 5 MB

class UploadsService:
    async def upload (self, file: UploadFile, folder: str = "foodstore/productos") -> CloudinaryResponse:
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= f"Tipo de archivo no permitido:'{file.content_type}'.Se aceptan: jpeg, png, webp."
            )
        content= await file.read()
        if len(content) > MAX_SIZE_BYTES:
            raise HTTPException (
                status_code= status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
                detail= "El archivo supera el limite de 5 MB",
            )
        # El SDK es sincronico, usamos asyncio
        # Para no bloquear el event loop de FastAPI mientras se sube
        result= await asyncio.to_thread(
            cloudinary.uploader.upload,
            content,
            folder= folder, #carpeta dentro de Cloudinary
            resource_type= "image",
            overwhite= False, #No sobreescribe si existe un nombre igual
            unique_filename= True, # Genera un nombre unico automatico
            allowed_formats= ["jpg", "jpeg", "png", "webp"]
        )
        return CloudinaryResponse(
            secure_url= result["secure_url"],
            public_id= result["public_id"],
            width= result.get("width", 0),
            height= result.get("height", 0),
            format= result.get("format", ""),
            resource_type= result.get("resource_type", "image"),
        )
    def delete(self, public_id: str) -> None:

        #Elimina la imagen usando el public_id
        result= cloudinary.uploader.destroy(public_id, resource_type="image")
        if result.get("result") not in ("ok", "not found"):
            raise HTTPException(
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= "Error al eliminar la imagen"
            )