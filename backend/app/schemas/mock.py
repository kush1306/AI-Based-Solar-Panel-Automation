from datetime import datetime

from pydantic import Field

from app.schemas.common import ORMModel


class MockSolarPredictionResponse(ORMModel):
    panel_id: int
    weather_id: int
    prediction_time: datetime
    predicted_tilt: float
    expected_power: float
    confidence_score: float
    model_version: str
    city: str = "Delhi"
    irradiance_wm2: float
    optimal_azimuth: float
    estimated_generation_kwh: float
    source: str = "mock"
    note: str = Field(
        default="Placeholder response until the AI solar model is integrated."
    )


class EnergyForecastPoint(ORMModel):
    hour: int
    timestamp: datetime
    predicted_load_kw: float
    temperature: float | None = None
    humidity: float | None = None


class MockEnergyForecastResponse(ORMModel):
    city: str = "Delhi"
    forecast_start: datetime
    forecast_end: datetime
    horizon_hours: int
    total_predicted_load_kwh: float
    peak_load_kw: float
    peak_hour: int
    average_load_kw: float
    model_version: str
    forecast: list[EnergyForecastPoint]
    source: str = "mock"
    note: str = Field(
        default="Placeholder response until the AI energy model is integrated."
    )
