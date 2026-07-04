from __future__ import annotations

from app.core.config import settings
from app.schemas.energy_model import (
    EnergyForecastNextResponse,
    EnergyModelHealthResponse,
    EnergyOptimizeAnnualResponse,
    EnergySummaryResponse,
)
from app.services.model_http_client import ModelHttpClient

_energy_client = ModelHttpClient(
    service_name="Energy optimization service",
    base_url=settings.energy_optimization_service_url,
    timeout_seconds=settings.model_service_timeout,
)


class EnergyOptimizationClient:
    """HTTP client for Member 2 Demand Forecast & Battery Optimization API."""

    def __init__(self, http_client: ModelHttpClient | None = None) -> None:
        self._http = http_client or _energy_client

    async def get_health(self) -> EnergyModelHealthResponse:
        return await self._http.get_model("/health", EnergyModelHealthResponse)

    async def get_summary(self) -> EnergySummaryResponse:
        return await self._http.get_model("/summary", EnergySummaryResponse)

    async def get_annual_optimization(self) -> EnergyOptimizeAnnualResponse:
        return await self._http.get_model("/optimize/annual", EnergyOptimizeAnnualResponse)

    async def get_forecast_next(self, *, hours: int = 24) -> EnergyForecastNextResponse:
        return await self._http.get_model(
            "/forecast/next",
            EnergyForecastNextResponse,
            params={"hours": hours},
        )


energy_optimization_client = EnergyOptimizationClient()
