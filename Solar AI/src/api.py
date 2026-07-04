# -*- coding: utf-8 -*-
"""
api.py — FastAPI application
Week 2, Member 2 | AI Solar Panel Automation System

Endpoints
─────────
GET  /                    Health check
GET  /health              Detailed health + model status
GET  /data/status         Weather dataset info (source, rows, date range)
POST /data/reload         Re-fetch/download weather data from OpenMeteo
POST /train               Train (or re-train) the demand forecasting model
GET  /forecast/next       Forecast demand for the next N hours
POST /forecast/predict    Predict demand for arbitrary input rows
POST /optimize/day        Run LP day-ahead battery optimizer for 24 hours
GET  /optimize/annual     Run rule-based optimizer over full dataset → annual report
GET  /summary             Annual energy & cost summary in INR

Run locally:
    uvicorn src.api:app --reload --port 8000
"""

from __future__ import annotations

import os
import sys
import logging
from datetime import datetime, timedelta
from typing import List, Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ── path fix so imports work from project root ────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

from data_loader import load_full_dataset, load_weather, generate_demand, download_from_openmeteo
from demand_forecaster import DemandForecaster
from battery_optimizer import RuleBasedOptimizer, LPDayAheadOptimizer, annual_report, BatteryConfig, SolarConfig, TariffConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("solar-api")

