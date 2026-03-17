"""
employee_example.py — Find a real high-risk employee for the presentation

This script trains the final model (RF Tuned, set 2 features),
finds employees who were correctly flagged as high risk and actually left,
then prints their details for use in slides and documentation.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# --- Load and prep ---
df = pd.read_csv("data\\cleaned\\HRDataset_cleaned.csv")
df['Age'] = df['Age'].abs()
leakage_cols = [col for col in df.columns if col.startswith('EmploymentStatus_')]
df = df.drop(columns=leakage_cols + ['State', 'EmpStatusID', 'Tenure_Years', 'Years_Since_Last_Review'])

X = df.drop(columns=['Termd'])
y = df['Termd']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- Feature set 2 (final) ---
top10_cols = [
    "RecruitmentSource_Google Search",
    "Department_Production       ",
    "FromDiversityJobFairID",
    "RecruitmentSource_Diversity Job Fair",
    "SpecialProjectsCount",
    "Remote_Work_Frequency",
    "DaysLateLast30",
    "MaritalDesc_Single",
    "Department_IT/IS",
    "RecruitmentSource_Indeed"
]

# --- Train final model ---
rf = RandomForestClassifier(
    n_estimators=200, max_depth=8, min_samples_leaf=5,
    class_weight='balanced_subsample', random_state=42
)
rf.fit(X_train[top10_cols], y_train)

# --- Find high-risk employees who actually left ---
proba = rf.predict_proba(X_test[top10_cols])[:, 1]
test_df = X_test[top10_cols].copy()
test_df['risk_score'] = proba
test_df['actual'] = y_test.values

high_risk = test_df[test_df['actual'] == 1].sort_values('risk_score', ascending=False)

# --- Company averages for comparison ---
print("=== Company averages ===")
print(f"  Remote_Work_Frequency: {df['Remote_Work_Frequency'].mean():.1f}")
print(f"  SpecialProjectsCount: {df['SpecialProjectsCount'].mean():.1f}")
print()

# --- Top 3 high-risk employees ---
print("=== Top 3 correctly flagged employees ===\n")
for rank, (idx, row) in enumerate(high_risk.head(3).iterrows()):
    print(f"--- Employee #{idx} — Risk Score: {row['risk_score']:.2f} ---")
    for col in top10_cols:
        val = row[col]
        if val != 0:
            print(f"  {col} = {val}")
    print()