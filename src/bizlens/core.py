"""
BizLens v2.2.9 — Descriptive Analytics Core
Rich educational output + full support for process mining event logs with any extra columns.
"""

import warnings
import numpy as np
import pandas as pd
import polars as pl
import narwhals as nw
from narwhals.selectors import numeric, categorical
import matplotlib.pyplot as plt
import seaborn as sns
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime

warnings.filterwarnings("ignore")
console = Console()

# ─────────────────────────────────────────────────────────────────────────────
# MAIN DESCRIBE FUNCTION
# ─────────────────────────────────────────────────────────────────────────────
def describe(data, include_plots: bool = True, norm_compare: bool = False):
    """Comprehensive descriptive analytics with smart event log detection."""
    console.print(Panel("[bold cyan]BizLens Descriptive Analytics v2.2.9[/bold cyan]", style="bold blue"))

    # Convert to Polars for consistency
    if isinstance(data, pd.DataFrame):
        df = pl.from_pandas(data)
    elif isinstance(data, pl.DataFrame):
        df = data
    else:
        console.print("[red]Error: Please provide a pandas or polars DataFrame.[/red]")
        return None

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

    numeric_cols = _get_numeric_columns(df)
    categorical_cols = _get_categorical_columns(df)

    console.print(f"[bold green]Numeric Columns ({len(numeric_cols)}):[/bold green] {numeric_cols}")
    console.print(f"[bold yellow]Categorical Columns ({len(categorical_cols)}):[/bold yellow] {categorical_cols}\n")

    if is_event_log:
        console.print(Panel("[bold magenta]Process Mining Event Log Detected[/bold magenta]", style="magenta"))
        num_cases = df[case_col].n_unique() if case_col else 0
        unique_acts = df[activity_col].n_unique() if activity_col else 0
        total_events = len(df)
        time_span = f"{df[ts_col].min()} → {df[ts_col].max()}" if ts_col else "N/A"

        console.print(f"• Cases: {num_cases:,} | Unique Activities: {unique_acts}")
        console.print(f"• Total Events: {total_events:,} | Time Span: {time_span}")

        # Show summary of extra numeric attributes (cost, co2_impact, etc.)
        extra_numeric = [c for c in numeric_cols if c.lower() not in [case_col.lower(), ts_col.lower() if ts_col else ""]]
        if extra_numeric:
            console.print(f"• Extra Numeric Attributes: {extra_numeric}")

    # Detailed numeric analysis for all numeric columns (including extra ones)
    for col in numeric_cols:
        console.print(f"\n[bold]Column: {col}[/bold]")
        arr = np.array(df[col].to_list(), dtype=float)
        arr = arr[~np.isnan(arr)]
        n = len(arr)

        table = Table(title=col)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Count", f"{n:,}")
        table.add_row("Mean", f"{arr.mean():.2f}")
        table.add_row("Median", f"{np.median(arr):.2f}")
        table.add_row("Std Dev", f"{arr.std():.2f}")
        console.print(table)

    # Plots (limited to first 4 numeric columns to avoid too many plots)
    if include_plots and numeric_cols:
        for col in numeric_cols[:4]:
            plt.figure(figsize=(8, 4))
            sns.histplot(df[col].to_list(), kde=True, color="skyblue")
            plt.title(f"Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            plt.show()

    console.print(Panel("[bold green]Analysis Complete — Full support for additional columns[/bold green]", style="green"))
    return "Done"


def _get_numeric_columns(data):
    df_nw = nw.from_native(data, eager_only=True)
    return list(df_nw.select(numeric()).columns)


def _get_categorical_columns(data):
    df_nw = nw.from_native(data, eager_only=True)
    return list(df_nw.select(categorical()).columns)


class BizDesc:
    def __init__(self, data):
        self.data = data

    def summary(self, include_plots: bool = True):
        return describe(self.data, include_plots=include_plots)


# Keep synthetic generators here for backward compatibility
def generate_sample_data(n_rows: int = 1000, seed: int = 42) -> pl.DataFrame:
    """Classic business dataset (kept for compatibility)"""
    from .datasets import generate_sample_data as ds_generate
    return ds_generate(n_rows, seed)


def generate_event_log(num_cases: int = 500, seed: int = 42) -> pl.DataFrame:
    """Original event log generator (kept for compatibility)"""
    from .datasets import generate_hr_onboarding_event_log
    return generate_hr_onboarding_event_log(num_cases, seed)