from fastapi import APIRouter, Depends
from typing import Annotated

from books.dependencies import BookService, get_book_service
from books.schemas import BookDto, CreateBookDto

ServiceDep = Annotated[BookService, Depends(get_book_service)]

book_router = APIRouter(tags=["Books"])

@book_router.post("", status_code=201, response_model=BookDto)
async def save_book(data: CreateBookDto, service: ServiceDep):
    return await service.save_book(data)

@book_router.get("", status_code=200, response_model=list[BookDto])
async def get_all_books(service: ServiceDep):
    return await service.get_books()

@book_router.get("/{id}", status_code=200, response_model=BookDto)
async def get_book_by_id(id: int, service: ServiceDep):
    return await service.get_book_by_id(id)

@book_router.put("", status_code=200, response_model=BookDto)
async def update_book(data: BookDto, service: ServiceDep):
    return await service.update_book(data)