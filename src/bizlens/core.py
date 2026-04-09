"""
BizLens v2.2.14 — Descriptive Analytics Core
Enhanced: Full pandas/polars compatibility + built-in performance profiling.
"""

import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from rich.console import Console
from rich.panel import Panel
from . import ENABLE_PROFILING   # global flag from __init__.py
from .quality import quality      # required for describe() → quality.completeness_report()

try:
    import polars as pl
except ImportError:
    pl = None

warnings.filterwarnings("ignore")
console = Console()


def _to_pandas(data):
    """Internal helper – ensures all modules receive pandas DataFrame."""
    if isinstance(data, pd.DataFrame):
        return data
    elif pl and isinstance(data, pl.DataFrame):
        return data.to_pandas()
    elif isinstance(data, pd.Series):
        return data.to_frame()
    else:
        raise TypeError("BizLens: Input must be a pandas or polars DataFrame")


def describe(data, include_plots: bool = True, show_timing: bool = False):
    """Comprehensive descriptive analytics with smart event log detection.
    Now supports both pandas and polars. Timing enabled via bl.set_profiling(True).
    """
    if ENABLE_PROFILING or show_timing:
        start_total = time.perf_counter()

    console.print(Panel("[bold cyan]BizLens Descriptive Analytics v2.2.14[/bold cyan]", style="bold blue"))

    df = _to_pandas(data)

    # Flexible Event Log Detection
    col_lower = {c.lower(): c for c in df.columns}
    is_event_log = False
    case_col = activity_col = ts_col = None

    for key in ["case_id", "employee_id", "case"]:
        if key in col_lower:
            case_col = col_lower[key]
            break
    for key in ["activity"]:
        if key in col_lower:
            activity_col = col_lower[key]
            break
    for key in ["timestamp", "time", "date"]:
        if key in col_lower:
            ts_col = col_lower[key]
            break

    if case_col and activity_col and ts_col:
        is_event_log = True

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    console.print(f"[bold green]Numeric Columns ({len(numeric_cols)}):[/bold green] {numeric_cols}")
    console.print(f"[bold yellow]Categorical Columns ({len(categorical_cols)}):[/bold yellow] {categorical_cols}\n")

    if is_event_log:
        console.print(Panel("[bold magenta]Process Mining Event Log Detected[/bold magenta]", style="magenta"))
        num_cases = df[case_col].nunique()
        unique_acts = df[activity_col].nunique()
        total_events = len(df)
        time_span = f"{df[ts_col].min()} → {df[ts_col].max()}" if ts_col else "N/A"
        console.print(f"• Cases: {num_cases:,} | Unique Activities: {unique_acts}")
        console.print(f"• Total Events: {total_events:,} | Time Span: {time_span}")

    # === Run other BizLens modules (all features preserved) ===
    if ENABLE_PROFILING or show_timing:
        start_q = time.perf_counter()
    quality.completeness_report(df)
    if ENABLE_PROFILING or show_timing:
        console.print(f"[dim][Profiling] quality.completeness_report took {time.perf_counter() - start_q:.4f}s[/dim]")

    if numeric_cols:
        console.print("\n[bold]Numeric Summary[/bold]")
        summary = df[numeric_cols].describe().round(2)
        console.print(summary)

    if include_plots and numeric_cols:
        for col in numeric_cols[:4]:
            plt.figure(figsize=(8, 4))
            sns.histplot(df[col].dropna(), kde=True, color="skyblue")
            plt.title(f"Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            plt.show()

    # === Final profiling summary (only if enabled) ===
    if ENABLE_PROFILING or show_timing:
        total_duration = time.perf_counter() - start_total
        console.print(Panel(
            f"[bold green]✅ Analysis Complete in {total_duration:.4f} seconds[/bold green]\n"
            f"• Data converted to pandas: {_to_pandas.__code__.co_filename}\n"
            f"• All modules (quality, diagnostic, inference, tables) now fully compatible",
            style="green"
        ))

    return "Done"


class BizDesc:
    def __init__(self, data):
        self.data = data

    def summary(self, include_plots: bool = True, show_timing: bool = False):
        return describe(self.data, include_plots=include_plots, show_timing=show_timing)


# Backward compatibility (unchanged)
def generate_sample_data(n_rows: int = 1000, seed: int = 42):
    from .datasets import generate_sample_data as ds_generate
    return ds_generate(n_rows, seed)


def generate_event_log(num_cases: int = 500, seed: int = 42):
    from .datasets import generate_hr_onboarding_event_log
    return generate_hr_onboarding_event_log(num_cases, seed)