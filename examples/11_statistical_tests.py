"""
BizLens — Example 11: Statistical Hypothesis Testing (Comprehensive)
=====================================================================
Topics covered — from BASICS to ADVANCED
-----------------------------------------
PARAMETRIC TESTS (assume normality)
  • diagnostic.normality_test()  — Shapiro-Wilk (prerequisite for all tests)
  • diagnostic.ztest()           — One-sample & two-sample Z-test (n ≥ 30, σ known)
  • diagnostic.ttest()           — Independent samples t-test (Student's)
  • diagnostic.welch_ttest()     — Welch's t-test (unequal variances)
  • diagnostic.paired_ttest()    — Paired / dependent samples t-test
  • diagnostic.anova()           — One-way ANOVA (3+ groups)
  • diagnostic.two_way_anova()   — Two-way ANOVA with interaction

NON-PARAMETRIC TESTS (no normality assumption)
  • diagnostic.mann_whitney()    — Non-parametric independent-group comparison
  • diagnostic.kruskal_wallis()  — Non-parametric one-way ANOVA (3+ groups)
  • diagnostic.chi_square()      — Association between two categorical variables
  • diagnostic.correlation()     — Spearman rank correlation (non-parametric)

CHOOSING THE RIGHT TEST
  • Decision guide table at the end of the script

Run anywhere
------------
  Google Colab : paste into a code cell and run
  VSCode / Jupyter / Terminal : python 11_statistical_tests.py
"""

# ── Auto-install ──────────────────────────────────────────────────────────────
import subprocess, sys

def _install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

for pkg in ["bizlens", "numpy", "pandas", "matplotlib", "scipy", "statsmodels"]:
    try:
        import_name = pkg.replace("-", "_")
        __import__(import_name)
    except ImportError:
        print(f"Installing {pkg}...")
        _install(pkg)

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # Safe for Colab / headless
import matplotlib.pyplot as plt
import bizlens as bl
from scipy import stats as sp_stats

np.random.seed(42)
print(f"BizLens version: {bl.__version__}\n")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 0: Always check normality FIRST
# ─────────────────────────────────────────────────────────────────────────────
print("="*60)
print("STEP 0: Always test normality BEFORE choosing a parametric test")
print("─"*60)

# Generate datasets we will use throughout
salary_a = np.random.normal(loc=55_000, scale=8_000, size=50)   # Dept A salaries
salary_b = np.random.normal(loc=60_000, scale=9_000, size=50)   # Dept B salaries
salary_c = np.random.normal(loc=58_000, scale=7_500, size=50)   # Dept C salaries
salary_d = np.random.normal(loc=62_000, scale=10_000, size=50)  # Dept D salaries
before   = np.random.normal(loc=120, scale=15, size=30)          # BP before treatment
after    = before - np.random.normal(loc=10, scale=5, size=30)   # BP after (paired)
skewed   = np.random.exponential(scale=2, size=50)               # Non-normal (skewed)

print("\nSalary Dept A:")
norm_a = bl.diagnostic.normality_test(salary_a, alpha=0.05)
print("\nSalary Dept B:")
norm_b = bl.diagnostic.normality_test(salary_b, alpha=0.05)
print("\nSkewed data (exponential):")
norm_s = bl.diagnostic.normality_test(skewed, alpha=0.05)
print(f"\n→ Salary A normal? {norm_a['normal']}  |  Salary B normal? {norm_b['normal']}"
      f"  |  Skewed normal? {norm_s['normal']}")
