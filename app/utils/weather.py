import json
from asyncio import Semaphore
from typing import Mapping

import aiohttp

from app.config import settings
from app.exceptions import ConnectionToAPIError, WrongCity
from app.utils.schemas import CitySchema, WeatherSchema


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

    async def convert_weather_response_to_scheme(self, response) -> WeatherSchema:
        temperature = response['fact']['temp']
        feels_like = response['fact']['feels_like']
        pressure = response['fact']['pressure_mm']
        humidity = response['fact']['humidity']
        wind_speed = response['fact']['wind_speed']

        weather_scheme: WeatherSchema = WeatherSchema.model_validate(
            {
             'temperature': temperature,
             'feels_like': feels_like,
             'pressure': pressure,
             'humidity': humidity,
             'wind_speed': wind_speed,
             }
        )

        return weather_scheme


class Weather(ConvertSchemaMixin):
    semaphor = Semaphore(settings.YANDEX_API_LIMITS)
    lang = 'ru_RU'
    limit = 3

    async def fetch_data(
            self, url: str, header: Mapping[str, str], params: Mapping[str, str]):

        async with aiohttp.ClientSession(headers=header) as session:
            async with self.semaphor, session.get(url, params=params) as response:
                if response.status == 200:
                    result = json.loads(await response.text())
                    return result
                else:
                    raise ConnectionToAPIError

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
        try:
            convert_to_schema: WeatherSchema = await self.convert_weather_response_to_scheme(response)
        except (IndexError, TypeError, KeyError):
            raise WrongCity

        return convert_to_schema

    async def get_city_geo_by_name(self, name) -> CitySchema:
        url = settings.YANDEX_GEOCODER_URL
        header = {}
        params = {
            'apikey': settings.YANDEX_GEOCODER_API_KEY,
            'geocode': name,
            'result': 1,
            'lang': self.lang,
            'format': 'json'
                  }

        response = await self.fetch_data(url, header, params)
        try:
            convert_to_schema: CitySchema = await self.convert_city_response_to_scheme(response)
        except (IndexError, TypeError, KeyError):
            raise WrongCity

        return convert_to_schema


weather: Weather = Weather()
