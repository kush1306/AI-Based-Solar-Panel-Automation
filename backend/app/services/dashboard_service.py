from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import (
    Alert,
    BatteryStatus,
    EnergyConsumption,
    SolarPanel,
    SolarPrediction,
    SystemLog,
    Telemetry,
    WeatherData,
)
from app.schemas.dashboard import ChartDataPoint, DashboardCharts, DashboardOverview
from app.schemas.entities import AlertResponse, SystemLogResponse


class DashboardService:
    def get_overview(self, db: Session) -> DashboardOverview:
        latest_telemetry = db.scalar(
            select(Telemetry).order_by(Telemetry.timestamp.desc()).limit(1)
        )
        latest_battery = db.scalar(
            select(BatteryStatus).order_by(BatteryStatus.timestamp.desc()).limit(1)
        )
        latest_weather = db.scalar(
            select(WeatherData).order_by(WeatherData.recorded_at.desc()).limit(1)
        )
        latest_prediction = db.scalar(
            select(SolarPrediction).order_by(SolarPrediction.prediction_time.desc()).limit(1)
        )

        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_energy = db.scalar(
            select(func.coalesce(func.sum(EnergyConsumption.load_kw), 0)).where(
                EnergyConsumption.recorded_at >= today_start
            )
        )

        active_alerts_count = db.scalar(
            select(func.count()).select_from(Alert).where(Alert.status == "Active")
        ) or 0

        active_alerts = db.scalars(
            select(Alert)
            .where(Alert.status == "Active")
            .order_by(Alert.alert_time.desc())
            .limit(5)
        ).all()

        recent_logs = db.scalars(
            select(SystemLog).order_by(SystemLog.timestamp.desc()).limit(5)
        ).all()

        active_panels = db.scalar(
            select(func.count()).select_from(SolarPanel).where(SolarPanel.status == "Active")
        ) or 0
        total_panels = db.scalar(select(func.count()).select_from(SolarPanel)) or 0

        if total_panels == 0:
            system_status = "unknown"
        elif active_panels == total_panels:
            system_status = "online"
        elif active_panels > 0:
            system_status = "degraded"
        else:
            system_status = "offline"

        return DashboardOverview(
            current_power=float(latest_telemetry.power) if latest_telemetry else 0.0,
            battery_soc=float(latest_battery.soc) if latest_battery else 0.0,
            temperature=float(latest_weather.temperature)
            if latest_weather and latest_weather.temperature is not None
            else None,
            humidity=float(latest_weather.humidity)
            if latest_weather and latest_weather.humidity is not None
            else None,
            optimal_tilt=float(latest_prediction.predicted_tilt) if latest_prediction else None,
            today_energy=float(today_energy or 0),
            system_status=system_status,
            active_alerts=active_alerts_count,
            recent_logs=[SystemLogResponse.model_validate(log) for log in recent_logs],
            active_alert_items=[AlertResponse.model_validate(alert) for alert in active_alerts],
        )

    def get_charts(self, db: Session, hours: int = 24) -> DashboardCharts:
        since = datetime.now() - timedelta(hours=hours)

        telemetry_rows = db.scalars(
            select(Telemetry)
            .where(Telemetry.timestamp >= since)
            .order_by(Telemetry.timestamp.asc())
        ).all()

        battery_rows = db.scalars(
            select(BatteryStatus)
            .where(BatteryStatus.timestamp >= since)
            .order_by(BatteryStatus.timestamp.asc())
        ).all()

        weather_rows = db.scalars(
            select(WeatherData)
            .where(WeatherData.recorded_at >= since)
            .order_by(WeatherData.recorded_at.asc())
        ).all()

        energy_rows = db.scalars(
            select(EnergyConsumption)
            .where(EnergyConsumption.recorded_at >= since)
            .order_by(EnergyConsumption.recorded_at.asc())
        ).all()

        tilt_predictions = db.scalars(
            select(SolarPrediction)
            .where(SolarPrediction.prediction_time >= since)
            .order_by(SolarPrediction.prediction_time.asc())
        ).all()

        return DashboardCharts(
            power_generation=[
                ChartDataPoint(
                    timestamp=row.timestamp,
                    value=float(row.power),
                    label=f"Panel {row.panel_id}",
                )
                for row in telemetry_rows
            ],
            battery_soc=[
                ChartDataPoint(timestamp=row.timestamp, value=float(row.soc))
                for row in battery_rows
            ],
            temperature=[
                ChartDataPoint(
                    timestamp=row.recorded_at,
                    value=float(row.temperature or 0),
                )
                for row in weather_rows
            ],
            energy_consumption=[
                ChartDataPoint(
                    timestamp=row.recorded_at,
                    value=float(row.load_kw),
                )
                for row in energy_rows
            ],
            telemetry=[
                ChartDataPoint(
                    timestamp=row.timestamp,
                    value=float(row.power),
                    label="power_w",
                )
                for row in telemetry_rows
            ],
            predicted_tilt=[
                ChartDataPoint(
                    timestamp=row.prediction_time,
                    value=float(row.predicted_tilt),
                )
                for row in tilt_predictions
            ],
        )


dashboard_service = DashboardService()
