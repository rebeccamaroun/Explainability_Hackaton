# Explainability Hackathon — Trusted AI × HR

**Themes:** Frugal AI + Explainable AI

## Context

A fictional company faces high employee turnover (33.4%) and wants an AI-powered solution to help HR understand why people leave and take preventive action. We build a prediction model that is both **lightweight (frugal)** and **transparent (explainable)**.

## Business value

Replacing an employee costs 50–200% of their annual salary. Our solution helps HR:
- **Detect** at-risk employees before they resign
- **Understand** why they are at risk (not just a score, but the reasons behind it)
- **Act** with targeted interventions (salary review, workload adjustment, etc.)
- **Deploy cheaply** — a lean model that runs on any laptop, no expensive infrastructure

## Use cases

| UC | Description |
|----|-------------|
| UC1 — Attrition prediction | Predict which employees are likely to leave based on structured HR data |
| UC2 — Explainable risk report | For each at-risk employee, show the top factors driving their risk score |
| UC3 — Frugal model selection | Compare full vs lightweight models to find the best performance-cost tradeoff |

## Personas

**Sarah — VP of Human Resources (the client)**
> "I need a solution to retain my employees. I want to know WHO is at risk and WHY, with clear evidence I can present to the board. I don't trust black-box AI."

**DataTrust AI — the solution provider (our team)**
> "We build transparent, lightweight AI solutions for HR. We explain every prediction and prove our models are resource-efficient."

## Team workstreams

| Workstream | Folder | 
|------------|--------|
| Data cleaning & augmentation | `data/` | 
| Model (training, XAI, frugality) | `model/` | 
| Frontend / demo UI | `frontend/` | 

## Repo structure
```
## Repo structure
```
Explainability_Hackaton/
├── data/
│   ├── raw/                  # Original dataset (do not modify)
│   ├── cleaned/              # Cleaned data + train/test splits
│   └── augmented/            # Enriched dataset
├── model/
│   ├── Modele Frugal.ipynb   # Main model — trains and compares all models
│   ├── explain.py            # SHAP explanation plots
│   └── README.md             # Model documentation
├── frontend/
│   └── graphic interface/    # Streamlit demo UI (4 tabs)
├── assets/                   # SHAP plots, risk scores
├── docs/                     # Data card, model card, architecture, summary
├── slides/                   # Pitch deck
├── requirements.txt
└── .gitignore
```

## Quick start
```bash
git clone https://github.com/rebeccamaroun/Explainability_Hackaton.git
cd Explainability_Hackaton
pip install -r requirements.txt
```

### Model
Open and run `model/Modele Frugal.ipynb` in Jupyter Notebook.

### SHAP explanations
```bash
py model\explain.py
```

### Frontend
```bash
cd frontend/graphic\ interface
streamlit run app.py
```

## Key results

| Model | Features | AUC-ROC | F1 |
|-------|----------|---------|-----|
| RF (73 features) | 73 | 0.769 | 0.222 |
| **RF Tuned Frugal (10 features)** | **10** | **0.830** | **0.653** |

**86% fewer features, 96% faster training and the frugal model actually performs better.**

## Deliverables

| # | Deliverable | Location | Status |
|---|-------------|----------|--------|
| 1 | README | `README.md` | Done |
| 2 | Data card | `docs/DATA_CARD.md` | Done |
| 3 | Model card | `docs/MODEL_CARD.md` | Done |
| 4 | Technical documentation | `docs/TECHNICAL_DOCUMENTATION.md` | Done |
| 5 | Architecture diagram | `docs/ARCHITECTURE.md` | Done |
| 6 | Executive summary | `docs/EXECUTIVE_SUMMARY.md` | Done |
| 7 | Demo | `docs/DEMO_SCRIPT.md` | Done |
| 8 | Slides / Pitch | `slides/` | Done |

## Key tools

| Purpose | Tool |
|---------|------|
| Explainability | SHAP |
| Carbon tracking | CodeCarbon |
| Frontend | Streamlit |