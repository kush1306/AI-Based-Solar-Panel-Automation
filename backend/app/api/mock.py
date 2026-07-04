import logging

from fastapi import APIRouter, Query

from app.core.exceptions import AppException
from app.schemas.mock import MockEnergyForecastResponse, MockSolarPredictionResponse
from app.services.energy_forecast_adapter import map_energy_forecast_to_mock
from app.services.energy_optimization_client import energy_optimization_client
from app.services.mock_service import mock_ai_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mock", tags=["Mock AI (Placeholder)"])


@router.get(
    "/solar-prediction",
    response_model=MockSolarPredictionResponse,
    summary="Mock solar tilt and power prediction",
    description="Placeholder solar prediction data for frontend development.",
)
async def mock_solar_prediction(
    panel_id: int = Query(1, ge=1, description="Solar panel ID"),
    weather_id: int = Query(1, ge=1, description="Weather record ID"),
):
    return mock_ai_service.get_solar_prediction(
        panel_id=panel_id,
        weather_id=weather_id,
    )


@router.get(
    "/energy",
    response_model=MockEnergyForecastResponse,
    summary="Energy load forecast (Model 2 proxy with mock fallback)",
    description=(
        "Returns live demand forecast from the Energy Optimization API when available. "
        "Falls back to deterministic mock data if Model 2 is unavailable."
    ),
)
async def mock_energy_forecast(
    horizon_hours: int = Query(
        24,
        ge=1,
        le=168,
        description="Number of hours to forecast",
    ),
):
    try:
        forecast = await energy_optimization_client.get_forecast_next(hours=horizon_hours)
        return map_energy_forecast_to_mock(forecast)
    except AppException as exc:
        logger.warning("Model 2 forecast unavailable, using mock fallback: %s", exc.message)
        return mock_ai_service.get_energy_forecast(horizon_hours=horizon_hours)
