from typing import Annotated, List

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.limiter import limiter
from app.core.deps import get_current_active_user, require_role
from app.core.uow import UnitOfWork, get_uow
from app.modules.usuarios.model import Usuario
from app.modules.usuarios.schemas import UsuarioCreate, UsuarioList, UsuarioPublico, UsuarioRead, UsuarioUpdate
from app.modules.usuarios.service import UsuarioService


router = APIRouter(prefix="/api/v1", tags=["auth"])

service = UsuarioService()

#-------------------------------#
# Rutas Públicas
#-------------------------------#

@router.post("/register", response_model= UsuarioPublico, status_code= status.HTTP_201_CREATED)
@limiter.limit("100/15minute") 
def register(usuario: UsuarioCreate, request: Request):
    return service.crear_usuario(usuario)


@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("100/15minute") 
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
    response: Response
):
    token = service.autenticar_usuario(form_data.username, form_data.password)
    response.set_cookie(key="access_token",
                        value=token.access_token, 
                        httponly=True, 
                        max_age=token.expires_in,
                        samesite="lax",
                        secure=False)
    return {"mensaje": "Inicio de sesión exitoso"}

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    # Limpiar la cookie HttpOnly al cerrar sesión
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=False,
    )
    return {"mensaje": "Sesión cerrada exitosamente"}

    #-------------------------------#
    # Rutas Protegidas
    #-------------------------------#

@router.get("/me", response_model= UsuarioPublico)
def read_current_user(current_user: Annotated[Usuario, 
                        Depends(get_current_active_user)]):
    return {
        "id": current_user.id,
        "nombre": current_user.nombre,
        "apellido": current_user.apellido,
        "email": current_user.email,
        "celular": current_user.celular,
        "disabled": current_user.disabled,
        "roles": [rol.codigo for rol in current_user.roles]
    }

@router.get("/admin/usuarios", response_model = UsuarioList)
def listar_usuarios(admin: Annotated[Usuario, Depends(require_role(["ADMIN"]))]):
    usuarios = service.traertodos()
    return usuarios

    #Actualiza perfil propio#

@router.put("/usuarios/me", response_model= UsuarioPublico)
def update_usuario(
    usuario_update: UsuarioUpdate,
    current_user: Annotated[Usuario, Depends(get_current_active_user)]
):
    service.es_admin_o_me(current_user, current_user.id)
    return service.actualizar_usuario(current_user.id, usuario_update)

    #Activa o desactva un usuario usuario (solo admin)#

@router.post("/usuarios/{usuario_id}/desactivar", response_model= UsuarioPublico)
def disable_usuario(
    usuario_id: int,
    es_admin: Annotated[Usuario, Depends(require_role(["ADMIN"]))]):
    return service.set_disabled(usuario_id, True)

@router.post("/usuarios/{usuario_id}/reactivar", response_model= UsuarioPublico)
def enable_usuario(
    usuario_id: int,
    es_admin: Annotated[Usuario, Depends(require_role(["ADMIN"]))]):
    return service.set_disabled(usuario_id, False)

    # Admin modifica roles de usuario (solo admin) #

@router.put("/admin/usuarios/{usuario_id}/roles", response_model= UsuarioRead, status_code=status.HTTP_200_OK)
def modificar_roles(
    usuario_id: int,
    roles: list[str],
    es_admin: Annotated[Usuario, Depends(require_role(["ADMIN"]))]):
    return service.modificar_roles(usuario_id, roles)

    # Admin puede ver detalle de un usuario #

@router.get("/admin/usuarios/{usuario_id}", response_model= UsuarioPublico)
def get_usuario(
    usuario_id: int,
    es_admin: Annotated[Usuario, Depends(require_role(["ADMIN"]))]):
    return service.traer_por_id(usuario_id)


