# AI-Based Solar Panel Automation

## Project Overview

AI-powered system for solar panel monitoring, optimization, and energy forecasting.

## Team Members

- Member 1 – Solar AI
- Member 2 – Energy AI
- Member 3 – Full Stack (backend, frontend, database)
- Member 4 – DevOps & Integration
- Member 5 – Data Engineer

## Project Structure

```
├── backend/          # FastAPI REST API + MySQL (Member 3)
├── dashboard/        # Next.js 15 dashboard UI (Member 3)
├── models/           # AI/ML model services (Member 1 & 2)
├── docker/           # Docker Compose (Member 4 — DevOps)
└── run-local.ps1     # Run backend + frontend together locally
```

---

## Member 3 — Backend, Frontend & Database

### Database

- **Name:** `solar_panel_automation`
- **Tables:** weather_data, solar_panel, solar_predictions, energy_consumption, battery, battery_status, telemetry, alerts, system_logs
- Models: `backend/app/models/entities.py`

### Run everything locally (one command)

```powershell
.\run-local.ps1
```

Or run separately:

| Service | Command | URL |
|---|---|---|
| Backend | `cd backend && uvicorn app.main:app --reload --port 8000` | http://localhost:8000/docs |
| Frontend | `cd dashboard && npm run dev` | http://localhost:8501 |
| MySQL | Must be running locally | port 3306 |

Copy env files first:
- `backend/.env.example` → `backend/.env`
- `dashboard/.env.example` → `dashboard/.env.local`

### Deployment handoff → Member 4

Member 3 does **not** handle Docker/AWS. See **`backend/HANDOFF.md`** for ports, env vars, health checks, and build commands DevOps needs.

---

## Dashboard — Smart Solar Optimization System

The dashboard UI is built with Next.js. Pages currently use mock data; API routes are ready at `dashboard/src/lib/api-config.ts` for wiring to the backend.

### Tech Stack

- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui
- Framer Motion
- Recharts
- Lucide Icons

### Pages

| Route | Description |
|---|---|
| `/` | Main dashboard — KPIs, Solar Factory, energy flow, AI widgets |
| `/solar-analytics` | Generation, irradiance, and performance analytics |
| `/ai-predictions` | Solar orientation and consumption forecast AI |
| `/battery` | Battery SOC, health, charge/discharge history |
| `/energy-flow` | Animated system energy map |
| `/weather` | Weather intelligence and AQI for Delhi |
| `/devices` | Device monitoring table |
| `/reports` | Demo reports with export buttons (UI only) |
| `/settings` | App settings stored in localStorage |

### Local Development

```bash
cd dashboard
npm install
npm run dev
```

Open [http://localhost:8501](http://localhost:8501)

### Production Build

```bash
cd dashboard
npm run build
npm start
```

## Solar Position AI Model (Member 1)

Merged from `member1-solar-ai` into `models/solar-position-api/`.

### What it does

- **FastAPI** inference service on port **8001**
- **pvlib** sun-position calculations for Delhi
- **XGBoost / LightGBM** irradiance prediction
- Live weather from **Open-Meteo** (with fallback)
- Endpoints: `GET /health`, `GET /predict`, `GET /docs`

### Folder structure

```
models/solar-position-api/
├── app/           # FastAPI routes (main.py, energy.py, weather_client.py)
├── src/           # Training pipeline (train.py, features.py, config.py)
├── data/          # Delhi weather CSV datasets
├── tests/         # API tests
├── Dockerfile     # Container build + train + serve
└── run-local.ps1  # Windows local setup script
```

### Run locally (Windows)

```powershell
cd models/solar-position-api
.\run-local.ps1
```

First run trains the model (~5–15 min), then starts the API:

- Health: http://localhost:8001/health
- Predict: http://localhost:8001/predict
- Swagger: http://localhost:8001/docs

### Manual setup

```powershell
cd models/solar-position-api
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
python -m src.train
uvicorn app.main:app --reload --port 8001
```

### Dashboard integration (future)

The dashboard currently uses mock data. To wire live AI predictions:

1. Start the model API on port 8001
2. Call `http://localhost:8001/predict` from dashboard pages
3. Map response fields: `optimal_tilt_deg`, `estimated_energy_output_watts`, `predicted_shortwave_radiation_wm2`

## Docker & Deployment (Member 4 — DevOps)

Docker, AWS, Jenkins, and production deployment are **Member 4's responsibility**.

See `backend/HANDOFF.md` for what Member 3 delivers and what DevOps needs to configure.

## Future Enhancements

- Wire dashboard pages to backend APIs via `api-config.ts`
- Integrate real-time MQTT data from ESP32 sensors
- Deploy solar orientation and consumption AI models
- Add user authentication and role-based access
- Enable live weather and AQI API feeds
