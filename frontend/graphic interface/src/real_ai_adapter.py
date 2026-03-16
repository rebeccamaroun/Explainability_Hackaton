from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.config import AI_OUTPUT_FILES


def _detect_join_key(df: pd.DataFrame, incoming: pd.DataFrame) -> str | None:
    for candidate in ["EmpID", "Employee_Name", "EmployeeName", "employee_id", "employee_name"]:
        if candidate in df.columns and candidate in incoming.columns:
            return candidate
    return None


def _load_csv_if_exists(path: Path) -> pd.DataFrame | None:
    if path.exists():
        return pd.read_csv(path)
    return None


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


def _overlay_known_outputs(df: pd.DataFrame) -> pd.DataFrame:
    for base_column in [
        "risk_score",
        "risk_level",
        "key_factors",
        "priority_action",
        "hr_summary",
        "priority_status",
        "recommended_actions",
        "explanation_details",
        "summary_is_simulated",
    ]:
        ai_column = f"{base_column}_ai"
        if ai_column in df.columns:
            df[base_column] = df[ai_column].combine_first(df[base_column]) if base_column in df.columns else df[ai_column]
            df = df.drop(columns=[ai_column])
    return df


def _scale_risk_scores(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.dropna().empty:
        return numeric
    if numeric.max() <= 1.0:
        numeric = numeric * 100
    return numeric.clip(0, 100)


def _humanize_feature_name(feature_name: str, feature_value) -> str:
    categorical_prefixes = [
        "Department_",
        "Position_",
        "RecruitmentSource_",
        "RaceDesc_",
        "MaritalDesc_",
        "CitizenDesc_",
        "PerformanceScore_",
    ]
    for prefix in categorical_prefixes:
        if feature_name.startswith(prefix):
            label = prefix.replace("_", "").replace("Desc", " description").strip()
            value_label = feature_name.replace(prefix, "").strip()
            return f"{label}: {value_label}"
    return feature_name.replace("_", " ").strip()


def _is_informative_feature(feature_name: str, feature_value) -> bool:
    one_hot_prefixes = (
        "Department_",
        "Position_",
        "RecruitmentSource_",
        "RaceDesc_",
        "MaritalDesc_",
        "CitizenDesc_",
        "PerformanceScore_",
    )
    if feature_name.startswith(one_hot_prefixes) and str(feature_value).strip() in {"0", "0.0", "False", "false"}:
        return False
    return True


def _load_project_risk_scores(enriched: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    path = AI_OUTPUT_FILES["project_risk_scores"]
    if not path.exists():
        return enriched, False

    risk_df = pd.read_csv(path)
    if "risk_score" not in risk_df.columns:
        return enriched, False

    risk_scores = _scale_risk_scores(risk_df["risk_score"])
    limit = min(len(enriched), len(risk_scores))
    aligned_scores = pd.Series(index=enriched.index, dtype="float64")
    aligned_scores.iloc[:limit] = risk_scores.iloc[:limit].to_numpy()

    enriched["risk_score"] = aligned_scores.combine_first(pd.to_numeric(enriched["risk_score"], errors="coerce"))
    enriched["risk_level"] = enriched["risk_score"].apply(_risk_level)

    if "prediction" in risk_df.columns:
        aligned_predictions = pd.Series(index=enriched.index, dtype="float64")
        aligned_predictions.iloc[:limit] = pd.to_numeric(risk_df["prediction"], errors="coerce").iloc[:limit].to_numpy()
        enriched["model_prediction"] = aligned_predictions

    return enriched, True


def _load_project_shap_explanations(enriched: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    path = AI_OUTPUT_FILES["project_shap_explanations"]
    if not path.exists():
        return enriched, False

    explanations = json.loads(path.read_text(encoding="utf-8"))
    explanation_map: dict[int, list[dict]] = {}
    summary_map: dict[int, str] = {}

    for item in explanations:
        row_index = item.get("index")
        features = item.get("features", {})
        ranked_features = []
        for feature_name, feature_data in features.items():
            feature_value = feature_data.get("value")
            if not _is_informative_feature(feature_name, feature_value):
                continue
            impact = float(feature_data.get("shap_impact", 0))
            ranked_features.append(
                {
                    "factor": _humanize_feature_name(feature_name, feature_value),
                    "contribution": impact * 100,
                    "raw_impact": impact,
                    "value": feature_value,
                }
            )

        ranked_features = sorted(ranked_features, key=lambda row: abs(row["raw_impact"]), reverse=True)[:5]
        explanation_map[row_index] = [{"factor": row["factor"], "contribution": row["contribution"]} for row in ranked_features]
        if ranked_features:
            lead_factors = ", ".join(row["factor"] for row in ranked_features[:3])
            summary_map[row_index] = f"Top explainability signals from the trained model include {lead_factors}."

    if not explanation_map:
        return enriched, False

    enriched["explanation_details"] = [explanation_map.get(index, row) for index, row in zip(enriched.index, enriched["explanation_details"])]
    enriched["key_factors"] = [
        ", ".join(item["factor"] for item in explanation_map[index][:3]) if index in explanation_map else value
        for index, value in zip(enriched.index, enriched["key_factors"])
    ]
    enriched["model_explanation_summary"] = [summary_map.get(index, pd.NA) for index in enriched.index]
    return enriched, True


def enrich_with_ai_outputs(df: pd.DataFrame, schema: dict[str, str | None]) -> tuple[pd.DataFrame, dict]:
    enriched = df.copy()

    available_files = {name: path for name, path in AI_OUTPUT_FILES.items() if path.exists()}
    metadata = {}
    if AI_OUTPUT_FILES["metadata"].exists():
        metadata = json.loads(AI_OUTPUT_FILES["metadata"].read_text(encoding="utf-8"))

    # Generic adapter for optional local integration files.
    predictions = _load_csv_if_exists(AI_OUTPUT_FILES["predictions"])
    explanations = _load_csv_if_exists(AI_OUTPUT_FILES["explanations"])
    recommendations = _load_csv_if_exists(AI_OUTPUT_FILES["recommendations"])

    for incoming in [predictions, explanations, recommendations]:
        if incoming is None:
            continue
        join_key = _detect_join_key(enriched, incoming)
        if not join_key:
            continue
        enriched = enriched.merge(incoming, how="left", on=join_key, suffixes=("", "_ai"))
        enriched = _overlay_known_outputs(enriched)

    risk_real = False
    explanations_real = False
    recommendations_real = recommendations is not None

    enriched, risk_real = _load_project_risk_scores(enriched)
    enriched, explanations_real = _load_project_shap_explanations(enriched)

    if "priority_status" not in enriched.columns:
        enriched["priority_status"] = "Under review"

    if "model_explanation_summary" in enriched.columns:
        enriched["hr_summary"] = enriched["model_explanation_summary"].fillna(enriched["hr_summary"])
        enriched["summary_is_simulated"] = enriched["model_explanation_summary"].isna()

    if risk_real or explanations_real or recommendations_real:
        components = {
            "risk_scores": "real" if risk_real else "demo",
            "explanations": "real" if explanations_real else "demo",
            "recommendations": "real" if recommendations_real else "demo",
        }
        if all(status == "real" for status in components.values()):
            mode = "real"
            label = "Integrated AI outputs detected"
        else:
            mode = "hybrid"
            label = "Model outputs integrated - some guidance remains heuristic"
        return (
            enriched,
            {
                "mode": mode,
                "label": label,
                "available_files": sorted(available_files.keys()),
                "metadata": metadata,
                "components": components,
            },
        )

    return (
        enriched,
        {
            "mode": "demo",
            "label": "Demo Version - heuristic outputs only",
            "available_files": sorted(available_files.keys()),
            "metadata": metadata,
            "components": {
                "risk_scores": "demo",
                "explanations": "demo",
                "recommendations": "demo",
            },
        },
    )
