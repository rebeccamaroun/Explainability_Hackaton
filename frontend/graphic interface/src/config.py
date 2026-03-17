import os
from pathlib import Path

APP_NAME = "TalentGuard"
APP_TAGLINE = "Explainable employee retention monitoring for HR teams"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"


def _unique_paths(paths: list[Path]) -> list[Path]:
    unique: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = str(path)
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique


POTENTIAL_ROOTS = _unique_paths(
    [
        BASE_DIR,
        BASE_DIR.parent,
        BASE_DIR.parent.parent,
        BASE_DIR.parent.parent.parent,
        BASE_DIR.parent.parent.parent.parent,
    ]
)

EXPLAINABILITY_ROOTS = _unique_paths(
    [root for root in POTENTIAL_ROOTS if root.name == "Explainability_Hackaton"]
    + [root / "Explainability_Hackaton" for root in POTENTIAL_ROOTS]
)

DATASET_CANDIDATES = _unique_paths(
    [
        root / "data" / "cleaned" / "HRDataset_cleaned_ALL.csv" for root in EXPLAINABILITY_ROOTS
    ]
    + [
        root / "data" / "cleaned" / "HRDataset_cleaned.csv" for root in EXPLAINABILITY_ROOTS
    ]
    + [
        DATA_DIR / "HRDataset_v14.csv",
    ]
    + [
        root / "HRDataset_v14.csv" for root in EXPLAINABILITY_ROOTS
    ]
    + [
        root / "data" / "raw" / "HRDataset_v14.csv" for root in EXPLAINABILITY_ROOTS
    ]
)

AI_OUTPUT_FILES = {
    "predictions": DATA_DIR / "predictions.csv",
    "explanations": DATA_DIR / "explanations.csv",
    "recommendations": DATA_DIR / "recommendations.csv",
    "text_insights": DATA_DIR / "text_insights.csv",
    "metadata": DATA_DIR / "metadata.json",
}

PROJECT_ROOT = EXPLAINABILITY_ROOTS[0] if EXPLAINABILITY_ROOTS else BASE_DIR.parent
AI_OUTPUT_FILES["project_risk_scores"] = PROJECT_ROOT / "assets" / "employee_risk_scores.csv"
AI_OUTPUT_FILES["project_shap_explanations"] = PROJECT_ROOT / "assets" / "shap_explanations.json"
AI_OUTPUT_FILES["project_shap_summary"] = PROJECT_ROOT / "assets" / "shap_summary.png"
AI_OUTPUT_FILES["project_shap_individual"] = PROJECT_ROOT / "assets" / "shap_individual.png"


RISK_LEVEL_ORDER = ["Low", "Medium", "High"]
STATUS_OPTIONS = ["To launch", "In progress", "Under review"]

SENSITIVE_COLUMNS = [
    "Sex",
    "RaceDesc",
    "HispanicLatino",
    "CitizenDesc",
    "MaritalDesc",
    "GenderID",
]

OLLAMA_ENABLED = os.getenv("OLLAMA_ENABLED", "true").strip().lower() in {"1", "true", "yes", "on"}
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")
OLLAMA_TIMEOUT_SECONDS = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "25"))
