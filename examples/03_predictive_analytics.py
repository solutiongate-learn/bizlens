"""
BizLens — Example 03: Predictive Analytics
===========================================
Topics covered
--------------
• predict.linear_regression()    — OLS with 95% CI, residuals, R²
• predict.multiple_regression()  — Multiple regression + 5-fold cross-validation
• predict.logistic_regression()  — Binary classifier with AUC-ROC curve
• predict.decision_tree()        — Classification & regression trees
• predict.confusion_matrix_plot()— Visualise TP/TN/FP/FN + precision/recall
• Interpretation guide           — What R², AUC, Accuracy mean in practice

Run anywhere
------------
  Google Colab : paste into a code cell and run
  VSCode / Jupyter / Terminal : python 03_predictive_analytics.py
"""

# ── Auto-install ──────────────────────────────────────────────────────────────
import subprocess, sys

def _install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

for pkg in ["bizlens", "scikit-learn", "scipy", "matplotlib", "numpy", "pandas"]:
    try:
        import_name = pkg.replace("-", "_").replace("scikit_learn", "sklearn")
        __import__(import_name)
    except ImportError:
        print(f"Installing {pkg}...")
        _install(pkg)

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import bizlens as bl

print(f"BizLens version: {bl.__version__}\n")

# ── Load data ─────────────────────────────────────────────────────────────────
tips = bl.load_dataset("tips", show_citation=False)
tips["smoker_bin"] = (tips["smoker"] == "Yes").astype(int)
print(f"Dataset: tips | Shape: {tips.shape}\n")

# ── 1. Simple Linear Regression ───────────────────────────────────────────────
print("="*60)
print("1. Simple Linear Regression — tip ~ total_bill:")
lr = bl.predict.linear_regression(
    x=tips["total_bill"],
    y=tips["tip"],
    calculation_level="sample",
    confidence=0.95,
    show_plot=True,
)
print(f"\n   Equation: tip = {lr['intercept']:.4f} + {lr['slope']:.4f} × total_bill")
print(f"   R² = {lr['r_squared']:.4f}  → model explains {lr['r_squared']*100:.1f}% of tip variance")
print(f"   95% CI for slope: [{lr['slope_ci'][0]:.4f}, {lr['slope_ci'][1]:.4f}]")
print(f"   RMSE = {lr['rmse']:.4f}  |  p-value = {lr['p_value']:.6f}")
print(f"   Significant predictor? {'YES ✅' if lr['p_value'] < 0.05 else 'NO ❌'}")

# ── 2. Multiple Linear Regression ─────────────────────────────────────────────
print("\n" + "="*60)
print("2. Multiple Linear Regression — tip ~ total_bill + size:")
X_multi = tips[["total_bill", "size"]]
y_tip   = tips["tip"]
mlr = bl.predict.multiple_regression(
    X=X_multi, y=y_tip, calculation_level="sample"
)
print(f"\n   R²       = {mlr['r_squared']:.4f}")
print(f"   Adj R²   = {mlr['adj_r_squared']:.4f}  (penalises extra predictors)")
print(f"   5-fold CV R²: {mlr['cv_r2_mean']:.4f} ± {mlr['cv_r2_std']:.4f}")
print(f"   Coefficients:")
for col, coef in mlr['coefficients'].items():
    print(f"     {col:15s}: {coef:+.4f}")

print("\n   Adding smoker as a binary predictor:")
X_multi3 = tips[["total_bill", "size", "smoker_bin"]]
mlr3 = bl.predict.multiple_regression(X=X_multi3, y=y_tip)
print(f"   R² with 3 vars = {mlr3['r_squared']:.4f}  (was {mlr['r_squared']:.4f})")
print(f"   Improvement: {(mlr3['r_squared'] - mlr['r_squared'])*100:.2f} percentage points")

# ── 3. Logistic Regression ────────────────────────────────────────────────────
print("\n" + "="*60)
print("3. Logistic Regression — predict smoker status from bill data:")
X_log = tips[["total_bill", "tip", "size"]]
y_log = tips["smoker_bin"]
log_r = bl.predict.logistic_regression(
    X=X_log, y=y_log, threshold=0.5
)
print(f"\n   Accuracy = {log_r['accuracy']:.4f}")
print(f"   AUC-ROC  = {log_r['auc_roc']:.4f}  (0.5=random, 1.0=perfect)")
print(f"   Baseline accuracy (always predict majority): "
      f"{max(y_log.mean(), 1-y_log.mean()):.4f}")

