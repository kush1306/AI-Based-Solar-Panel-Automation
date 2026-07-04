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
