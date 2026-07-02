"""
test_api.py -- Hermetic integration tests for the solar-position-api FastAPI app.

All tests are fully self-contained:
  - Model loading is patched so no real best_model.pkl is required.
  - Metadata is written to a temp directory so no src/model/ artefacts are needed.
  - fetch_live_weather is patched so no Open-Meteo network access is required.
  - The weather-client fallback tests patch _load_fallback_df so no
    data/delhi_features.csv is required.

Run with:
    pytest tests/test_api.py -v
"""

from __future__ import annotations

import io
import json
import sys
import tempfile
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app  # noqa: E402

# ---------------------------------------------------------------------------
# Shared fake constants
# ---------------------------------------------------------------------------

# Mirrors the real model_metadata.json schema exactly.
_FAKE_METADATA: dict = {
    "model_name": "lightgbm",
    "test_rmse": 35.3691,
    "test_mae": 16.5581,
    "test_r2": 0.9830,
    "feature_names": [
        "azimuth", "elevation", "sin_hour", "cos_hour",
        "sin_doy", "cos_doy", "temperature_2m",
        "relative_humidity_2m", "cloud_cover", "wind_speed_10m",
    ],
    "trained_at": "2026-06-21T11:32:01+00:00",
}

# A realistic midday weather snapshot (sun above horizon).
_FAKE_WEATHER_LIVE: dict = {
    "temperature_2m": 30.0,
    "relative_humidity_2m": 50.0,
    "cloud_cover": 20.0,
    "wind_speed_10m": 10.0,
    "weather_source": "live",
}

# A minimal DataFrame that satisfies _historical_average_fallback().
_FAKE_FALLBACK_DF = pd.DataFrame(
    {
        "temperature_2m": [28.0],
        "relative_humidity_2m": [55.0],
        "cloud_cover": [30.0],
        "wind_speed_10m": [8.0],
    },
    index=pd.DatetimeIndex(
        ["2024-06-21 12:00:00+05:30"],
        dtype="datetime64[ns, Asia/Kolkata]",
    ),
)


def _make_mock_model() -> MagicMock:
    """
    Return a mock scikit-learn-compatible estimator.

    predict() always returns 500.0 W/m² (a physically valid daytime value),
    ensuring that the response-schema tests receive sensible, deterministic
    numbers regardless of which code path is exercised.
    """
    mock = MagicMock()
    mock.predict.return_value = np.array([500.0])
    mock.feature_importances_ = np.ones(len(_FAKE_METADATA["feature_names"])) / len(
        _FAKE_METADATA["feature_names"]
    )
    return mock


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def api_client() -> Generator[TestClient, None, None]:
    """
    Yield a hermetic TestClient with the FastAPI lifespan active.

    Patches applied for the duration of the module:

    1. app.main._MODEL_PKL  -- redirected to a real (empty) tmp file so that
                               Path.exists() returns True without repo artefacts.
    2. app.main._MODEL_META -- redirected to a real tmp JSON file containing
                               _FAKE_METADATA so open() / json.load() work
                               naturally without any mock of builtins.
    3. joblib.load          -- returns _make_mock_model() so no .pkl
                               deserialisation occurs.
    4. app.main.fetch_live_weather
                            -- returns _FAKE_WEATHER_LIVE (deterministic, no
                               HTTP calls, no delhi_features.csv dependency).
    """
    mock_model = _make_mock_model()

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)

        # Write a real metadata JSON -- avoids patching builtins.open globally.
        fake_meta_path = tmp / "model_metadata.json"
        fake_meta_path.write_text(json.dumps(_FAKE_METADATA), encoding="utf-8")

        # An empty file makes Path.exists() return True; joblib.load is patched
        # to never actually read the bytes.
        fake_pkl_path = tmp / "best_model.pkl"
        fake_pkl_path.touch()

        with (
            patch("app.main._MODEL_PKL", fake_pkl_path),
            patch("app.main._MODEL_META", fake_meta_path),
            patch("joblib.load", return_value=mock_model),
            # Patch in app.main's namespace (where it is imported/called).
            # Use side_effect (not return_value) so that every call gets its
            # own fresh dict copy -- main.py does weather_raw.pop("weather_source")
            # which would mutate a shared return_value dict and cause a KeyError
            # on every subsequent request within the same test module.
            patch(
                "app.main.fetch_live_weather",
                side_effect=lambda *a, **kw: _FAKE_WEATHER_LIVE.copy(),
            ),
        ):
            with TestClient(app) as c:
                yield c


# ---------------------------------------------------------------------------
# /health
# ---------------------------------------------------------------------------

class TestHealth:
    def test_returns_200(self, api_client: TestClient) -> None:
        assert api_client.get("/health").status_code == 200

    def test_response_schema(self, api_client: TestClient) -> None:
        data = api_client.get("/health").json()
        assert "status" in data
        assert "model_loaded" in data
        assert "model_name" in data
        assert "timestamp" in data

    def test_status_ok_and_model_loaded(self, api_client: TestClient) -> None:
        data = api_client.get("/health").json()
        assert data["status"] == "ok"
        assert data["model_loaded"] is True

    def test_model_name_is_non_empty_string(self, api_client: TestClient) -> None:
        data = api_client.get("/health").json()
        assert isinstance(data["model_name"], str)
        assert len(data["model_name"]) > 0


# ---------------------------------------------------------------------------
# /predict
# ---------------------------------------------------------------------------

