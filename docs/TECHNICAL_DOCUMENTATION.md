# Technical Documentation

## 1. Overview

This document describes the full technical pipeline for our HR attrition prediction tool, built for the Trusted AI × HR hackathon. Our two themes are **Frugal AI** and **Explainable AI**.

The goal: predict which employees are likely to leave and explain why, using a lightweight model that any company can deploy.

## 2. Data pipeline

### 2.1 Source data
- **Dataset:** HRDataset_v14 from Kaggle (Dr. Rich Huebner)
- **Size:** 311 employees, 36 columns
- **Enrichment:** Dataset was augmented with additional columns (overtime hours, distance from home, remote work frequency, internal transfer requests)

### 2.2 Cleaning steps
| Step | Action |
|------|--------|
| Column removal | Dropped identifiers (names, IDs, manager names) and redundant columns |
| Date processing | Converted DOB, hire/termination dates to datetime; calculated Age and Tenure |
| Binary encoding | Sex (M/F → 1/0), HispanicLatino (Yes/No → 1/0), Internal Transfer (Yes/No → 1/0) |
| One-Hot encoding | MaritalDesc, CitizenDesc, RaceDesc, Department, Position, RecruitmentSource, PerformanceScore |
| Missing values | Filled remaining nulls with median |

### 2.3 Data leakage removal
These columns were removed because they contain information only available after an employee leaves:
- `EmploymentStatus_*` — directly encodes the outcome
- `EmpStatusID` — numeric version of employment status
- `Tenure_Years` — calculated using termination date
- `Years_Since_Last_Review` — same issue
- `State` — not encoded, low predictive value

### 2.4 Final dataset
- **Shape after cleaning:** 311 rows, 73 features + 1 target (`Termd`)
- **Train/test split:** 80/20, stratified, seed = 42

## 3. Model

### 3.1 Feature sets tested
Two different sets of 10 features were compared:

**Set 1** (automatic — based on Random Forest feature importance):
Salary, Avg_Overtime_Hours, Distance_From_Home_Km, Age, EngagementSurvey, Absences, RecruitmentSource_Google Search, Remote_Work_Frequency, EmpSatisfaction, RecruitmentSource_LinkedIn

**Set 2** (domain-informed — selected based on HR knowledge):
RecruitmentSource_Google Search, Department_Production, FromDiversityJobFairID, RecruitmentSource_Diversity Job Fair, SpecialProjectsCount, Remote_Work_Frequency, DaysLateLast30, MaritalDesc_Single, Department_IT/IS, RecruitmentSource_Indeed

### 3.2 Results
| Model | Features | AUC | Acc | F1 | Prec |
|-------|----------|-----|-----|-----|------|
| RF (73 feat) | 73 | 0.769 | 0.667 | 0.222 | 0.500 |
| RF (10 feat, set 1) | 10 | 0.692 | 0.683 | 0.333 | 0.556 |
| RF (10 feat, set 2) | 10 | 0.795 | 0.746 | 0.600 | 0.632 |
| XGB (set 2) | 10 | 0.799 | 0.714 | 0.438 | 0.636 |
| **RF Tuned (set 2)** | **10** | **0.830** | **0.730** | **0.653** | **0.571** |

### 3.3 Best model
**Random Forest Tuned (set 2)** — AUC 0.830, F1 0.653, using only 10 features.

Settings: n_estimators=200, max_depth=8, min_samples_leaf=5, class_weight=balanced_subsample, seed=42

### 3.4 Key insight
The domain-informed feature set (set 2) outperformed the automatic feature importance set (set 1). Understanding the business context matters more than letting the algorithm pick features blindly.

## 4. Explainability (SHAP)

We use SHAP (SHapley Additive exPlanations) to make every prediction transparent.

### What SHAP does
For each employee, SHAP shows how much each feature pushed their risk score up or down. It turns a number into a reason.

### Two levels of explanation:
- **Global:** Which features matter most across all employees (summary plot)
- **Individual:** For one specific employee, what caused their score (force plot)

### Real example — Employee #302 (risk score: 0.75)
- Recruited via Google Search (highest churn channel)
- Works in Production (40% department turnover)
- No remote work (company average: 1.1 days/week)
- Zero special projects (company average: 1.2)
- Outcome: left for another position

### Why it matters
HR managers will not act on a score they don't understand. SHAP turns "risk = 0.75" into "this employee is at risk because of these specific reasons." That builds trust and enables action.

## 5. Frugal AI

### Approach
Instead of using all 73 features, we tested two curated sets of 10 features each. The best model uses only 10 features and actually outperforms the full model.

### Results
| Metric | Full model (73 feat) | Frugal model (10 feat) |
|--------|---------------------|----------------------|
| AUC-ROC | 0.769 | 0.830 |
| Features | 73 | 10 (86% reduction) |
| Training time | ~3.9s | ~0.14s (96% reduction) |
| CO2 emissions | ~0.000001 kg | ~0.000000 kg |

### Tools
- **CodeCarbon** — measures carbon emissions during model training
- **Feature importance** + domain expertise for feature selection

### Philosophy
Less data, better results. The frugal model is not a compromise — it is an improvement. Smarter feature selection beats brute-force computation.

## 6. Frontend

Built with **Streamlit** — a Python-based web framework for data apps.

### Four tabs:
1. **Global Dashboard** — overview of all employees, risk distribution, department breakdown
2. **Employee Deep Dive** — select any employee, see risk score and SHAP breakdown
3. **Action Plan** — prioritized list of at-risk employees with suggested interventions
4. **AI Manager** — model transparency, how it works, what data it uses

### How to run:
```bash
cd frontend/graphic\ interface
streamlit run app.py
```

## 7. Tech stack

| Component | Tool |
|-----------|------|
| Language | Python 3.x |
| Data processing | pandas, numpy |
| Modeling | scikit-learn, xgboost |
| Explainability | SHAP |
| Carbon tracking | CodeCarbon |
| Visualization | matplotlib |
| Frontend | Streamlit |

## 8. How to reproduce
```bash
git clone https://github.com/rebeccamaroun/Explainability_Hackaton.git
cd Explainability_Hackaton
pip install -r requirements.txt
```

### Model
Open and run `model/Modele Frugal.ipynb` in Jupyter Notebook — this trains all models and shows the comparison table.

### SHAP explanations
```bash
py model/explain.py
```

### Frontend
```bash
cd frontend/graphic\ interface
streamlit run app.py
```

All random seeds fixed to 42 for reproducibility.