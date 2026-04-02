"""
BizLens v2.2.4 — Integrated Analytics Platform
Descriptive · Diagnostic · Predictive · Optimization

Core module providing unified analytics with:
- Sample vs Population distinction (n-1 vs n)
- FULL DataFrame support (tips, iris, titanic, penguins, etc.)
- Modern Narwhals selector (no more NUMERIC_DTYPES error)
- Educational output with formulas and interpretation
- Professional visualizations
"""

import warnings
import numpy as np
import pandas as pd
import polars as pl
import narwhals as nw
from narwhals.selectors import numeric          # ← NEW: modern selector
from narwhals.typing import IntoFrame
import scipy.stats as sp_stats
import matplotlib.pyplot as plt
import seaborn as sns
from rich.console import Console
from rich.table import Table
from typing import Any, Dict, List, Optional, Union, Tuple
from pathlib import Path

warnings.filterwarnings("ignore")
console = Console()

# ─────────────────────────────────────────────────────────────────────────────
# COLOR SCHEMES
# ─────────────────────────────────────────────────────────────────────────────
COLOR_SCHEMES = {
    "academic": {
        "primary": "#2E86AB", "secondary": "#A23B72", "accent": "#F18F01",
        "success": "#06A77D", "danger": "#D62828",
        "palette": ["#2E86AB", "#A23B72", "#F18F01", "#06A77D", "#D62828"],
    },
    "pastel": {
        "primary": "#8ECAE6", "secondary": "#FFB4A2", "accent": "#E5989B",
        "success": "#90E0EF", "danger": "#F77F88",
        "palette": ["#8ECAE6", "#FFB4A2", "#E5989B", "#90E0EF", "#F77F88"],
    },
    "vibrant": {
        "primary": "#FF6B6B", "secondary": "#4ECDC4", "accent": "#FFE66D",
        "success": "#95E1D3", "danger": "#C9184A",
        "palette": ["#FF6B6B", "#4ECDC4", "#FFE66D", "#95E1D3", "#C9184A"],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: Modern Narwhals numeric column selector (fixes your error)
# ─────────────────────────────────────────────────────────────────────────────
def _get_numeric_columns(data) -> List[str]:
    """Return list of numeric column names – works with narwhals >= 1.x"""
    df_nw = nw.from_native(data, eager_only=True)
    return df_nw.select(numeric()).columns.tolist()

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: Load native data as numpy array (unchanged)
# ─────────────────────────────────────────────────────────────────────────────
def _to_numpy(data) -> np.ndarray:
    """Convert any array-like, pandas Series, or polars Series to numpy array."""
    if isinstance(data, pl.Series):
        arr = data.to_numpy()
    elif isinstance(data, pd.Series):
        arr = data.to_numpy()
    elif isinstance(data, np.ndarray):
        arr = data
    else:
        arr = np.array(data, dtype=float)
    return arr[~np.isnan(arr.astype(float))]

# ─────────────────────────────────────────────────────────────────────────────
# DESCRIPTIVE ANALYTICS – NOW WORKS ON FULL DATAFRAMES!
# ─────────────────────────────────────────────────────────────────────────────
def describe(
    data,
    calculation_level: str = "sample",
    show_formula: bool = True,
    color_scheme: str = "academic",
    include_plots: bool = False,
) -> Dict[str, Any]:
    """
    Comprehensive descriptive statistics.
    NOW SUPPORTS:
      - Single numeric column (old behaviour)
      - Full DataFrame (new behaviour) → automatically analyses all numeric columns
    """
    if calculation_level not in ("sample", "population"):
        raise ValueError("calculation_level must be 'sample' or 'population'")

    # ── NEW: Auto-handle full DataFrames (tips, iris, titanic, etc.)
    if isinstance(data, (pd.DataFrame, pl.DataFrame)) or hasattr(data, "columns"):
        numeric_cols = _get_numeric_columns(data)
        if len(numeric_cols) == 0:
            raise ValueError("No numeric columns found in the DataFrame.")
        if len(numeric_cols) == 1:
            # single column → univariate path
            return _describe_univariate(data[numeric_cols[0]],
                                        calculation_level, show_formula,
                                        color_scheme, include_plots)
        else:
            # multiple columns → use BizDesc
            return BizDesc(data).summary(include_plots=include_plots)

    # Original univariate path (list, Series, single column)
    return _describe_univariate(data, calculation_level, show_formula,
                                color_scheme, include_plots)

def _describe_univariate(
    data,
    calculation_level: str = "sample",
    show_formula: bool = True,
    color_scheme: str = "academic",
    include_plots: bool = False,
) -> Dict[str, Any]:
    """Internal univariate implementation (kept exactly as before)"""
    arr = _to_numpy(data)
    n = len(arr)
    if n == 0:
        raise ValueError("Data is empty after removing missing values.")

    ddof = 1 if calculation_level == "sample" else 0
    symbol = "s" if calculation_level == "sample" else "σ"
    var_symbol = "s²" if calculation_level == "sample" else "σ²"

    mean_val = float(np.mean(arr))
    median_val = float(np.median(arr))
    mode_result = sp_stats.mode(arr, keepdims=True)
    mode_val = float(mode_result.mode[0]) if n > 0 else float("nan")
    std_val = float(np.std(arr, ddof=ddof))
    var_val = float(np.var(arr, ddof=ddof))
    q1, q3 = float(np.percentile(arr, 25)), float(np.percentile(arr, 75))
    iqr_val = q3 - q1
    skew_val = float(sp_stats.skew(arr))
    kurt_val = float(sp_stats.kurtosis(arr))
    cv_val = (std_val / mean_val * 100) if mean_val != 0 else float("nan")

    if abs(skew_val) < 0.5:
        shape = "Symmetric (Normal-like)"
    elif skew_val > 0.5:
        shape = "Right-Skewed (Positive) — mean > median"
    else:
        shape = "Left-Skewed (Negative) — mean < median"

    result = {
        "n": n,
        "calculation_level": calculation_level,
        "mean": round(mean_val, 4),
        "median": round(median_val, 4),
        "mode": round(mode_val, 4),
        "std": round(std_val, 4),
        "variance": round(var_val, 4),
        "min": round(float(np.min(arr)), 4),
        "max": round(float(np.max(arr)), 4),
        "range": round(float(np.max(arr) - np.min(arr)), 4),
        "q1": round(q1, 4),
        "q3": round(q3, 4),
        "iqr": round(iqr_val, 4),
        "skewness": round(skew_val, 4),
        "kurtosis": round(kurt_val, 4),
        "cv_percent": round(cv_val, 2),
        "distribution_shape": shape,
        "symbol_std": symbol,
        "symbol_var": var_symbol,
    }

    # Rich console output (unchanged from your original)
    colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])
    table = Table(title=f"Descriptive Statistics [{calculation_level.upper()}]", style="bold", show_lines=True)
    table.add_column("Statistic", style="cyan", width=22)
    table.add_column("Value", style="green", justify="right", width=14)
    table.add_column("Formula / Note", style="dim", width=40)

    rows = [
        ("Count (n)", str(n), "Number of valid observations"),
        ("Mean (x̄ / μ)", f"{mean_val:.4f}", "Σxᵢ / n"),
        ("Median", f"{median_val:.4f}", "Middle value when sorted"),
        ("Mode", f"{mode_val:.4f}", "Most frequently occurring value"),
        (f"Std Dev ({symbol})", f"{std_val:.4f}", f"√(Σ(xᵢ-x̄)² / (n-{ddof}))"),
        (f"Variance ({var_symbol})", f"{var_val:.4f}", f"Σ(xᵢ-x̄)² / (n-{ddof})"),
        ("Min / Max", f"{np.min(arr):.4f} / {np.max(arr):.4f}", ""),
        ("Range", f"{result['range']:.4f}", "Max − Min"),
        ("Q1 / Q3", f"{q1:.4f} / {q3:.4f}", "25th and 75th percentiles"),
        ("IQR", f"{iqr_val:.4f}", "Q3 − Q1"),
        ("Skewness", f"{skew_val:.4f}", shape),
        ("Kurtosis", f"{kurt_val:.4f}", "Measure of tailedness"),
        ("CV %", f"{cv_val:.2f}", "Coefficient of variation"),
    ]
    for row in rows:
        table.add_row(*row)
    console.print(table)

    if include_plots:
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        sns.histplot(arr, kde=True, ax=axes[0], color=colors["primary"])
        axes[0].set_title("Histogram with KDE")
        sns.boxplot(x=arr, ax=axes[1], color=colors["accent"])
        axes[1].set_title("Box Plot")
        plt.suptitle(f"Distribution of {getattr(data, 'name', 'Variable')}", fontsize=14, fontweight="bold")
        plt.tight_layout()
        plt.show()

    return result

# ─────────────────────────────────────────────────────────────────────────────
# BIZDESC CLASS (full DataFrame support)
# ─────────────────────────────────────────────────────────────────────────────
class BizDesc:
    def __init__(self, data: IntoFrame):
        self.data = data
        self.calculation_level = "sample"
        self.color_scheme = "academic"

    def summary(self, include_plots: bool = False):
        """Full DataFrame summary using modern Narwhals selector"""
        numeric_cols = _get_numeric_columns(self.data)
        results = {}
        console.print(f"[bold cyan]Analyzing {len(numeric_cols)} numeric columns[/bold cyan]")
        for col in numeric_cols:
            console.print(f"\n[bold]Column: {col}[/bold]")
            results[col] = _describe_univariate(
                self.data[col],
                calculation_level=self.calculation_level,
                show_formula=True,
                color_scheme=self.color_scheme,
                include_plots=include_plots
            )
        return results

# ─────────────────────────────────────────────────────────────────────────────
# (All your other classes — diagnostic, predict, optimize, tables, quality, project, text, etc.)
# are kept exactly as they were in v2.2.3 — no changes needed for the current errors.
# (They are very long, so they are omitted here for brevity. Your original file already has them.)
# ─────────────────────────────────────────────────────────────────────────────