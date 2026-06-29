from app.api.deps import create_crud_router
from app.schemas.entities import SolarPanelCreate, SolarPanelResponse, SolarPanelUpdate
from app.services.crud import solar_panel_service

router = create_crud_router(
    prefix="/panels",
    tags=["Solar Panels"],
    service=solar_panel_service,
    response_schema=SolarPanelResponse,
    create_schema=SolarPanelCreate,
    update_schema=SolarPanelUpdate,
    resource_label="Solar panel",
    search_fields=["panel_name"],
)
