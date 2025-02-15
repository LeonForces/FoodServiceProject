from sqlalchemy.ext.asyncio import AsyncSession, \
    async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from typing import AsyncIterator

from src.core.config import settings

Base = declarative_base()

engine = create_async_engine(
    str(settings.db_url), echo=settings.echo, future=True
)

async_session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
