from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


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


def load_shap_explanations(path: Path) -> dict[int, dict]:
    explanations = json.loads(path.read_text(encoding="utf-8"))
    explanation_map: dict[int, dict] = {}
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
        if not ranked_features:
            continue

        explanation_map[int(row_index)] = {
            "details": [{"factor": row["factor"], "contribution": row["contribution"]} for row in ranked_features],
            "key_factors": ", ".join(row["factor"] for row in ranked_features[:3]),
            "summary": f"Top explainability signals from the trained model include {', '.join(row['factor'] for row in ranked_features[:3])}.",
        }

    return explanation_map
