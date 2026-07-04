from functools import lru_cache
import os
from pathlib import Path
from typing import List
from urllib.parse import quote_plus

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BACKEND_DIR / ".env"


def _first_env(*keys: str, default: str) -> str:
    for key in keys:
        value = os.getenv(key)
        if value:
            return value.rstrip("/")
    return default


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        protected_namespaces=("settings_",),
    )

    app_name: str = "Solar Intelligence Platform API"
    app_version: str = "1.0.0"
    debug: bool = False

    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_name: str = "solar_panel_automation"
    db_user: str = "admin"
    db_password: str = "admin"

    # Optional full URL override (e.g. from Docker Compose)
    database_url: str | None = None

    cors_origins: str = "http://localhost:8501,http://127.0.0.1:8501,http://localhost:3000"

    log_level: str = "INFO"

    # Model 1 — Solar Position API (Docker service name, never localhost inside Compose)
    model1_service_url: str = "http://models:8000"
    # Model 2 — Energy Optimization API (Docker service name)
    energy_optimization_service_url: str = "http://energy-optimization:8000"
    # Model 2 trains on startup; allow longer upstream calls than Model 1.
    model_service_timeout: float = 120.0

    @model_validator(mode="after")
    def apply_service_url_aliases(self) -> "Settings":
        object.__setattr__(
            self,
            "model1_service_url",
            _first_env(
                "MODEL1_SERVICE_URL",
                "MODEL_SERVICE_URL",
                "SOLAR_POSITION_API_URL",
                default=self.model1_service_url,
            ),
        )
        object.__setattr__(
            self,
            "energy_optimization_service_url",
            _first_env(
                "ENERGY_OPTIMIZATION_SERVICE_URL",
                "ENERGY_OPTIMIZATION_API_URL",
                default=self.energy_optimization_service_url,
            ),
        )
        return self

    @property
    def model_service_url(self) -> str:
        """Backward-compatible alias for Model 1 URL."""
        return self.model1_service_url

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
