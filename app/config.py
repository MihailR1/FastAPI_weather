from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_LOGIN: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_ENGINE: str = 'asyncpg'
    DB_TYPE: str = 'postgresql'

    YANDEX_WEATHER_API_KEY: str
    YANDEX_WEATHER_URL: str = 'https://api.weather.yandex.ru/v2/forecast'
    YANDEX_GEOCODER_API_KEY: str
    YANDEX_GEOCODER_URL: str = 'https://geocode-maps.yandex.ru/1.x'
    YANDEX_API_LIMITS: int = 10

    LOG_LEVEL: str = 'INFO'

    @property
    def DATABASE_URL(self) -> str:
        return f'{self.DB_TYPE}+{self.DB_ENGINE}://{self.DB_LOGIN}:' \
               f'{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
