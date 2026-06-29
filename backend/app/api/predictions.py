from app.crud import solar_prediction_crud
from app.dependencies.crud_router import create_crud_router
from app.schemas.entities import (
    SolarPredictionCreate,
    SolarPredictionResponse,
    SolarPredictionUpdate,
)

router = create_crud_router(
    prefix="/predictions",
    tags=["Solar Predictions"],
    crud=solar_prediction_crud,
    response_schema=SolarPredictionResponse,
    create_schema=SolarPredictionCreate,
    update_schema=SolarPredictionUpdate,
    resource_label="Solar prediction",
    search_fields=["model_version"],
)
