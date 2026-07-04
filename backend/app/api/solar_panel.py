from app.crud import solar_panel_crud
from app.dependencies.crud_router import create_crud_router
from app.schemas.entities import SolarPanelCreate, SolarPanelResponse, SolarPanelUpdate

router = create_crud_router(
    prefix="/panels",
    tags=["Solar Panels"],
    crud=solar_panel_crud,
    response_schema=SolarPanelResponse,
    create_schema=SolarPanelCreate,
    update_schema=SolarPanelUpdate,
    resource_label="Solar panel",
    search_fields=["panel_name", "status"],
)
