from typing import Annotated

from fastapi import Depends
from auth.services.current_user_service import CurrentUserService
from core.dbcontext import get_session
from core.s3_client import get_s3_client
from .service import FileService
from sqlmodel.ext.asyncio.session import AsyncSession


def get_file_service(session: AsyncSession = Depends(get_session)) -> FileService:
    return FileService(session=session)


FileServiceDep = Annotated[FileService, Depends(get_file_service)]
