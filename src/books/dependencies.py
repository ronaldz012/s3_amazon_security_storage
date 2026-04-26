from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.dbcontext import get_session
from books.service import BookService


def get_book_service(session: AsyncSession = Depends(get_session)) -> BookService:
    return BookService(session)