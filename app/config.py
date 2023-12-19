import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    YANDEX_WEATHER_API_KEY: str
    YANDEX_WEATHER_URL: str = 'https://api.weather.yandex.ru/v2/forecast'
    YANDEX_GEOCODER_API_KEY: str
    YANDEX_GEOCODER_URL: str = 'https://geocode-maps.yandex.ru/1.x'
    YANDEX_API_LIMITS: int = 10

    LOG_LEVEL: str = 'INFO'
    BASEDIR: str = os.path.abspath(os.path.dirname(__file__))
    ENV_FILE_PATH: str = os.path.join(BASEDIR, '..', '.env')

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra='ignore')


settings = Settings()
