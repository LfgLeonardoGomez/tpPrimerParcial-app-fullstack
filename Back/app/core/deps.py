"""
Dependencias de autenticación y autorización para inyectar vía Depends().

Flujo de resolución:
    Request
→ oauth2_scheme extrae el Bearer token del header Authorization
→ get_current_user abre un UoW, decodifica el JWT, carga el usuario
→ get_current_active_user verifica que disabled=False
→ require_role([...]) verifica que el rol del usuario esté permitido

Separación semántica de errores HTTP:
    401 = no autenticado (sin token / token inválido / expirado)
    403 = autenticado pero sin permisos (rol insuficiente)

Capa: Core (dependencias transversales)
Conoce a: UoW, Security, Model
"""

from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer


from app.core.security import decode_access_token
from app.core.uow import UnitOfWork, get_uow
from app.modules.usuarios.model import Usuario
from app.modules.usuarios.schemas import UsuarioPublico


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    """
    Extensión de OAuth2PasswordBearer que también busca el token en cookies.

    Esto permite soportar clientes que no pueden enviar headers Authorization,
    como navegadores con autenticación basada en cookies.
    """
    async def __call__(self, request: Request) -> str | None:
        token= request.cookies.get("access_token")
        if not token: 
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="No se proporcionó un token de autenticación",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return token

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> Usuario:
    """Decodifica el JWT y retorna el Usuario correspondiente."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str | None = payload.get("sub")
    if email is None:
        raise credentials_exception

    
    user = uow.usuarios.get_by_email(email)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[Usuario, Depends(get_current_user)],
) -> Usuario:
    """Verifica que el usuario autenticado no esté desactivado."""
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cuenta de usuario desactivada",
        )
    return current_user


def require_role(allowed_roles: list[str]):
    """
    Factory de dependencias para control de acceso basado en roles (RBAC).

    Uso:
        @router.get("/admin/...", dependencies=[Depends(require_role(["admin"]))])
    """
    async def role_checker(
        current_user: Annotated[Usuario, Depends(get_current_active_user)],
    ) -> Usuario:
        user_roles = [rol.codigo for rol in current_user.roles]

        if not any (role in allowed_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Permisos insuficientes. Tu rol es '{current_user.roles}'. "
                    f"Se requiere uno de: {allowed_roles}"
                ),
            )
        return current_user

    return role_checker
