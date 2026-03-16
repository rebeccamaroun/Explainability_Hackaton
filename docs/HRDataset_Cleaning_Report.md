# HRDataset_v14 Data Cleaning Report (Frugal AI Aligned)
## Overview
This document details the data cleaning process performed on `HRDataset_v14.csv` for the AI×HR Hackathon (Frugal AI + Explainable AI track). The cleaning follows **Frugal AI principles** (minimal computation, memory efficiency, no redundant processing) while retaining full data flexibility for modeling teams.

## 1. Preprocessing Objectives
- Remove data noise and fill missing values (minimalist approach)
- Encode categorical features (memory-efficient LabelEncoder vs. OneHotEncoder)
- Retain ALL original columns (no permanent deletion) + create a "core features" subset for Frugal AI
- Split data into train/test sets (80/20) for modeling
- Ensure full reproducibility and interpretability (save encoding mappings)

## 2. Step-by-Step Cleaning Process
### 2.1 Dataset Loading & Initial Inspection
- Loaded raw dataset: `HRDataset_v14.csv`
- Validated target column (`Termd` = employee turnover label: 1 = terminated, 0 = active) exists
- Inspected column types, missing values, and data structure (total rows: ~400, total columns: 30+)
- Identified key categorical columns (e.g., `Sex`, `MaritalDesc`, `Position`) and numeric columns (e.g., `Salary`, `PerfScoreID`)

### 2.2 Feature Enhancement (Frugal Calculation)
- Calculated `Age` from `DOB` (date of birth) using a simple, low-computation method:  
  `Age = 2024 - DOB.dt.year` (no complex datetime operations)
- Added `Age` to the dataset (critical feature for turnover prediction)

### 2.3 Missing Value Imputation (Minimalist Approach)
Filled missing values with the simplest methods (no resource-heavy interpolation):
| Column Type | Imputation Method | Rationale (Frugal AI) |
|-------------|-------------------|-----------------------|
| Numeric (e.g., `Salary`, `Age`, `PerfScoreID`) | Mean value | Fast computation, no overfitting risk for small datasets |
| Categorical (e.g., `Sex`, `MaritalDesc`, `TermReason`) | Mode (most frequent value) | Preserves distribution, minimal computational cost |
- **Result**: 0 missing values remaining in the cleaned dataset

### 2.4 Categorical Feature Encoding
- Used `LabelEncoder` (memory-efficient vs. OneHotEncoder) to convert text-based categorical columns to numeric values
- Encoded columns: `Sex`, `MaritalDesc`, `CitizenDesc`, `RaceDesc`, `TermReason`, `Position`, `State`, `Department`
- Converted numpy `int64` outputs to native Python `int` (to enable JSON serialization)
- Saved encoding mappings to `encoding_mappings.json` (critical for Explainable AI):  
  Example mapping: `{"Sex": {"F": 0, "M": 1}, "MaritalDesc": {"Single": 0, "Married": 1}}`

### 2.5 Column Selection (Dual Versions for Flexibility)
No permanent column deletion—created two versions of the cleaned dataset:
| Version | Columns Included | Use Case |
|---------|------------------|----------|
| Core (Frugal AI) | 8 high-impact features + target (`Termd`):<br>`Age`, `Salary`, `PerfScoreID`, `DaysLateLast30`, `DeptID`, `PositionID`, `MaritalDesc`, `Sex` | Fast training, low resource consumption (Frugal AI priority) |
| Full | All original columns (30+) | Flexible modeling (teammates may use additional features) |

### 2.6 Train/Test Split (Reproducible)
- Split data into 80% training / 20% testing sets (fixed `random_state=42` for reproducibility)
- Generated split files for both Core and Full versions:
  - Core: `X_train_CORE.csv`, `X_test_CORE.csv`
  - Full: `X_train_ALL.csv`, `X_test_ALL.csv`
  - Shared target sets: `y_train.csv`, `y_test.csv` (label = `Termd`)

## 3. Output Files
| File Name | Purpose | Key Details |
|-----------|---------|-------------|
| `HRDataset_cleaned_ALL.csv` | Full cleaned dataset | All columns, no missing values, encoded categoricals |
| `HRDataset_cleaned_CORE.csv` | Core features dataset | 8 high-impact columns (Frugal AI optimized) |
| `X_train_CORE.csv` / `X_test_CORE.csv` | Core features train/test sets | Ready for Frugal AI modeling (lightweight models) |
| `X_train_ALL.csv` / `X_test_ALL.csv` | Full features train/test sets | Flexible for extended modeling |
| `y_train.csv` / `y_test.csv` | Target label sets | Shared for both Core/Full versions (label = `Termd`) |
| `encoding_mappings.json` | Encoding reference | Decode numeric categorical values back to original text (Explainable AI) |

## 4. Compliance with Frugal AI Principles
1. **Minimal computation**: Used mean/mode imputation (no complex ML-based imputation) and simple age calculation
2. **Memory efficiency**: LabelEncoder (no redundant columns from OneHotEncoder)
3. **Data efficiency**: Core feature subset reduces dataset size without losing predictive power
4. **Flexibility**: Full dataset retained for teammates (no data loss)
5. **Reproducibility**: Fixed random seed for train/test split, documented all steps

## 5. Notes for Modeling Team
- **Priority**: Use `CORE` files for Frugal AI modeling (logistic regression, low energy consumption)
- **Interpretability**: Reference `encoding_mappings.json` to decode categorical values (critical for Explainable AI)
- **Flexibility**: Use `ALL` files if additional features are needed (compare resource usage vs. Core version)
- **No further cleaning needed**: All files are ready for model training (no missing values/raw text)