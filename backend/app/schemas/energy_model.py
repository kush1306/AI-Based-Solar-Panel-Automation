from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class EnergyModelHealthResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    status: str
    model_trained: bool | None = None
    model_name: str | None = None
    train_metrics: dict[str, Any] | None = None
    dataset_rows: int | None = None
    data_source: str | None = None
    loaded_at: str | None = None
    timestamp_utc: str | None = None


class EnergyForecastPrediction(BaseModel):
    time: str
    predicted_demand_kw: float | None = None


class EnergyForecastNextResponse(BaseModel):
    forecast_hours: int
    from_time: str | None = None
    to_time: str | None = None
    predictions: list[dict[str, Any]] = Field(default_factory=list)
    total_predicted_kwh: float | None = None
    avg_demand_kw: float | None = None


class EnergyAnnualSummary(BaseModel):
    total_demand_kwh: float | None = None
    total_solar_kwh: float | None = None
    total_import_kwh: float | None = None
    total_export_kwh: float | None = None
    annual_savings_inr: float | None = None
    monthly_avg_saving_inr: float | None = None
    self_sufficiency_pct: float | None = None


class EnergyOptimizeAnnualResponse(BaseModel):
    annual_summary: dict[str, Any]
    monthly_breakdown: list[dict[str, Any]] = Field(default_factory=list)
    currency: str | None = None
    system: dict[str, Any] | None = None


class EnergySummaryResponse(BaseModel):
    system: dict[str, Any] | None = None
    model: dict[str, Any] | None = None
    dataset: dict[str, Any] | None = None
    economics: dict[str, Any] | None = None
    timestamp_utc: str | None = None


class CombinedAiInsightsResponse(ORMModel):
    solar_prediction: dict[str, Any] | None = None
    energy_summary: dict[str, Any] | None = None
    energy_forecast: dict[str, Any] | None = None
    solar_model_available: bool = False
    energy_model_available: bool = False
    errors: list[str] = Field(default_factory=list)
