from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Hot Topics API"
    DATABASE_URL: str = "sqlite+aiosqlite:///./hot_topics.db"
    CRAWLER_INTERVAL: int = 3600
    CACHE_EXPIRE: int = 86400

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
