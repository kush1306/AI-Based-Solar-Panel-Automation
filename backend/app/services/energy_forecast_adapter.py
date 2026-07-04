from datetime import datetime

from app.schemas.mock import EnergyForecastPoint, MockEnergyForecastResponse
from app.schemas.energy_model import EnergyForecastNextResponse


def map_energy_forecast_to_mock(
    forecast: EnergyForecastNextResponse,
) -> MockEnergyForecastResponse:
    points: list[EnergyForecastPoint] = []
    for index, row in enumerate(forecast.predictions):
        timestamp_raw = row.get("time")
        timestamp = (
            datetime.fromisoformat(str(timestamp_raw).replace("Z", "+00:00"))
            if timestamp_raw
            else datetime.utcnow()
        )
        load_kw = float(row.get("predicted_demand_kw") or row.get("predicted_load_kw") or 0)
        points.append(
            EnergyForecastPoint(
                hour=index,
                timestamp=timestamp,
                predicted_load_kw=load_kw,
                temperature=None,
                humidity=None,
            )
        )

    loads = [point.predicted_load_kw for point in points]
    peak_load = max(loads) if loads else 0.0
    peak_hour = loads.index(peak_load) if loads else 0

    start = points[0].timestamp if points else datetime.utcnow()
    end = points[-1].timestamp if points else start

    return MockEnergyForecastResponse(
        city="Delhi",
        forecast_start=start,
        forecast_end=end,
        horizon_hours=forecast.forecast_hours,
        total_predicted_load_kwh=float(forecast.total_predicted_kwh or sum(loads)),
        peak_load_kw=peak_load,
        peak_hour=peak_hour,
        average_load_kw=float(forecast.avg_demand_kw or (sum(loads) / len(loads) if loads else 0)),
        model_version="member2-demand-forecast",
        forecast=points,
        source="model2-service",
        note="Live forecast from the Energy Optimization API (Model 2).",
    )
