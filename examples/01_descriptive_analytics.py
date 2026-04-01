"""
BizLens — Example 01: Descriptive Analytics
============================================
Covers:
  • describe()                    — Full descriptive stats with sample vs population
  • compare_sample_population()   — Side-by-side comparison of n-1 vs n formulas
  • BizDesc context manager       — Auto-describe any DataFrame
  • tables.descriptive_comparison() — Multi-column side-by-side table
  • tables.frequency()            — Frequency distribution
  • tables.percentile_table()     — Percentile / quantile table

Works with both Pandas and Polars DataFrames.

Run:   python 01_descriptive_analytics.py
       pip install bizlens       (if not already installed)
"""

import numpy as np
import pandas as pd
import bizlens as bl

# ──────────────────────────────────────────────────────────────────────────────
# 1. Load a built-in dataset
# ──────────────────────────────────────────────────────────────────────────────
df = bl.load_dataset("tips", show_citation=True)
print(f"\nDataset shape: {df.shape}")
print(df.head())

# ──────────────────────────────────────────────────────────────────────────────
# 2. describe() — sample (n-1) vs population (n)
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("SAMPLE descriptive stats (ddof=1, Bessel's correction):")
sample_stats = bl.describe(df["total_bill"], calculation_level="sample", show_formula=True)

print("\nPOPULATION descriptive stats (ddof=0):")
pop_stats = bl.describe(df["total_bill"], calculation_level="population", show_formula=True)

# ──────────────────────────────────────────────────────────────────────────────
# 3. Compare sample vs population side-by-side
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("COMPARISON — sample vs population:")
comparison = bl.compare_sample_population(df["total_bill"])

# ──────────────────────────────────────────────────────────────────────────────
# 4. Describe a full DataFrame (multiple columns)
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("Multi-column descriptive stats:")
numeric_cols = ["total_bill", "tip", "size"]
for col in numeric_cols:
    bl.describe(df[col], label=col, calculation_level="sample")

# ──────────────────────────────────────────────────────────────────────────────
# 5. BizDesc context manager
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("BizDesc context manager (auto-describe on exit):")
with bl.BizDesc(df[numeric_cols], calculation_level="sample") as bd:
    # Inside context: run analysis, clean data, etc.
    df_clean = df.dropna()
    print(f"  Rows after dropna: {len(df_clean)}")
# On exit, BizDesc prints summary stats automatically

# ──────────────────────────────────────────────────────────────────────────────
# 6. tables.descriptive_comparison()
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("Side-by-side descriptive comparison (all numeric columns):")
comparison_tbl = bl.tables.descriptive_comparison(df, calculation_level="sample")

# ──────────────────────────────────────────────────────────────────────────────
# 7. tables.frequency() — numeric (binned) and categorical
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("Frequency distribution — total_bill (numeric, 10 bins):")
freq_num = bl.tables.frequency(df, column="total_bill", bins=10, show_plot=True)

print("\nFrequency distribution — day (categorical):")
freq_cat = bl.tables.frequency(df, column="day", show_plot=True)

# ──────────────────────────────────────────────────────────────────────────────
# 8. tables.percentile_table()
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("Percentile table — total_bill:")
pct_tbl = bl.tables.percentile_table(df, column="total_bill",
                                     percentiles=[1, 5, 10, 25, 50, 75, 90, 95, 99])

# ──────────────────────────────────────────────────────────────────────────────
# 9. Using Polars DataFrame (same API)
# ──────────────────────────────────────────────────────────────────────────────
try:
    import polars as pl
    df_polars = pl.from_pandas(df)
    print("\n" + "="*60)
    print("Same API with a Polars DataFrame:")
    bl.describe(df_polars["total_bill"], calculation_level="sample")
except ImportError:
    print("(Polars not installed — skipping polars demo)")

print("\n✅ Example 01 complete.")
