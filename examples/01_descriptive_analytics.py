"""
BizLens — Example 01: Descriptive Analytics
============================================
Topics covered
--------------
• Auto-install: works in Google Colab, VSCode, Jupyter, or plain terminal
• describe()                      — Full stats with sample vs population
• compare_sample_population()     — Side-by-side n-1 vs n comparison
• BizDesc context manager         — Auto-describe any DataFrame on exit
• tables.descriptive_comparison() — Multi-column side-by-side table
• tables.frequency()              — Frequency distribution (numeric + categorical)
• tables.percentile_table()       — Percentile / quantile table with z-scores
• tables.distribution_fit()       — Which distribution best fits your data?

Works with both Pandas and Polars DataFrames (narwhals under the hood).

Run anywhere
------------
  Google Colab : paste into a code cell and run
  VSCode       : python 01_descriptive_analytics.py
  Jupyter      : %run 01_descriptive_analytics.py  (or paste cells)
  Terminal     : python 01_descriptive_analytics.py
"""

# ── Auto-install dependencies ─────────────────────────────────────────────────
import subprocess, sys

def _install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

for pkg, name in [("bizlens", "bizlens"), ("numpy", "numpy"),
                  ("pandas", "pandas"), ("matplotlib", "matplotlib"),
                  ("scipy", "scipy"), ("rich", "rich")]:
    try:
        __import__(name)
    except ImportError:
        print(f"Installing {pkg}...")
        _install(pkg)

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # Safe for Colab / headless; remove to see pop-up windows
import matplotlib.pyplot as plt
import bizlens as bl

print(f"BizLens version: {bl.__version__}")

# ── 1. Load a built-in dataset ────────────────────────────────────────────────
print("\n" + "="*60)
print("1. Loading built-in 'tips' dataset:")
df = bl.load_dataset("tips", show_citation=True)
print(f"   Shape: {df.shape}")
print(df.head(3).to_string())

# ── 2. describe() — sample vs population ────────────────────────────────────
print("\n" + "="*60)
print("2. Sample statistics (ddof=1, Bessel's correction):")
sample_stats = bl.describe(df["total_bill"], calculation_level="sample",
                            show_formula=True)

print("\nPopulation statistics (ddof=0):")
pop_stats = bl.describe(df["total_bill"], calculation_level="population",
                         show_formula=True)

# ── 3. Why n-1? Visualise the difference ────────────────────────────────────
print("\n" + "="*60)
print("3. Why does n-1 matter? Compare Std Dev formulas:")
arr = df["total_bill"].values
n = len(arr)
std_sample = np.std(arr, ddof=1)
std_pop    = np.std(arr, ddof=0)
diff_pct   = (std_sample - std_pop) / std_pop * 100
print(f"   n = {n}")
print(f"   Population Std (ddof=0): {std_pop:.4f}")
print(f"   Sample Std     (ddof=1): {std_sample:.4f}")
print(f"   Difference: {diff_pct:.2f}%  ← Bessel's correction adds {diff_pct:.2f}%")
print("   Rule of thumb: use ddof=1 unless you have the ENTIRE population.")

# ── 4. compare_sample_population ────────────────────────────────────────────
print("\n" + "="*60)
print("4. Side-by-side comparison:")
comparison = bl.compare_sample_population(df["total_bill"])

# ── 5. BizDesc context manager ───────────────────────────────────────────────
print("\n" + "="*60)
print("5. BizDesc context manager (auto-describes on exit):")
numeric_cols = ["total_bill", "tip", "size"]
with bl.BizDesc(df[numeric_cols], calculation_level="sample") as bd:
    df_clean = df.dropna()
    print(f"   Rows after dropna: {len(df_clean)}")
# Summary prints automatically on exit

# ── 6. tables.descriptive_comparison ─────────────────────────────────────────
print("\n" + "="*60)
print("6. Multi-column descriptive comparison (sample, ddof=1):")
comp_tbl = bl.tables.descriptive_comparison(
    df, columns=["total_bill", "tip", "size"], calculation_level="sample"
)

# ── 7. Frequency — numeric with custom bins ───────────────────────────────────
print("\n" + "="*60)
print("7. Frequency distribution — total_bill (10 bins):")
freq_num = bl.tables.frequency(df, column="total_bill", bins=10, show_plot=True)
print(freq_num.to_string())

print("\nFrequency distribution — day (categorical):")
freq_cat = bl.tables.frequency(df, column="day", show_plot=True)
print(freq_cat.to_string())

# ── 8. Percentile table ───────────────────────────────────────────────────────
print("\n" + "="*60)
print("8. Percentile table with z-scores and outlier flags — total_bill:")
pct_tbl = bl.tables.percentile_table(
    df, column="total_bill",
    percentiles=[1, 5, 10, 25, 50, 75, 90, 95, 99]
)
print(pct_tbl.to_string())

# ── 9. Distribution fit ───────────────────────────────────────────────────────
print("\n" + "="*60)
print("9. Which distribution best fits total_bill? (ranked by AIC):")
dist_fit = bl.tables.distribution_fit(
    df, column="total_bill",
    distributions=["norm", "lognorm", "gamma", "expon", "weibull_min"],
    show_plot=True
)
print(f"   Best fit: {dist_fit.iloc[0]['Distribution']}  (AIC={dist_fit.iloc[0]['AIC']})")

# ── 10. Multiple datasets ─────────────────────────────────────────────────────
print("\n" + "="*60)
print("10. Comparing stats across multiple datasets:")
for name in ["iris", "penguins", "tips"]:
    d = bl.load_dataset(name, show_citation=False)
    numeric = d.select_dtypes(include="number")
    means   = numeric.mean().round(3).to_dict()
    print(f"   {name:10s} | {len(d)} rows | means: {means}")

# ── 11. Polars support ────────────────────────────────────────────────────────
print("\n" + "="*60)
try:
    import polars as pl
    df_polars = pl.from_pandas(df)
    print("11. Same API with Polars DataFrame:")
    bl.describe(df_polars["total_bill"], calculation_level="sample")
    print("   ✅ Polars supported via narwhals")
except ImportError:
    print("11. (Polars not installed — skipping. Install with: pip install polars)")

print("\n" + "="*60)
print("✅ Example 01 complete — Descriptive Analytics")
