from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.explainability_service import load_shap_explanations
from src.model_artifacts import build_model_metadata, locate_model_artifacts


@dataclass
class PredictionIntegrationResult:
    df: pd.DataFrame
    components: dict[str, str]
    artifacts_found: list[str]
    metadata: dict


def _risk_level(score: float | int | None) -> str:
    try:
        value = float(score)
    except (TypeError, ValueError):
        return "Low"
    if value >= 70:
        return "High"
    if value >= 45:
        return "Medium"
    return "Low"


def _scale_risk_scores(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.dropna().empty:
        return numeric
    if numeric.max() <= 1.0:
        numeric = numeric * 100
    return numeric.clip(0, 100)


def integrate_predictions(base_df: pd.DataFrame) -> PredictionIntegrationResult:
    enriched = base_df.copy()
    artifacts = locate_model_artifacts()
    metadata = build_model_metadata()
    artifacts_found: list[str] = []
    components = {
        "risk_scores": "demo",
        "explanations": "demo",
        "recommendations": "demo",
    }

    if artifacts.risk_scores_path and artifacts.risk_scores_path.exists():
        risk_df = pd.read_csv(artifacts.risk_scores_path)
        if "risk_score" in risk_df.columns:
            risk_scores = _scale_risk_scores(risk_df["risk_score"])
            limit = min(len(enriched), len(risk_scores))
            aligned_scores = pd.Series(index=enriched.index, dtype="float64")
            aligned_scores.iloc[:limit] = risk_scores.iloc[:limit].to_numpy()
            enriched["risk_score"] = aligned_scores.combine_first(pd.to_numeric(enriched["risk_score"], errors="coerce"))
            enriched["risk_level"] = enriched["risk_score"].apply(_risk_level)
            components["risk_scores"] = "real"
            artifacts_found.append(artifacts.risk_scores_path.name)

        if "prediction" in risk_df.columns:
            limit = min(len(enriched), len(risk_df))
            aligned_predictions = pd.Series(index=enriched.index, dtype="float64")
            aligned_predictions.iloc[:limit] = pd.to_numeric(risk_df["prediction"], errors="coerce").iloc[:limit].to_numpy()
            enriched["model_prediction"] = aligned_predictions

    if artifacts.shap_explanations_path and artifacts.shap_explanations_path.exists():
        explanation_map = load_shap_explanations(artifacts.shap_explanations_path)
        if explanation_map:
            enriched["explanation_details"] = [
                explanation_map.get(index, {}).get("details", current)
                for index, current in zip(enriched.index, enriched["explanation_details"])
            ]
            enriched["key_factors"] = [
                explanation_map.get(index, {}).get("key_factors", current)
                for index, current in zip(enriched.index, enriched["key_factors"])
            ]
            enriched["hr_summary"] = [
                explanation_map.get(index, {}).get("summary", current)
                for index, current in zip(enriched.index, enriched["hr_summary"])
            ]
            enriched["summary_is_simulated"] = [
                False if index in explanation_map else current
                for index, current in zip(enriched.index, enriched["summary_is_simulated"])
            ]
            components["explanations"] = "real"
            artifacts_found.append(artifacts.shap_explanations_path.name)

    return PredictionIntegrationResult(
        df=enriched,
        components=components,
        artifacts_found=artifacts_found,
        metadata=metadata,
    )
