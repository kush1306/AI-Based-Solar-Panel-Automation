from app.crud import telemetry_crud
from app.dependencies.crud_router import create_crud_router
from app.schemas.entities import TelemetryCreate, TelemetryResponse, TelemetryUpdate

router = create_crud_router(
    prefix="/telemetry",
    tags=["Telemetry"],
    crud=telemetry_crud,
    response_schema=TelemetryResponse,
    create_schema=TelemetryCreate,
    update_schema=TelemetryUpdate,
    resource_label="Telemetry record",
    search_fields=[],
)
