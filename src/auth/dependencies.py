from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.service import AuthService
from shared.dbcontext import get_session


def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session)