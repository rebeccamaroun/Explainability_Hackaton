# Model Card: HR Attrition Predictor

## 1. Model objective

- **Use case:** Binary classification — predict which employees will leave the company
- **Input:** Tabular data — 10 selected features from the cleaned HR dataset (73 available, 10 used)
- **Output:** Risk score (probability 0 to 1) + SHAP explanation per employee showing which factors drive the prediction

## 2. Training data

- **Dataset:** HRDataset_v14 (Kaggle, Dr. Rich Huebner) + enriched version with augmented columns
- **Size:** 311 employees, 73 features after cleaning
- **Target:** `Termd` (1 = left, 0 = stayed)
- **Class balance:** 207 stayed (66.6%) vs 104 left (33.4%)
- **Split:** 80/20 train/test, stratified, random seed = 42
- **Known limitations:**
  - Small dataset (311 rows) — limits model generalization
  - Synthetic data — patterns may not reflect real-world attrition
  - Some demographic groups are underrepresented (e.g., 3 American Indian employees, 4 Non-Citizens)

## 3. Performance

| Model | Features | AUC | Acc | F1 | Prec |
|-------|----------|-----|-----|-----|------|
| RF (73 feat) | 73 | 0.769 | 0.667 | 0.222 | 0.500 |
| LR (set 2) | 10 | 0.782 | 0.730 | 0.485 | 0.667 |
| RF (set 2) | 10 | 0.795 | 0.746 | 0.600 | 0.632 |
| XGB (set 2) | 10 | 0.799 | 0.714 | 0.438 | 0.636 |
| LR Balanced (set 2) | 10 | 0.787 | 0.714 | 0.625 | 0.556 |
| **RF Tuned (set 2)** | **10** | **0.830** | **0.730** | **0.653** | **0.571** |

Best model: **Random Forest Tuned (set 2)** — AUC 0.830, F1 0.653, using only 10 features.

## 4. Limitations

- **Moderate recall:** The best model catches more at-risk employees than earlier versions (F1 improved from 0.22 to 0.65), but some will still go undetected.
- **Small dataset:** 311 records is not enough for a production model. Performance would likely improve with 1000+ real records.
- **Synthetic data:** Patterns in this dataset may not exist in a real company.
- **Bias risk:** Protected attributes (sex, race, age, marital status) are present in the data. The model has not been fully audited for fairness across all subgroups.

## 5. Risks & mitigation

- **Risk of over-reliance:** HR should not use this model as the sole basis for decisions about employees. It is a screening tool, not a verdict.
- **Controls:**
  - SHAP explanations provided for every prediction so HR can verify the reasoning
  - Risk scores are probabilities (0–1), not binary yes/no — HR sets their own threshold
  - Human review required before any action is taken on a flagged employee

## 6. Energy and frugality

| Metric | Full model (73 feat) | Frugal model (10 feat) |
|--------|---------------------|----------------------|
| AUC-ROC | 0.769 | 0.830 |
| Features | 73 | 10 (86% reduction) |
| Training time | ~3.9s | ~0.14s (96% reduction) |
| CO2 (CodeCarbon) | ~0.000001 kg | ~0.000000 kg |

The frugal model does not just match the full model — it outperforms it. Less data, better results, deployable on any laptop with no GPU.

## 7. Security

- **Input validation:** Model only accepts numeric tabular data in expected format. No free-text input, no prompt injection risk.
- **No secrets in repo:** No API keys or credentials stored in code.
- **Data sensitivity:** Raw dataset contains employee names and protected attributes. Anonymization recommended before any production use.