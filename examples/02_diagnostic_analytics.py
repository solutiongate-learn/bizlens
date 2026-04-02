"""
BizLens — Example 02: Diagnostic Analytics
===========================================
Topics covered
--------------
• diagnostic.normality_test()    — Shapiro-Wilk normality check
• diagnostic.ttest()             — One and two-sample t-tests
• diagnostic.anova()             — One-way ANOVA with interpretation
• diagnostic.chi_square()        — Chi-square independence test
• diagnostic.correlation()       — Pearson / Spearman correlation
• tables.crosstab()              — Cross-tabulation with chi-square
• tables.correlation_matrix()    — Full correlation matrix with ★ stars
• tables.group_comparison()      — Descriptive stats by group + ANOVA
• tables.distribution_fit()      — Fit distributions and rank by AIC

Run anywhere
------------
  Google Colab : paste into a code cell and run
  VSCode / Jupyter / Terminal : python 02_diagnostic_analytics.py
"""

# ── Auto-install ──────────────────────────────────────────────────────────────
import subprocess, sys

def _install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

for pkg in ["bizlens", "scipy", "matplotlib", "seaborn", "rich"]:
    try:
        __import__(pkg.split("[")[0])
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
df = bl.load_dataset("tips", show_citation=False)
print(f"Dataset: tips | Shape: {df.shape}\n")

# ── 1. Always start with normality check ─────────────────────────────────────
print("="*60)
print("1. Shapiro-Wilk Normality Test — total_bill:")
norm = bl.diagnostic.normality_test(df["total_bill"], alpha=0.05)
print(f"   W={norm['statistic']:.4f}, p={norm['p_value']:.4f}")
print(f"   Normally distributed? {'YES ✅' if norm['normal'] else 'NO ❌ → prefer non-parametric tests'}")

print("\nShapiro-Wilk — tip:")
norm_tip = bl.diagnostic.normality_test(df["tip"], alpha=0.05)
print(f"   W={norm_tip['statistic']:.4f}, p={norm_tip['p_value']:.4f}, Normal? {norm_tip['normal']}")

# ── 2. One-sample t-test (is mean tip different from $3.00?) ─────────────────
print("\n" + "="*60)
print("2. One-sample t-test — is the mean tip equal to $3.00?")
from scipy import stats as sp
t_stat, p_val = sp.ttest_1samp(df["tip"], popmean=3.0)
print(f"   Observed mean tip: ${df['tip'].mean():.4f}")
print(f"   H₀: mean = $3.00   |   t={t_stat:.4f}, p={p_val:.4f}")
print(f"   Result: {'Reject H₀ ✅' if p_val < 0.05 else 'Fail to reject H₀ ❌'}")

# ── 3. Two-sample t-test ──────────────────────────────────────────────────────
print("\n" + "="*60)
print("3. Two-sample t-test — Lunch vs Dinner total_bill:")
lunch  = df[df["time"] == "Lunch"]["total_bill"]
dinner = df[df["time"] == "Dinner"]["total_bill"]
print(f"   Lunch  mean: ${lunch.mean():.4f}  (n={len(lunch)})")
print(f"   Dinner mean: ${dinner.mean():.4f}  (n={len(dinner)})")
ttest = bl.diagnostic.ttest(lunch, dinner, alternative="two-sided", alpha=0.05)
print(f"   t={ttest['t_statistic']:.4f}, p={ttest['p_value']:.4f}")
print(f"   Significant difference? {'YES ✅' if ttest['significant'] else 'NO ❌'}")
print(f"   Cohen's d (effect size): {ttest.get('cohens_d', 'N/A')}")

# ── 4. One-way ANOVA ──────────────────────────────────────────────────────────
print("\n" + "="*60)
print("4. One-way ANOVA — does tip vary significantly by day?")
days = df["day"].unique()
groups = [df[df["day"] == d]["tip"].values for d in sorted(days)]
for d, g in zip(sorted(days), groups):
    print(f"   {d}: mean=${np.mean(g):.3f}, n={len(g)}")
anova = bl.diagnostic.anova(*groups, alpha=0.05)
print(f"\n   F={anova['f_statistic']:.4f}, p={anova['p_value']:.4f}")
print(f"   Significant? {'YES ✅ — at least one group differs' if anova['significant'] else 'NO ❌ — no significant difference'}")

