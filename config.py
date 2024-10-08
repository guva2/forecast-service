import os

from pydantic import computed_field, PostgresDsn, validator
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD_FILE: str
    POSTGRES_DB: str

    FORECAST_LATITUDE: str
    FORECAST_LONGITUDE: str
    SCHEDULER_INTERVAL_MINUTES: int = 60
    NWS_API_BASE: str

    @validator('POSTGRES_PASSWORD_FILE', pre=True, always=True)
    def read_postgres_password(cls, file_path):
        if file_path:
            with open(file_path, 'r') as file:
                return file.read().strip()
        return file_path 

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD_FILE,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

settings = Settings()