# ── 4. Decision Tree Classifier ───────────────────────────────────────────────
print("\n" + "="*60)
print("4. Decision Tree Classifier — predict smoker status (max_depth=4):")
dt_cls = bl.predict.decision_tree(
    X=X_log, y=y_log,
    task="classification",
    max_depth=4,
    show_plot=True,
    feature_names=["total_bill", "tip", "size"],
    class_names=["Non-smoker", "Smoker"],
)
print(f"\n   Training Accuracy  = {dt_cls['accuracy']:.4f}")
print(f"   CV Accuracy (mean) = {dt_cls['cv_mean']:.4f} ± {dt_cls['cv_std']:.4f}")
print(f"   Tree depth used    = {dt_cls['tree_depth']}")
print(f"   Leaf nodes         = {dt_cls['n_leaves']}")
print("\n   Feature Importance (higher = more useful split criterion):")
for feat, imp in sorted(dt_cls['feature_importance'].items(),
                         key=lambda x: x[1], reverse=True):
    bar = "█" * int(imp * 30)
    print(f"     {feat:15s}: {imp:.4f}  {bar}")

# ── 5. Decision Tree Regressor ────────────────────────────────────────────────
print("\n" + "="*60)
print("5. Decision Tree Regressor — predict tip (max_depth=4):")
dt_reg = bl.predict.decision_tree(
    X=tips[["total_bill", "size"]],
    y=tips["tip"],
    task="regression",
    max_depth=4,
    show_plot=True,
    feature_names=["total_bill", "size"],
)
print(f"\n   R²         = {dt_reg['r_squared']:.4f}")
print(f"   CV R² mean = {dt_reg['cv_mean']:.4f} ± {dt_reg['cv_std']:.4f}")

# ── 6. Confusion Matrix ───────────────────────────────────────────────────────
print("\n" + "="*60)
print("6. Confusion Matrix — logistic regression predictions:")
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
sc  = StandardScaler()
X_s = sc.fit_transform(X_log)
clf = LogisticRegression(random_state=42, max_iter=1000)
clf.fit(X_s, y_log)
y_pred_log = clf.predict(X_s)

cm = bl.predict.confusion_matrix_plot(
    y_true=y_log,
    y_pred=y_pred_log,
    labels=["Non-smoker", "Smoker"],
    title="Logistic Regression — Confusion Matrix",
)
print(f"\n   Accuracy  = {cm['accuracy']:.4f}")
print(f"   Precision = {cm['precision']:.4f}  (of predicted positives, how many are correct)")
print(f"   Recall    = {cm['recall']:.4f}  (of actual positives, how many did we catch)")
print(f"   F1 Score  = {cm['f1_score']:.4f}  (harmonic mean of precision and recall)")

# ── 7. Breast cancer dataset — larger classification ──────────────────────────
print("\n" + "="*60)
print("7. Breast Cancer Classification (569 rows, 30 features):")
cancer_df = bl.load_dataset("breast_cancer", show_citation=False)
target_col = "target" if "target" in cancer_df.columns else cancer_df.columns[-1]
feature_cols = [c for c in cancer_df.columns if c != target_col][:10]  # use first 10
print(f"   Features used: {feature_cols}")

dt_cancer = bl.predict.decision_tree(
    X=cancer_df[feature_cols],
    y=cancer_df[target_col].astype(int),
    task="classification",
    max_depth=5,
    show_plot=True,
    feature_names=feature_cols,
    class_names=["Malignant", "Benign"],
)
print(f"   CV Accuracy: {dt_cancer['cv_mean']:.4f} ± {dt_cancer['cv_std']:.4f}")

# ── 8. Interpretation guide ───────────────────────────────────────────────────
print("\n" + "="*60)
print("8. Quick interpretation guide:")
print("""
  R² (R-squared) — Regression
  ─────────────────────────────
  0.0 – 0.3  : Weak fit — model explains very little variance
  0.3 – 0.6  : Moderate fit — some predictive power
  0.6 – 0.8  : Good fit — useful for many business applications
  0.8 – 1.0  : Strong fit (check for overfitting if too close to 1.0)

  AUC-ROC — Classification
  ─────────────────────────
  0.5        : Random guessing (no better than a coin flip)
  0.7 – 0.8  : Acceptable
  0.8 – 0.9  : Excellent
  0.9 – 1.0  : Outstanding (check for data leakage)

  Cross-validation mean vs std
  ─────────────────────────────
  High mean, low std  → stable, generalisable model
  High mean, high std → model varies a lot — possibly overfitting
  Low mean            → model needs more features or a different algorithm
""")

print("✅ Example 03 complete — Predictive Analytics")
