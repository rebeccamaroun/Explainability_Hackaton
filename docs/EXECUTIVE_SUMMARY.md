 # Executive Summary

## The problem

One in three employees is leaving. With a 33.4% turnover rate, this company loses an estimated $1.2–2.4M per year in replacement costs. HR knows people are leaving but doesn't know who's next or why.

## What we built

An AI tool that predicts which employees are at risk of leaving and explains exactly why. Built on two principles:

- **Explainable AI** : every prediction comes with clear, human-readable reasons powered by SHAP. Not a black box.
- **Frugal AI** : we use only 10 features instead of 73, achieving better results with 96% less compute time and near-zero carbon emissions.

## How it works

1. We clean and prepare the HR dataset (311 employees, enriched with overtime, distance, and remote work data)
2. We train a lightweight Random Forest model on 10 carefully selected features
3. Each employee gets a risk score (0 to 1) with a SHAP breakdown showing which factors drive their score
4. A Streamlit dashboard lets HR managers explore risks, drill into individual employees, and generate action plans

## Key results

- **Best model:** Random Forest Tuned — AUC 0.830, F1 0.653, using only 10 features
- **86% fewer features** than the full model, **96% faster** training, **near-zero CO2**
- **Frugal model outperforms the full model** — AUC 0.830 vs 0.769 with 73 features
- **Real example:** Employee#302 was correctly flagged as high risk (0.75) due to recruitment channel, department, lack of remote work, and no special projects. They left for another position.

## Business value

- **Detect** at-risk employees before they resign
- **Understand** the specific reasons behind each risk score
- **Act** with targeted interventions (remote work policy, project assignments, recruitment channel review)
- **Deploy cheaply** because runs on any laptop, no cloud or GPU needed

## What's next

With real company data (instead of this synthetic dataset), the model would be retrained and validated. The same pipeline, tools, and dashboard apply only the data changes.




