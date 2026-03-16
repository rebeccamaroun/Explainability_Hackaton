# TalentGuard

TalentGuard is a Streamlit application for HR teams to explore employee retention risk, understand drivers of turnover, and prioritize preventive actions. It is designed for a hackathon context focused on frugal and explainable AI.

The application reads the cleaned HR dataset when available, then falls back to a small internal mock dataset if no CSV is found. The current project state is hybrid:

- real HR data loading
- trained-model risk scores and SHAP-based explanations when available
- heuristic HR guidance for layers not yet exported by the project

## Main features

- Executive-style HR dashboard with business KPIs
- Individual employee analysis with transparent demo risk logic
- Action plan page for prioritization and CSV export
- Responsible AI and transparency page aligned with the hackathon brief
- Automatic detection of model outputs already exported by the project

## Installation

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the application

From the `graphic interface` folder, run:

```bash
streamlit run app.py
```

## Data setup

The application automatically searches for HR data in these locations:

- `../Explainability_Hackaton/data/cleaned/HRDataset_cleaned_ALL.csv`
- `../Explainability_Hackaton/data/cleaned/HRDataset_cleaned.csv`
- `graphic interface/data/HRDataset_v14.csv`
- `../Explainability_Hackaton/HRDataset_v14.csv`
- `../HRDataset_v14.csv`

If the file is not found, the app still opens using a built-in mock dataset and shows a clear warning.

## Current AI integration state

When exported model files are available, TalentGuard uses them directly:

- `Explainability_Hackaton/assets/employee_risk_scores.csv`
- `Explainability_Hackaton/assets/shap_explanations.json`

This means the app can already display:

- trained-model risk scores
- SHAP-based explanation signals

If a component is still missing, the app falls back only for that layer. In practice, the current interface may run in a hybrid mode where recommendations and summaries remain heuristic while risk scoring and explainability come from exported model artifacts.

## Future AI pipeline integration

The app can still consume additional integration files placed in `graphic interface/data/`:

- `predictions.csv`
- `explanations.csv`
- `recommendations.csv`
- `text_insights.csv`
- `metadata.json`

The integration layer detects both local integration files and the current project exports from `Explainability_Hackaton/assets`. If a layer is missing, the app falls back gracefully without breaking the interface.

## Project structure

```text
graphic interface/
  app.py
  requirements.txt
  README.md
  .gitignore
  assets/
  data/
  src/
    __init__.py
    config.py
    data_loader.py
    schema_utils.py
    demo_ai.py
    real_ai_adapter.py
    ui_components.py
    pages/
      dashboard.py
      employee_analysis.py
      action_plan.py
      responsible_ai.py
```

## Notes on responsible use

- The tool is intended as decision support only.
- Some layers may remain heuristic when no exported artifact exists yet.
- Sensitive variables should be monitored for audit and fairness review, not used carelessly in individual decisions.
- The current demo prioritizes lightweight and interpretable logic over opaque models.
