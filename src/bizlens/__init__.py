"""
BizLens v2.2.10 — Descriptive Analytics + Process Mining Event Logs
"""

from .core import describe, BizDesc, generate_sample_data, generate_event_log
from .datasets import (
    load_dataset,
    list_datasets,
    generate_hr_onboarding_event_log,
    generate_healthcare_event_log,
    generate_manufacturing_event_log,
    generate_tech_support_event_log,
    load_event_log_from_csv,
)

__version__ = "2.2.9"

__all__ = [
    "describe", 
    "BizDesc",
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