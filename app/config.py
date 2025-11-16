from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    APP_NAME: str
    APP_ENV: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: int

    API_PORT: int

    class Config:
        env_file = ".env"


# If running under pytest, override
if "PYTEST_CURRENT_TEST" in os.environ:
    settings = Settings(_env_file=".env.test")
else:
    settings = Settings()
