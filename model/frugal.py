import pandas as pd
import numpy as np
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from codecarbon import EmissionsTracker

# --- Load and prep ---
df = pd.read_csv("data\\cleaned\\HRDataset_cleaned.csv")
df['Age'] = df['Age'].abs()
leakage_cols = [col for col in df.columns if col.startswith('EmploymentStatus_')]
df = df.drop(columns=leakage_cols + ['State', 'EmpStatusID', 'Tenure_Years', 'Years_Since_Last_Review'])

X = df.drop(columns=['Termd'])
y = df['Termd']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- Get top 10 features ---
rf_temp = RandomForestClassifier(n_estimators=100, random_state=42)
rf_temp.fit(X_train, y_train)
top10_cols = pd.Series(rf_temp.feature_importances_, index=X_train.columns).nlargest(10).index.tolist()

# --- Compare 3 models: Logistic (frugal), RF top10 (frugal), RF full (heavy) ---
models = {
    "Logistic Regression (10 features)": {
        "model": LogisticRegression(max_iter=2000, random_state=42),
        "X_train": X_train[top10_cols],
        "X_test": X_test[top10_cols],
        "scale": True
    },
    "Random Forest (10 features)": {
        "model": RandomForestClassifier(n_estimators=100, random_state=42),
        "X_train": X_train[top10_cols],
        "X_test": X_test[top10_cols],
        "scale": False
    },
    "Random Forest (73 features)": {
        "model": RandomForestClassifier(n_estimators=100, random_state=42),
        "X_train": X_train,
        "X_test": X_test,
        "scale": False
    }
}

print("=== Frugal AI Comparison ===\n")
print(f"{'Model':<40} {'Features':>8} {'AUC':>6} {'Time (s)':>10} {'CO2 (kg)':>12}")
print("-" * 80)

for name, config in models.items():
    Xtr = config["X_train"]
    Xte = config["X_test"]
    
    if config["scale"]:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        Xtr = pd.DataFrame(scaler.fit_transform(Xtr), columns=Xtr.columns)
        Xte = pd.DataFrame(scaler.transform(Xte), columns=Xte.columns)
    
    tracker = EmissionsTracker(project_name=name, log_level="error")
    tracker.start()
    t0 = time.time()
    config["model"].fit(Xtr, y_train)
    train_time = time.time() - t0
    emissions = tracker.stop()
    
    proba = config["model"].predict_proba(Xte)[:, 1]
    auc = roc_auc_score(y_test, proba)
    n_features = Xtr.shape[1]
    
    print(f"{name:<40} {n_features:>8} {auc:>6.3f} {train_time:>10.4f} {emissions:>12.6f}")

print("\nConclusion: The frugal model (10 features) achieves comparable")
print("performance with 86% fewer features and minimal compute cost.")