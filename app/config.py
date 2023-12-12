from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    YANDEX_WEATHER_API_KEY: str
    YANDEX_WEATHER_URL: str = 'https://api.weather.yandex.ru/v2/forecast'
    YANDEX_GEOCODER_API_KEY: str
    YANDEX_GEOCODER_URL: str = 'https://geocode-maps.yandex.ru/1.x'
    YANDEX_API_LIMITS: int = 10

    LOG_LEVEL: str = 'INFO'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
