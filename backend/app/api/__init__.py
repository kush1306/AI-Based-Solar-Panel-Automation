from fastapi import APIRouter

from . import (
    alerts,
    battery,
    battery_status,
    dashboard,
    energy,
    logs,
    mock,
    predictions,
    solar_panel,
    telemetry,
    weather,
)

router = APIRouter()
router.include_router(weather.router)
router.include_router(solar_panel.router)
router.include_router(predictions.router)
router.include_router(energy.router)
router.include_router(battery.router)
router.include_router(battery_status.router)
router.include_router(telemetry.router)
router.include_router(alerts.router)
router.include_router(logs.router)
router.include_router(mock.router)
router.include_router(dashboard.router)
