# Solar Intelligence Platform — Backend API

FastAPI REST backend with MySQL connectivity for the solar monitoring platform.

## Stack

- FastAPI + Uvicorn
- SQLAlchemy ORM
- Pydantic v2
- MySQL (PyMySQL)

## Quick Start (Local)

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
pip install -e .
copy .env.example .env   # or edit backend/.env
uvicorn app.main:app --reload --port 8000
```

- **Swagger UI:** http://localhost:8000/docs
- **Health:** http://localhost:8000/health

## Environment Variables

| Variable | Description |
|---|---|
| `DB_HOST` | MySQL host |
| `DB_PORT` | MySQL port (default 3306) |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
| `DATABASE_URL` | Optional full SQLAlchemy URL override |
| `CORS_ORIGINS` | Comma-separated frontend origins |

## API Overview

| Resource | Base Path |
|---|---|
| Weather | `/api/weather` |
| Solar Panels | `/api/panels` |
| Predictions | `/api/predictions` |
| Energy | `/api/energy` |
| Battery | `/api/battery` |
| Battery Status | `/api/battery-status` |
| Telemetry | `/api/telemetry` |
| Alerts | `/api/alerts` (+ `/active`, `/history`) |
| System Logs | `/api/logs` |
| Dashboard | `/api/dashboard`, `/api/dashboard/charts` |

All list endpoints support pagination (`page`, `page_size`), search, and sorting parameters where applicable.

## AI Integration (Future)

AI inference is **not implemented**. Placeholder functions live in `app/services/ai_service.py` and raise `NotImplementedError`. The AI team can integrate models there without changing API routes.

## Schema Reference

SQLAlchemy models map to existing MySQL tables. See `database/schema_reference.sql` for expected column layout. **Do not run this file if your database already exists** — it is documentation only.

## Docker

From `docker/` directory:

```bash
docker-compose up backend db
```

Backend runs on port **8000**.
