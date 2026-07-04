"""AI service integration helpers."""

from app.services.energy_optimization_client import energy_optimization_client
from app.services.solar_model_client import solar_model_client


async def predict_optimal_tilt() -> dict:
    """Fetch live solar tilt/power prediction from Model 1."""
    result = await solar_model_client.get_prediction()
    return result.model_dump()


async def predict_energy_load(*, hours: int = 24) -> dict:
    """Fetch live demand forecast from Model 2."""
    result = await energy_optimization_client.get_forecast_next(hours=hours)
    return result.model_dump()


async def get_energy_summary() -> dict:
    """Fetch annual economics summary from Model 2."""
    result = await energy_optimization_client.get_summary()
    return result.model_dump()
