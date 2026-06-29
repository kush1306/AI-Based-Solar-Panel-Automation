from app.api.deps import create_crud_router
from app.schemas.entities import (
    SolarPredictionCreate,
    SolarPredictionResponse,
    SolarPredictionUpdate,
)
from app.services.crud import solar_prediction_service

router = create_crud_router(
    prefix="/predictions",
    tags=["Solar Predictions"],
    service=solar_prediction_service,
    response_schema=SolarPredictionResponse,
    create_schema=SolarPredictionCreate,
    update_schema=SolarPredictionUpdate,
    resource_label="Solar prediction",
    search_fields=["model_version"],
)
