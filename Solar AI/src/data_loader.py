
from __future__ import annotations

import os
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")


OPENMETEO_COL_MAP = {
    "time": "time", "date": "time", "timestamp": "time",
    "temperature_2m (°c)":       "temperature_2m",
    "temperature_2m":            "temperature_2m",
    "relative_humidity_2m (%)":  "relative_humidity_2m",
    "relative_humidity_2m":      "relative_humidity_2m",
    "shortwave_radiation (w/m²)":"shortwave_radiation",
    "shortwave_radiation":       "shortwave_radiation",
    "direct_radiation":          "shortwave_radiation",
    "wind_speed_10m (km/h)":     "wind_speed_10m",
    "wind_speed_10m (m/s)":      "wind_speed_10m",
    "wind_speed_10m":            "wind_speed_10m",
    "precipitation (mm)":        "precipitation",
    "precipitation":             "precipitation",
    "cloud_cover (%)":           "cloud_cover",
    "cloud_cover":               "cloud_cover",
}

TARGET_COL = "demand_kw"

# ── 2. Local file loader ─────────────────────────────────────────────────────

def load_from_file(filepath: str) -> pd.DataFrame | None:
    """Load CSV from local path."""
    if not os.path.exists(filepath):
        return None
    try:
        df = pd.read_csv(filepath)
        df = _standardise(df)
        print(f"[data_loader] Local file OK — {len(df):,} rows from {filepath}")
        return df
    except Exception as e:
        print(f"[data_loader] Local load failed: {e}")
        return None


def _standardise(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    rename = {c: s for c, s in OPENMETEO_COL_MAP.items() if c in df.columns}
    df = df.rename(columns=rename)
    time_col = next((c for c in df.columns if c in ("time","date","timestamp")), None)
    if time_col is None:
        raise ValueError("No time/date column found.")
    if time_col != "time":
        df = df.rename(columns={time_col: "time"})
    df["time"] = pd.to_datetime(df["time"])
    if "wind_speed_10m" in df.columns and df["wind_speed_10m"].median() > 15:
        df["wind_speed_10m"] = df["wind_speed_10m"] / 3.6
    return df.sort_values("time").reset_index(drop=True)

def load_weather() -> pd.DataFrame:
    """
    Load Delhi weather dataset from the local repository.
    """

    path = "data/delhi_openmeteo_hourly.csv"

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    df = pd.read_csv(path)

    return _standardise(df)

HOURLY_SHAPE = np.array([
    0.15,0.12,0.10,0.10,0.12,0.20,   # 00-05
    0.55,0.80,0.90,0.70,0.55,0.50,   # 06-11
    0.50,0.50,0.48,0.45,0.50,0.60,   # 12-17
    0.70,0.90,1.00,0.95,0.80,0.40,   # 18-23
])

def generate_demand(weather_df: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    """
    Add realistic Indian household energy demand (kW) to a weather DataFrame.
    Based on a middle-class 3BHK in Delhi with 3kWp solar + 5kWh battery.
    """
    np.random.seed(seed)
    df    = weather_df.copy()
    n     = len(df)
    hour  = df["time"].dt.hour.values
    month = df["time"].dt.month.values
    dow   = df["time"].dt.dayofweek.values

    base = HOURLY_SHAPE[hour]

    seasonal = np.zeros(n)
    # AC 1.5-ton: Apr-Sep, 10am-10pm
    ac_m = np.isin(month, [4,5,6,7,8,9]) & ((hour>=10)&(hour<=22))
    ac_i = np.where(np.isin(month,[5,6]), 1.3, 0.9)
    seasonal += np.where(ac_m, 1.5*ac_i, 0)
    # Geyser 2kW: Nov-Feb, 6-8am
    gy_m = np.isin(month,[11,12,1,2]) & ((hour>=6)&(hour<=8))
    seasonal += np.where(gy_m, 2.0, 0)
    # Weekend +15%
    seasonal += np.where(dow>=5, 0.15, 0.0)
    # Temp-driven
    temp_b = np.zeros(n)
    if "temperature_2m" in df.columns:
        temp_b = np.clip((df["temperature_2m"].values - 30)*0.03, 0, 0.5)

    noise = np.random.normal(0, 0.05, n)
    df[TARGET_COL]  = np.clip(base + seasonal + temp_b + noise, 0.08, 5.5).round(4)
    df["demand_kwh"]= df[TARGET_COL]   # 1-h interval
    df["is_weekend"]= (dow>=5).astype(int)
    season_map = {1:"Winter",2:"Winter",3:"Spring",4:"Spring",5:"Summer",6:"Summer",
                  7:"Monsoon",8:"Monsoon",9:"Monsoon",10:"Autumn",11:"Autumn",12:"Winter"}
    df["season"] = pd.Series(month).map(season_map).values
    return df


def load_full_dataset(**kwargs) -> pd.DataFrame:
    """Convenience: load weather + add demand in one call."""
    weather = load_weather(**kwargs)
    return generate_demand(weather)
