"""
BizLens v2.3.2
"""

__version__ = "2.3.2"

ENABLE_PROFILING = False

def set_profiling(enabled: bool = True):
    global ENABLE_PROFILING
    ENABLE_PROFILING = enabled
    from rich.console import Console
    console = Console()
    console.print(f"[bold green]🔍 Profiling {'ENABLED' if enabled else 'DISABLED'}[/bold green]")

from .utils import to_pandas
from .core import describe, BizDesc
from .tables import tables
from .diagnostic import diagnostic
from .inference import inference
from .process_mining import process_mining
from .quality import quality
from .datasets import load_dataset, list_datasets, generate_clean_ecommerce_data
from .preprocess import preprocess
from .eda import eda
from .deploy import deploy, packages

__all__ = [
    "__version__", "set_profiling", "to_pandas",
    "describe", "BizDesc",
    "tables", "diagnostic", "quality", "inference", "process_mining",
    "load_dataset", "list_datasets", "generate_clean_ecommerce_data",
    "preprocess", "eda",
    "deploy", "packages",
]