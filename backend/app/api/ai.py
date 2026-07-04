import logging

from fastapi import APIRouter, Query

from app.core.exceptions import AppException
from app.schemas.energy_model import (
    CombinedAiInsightsResponse,
    EnergyForecastNextResponse,
    EnergyModelHealthResponse,
    EnergyOptimizeAnnualResponse,
    EnergySummaryResponse,
)
from app.schemas.solar_model import SolarModelHealthResponse, SolarModelPredictResponse
from app.services.energy_optimization_client import energy_optimization_client
from app.services.solar_model_client import solar_model_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["AI Integration"])


@router.get(
    "/solar-prediction",
    response_model=SolarModelPredictResponse,
    summary="Live solar prediction via Model 1",
    description="Proxies to the Member 1 Solar Position API at http://models:8000/predict.",
)
async def live_solar_prediction():
    return await solar_model_client.get_prediction()


@router.get(
    "/solar-prediction/health",
    response_model=SolarModelHealthResponse,
    summary="Model 1 service health",
)
async def solar_model_health():
    return await solar_model_client.get_health()


@router.get(
    "/energy/summary",
    response_model=EnergySummaryResponse,
    summary="Energy optimization summary via Model 2",
    description="Proxies to http://energy-optimization:8000/summary.",
)
async def energy_summary():
    return await energy_optimization_client.get_summary()


@router.get(
    "/energy/optimize/annual",
    response_model=EnergyOptimizeAnnualResponse,
    summary="Annual battery optimization via Model 2",
    description="Proxies to http://energy-optimization:8000/optimize/annual.",
)
async def energy_optimize_annual():
    return await energy_optimization_client.get_annual_optimization()


@router.get(
    "/energy/forecast/next",
    response_model=EnergyForecastNextResponse,
    summary="Next-hour demand forecast via Model 2",
    description="Proxies to http://energy-optimization:8000/forecast/next.",
)
async def energy_forecast_next(
    hours: int = Query(24, ge=1, le=168, description="Forecast horizon in hours"),
):
    return await energy_optimization_client.get_forecast_next(hours=hours)


@router.get(
    "/energy/health",
    response_model=EnergyModelHealthResponse,
    summary="Model 2 service health",
)
async def energy_model_health():
    return await energy_optimization_client.get_health()


@router.get(
    "/insights",
    response_model=CombinedAiInsightsResponse,
    summary="Combined Model 1 + Model 2 insights",
    description=(
        "Aggregates solar prediction (Model 1) and energy optimization data (Model 2). "
        "Partial results are returned when one model service is unavailable."
    ),
)
async def combined_ai_insights(
    hours: int = Query(24, ge=1, le=168, description="Forecast horizon for Model 2"),
):
    response = CombinedAiInsightsResponse()
    errors: list[str] = []

    try:
        solar = await solar_model_client.get_prediction()
        response.solar_prediction = solar.model_dump()
        response.solar_model_available = True
    except AppException as exc:
        errors.append(exc.message)
        logger.warning("Model 1 unavailable for combined insights: %s", exc.message)

    try:
        summary = await energy_optimization_client.get_summary()
        response.energy_summary = summary.model_dump()
        response.energy_model_available = True
    except AppException as exc:
        errors.append(exc.message)
        logger.warning("Model 2 summary unavailable: %s", exc.message)

    try:
        forecast = await energy_optimization_client.get_forecast_next(hours=hours)
        response.energy_forecast = forecast.model_dump()
        response.energy_model_available = True
    except AppException as exc:
        errors.append(exc.message)
        logger.warning("Model 2 forecast unavailable: %s", exc.message)

    response.errors = errors
    return response
