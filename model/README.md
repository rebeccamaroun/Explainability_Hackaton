# Model

## Overview

Predicts employee attrition (`Termd` = 1 means left, 0 means stayed).
Built around two hackathon themes: **Frugal AI** and **Explainable AI**.

## Files

| File | What it does | Run command |
|------|-------------|-------------|
| `train.py` | Trains models, exports risk scores and SHAP values | `py model\train.py` |
| `explain.py` | Generates SHAP plots (summary + individual) | `py model\explain.py` |
| `frugal.py` | Compares full vs frugal model (features, time, CO2) | `py model\frugal.py` |

## Results

| Model | Features | AUC-ROC |
|-------|----------|---------|
| Logistic Regression | 73 | 0.684 |
| Random Forest (full) | 73 | 0.769 |
| Random Forest (frugal) | 10 | 0.692 |

Frugal takeaway: 86% fewer features, only 10% performance drop, 96% faster training.

## Top 10 features

1. Salary
2. Avg_Overtime_Hours
3. Distance_From_Home_Km
4. Age
5. EngagementSurvey
6. Absences
7. RecruitmentSource_Google Search
8. Remote_Work_Frequency
9. EmpSatisfaction
10. RecruitmentSource_LinkedIn

## Data leakage removed

These columns were dropped because they contain info only known after an employee leaves:
- `EmploymentStatus_*`
- `EmpStatusID`
- `Tenure_Years`
- `Years_Since_Last_Review`
- `State` (not encoded, low value)

## Outputs for frontend

`train.py` generates two files in `assets/`:

- `employee_risk_scores.csv` — every employee with a risk score (0 to 1) and prediction (0 or 1)
- `shap_explanations.json` — per-employee SHAP values explaining why they were flagged

Example from the JSON:
```json
{
  "index": 0,
  "risk_score": 0.35,
  "features": {
    "Salary": {"value": 62506, "shap_impact": -0.02},
    "Avg_Overtime_Hours": {"value": 6.7, "shap_impact": 0.01}
  }
}
```

## How to run
```bash
pip install scikit-learn shap codecarbon matplotlib
py model\train.py
py model\explain.py
py model\frugal.py
```

## Input

Expects `data\cleaned\HRDataset_cleaned.csv` (from the data team's cleaning pipeline).