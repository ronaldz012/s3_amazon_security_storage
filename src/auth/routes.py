from fastapi import APIRouter, Depends, status
from typing import Annotated

from .dependencies import get_auth_service
from .services.auth_service import AuthService
from .schemas import LoginDTO, LoginSuccessDTO, RegisterDTO

# Definición del tipo de dependencia para reutilizar
ServiceDep = Annotated[AuthService, Depends(get_auth_service)]

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post(
    "/register", 
    response_model=LoginSuccessDTO, 
    status_code=status.HTTP_201_CREATED
)
async def register(dto: RegisterDTO, service: ServiceDep):
    """
    Registra un nuevo usuario y devuelve el token de acceso.
    """
    return await service.register(dto)

@auth_router.post(
    "/login", 
    response_model=LoginSuccessDTO, 
    status_code=status.HTTP_200_OK
)
async def login(dto: LoginDTO, service: ServiceDep):
    """
    Autentica al usuario y devuelve el token de acceso.
    """
    return await service.login(dto)