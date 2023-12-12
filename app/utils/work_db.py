from sqlalchemy import RowMapping

from app.logger import logger
from app.utils.crud import CityCRUD, WeatherCRUD
from app.utils.schemas import CitySchema, WeatherSchema


async def save_city_in_database(city: CitySchema) -> RowMapping:
    find_in_db = await CityCRUD.find_by_name_and_region_or_none(
        name=city.name,
        region=city.region
    )

    if not find_in_db:
        dumto_to_dict = CitySchema.model_dump(city, mode='dict')
        query = await CityCRUD.add_one(**dumto_to_dict)

        logger.info('Add new city - to DB')
        return query

    return find_in_db


async def update_weather_in_db(city_id: int, weather: WeatherSchema) -> RowMapping:
    find_in_db = await WeatherCRUD.find_by_city_id_or_none(city_id)
    dumto_to_dict = WeatherSchema.model_dump(weather, mode='dict')

    if find_in_db:
        result = await WeatherCRUD.update_by_city_id(city_id=city_id, **dumto_to_dict)
    else:
        result = await WeatherCRUD.add_one(city_id=city_id, **dumto_to_dict)

    logger.info(f'Update weather city_id {city_id}')

    return result
