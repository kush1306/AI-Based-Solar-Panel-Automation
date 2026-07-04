from app.crud.base import CRUDBase
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
from app.schemas import (
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
    SystemLogUpdate,
    TelemetryCreate,
    TelemetryUpdate,
    WeatherCreate,
    WeatherUpdate,
)


class WeatherCRUD(CRUDBase[WeatherData, WeatherCreate, WeatherUpdate]):
    pass


class SolarPanelCRUD(CRUDBase[SolarPanel, SolarPanelCreate, SolarPanelUpdate]):
    pass


class SolarPredictionCRUD(
    CRUDBase[SolarPrediction, SolarPredictionCreate, SolarPredictionUpdate]
):
    pass


class EnergyConsumptionCRUD(
    CRUDBase[EnergyConsumption, EnergyConsumptionCreate, EnergyConsumptionUpdate]
):
    pass


class BatteryCRUD(CRUDBase[Battery, BatteryCreate, BatteryUpdate]):
    pass


class BatteryStatusCRUD(
    CRUDBase[BatteryStatus, BatteryStatusCreate, BatteryStatusUpdate]
):
    pass


class TelemetryCRUD(CRUDBase[Telemetry, TelemetryCreate, TelemetryUpdate]):
    pass


class AlertCRUD(CRUDBase[Alert, AlertCreate, AlertUpdate]):
    pass


class SystemLogCRUD(CRUDBase[SystemLog, SystemLogCreate, SystemLogUpdate]):
    pass


weather_crud = WeatherCRUD(WeatherData, "Weather record")
solar_panel_crud = SolarPanelCRUD(SolarPanel, "Solar panel")
solar_prediction_crud = SolarPredictionCRUD(SolarPrediction, "Solar prediction")
energy_consumption_crud = EnergyConsumptionCRUD(
    EnergyConsumption, "Energy consumption record"
)
battery_crud = BatteryCRUD(Battery, "Battery")
battery_status_crud = BatteryStatusCRUD(BatteryStatus, "Battery status record")
telemetry_crud = TelemetryCRUD(Telemetry, "Telemetry record")
alert_crud = AlertCRUD(Alert, "Alert")
system_log_crud = SystemLogCRUD(SystemLog, "System log")
