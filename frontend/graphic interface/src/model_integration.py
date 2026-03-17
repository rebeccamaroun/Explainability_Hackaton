from __future__ import annotations

from src.model_artifacts import build_model_metadata
from src.prediction_service import integrate_predictions


def integrate_model_outputs(df):
    result = integrate_predictions(df)
    components = result.components
    if all(status == "real" for status in components.values()):
        mode = "real"
        label = "Real model outputs integrated"
    elif any(status == "real" for status in components.values()):
        mode = "hybrid"
        label = "Real model outputs integrated with targeted fallbacks"
    else:
        mode = "demo"
        label = "Fallback heuristic outputs only"

    ai_context = {
        "mode": mode,
        "label": label,
        "available_files": result.artifacts_found,
        "metadata": build_model_metadata(),
        "components": components,
    }
    return result.df, ai_context
