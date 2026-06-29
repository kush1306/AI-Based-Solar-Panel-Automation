from functools import lru_cache
from pathlib import Path
from typing import List
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BACKEND_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Solar Intelligence Platform API"
    app_version: str = "1.0.0"
    debug: bool = False

    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_name: str = "solar_demand_db"
    db_user: str = "admin"
    db_password: str = "admin"

    # Optional full URL override (e.g. from Docker Compose)
    database_url: str | None = None

    cors_origins: str = "http://localhost:8501,http://127.0.0.1:8501,http://localhost:3000"

    log_level: str = "INFO"

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        user = quote_plus(self.db_user)
        password = quote_plus(self.db_password)
        return (
            f"mysql+pymysql://{user}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
