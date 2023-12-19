import json
from asyncio import Semaphore
from typing import Mapping, Any

import aiohttp
from fastapi import status

from app.config import settings
from app.schemas.response_schemas import CitySchema, WeatherSchema
from app.schemas.validate_schemas import validate_response_to_schema
from app.utils.exceptions import ConnectionToAPIError, ValidationSchemaError, WrongCityError
from app.utils.logger import logger


class Weather:
    semaphor = Semaphore(settings.YANDEX_API_LIMITS)
    lang = 'ru_RU'
    limit = 3

    async def fetch_data(
            self,
            url: str,
            header: Mapping[str, str],
            params: Mapping[str, str | int]) -> Mapping[str, Any]:

        async with aiohttp.ClientSession(headers=header) as session:
            async with self.semaphor, session.get(url, params=params) as response:
                response_text = await response.text()

                if response.status == status.HTTP_200_OK:
                    result = json.loads(response_text)
                    return result
                else:
                    logger.error(f'Ошибка при обращении к API Yandex, status: {response.status}, '
                                 f'error: {response_text}')
                    raise ConnectionToAPIError

    async def get_weather_data(self, lat: float, lon: float) -> WeatherSchema:
        header = {'X-Yandex-API-Key': settings.YANDEX_WEATHER_API_KEY}
        params = {'lat': lat,
                  'lon': lon,
                  'limit': self.limit,
                  'hours': 'false',
                  'extra': 'false',
                  'lang': self.lang
                  }

        response = await self.fetch_data(settings.YANDEX_WEATHER_URL, header=header, params=params)
        try:
            result = await validate_response_to_schema(WeatherSchema, response)
        except ValidationSchemaError:
            raise WrongCityError

        return result

    async def get_city_geo_by_name(self, name: str) -> CitySchema:
        url = settings.YANDEX_GEOCODER_URL
        header = {}
        params = {
            'apikey': settings.YANDEX_GEOCODER_API_KEY,
            'geocode': name,
            'result': self.limit,
            'lang': self.lang,
            'format': 'json'
                  }

        response = await self.fetch_data(url, header, params)

        try:
            main_response_body = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
            result = await validate_response_to_schema(CitySchema, main_response_body)
        except (IndexError, ValidationSchemaError):
            raise WrongCityError

        return result


weather: Weather = Weather()
