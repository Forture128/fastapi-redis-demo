# app/config.py
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/dbname"
    )
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")


settings = Settings()
