# -*- coding: utf-8 -*-
"""
demand_forecaster.py  —  DemandForecaster class
Week 2, Member 2 | AI Solar Panel Automation System
"""
from __future__ import annotations

import os, warnings
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.preprocessing import StandardScaler

try:
    from xgboost import XGBRegressor
    _XGBOOST = True
except ImportError:
    _XGBOOST = False

warnings.filterwarnings("ignore")

TARGET_COL = "demand_kw"

FEATURE_COLS = [
    "hour_sin","hour_cos","month_sin","month_cos","dow_sin","dow_cos",
    "is_weekend","is_morning_peak","is_evening_peak","quarter",
    "temperature_2m","temp_sq","feels_hot","feels_cold",
    "ghi_norm","humidity_norm","wind_speed_10m",
    "demand_lag_1h","demand_lag_2h","demand_lag_3h","demand_lag_6h",
    "demand_lag_12h","demand_lag_24h","demand_lag_48h",
    "demand_same_hour_yesterday","demand_same_hour_lastweek",
    "demand_roll_mean_3h","demand_roll_mean_6h","demand_roll_mean_24h",
    "demand_roll_std_6h","demand_roll_std_24h",
]


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add temporal + weather + lag/rolling features."""
    feat = df.copy()
    t = feat["time"]

    feat["hour"]            = t.dt.hour
    feat["day_of_week"]     = t.dt.dayofweek
    feat["month"]           = t.dt.month
    feat["quarter"]         = t.dt.quarter
    feat["is_weekend"]      = (t.dt.dayofweek >= 5).astype(int)
    feat["is_morning_peak"] = ((t.dt.hour >= 6) & (t.dt.hour <= 9)).astype(int)
    feat["is_evening_peak"] = ((t.dt.hour >= 18) & (t.dt.hour <= 23)).astype(int)

    feat["hour_sin"]  = np.sin(2*np.pi*feat["hour"]/24)
    feat["hour_cos"]  = np.cos(2*np.pi*feat["hour"]/24)
    feat["month_sin"] = np.sin(2*np.pi*feat["month"]/12)
    feat["month_cos"] = np.cos(2*np.pi*feat["month"]/12)
    feat["dow_sin"]   = np.sin(2*np.pi*feat["day_of_week"]/7)
    feat["dow_cos"]   = np.cos(2*np.pi*feat["day_of_week"]/7)

    if "temperature_2m" in feat.columns:
        feat["temp_sq"]    = feat["temperature_2m"]**2
        feat["feels_hot"]  = (feat["temperature_2m"] > 32).astype(int)
        feat["feels_cold"] = (feat["temperature_2m"] < 15).astype(int)
    if "shortwave_radiation" in feat.columns:
        feat["ghi_norm"]   = feat["shortwave_radiation"] / 1000
    if "relative_humidity_2m" in feat.columns:
        feat["humidity_norm"] = feat["relative_humidity_2m"] / 100

    for lag in [1,2,3,6,12,24,48,168]:
        feat[f"demand_lag_{lag}h"] = feat[TARGET_COL].shift(lag)

    for w in [3,6,12,24]:
        feat[f"demand_roll_mean_{w}h"] = feat[TARGET_COL].shift(1).rolling(w,min_periods=1).mean()
        feat[f"demand_roll_std_{w}h"]  = feat[TARGET_COL].shift(1).rolling(w,min_periods=1).std().fillna(0)

    feat["demand_same_hour_yesterday"] = feat[TARGET_COL].shift(24)
    feat["demand_same_hour_lastweek"]  = feat[TARGET_COL].shift(168)
    return feat


def _registry():
    r = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression":  Ridge(alpha=1.0),
        "Random Forest":     RandomForestRegressor(n_estimators=100, max_depth=12,
                                                    min_samples_leaf=5, n_jobs=-1, random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(n_estimators=150, max_depth=5,
                                                        learning_rate=0.05, random_state=42),
    }
    if _XGBOOST:
        r["XGBoost"] = XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.05,
                                     subsample=0.8, colsample_bytree=0.8, random_state=42, verbosity=0)
    return r


class DemandForecaster:
    """ML demand forecasting pipeline for an Indian household."""

    def __init__(self, model_name="Random Forest", feature_cols=None, scale_features=False):
        reg = _registry()
        if model_name not in reg:
            raise ValueError(f"model_name must be one of {list(reg.keys())}")
        self.model_name    = model_name
        self.model         = reg[model_name]
        self.feature_cols  = feature_cols or FEATURE_COLS
        self.scale_features= scale_features
        self.scaler        = StandardScaler() if scale_features else None
        self._is_trained   = False
        self.metrics_      = {}

    def fit(self, df: pd.DataFrame, verbose=True):
        feat  = engineer_features(df).dropna().reset_index(drop=True)
        avail = [c for c in self.feature_cols if c in feat.columns]
        X = feat[avail].values
        y = feat[TARGET_COL].values
        if self.scale_features:
            X = self.scaler.fit_transform(X)
        self.model.fit(X, y)
        self._is_trained   = True
        self._feature_cols = avail
        if verbose:
            p = self.model.predict(X)
            print(f"[{self.model_name}] Trained {len(X):,} rows | "
                  f"Train MAE={mean_absolute_error(y,p):.4f} kW | R²={r2_score(y,p):.4f}")
        return self

    def evaluate(self, df: pd.DataFrame) -> dict:
        self._check_trained()
        feat  = engineer_features(df).fillna(0).reset_index(drop=True)
        X = feat[self._feature_cols].values
        y = feat[TARGET_COL].values
        if self.scale_features:
            X = self.scaler.transform(X)
        preds = self.model.predict(X)
        m = {
            "mae":  float(mean_absolute_error(y, preds)),
            "rmse": float(np.sqrt(mean_squared_error(y, preds))),
            "r2":   float(r2_score(y, preds)),
            "mape": float(np.mean(np.abs((y - preds)/(y+1e-9)))*100),
        }
        self.metrics_ = m
        return m

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        self._check_trained()
        feat = engineer_features(df).fillna(0)
        X    = feat[self._feature_cols].values
        if self.scale_features:
            X = self.scaler.transform(X)
        return self.model.predict(X)

    def predict_next_hours(self, history_df: pd.DataFrame, n_hours: int = 24) -> pd.DataFrame:
        """
        Forecast the next n_hours demand given a history DataFrame.
        Uses recursive single-step prediction.
        """
        self._check_trained()
        buf = history_df.copy()
        last_ts = pd.to_datetime(buf["time"].iloc[-1])
        out_records = []

        for i in range(n_hours):
            next_ts = last_ts + pd.Timedelta(hours=i+1)
            # Build a single-row input
            new_row = buf.iloc[-1:].copy()
            new_row["time"] = next_ts
            # Copy weather columns forward (persistence assumption)
            extended = pd.concat([buf, new_row], ignore_index=True)
            feat     = engineer_features(extended).fillna(0)
            X        = feat.iloc[[-1]][self._feature_cols].values
            if self.scale_features:
                X = self.scaler.transform(X)
            pred_kw  = float(self.model.predict(X)[0])
            new_row[TARGET_COL] = pred_kw
            buf = pd.concat([buf, new_row], ignore_index=True)
            out_records.append({"time": next_ts, "predicted_demand_kw": round(pred_kw, 4)})

        return pd.DataFrame(out_records)

    def feature_importances(self) -> pd.DataFrame | None:
        self._check_trained()
        if not hasattr(self.model, "feature_importances_"):
            return None
        fi = self.model.feature_importances_
        return (pd.DataFrame({"feature": self._feature_cols, "importance": fi})
                .sort_values("importance", ascending=False).reset_index(drop=True))

    def save(self, directory="../models") -> str:
        self._check_trained()
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, f"demand_{self.model_name.lower().replace(' ','_')}.pkl")
        joblib.dump({"model": self.model, "scaler": self.scaler,
                     "feature_cols": self._feature_cols, "model_name": self.model_name}, path)
        print(f"Saved model → {path}")
        return path

    @classmethod
    def load(cls, path: str):
        p   = joblib.load(path)
        obj = cls.__new__(cls)
        obj.model_name    = p["model_name"]
        obj.model         = p["model"]
        obj.scaler        = p["scaler"]
        obj._feature_cols = p["feature_cols"]
        obj.feature_cols  = p["feature_cols"]
        obj.scale_features= obj.scaler is not None
        obj._is_trained   = True
        obj.metrics_      = {}
        print(f"Loaded model ← {path}")
        return obj

    def _check_trained(self):
        if not self._is_trained:
            raise RuntimeError("Model not trained. Call .fit() first.")
