\# Model Card: HR Attrition Predictor



\## 1. Model objective



\- \*\*Use case:\*\* Binary classification — predict which employees will leave the company (attrition)

\- \*\*Input:\*\* Tabular data — 73 numeric features (salary, age, overtime, satisfaction, etc.) from the cleaned HR dataset

\- \*\*Output:\*\* Risk score (probability 0 to 1) + SHAP explanation per employee showing which factors drive the prediction





\## 2. Training data



\- \*\*Dataset:\*\* HRDataset\_v14 (Kaggle, Dr. Rich Huebner) + enriched version with augmented columns

\- \*\*Size:\*\* 311 employees, 73 features after cleaning

\- \*\*Target:\*\* `Termd` (1 = left, 0 = stayed)

\- \*\*Class balance:\*\* 207 stayed (66.6%) vs 104 left (33.4%)

\- \*\*Split:\*\* 80/20 train/test, stratified, random seed = 42

\- \*\*Known limitations:\*\*

&#x20; - Small dataset (311 rows) — limits model generalization

&#x20; - Synthetic data — patterns may not reflect real-world attrition

&#x20; - Some demographic groups are underrepresented (e.g., 3 American Indian employees, 4 Non-Citizens)





\## 3. Performance



| Metric | Logistic Regression (73 feat.) | Random Forest (73 feat.) | Random Forest Frugal (10 feat.) |

|--------|-------------------------------|--------------------------|--------------------------------|

| AUC-ROC | 0.684 | 0.769 | 0.692 |

| Accuracy | 0.63 | 0.67 | 0.68 |

| Precision (class 1) | 0.45 | 0.50 | 0.56 |

| Recall (class 1) | 0.43 | 0.14 | 0.24 |

| F1 (class 1) | 0.44 | 0.22 | 0.33 |



Best model by AUC: Random Forest (full). Best tradeoff: Random Forest Frugal (10 features).





\## 4. Limitations



\- \*\*Low recall:\*\* The model only catches 14–24% of employees who actually leave. Many at-risk employees go undetected.

\- \*\*Small dataset:\*\* 311 records is not enough for a production model. Performance would likely improve with 1000+ real records.

\- \*\*Synthetic data:\*\* Patterns in this dataset may not exist in a real company.

\- \*\*Bias risk:\*\* Protected attributes (sex, race, age, marital status) are present in the data. The model has not been fully audited for fairness across all subgroups.





\## 5. Risks \& mitigation



\- \*\*Risk of over-reliance:\*\* HR should not use this model as the sole basis for decisions about employees. It is a screening tool, not a verdict.

\- \*\*Controls:\*\*

&#x20; - SHAP explanations provided for every prediction so HR can verify the reasoning

&#x20; - Risk scores are probabilities (0–1), not binary yes/no — HR sets their own threshold

&#x20; - Human review required before any action is taken on a flagged employee





\## 6. Energy and frugality



| Metric | Full model (73 feat.) | Frugal model (10 feat.) |

|--------|-----------------------|------------------------|

| Features | 73 | 10 (86% reduction) |

| Training time | 3.94s | 0.14s (96% reduction) |

| CO2 (CodeCarbon) | 0.000001 kg | 0.000000 kg |



The frugal model achieves comparable performance with minimal compute cost, making it suitable for deployment on standard hardware with no GPU required.





\## 7. Security



\- \*\*Input validation:\*\* Model only accepts numeric tabular data in expected format. No free-text input, no prompt injection risk.

\- \*\*No secrets in repo:\*\* No API keys or credentials stored in code.

\- \*\*Data sensitivity:\*\* Raw dataset contains employee names and protected attributes. Anonymization recommended before any production use.





