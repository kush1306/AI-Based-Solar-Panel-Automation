"""
features.py — Feature engineering for the solar-position-api project.

Pipeline
--------
1. add_sun_position_features : deterministic sun geometry via pvlib.
2. add_cyclic_time_features  : hour-of-day and day-of-year encoded as
                               sine/cosine pairs so the model sees
                               temporal periodicity as a smooth signal.
3. build_feature_dataset     : orchestrates the full pipeline and writes
                               data/delhi_features.csv.
4. chronological_train_test_split : leakage-safe time-series split.

Run standalone:
    python -m src.features
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pvlib

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (  # noqa: E402
    CLEANED_CSV,
    LATITUDE,
    LONGITUDE,
    TIMEZONE,
)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Output path
# ---------------------------------------------------------------------------
FEATURES_CSV = Path(PROJECT_ROOT) / "data" / "delhi_features.csv"

# Final feature columns exposed to the model
FEATURE_COLS: list[str] = [
    "azimuth",
    "elevation",
    "sin_hour",
    "cos_hour",
    "sin_doy",
    "cos_doy",
    "temperature_2m",
    "relative_humidity_2m",
    "cloud_cover",
    "wind_speed_10m",
]
TARGET_COL: str = "shortwave_radiation"


# ---------------------------------------------------------------------------
# 1. Sun position features
# ---------------------------------------------------------------------------

def add_sun_position_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute deterministic solar geometry for every timestamp and attach the
    results as new columns on a copy of *df*.

    Uses ``pvlib.solarposition.get_solarposition`` which implements the
    NREL Solar Position Algorithm (SPA) — accurate to ±0.0003° over the
    period 2000–2050.

    New columns
    -----------
    azimuth   : Solar azimuth angle (degrees, 0° = North, clockwise).
    elevation : Apparent solar elevation angle above the horizon (degrees),
                corrected for atmospheric refraction.
    zenith    : Apparent solar zenith angle (degrees); = 90° - elevation.

    Parameters
    ----------
    df : pd.DataFrame
        Must have a timezone-aware DatetimeTZDtype index.

    Returns
    -------
    pd.DataFrame
        Original dataframe with three additional columns.
    """
    logger.info("Computing sun position features for %d timestamps ...", len(df))

    solpos = pvlib.solarposition.get_solarposition(
        time=df.index,
        latitude=LATITUDE,
        longitude=LONGITUDE,
        # Altitude defaults to 0 m (sea level) — acceptable for Delhi (~216 m).
        # Passing the index directly uses its timezone; no conversion needed.
    )

    df = df.copy()
    df["azimuth"] = solpos["azimuth"].values
    df["elevation"] = solpos["apparent_elevation"].values
    df["zenith"] = solpos["apparent_zenith"].values

    logger.info(
        "Sun position features added — azimuth [%.1f°, %.1f°], "
        "elevation [%.1f°, %.1f°].",
        df["azimuth"].min(), df["azimuth"].max(),
        df["elevation"].min(), df["elevation"].max(),
    )
    return df


# ---------------------------------------------------------------------------
# 2. Cyclic time features
# ---------------------------------------------------------------------------

