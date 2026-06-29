from app.api.deps import create_crud_router
from app.schemas.entities import (
    EnergyConsumptionCreate,
    EnergyConsumptionResponse,
    EnergyConsumptionUpdate,
)
from app.services.crud import energy_consumption_service

router = create_crud_router(
    prefix="/energy",
    tags=["Energy Consumption"],
    service=energy_consumption_service,
    response_schema=EnergyConsumptionResponse,
    create_schema=EnergyConsumptionCreate,
    update_schema=EnergyConsumptionUpdate,
    resource_label="Energy consumption record",
    search_fields=["day_of_week"],
)
