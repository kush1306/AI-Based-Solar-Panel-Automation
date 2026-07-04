# 🌞 AI-Based Solar Panel Automation System
## Week 2 | Member 2 — Demand Forecasting + Battery Optimization + FastAPI

[![CI](https://github.com/YOUR_USERNAME/solar-ai-system/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/solar-ai-system/actions)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)

---

## 📌 Task (Week 2, Member 2)
> Build baseline demand-forecasting model; formulate battery optimization logic.

---

## 🏠 System Assumptions (Delhi Household)

| Parameter | Value |
|-----------|-------|
| Location | Delhi, India (28.6°N, 77.2°E) |
| Solar | 3 kWp rooftop |
| Battery | 5 kWh Li-Ion (Luminous/Exide) |
| Grid tariff | ₹5/kWh (off-peak) · ₹10/kWh (5–11 PM peak) |
| Net metering | ₹3/kWh export |
| Annual savings | ~₹18,000–22,000 |

---

## 📂 Project Structure

```
solar-ai-member2-week2/
├── src/
│   ├── data_loader.py          ← Weather loader (OpenMeteo API / GitHub / local)
│   ├── demand_forecaster.py    ← ML demand forecasting (RF, XGBoost, etc.)
│   ├── battery_optimizer.py    ← Rule-based + LP battery optimizer
│   └── api.py                  ← FastAPI application (10 endpoints)
├── data/
│   └── delhi_openmeteo_hourly.csv   ← Real OpenMeteo data (auto-downloaded)
├── tests/
│   └── test_api.py             ← FastAPI + unit tests
├── scripts/
│   └── download_data.py        ← Manual data download script
├── models/                     ← Saved .pkl model files
├── start_api.py                ← One-click API launcher
└── requirements.txt
```

---

## ⚡ Quick Start

```bash
# 1. Clone & install
git clone https://github.com/YOUR_USERNAME/solar-ai-system.git
cd solar-ai-system
pip install -r requirements.txt

# 2. Start the API (auto-downloads Delhi weather data on first run)
python start_api.py

# 3. Open docs in browser
#    http://localhost:8000/docs
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Health check |
| `GET`  | `/health` | Model status + metrics |
| `GET`  | `/data/status` | Dataset info (rows, date range, source) |
| `POST` | `/data/reload?force_download=true` | Re-fetch from OpenMeteo API |
| `POST` | `/train` | Train/re-train forecasting model |
| `GET`  | `/forecast/next?hours=24` | Forecast next N hours |
| `POST` | `/forecast/predict` | Predict for custom weather inputs |
| `POST` | `/optimize/day` | Battery dispatch for a specific date |
| `GET`  | `/optimize/annual` | Full-year cost summary + monthly breakdown |
| `GET`  | `/summary` | Dashboard summary (model + economics) |

### Example: Forecast next 24 hours
```bash
curl http://localhost:8000/forecast/next?hours=24
```

### Example: Battery optimization for a specific day
```bash
curl -X POST http://localhost:8000/optimize/day \
  -H "Content-Type: application/json" \
  -d '{"date":"2024-06-15","optimizer":"lp","initial_soc":0.5}'
```

### Example: Custom demand prediction
```bash
curl -X POST http://localhost:8000/forecast/predict \
  -H "Content-Type: application/json" \
  -d '{
    "hours": [
      {"time":"2024-06-15T14:00:00","temperature_2m":40.0,
       "relative_humidity_2m":45.0,"shortwave_radiation":800.0,
       "wind_speed_10m":3.0,"precipitation":0.0}
    ]
  }'
```

---

## 🌦️ Weather Data (Delhi OpenMeteo)

Data is loaded in priority order:
1. **GitHub raw URL** — `data/delhi_openmeteo_hourly.csv` in repo
2. **Local file** — `data/delhi_openmeteo_hourly.csv`
3. **OpenMeteo API** — auto-downloaded on startup (2023–2024)
4. **Synthetic** — IMD statistical fallback (last resort only)

To force a fresh download:
```bash
curl -X POST "http://localhost:8000/data/reload?force_download=true"
# OR
python scripts/download_data.py
```

**Loading from GitHub in notebooks:**
```python
import pandas as pd
url = "https://raw.githubusercontent.com/YOUR_USERNAME/solar-ai-system/main/data/delhi_openmeteo_hourly.csv"
df = pd.read_csv(url)
```

---

## 🤖 ML Models

| Model | Notes |
|-------|-------|
| Naive Persistence | Baseline |
| Linear / Ridge Regression | Scaled, fast |
| **Random Forest** | Default — best accuracy/speed tradeoff |
| Gradient Boosting | sklearn GBM |
| XGBoost | Often best accuracy |

**35 features:** Cyclical time encoding · Delhi weather · 1h–7day lag features · Rolling statistics

---

## 🔋 Battery Optimizer Strategies

- **Rule-based** (`optimizer: "rule"`) — Real-time greedy, works without forecasts
- **LP Day-ahead** (`optimizer: "lp"`) — scipy HiGHS LP, optimal given perfect foresight

---

## 🧪 Tests

```bash
pytest tests/ -v
```

---

## 📤 GitHub Upload

```bash
git clone https://github.com/YOUR_USERNAME/solar-ai-system.git
cd solar-ai-system
# copy project files here
git add .
git commit -m "Week 2 Member 2: Demand forecasting + battery optimizer + FastAPI"
git push origin main
```
