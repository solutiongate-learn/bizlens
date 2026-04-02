"""
BizLens — Example 10: Datasets, Deployment & Package Discovery
===============================================================
Topics covered
--------------
• load_dataset()         — Built-in datasets with APA + BibTeX citations
• list_datasets()        — Browse all available datasets
• dataset_info()         — Detailed metadata for any dataset
• load_from_openml()     — Free OpenML dataset repository (no credentials)
• load_from_world_bank() — Live World Bank development indicators
• deploy.show_options()  — Deployment platform overview
• deploy.streamlit_app() — Generate a Streamlit dashboard script
• deploy.gradio_app()    — Generate a Gradio demo script
• packages.ecosystem()   — Full curated analytics package list
• packages.search()      — Search packages by keyword
• packages.check_installed() — Audit what's installed

Run anywhere
------------
  Google Colab : paste into a code cell and run
  VSCode / Jupyter / Terminal : python 10_datasets_and_deployment.py
"""

# ── Auto-install ──────────────────────────────────────────────────────────────
import subprocess, sys

def _install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

for pkg in ["bizlens", "numpy", "pandas", "matplotlib", "scipy"]:
    try:
        __import__(pkg)
    except ImportError:
        print(f"Installing {pkg}...")
        _install(pkg)

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # Safe for Colab / headless; remove for pop-up windows
import matplotlib.pyplot as plt
import bizlens as bl

print(f"BizLens version: {bl.__version__}\n")

# ── 1. List all built-in datasets ────────────────────────────────────────────
print("="*60)
print("1. Available built-in datasets:")
bl.list_datasets()

# ── 2. Load datasets with automatic citation ──────────────────────────────────
print("\n" + "="*60)
print("2. Load datasets with automatic APA + BibTeX citations:")

iris = bl.load_dataset("iris", show_citation=True)
print(f"\n   Iris: {iris.shape}  |  Classes: {iris['species'].nunique()}")

titanic = bl.load_dataset("titanic", show_citation=False)
survived_pct = titanic["survived"].mean()
print(f"   Titanic: {titanic.shape}  |  Survival rate: {survived_pct:.1%}")

tips = bl.load_dataset("tips", show_citation=False)
print(f"   Tips: {tips.shape}  |  Avg tip: ${tips['tip'].mean():.2f}  |  Avg bill: ${tips['total_bill'].mean():.2f}")

print("\n   All three datasets loaded ✅")

# ── 3. Dataset metadata ───────────────────────────────────────────────────────
print("\n" + "="*60)
print("3. Dataset metadata — Titanic:")
bl.dataset_info("titanic")

# ── 4. Quick analytics pipeline on Iris ──────────────────────────────────────
print("\n" + "="*60)
print("4. Quick analytics pipeline on Iris dataset:")
numeric_cols = [c for c in iris.columns if iris[c].dtype in [float, int]
                and c != "target"]

print("\n   Descriptive stats (sample, ddof=1):")
bl.describe(iris["sepal_length"], calculation_level="sample")

print("\n   Multi-column comparison:")
bl.tables.descriptive_comparison(iris, columns=numeric_cols[:4],
                                  calculation_level="sample")

print("\n   Correlation matrix (* p<0.05  ** p<0.01  *** p<0.001):")
bl.tables.correlation_matrix(iris, columns=numeric_cols[:4],
                              method="pearson", show_plot=True)

print("\n   Group comparison — petal length by species:")
if "species" in iris.columns:
    bl.tables.group_comparison(iris, group_col="species",
                               value_col="petal_length", show_plot=True)

# ── 5. Quick survey across multiple datasets ──────────────────────────────────
print("\n" + "="*60)
print("5. Dataset survey — stats across all built-in datasets:")
for name in ["iris", "tips", "titanic", "penguins", "diamonds", "breast_cancer"]:
    try:
        d = bl.load_dataset(name, show_citation=False)
        numerics = d.select_dtypes(include="number")
        cats     = d.select_dtypes(include="object")
        print(f"   {name:15s}  rows={len(d):5d}  numeric={len(numerics.columns):2d}"
              f"  categorical={len(cats.columns):2d}"
              f"  missing={d.isnull().sum().sum():3d}")
    except Exception as e:
        print(f"   {name:15s}  (unavailable: {e})")

# ── 6. OpenML (free, no credentials) ─────────────────────────────────────────
print("\n" + "="*60)
print("6. Load from OpenML (no account required):")
print("   OpenML hosts 20,000+ datasets — ID 61=Iris, 40945=Titanic, 31=Credit-G")
try:
    import openml  # noqa: F401
