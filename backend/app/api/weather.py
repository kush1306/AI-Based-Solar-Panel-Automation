from app.crud import weather_crud
from app.dependencies.crud_router import create_crud_router
from app.schemas.entities import WeatherCreate, WeatherResponse, WeatherUpdate

router = create_crud_router(
    prefix="/weather",
    tags=["Weather"],
    crud=weather_crud,
    response_schema=WeatherResponse,
    create_schema=WeatherCreate,
    update_schema=WeatherUpdate,
    resource_label="Weather record",
    search_fields=["city"],
)
