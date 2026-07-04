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

## Configuration

Edit **`src/config.py`** to change:

| Constant | Default | Description |
|---|---|---|
| `LATITUDE` | `28.6139` | Site latitude |
| `LONGITUDE` | `77.2090` | Site longitude |
| `TIMEZONE` | `Asia/Kolkata` | Local timezone |
| `PANEL_AREA_M2` | `1.2` | Panel surface area (m²) |
| `PANEL_EFFICIENCY` | `0.20` | Panel efficiency (0–1) |

---

## License

MIT
