from pydantic import BaseModel


class CitySchema(BaseModel):
    country: str
    region: str
    name: str
    latitude: float
    longitude: float


class WeatherSchema(BaseModel):
    temperature: float
    feels_like: float
    pressure: float
    humidity: float
    wind_speed: float
    city: str
