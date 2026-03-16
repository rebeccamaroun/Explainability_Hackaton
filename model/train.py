import pandas as pd
import numpy as np
import json
import shap
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler

# --- Load and clean ---
df = pd.read_csv("data\\cleaned\\HRDataset_cleaned.csv")
df['Age'] = df['Age'].abs()
leakage_cols = [col for col in df.columns if col.startswith('EmploymentStatus_')]
df = df.drop(columns=leakage_cols)
df = df.drop(columns=['State', 'EmpStatusID', 'Tenure_Years', 'Years_Since_Last_Review'])

print(f"Shape: {df.shape}")
print(f"Age range: {df['Age'].min()} to {df['Age'].max()}")

# --- Split ---
X = df.drop(columns=['Termd'])
y = df['Termd']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"Train: {X_train.shape}, Test: {X_test.shape}")
print(f"Target balance: {y.value_counts().to_dict()}")

# --- Model 1: Logistic Regression ---
scaler = StandardScaler()
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

lr = LogisticRegression(max_iter=2000, random_state=42)
lr.fit(X_train_scaled, y_train)
lr_proba = lr.predict_proba(X_test_scaled)[:, 1]

print("\n=== Logistic Regression ===")
print(classification_report(y_test, lr.predict(X_test_scaled)))
print(f"AUC-ROC: {roc_auc_score(y_test, lr_proba):.3f}")

# --- Model 2: Random Forest (full) ---
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_proba = rf.predict_proba(X_test)[:, 1]

print("\n=== Random Forest ===")
print(classification_report(y_test, rf.predict(X_test)))
print(f"AUC-ROC: {roc_auc_score(y_test, rf_proba):.3f}")

# --- Feature importance → select top 10 ---
importances = pd.Series(rf.feature_importances_, index=X_train.columns)
top10_cols = importances.nlargest(10).index.tolist()

print("\n=== Top 10 features ===")
for feat, imp in importances.nlargest(10).items():
    print(f"  {feat}: {imp:.4f}")

# --- Model 3: Random Forest Frugal (top 10 features) ---
rf_frugal = RandomForestClassifier(n_estimators=100, random_state=42)
rf_frugal.fit(X_train[top10_cols], y_train)
rf_frugal_proba = rf_frugal.predict_proba(X_test[top10_cols])[:, 1]

print("\n=== Random Forest Frugal (10 features) ===")
print(classification_report(y_test, rf_frugal.predict(X_test[top10_cols])))
print(f"AUC-ROC: {roc_auc_score(y_test, rf_frugal_proba):.3f}")

# --- Export for frontend ---
risk_df = df.copy()
risk_df['risk_score'] = rf_frugal.predict_proba(X[top10_cols])[:, 1]
risk_df['prediction'] = rf_frugal.predict(X[top10_cols])
risk_df.to_csv("assets\\employee_risk_scores.csv", index=False)
print("\nSaved: assets/employee_risk_scores.csv")

explainer = shap.TreeExplainer(rf_frugal)
shap_values = explainer.shap_values(X[top10_cols])

shap_output = []
for i in range(len(X)):
    employee = {
        "index": i,
        "risk_score": round(float(rf_frugal.predict_proba(X[top10_cols].iloc[[i]])[:, 1][0]), 3),
        "features": {}
    }
    for j, col in enumerate(top10_cols):
        employee["features"][col] = {
            "value": round(float(X[top10_cols].iloc[i][col]), 2),
            "shap_impact": round(float(shap_values[i, j, 1]), 4)
        }
    shap_output.append(employee)

with open("assets\\shap_explanations.json", "w") as f:
    json.dump(shap_output, f, indent=2)
print("Saved: assets/shap_explanations.json")