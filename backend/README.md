# Solar Intelligence Platform — Backend API

Production-ready FastAPI REST backend with MySQL connectivity for the solar monitoring platform.

## Stack

- FastAPI + Uvicorn
- SQLAlchemy ORM
- Pydantic v2
- PyMySQL
- python-dotenv

## Project Structure

```
backend/
├── app/
│   ├── api/              # Route handlers (one module per resource)
│   ├── crud/             # Reusable CRUD operations per table
│   ├── dependencies/       # FastAPI dependencies (DB session, router factory)
│   ├── models/             # SQLAlchemy models (maps to existing MySQL tables)
│   ├── schemas/            # Pydantic request/response schemas
│   ├── services/           # Business logic (dashboard aggregation, AI stub)
│   ├── utils/              # Shared helpers (pagination)
│   ├── core/               # Config, database, logging, exceptions
│   └── main.py             # Application entry point
├── requirements.txt
├── .env.example
└── README.md
```

## Quick Start

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
copy .env.example .env   # set your MySQL credentials
uvicorn app.main:app --reload --port 8000
```

- **Swagger UI:** http://localhost:8000/docs
- **Health:** http://localhost:8000/health (includes database status)
- **Readiness:** http://localhost:8000/health/ready

## Environment Variables

| Variable | Description |
|---|---|
| `DB_HOST` | MySQL host |
| `DB_PORT` | MySQL port (default 3306) |
| `DB_NAME` | Database name (`solar_panel_automation`) |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |
| `DATABASE_URL` | Optional full SQLAlchemy URL override |
| `CORS_ORIGINS` | Comma-separated frontend origins |

Credentials are read from `backend/.env` — never hardcoded.

## Database

Connects to the **existing** MySQL database `solar_panel_automation`. The backend does **not** create or modify tables.

| Table | Model | API prefix |
|---|---|---|
| `weather_data` | `WeatherData` | `/api/weather` |
| `solar_panel` | `SolarPanel` | `/api/panels` |
| `solar_predictions` | `SolarPrediction` | `/api/predictions` |
| `energy_consumption` | `EnergyConsumption` | `/api/energy` |
| `battery` | `Battery` | `/api/battery` |
| `battery_status` | `BatteryStatus` | `/api/battery-status` |
| `telemetry` | `Telemetry` | `/api/telemetry` |
| `alerts` | `Alert` | `/api/alerts` |
| `system_logs` | `SystemLog` | `/api/logs` |

## CRUD Endpoints (every table)

Each resource supports:

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/{resource}` | List all (paginated) |
| `GET` | `/api/{resource}/{id}` | Get by ID |
| `POST` | `/api/{resource}` | Create |
| `PUT` | `/api/{resource}/{id}` | Update |
| `DELETE` | `/api/{resource}/{id}` | Delete |

List endpoints support `page`, `page_size`, `search`, `sort_by`, and `sort_order` query parameters.

## HTTP Status Codes

| Code | When |
|---|---|
| 200 | Successful read/update/delete |
| 201 | Successful create |
| 400 | Application validation errors |
| 404 | Record not found |
| 422 | Request validation failed |
| 500 | Database or internal errors |

## CORS

CORS is enabled for the Next.js frontend. Default allowed origins:

- `http://localhost:8501`
- `http://127.0.0.1:8501`

Set `CORS_ORIGINS` in `.env` for additional origins.

## Logging & Error Handling

- Request/response logging via middleware
- Validation errors logged and returned as JSON
- Database errors caught centrally and returned as clean JSON responses

## AI Integration

Real AI inference is **not implemented**. Placeholder stubs in `app/services/ai_service.py` raise `NotImplementedError`.

For frontend development, use the **mock endpoints** (realistic dummy data):

| Endpoint | Description |
|---|---|
| `GET /api/mock/solar-prediction` | Mock tilt, power, irradiance prediction |
| `GET /api/mock/energy` | Mock hourly energy load forecast (`horizon_hours=1-48`) |

Both responses include `"source": "mock"`. Replace with real model calls when the AI team integrates.

## Frontend Integration

From the Next.js dashboard, call the API at:

```
http://localhost:8000/api/{resource}
```

Example:

```
GET http://localhost:8000/api/panels
GET http://localhost:8000/api/dashboard
```

Ensure the frontend origin is listed in `CORS_ORIGINS`.

## Deployment handoff (Member 4)

Member 3 scope: backend, frontend, database connectivity only.
See **[HANDOFF.md](HANDOFF.md)** for ports, env vars, health checks, and what DevOps needs to deploy.
