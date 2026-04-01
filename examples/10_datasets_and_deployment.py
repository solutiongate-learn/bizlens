"""
BizLens — Example 10: Datasets, Deployment & Package Discovery
===============================================================
Covers:
  • load_dataset()         — Built-in datasets with citations
  • list_datasets()        — Browse all available datasets
  • load_from_openml()     — Free OpenML dataset repository
  • load_from_world_bank() — Live World Bank data
  • deploy.show_options()  — Deployment platform options
  • deploy.streamlit_app() — Generate a Streamlit dashboard
  • deploy.gradio_app()    — Generate a Gradio demo
  • packages.ecosystem()  — Full curated analytics package list
  • packages.search()     — Search for packages by keyword
  • packages.check_installed() — Check what's installed

Run:   python 10_datasets_and_deployment.py
"""

import bizlens as bl

# ──────────────────────────────────────────────────────────────────────────────
# 1. List all built-in datasets
# ──────────────────────────────────────────────────────────────────────────────
print("="*60)
print("1. Available built-in datasets:")
bl.list_datasets()

# ──────────────────────────────────────────────────────────────────────────────
# 2. Load datasets with automatic citation
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("2. Load Iris dataset (with APA + BibTeX citation):")
iris = bl.load_dataset("iris", show_citation=True)
print(f"   Shape: {iris.shape}")
print(iris.head(3))

print("\n" + "─"*40)
print("Titanic dataset:")
titanic = bl.load_dataset("titanic", show_citation=False)
print(f"   Shape: {titanic.shape}, Survival rate: {titanic['survived'].mean():.1%}")

print("\n" + "─"*40)
print("Tips dataset:")
tips = bl.load_dataset("tips", show_citation=False)
print(f"   Shape: {tips.shape}, Avg tip: ${tips['tip'].mean():.2f}")

# ──────────────────────────────────────────────────────────────────────────────
# 3. Dataset info
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("3. Dataset info — Titanic:")
bl.dataset_info("titanic")

# ──────────────────────────────────────────────────────────────────────────────
# 4. Run descriptive analytics on a built-in dataset
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("4. Quick analysis pipeline on Iris:")
print("\nDescriptive stats:")
bl.describe(iris["sepal_length"], calculation_level="sample")

print("\nDescriptive comparison — all numeric columns:")
bl.tables.descriptive_comparison(iris, calculation_level="sample")

print("\nCorrelation matrix:")
bl.tables.correlation_matrix(iris, columns=["sepal_length","sepal_width","petal_length","petal_width"])

# ──────────────────────────────────────────────────────────────────────────────
# 5. OpenML (free, no credentials needed)
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("5. Load from OpenML (free — no credentials required):")
try:
    # OpenML dataset ID 61 = Iris, 40945 = Titanic, 31 = Credit-g
    df_openml = bl.load_from_openml(dataset_id=61, dataset_name=None)
    print(f"   OpenML Iris: {df_openml.shape}")
    print(df_openml.head(3))
except Exception as e:
    print(f"   (OpenML requires: pip install openml) — {e}")

# ──────────────────────────────────────────────────────────────────────────────
# 6. World Bank live data
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("6. World Bank live data — GDP per capita (2015–2023):")
try:
    gdp = bl.load_from_world_bank(
        indicator="NY.GDP.PCAP.CD",    # GDP per capita (current USD)
        countries=["US", "CN", "IN", "DE", "GB"],
        start_year=2015,
        end_year=2023,
    )
    print(f"   Shape: {gdp.shape}")
    print(gdp.head())
except Exception as e:
    print(f"   (World Bank requires: pip install wbgapi or pandas_datareader) — {e}")

# ──────────────────────────────────────────────────────────────────────────────
# 7. Deploy — show all options
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("7. Deployment options:")
bl.deploy.show_options()

# ──────────────────────────────────────────────────────────────────────────────
# 8. Generate a Streamlit dashboard
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("8. Generate Streamlit dashboard code from the tips dataset:")
bl.deploy.streamlit_app(
    data=tips,
    title="Tips Analytics Dashboard",
    save_path="tips_dashboard.py",
    launch=False,    # Set True to launch immediately
)
print("   Generated: tips_dashboard.py")
print("   To launch: streamlit run tips_dashboard.py")

# ──────────────────────────────────────────────────────────────────────────────
# 9. Generate Gradio demo
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("9. Generate Gradio demo:")
bl.deploy.gradio_app(
    data=iris,
    title="Iris Dataset Explorer",
    launch=False,
)

# ──────────────────────────────────────────────────────────────────────────────
# 10. Package ecosystem discovery
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("10. Full analytics package ecosystem:")
bl.packages.ecosystem()

print("\n" + "─"*40)
print("Search for 'time series' packages:")
bl.packages.search("time series")

print("\n" + "─"*40)
print("Search for 'optimisation' packages:")
bl.packages.search("optimisation")

print("\n" + "─"*40)
print("Checking what's currently installed:")
bl.packages.check_installed()

# ──────────────────────────────────────────────────────────────────────────────
# 11. Live PyPI search
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("11. Live PyPI package search — 'forecasting':")
try:
    results = bl.packages.search_pypi("forecasting")
except Exception as e:
    print(f"   (Requires internet connection) — {e}")

print("\n✅ Example 10 complete.")
