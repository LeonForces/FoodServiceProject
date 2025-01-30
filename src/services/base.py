from sqlalchemy import insert, select, delete, update, Result
from src.db.postgres import get_session


class BaseDAO():
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async for session in get_session():
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result: Result = await session.execute(query)
            return result.one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async for session in get_session():
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result: Result = await session.execute(query)
            return result

    @classmethod
    async def add(cls, **data):
        async for session in get_session():
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def _delete(cls, **filter_by):
        async for session in get_session():
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def _update(cls, model_id: int, **data):
        async for session in get_session():
            query = update(cls.model)\
                .where(cls.model.id == model_id)\
                .values(**data)
            await session.execute(query)
            await session.commit()