# ── 5. Chi-square test ────────────────────────────────────────────────────────
print("\n" + "="*60)
print("5. Chi-square test — is smoking status independent of day?")
chi2 = bl.diagnostic.chi_square(df, col1="smoker", col2="day", alpha=0.05)
print(f"   χ²={chi2['chi2_statistic']:.4f}, df={chi2['degrees_of_freedom']}, p={chi2['p_value']:.4f}")
print(f"   Independent? {'NO ❌ — association exists' if chi2['significant'] else 'YES ✅ — no association'}")
print(f"   Cramér's V (effect size): {chi2.get('cramers_v', 'N/A')}")

print("\nChi-square — sex × smoker:")
chi2b = bl.diagnostic.chi_square(df, col1="sex", col2="smoker", alpha=0.05)
print(f"   χ²={chi2b['chi2_statistic']:.4f}, p={chi2b['p_value']:.4f}, Significant? {chi2b['significant']}")

# ── 6. Pearson correlation ────────────────────────────────────────────────────
print("\n" + "="*60)
print("6. Pearson correlation — all numeric columns vs tip:")
corr = bl.diagnostic.correlation(df, method="pearson", target="tip")
print("   (see table above for full correlation coefficients and p-values)")

print("\nSpearman correlation (rank-based, robust to outliers):")
corr_s = bl.diagnostic.correlation(df, method="spearman", target="tip")

# ── 7. Cross-tabulation ───────────────────────────────────────────────────────
print("\n" + "="*60)
print("7. Cross-tabulation — sex × smoker (with counts and %):")
ct = bl.tables.crosstab(df, row_col="sex", col_col="smoker",
                         normalize=None, show_plot=True)
print("\nRow-normalized (% within each sex):")
ct_norm = bl.tables.crosstab(df, row_col="sex", col_col="smoker",
                              normalize="index", show_plot=False)

# ── 8. Correlation matrix with significance stars ─────────────────────────────
print("\n" + "="*60)
print("8. Correlation matrix — numeric columns (* p<0.05  ** p<0.01  *** p<0.001):")
corr_matrix = bl.tables.correlation_matrix(
    df, columns=["total_bill", "tip", "size"], method="pearson", show_plot=True
)

print("\nSpearman correlation matrix:")
corr_s_matrix = bl.tables.correlation_matrix(
    df, columns=["total_bill", "tip", "size"], method="spearman", show_plot=False
)

# ── 9. Group comparison with ANOVA ────────────────────────────────────────────
print("\n" + "="*60)
print("9. Group comparison — tip by smoker status:")
grp_smoker = bl.tables.group_comparison(df, group_col="smoker",
                                         value_col="tip", show_plot=True)

print("\nGroup comparison — total_bill by day:")
grp_day = bl.tables.group_comparison(df, group_col="day",
                                      value_col="total_bill", show_plot=True)

# ── 10. Distribution fit ──────────────────────────────────────────────────────
print("\n" + "="*60)
print("10. Distribution fit — total_bill (which theoretical distribution fits best?):")
dist_fit = bl.tables.distribution_fit(
    df, column="total_bill",
    distributions=["norm", "lognorm", "gamma", "expon", "weibull_min"],
    show_plot=True
)
best = dist_fit.iloc[0]
print(f"\n   Best fit: {best['Distribution']}  AIC={best['AIC']}  KS p={best['KS p-value']}")

# ── 11. Practical interpretation guide ────────────────────────────────────────
print("\n" + "="*60)
print("11. When to use which test:")
print("""
  ┌─────────────────────────────────────────────────────────────────┐
  │ Test             │ Use when                                      │
  ├─────────────────────────────────────────────────────────────────┤
  │ t-test           │ Compare means of 2 groups (numeric)           │
  │ ANOVA            │ Compare means of 3+ groups (numeric)          │
  │ Chi-square       │ Test association between 2 categorical vars   │
  │ Pearson r        │ Linear relationship (both normally dist.)     │
  │ Spearman ρ       │ Monotonic relationship (non-normal / ordinal) │
  │ Shapiro-Wilk     │ Test if data is normally distributed          │
  └─────────────────────────────────────────────────────────────────┘

  Rule: Always check normality BEFORE choosing a parametric test!
""")

print("✅ Example 02 complete — Diagnostic Analytics")
