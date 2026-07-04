# Member 4 — Deployment Handoff (Member 3 deliverables)

This document summarizes what Member 3 built and what DevOps needs to deploy it.
Member 3 does **not** provide Docker/AWS configs — that is Member 4's responsibility.

## What Member 3 delivered

| Component | Location | Port |
|---|---|---|
| FastAPI backend | `backend/` | **8000** |
| Next.js dashboard | `dashboard/` | **8501** |
| MySQL database | `solar_panel_automation` | **3306** |

## Backend — run locally

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
copy .env.example .env   # set DB credentials
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Production-style run:

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

## Frontend — run locally

```powershell
cd dashboard
npm install
copy .env.example .env.local
npm run dev
```

Production build:

```powershell
npm run build
npm start
```

Set `NEXT_PUBLIC_API_URL` to the public backend URL before building for production.

## Required environment variables

### Backend (`backend/.env`)

| Variable | Example | Notes |
|---|---|---|
| `DB_HOST` | `127.0.0.1` or RDS endpoint | MySQL host |
| `DB_PORT` | `3306` | MySQL port |
| `DB_NAME` | `solar_panel_automation` | Existing database |
| `DB_USER` | `your_user` | MySQL user |
| `DB_PASSWORD` | `***` | Use secrets manager in prod |
| `CORS_ORIGINS` | `https://your-dashboard-url.com` | Must match frontend URL |

### Frontend (`dashboard/.env.local` or build-time env)

| Variable | Example |
|---|---|
| `NEXT_PUBLIC_API_URL` | `https://your-api-url.com` |

## Health checks (for load balancers)

| Endpoint | Purpose | Success |
|---|---|---|
| `GET /health` | Liveness | 200 |
| `GET /health/ready` | Readiness (DB connected) | 200 with `"database": "connected"` |

## API documentation

- Swagger UI: `http://localhost:8000/docs`
- All 9 tables have full CRUD at `/api/*`

## Database

- **Name:** `solar_panel_automation`
- **Tables:** `weather_data`, `solar_panel`, `solar_predictions`, `energy_consumption`, `battery`, `battery_status`, `telemetry`, `alerts`, `system_logs`
- SQLAlchemy models: `backend/app/models/entities.py`
- Schema is **not modified** by the backend — tables must already exist

## CORS

Backend allows origins listed in `CORS_ORIGINS`. For production, set this to the exact dashboard URL before deployment.

## What Member 4 still needs to do

- Containerize backend and frontend (Docker)
- Provision AWS RDS MySQL or connect to existing DB
- Set up ECS/EC2/ALB or equivalent
- Configure secrets for `DB_PASSWORD`
- Set production `CORS_ORIGINS` and `NEXT_PUBLIC_API_URL`
- Wire CI/CD (Jenkins or GitHub Actions)

## Quick verification before deploy

```powershell
# 1. Backend health
curl http://localhost:8000/health/ready

# 2. Sample API
curl http://localhost:8000/api/panels

# 3. Frontend
# Open http://localhost:8501
```
