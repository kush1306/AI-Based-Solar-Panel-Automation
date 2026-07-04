from app.crud import energy_consumption_crud
from app.dependencies.crud_router import create_crud_router
from app.schemas.entities import (
    EnergyConsumptionCreate,
    EnergyConsumptionResponse,
    EnergyConsumptionUpdate,
)

router = create_crud_router(
    prefix="/energy",
    tags=["Energy Consumption"],
    crud=energy_consumption_crud,
    response_schema=EnergyConsumptionResponse,
    create_schema=EnergyConsumptionCreate,
    update_schema=EnergyConsumptionUpdate,
    resource_label="Energy consumption record",
    search_fields=["day_of_week"],
)
