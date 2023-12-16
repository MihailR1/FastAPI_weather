import json
from asyncio import Semaphore
from typing import Mapping, Generic, Any

import aiohttp
from fastapi import status
from pydantic import ValidationError, BaseModel

from app.config import settings
from app.utils.exceptions import ConnectionToAPIError, WrongCity
from app.schemas.schemas import CitySchema, WeatherSchema
from app.utils.logger import logger


class ConvertSchemaMixin:
    async def convert_city_response_to_scheme(self, response) -> CitySchema:
        main_response_body = (
            response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        )
        city_data_response = (
            main_response_body['metaDataProperty']['GeocoderMetaData']['AddressDetails']['Country']
        )
        geo_coordinates = main_response_body['Point']['pos']

        country = city_data_response['CountryName']
        region = city_data_response['AdministrativeArea']['AdministrativeAreaName']
        name = main_response_body['name']
        lon, lat = geo_coordinates.split()

        city_schema: CitySchema = CitySchema.model_validate(
            {'country': country,
             'region': region,
             'name': name,
             'latitude': lat,
             'longitude': lon
             }
        )

        return city_schema


class Weather(ConvertSchemaMixin):
    semaphor = Semaphore(settings.YANDEX_API_LIMITS)
    lang = 'ru_RU'
    limit = 3

    async def fetch_data(
            self, url: str, header: Mapping[str, str], params: Mapping[str, str]) -> json:

        async with aiohttp.ClientSession(headers=header) as session:
            async with self.semaphor, session.get(url, params=params) as response:
                if response.status == status.HTTP_200_OK:
                    result = json.loads(await response.text())
                    return result
                else:
                    logger.error(f'Ошибка при обращении к API Yandex, status: {response.status}, '
                                 f'error: {json.loads(await response.text())["errors"]}')
                    raise ConnectionToAPIError

    @staticmethod
    async def validate_response_to_schema(schema: Any, response: Mapping[str, str]):
        try:
            convert_to_schema = schema.model_validate(response)
        except (IndexError, TypeError, KeyError, ValidationError) as error:
            logger.error(f'Ошибка при валидации данных. error: {error}')
            raise WrongCity

        return convert_to_schema

    async def get_weather_data(self, lat, lon) -> WeatherSchema:
        header = {'X-Yandex-API-Key': settings.YANDEX_WEATHER_API_KEY}
        params = {'lat': lat,
                  'lon': lon,
                  'limit': self.limit,
                  'hours': 'false',
                  'extra': 'false',
                  'lang': self.lang
                  }

        response = await self.fetch_data(settings.YANDEX_WEATHER_URL, header=header, params=params)

        return await self.validate_response_to_schema(WeatherSchema, response)

    async def get_city_geo_by_name(self, name) -> CitySchema:
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
        main_response_body = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        print(CitySchema.model_json_schema())
        result = await self.validate_response_to_schema(CitySchema, main_response_body)
        print(result)

        return None


weather: Weather = Weather()
