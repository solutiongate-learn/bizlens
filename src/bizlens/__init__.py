"""
BizLens v2.2.13 — Descriptive Analytics + Statistical Inference + Process Mining
Educational analytics package for business analysis, teaching, and data exploration.
"""

__version__ = "2.2.14"

# Global profiling flag (used by all modules)
ENABLE_PROFILING = False

def set_profiling(enabled: bool = True):
    """Enable/disable performance timing across all BizLens methods.
    Call bl.set_profiling(True) to see time duration for every cell run.
    """
    global ENABLE_PROFILING
    ENABLE_PROFILING = enabled
    from rich.console import Console
    console = Console()
    console.print(f"[bold green]🔍 Profiling {'ENABLED' if enabled else 'DISABLED'} — time durations will now appear[/bold green]")

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
from .deploy import deploy, packages

__all__ = [
    "describe", "BizDesc", "set_profiling",
    "tables", "diagnostic", "quality", "inference",
    "process_mining",
    "load_dataset", "list_datasets",
    "generate_sample_data", "generate_event_log",
    "generate_hr_onboarding_event_log",
    "generate_healthcare_event_log",
    "generate_manufacturing_event_log",
    "generate_tech_support_event_log",
    "load_event_log_from_csv",
    "deploy", "packages",
]