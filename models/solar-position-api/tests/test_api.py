"""
test_api.py -- Integration tests for the solar-position-api FastAPI application.

Run with:
    pytest tests/test_api.py -v
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# Ensure project root is on the path before importing app
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app  # noqa: E402

client = TestClient(app)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def api_client():
    """Yield a TestClient with the app lifespan active."""
    with TestClient(app) as c:
        yield c


# ---------------------------------------------------------------------------
# /health
# ---------------------------------------------------------------------------

class TestHealth:
    def test_returns_200(self, api_client: TestClient):
        response = api_client.get("/health")
        assert response.status_code == 200, response.text

    def test_response_schema(self, api_client: TestClient):
        data = api_client.get("/health").json()
        assert "status" in data
        assert "model_loaded" in data
        assert "model_name" in data
        assert "timestamp" in data

    def test_status_is_ok_when_model_loaded(self, api_client: TestClient):
        data = api_client.get("/health").json()
        # If model files exist and loaded correctly this must be "ok"
        assert data["status"] == "ok"
        assert data["model_loaded"] is True

    def test_model_name_is_string(self, api_client: TestClient):
        data = api_client.get("/health").json()
        if data["model_loaded"]:
            assert isinstance(data["model_name"], str)
            assert len(data["model_name"]) > 0


# ---------------------------------------------------------------------------
# /predict
# ---------------------------------------------------------------------------

EXPECTED_PREDICT_FIELDS = {
    "timestamp": str,
    "location": dict,
    "azimuth_deg": float,
    "elevation_deg": float,
    "zenith_deg": float,
    "predicted_shortwave_radiation_wm2": float,
    "estimated_energy_output_watts": float,
    "optimal_tilt_deg": float,
    "panel_facing_direction": str,
    "model_used": str,
    "weather_source": str,
    "weather": dict,
}

VALID_COMPASS = {
    "North", "North-East", "East", "South-East",
    "South", "South-West", "West", "North-West",
}

VALID_WEATHER_SOURCES = {"live", "fallback_historical_average"}


class TestPredict:
    def test_returns_200(self, api_client: TestClient):
        response = api_client.get("/predict")
        assert response.status_code == 200, response.text

    def test_all_expected_fields_present(self, api_client: TestClient):
        data = api_client.get("/predict").json()
        for field in EXPECTED_PREDICT_FIELDS:
            assert field in data, f"Missing field: {field}"

    def test_field_types(self, api_client: TestClient):
        data = api_client.get("/predict").json()
        for field, expected_type in EXPECTED_PREDICT_FIELDS.items():
            assert isinstance(data[field], expected_type), (
                f"Field '{field}': expected {expected_type.__name__}, "
                f"got {type(data[field]).__name__}"
            )

    def test_location_has_lat_lon(self, api_client: TestClient):
        location = api_client.get("/predict").json()["location"]
        assert "latitude" in location
        assert "longitude" in location
        assert isinstance(location["latitude"], float)
        assert isinstance(location["longitude"], float)

    def test_radiation_is_non_negative(self, api_client: TestClient):
        data = api_client.get("/predict").json()
        assert data["predicted_shortwave_radiation_wm2"] >= 0.0

    def test_energy_output_is_non_negative(self, api_client: TestClient):
        data = api_client.get("/predict").json()
        assert data["estimated_energy_output_watts"] >= 0.0

    def test_tilt_in_valid_range(self, api_client: TestClient):
        data = api_client.get("/predict").json()
        assert 0.0 <= data["optimal_tilt_deg"] <= 90.0

    def test_compass_direction_is_valid(self, api_client: TestClient):
        data = api_client.get("/predict").json()
        assert data["panel_facing_direction"] in VALID_COMPASS

    def test_weather_source_is_valid(self, api_client: TestClient):
        data = api_client.get("/predict").json()
        assert data["weather_source"] in VALID_WEATHER_SOURCES

    def test_weather_dict_has_four_keys(self, api_client: TestClient):
        weather = api_client.get("/predict").json()["weather"]
        required = {"temperature_2m", "relative_humidity_2m", "cloud_cover", "wind_speed_10m"}
        assert required.issubset(set(weather.keys()))


# ---------------------------------------------------------------------------
# Weather client fallback
# ---------------------------------------------------------------------------

class TestWeatherClientFallback:
    """
    Verify that fetch_live_weather() gracefully falls back to the historical
    average when the Open-Meteo API is unreachable.
    """

    def test_fallback_used_when_request_fails(self):
        from app.weather_client import fetch_live_weather
        from src.config import LATITUDE, LONGITUDE

        # Simulate a connection error on every HTTP GET
        with patch("requests.get", side_effect=ConnectionError("network unreachable")):
            result = fetch_live_weather(LATITUDE, LONGITUDE)

        assert result["weather_source"] == "fallback_historical_average"
        # All four weather fields must be present and numeric
        for key in ("temperature_2m", "relative_humidity_2m", "cloud_cover", "wind_speed_10m"):
            assert key in result, f"Missing key in fallback result: {key}"
            assert isinstance(result[key], float), f"Key '{key}' is not float"

    def test_fallback_used_when_timeout(self):
        from app.weather_client import fetch_live_weather
        from src.config import LATITUDE, LONGITUDE
        import requests as req_module

        with patch("requests.get", side_effect=req_module.exceptions.Timeout("timed out")):
            result = fetch_live_weather(LATITUDE, LONGITUDE)

        assert result["weather_source"] == "fallback_historical_average"

    def test_fallback_used_on_non_200_response(self):
        from app.weather_client import fetch_live_weather
        from src.config import LATITUDE, LONGITUDE
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        with patch("requests.get", return_value=mock_response):
            result = fetch_live_weather(LATITUDE, LONGITUDE)

        assert result["weather_source"] == "fallback_historical_average"
