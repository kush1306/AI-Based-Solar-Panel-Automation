"""AI service placeholder — real model integration will be added by the AI team."""

from typing import Any


def predict_optimal_tilt(**kwargs: Any) -> dict[str, Any]:
    """
    Placeholder for optimal tilt prediction.
    Future: call trained XGBoost / solar position model.
    """
    raise NotImplementedError(
        "AI tilt prediction is not implemented. "
        "This will be integrated by the AI engineering team."
    )


def predict_energy_load(**kwargs: Any) -> dict[str, Any]:
    """
    Placeholder for energy load prediction.
    Future: call trained LSTM / consumption model.
    """
    raise NotImplementedError(
        "AI energy load prediction is not implemented. "
        "This will be integrated by the AI engineering team."
    )