except ImportError:
    print("   Installing openml...")
    try:
        _install("openml")
    except Exception:
        pass

try:
    df_openml = bl.load_from_openml(dataset_id=61, dataset_name=None)
    print(f"   OpenML Iris (id=61): shape={df_openml.shape}")
    print(df_openml.head(3).to_string())
except Exception as e:
    print(f"   OpenML requires internet + 'pip install openml': {e}")

# ── 7. World Bank live data ───────────────────────────────────────────────────
print("\n" + "="*60)
print("7. World Bank live data — GDP per capita, selected countries (2015–2023):")
print("   Indicator: NY.GDP.PCAP.CD (GDP per capita, current USD)")
try:
    gdp = bl.load_from_world_bank(
        indicator="NY.GDP.PCAP.CD",
        countries=["US", "CN", "IN", "DE", "GB"],
        start_year=2015,
        end_year=2023,
    )
    print(f"   Shape: {gdp.shape}")
    print(gdp.head(10).to_string())
except Exception as e:
    print(f"   World Bank requires internet + 'pip install wbgapi': {e}")

# ── 8. Deployment options overview ───────────────────────────────────────────
print("\n" + "="*60)
print("8. Deployment platform options:")
bl.deploy.show_options()

# ── 9. Generate Streamlit dashboard ──────────────────────────────────────────
print("\n" + "="*60)
print("9. Generate Streamlit dashboard — Tips dataset:")
import os, tempfile
streamlit_path = os.path.join(tempfile.gettempdir(), "tips_dashboard.py")
bl.deploy.streamlit_app(
    data=tips,
    title="Tips Analytics Dashboard",
    save_path=streamlit_path,
    launch=False,    # Set True to launch immediately (requires streamlit installed)
)
print(f"   Generated: tips_dashboard.py")
print(f"   To launch: pip install streamlit && streamlit run tips_dashboard.py")

# ── 10. Generate Gradio demo ──────────────────────────────────────────────────
print("\n" + "="*60)
print("10. Generate Gradio demo — Iris Explorer:")
bl.deploy.gradio_app(
    data=iris,
    title="Iris Dataset Explorer",
    launch=False,    # Set True to launch in browser (requires gradio installed)
)
print("   To launch: pip install gradio && run the generated script")

# ── 11. Package ecosystem discovery ──────────────────────────────────────────
print("\n" + "="*60)
print("11. Python analytics package ecosystem (curated):")
bl.packages.ecosystem()

print("\n   Search — 'time series':")
bl.packages.search("time series")

print("\n   Search — 'optimisation':")
bl.packages.search("optimisation")

print("\n   Search — 'deep learning':")
bl.packages.search("deep learning")

# ── 12. Check what's currently installed ─────────────────────────────────────
print("\n" + "="*60)
print("12. Check installed analytics packages:")
bl.packages.check_installed()

# ── 13. Live PyPI search ──────────────────────────────────────────────────────
print("\n" + "="*60)
print("13. Live PyPI package search:")
for keyword in ["forecasting", "causal inference", "AutoML"]:
    print(f"\n   Searching PyPI for '{keyword}':")
    try:
        results = bl.packages.search_pypi(keyword)
    except Exception as e:
        print(f"   (Requires internet connection: {e})")

# ── 14. Deployment decision guide ────────────────────────────────────────────
print("\n" + "="*60)
print("14. Deployment platform decision guide:")
print("""
  Platform         | Best for                         | Effort  | Cost
  ─────────────────────────────────────────────────────────────────────
  Streamlit        | Internal dashboards, data apps   | Low     | Free
  Gradio           | ML model demos, quick UIs        | Low     | Free
  Dash / Plotly    | Interactive web analytics        | Medium  | Free
  Flask / FastAPI  | REST API for analytics models    | Medium  | Free
  Hugging Face     | Public ML model demos            | Low     | Free
  Shiny for Python | R-style reactive apps            | Medium  | Free
  Docker           | Containerised, portable deploy   | Medium  | Free
  AWS / GCP / Azure| Production, scalable             | High    | Pay-as-go

  Quick start: Streamlit → 'pip install streamlit && streamlit run app.py'
  Share publicly: Deploy to Streamlit Cloud (free for public repos)
""")

print("✅ Example 10 complete — Datasets, Deployment & Package Discovery")
