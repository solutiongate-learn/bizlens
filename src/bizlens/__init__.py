"""
BizLens v2.2.9 — Educational Descriptive Analytics Library
Focused on rich tables, visualizations, synthetic data generation, and teaching support.
"""

from .core import (
    describe,
    BizDesc,
    generate_sample_data,
    generate_event_log,
)

from .datasets import (
    load_dataset,
    list_datasets,
    dataset_info,
)

__version__ = "2.2.8"
__author__ = "Sudhanshu Singh"
__email__ = "cc9n8y8tqc@privaterelay.appleid.com"

__all__ = [
    "describe",
    "BizDesc",
    "generate_sample_data",
    "generate_event_log",
    "load_dataset",
    "list_datasets",
    "dataset_info",
]