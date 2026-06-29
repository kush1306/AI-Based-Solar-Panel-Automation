from app.crud.base import CRUDBase
from app.crud.entities import (
    alert_crud,
    battery_crud,
    battery_status_crud,
    energy_consumption_crud,
    solar_panel_crud,
    solar_prediction_crud,
    system_log_crud,
    telemetry_crud,
    weather_crud,
)

__all__ = [
    "CRUDBase",
    "weather_crud",
    "solar_panel_crud",
    "solar_prediction_crud",
    "energy_consumption_crud",
    "battery_crud",
    "battery_status_crud",
    "telemetry_crud",
    "alert_crud",
    "system_log_crud",
]
