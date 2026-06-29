from app.api.deps import create_crud_router
from app.schemas.entities import BatteryCreate, BatteryResponse, BatteryUpdate
from app.services.crud import battery_service

router = create_crud_router(
    prefix="/battery",
    tags=["Battery"],
    service=battery_service,
    response_schema=BatteryResponse,
    create_schema=BatteryCreate,
    update_schema=BatteryUpdate,
    resource_label="Battery",
    search_fields=["battery_name", "battery_type"],
)
