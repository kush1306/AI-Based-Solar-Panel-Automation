from app.api.deps import create_crud_router
from app.schemas.entities import (
    BatteryStatusCreate,
    BatteryStatusResponse,
    BatteryStatusUpdate,
)
from app.services.crud import battery_status_service

router = create_crud_router(
    prefix="/battery-status",
    tags=["Battery Status"],
    service=battery_status_service,
    response_schema=BatteryStatusResponse,
    create_schema=BatteryStatusCreate,
    update_schema=BatteryStatusUpdate,
    resource_label="Battery status record",
    search_fields=["charging_status"],
)
