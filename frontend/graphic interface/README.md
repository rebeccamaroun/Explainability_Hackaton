# TalentGuard

TalentGuard is a Streamlit application for HR teams to explore employee retention risk, understand drivers of turnover, and prioritize preventive actions. It is designed for a hackathon context focused on frugal and explainable AI.

The application reads the cleaned HR dataset when available, then falls back to a small internal mock dataset if no CSV is found. The current project state combines:

- real HR data loading
- real model-backed risk scores from exported notebook artifacts
- real SHAP-based explainability artifacts
- local Ollama-assisted narrative phrasing for HR-facing summaries and talking points
- narrow heuristic fallbacks only where no exported artifact exists yet

## Main features

- Executive-style HR dashboard with business KPIs
- Individual employee analysis with real scores and explainability evidence
- Action plan page for prioritization and CSV export
- Responsible AI and transparency page aligned with the hackathon brief
- Automatic detection of exported model artifacts and local LLM availability

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

## Notebook-derived model integration

The app does not run the notebook directly at runtime.

Instead, it consumes exported artifacts produced by the frugal model notebook:

- notebook source: `Explainability_Hackaton/model/Modele Frugal final.ipynb`
- risk scores: `Explainability_Hackaton/assets/employee_risk_scores.csv`
- local explanations: `Explainability_Hackaton/assets/shap_explanations.json`
- SHAP visuals: `Explainability_Hackaton/assets/shap_summary.png` and `Explainability_Hackaton/assets/shap_individual.png`

The current model metadata reflected in the app is:

- model family: Random Forest Frugal
- feature count: 10 selected features
- explainability source: exported SHAP impacts
- runtime mode: precomputed artifact integration

## Data setup

The application automatically searches for HR data in these locations:

- `../Explainability_Hackaton/data/cleaned/HRDataset_cleaned_ALL.csv`
- `../Explainability_Hackaton/data/cleaned/HRDataset_cleaned.csv`
- `graphic interface/data/HRDataset_v14.csv`
- `../Explainability_Hackaton/HRDataset_v14.csv`
- `../HRDataset_v14.csv`

If the file is not found, the app still opens using a built-in mock dataset and shows a clear warning.

## Current prediction and explainability state

When exported model files are available, TalentGuard uses them directly:

- `Explainability_Hackaton/assets/employee_risk_scores.csv`
- `Explainability_Hackaton/assets/shap_explanations.json`

This means the app can already display:

- trained-model risk scores
- SHAP-based explanation signals
- real employee ranking for prioritization
- real dashboard aggregates based on exported scores

If a component is still missing, the app falls back only for that layer. In practice, the current interface may run in a hybrid mode where recommendations or some narrative blocks remain heuristic while risk scoring and explainability come from exported model artifacts.

## Ollama integration

TalentGuard can use a local Ollama model for HR-friendly narrative assistance only.

Supported uses:

- rewriting evidence-based summaries in polished HR English
- generating concise talking points for managers or HR
- phrasing recommended actions from deterministic evidence

Not allowed:

- generating the risk score
- replacing the predictive model
- overriding deterministic model evidence
- making autonomous HR decisions

### Environment variables

You can configure Ollama with:

```bash
OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3:8b
OLLAMA_TIMEOUT_SECONDS=25
```

### Ollama behavior

- if Ollama is reachable, LLM-assisted summaries and talking points can be generated on demand
- if Ollama is unavailable, only those narrative sections are disabled
- the predictive and explainability layers continue to work from real exported artifacts
- LLM calls are not part of the critical rendering path for the main pages
- Employee Analysis and Action Plan render deterministic content first, then offer optional AI generation buttons
- generated LLM outputs are cached by employee and model/explanation version to speed up repeated use

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
    model_artifacts.py
    prediction_service.py
    explainability_service.py
    llm_service.py
    model_integration.py
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
- Predictive truth comes from the real model artifacts, not from the LLM.
- Local LLM assistance is limited to wording and summarization based on supplied evidence.
- Some layers may remain heuristic when no exported artifact exists yet.
- If Ollama is unreachable, only LLM-assisted sections are disabled and the app keeps running.
- LLM outputs are short, structured, timeout-bounded, and generated only on request.
- Sensitive variables should be monitored for audit and fairness review, not used carelessly in individual decisions.
- The system prioritizes lightweight and interpretable logic over opaque models.
