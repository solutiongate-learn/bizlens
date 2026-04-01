"""
BizLens v2.0.0 — Integrated Analytics Platform
Descriptive, Diagnostic & Predictive Analytics with Sample vs Population Distinction

Features:
- Descriptive Analytics: Central Tendency, Dispersion, Distributions
- Diagnostic Analytics: Hypothesis Testing, Correlations, Assumptions
- Predictive Analytics: Regression, Forecasting, Confidence Intervals
- Sample vs Population: Explicit distinction (n-1 vs n) in all calculations
- Professional Visualizations: 9+ visualization types with distribution annotations
- Real Datasets: Integrated sample datasets with proper citations
- Educational Focus: From High School → Undergraduate → Postgraduate

Version: 2.0.0
License: MIT
"""

# Import from enhanced v0.6.0 core
from .core_v0_6_0_enhanced import (
    describe,
    BizDesc,
    load_dataset,
    list_sample_datasets,
    dataset_info,
)

# Import dataset utilities
from .datasets import (
    load_sample_dataset,
    list_available_datasets,
    describe_dataset,
    print_dataset_info,
    explore_datasets,
)

__version__ = "2.0.0"
__author__ = "Sudhanshu Singh"
__email__ = "cc9n8y8tqc@privaterelay.appleid.com"

__all__ = [
    # Core functions
    "describe",
    "BizDesc",
    "load_dataset",
    "list_sample_datasets",
    "dataset_info",
    # Dataset utilities
    "load_sample_dataset",
    "list_available_datasets",
    "describe_dataset",
    "print_dataset_info",
    "explore_datasets",
]
