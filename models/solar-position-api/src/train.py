"""
train.py -- Train, evaluate, and persist regression models for shortwave
irradiance prediction in the solar-position-api project.

Models trained
--------------
- XGBoost        (XGBRegressor)
- LightGBM       (LGBMRegressor)
- Random Forest  (RandomForestRegressor)  -- baseline

Each model undergoes a light RandomizedSearchCV over a small parameter space,
using TimeSeriesSplit so that CV folds respect temporal ordering (no leakage).

The model with the lowest test-set RMSE is saved as the winner.

Run standalone:
    python -m src.train
"""

from __future__ import annotations

import json
import logging
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")  # non-interactive backend -- safe for headless runs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit
from xgboost import XGBRegressor

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import MODEL_DIR  # noqa: E402
from src.features import (  # noqa: E402
    FEATURE_COLS,
    FEATURES_CSV,
    TARGET_COL,
    build_feature_dataset,
    chronological_train_test_split,
)

warnings.filterwarnings("ignore", category=UserWarning)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
MODEL_PATH = Path(PROJECT_ROOT) / MODEL_DIR
BEST_MODEL_PKL = MODEL_PATH / "best_model.pkl"
MODEL_METADATA_JSON = MODEL_PATH / "model_metadata.json"
FEATURE_IMPORTANCE_PNG = MODEL_PATH / "feature_importance.png"

# ---------------------------------------------------------------------------
# Hyperparameter search configuration
# ---------------------------------------------------------------------------
# TimeSeriesSplit keeps CV folds in temporal order, preventing look-ahead bias
# inside the training window (analagous to the train/test split rationale).
CV_SPLITS = 3
N_ITER_XGBOOST = 10
N_ITER_LGBM = 10
N_ITER_RF = 5      # Random Forest is slower -- fewer iterations
SHAP_SAMPLE_SIZE = 1_000  # rows sampled from test set for SHAP computation

PARAM_DISTRIBUTIONS: dict[str, dict] = {
    "xgboost": {
        "n_estimators": [300, 500, 800],
        "max_depth": [4, 6, 8],
        "learning_rate": [0.01, 0.05, 0.10],
        "subsample": [0.8, 1.0],
        "colsample_bytree": [0.8, 1.0],
        "min_child_weight": [1, 3, 5],
    },
    "lightgbm": {
        "n_estimators": [300, 500, 800],
        "max_depth": [-1, 6, 8],
        "learning_rate": [0.01, 0.05, 0.10],
        "num_leaves": [31, 63, 127],
        "subsample": [0.8, 1.0],
        "colsample_bytree": [0.8, 1.0],
    },
    "random_forest": {
        "n_estimators": [100, 200, 300],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5, 10],
        "max_features": ["sqrt", "log2"],
    },
}


# ---------------------------------------------------------------------------
# 1. Data loading
# ---------------------------------------------------------------------------

def load_data(test_years: int = 2) -> tuple[
    pd.DataFrame, pd.DataFrame, pd.Series, pd.Series
]:
    """
    Load the feature dataset (building it from scratch if not cached) and
    return a chronological train/test split.

    Parameters
    ----------
    test_years : int
        Number of most-recent years to reserve for the test set.

    Returns
    -------
    X_train, X_test : pd.DataFrame
    y_train, y_test : pd.Series
    """
    features_path = Path(FEATURES_CSV)
    if features_path.exists():
        logger.info("Loading cached feature dataset from '%s' ...", features_path)
        df = pd.read_csv(features_path, index_col="time", parse_dates=True)
        from src.config import TIMEZONE  # noqa: F401
        if df.index.tz is None:
            df.index = df.index.tz_localize("Asia/Kolkata")
    else:
        logger.info("Feature dataset not found -- running build_feature_dataset() ...")
        df = build_feature_dataset()

    X_train, X_test, y_train, y_test = chronological_train_test_split(
        df, test_years=test_years
    )
    logger.info(
        "Data loaded -- train: %d rows | test: %d rows | features: %d",
        len(X_train), len(X_test), len(FEATURE_COLS),
    )
    return X_train, X_test, y_train, y_test


