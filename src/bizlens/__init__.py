"""
BizLens v2.2.0 — Integrated Analytics Platform
Descriptive · Diagnostic · Predictive · Optimization · Quality · Project · Text

Features:
- Descriptive Analytics: describe(), compare_sample_population(), BizDesc
- Diagnostic Analytics: diagnostic.ttest(), anova(), chi_square(), correlation()
- Predictive Analytics:
    predict.linear_regression()       — Simple regression with confidence intervals
    predict.multiple_regression()     — Multiple regression with cross-validation
    predict.logistic_regression()     — Binary classification with confusion matrix + AUC
    predict.decision_tree()           — Decision tree classifier/regressor
    predict.confusion_matrix_plot()   — Visualize confusion matrix
- Optimization: optimize.linear_program() via PuLP
- Statistical Tables:
    tables.frequency()                — Frequency distribution table
    tables.descriptive_comparison()   — Side-by-side stats for multiple columns
    tables.crosstab()                 — Cross-tabulation with chi-square test
    tables.correlation_matrix()       — Correlation matrix with significance stars
    tables.group_comparison()         — Descriptive stats by group + ANOVA
    tables.percentile_table()         — Percentile/quantile table with z-scores
    tables.distribution_fit()         — Fit & compare statistical distributions
- Quality / Six Sigma:
    quality.process_capability()      — Cp, Cpk, Pp, Ppk, sigma level, DPMO
    quality.control_chart()           — X-bar, R, S, P, C, U control charts
    quality.pareto()                  — Pareto chart for defect analysis
    quality.fishbone()                — Cause-and-effect (Ishikawa) diagram
- Project Management:
    project.gantt()                   — Gantt chart from task data
    project.network()                 — Network/CPM diagram with critical path
    project.pert()                    — PERT chart with slack/float analysis
- Text Analytics:
    text.wordcloud()                  — Word cloud visualization
    text.frequency()                  — Word/n-gram frequency analysis
    text.sentiment()                  — Sentiment analysis (VADER/TextBlob)
    text.tfidf()                      — TF-IDF keyword extraction
- Deployment:
    deploy.streamlit_app()            — Launch Streamlit dashboard
    deploy.gradio_app()               — Launch Gradio demo
    deploy.show_options()             — Show all deployment platforms
- Package Discovery:
    packages.ecosystem()              — Full curated analytics ecosystem
    packages.search()                 — Search by keyword
    packages.search_pypi()            — Live PyPI lookup
    packages.check_installed()        — Check what's installed
- Datasets:
    load_dataset()                    — Built-in datasets with citations
    load_from_kaggle()                — Download from Kaggle
    load_from_openml()                — Load from OpenML (free)
    load_from_world_bank()            — Live World Bank data
- Sample vs Population: Explicit n-1 vs n throughout all calculations

Version: 2.2.1
Author: Sudhanshu Singh
License: MIT
GitHub: https://github.com/solutiongate-learn/bizlens
"""

from .core import (
    describe,
    compare_sample_population,
    BizDesc,
    diagnostic,
    predict,
    optimize,
    tables,
    quality,
    project,
    text,
    simulate,
    prescriptive,
)

from .datasets import (
    load_dataset,
    list_datasets,
    dataset_info,
    load_from_kaggle,
    load_from_openml,
    load_from_world_bank,
)

from .deploy import deploy, packages

__version__ = "2.2.1"
__author__ = "Sudhanshu Singh"
__email__ = "cc9n8y8tqc@privaterelay.appleid.com"
__license__ = "MIT"
__url__ = "https://github.com/solutiongate-learn/bizlens"

__all__ = [
    # Descriptive
    "describe",
    "compare_sample_population",
    "BizDesc",
    # Diagnostic
    "diagnostic",
    # Predictive
    "predict",
    # Optimization
    "optimize",
    # Statistical Tables
    "tables",
    # Quality / Six Sigma
    "quality",
    # Project Management
    "project",
    # Text Analytics
    "text",
    # Monte Carlo Simulation
    "simulate",
    # Prescriptive Analytics / Operations Research
    "prescriptive",
    # Deployment
    "deploy",
    # Package ecosystem
    "packages",
    # Datasets
    "load_dataset",
    "list_datasets",
    "dataset_info",
    "load_from_kaggle",
    "load_from_openml",
    "load_from_world_bank",
]
