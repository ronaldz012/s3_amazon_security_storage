from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from shared.app_exception import AppException
from contextlib import asynccontextmanager
from shared.model import Book
from shared.dbcontext import init_db

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting")
    await init_db()
    yield
    print("server stoped")

version ="V1"
app = FastAPI(
    version=version,
    title="F1 API",
    description="Esto es una descripcion",
    lifespan = life_span
)
from books.router import book_router

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
app.include_router(book_router, prefix="/api/book",)


##EXCEPTION EXAMPLE
# from sqlalchemy.exc import (
#     IntegrityError,        # UK/FK violado, NOT NULL violado
#     NoResultFound,         # .one() no encontró nada
#     MultipleResultsFound,  # .one() encontró más de uno
#     OperationalError,      # DB caída, conexión perdida, timeout
#     DataError,             # dato inválido para la columna (string muy largo, tipo incorrecto)
# )