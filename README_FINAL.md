# BizLens v2.2.1

**Integrated Analytics Platform — Descriptive · Diagnostic · Predictive · Prescriptive · Simulation**

[![PyPI version](https://img.shields.io/pypi/v/bizlens)](https://pypi.org/project/bizlens/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-solutiongate--learn%2Fbizlens-181717?logo=github)](https://github.com/solutiongate-learn/bizlens)

---

## What is BizLens?

BizLens is a **full-stack analytics platform** covering every tier of the analytics pyramid in a single `pip install`. It is designed for business students, academics, data analysts, and practitioners who want a clean, educational Python interface that makes statistical reasoning explicit.

```
🎯 Prescriptive  → What should we do?     (prescriptive, optimize, simulate)
🔮 Predictive    → What will happen?       (predict, simulate)
🔍 Diagnostic    → Why did it happen?      (diagnostic, tables)
📊 Descriptive   → What happened?          (describe, tables, quality)
```

**Core educational principle:** Sample vs Population distinction (`ddof=1` vs `ddof=0`) is explicit in every calculation with formulas, interpretation, and visual explanation.

---

## Installation

```bash
# Standard install (core analytics)
pip install bizlens

# With text analytics (word cloud, sentiment)
pip install "bizlens[text]"

# With advanced optimisation (Pyomo, CVXPY)
pip install "bizlens[optimization]"

# With dataset sources (Kaggle, OpenML, World Bank)
pip install "bizlens[kaggle,openml,worldbank]"

# Full install (everything)
pip install "bizlens[full]"
```

---

## Quick Start

```python
import bizlens as bl

# Load a built-in dataset (with automatic citation)
df = bl.load_dataset("tips", show_citation=True)

# --- Descriptive Analytics ---
bl.describe(df["total_bill"], calculation_level="sample")   # n-1 Bessel-corrected
bl.compare_sample_population(df["total_bill"])              # Side-by-side comparison

# --- Diagnostic Analytics ---
bl.diagnostic.ttest(df[df["time"]=="Lunch"]["total_bill"],
                    df[df["time"]=="Dinner"]["total_bill"])
bl.diagnostic.anova(*[df[df["day"]==d]["tip"].values for d in df["day"].unique()])
bl.diagnostic.chi_square(df, col1="smoker", col2="day")
bl.tables.correlation_matrix(df, method="pearson")

# --- Predictive Analytics ---
bl.predict.linear_regression(x=df["total_bill"], y=df["tip"], confidence=0.95)
bl.predict.multiple_regression(X=df[["total_bill","size"]], y=df["tip"])
bl.predict.decision_tree(X=df[["total_bill","size"]], y=(df["smoker"]=="Yes").astype(int),
                         task="classification")

# --- Prescriptive Analytics (Linear Programming) ---
bl.prescriptive.lp(
    objective=[5, 4],
    constraints=[[6, 4], [1, 2]],
    rhs=[24, 6],
    variable_names=["ProductA", "ProductB"],
    maximize=True,
)

# --- Monte Carlo Simulation ---
bl.simulate.run(
    model_fn=lambda revenue, cost: revenue - cost,
    n_trials=10_000,
    inputs={
        "revenue": {"dist": "triangular", "low": 80, "mode": 100, "high": 130},
        "cost":    {"dist": "normal",     "mean": 60, "std": 10},
    }
)
```

---

## Full API Reference

### 📊 Descriptive Analytics

```python
import bizlens as bl

# Single-column descriptive statistics
stats = bl.describe(data["column"], calculation_level="sample")   # or "population"
stats = bl.describe(data["column"], calculation_level="population", show_formula=True)

# Compare sample vs population side-by-side
bl.compare_sample_population(data["column"])

# Context manager — auto-describe a DataFrame on exit
with bl.BizDesc(df[["col1","col2"]], calculation_level="sample") as bd:
    df_clean = df.dropna()
```

---

### 🗂️ Statistical Tables

```python
# Frequency distribution (numeric bins or categorical counts)
bl.tables.frequency(df, column="total_bill", bins=10)
bl.tables.frequency(df, column="day")

# Side-by-side descriptive stats for multiple columns
bl.tables.descriptive_comparison(df, columns=["col1","col2","col3"],
                                  calculation_level="sample")

# Cross-tabulation with chi-square test
bl.tables.crosstab(df, row_col="smoker", col_col="day",
                   normalize=None)                   # or 'index','columns','all'

# Correlation matrix with significance stars (*, **, ***)
bl.tables.correlation_matrix(df, method="pearson")  # or "spearman","kendall"

# Group comparison with ANOVA
bl.tables.group_comparison(df, group_col="smoker", value_col="tip")

# Percentile / quantile table with z-scores and IQR outlier flags
bl.tables.percentile_table(df, column="total_bill",
                            percentiles=[1,5,10,25,50,75,90,95,99])

# Fit distributions and rank by AIC
bl.tables.distribution_fit(df, column="total_bill",
                            distributions=["norm","lognorm","gamma","weibull_min"])
```

---

### 🔍 Diagnostic Analytics

```python
# Normality test (Shapiro-Wilk)
bl.diagnostic.normality_test(data["column"], alpha=0.05)

# Two-sample t-test
bl.diagnostic.ttest(group1, group2, alternative="two-sided", alpha=0.05)
# alternative: "two-sided" | "less" | "greater"

# One-way ANOVA (accepts any number of groups)
bl.diagnostic.anova(*[group1, group2, group3], alpha=0.05)

# Chi-square test of independence
bl.diagnostic.chi_square(df, col1="smoker", col2="day", alpha=0.05)

# Correlation analysis (all numeric columns vs optional target)
bl.diagnostic.correlation(df, method="pearson", target="tip")
```

---

### 🔮 Predictive Analytics

```python
# Simple linear regression (OLS with CI and residual plots)
bl.predict.linear_regression(x=df["total_bill"], y=df["tip"],
                              calculation_level="sample", confidence=0.95)

# Multiple regression (with 5-fold cross-validation)
bl.predict.multiple_regression(X=df[["total_bill","size"]], y=df["tip"],
                                calculation_level="sample")

# Logistic regression (binary classification with AUC curve)
bl.predict.logistic_regression(X=X_features, y=y_binary, threshold=0.5)

# Decision tree — classification or regression
bl.predict.decision_tree(X=X_features, y=y_target,
                         task="classification",     # or "regression"
                         max_depth=4,
                         feature_names=["col1","col2"],
                         class_names=["Class0","Class1"])

# Confusion matrix visualisation
bl.predict.confusion_matrix_plot(y_true=y_actual, y_pred=y_predicted,
                                  labels=["Negative","Positive"],
                                  title="Model Confusion Matrix")
```

---

### 🎯 Optimization (Core LP)

```python
# Linear Programming via PuLP (maximise or minimise)
prob, result = bl.optimize.linear_program(
    objective=[5, 4],
    constraints=[[6, 4], [1, 2]],
    rhs=[24, 6],
    variable_names=["ProductA", "ProductB"],
    maximize=True,
)
```

---

### 🎯 Prescriptive Analytics (Operations Research)

```python
# Linear Programming with shadow prices + feasibility plot
bl.prescriptive.lp(
    objective=[5, 4],
    constraints=[[6, 4], [1, 2]],
    rhs=[24, 6],
    variable_names=["ProductA", "ProductB"],
    constraint_types=["<=", "<="],
    maximize=True,
)

# Mixed-Integer Linear Programming (MILP) — e.g. knapsack/project selection
bl.prescriptive.integer_lp(
    objective=[120, 310, 85, 60, 180],        # NPV of each project
    constraints=[[150, 400, 120, 80, 220]],    # Cost
    rhs=[500],                                  # Budget
    binary_vars=["CRM","Factory","RnD","Marketing","ERP"],
    variable_names=["CRM","Factory","RnD","Marketing","ERP"],
    maximize=True,
)

# Transportation problem (minimise total shipping cost)
bl.prescriptive.transportation(
    supply=[300, 400, 500],
    demand=[250, 350, 400, 200],
    costs=[[2,3,1,5],[4,1,3,2],[3,5,2,4]],
    supply_names=["Warehouse A","Warehouse B","Warehouse C"],
    demand_names=["Store 1","Store 2","Store 3","Store 4"],
)

# Assignment problem — Hungarian algorithm
bl.prescriptive.assignment(
    cost_matrix=[[15,18,20,25],[20,12,22,18],[25,20,10,15],[18,25,15,12]],
    agent_names=["Alice","Bob","Carol","Dave"],
    task_names=["Alpha","Beta","Gamma","Delta"],
    maximize=False,
)

# Sensitivity / what-if analysis
bl.prescriptive.sensitivity(
    objective=[5, 4], constraints=[[6,4],[1,2]], rhs=[24, 6],
    param="rhs", param_idx=0, delta_range=(10, 40),
)

# OR ecosystem overview
bl.prescriptive.packages()
```

---

### 🎲 Monte Carlo Simulation

```python
# Generic Monte Carlo engine — any model function
result = bl.simulate.run(
    model_fn=lambda revenue, cost, fixed: revenue - cost - fixed,
    n_trials=10_000,
    inputs={
        "revenue": {"dist": "triangular", "low": 80,  "mode": 100, "high": 130},
        "cost":    {"dist": "normal",     "mean": 60,  "std": 10},
        "fixed":   {"dist": "fixed",      "value": 20},
    }
)
# Returns: mean, std, P5–P95, P(>0)%, S-curve plot

# Distributions supported:
# normal, uniform, triangular, lognormal, poisson,
# binomial, exponential, beta, fixed

# NPV simulation — project investment under uncertainty
bl.simulate.npv(
    cash_flows_dist=[
        {"dist": "fixed",      "value": -1_000_000},            # Year 0: investment
        {"dist": "triangular", "low": 150_000, "mode": 250_000, "high": 350_000},
        {"dist": "normal",     "mean": 300_000, "std": 60_000},
        {"dist": "normal",     "mean": 350_000, "std": 70_000},
    ],
    discount_rate_dist={"dist": "normal", "mean": 0.10, "std": 0.02},
    n_trials=10_000,
)

# Bootstrap confidence intervals for any statistic
bl.simulate.bootstrap(data=df, column="spend",
                       statistic=np.mean, n_trials=10_000, confidence=0.95)

# Risk register simulation — probability × impact + tornado chart
bl.simulate.risk_matrix([
    {"name": "Supplier delay",
     "probability": 0.40,
     "impact": {"dist": "triangular", "low": 20_000, "mode": 50_000, "high": 120_000}},
    {"name": "Regulatory fine",
     "probability": 0.10,
     "impact": {"dist": "uniform", "low": 50_000, "high": 300_000}},
], n_trials=10_000)
```

---

### 🏭 Quality Analytics & Six Sigma

```python
# Process capability (Cp, Cpk, Pp, Ppk, sigma level, DPMO, yield)
bl.quality.process_capability(
    data=df, column="diameter",
    lsl=9.95, usl=10.05, target=10.0,
)

# Statistical Process Control charts
bl.quality.control_chart(df, column="diameter",
                          chart_type="xbar",    # "xbar" | "r" | "s" | "imr" | "p" | "c"
                          subgroup_size=5)

# Pareto chart — 80/20 defect analysis
bl.quality.pareto(df, category_col="defect_type")
bl.quality.pareto(df, category_col="defect_type", value_col="cost_usd")

# Cause-and-effect (Ishikawa / Fishbone) diagram
bl.quality.fishbone(
    categories={
        "Machine":   ["Worn tooling", "Poor calibration"],
        "Method":    ["No SOP", "Inconsistent process"],
        "Material":  ["Wrong grade", "Moisture content"],
        "Man":       ["Fatigue", "Insufficient training"],
        "Measurement": ["Wrong gauge", "Human error"],
        "Environment": ["Temperature", "Humidity"],
    },
    effect="High Defect Rate",
)
```

---

### 📅 Project Management

```python
# Gantt chart (accepts date strings or numeric day numbers)
bl.project.gantt([
    {"task": "Design",    "start": "2024-01-01", "end": "2024-01-10",
     "resource": "Alice", "progress": 100},
    {"task": "Dev",       "start": "2024-01-08", "end": "2024-01-25",
     "resource": "Bob",   "progress": 60},
    {"task": "Testing",   "start": "2024-01-22", "end": "2024-02-01",
     "resource": "Alice", "progress": 0},
], title="Project Schedule")

# CPM Network diagram with critical path
bl.project.network(
    tasks=[
        {"id":"A","name":"Research","duration":5},
        {"id":"B","name":"Design","duration":8},
        {"id":"C","name":"Build","duration":6},
        {"id":"D","name":"Test","duration":4},
    ],
    dependencies={"A":[],"B":["A"],"C":["B"],"D":["C"]},
)
# Returns: critical_path, project_duration, ES/EF/LS/LF/slack per task

# PERT analysis — uncertainty-based project duration
bl.project.pert([
    {"id":"A","name":"Foundation",   "optimistic":8, "likely":10,"pessimistic":15},
    {"id":"B","name":"Framing",      "optimistic":12,"likely":15,"pessimistic":25},
    {"id":"C","name":"Inspection",   "optimistic":2, "likely":3, "pessimistic":5},
])
```

---

### 📝 Text Analytics

```python
# Word cloud (requires: pip install wordcloud)
bl.text.wordcloud(df, column="review", max_words=100, title="Customer Reviews")
bl.text.wordcloud("Any text string or list of strings")

# Word and n-gram frequency tables
bl.text.frequency(df, column="review", n=1, top_n=20)    # Unigrams
bl.text.frequency(df, column="review", n=2, top_n=15)    # Bigrams
bl.text.frequency(df, column="review", n=3, top_n=10)    # Trigrams

# Sentiment analysis (uses VADER → TextBlob → rule-based fallback)
bl.text.sentiment(df, column="review")
bl.text.sentiment(["Great product!", "Terrible quality.", "Average."])

# TF-IDF keyword extraction (requires scikit-learn)
bl.text.tfidf(df, column="review", top_n=15)
```

---

### 📦 Built-in Datasets

```python
# List all datasets
bl.list_datasets()

# Load with automatic APA + BibTeX citation
df = bl.load_dataset("iris",     show_citation=True)
df = bl.load_dataset("titanic",  show_citation=True)
df = bl.load_dataset("tips",     show_citation=True)
df = bl.load_dataset("penguins", show_citation=True)
df = bl.load_dataset("diamonds", show_citation=True)
df = bl.load_dataset("wine_quality",    show_citation=True)
df = bl.load_dataset("breast_cancer",   show_citation=True)
df = bl.load_dataset("boston_housing",  show_citation=True)
df = bl.load_dataset("flights",  show_citation=True)
df = bl.load_dataset("mpg",      show_citation=True)

# Dataset metadata
bl.dataset_info("titanic")

# OpenML — free, no credentials required
df = bl.load_from_openml(dataset_id=61)            # ID-based
df = bl.load_from_openml(dataset_name="credit-g")  # Name-based

# Kaggle — requires ~/.kaggle/kaggle.json token
df = bl.load_from_kaggle("username/dataset-name", file_name="data.csv")

# World Bank — live API (GDP, CPI, population, etc.)
df = bl.load_from_world_bank(
    indicator="NY.GDP.PCAP.CD",                    # GDP per capita
    countries=["US","CN","IN","DE","GB"],
    start_year=2015, end_year=2023,
)
```

---

### 🚀 Deployment

```python
# Generate a full Streamlit analytics dashboard
bl.deploy.streamlit_app(
    data=df,
    title="My Analytics Dashboard",
    save_path="dashboard.py",
    launch=False,            # Set True to launch browser immediately
)
# Launch: streamlit run dashboard.py

# Generate a Gradio ML demo
bl.deploy.gradio_app(
    data=df,
    title="Data Explorer",
    launch=False,
)

# Show all deployment platforms
bl.deploy.show_options()
```

---

### 🔍 Package Ecosystem Discovery

```python
# Browse 40+ curated analytics packages by category
bl.packages.ecosystem()                  # All categories
bl.packages.ecosystem(category="ml")     # Machine learning only
bl.packages.ecosystem(category="viz")    # Visualisation only

# Search by keyword
bl.packages.search("time series")
bl.packages.search("optimisation")
bl.packages.search("bayesian")

# Live PyPI search
bl.packages.search_pypi("forecasting")

# Check what's already installed
bl.packages.check_installed()
```

---

## Color Schemes

All visualisations support three built-in themes:

```python
bl.describe(data, color_scheme="academic")   # Blue/purple (default)
bl.describe(data, color_scheme="pastel")     # Soft pastels
bl.describe(data, color_scheme="vibrant")    # Bold colours
```

---

## Pandas & Polars Support

BizLens uses [narwhals](https://github.com/narwhals-dev/narwhals) to accept both Pandas and Polars DataFrames transparently:

```python
import pandas as pd
import polars as pl
import bizlens as bl

# Both work identically
df_pandas = pd.read_csv("data.csv")
df_polars  = pl.read_csv("data.csv")

bl.describe(df_pandas["column"])   # ✅
bl.describe(df_polars["column"])   # ✅
```

---

## Example Scripts

Ten fully self-contained example scripts are included in the `examples/` folder:

| File | Topic |
|---|---|
| `01_descriptive_analytics.py` | describe, compare_sample_population, frequency, percentile tables |
| `02_diagnostic_analytics.py` | t-test, ANOVA, chi-square, correlation, distribution fit |
| `03_predictive_analytics.py` | linear/multiple/logistic regression, decision tree, confusion matrix |
| `04_quality_six_sigma.py` | Cp/Cpk, control charts, Pareto, Fishbone |
| `05_project_management.py` | Gantt, CPM network, PERT |
| `06_text_analytics.py` | Word cloud, n-gram frequency, sentiment, TF-IDF |
| `07_monte_carlo_simulation.py` | Generic MC, NPV simulation, bootstrap CI, risk register |
| `08_prescriptive_analytics.py` | LP, MILP, transportation, assignment, sensitivity |
| `09_optimization_linear_programming.py` | Production planning, staff scheduling, portfolio selection |
| `10_datasets_and_deployment.py` | Datasets, Streamlit/Gradio deploy, package discovery |

---

## Dependencies

**Core (installed automatically):**
`numpy`, `pandas`, `polars`, `narwhals`, `scipy`, `matplotlib`, `seaborn`, `scikit-learn`, `statsmodels`, `PuLP`, `networkx`, `rich`

**Optional extras:**

| Extra | Packages | Install |
|---|---|---|
| `text` | wordcloud, vaderSentiment, textblob | `pip install "bizlens[text]"` |
| `optimization` | pyomo, cvxpy, gekko, pymoo | `pip install "bizlens[optimization]"` |
| `simulation` | simpy | `pip install "bizlens[simulation]"` |
| `kaggle` | kaggle | `pip install "bizlens[kaggle]"` |
| `openml` | openml | `pip install "bizlens[openml]"` |
| `worldbank` | wbgapi | `pip install "bizlens[worldbank]"` |
| `interactive` | plotly, altair, ipywidgets | `pip install "bizlens[interactive]"` |
| `full` | Everything above | `pip install "bizlens[full]"` |

---

## Who Is This For?

- **Students**: High school → undergraduate → postgraduate analytics curricula
- **Educators**: Ready-made examples, formula display, sample vs population pedagogy
- **Analysts**: Quick EDA, hypothesis testing, predictive modelling in minimal code
- **Operations teams**: Scheduling (Gantt/CPM/PERT), quality (Six Sigma), optimisation (LP/MILP)
- **Data scientists**: Consistent API over pandas + polars, bootstrap CI, distribution fitting
- **Business leaders**: Monte Carlo risk analysis, NPV simulation, prescriptive recommendations

---

## Roadmap

| Version | Status | Highlights |
|---|---|---|
| v2.0.0 | ✅ Released | Descriptive, diagnostic, predictive analytics |
| v2.1.0 | ✅ Released | Multiple regression, logistic, decision tree, confusion matrix, deployment |
| v2.2.0 | ✅ Released | Statistical tables, quality/Six Sigma, project management, text analytics, Monte Carlo, prescriptive analytics |
| v2.2.1 | ✅ **Current** | Corrected PyPI description and complete package metadata |
| v2.3.0 | 🗓 Planned | Time series (ARIMA/Prophet), clustering (K-means/DBSCAN), dimensionality reduction (PCA/t-SNE) |
| v2.4.0 | 🗓 Planned | Bayesian inference, A/B testing framework, causal inference (DoWhy) |
| v3.0.0 | 🗓 Planned | Deep learning integration, AutoML, natural language querying |

---

## License

MIT License — free for academic and commercial use.

## Author

**Sudhanshu Singh** — [GitHub: solutiongate-learn](https://github.com/solutiongate-learn)

## Links

- **PyPI**: https://pypi.org/project/bizlens/
- **GitHub**: https://github.com/solutiongate-learn/bizlens
- **Issues**: https://github.com/solutiongate-learn/bizlens/issues
