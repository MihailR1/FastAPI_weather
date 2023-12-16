import pytest

from app.routes.weather import get_weather_by_city_geo, get_weather_by_city_name
from app.schemas.response_schemas import WeatherSchema
from app.utils.exceptions import ConnectionToAPIError, WrongCityError


@pytest.mark.parametrize(
    "lat, lon, city",
    [
        (55.755864, 37.617698, "Москва"),
        (28.614243, 77.202788, "Нью-Дели"),
        (59.938676, 30.314494, "Санкт-Петербург"),
        (13.097396, -59.606291, "Бриджтаун"),
    ],
)
async def test__get_weather_by_city_geo__valid_geocoordinates(lat, lon, city):
    result: WeatherSchema = await get_weather_by_city_geo(lat, lon)

    assert result.city == city
    assert result.temperature
    assert result.humidity


@pytest.mark.parametrize(
    "lat, lon",
    [(-2312, 342), (23928278.614243, 77.202788), (0, -324), (-0.4328, 213.7827)],
)
async def test__get_weather_by_city_geo__wrong_geocoordinates(lat, lon):
    with pytest.raises(ConnectionToAPIError):
        assert await get_weather_by_city_geo(lat, lon)


@pytest.mark.parametrize(
    "city", ["Москва", "мск", "МАСКВА", "спб", "Екб", "екат", "чикаого", "нью-йорк"]
)
async def test__get_weather_by_city_name__valid__cities_names(city):
    result: WeatherSchema = await get_weather_by_city_name(city)

    assert result.temperature
    assert result.humidity


@pytest.mark.parametrize(
    "city",
    [
        "EkатерuHburg",
        "1231d",
        "dfg",
    ],
)
async def test__get_weather_by_city_name__wrong_cities_names(city):
    with pytest.raises(WrongCityError):
        assert await get_weather_by_city_name(city)
