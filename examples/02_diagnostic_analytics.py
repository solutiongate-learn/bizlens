"""
BizLens — Example 02: Diagnostic Analytics
===========================================
Covers:
  • diagnostic.ttest()         — One-sample and two-sample t-tests
  • diagnostic.anova()         — One-way ANOVA with post-hoc
  • diagnostic.chi_square()    — Chi-square test of independence
  • diagnostic.correlation()   — Pearson / Spearman correlation
  • diagnostic.normality_test()— Shapiro-Wilk normality test
  • tables.crosstab()          — Cross-tabulation + chi-square
  • tables.correlation_matrix()— Full correlation matrix with stars
  • tables.group_comparison()  — Descriptive stats by group

Run:   python 02_diagnostic_analytics.py
"""

import numpy as np
import pandas as pd
import bizlens as bl

# ──────────────────────────────────────────────────────────────────────────────
# Load data
# ──────────────────────────────────────────────────────────────────────────────
df = bl.load_dataset("tips")
print(f"Dataset: tips  |  Shape: {df.shape}\n")

# ──────────────────────────────────────────────────────────────────────────────
# 1. Normality test (before running parametric tests)
# ──────────────────────────────────────────────────────────────────────────────
print("="*60)
print("1. Normality Test (Shapiro-Wilk) — total_bill:")
norm = bl.diagnostic.normality_test(df["total_bill"], alpha=0.05)
print(f"   Normal? {norm['normal']}, p={norm['p_value']:.4f}")

# ──────────────────────────────────────────────────────────────────────────────
# 2. Two-sample t-test — do lunch vs dinner bills differ?
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("2. Two-sample t-test — Lunch vs Dinner total_bill:")
lunch  = df[df["time"] == "Lunch"]["total_bill"]
dinner = df[df["time"] == "Dinner"]["total_bill"]
ttest = bl.diagnostic.ttest(lunch, dinner, alternative="two-sided", alpha=0.05)
print(f"   t={ttest['t_statistic']:.4f}, p={ttest['p_value']:.4f}, Significant? {ttest['significant']}")

# ──────────────────────────────────────────────────────────────────────────────
# 3. One-way ANOVA — does tip vary by day?
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("3. One-way ANOVA — tip by day of week:")
groups = [df[df["day"] == d]["tip"].values for d in df["day"].unique()]
anova = bl.diagnostic.anova(*groups, alpha=0.05)
print(f"   F={anova['f_statistic']:.4f}, p={anova['p_value']:.4f}, Significant? {anova['significant']}")

# ──────────────────────────────────────────────────────────────────────────────
# 4. Chi-square test — is smoking related to the day of the week?
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("4. Chi-square test — smoker × day independence:")
chi2 = bl.diagnostic.chi_square(df, col1="smoker", col2="day", alpha=0.05)
print(f"   chi2={chi2['chi2_statistic']:.4f}, p={chi2['p_value']:.4f}, Significant? {chi2['significant']}")

# ──────────────────────────────────────────────────────────────────────────────
# 5. Correlation — how does total_bill correlate with tip?
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("5. Pearson correlation — all numeric columns vs tip:")
corr = bl.diagnostic.correlation(df, method="pearson", target="tip")

# ──────────────────────────────────────────────────────────────────────────────
# 6. Cross-tabulation with chi-square
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("6. Cross-tabulation — sex × smoker:")
ct = bl.tables.crosstab(df, row_col="sex", col_col="smoker",
                         normalize=None, show_plot=True)

# ──────────────────────────────────────────────────────────────────────────────
# 7. Full correlation matrix with significance stars
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("7. Correlation matrix — all numeric columns:")
corr_matrix = bl.tables.correlation_matrix(df,
    columns=["total_bill", "tip", "size"],
    method="pearson", show_plot=True)

# ──────────────────────────────────────────────────────────────────────────────
# 8. Group comparison — tip by smoker
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("8. Group comparison — tip by smoker status:")
grp = bl.tables.group_comparison(df, group_col="smoker", value_col="tip", show_plot=True)

# ──────────────────────────────────────────────────────────────────────────────
# 9. Distribution fit — which distribution best describes total_bill?
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("9. Distribution fit comparison — total_bill:")
dist_fit = bl.tables.distribution_fit(df, column="total_bill",
    distributions=["norm", "lognorm", "gamma", "expon"], show_plot=True)

print("\n✅ Example 02 complete.")
