from datetime import date
from datetime import datetime as DateTimeType

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    weather_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recorded_at: Mapped[DateTimeType] = mapped_column("datetime", DateTime, nullable=False, index=True)
    temperature: Mapped[float | None] = mapped_column(Numeric(5, 2))
    humidity: Mapped[float | None] = mapped_column(Numeric(5, 2))
    cloud_cover: Mapped[float | None] = mapped_column(Numeric(5, 2))
    wind_speed: Mapped[float | None] = mapped_column(Numeric(5, 2))
    ghi: Mapped[float | None] = mapped_column(Numeric(8, 2))
    dni: Mapped[float | None] = mapped_column(Numeric(8, 2))
    aqi: Mapped[int | None] = mapped_column(Integer)
    city: Mapped[str | None] = mapped_column(String(50), default="Delhi")


class SolarPanel(Base):
    __tablename__ = "solar_panel"

    panel_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    panel_name: Mapped[str] = mapped_column(String(50), nullable=False)
    panel_capacity: Mapped[float | None] = mapped_column(Numeric(6, 2))
    panel_efficiency: Mapped[float | None] = mapped_column(Numeric(5, 2))
    installation_date: Mapped[date | None] = mapped_column(Date)
    current_tilt: Mapped[float | None] = mapped_column(Numeric(5, 2))
    status: Mapped[str | None] = mapped_column(String(20), default="Active")

    predictions: Mapped[list["SolarPrediction"]] = relationship(
        "SolarPrediction", back_populates="panel"
    )
    telemetry_records: Mapped[list["Telemetry"]] = relationship(
        "Telemetry", back_populates="panel"
    )


class SolarPrediction(Base):
    __tablename__ = "solar_predictions"

    prediction_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    panel_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("solar_panel.panel_id"), nullable=False, index=True
    )
    weather_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("weather_data.weather_id"), nullable=False, index=True
    )
    prediction_time: Mapped[DateTimeType] = mapped_column(DateTime, nullable=False, index=True)
    predicted_tilt: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    expected_power: Mapped[float | None] = mapped_column(Numeric(8, 2))
    confidence_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    model_version: Mapped[str | None] = mapped_column(String(50))

    panel: Mapped["SolarPanel"] = relationship("SolarPanel", back_populates="predictions")


class EnergyConsumption(Base):
    __tablename__ = "energy_consumption"

    consumption_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    recorded_at: Mapped[DateTimeType] = mapped_column("datetime", DateTime, nullable=False)
    load_kw: Mapped[float] = mapped_column(Numeric(6, 2), nullable=False)
    temperature: Mapped[float | None] = mapped_column(Numeric(5, 2))
    humidity: Mapped[float | None] = mapped_column(Numeric(5, 2))
    hour_of_day: Mapped[int | None] = mapped_column(Integer)
    day_of_week: Mapped[str | None] = mapped_column(String(10))
    is_weekend: Mapped[bool | None] = mapped_column(Boolean)


class Battery(Base):
    __tablename__ = "battery"

    battery_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    battery_name: Mapped[str] = mapped_column(String(50), nullable=False)
    battery_type: Mapped[str | None] = mapped_column(String(30))
    capacity_mah: Mapped[int | None] = mapped_column(Integer)
    nominal_voltage: Mapped[float | None] = mapped_column(Numeric(4, 2))
    installation_date: Mapped[date | None] = mapped_column(Date)
    health_percentage: Mapped[float | None] = mapped_column(Numeric(5, 2))
    status: Mapped[str | None] = mapped_column(String(20), default="Active")

    status_records: Mapped[list["BatteryStatus"]] = relationship(
        "BatteryStatus", back_populates="battery"
    )
    telemetry_records: Mapped[list["Telemetry"]] = relationship(
        "Telemetry", back_populates="battery"
    )


class BatteryStatus(Base):
    __tablename__ = "battery_status"

    status_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    battery_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("battery.battery_id"), nullable=False, index=True
    )
    timestamp: Mapped[DateTimeType] = mapped_column(DateTime, nullable=False)
    soc: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    voltage: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    current: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    temperature: Mapped[float | None] = mapped_column(Numeric(5, 2))
    charging_status: Mapped[str] = mapped_column(String(20), nullable=False)

    battery: Mapped["Battery"] = relationship("Battery", back_populates="status_records")


class Telemetry(Base):
    __tablename__ = "telemetry"

    telemetry_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    panel_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("solar_panel.panel_id"), nullable=False, index=True
    )
    battery_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("battery.battery_id"), nullable=False, index=True
    )
    timestamp: Mapped[DateTimeType] = mapped_column(DateTime, nullable=False, index=True)
    voltage: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    current: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    power: Mapped[float] = mapped_column(Numeric(8, 2), nullable=False)
    lux: Mapped[int | None] = mapped_column(Integer)
    tilt_angle: Mapped[float | None] = mapped_column(Numeric(5, 2))
    soc: Mapped[float | None] = mapped_column(Numeric(5, 2))

    panel: Mapped["SolarPanel"] = relationship("SolarPanel", back_populates="telemetry_records")
    battery: Mapped["Battery"] = relationship("Battery", back_populates="telemetry_records")


class Alert(Base):
    __tablename__ = "alerts"

    alert_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    panel_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("solar_panel.panel_id"), index=True
    )
    battery_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("battery.battery_id"), index=True
    )
    alert_time: Mapped[DateTimeType] = mapped_column(DateTime, nullable=False)
    alert_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    message: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str | None] = mapped_column(String(20), default="Active", index=True)


class SystemLog(Base):
    __tablename__ = "system_logs"

    log_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[DateTimeType] = mapped_column(DateTime, nullable=False, index=True)
    module: Mapped[str] = mapped_column(String(50), nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20), nullable=False)
