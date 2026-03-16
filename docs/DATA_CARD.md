\# Data Card — HRDataset\_v14



\## Overview



| Property | Value |

|----------|-------|

| \*\*Name\*\* | HRDataset\_v14 |

| \*\*Source\*\* | Kaggle |

| \*\*Format\*\* | CSV |

| \*\*Size\*\* |311 rows and 36 columns |

| \*\*Domain\*\* | Human Resources |

| \*\*Target variable\*\* | `Termd` — 1 = employee left (terminated/resigned), 0 = still active |



\## Sensitive attributes



| Column | Values | Why sensitive |

|--------|--------|---------------|

| `Sex` | M, F | Gender is protected by anti-discrimination law |

| `RaceDesc` | White, Black, Asian, Hispanic, etc. | Ethnicity because a model could unfairly penalize a racial group |

| `MaritalDesc` | Single, Married, Divorced, Widowed | Personal life should not influence employment decisions |

| `CitizenDesc` | US Citizen, Eligible NonCitizen, Non-Citizen | Immigration status informations are legally protected |

| `Age` | Numeric | Age discrimination is illegal in most countries |



\## Cleaning steps



| Step | What was done | Why |

|------|---------------|-----|

| Age calculation | Created `Age` column from `DOB` (2024 - birth year) | Key feature for turnover prediction |

| Missing values | Numeric are filled with mean, Categorical are filled with mode | Simple, low-cost imputation (Frugal AI) |

| Encoding | LabelEncoder on categorical columns (Sex, MaritalDesc, Position, etc.) | Memory-efficient, mappings saved for explainability |

| Two versions | CORE (8 features) and ALL (30+ features) | CORE for frugal modeling, ALL for flexibility |

| Train/test split | 80/20 split, random seed = 42 | Reproducibility |





\## Dataset versions



| File | Description |

|------|-------------|

| `data/raw/HRDataset\_v14.csv` | Original untouched dataset |

| `data/cleaned/HRDataset\_cleaned\_CORE.csv` | 8 key features + target — optimized for Frugal AI |

| `data/cleaned/HRDataset\_cleaned\_ALL.csv` | All columns cleaned — for extended modeling |

| `data/cleaned/X\_train\_CORE.csv` / `X\_test\_CORE.csv` | Train/test features (CORE version) |

| `data/cleaned/X\_train\_ALL.csv` / `X\_test\_ALL.csv` | Train/test features (ALL version) |

| `data/cleaned/y\_train.csv` / `y\_test.csv` | Train/test target (shared by both versions) |

| `data/cleaned/encoding\_mappings.json` | Categorical encoding reference for explainability |



\### CORE features (Frugal AI priority)



`Age`, `Salary`, `PerfScoreID`, `DaysLateLast30`, `DeptID`, `PositionID`, `MaritalDesc`, `Sex`





\## Known issues



\- `encoding\_mappings.json` is currently empty — mappings need to be regenerated

\- One employee has `Age = -51` (likely a date parsing error in DOB)

\- Dataset is synthetic — findings may not generalize to real organizations

\- Small sample sizes for some groups (e.g., 3 American Indian employees, 4 Non-Citizens) make fairness analysis unreliable for those subgroups





\## Ethical considerations



\- Dataset contains protected attributes (gender, race, age, citizenship) so any model must be audited for bias before deployment

\- Employee names are present in the raw data so anonymization is required under GDPR

\- This data is synthetic and intended for educational purposes only