# ── App setup ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Solar AI — Demand Forecast & Battery Optimizer API",
    description=(
        "Week 2 | Member 2\n\n"
        "Provides demand forecasting and battery optimization for a Delhi rooftop solar household.\n\n"
        "**System specs:** 3 kWp solar · 5 kWh battery · Delhi BSES tariff (INR)\n\n"
        "**Data source:** Delhi OpenMeteo hourly weather data"
    ),
    version="1.0.0",
    contact={"name": "Solar AI Team", "url": "https://github.com/YOUR_USERNAME/solar-ai-system"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── App state (in-memory, single-process) ─────────────────────────────────────

STATE = {
    "full_df":      None,   # pd.DataFrame: weather + demand
    "forecaster":   None,   # DemandForecaster (trained)
    "optimizer":    RuleBasedOptimizer(),
    "lp_optimizer": LPDayAheadOptimizer(),
    "data_source":  "not loaded",
    "loaded_at":    None,
    "train_metrics":{},
}

LOCAL_CSV = "data/delhi_openmeteo_hourly.csv"
MODEL_PATH = "models/demand_random_forest.pkl"


def _load_and_train(force_download=False):
    """Load Delhi data + train model. Called at startup and /data/reload."""
    global STATE

    if force_download:
        logger.info("Force-downloading Delhi weather from OpenMeteo API...")
        df = download_from_openmeteo(save_path=LOCAL_CSV)
        source = "openmeteo_api_download"
        if df is None:
            logger.warning("OpenMeteo download failed, using fallback loader.")
            df = None
    else:
        df = None

    if df is None:
        df = load_full_dataset(
            local_path=LOCAL_CSV,
            save_downloaded_to=LOCAL_CSV,
        )
        source = _infer_source()

    STATE["full_df"]    = df
    STATE["data_source"]= source
    STATE["loaded_at"]  = datetime.utcnow().isoformat()
    logger.info(f"Dataset loaded: {len(df):,} rows from {source}")

    # Train model
    split = int(len(df) * 0.80)
    fc = DemandForecaster("Random Forest")
    fc.fit(df.iloc[:split], verbose=True)
    m  = fc.evaluate(df.iloc[split:])
    fc.save("models")
    STATE["forecaster"]    = fc
    STATE["train_metrics"] = m
    logger.info(f"Model trained | MAE={m['mae']:.4f} kW | R²={m['r2']:.4f}")


def _infer_source():
    if os.path.exists(LOCAL_CSV):
        return "local_file"
    return "synthetic_fallback"


@app.on_event("startup")
async def startup():
    logger.info("Starting Solar AI API — loading data & training model...")
    try:
        _load_and_train(force_download=False)
    except Exception as e:
        logger.error(f"Startup load failed: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# Pydantic Schemas
# ═══════════════════════════════════════════════════════════════════════════════

class WeatherHour(BaseModel):
    """Input weather + time for a single hour."""
    time: str                            = Field(..., example="2024-06-15T14:00:00")
    temperature_2m: float                = Field(32.0, ge=-10, le=55, description="°C")
    relative_humidity_2m: float          = Field(60.0, ge=0, le=100, description="%")
    shortwave_radiation: float           = Field(600.0, ge=0, le=1400, description="W/m²")
    wind_speed_10m: float                = Field(3.0, ge=0, le=30, description="m/s")
    precipitation: float                 = Field(0.0, ge=0, description="mm")
    demand_kw: Optional[float]           = Field(None, description="Known demand (optional)")

class PredictRequest(BaseModel):
    hours: List[WeatherHour]

class DayOptimizeRequest(BaseModel):
    date: str                            = Field(..., example="2024-06-15",
                                                  description="Date to optimise (YYYY-MM-DD)")
    optimizer: str                       = Field("lp", description="'rule' or 'lp'")
    initial_soc: float                   = Field(0.50, ge=0, le=1)

class TrainRequest(BaseModel):
    model_name: str = Field("Random Forest",
                             description="Linear Regression | Ridge Regression | Random Forest | Gradient Boosting | XGBoost")
    train_ratio: float = Field(0.80, ge=0.5, le=0.95)


# ═══════════════════════════════════════════════════════════════════════════════
# Endpoints
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/", tags=["Health"])
def root():
    return {
        "service": "Solar AI — Demand Forecast & Battery Optimizer",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
def health():
    fc  = STATE["forecaster"]
    df  = STATE["full_df"]
    return {
        "status":        "healthy" if fc is not None else "degraded",
        "model_trained": fc is not None,
        "model_name":    fc.model_name if fc else None,
        "train_metrics": STATE["train_metrics"],
        "dataset_rows":  len(df) if df is not None else 0,
        "data_source":   STATE["data_source"],
        "loaded_at":     STATE["loaded_at"],
        "timestamp_utc": datetime.utcnow().isoformat(),
    }


@app.get("/data/status", tags=["Data"])
def data_status():
    df = STATE["full_df"]
    if df is None:
        raise HTTPException(503, "Dataset not loaded yet.")
    return {
        "rows":        len(df),
        "start_date":  str(df["time"].min()),
        "end_date":    str(df["time"].max()),
        "columns":     df.columns.tolist(),
        "data_source": STATE["data_source"],
        "loaded_at":   STATE["loaded_at"],
        "mean_demand_kw":  round(df["demand_kw"].mean(), 4),
        "daily_avg_kwh":   round(df["demand_kw"].sum() / max(df["time"].dt.date.nunique(),1), 2),
    }


@app.post("/data/reload", tags=["Data"])
def data_reload(background_tasks: BackgroundTasks, force_download: bool = Query(False)):
    """
    Reload dataset.
    Set force_download=true to fetch fresh data from the OpenMeteo API.
    """
    background_tasks.add_task(_load_and_train, force_download=force_download)
    return {
        "message": ("Reloading dataset from OpenMeteo API..." if force_download
                    else "Reloading dataset (local/GitHub)..."),
        "hint": "Call /health after a few seconds to check status.",
    }


@app.post("/train", tags=["Model"])
def train(req: TrainRequest):
    """Re-train the demand forecasting model on the loaded dataset."""
    df = STATE["full_df"]
    if df is None:
        raise HTTPException(503, "Dataset not loaded. Call /data/reload first.")
    split = int(len(df) * req.train_ratio)
    if split < 200:
        raise HTTPException(400, f"Training split too small ({split} rows). Need at least 200.")
    try:
        fc = DemandForecaster(req.model_name)
    except ValueError as e:
        raise HTTPException(400, str(e))

    fc.fit(df.iloc[:split], verbose=True)
    m  = fc.evaluate(df.iloc[split:])
    fc.save("models")
    STATE["forecaster"]    = fc
    STATE["train_metrics"] = m

    return {
        "model":      req.model_name,
        "train_rows": split,
        "test_rows":  len(df) - split,
        "metrics": {
            "mae_kw":  round(m["mae"], 4),
            "rmse_kw": round(m["rmse"], 4),
            "r2":      round(m["r2"], 4),
            "mape_pct":round(m["mape"], 2),
        },
        "message": "Model trained and saved.",
    }


@app.get("/forecast/next", tags=["Forecast"])
def forecast_next(
    hours: int = Query(24, ge=1, le=168, description="Hours to forecast ahead"),
):
    """
    Forecast demand for the next N hours using the last available history.
    Returns predicted demand in kW per hour.
    """
    fc = STATE["forecaster"]
    df = STATE["full_df"]
    if fc is None:
        raise HTTPException(503, "Model not trained. Call /train first.")
    if df is None:
        raise HTTPException(503, "Dataset not loaded.")

    # Use last 7 days as context window
    context = df.tail(168).copy()
    preds   = fc.predict_next_hours(context, n_hours=hours)

    return {
        "forecast_hours": hours,
        "from_time":      str(preds["time"].iloc[0]),
        "to_time":        str(preds["time"].iloc[-1]),
        "predictions":    preds.to_dict(orient="records"),
        "total_predicted_kwh": round(preds["predicted_demand_kw"].sum(), 3),
        "avg_demand_kw":  round(preds["predicted_demand_kw"].mean(), 4),
    }


@app.post("/forecast/predict", tags=["Forecast"])
def forecast_predict(req: PredictRequest):
    """
    Predict demand for a list of arbitrary weather + time inputs.
    Each row should provide temperature, GHI, humidity, wind, and timestamp.
    Optionally supply demand_kw for the history rows to enable lag features.
    """
    fc = STATE["forecaster"]
    if fc is None:
        raise HTTPException(503, "Model not trained. Call /train first.")

    if not req.hours:
        return {"count": 0, "predictions": [], "total_kwh": 0.0}

    rows = []
    for h in req.hours:
        row = h.model_dump()          # Pydantic v2: model_dump() replaces .dict()
        row["time"] = pd.to_datetime(row["time"])
        if row["demand_kw"] is None:
            row["demand_kw"] = 0.5
        rows.append(row)

    df_in = pd.DataFrame(rows)
    preds  = fc.predict(df_in)

    result = []
    for i, h in enumerate(req.hours):
        result.append({
            "time":              h.time,
            "predicted_demand_kw": round(float(preds[i]), 4),
            "inputs": {
                "temperature_c": h.temperature_2m,
                "ghi_wm2":       h.shortwave_radiation,
                "humidity_pct":  h.relative_humidity_2m,
            }
        })

    return {
        "count":       len(result),
        "predictions": result,
        "total_kwh":   round(sum(r["predicted_demand_kw"] for r in result), 3),
    }


@app.post("/optimize/day", tags=["Battery Optimizer"])
def optimize_day(req: DayOptimizeRequest):
    """
    Run battery optimizer for a specific date (24-hour horizon).
    Uses the dataset's real solar irradiance and demand for that date.
    Returns hourly energy dispatch and INR costs.
    """
    df = STATE["full_df"]
    if df is None:
        raise HTTPException(503, "Dataset not loaded.")

    day_df = df[df["time"].dt.strftime("%Y-%m-%d") == req.date]
    if len(day_df) == 0:
        raise HTTPException(404, f"No data for date {req.date}. "
                                  f"Available range: {df['time'].min().date()} – {df['time'].max().date()}")

    if req.optimizer == "lp":
        lp   = STATE["lp_optimizer"]
        lp.batt.initial_soc = req.initial_soc
        result = lp.optimize_day(
            demand_kw=day_df["demand_kw"].values,
            ghi_wm2=day_df.get("shortwave_radiation", pd.Series([0]*24)).values,
            initial_soc=req.initial_soc,
        )
    else:
        opt = RuleBasedOptimizer()
        opt.batt.initial_soc = req.initial_soc
        result = opt.run(day_df)

    total_cost   = result["grid_cost_inr"].sum()
    total_earn   = result["export_earn_inr"].sum()
    total_import = result["grid_import_kw"].sum()
    total_demand = result["demand_kw"].sum()

    return {
        "date":         req.date,
        "optimizer":    req.optimizer,
        "initial_soc":  req.initial_soc,
        "total_demand_kwh":   round(total_demand, 3),
        "total_solar_kwh":    round(result["solar_gen_kw"].sum(), 3),
        "total_import_kwh":   round(total_import, 3),
        "total_export_kwh":   round(result["grid_export_kw"].sum(), 3),
        "grid_cost_inr":      round(total_cost, 2),
        "export_earn_inr":    round(total_earn, 2),
        "net_cost_inr":       round(total_cost - total_earn, 2),
        "self_sufficiency_pct": round((1-total_import/max(total_demand,1e-6))*100, 1),
        "hourly_schedule": result.to_dict(orient="records"),
    }


@app.get("/optimize/annual", tags=["Battery Optimizer"])
def optimize_annual():
    """
    Run rule-based optimizer across the entire loaded dataset.
    Returns annual energy and cost summary in INR.
    """
    df = STATE["full_df"]
    if df is None:
        raise HTTPException(503, "Dataset not loaded.")

    opt    = RuleBasedOptimizer()
    result = opt.run(df)
    rep    = annual_report(result)

    # Monthly breakdown
    result["month"] = pd.to_datetime([r["time"] for _, r in result.iterrows()]).month
    monthly = (result.groupby("month")
               .agg(demand_kwh=("demand_kw","sum"), solar_kwh=("solar_gen_kw","sum"),
                    import_kwh=("grid_import_kw","sum"), export_kwh=("grid_export_kw","sum"),
                    net_cost_inr=("net_cost_inr","sum"))
               .reset_index())
    months = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
              7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    monthly["month"] = monthly["month"].map(months)

    return {
        "annual_summary": rep,
        "monthly_breakdown": monthly.round(2).to_dict(orient="records"),
        "currency": "INR",
        "system": {"solar_kwp":3.0,"battery_kwh":5.0,"location":"Delhi, India"},
    }


@app.get("/summary", tags=["Summary"])
def summary():
    """High-level dashboard summary combining model status + annual economics."""
    fc = STATE["forecaster"]
    df = STATE["full_df"]
    if df is None:
        raise HTTPException(503, "Dataset not loaded.")

    opt    = RuleBasedOptimizer()
    result = opt.run(df.head(8760) if len(df) > 8760 else df)  # cap at 1 year
    rep    = annual_report(result)

    return {
        "system": {
            "location":     "Delhi, India (28.6°N, 77.2°E)",
            "solar_kwp":    3.0,
            "battery_kwh":  5.0,
            "grid_tariff":  "Rs.5-10/kWh (BSES Delhi ToU)",
            "export_rate":  "Rs.3/kWh (net metering)",
        },
        "model": {
            "name":    fc.model_name if fc else "not trained",
            "trained": fc is not None,
            "metrics": STATE["train_metrics"],
        },
        "dataset": {
            "source":     STATE["data_source"],
            "rows":       len(df),
            "start":      str(df["time"].min().date()),
            "end":        str(df["time"].max().date()),
        },
        "economics": rep,
        "timestamp_utc": datetime.utcnow().isoformat(),
    }
