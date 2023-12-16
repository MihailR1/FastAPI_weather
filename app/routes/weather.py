from fastapi import APIRouter

from app.schemas.schemas import CitySchema, WeatherSchema
from app.services.weather import weather

router = APIRouter(prefix="/weather", tags=["Погода"])


@router.get('city/geo/')
async def get_weather_by_city_geo(lat: float = 55.755864, lon: float = 37.617698) -> WeatherSchema:
    """Выводит погоду по гео-координатам долготы и широты"""

    city_weather: WeatherSchema = await weather.get_weather_data(lat, lon)
    return city_weather


@router.get('/city/')
async def get_weather_by_city_name(name: str = 'Moscow') -> WeatherSchema:
    """Выводит погоду по названию города, исправляет опечатки в запросе.
    Допустимы любые города мира
    Допустимые запросы:
    Екатеринбург,
    Yekaterinburg,
    Екатеринбург Свердловская область,
    екб,
    екат"""

    city_geo_data: CitySchema = await weather.get_city_geo_by_name(name)

    # #city_weather: WeatherSchema = await get_weather_by_city_geo(
    #     city_geo_data.latitude,
    #     city_geo_data.longitude
    # )

    #return city_weather