# ---------------------------------------------------------------------------
# 2. Model training with RandomizedSearchCV
# ---------------------------------------------------------------------------

def _make_base_estimators() -> dict[str, object]:
    """Return fresh base estimator instances keyed by model name.

    All estimators are seeded with random_state=42 so that training runs are
    fully reproducible across machines and Python sessions.
    """
    return {
        "xgboost": XGBRegressor(
            objective="reg:squarederror",
            random_state=42,
            n_jobs=-1,
            verbosity=0,
        ),
        "lightgbm": LGBMRegressor(
            objective="regression",
            random_state=42,
            n_jobs=-1,
            verbose=-1,
        ),
        "random_forest": RandomForestRegressor(
            random_state=42,
            n_jobs=-1,
        ),
    }


def train_all_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> dict[str, object]:
    """
    Run RandomizedSearchCV for each candidate model over its parameter grid.

    Uses TimeSeriesSplit to ensure that each validation fold only ever sees
    data that is chronologically *after* its corresponding training fold.

    Parameters
    ----------
    X_train : pd.DataFrame
    y_train : pd.Series

    Returns
    -------
    dict[str, best_estimator]
        Mapping of model name to the best fitted estimator found by search.
    """
    tscv = TimeSeriesSplit(n_splits=CV_SPLITS)
    base_estimators = _make_base_estimators()
    n_iters = {
        "xgboost": N_ITER_XGBOOST,
        "lightgbm": N_ITER_LGBM,
        "random_forest": N_ITER_RF,
    }
    best_models: dict[str, object] = {}

    for name, estimator in base_estimators.items():
        logger.info(
            "Training %s with RandomizedSearchCV (n_iter=%d, cv=%d) ...",
            name, n_iters[name], CV_SPLITS,
        )
        search = RandomizedSearchCV(
            estimator=estimator,
            param_distributions=PARAM_DISTRIBUTIONS[name],
            n_iter=n_iters[name],
            scoring="neg_root_mean_squared_error",
            cv=tscv,
            random_state=42,
            n_jobs=-1,
            refit=True,
            verbose=0,
        )
        search.fit(X_train, y_train)
        best_models[name] = search.best_estimator_
        logger.info(
            "  %s -- best CV RMSE: %.4f | best params: %s",
            name,
            -search.best_score_,
            search.best_params_,
        )

    return best_models


# ---------------------------------------------------------------------------
# 3. Evaluation
# ---------------------------------------------------------------------------

