from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.exceptions import AppException
from contextlib import asynccontextmanager
from core.dbcontext import init_db
from auth.routes import auth_router
from books.router import book_router
from core.s3_client import close_s3_client, init_s3_client
from files.routes import file_router
@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting")
    await init_db()
    init_s3_client()  


    yield


    print("server stoped")
    close_s3_client()  # limpia al cerrar


version ="V1"
app = FastAPI(
    version=version,
    title="F1 API",
    description="Esto es una descripcion",
    lifespan = life_span
)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
app.include_router(book_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(file_router,prefix= "/api")

##EXCEPTION EXAMPLE
# from sqlalchemy.exc import (
#     IntegrityError,        # UK/FK violado, NOT NULL violado
#     NoResultFound,         # .one() no encontró nada
#     MultipleResultsFound,  # .one() encontró más de uno
#     OperationalError,      # DB caída, conexión perdida, timeout
#     DataError,             # dato inválido para la columna (string muy largo, tipo incorrecto)
# )