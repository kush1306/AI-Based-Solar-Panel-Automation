from __future__ import annotations

from app.core.config import settings
from app.schemas.solar_model import SolarModelHealthResponse, SolarModelPredictResponse
from app.services.model_http_client import ModelHttpClient

_solar_client = ModelHttpClient(
    service_name="Solar prediction service",
    base_url=settings.model1_service_url,
    timeout_seconds=settings.model_service_timeout,
)


class SolarModelClient:
    """HTTP client for Member 1 Solar Position API (Model 1)."""

    def __init__(self, http_client: ModelHttpClient | None = None) -> None:
        self._http = http_client or _solar_client

    async def get_prediction(self) -> SolarModelPredictResponse:
        return await self._http.get_model("/predict", SolarModelPredictResponse)

    async def get_health(self) -> SolarModelHealthResponse:
        return await self._http.get_model("/health", SolarModelHealthResponse)


solar_model_client = SolarModelClient()
