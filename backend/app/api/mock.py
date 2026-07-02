from fastapi import APIRouter, Query

from app.schemas.mock import MockEnergyForecastResponse, MockSolarPredictionResponse
from app.services.mock_service import mock_ai_service

router = APIRouter(prefix="/mock", tags=["Mock AI (Placeholder)"])


@router.get(
    "/solar-prediction",
    response_model=MockSolarPredictionResponse,
    summary="Mock solar tilt and power prediction",
    description=(
        "Returns realistic dummy solar prediction data for frontend development. "
        "Replace with the real AI model service when integrated."
    ),
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
    summary="Mock energy load forecast",
    description=(
        "Returns realistic dummy energy consumption forecast data for frontend "
        "development. Replace with the real AI model service when integrated."
    ),
)
async def mock_energy_forecast(
    horizon_hours: int = Query(
        24,
        ge=1,
        le=48,
        description="Number of hours to forecast",
    ),
):
    return mock_ai_service.get_energy_forecast(horizon_hours=horizon_hours)
