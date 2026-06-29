from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.schemas.entities import AlertResponse, SystemLogResponse


class DashboardOverview(BaseModel):
    current_power: float
    battery_soc: float
    temperature: float | None
    humidity: float | None
    optimal_tilt: float | None
    today_energy: float
    system_status: str
    active_alerts: int
    recent_logs: list[SystemLogResponse]
    active_alert_items: list[AlertResponse]


class ChartDataPoint(BaseModel):
    timestamp: datetime
    value: float
    label: str | None = None


class DashboardCharts(BaseModel):
    power_generation: list[ChartDataPoint]
    battery_soc: list[ChartDataPoint]
    temperature: list[ChartDataPoint]
    energy_consumption: list[ChartDataPoint]
    telemetry: list[ChartDataPoint]
    predicted_tilt: list[ChartDataPoint]


class DashboardChartsQuery(BaseModel):
    hours: int = 24
