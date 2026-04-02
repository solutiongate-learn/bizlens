"""
BizLens v2.2.4 — Integrated Analytics Platform
Descriptive · Diagnostic · Predictive · Forecasting · Optimization · Quality · Project · Text

Version: 2.2.4
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
    forecast,
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

__version__ = "2.2.4"
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
    # Forecasting
    "forecast",
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