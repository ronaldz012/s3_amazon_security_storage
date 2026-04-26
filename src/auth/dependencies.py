from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from greenlet import getcurrent
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.services import auth_service
from auth.services.current_user_service import CurrentUserService
from auth.services.auth_service import AuthService
from core.dbcontext import SessionDep, get_session


bearer_scheme = HTTPBearer()
def get_auth_service(session: SessionDep) -> AuthService:
    return AuthService(session=session)

# /auth/dependencies.py
def get_current_user_service(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> CurrentUserService:
    return CurrentUserService(token=credentials.credentials)


CurrentUserServiceDep = Annotated[CurrentUserService, Depends(get_current_user_service)]
AuthServiceServiceDep = Annotated[auth_service, Depends(get_auth_service)]


