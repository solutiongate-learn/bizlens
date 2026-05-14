"""
BizLens - Integrated Analytics Platform
Version 2.3.4
"""

__version__ = "2.3.4"
__author__ = "Sudhanshu Singh"
__email__ = "sudhanshu@solutiongate.in"

ENABLE_PROFILING = False

def set_profiling(enabled: bool = True):
    global ENABLE_PROFILING
    ENABLE_PROFILING = enabled
    from rich.console import Console
    console = Console()
    status = "enabled" if enabled else "disabled"
    console.print(f"[bold green]BizLens profiling {status}[/bold green]")

from .core import describe, BizDesc
from . import tables, diagnostic, quality, inference, process_mining, eda, datasets, preprocess
from .datasets import load_dataset, list_datasets, generate_clean_ecommerce_data, generate_hr_onboarding_event_log, generate_healthcare_event_log

__all__ = ["__version__", "describe", "BizDesc", "tables", "diagnostic", "quality", "inference", "process_mining", "eda", "datasets", "preprocess", "load_dataset", "list_datasets", "set_profiling"]
