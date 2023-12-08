import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_LOGIN: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_ENGINE: str = 'asyncpg'
    DB_TYPE: str = 'postgresql'
    LOG_LEVEL: str = 'INFO'
    YANDEX_WEATHER_API_KEY: str
    BASEDIR: str = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
    LOG_FILES_PATH: str = os.path.join(BASEDIR, 'logs')

    @property
    def DATABASE_URL(self):
        return f'{self.DB_TYPE}+{self.DB_ENGINE}://{self.DB_LOGIN}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
