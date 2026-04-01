"""
BizLens — Example 03: Predictive Analytics
===========================================
Covers:
  • predict.linear_regression()    — Simple OLS with CI and residual plots
  • predict.multiple_regression()  — Multiple regression with cross-validation
  • predict.logistic_regression()  — Binary classification with AUC
  • predict.decision_tree()        — Decision tree (classification + regression)
  • predict.confusion_matrix_plot()— Visualize confusion matrix

Run:   python 03_predictive_analytics.py
"""

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, make_regression
import bizlens as bl

# ──────────────────────────────────────────────────────────────────────────────
# Load data
# ──────────────────────────────────────────────────────────────────────────────
tips = bl.load_dataset("tips")
print(f"Dataset: tips  |  Shape: {tips.shape}\n")

# ──────────────────────────────────────────────────────────────────────────────
# 1. Simple Linear Regression — predict tip from total_bill
# ──────────────────────────────────────────────────────────────────────────────
print("="*60)
print("1. Simple Linear Regression — tip ~ total_bill:")
lr = bl.predict.linear_regression(
    x=tips["total_bill"],
    y=tips["tip"],
    calculation_level="sample",
    confidence=0.95,
    show_plot=True,
)
print(f"   R²={lr['r_squared']:.4f}, slope={lr['slope']:.4f}, intercept={lr['intercept']:.4f}")
print(f"   95% CI for slope: [{lr['slope_ci'][0]:.4f}, {lr['slope_ci'][1]:.4f}]")

# ──────────────────────────────────────────────────────────────────────────────
# 2. Multiple Linear Regression — predict tip from total_bill + size
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("2. Multiple Linear Regression — tip ~ total_bill + size:")
X = tips[["total_bill", "size"]]
y = tips["tip"]
mlr = bl.predict.multiple_regression(X=X, y=y, calculation_level="sample")
print(f"   R²={mlr['r_squared']:.4f}, Adj R²={mlr['adj_r_squared']:.4f}")
print(f"   5-fold CV R²: {mlr['cv_r2_mean']:.4f} ± {mlr['cv_r2_std']:.4f}")

# ──────────────────────────────────────────────────────────────────────────────
# 3. Logistic Regression — predict smoker from total_bill + tip + size
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("3. Logistic Regression — predict smoker status:")
tips["smoker_bin"] = (tips["smoker"] == "Yes").astype(int)
X_log = tips[["total_bill", "tip", "size"]]
y_log = tips["smoker_bin"]
log_r = bl.predict.logistic_regression(X=X_log, y=y_log, threshold=0.5)
print(f"   Accuracy={log_r['accuracy']:.4f}, AUC={log_r['auc']:.4f}")

# ──────────────────────────────────────────────────────────────────────────────
# 4. Decision Tree Classifier — predict smoker
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("4. Decision Tree Classifier — predict smoker status:")
dt_cls = bl.predict.decision_tree(
    X=X_log, y=y_log,
    task="classification",
    max_depth=4,
    show_plot=True,
    feature_names=["total_bill", "tip", "size"],
    class_names=["Non-smoker", "Smoker"],
)
print(f"   Accuracy={dt_cls['accuracy']:.4f}, CV mean={dt_cls['cv_mean']:.4f}")
print(f"   Feature importance: {dt_cls['feature_importance']}")

# ──────────────────────────────────────────────────────────────────────────────
# 5. Decision Tree Regressor — predict tip
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("5. Decision Tree Regressor — predict tip from total_bill + size:")
dt_reg = bl.predict.decision_tree(
    X=tips[["total_bill", "size"]],
    y=tips["tip"],
    task="regression",
    max_depth=4,
    show_plot=True,
    feature_names=["total_bill", "size"],
)
print(f"   R²={dt_reg['r_squared']:.4f}, CV mean R²={dt_reg['cv_mean']:.4f}")

# ──────────────────────────────────────────────────────────────────────────────
# 6. Confusion matrix visualization
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("6. Confusion Matrix — logistic regression predictions:")
# Generate predictions from the logistic model
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
sc  = StandardScaler()
X_s = sc.fit_transform(X_log)
clf = LogisticRegression(random_state=42, max_iter=500)
clf.fit(X_s, y_log)
y_pred = clf.predict(X_s)
cm = bl.predict.confusion_matrix_plot(
    y_true=y_log,
    y_pred=y_pred,
    labels=["Non-smoker", "Smoker"],
    title="Logistic Regression — Confusion Matrix",
)
print(f"   Accuracy={cm['accuracy']:.4f}, F1={cm['f1_score']:.4f}")

# ──────────────────────────────────────────────────────────────────────────────
# 7. Synthetic dataset — larger regression example
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("7. Multiple Regression on synthetic dataset (500 rows, 4 features):")
X_syn, y_syn = make_regression(n_samples=500, n_features=4, noise=20, random_state=42)
X_df = pd.DataFrame(X_syn, columns=[f"feature_{i+1}" for i in range(4)])
syn_mlr = bl.predict.multiple_regression(X=X_df, y=pd.Series(y_syn, name="target"))
print(f"   R²={syn_mlr['r_squared']:.4f}, CV R²={syn_mlr['cv_r2_mean']:.4f}")

print("\n✅ Example 03 complete.")
