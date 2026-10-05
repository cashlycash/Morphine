from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Morphine API"
    app_env: str = "development"
    app_version: str = "0.1.0"

    database_url: str = Field(default="sqlite+pysqlite:///./morphine.db", alias="DATABASE_URL")
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")

    jwt_secret_key: str = Field(default="change-me", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = "HS256"
    access_token_exp_minutes: int = 60
    refresh_token_exp_days: int = 30

    cors_origins: list[str] = ["*"]
    rate_limit_per_minute: int = 100


@lru_cache
def get_settings() -> Settings:
    return Settings()
