from app.crud import battery_crud
from app.dependencies.crud_router import create_crud_router
from app.schemas.entities import BatteryCreate, BatteryResponse, BatteryUpdate

router = create_crud_router(
    prefix="/battery",
    tags=["Battery"],
    crud=battery_crud,
    response_schema=BatteryResponse,
    create_schema=BatteryCreate,
    update_schema=BatteryUpdate,
    resource_label="Battery",
    search_fields=["battery_name", "battery_type", "status"],
)
