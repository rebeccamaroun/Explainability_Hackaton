"""
explain.py is the SHAP Explainability for HR Attrition Model

This script generates SHAP (SHapley Additive exPlanations) plots
for our final Random Forest model (tuned, 10 domain-informed features).

It produces two outputs in assets/:
  - shap_summary.png: global view — which features matter most across all employees
  - shap_individual.png: individual view — why one specific employee was flagged

This is the core of our Explainable AI theme: every prediction comes
with a human-readable explanation that HR managers can trust and act on.
"""
import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# --- Load and prep (same as model notebook) ---
df = pd.read_csv("data\\cleaned\\HRDataset_cleaned.csv")
df['Age'] = df['Age'].abs()
leakage_cols = [col for col in df.columns if col.startswith('EmploymentStatus_')]
df = df.drop(columns=leakage_cols)
df = df.drop(columns=['State', 'EmpStatusID', 'Tenure_Years', 'Years_Since_Last_Review'])

X = df.drop(columns=['Termd'])
y = df['Termd']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- Feature set 2 (final, domain-informed) ---
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

# --- Train the final model (RF Tuned) ---
rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    min_samples_leaf=5,
    class_weight='balanced_subsample',
    random_state=42
)
rf.fit(X_train[top10_cols], y_train)

# --- SHAP explanations ---
explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_test[top10_cols])

# Plot 1: Global feature importance
print("Saving SHAP summary plot...")
shap.summary_plot(shap_values[:, :, 1], X_test[top10_cols], show=False)
plt.tight_layout()
plt.savefig("assets\\shap_summary.png", dpi=150, bbox_inches='tight')
plt.close()

# Plot 2: Single prediction explanation (bar chart — cleaner than force plot)
print("Saving individual explanation plot...")
shap.plots.bar(shap.Explanation(
    values=shap_values[0, :, 1],
    base_values=explainer.expected_value[1],
    data=X_test[top10_cols].iloc[0].values,
    feature_names=top10_cols
), show=False)
plt.tight_layout()
plt.savefig("assets\\shap_individual.png", dpi=150, bbox_inches='tight')
plt.close()

print("Done! Check assets/ folder for updated plots.")