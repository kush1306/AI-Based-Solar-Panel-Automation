from datetime import date
from datetime import datetime as DateTimeType

from pydantic import Field

from app.schemas.common import ORMModel


class WeatherBase(ORMModel):
    recorded_at: DateTimeType
    temperature: float | None = None
    humidity: float | None = None
    cloud_cover: float | None = None
    wind_speed: float | None = None
    ghi: float | None = None
    dni: float | None = None
    aqi: int | None = None
    city: str | None = "Delhi"


class WeatherCreate(WeatherBase):
    pass


class WeatherUpdate(ORMModel):
    recorded_at: DateTimeType | None = None
    temperature: float | None = None
    humidity: float | None = None
    cloud_cover: float | None = None
    wind_speed: float | None = None
    ghi: float | None = None
    dni: float | None = None
    aqi: int | None = None
    city: str | None = None


class WeatherResponse(WeatherBase):
    weather_id: int


class SolarPanelBase(ORMModel):
    panel_name: str = Field(..., max_length=50)
    panel_capacity: float | None = None
    panel_efficiency: float | None = None
    installation_date: date | None = None
    current_tilt: float | None = None
    status: str | None = "Active"


class SolarPanelCreate(SolarPanelBase):
    pass


class SolarPanelUpdate(ORMModel):
    panel_name: str | None = Field(None, max_length=50)
    panel_capacity: float | None = None
    panel_efficiency: float | None = None
    installation_date: date | None = None
    current_tilt: float | None = None
    status: str | None = None


class SolarPanelResponse(SolarPanelBase):
    panel_id: int


class SolarPredictionBase(ORMModel):
    panel_id: int
    weather_id: int
    prediction_time: DateTimeType
    predicted_tilt: float
    expected_power: float | None = None
    confidence_score: float | None = None
    model_version: str | None = None


class SolarPredictionCreate(SolarPredictionBase):
    pass


class SolarPredictionUpdate(ORMModel):
    panel_id: int | None = None
    weather_id: int | None = None
    prediction_time: DateTimeType | None = None
    predicted_tilt: float | None = None
    expected_power: float | None = None
    confidence_score: float | None = None
    model_version: str | None = None


class SolarPredictionResponse(SolarPredictionBase):
    prediction_id: int


class EnergyConsumptionBase(ORMModel):
    recorded_at: DateTimeType
    load_kw: float
    temperature: float | None = None
    humidity: float | None = None
    hour_of_day: int | None = None
    day_of_week: str | None = None
    is_weekend: bool | None = None


class EnergyConsumptionCreate(EnergyConsumptionBase):
    pass


class EnergyConsumptionUpdate(ORMModel):
    recorded_at: DateTimeType | None = None
    load_kw: float | None = None
    temperature: float | None = None
    humidity: float | None = None
    hour_of_day: int | None = None
    day_of_week: str | None = None
    is_weekend: bool | None = None


class EnergyConsumptionResponse(EnergyConsumptionBase):
    consumption_id: int


class BatteryBase(ORMModel):
    battery_name: str = Field(..., max_length=50)
    battery_type: str | None = Field(None, max_length=30)
    capacity_mah: int | None = None
    nominal_voltage: float | None = None
    installation_date: date | None = None
    health_percentage: float | None = None
    status: str | None = "Active"


class BatteryCreate(BatteryBase):
    pass


class BatteryUpdate(ORMModel):
    battery_name: str | None = Field(None, max_length=50)
    battery_type: str | None = Field(None, max_length=30)
    capacity_mah: int | None = None
    nominal_voltage: float | None = None
    installation_date: date | None = None
    health_percentage: float | None = None
    status: str | None = None


class BatteryResponse(BatteryBase):
    battery_id: int


class BatteryStatusBase(ORMModel):
    battery_id: int
    timestamp: DateTimeType
    soc: float
    voltage: float
    current: float
    temperature: float | None = None
    charging_status: str


class BatteryStatusCreate(BatteryStatusBase):
    pass


class BatteryStatusUpdate(ORMModel):
    battery_id: int | None = None
    timestamp: DateTimeType | None = None
    soc: float | None = None
    voltage: float | None = None
    current: float | None = None
    temperature: float | None = None
    charging_status: str | None = None


class BatteryStatusResponse(BatteryStatusBase):
    status_id: int


class TelemetryBase(ORMModel):
    panel_id: int
    battery_id: int
    timestamp: DateTimeType
    voltage: float
    current: float
    power: float
    lux: int | None = None
    tilt_angle: float | None = None
    soc: float | None = None


class TelemetryCreate(TelemetryBase):
    pass


class TelemetryUpdate(ORMModel):
    panel_id: int | None = None
    battery_id: int | None = None
    timestamp: DateTimeType | None = None
    voltage: float | None = None
    current: float | None = None
    power: float | None = None
    lux: int | None = None
    tilt_angle: float | None = None
    soc: float | None = None


class TelemetryResponse(TelemetryBase):
    telemetry_id: int


class AlertBase(ORMModel):
    panel_id: int | None = None
    battery_id: int | None = None
    alert_time: DateTimeType
    alert_type: str = Field(..., max_length=50)
    severity: str
    message: str | None = Field(None, max_length=255)
    status: str | None = "Active"


class AlertCreate(AlertBase):
    pass


class AlertUpdate(ORMModel):
    panel_id: int | None = None
    battery_id: int | None = None
    alert_time: DateTimeType | None = None
    alert_type: str | None = Field(None, max_length=50)
    severity: str | None = None
    message: str | None = Field(None, max_length=255)
    status: str | None = None


class AlertResponse(AlertBase):
    alert_id: int


class SystemLogBase(ORMModel):
    timestamp: DateTimeType
    module: str = Field(..., max_length=50)
    event_type: str = Field(..., max_length=50)
    description: str | None = Field(None, max_length=255)
    status: str


class SystemLogCreate(SystemLogBase):
    pass


class SystemLogUpdate(ORMModel):
    timestamp: DateTimeType | None = None
    module: str | None = Field(None, max_length=50)
    event_type: str | None = Field(None, max_length=50)
    description: str | None = Field(None, max_length=255)
    status: str | None = None


class SystemLogResponse(SystemLogBase):
    log_id: int


__all__ = [
    "WeatherCreate",
    "WeatherUpdate",
    "WeatherResponse",
    "SolarPanelCreate",
    "SolarPanelUpdate",
    "SolarPanelResponse",
    "SolarPredictionCreate",
    "SolarPredictionUpdate",
    "SolarPredictionResponse",
    "EnergyConsumptionCreate",
    "EnergyConsumptionUpdate",
    "EnergyConsumptionResponse",
    "BatteryCreate",
    "BatteryUpdate",
    "BatteryResponse",
    "BatteryStatusCreate",
    "BatteryStatusUpdate",
    "BatteryStatusResponse",
    "TelemetryCreate",
    "TelemetryUpdate",
    "TelemetryResponse",
    "AlertCreate",
    "AlertUpdate",
    "AlertResponse",
    "SystemLogCreate",
    "SystemLogUpdate",
    "SystemLogResponse",
]
