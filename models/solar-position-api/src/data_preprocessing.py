"""
data_preprocessing.py — Load, validate, clean, and export the raw Open-Meteo
hourly CSV for Delhi.

Run standalone:
    python -m src.data_preprocessing

Steps performed
---------------
1. Load the raw CSV and parse timestamps.
2. Report basic statistics (shape, date range, dtypes).
3. Check for and report duplicate timestamps → deduplicate.
4. Check for and report missing values.
   - Short gaps (≤ 3 consecutive NaNs): interpolated linearly.
     Rationale: hourly solar / weather data rarely has long outages; linear
     interpolation is physically reasonable for short gaps and avoids the bias
     introduced by forward-fill or zero-fill.
   - Remaining NaN rows (long gaps): dropped entirely.
5. Validate expected data ranges; log any out-of-range anomalies (rows are
   kept by default — flagging is informational unless you choose to drop them).
6. Save the cleaned dataframe to data/delhi_cleaned.csv.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Allow running as `python -m src.data_preprocessing` from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import CLEANED_CSV, RAW_CSV, TIMEZONE  # noqa: E402

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Expected valid data ranges for sanity checks
# Keys must match column names exactly (case-sensitive).
# ---------------------------------------------------------------------------
VALID_RANGES: dict[str, tuple[float, float]] = {
    "cloud_cover": (0.0, 100.0),        # percentage
    "shortwave_radiation": (0.0, 1500.0),  # W/m² — upper bound > theoretical max as safety
    "direct_radiation": (0.0, 1500.0),
    "diffuse_radiation": (0.0, 1500.0),
    "temperature_2m": (-20.0, 55.0),    # °C — Delhi historical extremes with margin
    "relative_humidity_2m": (0.0, 100.0),
    "wind_speed_10m": (0.0, 100.0),     # m/s
    "precipitation": (0.0, 500.0),      # mm
}

# Maximum number of consecutive NaNs to interpolate (anything longer is dropped)
MAX_INTERP_GAP: int = 3


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def load_raw(path: str | Path) -> pd.DataFrame:
    """
    Load the raw Open-Meteo CSV, parse the 'time' column as UTC-aware
    datetime, convert to the project timezone, and set it as the index.

    Parameters
    ----------
    path : str | Path
        Filesystem path to the raw CSV file.

    Returns
    -------
    pd.DataFrame
        DataFrame with a DatetimeTZDtype index (Asia/Kolkata).

    Raises
    ------
    FileNotFoundError
        If the CSV does not exist at the given path.
    KeyError
        If the required 'time' column is absent.
    """
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Raw CSV not found at '{csv_path}'. "
            "Place 'delhi_openmeteo_hourly.csv' inside the data/ directory."
        )

    logger.info("Loading raw CSV: %s", csv_path.resolve())
    df = pd.read_csv(csv_path)

    if "time" not in df.columns:
        raise KeyError(
            "Expected a column named 'time' in the CSV. "
            f"Found columns: {list(df.columns)}"
        )

    # Open-Meteo timestamps are UTC; convert to local timezone for easier interpretation.
    df["time"] = pd.to_datetime(df["time"], utc=True).dt.tz_convert(TIMEZONE)
    df = df.set_index("time")
    df.index.name = "time"

    logger.info(
        "Raw data loaded — shape: %s | date range: %s → %s",
        df.shape,
        df.index.min(),
        df.index.max(),
    )
    return df


def report_missing(df: pd.DataFrame) -> None:
    """Log a per-column missing-value report."""
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if missing.empty:
        logger.info("No missing values detected.")
    else:
        logger.warning("Missing values detected:\n%s", missing.to_string())


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate timestamps, keeping the first occurrence.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        DataFrame with unique timestamps.
    """
    n_dupes = df.index.duplicated().sum()
    if n_dupes > 0:
        logger.warning("Found %d duplicate timestamp(s) — keeping first occurrence.", n_dupes)
        df = df[~df.index.duplicated(keep="first")]
    else:
        logger.info("No duplicate timestamps found.")
    return df


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values with a two-stage strategy:

    1. Interpolate short gaps (≤ MAX_INTERP_GAP consecutive NaNs) linearly.
       This is appropriate for hourly meteorological series where a brief
       sensor outage can be plausibly filled by the surrounding observations.
    2. Drop any rows that still contain NaNs after interpolation (long gaps
       where interpolation would be unreliable).

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame.
    """
    n_before = len(df)
    total_missing_before = df.isnull().sum().sum()

    if total_missing_before > 0:
        # Stage 1: linear interpolation for short gaps
        df = df.interpolate(method="linear", limit=MAX_INTERP_GAP, limit_direction="forward")
        interpolated = total_missing_before - df.isnull().sum().sum()
        logger.info(
            "Interpolated %d NaN cell(s) (max consecutive gap: %d).",
            interpolated,
            MAX_INTERP_GAP,
        )

        # Stage 2: drop remaining rows with any NaN (long gaps)
        remaining_missing = df.isnull().sum().sum()
        if remaining_missing > 0:
            df = df.dropna()
            n_dropped = n_before - len(df)
            logger.warning(
                "Dropped %d row(s) with unfillable NaN values (long gaps).",
                n_dropped,
            )
    else:
        logger.info("No missing values to handle.")

    return df


def validate_ranges(df: pd.DataFrame) -> None:
    """
    Check each known column against its expected physical range.
    Anomalies are logged as warnings; no rows are removed — the caller
    can choose to filter based on this information if required.

    Parameters
    ----------
    df : pd.DataFrame
    """
    any_anomaly = False
    for col, (low, high) in VALID_RANGES.items():
        if col not in df.columns:
            continue
        mask = (df[col] < low) | (df[col] > high)
        n_anomalies = mask.sum()
        if n_anomalies > 0:
            any_anomaly = True
            logger.warning(
                "Column '%s': %d row(s) outside valid range [%.1f, %.1f]. "
                "Example timestamps: %s",
                col,
                n_anomalies,
                low,
                high,
                df.index[mask][:5].tolist(),
            )
    if not any_anomaly:
        logger.info("All columns passed range validation.")


def save_cleaned(df: pd.DataFrame, path: str | Path) -> None:
    """
    Persist the cleaned DataFrame as a CSV.

    Parameters
    ----------
    df : pd.DataFrame
    path : str | Path
    """
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path)
    logger.info("Cleaned data saved to '%s'.", out_path.resolve())


def preprocess(raw_path: str | Path = RAW_CSV, cleaned_path: str | Path = CLEANED_CSV) -> pd.DataFrame:
    """
    Full preprocessing pipeline.

    Parameters
    ----------
    raw_path : str | Path
        Path to the input raw CSV.
    cleaned_path : str | Path
        Destination path for the cleaned CSV.

    Returns
    -------
    pd.DataFrame
        The cleaned, validated DataFrame.
    """
    df = load_raw(raw_path)
    report_missing(df)
    df = deduplicate(df)
    df = handle_missing(df)
    validate_ranges(df)
    save_cleaned(df, cleaned_path)

    # ---- Final summary ----
    logger.info(
        "\n"
        "========== Preprocessing Summary ==========\n"
        "  Cleaned shape   : %s\n"
        "  Date range      : %s  →  %s\n"
        "  Columns         : %s\n"
        "===========================================",
        df.shape,
        df.index.min(),
        df.index.max(),
        list(df.columns),
    )
    return df


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting data preprocessing pipeline …")
    cleaned_df = preprocess()
    print("\n--- Cleaned DataFrame Head ---")
    print(cleaned_df.head())
    print("\n--- Descriptive Statistics ---")
    print(cleaned_df.describe())
