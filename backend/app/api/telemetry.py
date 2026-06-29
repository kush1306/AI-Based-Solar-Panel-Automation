from app.api.deps import create_crud_router
from app.schemas.entities import TelemetryCreate, TelemetryResponse, TelemetryUpdate
from app.services.crud import telemetry_service

router = create_crud_router(
    prefix="/telemetry",
    tags=["Telemetry"],
    service=telemetry_service,
    response_schema=TelemetryResponse,
    create_schema=TelemetryCreate,
    update_schema=TelemetryUpdate,
    resource_label="Telemetry record",
    search_fields=["panel_id", "battery_id"],
)
