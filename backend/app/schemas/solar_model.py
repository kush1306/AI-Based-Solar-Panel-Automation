from pydantic import Field

from app.schemas.common import ORMModel


class SolarModelLocation(ORMModel):
    latitude: float
    longitude: float


class SolarModelWeather(ORMModel):
    temperature_2m: float | None = None
    relative_humidity_2m: float | None = None
    cloud_cover: float | None = None
    wind_speed_10m: float | None = None


class SolarModelPredictResponse(ORMModel):
    timestamp: str
    location: SolarModelLocation
    azimuth_deg: float
    elevation_deg: float
    zenith_deg: float
    predicted_shortwave_radiation_wm2: float
    estimated_energy_output_watts: float
    optimal_tilt_deg: float
    panel_facing_direction: str
    model_used: str
    weather_source: str
    weather: SolarModelWeather


class SolarModelHealthResponse(ORMModel):
    status: str
    model_loaded: bool
    model_name: str | None = None
    timestamp: str


class SolarModelServiceError(ORMModel):
    success: bool = False
    error: str
    detail: str | None = None
    source: str = Field(default="model1-service")
