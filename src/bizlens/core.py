"""
BizLens v2.2.8 — Descriptive Analytics Core
Focused on rich educational output for teaching and business analysis.
"""

import warnings
import numpy as np
import pandas as pd
import polars as pl
import narwhals as nw
from narwhals.selectors import numeric, categorical
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")
console = Console()

# ─────────────────────────────────────────────────────────────────────────────
# SYNTHETIC DATA GENERATORS
# ─────────────────────────────────────────────────────────────────────────────
def generate_sample_data(n_rows: int = 1000, seed: int = 42) -> pl.DataFrame:
    """Generate realistic business data for teaching."""
    np.random.seed(seed)
    data = {
        "customer_id": [f"C{str(i).zfill(5)}" for i in range(n_rows)],
        "revenue": np.random.lognormal(mean=8, sigma=1.2, size=n_rows).round(2),
        "profit_margin": (np.random.beta(2, 5, size=n_rows) * 100).round(2),
        "customer_satisfaction": np.clip(np.random.normal(75, 12, size=n_rows), 0, 100).round(1),
        "units_sold": np.random.poisson(lam=45, size=n_rows),
        "region": np.random.choice(["North", "South", "East", "West"], size=n_rows),
    }
    df = pl.DataFrame(data)
    console.print(f"[bold green]✅ Generated business dataset ({n_rows} rows)[/bold green]")
    return df


def generate_event_log(num_cases: int = 500, seed: int = 42) -> pl.DataFrame:
    """Generate realistic event log for process mining introduction."""
    np.random.seed(seed)
    activities = ["Order Placed", "Payment Received", "Processing", "Quality Check", "Shipped", "Delivered"]
    events = []
    start_date = datetime(2025, 1, 1)

    for case_id in range(1, num_cases + 1):
        num_events = np.random.randint(3, len(activities) + 1)
        case_activities = np.random.choice(activities, num_events, replace=False)
        current_time = start_date + timedelta(days=np.random.randint(0, 90))

        for i, activity in enumerate(case_activities):
            timestamp = current_time + timedelta(minutes=np.random.randint(30, 1440))
            resource = np.random.choice(["Alice", "Bob", "Charlie", "Diana"])
            cost = round(np.random.uniform(10, 250), 2)
            status = "Completed" if i == len(case_activities)-1 else "In Progress"

            events.append({
                "case_id": f"CASE-{str(case_id).zfill(5)}",
                "activity": activity,
                "timestamp": timestamp,
                "resource": resource,
                "cost": cost,
                "status": status
            })
            current_time = timestamp

    df = pl.DataFrame(events)
    console.print(f"[bold green]✅ Generated Process Mining Event Log ({num_cases} cases)[/bold green]")
    return df


# ─────────────────────────────────────────────────────────────────────────────
# MAIN DESCRIBE FUNCTION
# ─────────────────────────────────────────────────────────────────────────────
def describe(data, include_plots: bool = True, norm_compare: bool = False):
    """Rich descriptive analysis with educational insights."""
    console.print(Panel("[bold cyan]BizLens Descriptive Analytics v2.2.8[/bold cyan]", style="bold blue"))

    if isinstance(data, pd.DataFrame):
        df = pl.from_pandas(data)
    elif isinstance(data, pl.DataFrame):
        df = data
    else:
        console.print("Single column support coming soon.")
        return None

    numeric_cols = _get_numeric_columns(df)
    categorical_cols = _get_categorical_columns(df)

    console.print(f"[bold green]Numeric Columns ({len(numeric_cols)}):[/] {numeric_cols}")
    console.print(f"[bold yellow]Categorical Columns ({len(categorical_cols)}):[/] {categorical_cols}\n")

    for col in numeric_cols:
        console.print(f"\n[bold]Column: {col}[/bold]")
        arr = np.array(df[col].to_list())
        arr = arr[~np.isnan(arr)]
        n = len(arr)
        mean_val = arr.mean()
        median_val = np.median(arr)
        std_val = arr.std()
        skew_val = stats.skew(arr)

        # Outlier detection
        q1, q3 = np.percentile(arr, [25, 75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        outliers = arr[(arr < lower) | (arr > upper)]
        outlier_pct = len(outliers) / n * 100 if n > 0 else 0

        # Normality test
        shapiro_p = stats.shapiro(arr[:5000] if n > 5000 else arr)[1]

        table = Table(title=col)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green", justify="right")
        table.add_column("Interpretation", style="dim")
        rows = [
            ("Count", str(n), ""),
            ("Mean", f"{mean_val:.2f}", ""),
            ("Median", f"{median_val:.2f}", "Robust to outliers"),
            ("Std Dev", f"{std_val:.2f}", ""),
            ("Skewness", f"{skew_val:.2f}", "Right-skewed" if skew_val > 0.5 else "Left-skewed" if skew_val < -0.5 else "Symmetric"),
            ("Outliers (IQR)", f"{len(outliers)} ({outlier_pct:.1f}%)", "Potential anomalies"),
            ("Shapiro p-value", f"{shapiro_p:.4f}", "Normal" if shapiro_p > 0.05 else "Non-normal"),
        ]
        for row in rows:
            table.add_row(*row)
        console.print(table)

    if include_plots:
        for col in numeric_cols[:3]:
            plt.figure(figsize=(8, 4))
            sns.histplot(df[col].to_list(), kde=True)
            plt.title(f"Distribution of {col}")
            plt.show()

    console.print(Panel("[bold green]Analysis Complete — Ready for teaching and business decisions[/bold green]", style="green"))
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


# Export synthetic generators
__all__ = ["describe", "BizDesc", "generate_sample_data", "generate_event_log"]