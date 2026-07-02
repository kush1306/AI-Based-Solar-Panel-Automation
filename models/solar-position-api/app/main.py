"""
main.py -- FastAPI application for the solar-position-api service.

Endpoints
---------
GET /health   -- Liveness / model-loaded check.
GET /predict  -- Zero-input prediction: uses server time + configured
                 location to return irradiance forecast, energy output,
                 and optimal panel geometry.

Start the server:
    uvicorn app.main:app --reload
"""

from __future__ import annotations

import json
import logging
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
import pvlib
import pytz
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (  # noqa: E402
    LATITUDE,
    LONGITUDE,
    PANEL_AREA_M2,
    PANEL_EFFICIENCY,
    TIMEZONE,
)
from app.energy import (  # noqa: E402
    azimuth_to_compass_direction,
    compute_energy_output,
    compute_optimal_tilt,
)
from app.weather_client import fetch_live_weather  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_MODEL_PKL = PROJECT_ROOT / "src" / "model" / "best_model.pkl"
_MODEL_META = PROJECT_ROOT / "src" / "model" / "model_metadata.json"

# ---------------------------------------------------------------------------
# Application state (loaded once at startup, shared across all requests)
# ---------------------------------------------------------------------------
_state: dict[str, Any] = {
    "model": None,
    "metadata": None,
    "model_loaded": False,
    "load_error": None,
}