def add_cyclic_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encode periodic time signals as sine/cosine pairs so that the model
    perceives temporal continuity (e.g., hour 23 is adjacent to hour 0).

    New columns
    -----------
    sin_hour, cos_hour : Hour of day encoded cyclically (period = 24 h).
    sin_doy,  cos_doy  : Day of year encoded cyclically (period = 365.25 d).

    Parameters
    ----------
    df : pd.DataFrame
        Must have a DatetimeTZDtype index.

    Returns
    -------
    pd.DataFrame
        Original dataframe with four additional columns.
    """
    df = df.copy()

    hour = df.index.hour.astype(float)
    df["sin_hour"] = np.sin(2 * np.pi * hour / 24.0)
    df["cos_hour"] = np.cos(2 * np.pi * hour / 24.0)

    doy = df.index.day_of_year.astype(float)
    df["sin_doy"] = np.sin(2 * np.pi * doy / 365.25)
    df["cos_doy"] = np.cos(2 * np.pi * doy / 365.25)

    logger.info("Cyclic time features added (sin/cos hour and day-of-year).")
    return df


# ---------------------------------------------------------------------------
# 3. Full feature dataset builder
# ---------------------------------------------------------------------------

def build_feature_dataset(
    cleaned_path: str | Path = CLEANED_CSV,
    output_path: str | Path = FEATURES_CSV,
) -> pd.DataFrame:
    """
    Orchestrates the complete feature engineering pipeline:

    1. Load the cleaned CSV (produced by data_preprocessing.py).
    2. Add deterministic sun position features.
    3. Add cyclic time features.
    4. Select the canonical feature + target columns.
    5. Persist the result to *output_path*.

    Parameters
    ----------
    cleaned_path : str | Path
        Path to data/delhi_cleaned.csv.
    output_path : str | Path
        Destination for the enriched feature CSV.

    Returns
    -------
    pd.DataFrame
        Feature dataset with FEATURE_COLS + TARGET_COL.
    """
    cleaned_path = Path(cleaned_path)
    if not cleaned_path.exists():
        raise FileNotFoundError(
            f"Cleaned CSV not found at '{cleaned_path}'. "
            "Run `python -m src.data_preprocessing` first."
        )

    logger.info("Loading cleaned data from '%s' ...", cleaned_path.resolve())
    df = pd.read_csv(cleaned_path, index_col="time", parse_dates=True)

    # Restore timezone (pd.read_csv strips tzinfo from the index string)
    if df.index.tz is None:
        df.index = df.index.tz_localize(TIMEZONE)

    df = add_sun_position_features(df)
    df = add_cyclic_time_features(df)

    # Validate that all required columns are present before selecting
    required = FEATURE_COLS + [TARGET_COL]
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        raise ValueError(
            f"The following required columns are absent after feature engineering: "
            f"{missing_cols}. Present columns: {list(df.columns)}"
        )

    df = df[required]

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path)
    logger.info("Feature dataset saved to '%s'.", output_path.resolve())

    logger.info(
        "\n"
        "========== Feature Dataset Summary ==========\n"
        "  Shape    : %s\n"
        "  Columns  : %s\n"
        "  Target   : %s\n"
        "  Date range: %s  ->  %s\n"
        "=============================================",
        df.shape,
        list(df.columns),
        TARGET_COL,
        df.index.min(),
        df.index.max(),
    )
    return df


# ---------------------------------------------------------------------------
# 4. Chronological train/test split
# ---------------------------------------------------------------------------

def chronological_train_test_split(
    df: pd.DataFrame,
    test_years: int = 2,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split the feature dataset into training and test sets **chronologically**.

    WHY chronological and NOT random split
    ---------------------------------------
    Solar and meteorological data exhibits strong temporal autocorrelation:
    weather patterns, seasonal cycles, and even multi-year climate trends mean
    that observations close in time are statistically dependent.

    A *random* split scatters future timestamps into the training set and past
    timestamps into the test set. The model then "sees" future irradiance
    conditions during training, artificially inflating validation scores.
    This is called **temporal data leakage** — the model learns patterns it
    could not possibly know at inference time, making benchmarks unreliable
    and production performance worse than reported.

    A *chronological* split keeps the most recent `test_years` years entirely
    out of training, faithfully simulating the real-world scenario where the
    model must forecast conditions it has never seen before.

    Parameters
    ----------
    df : pd.DataFrame
        Feature dataset with a DatetimeTZDtype index, produced by
        build_feature_dataset().
    test_years : int
        Number of most-recent years reserved for the test set (default: 2).

    Returns
    -------
    X_train, X_test : pd.DataFrame
        Feature matrices.
    y_train, y_test : pd.Series
        Target vectors (shortwave_radiation).
    """
    cutoff = df.index.max() - pd.DateOffset(years=test_years)

    train_mask = df.index <= cutoff
    test_mask = df.index > cutoff

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    X_train, y_train = X.loc[train_mask], y.loc[train_mask]
    X_test, y_test = X.loc[test_mask], y.loc[test_mask]

    logger.info(
        "Chronological split — cutoff: %s | "
        "train: %d rows (%s -> %s) | test: %d rows (%s -> %s)",
        cutoff.date(),
        len(X_train), X_train.index.min().date(), X_train.index.max().date(),
        len(X_test), X_test.index.min().date(), X_test.index.max().date(),
    )
    return X_train, X_test, y_train, y_test


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting feature engineering pipeline ...")

    feature_df = build_feature_dataset()

    print("\n--- Feature DataFrame Shape ---")
    print(feature_df.shape)

    print("\n--- Columns ---")
    print(feature_df.columns.tolist())

    print("\n--- Sample Rows ---")
    print(feature_df.head())

    print("\n--- Train / Test Split (test_years=2) ---")
    X_train, X_test, y_train, y_test = chronological_train_test_split(feature_df)
    print(f"  X_train : {X_train.shape}  ({X_train.index.min().date()} -> {X_train.index.max().date()})")
    print(f"  X_test  : {X_test.shape}  ({X_test.index.min().date()} -> {X_test.index.max().date()})")
    print(f"  y_train : {y_train.shape}")
    print(f"  y_test  : {y_test.shape}")
