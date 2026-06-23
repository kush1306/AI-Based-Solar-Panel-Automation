"""
weather_client.py -- Fetch real-time weather from Open-Meteo with a
graceful historical-average fallback.

The fallback strategy avoids a hard dependency on external connectivity:
if Open-Meteo is unreachable or returns an error, the client loads the
locally cached feature dataset and computes the mean weather conditions
for the current hour-of-day and the current day-of-year window (+/- 7 days),
giving a physically reasonable estimate without crashing the prediction
endpoint.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd
import requests

logger = logging.getLogger(__name__)

# Lazy import -- avoids a circular import chain at module load time.
_CONFIG_LOADED = False
_LATITUDE: float = 0.0
_LONGITUDE: float = 0.0
_BASE_URL: str = ""
_TIMEOUT: int = 5
_FEATURES_CSV: str = ""
_TIMEZONE: str = "UTC"

# Fallback window: include rows within +/- DOY_WINDOW days of current DOY
_DOY_WINDOW = 7

# Cached fallback dataframe (loaded once on first fallback hit)
_fallback_df: pd.DataFrame | None = None


def _load_config() -> None:
    """Load config constants lazily to prevent circular imports."""
    global _CONFIG_LOADED, _LATITUDE, _LONGITUDE, _BASE_URL, _TIMEOUT, _FEATURES_CSV, _TIMEZONE
    if _CONFIG_LOADED:
        return
    import sys
    from pathlib import Path as _Path
    sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
    from src.config import (
        LATITUDE, LONGITUDE, OPEN_METEO_BASE_URL,
        OPEN_METEO_TIMEOUT_SECONDS, TIMEZONE,
    )
    from src.features import FEATURES_CSV
    _LATITUDE = LATITUDE
    _LONGITUDE = LONGITUDE
    _BASE_URL = OPEN_METEO_BASE_URL
    _TIMEOUT = OPEN_METEO_TIMEOUT_SECONDS
    _FEATURES_CSV = str(FEATURES_CSV)
    _TIMEZONE = TIMEZONE
    _CONFIG_LOADED = True


def _load_fallback_df() -> pd.DataFrame:
    """Load and cache the features CSV for fallback computations."""
    global _fallback_df
    if _fallback_df is not None:
        return _fallback_df

    _load_config()
    path = Path(_FEATURES_CSV)
    if not path.exists():
        raise FileNotFoundError(
            f"Fallback dataset not found at '{path}'. "
            "Run `python -m src.features` to generate it."
        )
    df = pd.read_csv(path, index_col="time", parse_dates=True)
    if df.index.tz is None:
        df.index = df.index.tz_localize(_TIMEZONE)
    _fallback_df = df
    return _fallback_df


def _historical_average_fallback() -> dict:
    """
    Compute mean weather values from the historical feature dataset,
    filtered to the current hour-of-day and a DOY window of +/- 7 days.

    Returns
    -------
    dict with keys: temperature_2m, relative_humidity_2m, cloud_cover,
                    wind_speed_10m, source
    """
    import datetime
    import pytz

    _load_config()
    tz = pytz.timezone(_TIMEZONE)
    now = datetime.datetime.now(tz)
    current_hour = now.hour
    current_doy = now.timetuple().tm_yday

    df = _load_fallback_df()

    # Filter by hour-of-day
    hour_mask = df.index.hour == current_hour

    # Filter by DOY window (handles year-boundary wrap-around)
    doy = df.index.day_of_year
    lower = current_doy - _DOY_WINDOW
    upper = current_doy + _DOY_WINDOW
    if lower < 1:
        doy_mask = (doy >= (365 + lower)) | (doy <= upper)
    elif upper > 365:
        doy_mask = (doy >= lower) | (doy <= (upper - 365))
    else:
        doy_mask = (doy >= lower) & (doy <= upper)

    subset = df.loc[hour_mask & doy_mask]

    if subset.empty:
        # Widen to full hour match if the window is empty (edge case)
        subset = df.loc[hour_mask]

    weather_cols = ["temperature_2m", "relative_humidity_2m", "cloud_cover", "wind_speed_10m"]
    means = subset[weather_cols].mean()
    return {col: float(means[col]) for col in weather_cols}


def fetch_live_weather(latitude: float, longitude: float) -> dict:
    """
    Fetch current hourly weather from the Open-Meteo free forecast API.

    On any failure (timeout, connection error, non-200 status, malformed
    JSON), falls back to a historical average from the local dataset instead
    of raising, ensuring the prediction endpoint always returns a response.

    Parameters
    ----------
    latitude : float
    longitude : float

    Returns
    -------
    dict with keys:
        temperature_2m        (float, deg C)
        relative_humidity_2m  (float, %)
        cloud_cover           (float, %)
        wind_speed_10m        (float, m/s)
        weather_source        ("live" | "fallback_historical_average")
    """
    _load_config()

    weather_vars = [
        "temperature_2m",
        "relative_humidity_2m",
        "cloud_cover",
        "wind_speed_10m",
    ]

    try:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ",".join(weather_vars),
            "timezone": _TIMEZONE,
        }
        response = requests.get(_BASE_URL, params=params, timeout=_TIMEOUT)

        if response.status_code != 200:
            raise ValueError(
                f"Open-Meteo returned HTTP {response.status_code}: {response.text[:200]}"
            )

        payload = response.json()
        current = payload.get("current")
        if not current:
            raise ValueError("Open-Meteo response missing 'current' key.")

        result = {var: float(current[var]) for var in weather_vars}
        result["weather_source"] = "live"
        logger.info(
            "Live weather fetched successfully for (%.4f, %.4f).", latitude, longitude
        )
        return result

    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "Open-Meteo request failed (%s: %s) -- using historical average fallback.",
            type(exc).__name__, exc,
        )
        fallback = _historical_average_fallback()
        fallback["weather_source"] = "fallback_historical_average"
        return fallback