# All fields present on a successful /predict response.
EXPECTED_PREDICT_FIELDS: dict[str, type] = {
    "timestamp": str,
    "location": dict,
    "sun_above_horizon": bool,
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

VALID_COMPASS: frozenset[str] = frozenset({
    "North", "North-East", "East", "South-East",
    "South", "South-West", "West", "North-West",
    # physical override value returned when sun is below horizon
    "N/A (sun below horizon)",
})

VALID_WEATHER_SOURCES: frozenset[str] = frozenset({"live", "fallback_historical_average"})


class TestPredict:
    def test_returns_200(self, api_client: TestClient) -> None:
        assert api_client.get("/predict").status_code == 200

    def test_all_expected_fields_present(self, api_client: TestClient) -> None:
        data = api_client.get("/predict").json()
        for field in EXPECTED_PREDICT_FIELDS:
            assert field in data, f"Missing field: '{field}'"

    def test_field_types(self, api_client: TestClient) -> None:
        data = api_client.get("/predict").json()
        for field, expected_type in EXPECTED_PREDICT_FIELDS.items():
            assert isinstance(data[field], expected_type), (
                f"Field '{field}': expected {expected_type.__name__}, "
                f"got {type(data[field]).__name__}"
            )

    def test_location_has_lat_lon(self, api_client: TestClient) -> None:
        loc = api_client.get("/predict").json()["location"]
        assert "latitude" in loc and "longitude" in loc
        assert isinstance(loc["latitude"], float)
        assert isinstance(loc["longitude"], float)

    def test_radiation_is_non_negative(self, api_client: TestClient) -> None:
        assert api_client.get("/predict").json()["predicted_shortwave_radiation_wm2"] >= 0.0

    def test_energy_output_is_non_negative(self, api_client: TestClient) -> None:
        assert api_client.get("/predict").json()["estimated_energy_output_watts"] >= 0.0

    def test_tilt_in_valid_range(self, api_client: TestClient) -> None:
        tilt = api_client.get("/predict").json()["optimal_tilt_deg"]
        assert 0.0 <= tilt <= 90.0

    def test_compass_direction_is_valid(self, api_client: TestClient) -> None:
        assert api_client.get("/predict").json()["panel_facing_direction"] in VALID_COMPASS

    def test_weather_source_is_valid(self, api_client: TestClient) -> None:
        assert api_client.get("/predict").json()["weather_source"] in VALID_WEATHER_SOURCES

    def test_weather_dict_has_required_keys(self, api_client: TestClient) -> None:
        weather = api_client.get("/predict").json()["weather"]
        required = {"temperature_2m", "relative_humidity_2m", "cloud_cover", "wind_speed_10m"}
        assert required.issubset(set(weather.keys()))

    def test_sun_above_horizon_is_bool(self, api_client: TestClient) -> None:
        data = api_client.get("/predict").json()
        assert isinstance(data["sun_above_horizon"], bool)

    def test_physical_override_when_sun_below_horizon(self, api_client: TestClient) -> None:
        """
        When pvlib returns a negative elevation the physical override must fire:
        radiation = 0, energy = 0, tilt = 90, model_used = 'physical_override'.
        """
        # Inject a sub-horizon sun position while keeping everything else patched.
        night_solpos = MagicMock()
        night_solpos.__getitem__ = lambda self, key: {
            "azimuth":            MagicMock(iloc=[300.0]),
            "apparent_elevation": MagicMock(iloc=[-5.0]),
            "apparent_zenith":    MagicMock(iloc=[95.0]),
        }[key]

        import pvlib
        with patch.object(pvlib.solarposition, "get_solarposition", return_value=night_solpos):
            data = api_client.get("/predict").json()

        assert data["sun_above_horizon"] is False
        assert data["predicted_shortwave_radiation_wm2"] == 0.0
        assert data["estimated_energy_output_watts"] == 0.0
        assert data["optimal_tilt_deg"] == 90.0
        assert data["model_used"] == "physical_override"


# ---------------------------------------------------------------------------
# Weather client fallback (unit tests -- no TestClient needed)
# ---------------------------------------------------------------------------

class TestWeatherClientFallback:
    """
    Verify that fetch_live_weather() falls back gracefully when Open-Meteo is
    unreachable, without requiring data/delhi_features.csv on disk.

    _load_fallback_df is patched to return _FAKE_FALLBACK_DF, which is a
    minimal DataFrame satisfying the column/index requirements of
    _historical_average_fallback().
    """

    def _call_with_failing_http(self, http_exc: Exception) -> dict:
        from app.weather_client import fetch_live_weather
        from src.config import LATITUDE, LONGITUDE

        with (
            patch("requests.get", side_effect=http_exc),
            patch("app.weather_client._load_fallback_df", return_value=_FAKE_FALLBACK_DF),
        ):
            return fetch_live_weather(LATITUDE, LONGITUDE)

    def test_fallback_on_connection_error(self) -> None:
        result = self._call_with_failing_http(ConnectionError("network unreachable"))
        assert result["weather_source"] == "fallback_historical_average"
        for key in ("temperature_2m", "relative_humidity_2m", "cloud_cover", "wind_speed_10m"):
            assert key in result
            assert isinstance(result[key], float), f"'{key}' is not float"

    def test_fallback_on_timeout(self) -> None:
        import requests as req_module
        result = self._call_with_failing_http(req_module.exceptions.Timeout("timed out"))
        assert result["weather_source"] == "fallback_historical_average"

    def test_fallback_on_non_200_response(self) -> None:
        from app.weather_client import fetch_live_weather
        from src.config import LATITUDE, LONGITUDE

        bad_response = MagicMock()
        bad_response.status_code = 500
        bad_response.text = "Internal Server Error"

        with (
            patch("requests.get", return_value=bad_response),
            patch("app.weather_client._load_fallback_df", return_value=_FAKE_FALLBACK_DF),
        ):
            result = fetch_live_weather(LATITUDE, LONGITUDE)

        assert result["weather_source"] == "fallback_historical_average"
