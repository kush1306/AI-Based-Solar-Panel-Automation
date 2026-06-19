"""
config.py — Central configuration for the solar-position-api project.

All tunable constants live here so they can be updated in a single place
without hunting through the codebase.
"""

# ---------------------------------------------------------------------------
# Geographic location: New Delhi, India
# ---------------------------------------------------------------------------
LATITUDE: float = 28.6139   # degrees North
LONGITUDE: float = 77.2090  # degrees East
TIMEZONE: str = "Asia/Kolkata"

# ---------------------------------------------------------------------------
# Solar panel physical parameters
# Adjust these constants to match the panels being modelled.
# ---------------------------------------------------------------------------
PANEL_AREA_M2: float = 1.6   # m² — typical residential panel (~60-cell, 300 W); adjustable
PANEL_EFFICIENCY: float = 0.20  # 20% — standard monocrystalline efficiency; adjustable

# ---------------------------------------------------------------------------
# Open-Meteo API
# ---------------------------------------------------------------------------
OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_TIMEOUT_SECONDS: int = 5  # seconds before the HTTP request is aborted

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
MODEL_DIR: str = "src/model"  # directory where trained model artefacts are saved
DATA_DIR: str = "data"
RAW_CSV: str = f"{DATA_DIR}/delhi_openmeteo_hourly.csv"
CLEANED_CSV: str = f"{DATA_DIR}/delhi_cleaned.csv"
