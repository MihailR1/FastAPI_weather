from typing import Any, Mapping, Sequence

import sqlalchemy
from sqlalchemy import Result, RowMapping
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_factory
from app.exceptions import DataBaseError
from app.logger import logger
from app.utils.models import City, Weather


class BaseCRUD:
    model = None

    @staticmethod
    async def __make_execute(query, commit: bool = False) -> Result[Any]:
        async with async_session_factory() as session:
            try:
                result = await session.execute(query)

                if commit:
                    await session.commit()
                return result

            except SQLAlchemyError as error:
                logger.error(f"Error while work with db session - {error}")
                await session.rollback()
                raise DataBaseError

    @classmethod
    async def _select_basic(cls, **kwargs) -> Result[Any]:
        query = sqlalchemy.select(cls.model.__table__.columns).filter_by(**kwargs)
        return await cls.__make_execute(query)

    @classmethod
    async def _update_basic(cls, new_data: Mapping[str, Any], update_by: Mapping[str, Any]) -> Result[Any]:
        query = (
            sqlalchemy.update(cls.model).values(**new_data).filter_by(**update_by)
        ).returning(cls.model.__table__.columns)

        result = await cls.__make_execute(query, commit=True)
        return result

    @classmethod
    async def find_by_id_or_none(cls, id: int) -> RowMapping | None:
        result = await cls._select_basic(id=id)
        return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by) -> Sequence[RowMapping]:
        result = await cls._select_basic(**filter_by)
        return result.mappings().all()

    @classmethod
    async def add_one(cls, **data) -> RowMapping | None:
        query = sqlalchemy.insert(cls.model).values(**data).returning(cls.model.id)
        result = await cls.__make_execute(query, commit=True)
        return result.mappings().first()

    @classmethod
    async def add_bulk(cls, *data) -> RowMapping | None:
        query = sqlalchemy.insert(cls.model).values(*data).returning(cls.model.id)
        result = await cls.__make_execute(query, commit=True)
        return result.mappings().first()

    @classmethod
    async def update_by_name(cls, name, **new_data) -> RowMapping | None:
        result = await cls._update_basic(
            update_by={"name": name},
            new_data={**new_data}
        )
        return result.mappings().first()

    @classmethod
    async def delete(cls, **filter_by) -> RowMapping | None:
        query = sqlalchemy.delete(cls.model).filter_by(**filter_by)
        result = await cls.__make_execute(query, commit=True)
        return result.mappings().first()


class CityCRUD(BaseCRUD):
    model = City

    @classmethod
    async def find_by_name_and_region_or_none(cls, name: str, region: str) -> RowMapping | None:
        result = await cls._select_basic(name=name, region=region)
        return result.mappings().one_or_none()


class WeatherCRUD(BaseCRUD):
    model = Weather

    @classmethod
    async def find_by_city_id_or_none(cls, city_id: int) -> RowMapping | None:
        result = await cls._select_basic(city_id=city_id)
        return result.mappings().one_or_none()

    @classmethod
    async def update_by_city_id(cls, city_id, **new_data) -> RowMapping | None:
        result = await cls._update_basic(
            update_by={"city_id": city_id},
            new_data={**new_data}
        )
        return result.mappings().first()
