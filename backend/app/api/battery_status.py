from app.crud import battery_status_crud
from app.dependencies.crud_router import create_crud_router
from app.schemas.entities import (
    BatteryStatusCreate,
    BatteryStatusResponse,
    BatteryStatusUpdate,
)

router = create_crud_router(
    prefix="/battery-status",
    tags=["Battery Status"],
    crud=battery_status_crud,
    response_schema=BatteryStatusResponse,
    create_schema=BatteryStatusCreate,
    update_schema=BatteryStatusUpdate,
    resource_label="Battery status record",
    search_fields=["charging_status"],
)
