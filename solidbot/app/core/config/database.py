from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config.settings import settings
from functools import lru_cache
from typing import AsyncGenerator

Base = declarative_base()

@lru_cache()
def create_engine():
    # Use asyncpg as the driver
    return create_async_engine(
        settings.DATABASE_URL_STR.replace("postgresql://", "postgresql+asyncpg://"),
        echo=True
    )

@lru_cache()
def get_async_session_maker():
    engine = create_engine()
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async_session = get_async_session_maker()
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

engine = create_engine()
AsyncSessionLocal = get_async_session_maker()