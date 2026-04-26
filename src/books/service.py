# src/infrastructure/services/book_service.py
from ast import List
import logging
from sqlmodel import select, text
from sqlalchemy.exc import IntegrityError

from sqlmodel.ext.asyncio.session import AsyncSession
from core.models import Book
from books.schemas import BookDto, CreateBookDto
from core.exceptions import AppException, ConflictException, InternalException, NotFoundException

logger = logging.getLogger(__name__)

class BookService():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_book(self, data: CreateBookDto) -> BookDto:
        new_book = Book(title=data.title, description=data.description)
        try:
            self.session.add(new_book)
            await self.session.commit()
            await self.session.refresh(new_book)

            if new_book.id is None:
                raise InternalException()

            return BookDto.model_validate(new_book)
        except IntegrityError as e:
            await self.session.rollback()
            logger.error(f"IntegrityError: {e}")
            raise ConflictException("Ya existe un libro con esos datos")
        
        except AppException:
            raise

        except Exception as e:

            await self.session.rollback()
            logger.error(f"Error inesperado: {e}")
            raise InternalException()
        

    async def get_books(self) -> list[BookDto]:
        try:
            results = await self.session.exec(select(Book))
            return [BookDto.model_validate(book) for book in results.all()]
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            raise InternalException()
        
        
    async def get_book_by_id(self, book_id:int) -> BookDto:
        book = await self.session.get(Book,book_id) 
        if book is Book: raise NotFoundException(f"book with id: {book_id} not found")
        return BookDto.model_validate(book)
    
    async def update_book(self, dto:BookDto)->BookDto:
        book_to_update = await self.session.get(Book, dto.id) 
    
        if book_to_update is None: raise NotFoundException(f"book with id: {id} not found")

        try:
            update_data = dto.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(book_to_update, key, value)
            
            self.session.add(book_to_update)
            await self.session.commit()
            await self.session.refresh(book_to_update)
            
            return BookDto.model_validate(book_to_update)

        except Exception as e:
            await self.session.rollback()
            raise