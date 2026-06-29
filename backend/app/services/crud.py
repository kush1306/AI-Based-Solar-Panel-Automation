from app.models import (
    Alert,
    Battery,
    BatteryStatus,
    EnergyConsumption,
    SolarPanel,
    SolarPrediction,
    SystemLog,
    Telemetry,
    WeatherData,
)
from app.schemas.entities import (
    AlertCreate,
    AlertUpdate,
    BatteryCreate,
    BatteryStatusCreate,
    BatteryStatusUpdate,
    BatteryUpdate,
    EnergyConsumptionCreate,
    EnergyConsumptionUpdate,
    SolarPanelCreate,
    SolarPanelUpdate,
    SolarPredictionCreate,
    SolarPredictionUpdate,
    SystemLogCreate,
    TelemetryCreate,
    TelemetryUpdate,
    WeatherCreate,
    WeatherUpdate,
)
from app.services.base import CRUDBase


class WeatherService(CRUDBase[WeatherData, WeatherCreate, WeatherUpdate]):
    pass


class SolarPanelService(CRUDBase[SolarPanel, SolarPanelCreate, SolarPanelUpdate]):
    pass


class SolarPredictionService(
    CRUDBase[SolarPrediction, SolarPredictionCreate, SolarPredictionUpdate]
):
    pass


class EnergyConsumptionService(
    CRUDBase[EnergyConsumption, EnergyConsumptionCreate, EnergyConsumptionUpdate]
):
    pass


class BatteryService(CRUDBase[Battery, BatteryCreate, BatteryUpdate]):
    pass


class BatteryStatusService(
    CRUDBase[BatteryStatus, BatteryStatusCreate, BatteryStatusUpdate]
):
    pass


class TelemetryService(CRUDBase[Telemetry, TelemetryCreate, TelemetryUpdate]):
    pass


class AlertService(CRUDBase[Alert, AlertCreate, AlertUpdate]):
    pass


class SystemLogService(CRUDBase[SystemLog, SystemLogCreate, SystemLogCreate]):
    pass


weather_service = WeatherService(WeatherData, "Weather record")
solar_panel_service = SolarPanelService(SolarPanel, "Solar panel")
solar_prediction_service = SolarPredictionService(SolarPrediction, "Solar prediction")
energy_consumption_service = EnergyConsumptionService(
    EnergyConsumption, "Energy consumption record"
)
battery_service = BatteryService(Battery, "Battery")
battery_status_service = BatteryStatusService(BatteryStatus, "Battery status record")
telemetry_service = TelemetryService(Telemetry, "Telemetry record")
alert_service = AlertService(Alert, "Alert")
system_log_service = SystemLogService(SystemLog, "System log")
