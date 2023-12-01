from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_ENGINE: str
    DB_TYPE: str
    DB_LOGIN: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f'{self.DB_TYPE}+{self.DB_ENGINE}://{self.DB_LOGIN}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    class Config:
        env_file = ".env"


settings = Settings()
