from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_factory
from app.logger import logger


class BaseCRUD:
    model = None

    @staticmethod
    async def create_session() -> AsyncGenerator[AsyncSession, None]:
        async with async_session_factory() as session:
            try:
                yield session
            except SQLAlchemyError as error:
                logger.error(f'Error while work with db session - {error}')
                await session.rollback()

    @classmethod
    async def find_by_id_or_none(cls, model_id: int, session: AsyncSession = Depends(create_session)):
        query = select(cls.model).filter_by(id=model_id)
        result = await session.execute(query)
        return result.mappings().one_or_none()

    @classmethod
    async def delete(cls, session: AsyncSession = Depends(create_session), **filter_by):
        query = delete(cls.model).filter_by(**filter_by)
        await session.execute(query)
        await session.commit()
