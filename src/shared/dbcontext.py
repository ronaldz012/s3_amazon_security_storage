import asyncpg
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession
from config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker
from typing import AsyncGenerator


# Para crear la DB usamos asyncpg directamente (no SQLAlchemy)

async def create_database_if_not_exists():
    db_url: str = settings.DATA_BASE_URL
    db_name = db_url.rsplit("/", 1)[-1]
    base_url = db_url.rsplit("/", 1)[0] + "/postgres"

    base_url_clean = base_url.replace("postgresql+asyncpg://", "postgresql://")


    conn = await asyncpg.connect(base_url_clean)
    try:
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", db_name
                    )
        if not exists:
            await conn.execute(f'CREATE DATABASE "{db_name}"')
            print(f"Base de datos '{db_name}' creada.")
        else:
            print(f"Base de datos '{db_name}' ya existe.")
    finally:
        await conn.close()



engine = create_async_engine(
    url=settings.DATA_BASE_URL,
    echo=True,
)


async def init_db():
    await create_database_if_not_exists()
    async with engine.begin() as conn:
        from .model import Base  # importas Base, no SQLModel
        await conn.run_sync(Base.metadata.create_all)
        print("Tablas creadas o ya existentes.")



async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session