from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.config import AI_OUTPUT_FILES, DATASET_CANDIDATES, EXPLAINABILITY_ROOTS


@dataclass(frozen=True)
class ModelArtifacts:
    notebook_path: Path | None
    risk_scores_path: Path | None
    shap_explanations_path: Path | None
    shap_summary_path: Path | None
    shap_individual_path: Path | None
    dataset_path: Path | None


def _first_existing(paths: list[Path]) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


def locate_model_artifacts() -> ModelArtifacts:
    notebook_candidates = [root / "model" / "Modele Frugal final.ipynb" for root in EXPLAINABILITY_ROOTS]
    risk_scores = AI_OUTPUT_FILES.get("project_risk_scores")
    shap_explanations = AI_OUTPUT_FILES.get("project_shap_explanations")
    shap_summary = AI_OUTPUT_FILES.get("project_shap_summary")
    shap_individual = AI_OUTPUT_FILES.get("project_shap_individual")
    return ModelArtifacts(
        notebook_path=_first_existing(notebook_candidates),
        risk_scores_path=risk_scores if risk_scores and risk_scores.exists() else None,
        shap_explanations_path=shap_explanations if shap_explanations and shap_explanations.exists() else None,
        shap_summary_path=shap_summary if shap_summary and shap_summary.exists() else None,
        shap_individual_path=shap_individual if shap_individual and shap_individual.exists() else None,
        dataset_path=_first_existing(DATASET_CANDIDATES),
    )


def build_model_metadata() -> dict:
    artifacts = locate_model_artifacts()
    feature_names = [
        "Salary",
        "Avg_Overtime_Hours",
        "Distance_From_Home_Km",
        "Age",
        "EngagementSurvey",
        "Absences",
        "RecruitmentSource_Google Search",
        "Remote_Work_Frequency",
        "EmpSatisfaction",
        "RecruitmentSource_LinkedIn",
    ]
    return {
        "model_name": "Random Forest Frugal",
        "model_family": "RandomForestClassifier",
        "feature_count": 10,
        "selected_features": feature_names,
        "auc_roc": 0.692,
        "model_version": f"risk_scores:{artifacts.risk_scores_path.stat().st_mtime_ns}" if artifacts.risk_scores_path else "missing",
        "explanation_version": f"shap:{artifacts.shap_explanations_path.stat().st_mtime_ns}" if artifacts.shap_explanations_path else "missing",
        "notebook_path": str(artifacts.notebook_path) if artifacts.notebook_path else None,
        "risk_scores_path": str(artifacts.risk_scores_path) if artifacts.risk_scores_path else None,
        "explanations_path": str(artifacts.shap_explanations_path) if artifacts.shap_explanations_path else None,
        "runtime_mode": "precomputed-artifacts",
    }
