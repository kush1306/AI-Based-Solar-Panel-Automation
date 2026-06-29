from app.crud import system_log_crud
from app.dependencies.crud_router import create_crud_router
from app.schemas.entities import SystemLogCreate, SystemLogResponse, SystemLogUpdate

router = create_crud_router(
    prefix="/logs",
    tags=["System Logs"],
    crud=system_log_crud,
    response_schema=SystemLogResponse,
    create_schema=SystemLogCreate,
    update_schema=SystemLogUpdate,
    resource_label="System log",
    search_fields=["module", "event_type", "description"],
)