def evaluate_models(
    models: dict[str, object],
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> pd.DataFrame:
    """
    Evaluate all trained models on the held-out test set.

    Parameters
    ----------
    models : dict[str, estimator]
    X_test : pd.DataFrame
    y_test : pd.Series

    Returns
    -------
    pd.DataFrame
        Comparison table with columns: Model, RMSE, MAE, R2.
        Sorted ascending by RMSE.
    """
    rows = []
    for name, model in models.items():
        y_pred = model.predict(X_test)
        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        mae = float(mean_absolute_error(y_test, y_pred))
        r2 = float(r2_score(y_test, y_pred))
        rows.append({"Model": name, "RMSE": rmse, "MAE": mae, "R2": r2})
        logger.info(
            "  %-15s RMSE=%.4f | MAE=%.4f | R2=%.4f",
            name, rmse, mae, r2,
        )

    results = pd.DataFrame(rows).sort_values("RMSE").reset_index(drop=True)
    return results


# ---------------------------------------------------------------------------
# 4. SHAP feature importance
# ---------------------------------------------------------------------------

def compute_and_save_feature_importance(
    model_name: str,
    model: object,
    X_test: pd.DataFrame,
    feature_names: list[str],
    output_path: Path,
) -> list[dict]:
    """
    Compute feature importances via the model's built-in attribute (for
    tree-based models) and supplement with SHAP mean absolute values on a
    random sample of the test set.

    Saves a bar chart PNG to *output_path* and returns the top-5 list.

    Parameters
    ----------
    model_name : str
    model : fitted estimator
    X_test : pd.DataFrame
    feature_names : list[str]
    output_path : Path

    Returns
    -------
    list[dict]
        Top-5 features sorted by mean |SHAP value|.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # ---- Built-in importances (gain-based for XGB/LGB, impurity for RF) ----
    importances = model.feature_importances_
    imp_series = pd.Series(importances, index=feature_names).sort_values(ascending=False)

    # ---- SHAP values on a sample ----
    logger.info(
        "Computing SHAP values on %d test-set samples (model: %s) ...",
        SHAP_SAMPLE_SIZE, model_name,
    )
    rng = np.random.default_rng(42)
    sample_idx = rng.choice(len(X_test), size=min(SHAP_SAMPLE_SIZE, len(X_test)), replace=False)
    X_sample = X_test.iloc[sample_idx]

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)
    shap_importance = pd.Series(
        np.abs(shap_values).mean(axis=0),
        index=feature_names,
    ).sort_values(ascending=False)

    # ---- Plot: dual bar chart ----
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(
        f"Feature Importance -- {model_name.upper()}",
        fontsize=14, fontweight="bold",
    )

    # Subplot 1: built-in
    axes[0].barh(
        imp_series.index[::-1], imp_series.values[::-1],
        color="#4C72B0", edgecolor="white",
    )
    axes[0].set_title("Built-in Feature Importance (Gain / Impurity)")
    axes[0].set_xlabel("Importance Score")
    axes[0].tick_params(axis="y", labelsize=9)

    # Subplot 2: SHAP
    axes[1].barh(
        shap_importance.index[::-1], shap_importance.values[::-1],
        color="#DD8452", edgecolor="white",
    )
    axes[1].set_title(f"Mean |SHAP| (n={SHAP_SAMPLE_SIZE} samples)")
    axes[1].set_xlabel("Mean |SHAP value|")
    axes[1].tick_params(axis="y", labelsize=9)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Feature importance chart saved to '%s'.", output_path)

    # ---- Top-5 by SHAP ----
    top5 = [
        {"feature": feat, "shap_importance": round(float(score), 6)}
        for feat, score in shap_importance.head(5).items()
    ]
    return top5


# ---------------------------------------------------------------------------
# 5. Persist winner
# ---------------------------------------------------------------------------

def save_winner(
    model_name: str,
    model: object,
    metrics: dict,
    feature_names: list[str],
) -> None:
    """
    Persist the best model as a pickle file and write a JSON metadata sidecar.

    Parameters
    ----------
    model_name : str
    model : fitted estimator
    metrics : dict  -- keys: test_rmse, test_mae, test_r2
    feature_names : list[str]
    """
    MODEL_PATH.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, BEST_MODEL_PKL)
    logger.info("Best model saved to '%s'.", BEST_MODEL_PKL)

    metadata = {
        "model_name": model_name,
        "test_rmse": round(metrics["test_rmse"], 6),
        "test_mae": round(metrics["test_mae"], 6),
        "test_r2": round(metrics["test_r2"], 6),
        "feature_names": feature_names,
        "trained_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(MODEL_METADATA_JSON, "w", encoding="utf-8") as fh:
        json.dump(metadata, fh, indent=2)
    logger.info("Model metadata saved to '%s'.", MODEL_METADATA_JSON)


# ---------------------------------------------------------------------------
# 6. Full training pipeline
# ---------------------------------------------------------------------------

def run_training_pipeline(test_years: int = 2) -> dict:
    """
    Orchestrate the end-to-end training, evaluation, and persistence pipeline.

    Parameters
    ----------
    test_years : int
        Years reserved for the held-out test set.

    Returns
    -------
    dict
        Summary with keys: comparison_table, winner_name, winner_metrics,
        top5_features.
    """
    # -- Data ----------------------------------------------------------------
    X_train, X_test, y_train, y_test = load_data(test_years=test_years)

    # -- Train ---------------------------------------------------------------
    logger.info("=" * 55)
    logger.info("PHASE 1 -- Model training")
    logger.info("=" * 55)
    models = train_all_models(X_train, y_train)

    # -- Evaluate ------------------------------------------------------------
    logger.info("=" * 55)
    logger.info("PHASE 2 -- Test-set evaluation")
    logger.info("=" * 55)
    results_df = evaluate_models(models, X_test, y_test)

    # -- Select winner -------------------------------------------------------
    winner_row = results_df.iloc[0]
    winner_name = winner_row["Model"]
    winner_model = models[winner_name]
    winner_metrics = {
        "test_rmse": winner_row["RMSE"],
        "test_mae": winner_row["MAE"],
        "test_r2": winner_row["R2"],
    }

    logger.info(
        "Winner: %s (lowest test RMSE = %.4f)", winner_name, winner_metrics["test_rmse"]
    )

    # -- Feature importance + SHAP ------------------------------------------
    logger.info("=" * 55)
    logger.info("PHASE 3 -- Feature importance and SHAP analysis")
    logger.info("=" * 55)
    top5 = compute_and_save_feature_importance(
        model_name=winner_name,
        model=winner_model,
        X_test=X_test,
        feature_names=FEATURE_COLS,
        output_path=FEATURE_IMPORTANCE_PNG,
    )

    # -- Save ----------------------------------------------------------------
    logger.info("=" * 55)
    logger.info("PHASE 4 -- Persisting winner")
    logger.info("=" * 55)
    save_winner(winner_name, winner_model, winner_metrics, FEATURE_COLS)

    return {
        "comparison_table": results_df,
        "winner_name": winner_name,
        "winner_metrics": winner_metrics,
        "top5_features": top5,
    }


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting training pipeline ...")

    summary = run_training_pipeline()

    print("\n" + "=" * 60)
    print("MODEL COMPARISON TABLE (sorted by RMSE, ascending)")
    print("=" * 60)
    tbl = summary["comparison_table"].copy()
    tbl["RMSE"] = tbl["RMSE"].map("{:.4f}".format)
    tbl["MAE"] = tbl["MAE"].map("{:.4f}".format)
    tbl["R2"] = tbl["R2"].map("{:.4f}".format)
    print(tbl.to_string(index=False))

    print("\n" + "=" * 60)
    winner = summary["winner_name"]
    m = summary["winner_metrics"]
    print(f"WINNING MODEL : {winner}")
    print(f"  Test RMSE   : {m['test_rmse']:.4f} W/m2")
    print(f"  Test MAE    : {m['test_mae']:.4f} W/m2")
    print(f"  Test R2     : {m['test_r2']:.4f}")
    print(
        "\nWhy this model won: it achieved the lowest RMSE on the "
        "held-out chronological test set (2023-06-01 to 2025-06-01), "
        "meaning its predictions are closest to actual irradiance "
        "values on unseen future data -- the metric that matters most "
        "for production deployment."
    )

    print("\n" + "=" * 60)
    print("TOP 5 FEATURES BY MEAN |SHAP VALUE|")
    print("=" * 60)
    for rank, entry in enumerate(summary["top5_features"], start=1):
        print(f"  {rank}. {entry['feature']:<30} {entry['shap_importance']:.6f}")

    print("\nArtifacts written:")
    print(f"  Model   : {BEST_MODEL_PKL}")
    print(f"  Metadata: {MODEL_METADATA_JSON}")
    print(f"  Chart   : {FEATURE_IMPORTANCE_PNG}")
