from datetime import datetime, timedelta

from app.schemas.mock import (
    EnergyForecastPoint,
    MockEnergyForecastResponse,
    MockSolarPredictionResponse,
)


class MockAIService:
    """Returns realistic dummy AI predictions until real models are integrated."""

    def get_solar_prediction(
        self,
        *,
        panel_id: int = 1,
        weather_id: int = 1,
    ) -> MockSolarPredictionResponse:
        now = datetime.utcnow()
        predicted_tilt = 28.5
        expected_power = 4120.0
        return MockSolarPredictionResponse(
            panel_id=panel_id,
            weather_id=weather_id,
            prediction_time=now,
            predicted_tilt=predicted_tilt,
            expected_power=expected_power,
            confidence_score=0.91,
            model_version="mock-solar-v1.0",
            city="Delhi",
            irradiance_wm2=780.4,
            optimal_azimuth=180.0,
            estimated_generation_kwh=round(expected_power * 6.5 / 1000, 2),
        )

    def get_energy_forecast(
        self,
        *,
        horizon_hours: int = 24,
    ) -> MockEnergyForecastResponse:
        horizon = max(1, min(horizon_hours, 48))
        start = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        base_load = 3.8
        forecast: list[EnergyForecastPoint] = []

        for hour in range(horizon):
            timestamp = start + timedelta(hours=hour)
            hour_of_day = timestamp.hour
            # Realistic daily load curve: lower at night, peaks morning/evening
            if 6 <= hour_of_day <= 9:
                multiplier = 1.35
            elif 18 <= hour_of_day <= 22:
                multiplier = 1.45
            elif 0 <= hour_of_day <= 5:
                multiplier = 0.55
            else:
                multiplier = 1.0

            predicted_load = round(base_load * multiplier, 2)
            forecast.append(
                EnergyForecastPoint(
                    hour=hour,
                    timestamp=timestamp,
                    predicted_load_kw=predicted_load,
                    temperature=round(28 + (hour_of_day - 12) * 0.3, 1),
                    humidity=round(55 + (hour_of_day % 6), 1),
                )
            )

        loads = [point.predicted_load_kw for point in forecast]
        peak_load = max(loads)
        peak_hour = loads.index(peak_load)

        return MockEnergyForecastResponse(
            forecast_start=start,
            forecast_end=start + timedelta(hours=horizon - 1),
            horizon_hours=horizon,
            total_predicted_load_kwh=round(sum(loads), 2),
            peak_load_kw=peak_load,
            peak_hour=peak_hour,
            average_load_kw=round(sum(loads) / len(loads), 2),
            model_version="mock-energy-v1.0",
            forecast=forecast,
        )


mock_ai_service = MockAIService()
