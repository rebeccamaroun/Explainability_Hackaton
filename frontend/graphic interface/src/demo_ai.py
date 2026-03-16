from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from src.schema_utils import coerce_numeric, derive_tenure_years, get_column, normalize_text_value


PERFORMANCE_SCORE_MAP = {
    "PIP": 1.0,
    "Needs Improvement": 1.5,
    "Below Expectations": 1.5,
    "Fully Meets": 3.0,
    "Exceeds": 4.2,
    "Exceptional": 4.5,
}

ACTION_LIBRARY = {
    "low satisfaction level": "Schedule a listening session with HR and the manager.",
    "above-average absenteeism": "Review workload, wellbeing signals, and attendance constraints.",
    "frequent lateness in the last 30 days": "Clarify work conditions and short-term operational blockers.",
    "low engagement": "Launch a manager check-in and re-engagement plan.",
    "short tenure": "Strengthen onboarding support and assign a mentor.",
    "perceived stagnation": "Open a career growth or internal mobility discussion.",
    "weak performance signal": "Provide targeted coaching with clear short-term goals.",
    "strong engagement": "Maintain current support and recognize positive involvement.",
}


def _safe_standard_score(series: pd.Series) -> pd.Series:
    numeric = coerce_numeric(series)
    if numeric.notna().sum() < 2:
        return pd.Series([0.0] * len(series), index=series.index)
    std = numeric.std()
    if not std or np.isnan(std):
        return pd.Series([0.0] * len(series), index=series.index)
    return (numeric - numeric.mean()) / std


def _performance_numeric(performance_series: pd.Series) -> pd.Series:
    raw_numeric = coerce_numeric(performance_series)
    mapped = performance_series.map(PERFORMANCE_SCORE_MAP)
    return raw_numeric.fillna(mapped)


def _score_row(row: pd.Series) -> tuple[float, list[dict[str, Any]]]:
    score = 25.0
    factors: list[dict[str, Any]] = []

    def add_factor(label: str, contribution: float) -> None:
        nonlocal score
        score += contribution
        factors.append({"factor": label, "contribution": contribution})

    if row.get("_satisfaction", np.nan) <= 2:
        add_factor("low satisfaction level", 18)
    elif row.get("_satisfaction", np.nan) == 3:
        add_factor("moderate satisfaction signal", 6)

    if row.get("_engagement", np.nan) < 3:
        add_factor("low engagement", 14)
    elif row.get("_engagement", np.nan) >= 4.2:
        add_factor("strong engagement", -9)

    if row.get("_absences_z", 0) > 0.8 or row.get("_absences", 0) >= 10:
        add_factor("above-average absenteeism", 12)

    if row.get("_lateness", 0) >= 3:
        add_factor("frequent lateness in the last 30 days", 10)

    if row.get("_performance", np.nan) <= 2:
        add_factor("weak performance signal", 10)
    elif row.get("_performance", np.nan) >= 4:
        add_factor("positive performance signal", -5)

    if row.get("_tenure", np.nan) < 1.2:
        add_factor("short tenure", 8)
    elif row.get("_tenure", np.nan) > 6 and row.get("_projects", 0) == 0:
        add_factor("perceived stagnation", 8)

    if row.get("_projects", 0) >= 2 and row.get("_engagement", np.nan) >= 4:
        add_factor("cross-functional contribution", -4)

    score = float(np.clip(score, 5, 95))
    factors = sorted(factors, key=lambda item: abs(item["contribution"]), reverse=True)
    return score, factors[:5]


def _build_hr_summary(name: str, level: str, factors: list[dict[str, Any]]) -> str:
    if not factors:
        return (
            f"{name} currently shows a {level.lower()} estimated retention risk in demo mode. "
            "No strong warning signal was detected from the available structured fields."
        )

    key_points = ", ".join(factor["factor"] for factor in factors[:3])
    return (
        f"{name} is currently flagged with a {level.lower()} estimated retention risk. "
        f"This demo assessment is mainly driven by {key_points}. "
        "It should be reviewed by HR and management before any action is taken."
    )


def _risk_level(score: float) -> str:
    if score >= 70:
        return "High"
    if score >= 45:
        return "Medium"
    return "Low"


def build_demo_ai_outputs(df: pd.DataFrame, schema: dict[str, str | None]) -> pd.DataFrame:
    """
    Build transparent demo outputs from simple heuristics.

    This is deliberately not a predictive model. The logic uses lightweight
    business rules so the demo remains explainable and easy to replace later.
    """
    enriched = df.copy()
    enriched["_tenure"] = derive_tenure_years(enriched, schema)
    enriched["_engagement"] = coerce_numeric(get_column(enriched, schema, "engagement"))
    enriched["_satisfaction"] = coerce_numeric(get_column(enriched, schema, "satisfaction"))
    enriched["_projects"] = coerce_numeric(get_column(enriched, schema, "projects")).fillna(0)
    enriched["_absences"] = coerce_numeric(get_column(enriched, schema, "absences")).fillna(0)
    enriched["_lateness"] = coerce_numeric(get_column(enriched, schema, "lateness")).fillna(0)
    enriched["_performance"] = _performance_numeric(get_column(enriched, schema, "performance_score"))
    enriched["_absences_z"] = _safe_standard_score(enriched["_absences"])

    scored = enriched.apply(_score_row, axis=1, result_type="expand")
    enriched["risk_score"] = scored[0]
    enriched["explanation_details"] = scored[1]
    enriched["risk_level"] = enriched["risk_score"].apply(_risk_level)
    enriched["key_factors"] = enriched["explanation_details"].apply(
        lambda items: ", ".join(item["factor"] for item in items[:3]) if items else "No material signal detected"
    )
    enriched["recommended_actions"] = enriched["explanation_details"].apply(
        lambda items: [ACTION_LIBRARY.get(item["factor"], "Review the case with HR.") for item in items[:4]]
        or ["Maintain regular check-ins and monitor the situation."]
    )
    enriched["priority_action"] = enriched["recommended_actions"].apply(lambda items: items[0])

    name_series = get_column(enriched, schema, "employee_name").fillna("This employee")
    enriched["hr_summary"] = [
        _build_hr_summary(normalize_text_value(name), level, factors)
        for name, level, factors in zip(name_series, enriched["risk_level"], enriched["explanation_details"])
    ]
    enriched["summary_is_simulated"] = True
    enriched["priority_status"] = "To launch"
    return enriched
