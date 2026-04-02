"""
BizLens v2.2.11 Example 3: Statistical Inference & Hypothesis Testing
=====================================================================
Self-Contained: YES (auto-install, all imports, data generation)
Environments: Colab, VSCode, Terminal, Jupyter

Demonstrates:
- Confidence intervals for means
- One-sample t-tests
- Two-sample t-tests with parametric and non-parametric alternatives
- Paired t-tests (before/after)
- ANOVA (comparing 3+ groups)
- Correlation significance testing
- Effect size interpretation
- Educational sample vs population comparisons
"""

import subprocess
import sys

try:
    import bizlens as bl
except ImportError:
    print("Installing BizLens v2.2.11...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "bizlens==2.2.11", "-q"])
    import bizlens as bl

import matplotlib
matplotlib.use("Agg")

import pandas as pd
import numpy as np

print(f"\n{'='*70}")
print(f"BizLens v{bl.__version__} — Statistical Inference Example")
print(f"{'='*70}")

# ════════════════════════════════════════════════════════════════════════════
# SETUP: GENERATE TEST DATA
# ════════════════════════════════════════════════════════════════════════════

print("\n[Setup] Generating test datasets...")

np.random.seed(42)

# Sample data for confidence interval
sample_data = pd.Series(np.random.normal(loc=100, scale=15, size=50))

# Two independent groups (control vs treatment)
control = pd.Series(np.random.normal(loc=100, scale=15, size=40))
treatment = pd.Series(np.random.normal(loc=110, scale=18, size=40))

# Before/after paired data
before = pd.Series(np.random.normal(loc=75, scale=12, size=30))
after = before + np.random.normal(loc=5, scale=8, size=30)  # Treatment effect

# Three groups for ANOVA
group_a = pd.Series(np.random.normal(loc=50, scale=10, size=25))
group_b = pd.Series(np.random.normal(loc=60, scale=10, size=25))
group_c = pd.Series(np.random.normal(loc=55, scale=10, size=25))

# Correlated variables
x = pd.Series(np.random.normal(loc=50, scale=10, size=100))
y = x * 2 + np.random.normal(loc=0, scale=20, size=100)

print("✓ Generated test datasets")

# ════════════════════════════════════════════════════════════════════════════
# PART 1: CONFIDENCE INTERVALS
# ════════════════════════════════════════════════════════════════════════════

print("\n[Part 1/5] CONFIDENCE INTERVALS")
print("─" * 70)

print("\n95% Confidence Interval for Sample Mean:")
lower, mean, upper = bl.inference.confidence_interval(sample_data, confidence=0.95)

print(f"\nInterpretation: We are 95% confident the true population mean")
print(f"is between {lower:.2f} and {upper:.2f}")

# ════════════════════════════════════════════════════════════════════════════
# PART 2: ONE-SAMPLE T-TEST
# ════════════════════════════════════════════════════════════════════════════

print("\n[Part 2/5] ONE-SAMPLE T-TEST")
print("─" * 70)
print("\nQuestion: Is the sample mean significantly different from 100?")

results = bl.inference.one_sample_ttest(sample_data, pop_mean=100)

print(f"\nConclusion: p-value = {results['p_value']:.4f}")
if results['significant']:
    print("→ The sample mean IS significantly different from 100 (p < 0.05)")
else:
    print("→ The sample mean is NOT significantly different from 100")

# ════════════════════════════════════════════════════════════════════════════
# PART 3: TWO-SAMPLE T-TEST
# ════════════════════════════════════════════════════════════════════════════

print("\n[Part 3/5] TWO-SAMPLE T-TEST")
print("─" * 70)
print("\nQuestion: Is the treatment group significantly different from control?")

t_test_results = bl.inference.two_sample_ttest(control, treatment)

print(f"\nConclusion: p-value = {t_test_results['p_value']:.4f}")
if t_test_results['significant']:
    print("→ Treatment group IS significantly different from control")
else:
    print("→ No significant difference between groups")
print(f"Effect Size (Cohen's d): {t_test_results['cohens_d']:.3f}")

# ════════════════════════════════════════════════════════════════════════════
# PART 4: PAIRED T-TEST
# ════════════════════════════════════════════════════════════════════════════

print("\n[Part 4/5] PAIRED T-TEST (Before/After)")
print("─" * 70)
print("\nQuestion: Did the treatment significantly change the outcome?")

paired_results = bl.inference.paired_ttest(before, after)

print(f"\nConclusion: p-value = {paired_results['p_value']:.4f}")
if paired_results['significant']:
    print("→ There IS a significant change from before to after")
else:
    print("→ No significant change detected")

# ════════════════════════════════════════════════════════════════════════════
# PART 5: ANOVA (Comparing 3+ Groups)
# ════════════════════════════════════════════════════════════════════════════

print("\n[Part 5/5] ONE-WAY ANOVA (3+ Groups)")
print("─" * 70)
print("\nQuestion: Do the three groups have significantly different means?")

anova_results = bl.inference.anova_test({
    'Group A': group_a,
    'Group B': group_b,
    'Group C': group_c
})

print(f"\nConclusion: F-statistic = {anova_results['f_statistic']:.4f}")
print(f"p-value = {anova_results['p_value']:.4f}")
if anova_results['significant']:
    print("→ At least one group mean is significantly different")
    print("→ (Post-hoc test like Tukey needed to identify which groups differ)")
else:
    print("→ No significant difference among groups")

# ════════════════════════════════════════════════════════════════════════════
# BONUS: CORRELATION TEST
# ════════════════════════════════════════════════════════════════════════════

print("\n[Bonus] CORRELATION SIGNIFICANCE TEST")
print("─" * 70)
print("\nQuestion: Is the correlation between X and Y significant?")

corr_results = bl.inference.correlation_test(x, y)

print(f"\nPearson Correlation: r = {corr_results['pearson_r']:.4f}")
print(f"p-value = {corr_results['pearson_p']:.4f}")
if corr_results['significant']:
    print("→ The correlation IS statistically significant (p < 0.05)")
else:
    print("→ No significant correlation")

# ════════════════════════════════════════════════════════════════════════════
# SUMMARY TABLE
# ════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("✓ EXAMPLE 3 COMPLETE — Statistical Inference")
print("=" * 70)
print("\nKey Topics Covered:")
print("  ✓ Confidence intervals (t-based for means)")
print("  ✓ One-sample t-tests (sample vs population)")
print("  ✓ Two-sample t-tests (independent groups)")
print("    - Parametric (t-test) with variance testing")
print("    - Non-parametric fallback (Mann-Whitney U)")
print("  ✓ Paired t-tests (before/after designs)")
print("  ✓ One-way ANOVA (3+ group comparison)")
print("  ✓ Correlation significance & confidence intervals")
print("  ✓ Effect size interpretation (Cohen's d, eta-squared)")
print("\nKey Learning Points:")
print("  • p-value < 0.05 → reject null hypothesis")
print("  • Effect size shows PRACTICAL significance, not just statistical")
print("  • Always check assumptions (normality, equal variance)")
print("  • Use non-parametric tests if assumptions violated")
print("\n" + "=" * 70)