print("→ For skewed data, use non-parametric tests (Mann-Whitney, Kruskal-Wallis)")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Z-TEST — One-sample
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("1. One-Sample Z-Test — Is the average salary ≠ $55,000?")
print("   Use when: n ≥ 30 and σ is known (or large sample approximation)")
print("   H₀: μ = $55,000   H₁: μ ≠ $55,000   (two-sided)")
z1 = bl.diagnostic.ztest(
    data=salary_a,
    popmean=55_000,
    alternative="two-sided",
    alpha=0.05,
)
print(f"\n   n={len(salary_a)}, sample mean=${np.mean(salary_a):,.2f}, H₀ mean=$55,000")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Z-TEST — Two-sample
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("2. Two-Sample Z-Test — Do Dept A and Dept B have different mean salaries?")
print("   H₀: μ_A = μ_B   (no difference)")
z2 = bl.diagnostic.ztest(
    data=(salary_a, salary_b),
    alternative="two-sided",
    alpha=0.05,
)
print(f"\n   Dept A mean: ${np.mean(salary_a):,.0f}   Dept B mean: ${np.mean(salary_b):,.0f}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. INDEPENDENT SAMPLES T-TEST (Student's)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("3. Independent Samples t-Test (Student's) — Dept A vs Dept B:")
print("   Use when: two independent groups, both normally distributed, equal variances")
t1 = bl.diagnostic.ttest(salary_a, salary_b, alternative="two-sided", alpha=0.05)
print(f"\n   Cohen's d = {t1['cohens_d']:.4f} ({t1['effect_size']} effect size)")
print("   d < 0.2 = small,  0.2–0.5 = medium,  > 0.8 = large")

# ─────────────────────────────────────────────────────────────────────────────
# 4. WELCH'S T-TEST — Unequal variances
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("4. Welch's t-Test — Use when groups have UNEQUAL variances:")
print("   Welch's is more robust — recommended unless you have evidence of equal variances")
salary_unequal = np.random.normal(60_000, 20_000, 50)   # Much larger variance
w1 = bl.diagnostic.welch_ttest(salary_a, salary_unequal, alternative="two-sided", alpha=0.05)
f_ratio = np.var(salary_a, ddof=1) / np.var(salary_unequal, ddof=1)
print(f"\n   Variance ratio (s₁²/s₂²) = {f_ratio:.4f}  (≠ 1 → Welch's appropriate)")

# ─────────────────────────────────────────────────────────────────────────────
# 5. PAIRED T-TEST — Before/After
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("5. Paired Samples t-Test — Blood pressure before vs after treatment:")
print("   Use when: SAME subjects measured twice (before/after, pre/post)")
print("   Paired removes between-subject variability → more sensitive")
pt = bl.diagnostic.paired_ttest(before, after, alternative="two-sided", alpha=0.05)
print(f"\n   Mean BP before: {np.mean(before):.1f}   After: {np.mean(after):.1f}")
print(f"   Mean reduction: {pt['mean_diff']:.1f} mmHg  "
      f"({'significant ✅' if pt['significant'] else 'not significant ❌'})")

# ─────────────────────────────────────────────────────────────────────────────
# 6. ONE-WAY ANOVA — 3+ groups
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("6. One-Way ANOVA — Do 4 departments have different mean salaries?")
print("   Use when: 3+ independent groups, all normally distributed")
print("   H₀: all group means equal   H₁: at least one group differs")
for dept, sal in [("A", salary_a), ("B", salary_b), ("C", salary_c), ("D", salary_d)]:
    print(f"   Dept {dept}: n={len(sal)}, mean=${np.mean(sal):,.0f}, std=${np.std(sal,ddof=1):,.0f}")
anova1 = bl.diagnostic.anova(salary_a, salary_b, salary_c, salary_d, alpha=0.05)
print(f"\n   F={anova1['f_statistic']:.4f}, p={anova1['p_value']:.4f}")
if anova1['significant']:
    print("   → ANOVA is significant. Run post-hoc (e.g. Tukey HSD) to find which pairs differ.")
    # Manual Tukey-like pairwise check
    from itertools import combinations
    labels = ["A", "B", "C", "D"]
    arrays = [salary_a, salary_b, salary_c, salary_d]
    print("\n   Pairwise t-tests (Bonferroni-style — use with caution):")
    for (i1, l1), (i2, l2) in combinations(enumerate(labels), 2):
        t, p = sp_stats.ttest_ind(arrays[i1], arrays[i2])
        sig  = "✅" if p < 0.05/6 else "❌"  # Bonferroni: α/k comparisons
        print(f"     {l1} vs {l2}: t={t:.3f}, p={p:.4f} {sig}")

# ─────────────────────────────────────────────────────────────────────────────
# 7. TWO-WAY ANOVA — Two factors + interaction
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("7. Two-Way ANOVA — Salary ~ Department × Gender (with interaction):")
print("   Tests: Main effect of Dept, Main effect of Gender, Dept×Gender interaction")
np.random.seed(42)
n_per_cell = 15
departments = ["Engineering", "Marketing", "Finance"]
genders     = ["Male", "Female"]
rows = []
base = {"Engineering": 75000, "Marketing": 60000, "Finance": 70000}
gender_gap = {"Male": 5000, "Female": -5000}
for dept in departments:
    for gender in genders:
        sal = base[dept] + gender_gap[gender] + np.random.normal(0, 8000, n_per_cell)
        for s in sal:
            rows.append({"Salary": s, "Department": dept, "Gender": gender})
salary_df = pd.DataFrame(rows)

try:
    anova2 = bl.diagnostic.two_way_anova(
        data=salary_df,
        value_col="Salary",
        factor1_col="Department",
        factor2_col="Gender",
        alpha=0.05,
    )
    print("\n   Interpretation:")
    dept_sig   = anova2["main_effect_Department"]["significant"]
    gender_sig = anova2["main_effect_Gender"]["significant"]
    inter_sig  = anova2["interaction"]["significant"]
    print(f"   • Dept main effect:    {'✅ Significant' if dept_sig else '❌ Not significant'}")
    print(f"   • Gender main effect:  {'✅ Significant' if gender_sig else '❌ Not significant'}")
    print(f"   • Dept × Gender:       {'✅ Significant interaction' if inter_sig else '❌ No interaction'}")
    if inter_sig:
        print("     → Interaction means gender gap varies by department")
except Exception as e:
    print(f"   (Requires statsmodels: pip install statsmodels) — {e}")

# ─────────────────────────────────────────────────────────────────────────────
# 8. MANN-WHITNEY U — Non-parametric t-test alternative
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("8. Mann-Whitney U Test — Non-parametric (use when normality fails):")
print("   Equivalent to Wilcoxon rank-sum test")
print("   Tests whether one group tends to have higher VALUES than the other")
# Create a clearly non-normal dataset
income_urban = np.concatenate([
    np.random.lognormal(10.5, 0.7, 40),   # Most are modest
    np.random.lognormal(13.0, 0.4, 10),   # A few very high earners
])
income_rural = np.random.lognormal(10.2, 0.6, 50)
print(f"\n   Urban:  median=${np.median(income_urban):,.0f}  (non-normal: right-skewed)")
print(f"   Rural:  median=${np.median(income_rural):,.0f}")
mw = bl.diagnostic.mann_whitney(income_urban, income_rural, alternative="two-sided", alpha=0.05)
print(f"\n   Rank-biserial r = {mw['rank_biserial_r']:.4f}  (effect size: {mw['effect_size']})")
print("   r > 0 means Urban tends to be higher")

# ─────────────────────────────────────────────────────────────────────────────
# 9. KRUSKAL-WALLIS — Non-parametric ANOVA
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("9. Kruskal-Wallis H Test — Non-parametric one-way ANOVA (3+ groups):")
print("   Use when groups are not normally distributed")
satisfaction_a = np.random.choice([1,2,3,4,5], size=30, p=[0.05,0.10,0.30,0.35,0.20])
satisfaction_b = np.random.choice([1,2,3,4,5], size=30, p=[0.20,0.30,0.25,0.15,0.10])
satisfaction_c = np.random.choice([1,2,3,4,5], size=30, p=[0.10,0.15,0.20,0.30,0.25])
print(f"\n   Group A satisfaction  median={np.median(satisfaction_a):.1f}")
print(f"   Group B satisfaction  median={np.median(satisfaction_b):.1f}")
print(f"   Group C satisfaction  median={np.median(satisfaction_c):.1f}")
kw = bl.diagnostic.kruskal_wallis(satisfaction_a, satisfaction_b, satisfaction_c, alpha=0.05)
print(f"\n   η² (eta squared) = {kw['eta_squared']:.4f}  (effect size: {kw['effect_size']})")

# ─────────────────────────────────────────────────────────────────────────────
# 10. CHI-SQUARE — Categorical association
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("10. Chi-Square Test of Independence — Categorical × Categorical:")
print("    'Is customer satisfaction level associated with product category?'")
survey_df = pd.DataFrame({
    "Category": np.random.choice(["Electronics", "Clothing", "Food"], size=200,
                                  p=[0.40, 0.35, 0.25]),
    "Satisfaction": np.random.choice(["High", "Medium", "Low"], size=200,
                                      p=[0.45, 0.35, 0.20]),
})
chi = bl.diagnostic.chi_square(survey_df, col1="Category", col2="Satisfaction", alpha=0.05)
ct = pd.crosstab(survey_df["Category"], survey_df["Satisfaction"], normalize="index")
print("\n   Row-normalised contingency table (% within category):")
print(ct.round(3).to_string())

# ─────────────────────────────────────────────────────────────────────────────
# 11. CORRELATION — Pearson and Spearman
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("11. Correlation — Pearson (linear) vs Spearman (rank-based):")
print("    Pearson: requires normality + linear relationship")
print("    Spearman: no normality assumption, monotonic relationship")
df_corr = pd.DataFrame({
    "age":     np.random.randint(25, 65, 100),
    "salary":  np.random.normal(55000, 15000, 100),
    "tenure":  np.random.randint(0, 30, 100),
    "perf":    np.random.uniform(60, 100, 100),
})
df_corr["salary"] += df_corr["tenure"] * 1500   # Tenure increases salary
print("\n   Pearson (linear) correlations with salary:")
bl.diagnostic.correlation(df_corr, method="pearson", target="salary")
print("\n   Spearman (rank) correlations with salary:")
bl.diagnostic.correlation(df_corr, method="spearman", target="salary")

# ─────────────────────────────────────────────────────────────────────────────
# 12. Test selection guide
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("12. Statistical Test Selection Guide:")
print("""
  ┌────────────────────────────────────────────────────────────────────────────┐
  │  Comparison type          │  Normally distributed?  │  Test to use        │
  ├────────────────────────────────────────────────────────────────────────────┤
  │  1 group vs known mean    │  YES (n<30)              │  One-sample t-test  │
  │  1 group vs known mean    │  YES (n≥30)              │  Z-test             │
  │  2 independent groups     │  YES, equal variances    │  Student's t-test   │
  │  2 independent groups     │  YES, unequal variances  │  Welch's t-test     │
  │  2 independent groups     │  NO                      │  Mann-Whitney U     │
  │  2 related groups (pairs) │  YES                     │  Paired t-test      │
  │  2 related groups (pairs) │  NO                      │  Wilcoxon signed-rank│
  │  3+ independent groups    │  YES                     │  One-way ANOVA      │
  │  3+ independent groups    │  NO                      │  Kruskal-Wallis     │
  │  2 factors + interaction  │  YES                     │  Two-way ANOVA      │
  │  2 categorical variables  │  N/A                     │  Chi-square         │
  │  2 continuous variables   │  YES, linear             │  Pearson r          │
  │  2 continuous variables   │  NO / monotonic          │  Spearman ρ         │
  └────────────────────────────────────────────────────────────────────────────┘

  Rules to remember:
  ──────────────────
  1. ALWAYS check normality BEFORE picking a parametric test (Shapiro-Wilk)
  2. For large samples (n ≥ 30), the central limit theorem applies — parametric
     tests are generally robust to moderate non-normality
  3. Use Welch's t-test by default for two independent groups (safer than Student's)
  4. For paired data, NEVER use an independent t-test — you'll lose statistical power
  5. Effect sizes matter more than p-values for practical significance

  Effect size guide:
  ──────────────────
  Cohen's d (t-tests):      small=0.2,  medium=0.5,  large=0.8
  Eta squared η² (ANOVA):   small=0.01, medium=0.06, large=0.14
  Rank-biserial r (M-W, KW):small=0.1,  medium=0.3,  large=0.5
  Cramér's V (chi-square):  small=0.1,  medium=0.3,  large=0.5
""")

print("✅ Example 11 complete — Statistical Hypothesis Testing")
