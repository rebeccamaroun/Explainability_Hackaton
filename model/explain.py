import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# --- Load and prep (same as train.py) ---
df = pd.read_csv("data\\cleaned\\HRDataset_cleaned.csv")
df['Age'] = df['Age'].abs()
leakage_cols = [col for col in df.columns if col.startswith('EmploymentStatus_')]
df = df.drop(columns=leakage_cols)
df = df.drop(columns=['State'])
df = df.drop(columns=['EmpStatusID', 'Tenure_Years', 'Years_Since_Last_Review'])

X = df.drop(columns=['Termd'])
y = df['Termd']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- Train the frugal model ---
importances = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train).feature_importances_
top10_cols = pd.Series(importances, index=X_train.columns).nlargest(10).index.tolist()

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train[top10_cols], y_train)

# --- SHAP explanations ---
explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_test[top10_cols])

# Plot 1: Global feature importance (which features matter most overall)
print("Saving SHAP summary plot...")
shap.summary_plot(shap_values[:, :, 1], X_test[top10_cols], show=False)
plt.tight_layout()
plt.savefig("assets\\shap_summary.png", dpi=150, bbox_inches='tight')
plt.close()

# Plot 2: Single prediction explanation (why did we flag this employee?)
print("Saving individual explanation plot...")
shap.force_plot(explainer.expected_value[1], shap_values[0, :, 1], X_test[top10_cols].iloc[0], matplotlib=True, show=False)
plt.savefig("assets\\shap_individual.png", dpi=150, bbox_inches='tight')
plt.close()

print("Done! Check assets/ folder for plots.")