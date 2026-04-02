"""
BizLens v2.2.11 Example 1: Descriptive Analytics with Tables & Diagnostics
===========================================================================
Self-Contained: YES (auto-install, all imports, data generation)
Environments: Colab, VSCode, Terminal, Jupyter

Demonstrates:
- Statistical tables (frequency, percentile, summary)
- Descriptive analytics with smart data summarization
- Outlier detection and normality testing
- Correlation analysis
- Data quality assessment and profiling
- Professional visualizations

Run anywhere:
  Google Colab : paste into code cell
  VSCode/Terminal : python 01_descriptive_analytics.py
  Jupyter : %run 01_descriptive_analytics.py
"""

# ════════════════════════════════════════════════════════════════════════════
# STEP 1: AUTO-INSTALL & ENVIRONMENT SETUP
# ════════════════════════════════════════════════════════════════════════════

import subprocess
import sys

try:
    import bizlens as bl
except ImportError:
    print("Installing BizLens v2.2.11...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "bizlens==2.2.11", "-q"])
    import bizlens as bl

# Setup matplotlib for Colab/headless
import matplotlib
matplotlib.use("Agg")

# ════════════════════════════════════════════════════════════════════════════
# STEP 2: IMPORTS
# ════════════════════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"\n{'='*70}")
print(f"BizLens v{bl.__version__} — Descriptive Analytics Example")
print(f"{'='*70}")

# ════════════════════════════════════════════════════════════════════════════
# STEP 3: GENERATE SAMPLE DATA
# ════════════════════════════════════════════════════════════════════════════

print("\n[Step 1/5] Generating sample business data...")

np.random.seed(42)
n_records = 500

data = pd.DataFrame({
    'region': np.random.choice(['North', 'South', 'East', 'West'], n_records),
    'product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], n_records),
    'revenue': np.random.gamma(shape=2, scale=5000, size=n_records),
    'quantity': np.random.poisson(lam=10, size=n_records),
    'customer_satisfaction': np.random.normal(loc=7.5, scale=1.5, size=n_records).clip(1, 10),
    'days_to_delivery': np.random.exponential(scale=3, size=n_records) + 1,
})

print(f"✓ Generated {len(data)} records with {len(data.columns)} columns")
print(f"  Columns: {', '.join(data.columns.tolist())}")

# ════════════════════════════════════════════════════════════════════════════
# STEP 4: DESCRIPTIVE ANALYTICS
# ════════════════════════════════════════════════════════════════════════════

print("\n[Step 2/5] Running descriptive analytics...")
bl.describe(data)

# ════════════════════════════════════════════════════════════════════════════
# STEP 5: FREQUENCY TABLES
# ════════════════════════════════════════════════════════════════════════════

print("\n[Step 3/5] Creating statistical tables...")

print("\n" + "─" * 70)
print("FREQUENCY TABLE: Product Distribution")
print("─" * 70)
bl.tables.frequency_table(data['product'])

print("\n" + "─" * 70)
print("FREQUENCY TABLE: Regional Distribution")
print("─" * 70)
bl.tables.frequency_table(data['region'])

# ════════════════════════════════════════════════════════════════════════════
# STEP 6: PERCENTILE ANALYSIS
# ════════════════════════════════════════════════════════════════════════════

print("\n" + "─" * 70)
print("PERCENTILE ANALYSIS: Revenue Distribution")
print("─" * 70)
bl.tables.percentile_table(data['revenue'])

# ════════════════════════════════════════════════════════════════════════════
# STEP 7: SUMMARY STATISTICS
# ════════════════════════════════════════════════════════════════════════════

print("\n" + "─" * 70)
print("SUMMARY STATISTICS: All Numeric Columns")
print("─" * 70)
bl.tables.summary_statistics(data)

# ════════════════════════════════════════════════════════════════════════════
# STEP 8: DIAGNOSTIC ANALYTICS
# ════════════════════════════════════════════════════════════════════════════

print("\n[Step 4/5] Diagnostic analytics and data quality checks...")

print("\n" + "─" * 70)
print("OUTLIER DETECTION: Revenue (IQR Method)")
print("─" * 70)
outlier_indices, outlier_table = bl.diagnostic.detect_outliers(data['revenue'], method='iqr')
print(outlier_table)

print("\n" + "─" * 70)
print("NORMALITY TESTS: Revenue")
print("─" * 70)
normality_results = bl.diagnostic.normality_test(data['revenue'])

print("\n" + "─" * 70)
print("CORRELATION ANALYSIS")
print("─" * 70)
numeric_cols = data.select_dtypes(include=[np.number]).columns
numeric_data = data[numeric_cols]
correlation_table, corr_matrix = bl.diagnostic.correlation_analysis(numeric_data)

# ════════════════════════════════════════════════════════════════════════════
# STEP 9: DATA QUALITY ASSESSMENT
# ════════════════════════════════════════════════════════════════════════════

print("\n[Step 5/5] Data quality assessment...")

print("\n" + "─" * 70)
print("DATA QUALITY PROFILE")
print("─" * 70)
quality_score = bl.quality.data_profile(data)

# ════════════════════════════════════════════════════════════════════════════
# STEP 10: VISUALIZATIONS
# ════════════════════════════════════════════════════════════════════════════

print("\n[Bonus] Creating visualizations...")

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

axes[0, 0].hist(data['revenue'], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
axes[0, 0].set_title('Revenue Distribution')
axes[0, 0].set_xlabel('Revenue ($)')
axes[0, 0].set_ylabel('Frequency')

data['region'].value_counts().plot(kind='bar', ax=axes[0, 1], color='coral')
axes[0, 1].set_title('Orders by Region')
axes[0, 1].tick_params(axis='x', rotation=45)

data['product'].value_counts().plot(kind='barh', ax=axes[0, 2], color='lightgreen')
axes[0, 2].set_title('Orders by Product')

axes[1, 0].scatter(data['revenue'], data['customer_satisfaction'], alpha=0.5, color='purple', s=50)
axes[1, 0].set_title('Revenue vs Satisfaction')
axes[1, 0].set_xlabel('Revenue ($)')
axes[1, 0].set_ylabel('Satisfaction (1-10)')

axes[1, 1].hist(data['days_to_delivery'], bins=30, color='goldenrod', edgecolor='black', alpha=0.7)
axes[1, 1].set_title('Days to Delivery')
axes[1, 1].set_xlabel('Days')

axes[1, 2].text(0.5, 0.7, f"Quality Score", ha='center', va='center',
                fontsize=14, fontweight='bold', transform=axes[1, 2].transAxes)
axes[1, 2].text(0.5, 0.4, f"{quality_score['overall_score']:.1f}/100", ha='center', va='center',
                fontsize=48, fontweight='bold', color='darkgreen', transform=axes[1, 2].transAxes)
axes[1, 2].axis('off')

plt.tight_layout()
plt.savefig('descriptive_analytics_visualization.png', dpi=100, bbox_inches='tight')
print("✓ Visualization saved to: descriptive_analytics_visualization.png")
plt.close()

# ════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("✓ EXAMPLE 1 COMPLETE — Descriptive Analytics")
print("=" * 70)
print("\nKey Topics Covered:")
print("  ✓ Frequency tables for categorical data")
print("  ✓ Percentile analysis for distributions")
print("  ✓ Summary statistics (count, mean, std, quartiles)")
print("  ✓ Outlier detection using IQR method")
print("  ✓ Normality testing (Shapiro-Wilk, Anderson-Darling, KS)")
print("  ✓ Correlation analysis with heatmaps")
print("  ✓ Data quality assessment and profiling")
print("  ✓ Professional visualizations")
print("\n" + "=" * 70)