# ---------------------------------------------------------------------------
# Lifespan: load model exactly once at startup
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup: ensure the model is available (training if necessary), then load
    it into memory exactly once so all requests share a single instance.
    Shutdown: nothing to clean up.
    """
    try:
        if _MODEL_PKL.exists():
            # Happy path: model artefacts are present (committed to repo or
            # previously trained in this environment).
            logger.info(
                "Model found at '%s' -- loading from disk.", _MODEL_PKL
            )
        else:
            # Cold-start path: artefacts are missing (fresh clone, new
            # environment, CI runner without cached layers, etc.).
            # Run the full training pipeline to produce them before loading.
            logger.warning(
                "Model not found at '%s' -- running training pipeline before "
                "startup.  This may take several minutes.",
                _MODEL_PKL,
            )
            from src.train import run_training_pipeline  # noqa: PLC0415
            run_training_pipeline()
            logger.info("Training pipeline complete -- model artefacts written.")

        _state["model"] = joblib.load(_MODEL_PKL)
        with open(_MODEL_META, "r", encoding="utf-8") as fh:
            _state["metadata"] = json.load(fh)
        _state["model_loaded"] = True
        logger.info(
            "Model loaded successfully -- name: %s | test_rmse: %.4f",
            _state["metadata"]["model_name"],
            _state["metadata"]["test_rmse"],
        )
    except Exception as exc:  # noqa: BLE001
        _state["load_error"] = str(exc)
        logger.error("Failed to load or train model: %s", exc)
    yield
    logger.info("Server shutting down.")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Solar Position API",
    description=(
        "Real-time solar panel angle optimisation for New Delhi. "
        "Combines deterministic sun-position calculations (pvlib) with "
        "ML-based shortwave irradiance prediction (LightGBM)."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------
class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_name: str | None
    timestamp: str


class PredictResponse(BaseModel):
    timestamp: str
    location: dict[str, float]
    sun_above_horizon: bool
    azimuth_deg: float
    elevation_deg: float
    zenith_deg: float
    predicted_shortwave_radiation_wm2: float
    estimated_energy_output_watts: float
    optimal_tilt_deg: float
    panel_facing_direction: str
    model_used: str
    weather_source: str
    weather: dict[str, float]


# ---------------------------------------------------------------------------
# Helper: compute current sun position
# ---------------------------------------------------------------------------
def _get_sun_position(now: datetime) -> dict[str, float]:
    """
    Return azimuth, apparent_elevation, and apparent_zenith for the
    configured location at the given timezone-aware datetime.
    """
    times = pd.DatetimeIndex([now])
    solpos = pvlib.solarposition.get_solarposition(
        time=times,
        latitude=LATITUDE,
        longitude=LONGITUDE,
    )
    return {
        "azimuth": float(solpos["azimuth"].iloc[0]),
        "elevation": float(solpos["apparent_elevation"].iloc[0]),
        "zenith": float(solpos["apparent_zenith"].iloc[0]),
    }


# ---------------------------------------------------------------------------
# Helper: build feature vector
# ---------------------------------------------------------------------------
def _build_feature_vector(
    sun: dict[str, float],
    weather: dict[str, float],
    now: datetime,
    feature_names: list[str],
) -> pd.DataFrame:
    """
    Assemble the feature row in the exact order the model was trained on.
    Cyclic features are recomputed here to avoid importing features.py at
    request time.
    """
    hour = float(now.hour)
    doy = float(now.timetuple().tm_yday)

    values = {
        "azimuth": sun["azimuth"],
        "elevation": sun["elevation"],
        "sin_hour": np.sin(2 * np.pi * hour / 24.0),
        "cos_hour": np.cos(2 * np.pi * hour / 24.0),
        "sin_doy": np.sin(2 * np.pi * doy / 365.25),
        "cos_doy": np.cos(2 * np.pi * doy / 365.25),
        "temperature_2m": weather["temperature_2m"],
        "relative_humidity_2m": weather["relative_humidity_2m"],
        "cloud_cover": weather["cloud_cover"],
        "wind_speed_10m": weather["wind_speed_10m"],
    }

    # Respect the exact column order from model_metadata.json
    row = {feat: values[feat] for feat in feature_names}
    return pd.DataFrame([row])


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/health", response_model=HealthResponse, tags=["Ops"])
def health() -> HealthResponse:
    """
    Liveness and model-readiness check.

    Returns 200 with model_loaded=true when the service is ready to
    serve predictions. Returns 503 if the model failed to load at startup.
    """
    now_utc = datetime.now(pytz.utc).isoformat()
    model_name = (
        _state["metadata"]["model_name"] if _state["model_loaded"] else None
    )

    if not _state["model_loaded"]:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "model_loaded": False,
                "model_name": None,
                "timestamp": now_utc,
                "error": _state.get("load_error", "Unknown error"),
            },
        )

    return HealthResponse(
        status="ok",
        model_loaded=True,
        model_name=model_name,
        timestamp=now_utc,
    )


@app.get("/predict", response_model=PredictResponse, tags=["Inference"])
def predict() -> PredictResponse:
    """
    Generate a solar panel optimisation recommendation for the current moment.

    No input required -- the server uses its configured location (New Delhi)
    and the current wall-clock time automatically.

    Returns predicted irradiance, estimated power output, optimal panel tilt,
    and the compass direction the panel should face.
    """
    if not _state["model_loaded"]:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded. Check /health for details.",
        )

    try:
        # 1. Current time in the configured timezone
        tz = pytz.timezone(TIMEZONE)
        now = datetime.now(tz)
        timestamp_str = now.isoformat()

        # 2. Sun position
        sun = _get_sun_position(now)
        sun_above_horizon: bool = sun["elevation"] > 0.0

        # 3. Live weather (with automatic fallback)
        weather_raw = fetch_live_weather(LATITUDE, LONGITUDE)
        weather_source = weather_raw.pop("weather_source")
        weather_values: dict[str, float] = weather_raw

        # ------------------------------------------------------------------
        # Physical constraint: shortwave radiation is identically zero when
        # the sun is at or below the horizon (elevation <= 0).  The ML model
        # was trained on daytime data and has no physical guarantee of
        # outputting zero for negative elevations -- it may produce spurious
        # positive values.  We therefore short-circuit the model entirely
        # and return the physically correct answer directly.
        # ------------------------------------------------------------------
        if not sun_above_horizon:
            logger.info(
                "Sun below horizon (elevation=%.4f deg) -- skipping ML model, "
                "returning physical zero for radiation and energy.",
                sun["elevation"],
            )
            return PredictResponse(
                timestamp=timestamp_str,
                location={"latitude": LATITUDE, "longitude": LONGITUDE},
                sun_above_horizon=False,
                azimuth_deg=round(sun["azimuth"], 4),
                elevation_deg=round(sun["elevation"], 4),
                zenith_deg=round(sun["zenith"], 4),
                predicted_shortwave_radiation_wm2=0.0,
                estimated_energy_output_watts=0.0,
                optimal_tilt_deg=90.0,   # panel stowed flat at night
                panel_facing_direction="N/A (sun below horizon)",
                model_used="physical_override",
                weather_source=weather_source,
                weather={k: round(v, 4) for k, v in weather_values.items()},
            )

        # 4. Feature vector (only reached when sun is above the horizon)
        feature_names: list[str] = _state["metadata"]["feature_names"]
        X = _build_feature_vector(sun, weather_values, now, feature_names)

        # 5. Predict irradiance
        y_pred = float(_state["model"].predict(X)[0])
        y_pred = max(0.0, y_pred)   # belt-and-suspenders guard

        # 6. Derived quantities
        energy_watts = compute_energy_output(y_pred, PANEL_AREA_M2, PANEL_EFFICIENCY)
        optimal_tilt = compute_optimal_tilt(sun["elevation"])
        facing = azimuth_to_compass_direction(sun["azimuth"])

        logger.info(
            "Prediction -- radiation: %.2f W/m2 | energy: %.2f W | "
            "tilt: %.1f deg | facing: %s | source: %s",
            y_pred, energy_watts, optimal_tilt, facing, weather_source,
        )

        return PredictResponse(
            timestamp=timestamp_str,
            location={"latitude": LATITUDE, "longitude": LONGITUDE},
            sun_above_horizon=True,
            azimuth_deg=round(sun["azimuth"], 4),
            elevation_deg=round(sun["elevation"], 4),
            zenith_deg=round(sun["zenith"], 4),
            predicted_shortwave_radiation_wm2=round(y_pred, 4),
            estimated_energy_output_watts=round(energy_watts, 4),
            optimal_tilt_deg=round(optimal_tilt, 4),
            panel_facing_direction=facing,
            model_used=_state["metadata"]["model_name"],
            weather_source=weather_source,
            weather={k: round(v, 4) for k, v in weather_values.items()},
        )

    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        logger.exception("Prediction failed unexpectedly: %s", exc)
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {exc}",
        ) from exc
