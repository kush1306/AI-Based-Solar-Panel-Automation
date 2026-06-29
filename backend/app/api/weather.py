from app.api.deps import create_crud_router
from app.schemas.entities import WeatherCreate, WeatherResponse, WeatherUpdate
from app.services.crud import weather_service

router = create_crud_router(
    prefix="/weather",
    tags=["Weather"],
    service=weather_service,
    response_schema=WeatherResponse,
    create_schema=WeatherCreate,
    update_schema=WeatherUpdate,
    resource_label="Weather record",
    search_fields=["city"],
)
