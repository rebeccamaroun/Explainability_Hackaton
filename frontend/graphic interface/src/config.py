from pathlib import Path

APP_NAME = "TalentGuard"
APP_TAGLINE = "Explainable employee retention monitoring for HR teams"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

DATASET_CANDIDATES = [
    BASE_DIR.parent / "Explainability_Hackaton" / "data" / "cleaned" / "HRDataset_cleaned.csv",
    BASE_DIR.parent / "Explainability_Hackaton" / "data" / "cleaned" / "HRDataset_cleaned_ALL.csv",
    DATA_DIR / "HRDataset_v14.csv",
    BASE_DIR.parent / "Explainability_Hackaton" / "HRDataset_v14.csv",
    BASE_DIR.parent / "HRDataset_v14.csv",
]

AI_OUTPUT_FILES = {
    "predictions": DATA_DIR / "predictions.csv",
    "explanations": DATA_DIR / "explanations.csv",
    "recommendations": DATA_DIR / "recommendations.csv",
    "text_insights": DATA_DIR / "text_insights.csv",
    "metadata": DATA_DIR / "metadata.json",
}

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
