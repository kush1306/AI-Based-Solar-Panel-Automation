# -*- coding: utf-8 -*-
"""
tests/test_api.py — FastAPI endpoint tests using TestClient (httpx)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
import pandas as pd
import numpy as np
from fastapi.testclient import TestClient

# Patch data loading so tests don't hit network
import src.api as api_module


@pytest.fixture(scope="module")
def client():
    """TestClient that overrides startup to use synthetic data."""
    from src.data_loader import _synthetic_delhi, generate_demand
    from src.demand_forecaster import DemandForecaster

    weather = _synthetic_delhi("2024-01-01", "2024-06-30", seed=0)
    full_df = generate_demand(weather)
    split   = int(len(full_df)*0.8)

    fc = DemandForecaster("Random Forest")
    fc.fit(full_df.iloc[:split], verbose=False)

    api_module.STATE["full_df"]      = full_df
    api_module.STATE["forecaster"]   = fc
    api_module.STATE["data_source"]  = "test_synthetic"
    api_module.STATE["loaded_at"]    = "2024-01-01T00:00:00"
    api_module.STATE["train_metrics"]= fc.evaluate(full_df.iloc[split:])

    with TestClient(api_module.app) as c:
        yield c


class TestHealthEndpoints:
    def test_root(self, client):
        r = client.get("/")
        assert r.status_code == 200
        d = r.json()
        assert d["status"] == "running"
        assert "docs" in d

    def test_health(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        d = r.json()
        assert d["model_trained"] is True
        assert d["dataset_rows"] > 0
        assert "train_metrics" in d

    def test_health_has_metrics(self, client):
        r = client.get("/health")
        m = r.json()["train_metrics"]
        assert "mae" in m and "r2" in m
        assert m["mae"] >= 0


class TestDataEndpoints:
    def test_data_status(self, client):
        r = client.get("/data/status")
        assert r.status_code == 200
        d = r.json()
        assert d["rows"] > 0
        assert "start_date" in d
        assert "columns" in d
        assert isinstance(d["data_source"], str) and len(d["data_source"]) > 0

    def test_data_reload_returns_202(self, client):
        # reload is async — just check it accepts the request
        r = client.post("/data/reload?force_download=false")
        assert r.status_code == 200
        assert "message" in r.json()


class TestTrainEndpoint:
    def test_train_random_forest(self, client):
        r = client.post("/train", json={"model_name":"Random Forest","train_ratio":0.8})
        assert r.status_code == 200
        d = r.json()
        assert d["model"] == "Random Forest"
        assert d["metrics"]["mae_kw"] >= 0
        assert d["metrics"]["r2"] <= 1.0

    def test_train_ridge(self, client):
        r = client.post("/train", json={"model_name":"Ridge Regression","train_ratio":0.8})
        assert r.status_code == 200

    def test_train_invalid_model(self, client):
        r = client.post("/train", json={"model_name":"NonExistent","train_ratio":0.8})
        assert r.status_code == 400


class TestForecastEndpoints:
    def test_forecast_next_24h(self, client):
        r = client.get("/forecast/next?hours=24")
        assert r.status_code == 200
        d = r.json()
        assert d["forecast_hours"] == 24
        assert len(d["predictions"]) == 24
        assert all(p["predicted_demand_kw"] >= 0 for p in d["predictions"])

    def test_forecast_next_1h(self, client):
        r = client.get("/forecast/next?hours=1")
        assert r.status_code == 200
        assert len(r.json()["predictions"]) == 1

    def test_forecast_next_168h(self, client):
        r = client.get("/forecast/next?hours=168")
        assert r.status_code == 200
        assert len(r.json()["predictions"]) == 168

    def test_forecast_predict_custom(self, client):
        payload = {"hours": [
            {"time":"2024-06-15T14:00:00","temperature_2m":38.0,
             "relative_humidity_2m":45.0,"shortwave_radiation":750.0,
             "wind_speed_10m":3.5,"precipitation":0.0},
            {"time":"2024-06-15T20:00:00","temperature_2m":32.0,
             "relative_humidity_2m":60.0,"shortwave_radiation":0.0,
             "wind_speed_10m":2.0,"precipitation":0.0},
        ]}
        r = client.post("/forecast/predict", json=payload)
        assert r.status_code == 200
        d = r.json()
        assert d["count"] == 2
        assert len(d["predictions"]) == 2
        assert all(p["predicted_demand_kw"] >= 0 for p in d["predictions"])

    def test_forecast_predict_empty(self, client):
        r = client.post("/forecast/predict", json={"hours":[]})
        assert r.status_code == 200
        assert r.json()["count"] == 0


class TestBatteryOptimizer:
    def test_optimize_day_rule(self, client):
        r = client.post("/optimize/day",
                        json={"date":"2024-03-15","optimizer":"rule","initial_soc":0.5})
        assert r.status_code == 200
        d = r.json()
        assert "hourly_schedule" in d
        assert len(d["hourly_schedule"]) == 24
        assert d["net_cost_inr"] is not None
        assert 0 <= d["self_sufficiency_pct"] <= 100

    def test_optimize_day_lp(self, client):
        r = client.post("/optimize/day",
                        json={"date":"2024-03-15","optimizer":"lp","initial_soc":0.5})
        assert r.status_code == 200
        d = r.json()
        assert len(d["hourly_schedule"]) == 24

    def test_optimize_day_not_found(self, client):
        r = client.post("/optimize/day",
                        json={"date":"2020-01-01","optimizer":"rule","initial_soc":0.5})
        assert r.status_code == 404

    def test_optimize_annual(self, client):
        r = client.get("/optimize/annual")
        assert r.status_code == 200
        d = r.json()
        assert "annual_summary" in d
        rep = d["annual_summary"]
        assert rep["total_demand_kwh"] > 0
        assert rep["self_sufficiency_pct"] >= 0
        assert "annual_savings_inr" in rep
        assert "monthly_breakdown" in d

    def test_annual_has_12_months(self, client):
        r = client.get("/optimize/annual")
        mb = r.json()["monthly_breakdown"]
        assert 1 <= len(mb) <= 12


class TestSummaryEndpoint:
    def test_summary(self, client):
        r = client.get("/summary")
        assert r.status_code == 200
        d = r.json()
        assert "system" in d
        assert "model" in d
        assert "economics" in d
        assert "dataset" in d

    def test_summary_system_specs(self, client):
        d = client.get("/summary").json()["system"]
        assert d["solar_kwp"]   == 3.0
        assert d["battery_kwh"] == 5.0
        assert "Delhi" in d["location"]

    def test_summary_economics_keys(self, client):
        econ = client.get("/summary").json()["economics"]
        for key in ["annual_savings_inr","self_sufficiency_pct","net_cost_inr"]:
            assert key in econ, f"Missing key: {key}"
