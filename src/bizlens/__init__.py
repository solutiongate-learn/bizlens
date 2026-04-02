"""
BizLens v2.2.11 — Descriptive Analytics + Statistical Inference + Process Mining
Educational analytics package for business analysis, teaching, and data exploration.

Core Features:
- Descriptive analytics with smart event log detection
- Statistical tables (frequency, percentile, contingency)
- Diagnostic analytics (outliers, normality, correlations)
- Statistical inference (confidence intervals, hypothesis tests)
- Process mining (case metrics, variants, bottlenecks)
- Data quality assessment

For documentation: https://github.com/solutiongate-learn/bizlens
"""

from .core import describe, BizDesc, generate_sample_data, generate_event_log
from .tables import tables
from .diagnostic import diagnostic
from .inference import inference
from .process_mining import process_mining
from .quality import quality
from .datasets import (
    load_dataset,
    list_datasets,
    generate_hr_onboarding_event_log,
    generate_healthcare_event_log,
    generate_manufacturing_event_log,
    generate_tech_support_event_log,
    load_event_log_from_csv,
)

__version__ = "2.2.11"

__all__ = [
    # Core descriptive analytics
    "describe",
    "BizDesc",

    # Statistical tables and summaries
    "tables",

    # Diagnostic analytics and data quality
    "diagnostic",

    # Statistical inference and hypothesis testing
    "inference",

    # Process mining and event log analysis
    "process_mining",

    # Data quality assessment
    "quality",

    # Dataset utilities
    "load_dataset",
    "list_datasets",
    "generate_sample_data",
    "generate_event_log",
    "generate_hr_onboarding_event_log",
    "generate_healthcare_event_log",
    "generate_manufacturing_event_log",
    "generate_tech_support_event_log",
    "load_event_log_from_csv",
]