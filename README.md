# AI-Based Solar Panel Automation

## Project Overview

AI-powered system for solar panel monitoring, optimization, and energy forecasting. This repository contains the full-stack project scaffold with a **frontend-only demo dashboard** for the Smart Solar Optimization System.

## Team Members

- Member 1 – Solar AI
- Member 2 – Energy AI
- Member 3 – Full Stack
- Member 4 – DevOps & Integration
- Member 5 – Data Engineer

## Branch Strategy

- `main`
- `develop`
- `member1-solar-ai`
- `member2-energy-ai`
- `member3-fullstack`
- `member4-devops`
- `member5-data`

## Project Structure

```
├── backend/          # FastAPI backend (placeholder)
├── dashboard/        # Next.js 15 frontend demo (mock data only)
├── models/           # AI/ML model service (placeholder)
├── docker/           # Docker Compose orchestration
├── data/             # Shared data directory
└── .env.example      # Environment variable template
```

## Dashboard — Smart Solar Optimization System

The dashboard is a **frontend-only demo** built with mock data. No backend, authentication, or API integration is required to run it.

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

## Docker Setup

From the `docker/` directory:

```bash
docker-compose up
```

Services:

| Service | Port | Description |
|---|---|---|
| dashboard | 8501 | Next.js frontend |
| backend | 8000 | API server |
| models | 8001 | ML model service |
| db | 3306 | MySQL database |

## Jenkins Pipeline

CI/CD pipeline configuration (skeleton) — see project docs for pipeline stages.

## Deployment Plan

1. Build and push Docker images for each service
2. Deploy via Docker Compose or Kubernetes
3. Connect dashboard to backend APIs (future integration)
4. Wire AI model service for live predictions

## Future Enhancements

- Connect dashboard to FastAPI backend
- Integrate real-time MQTT data from ESP32 sensors
- Deploy solar orientation and consumption AI models
- Add user authentication and role-based access
- Enable live weather and AQI API feeds
