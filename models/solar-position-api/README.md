# Solar Position API

A **production-ready backend service** for real-time solar panel angle optimisation
in New Delhi, India. The system combines **deterministic sun-position calculations**
(via `pvlib`) with **ML-based irradiance prediction** (XGBoost / LightGBM) to
recommend the optimal tilt and azimuth angles for a rooftop solar panel at any
given moment, maximising energy yield throughout the day and across seasons.

---

## Architecture Overview

```
Open-Meteo API  ──►  Feature Engineering  ──►  ML Model (irradiance forecast)
pvlib (ephem)   ──►  Sun Position          ──►  Angle Optimiser  ──►  FastAPI
```

- **`src/config.py`** — all project constants (location, panel specs, API URLs).
- **`src/data_preprocessing.py`** — cleans historical Open-Meteo CSV data.
- **`app/`** — FastAPI application (routes, schemas, dependencies).
- **`src/model/`** — serialised trained model artefacts (not tracked in git).
- **`data/`** — raw and cleaned datasets (cleaned CSV not tracked in git).

---

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd solar-position-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add raw data

Place `delhi_openmeteo_hourly.csv` inside the `data/` directory.

### 5. Run data preprocessing

```bash
python -m src.data_preprocessing
```

This generates `data/delhi_cleaned.csv` which is used for model training.

### 6. Start the API server (development)

```bash
uvicorn app.main:app --reload
```

---

## API Usage

### Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Liveness check — returns model name and available features |
| `GET` | `/predict` | Solar prediction for current or specified datetime |

### `/predict` examples

```bash
# Current time (default) — uses live Open-Meteo weather
curl http://localhost:8000/predict

# Specific future datetime — uses historical average weather, no live API call
curl "http://localhost:8000/predict?datetime_str=2026-12-21T12:00"

# Specific past datetime — same historical weather path
curl "http://localhost:8000/predict?datetime_str=2024-06-01T09:00"

# Invalid format — returns HTTP 422 with clear error message
curl "http://localhost:8000/predict?datetime_str=bad-format"
```

The `datetime_str` parameter uses `YYYY-MM-DDTHH:MM` format (24-hour clock, local
`Asia/Kolkata` time). When omitted the server uses its current wall-clock time.

---

## Configuration

Edit **`src/config.py`** to change:

| Constant | Default | Description |
|---|---|---|
| `LATITUDE` | `28.6139` | Site latitude |
| `LONGITUDE` | `77.2090` | Site longitude |
| `TIMEZONE` | `Asia/Kolkata` | Local timezone |
| `PANEL_AREA_M2` | `1.6` | Panel surface area (m²) |
| `PANEL_EFFICIENCY` | `0.20` | Panel efficiency (0-1) |

---

## License

MIT
