# Model

## Overview

Predicts employee attrition (`Termd` = 1 means left, 0 means stayed).
Built around two hackathon themes: **Frugal AI** and **Explainable AI**.

## Files

| File | What it does |
|------|-------------|
| `Modele Frugal.ipynb` | Main notebook — trains 10 models, compares performance, selects best frugal model |
| `explain.py` | Generates SHAP plots (global summary + individual employee breakdown) |

## Best model

**Random Forest Tuned (set 2)** — AUC 0.830, F1 0.653, using only 10 features.

## Top 10 features (set 2)

1. RecruitmentSource_Google Search
2. Department_Production
3. FromDiversityJobFairID
4. RecruitmentSource_Diversity Job Fair
5. SpecialProjectsCount
6. Remote_Work_Frequency
7. DaysLateLast30
8. MaritalDesc_Single
9. Department_IT/IS
10. RecruitmentSource_Indeed

## How to run

Open `Modele Frugal.ipynb` in Jupyter Notebook and run all cells.

For SHAP plots:
```bash
py model\explain.py
```