"""
BizLens Tables Module — Educational Statistical Tables & Summaries
Version: 2.2.14
Enhanced: Full pandas + polars support + optional performance timing.
"""

import pandas as pd
import numpy as np
import time
from scipy import stats
from rich.table import Table as RichTable
from rich.console import Console
from typing import Union, Tuple, Optional
from . import ENABLE_PROFILING   # global flag from __init__.py

console = Console()


def _to_pandas(df):
    """Internal helper – ensures all methods receive pandas DataFrame."""
    if isinstance(df, pd.DataFrame):
        return df
    elif isinstance(df, pd.Series):
        return df.to_frame()
    elif hasattr(df, 'to_pandas'):   # polars
        return df.to_pandas()
    return pd.DataFrame(df)


class tables:
    """
    Professional statistical tables for data exploration and communication.
    All original methods preserved + timing + pandas/polars compatibility.
    """

    @staticmethod
    def frequency_table(series: pd.Series, top_n: int = 10, show_timing: bool = False) -> RichTable:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        # Handle Series input properly
        if isinstance(series, pd.Series):
            data = series.dropna()
        else:
            series = pd.Series(_to_pandas(series).iloc[:, 0])
            data = series.dropna()
        value_counts = data.value_counts().head(top_n)
        total = len(data)
        percentages = (value_counts / total * 100).round(2)
        cumulative_pct = (value_counts.cumsum() / total * 100).round(2)

        table = RichTable(title=f"Frequency Table — {series.name or 'Series'}",
                         show_header=True, header_style="bold blue")
        table.add_column("Value", style="cyan")
        table.add_column("Count", justify="right", style="magenta")
        table.add_column("Percentage", justify="right", style="green")
        table.add_column("Cumulative %", justify="right", style="yellow")

        for value, count in value_counts.items():
            table.add_row(str(value), str(count), f"{percentages[value]:.2f}%", f"{cumulative_pct[value]:.2f}%")

        if len(value_counts) < len(data.unique()):
            other_count = len(data) - value_counts.sum()
            table.add_row(f"[Other ({len(data.unique()) - top_n} categories)]", str(other_count),
                          f"{(other_count / total * 100):.2f}%", "100.00%")

        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] tables.frequency_table completed in {duration:.4f}s[/dim]")
        return table

    @staticmethod
    def percentile_table(series: pd.Series, show_timing: bool = False) -> RichTable:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        # Handle Series input properly
        if isinstance(series, pd.Series):
            data = series.dropna()
        else:
            series = pd.Series(_to_pandas(series).iloc[:, 0])
            data = series.dropna()
        percentiles = [0, 25, 50, 75, 100]
        percentile_values = np.percentile(data, percentiles)
        q1 = percentile_values[1]
        q3 = percentile_values[3]
        iqr = q3 - q1

        table = RichTable(title=f"Percentile Table — {series.name or 'Series'}",
                         show_header=True, header_style="bold blue")
        table.add_column("Percentile", style="cyan")
        table.add_column("Value", justify="right", style="magenta")
        table.add_column("Interpretation", style="green")

        interpretations = [
            "Minimum value (lowest)",
            "First Quartile (Q1) — 25% of data below this",
            "Median — 50% above, 50% below",
            "Third Quartile (Q3) — 75% of data below this",
            "Maximum value (highest)"
        ]

        for pct, value, interp in zip(percentiles, percentile_values, interpretations):
            table.add_row(f"{pct}th" if pct != 50 else "50th (Median)",
                          f"{value:.4f}".rstrip('0').rstrip('.'), interp)

        table.add_row("", "", "")
        table.add_row("[bold]IQR[/bold]", f"{iqr:.4f}".rstrip('0').rstrip('.'), "Q3 - Q1 = middle 50% spread")

        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] tables.percentile_table completed in {duration:.4f}s[/dim]")
        return table

    @staticmethod
    def contingency_table(df: pd.DataFrame, row_col: str, col_col: str, show_timing: bool = False) -> Tuple[RichTable, dict]:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        df = _to_pandas(df)
        # === ORIGINAL CODE (100% unchanged) ===
        crosstab = pd.crosstab(df[row_col], df[col_col], margins=True)
        chi2, p_value, dof, expected = stats.chi2_contingency(pd.crosstab(df[row_col], df[col_col]))
        n = len(df)
        min_dim = min(len(df[row_col].unique()), len(df[col_col].unique())) - 1
        cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0

        table = RichTable(title=f"Contingency Table — {row_col} × {col_col}",
                         show_header=True, header_style="bold blue")
        table.add_column(row_col, style="cyan")
        for col in crosstab.columns:
            table.add_column(str(col), justify="right")
        for idx, row in crosstab.iterrows():
            table.add_row(str(idx), *[str(int(val)) for val in row])
        console.print(table)

        chi_results = {
            'chi2': chi2, 'p_value': p_value, 'dof': dof, 'cramers_v': cramers_v,
            'independent': p_value > 0.05,
            'interpretation': f"Variables are {'independent' if p_value > 0.05 else 'associated'} (p={p_value:.4f}, Cramér's V={cramers_v:.3f})"
        }

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] tables.contingency_table completed in {duration:.4f}s[/dim]")
        return table, chi_results

    @staticmethod
    def summary_statistics(df: pd.DataFrame, show_timing: bool = False) -> RichTable:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        df = _to_pandas(df)
        # === ORIGINAL CODE (100% unchanged) ===
        numeric_df = df.select_dtypes(include=[np.number])
        summary = numeric_df.describe(include='all').T
        summary['null_count'] = df[numeric_df.columns].isnull().sum()
        summary['null_pct'] = (summary['null_count'] / len(df) * 100).round(2)

        table = RichTable(title="Summary Statistics", show_header=True, header_style="bold blue")
        table.add_column("Column", style="cyan")
        table.add_column("Count", justify="right")
        table.add_column("Mean", justify="right", style="green")
        table.add_column("Std", justify="right")
        table.add_column("Min", justify="right")
        table.add_column("25%", justify="right")
        table.add_column("50%", justify="right")
        table.add_column("75%", justify="right")
        table.add_column("Max", justify="right")
        table.add_column("Null", justify="right", style="red")

        for col in summary.index:
            table.add_row(
                col,
                str(int(summary.loc[col, 'count'])),
                f"{summary.loc[col, 'mean']:.4f}".rstrip('0').rstrip('.'),
                f"{summary.loc[col, 'std']:.4f}".rstrip('0').rstrip('.'),
                f"{summary.loc[col, 'min']:.4f}".rstrip('0').rstrip('.'),
                f"{summary.loc[col, '25%']:.4f}".rstrip('0').rstrip('.'),
                f"{summary.loc[col, '50%']:.4f}".rstrip('0').rstrip('.'),
                f"{summary.loc[col, '75%']:.4f}".rstrip('0').rstrip('.'),
                f"{summary.loc[col, 'max']:.4f}".rstrip('0').rstrip('.'),
                f"{int(summary.loc[col, 'null_count'])} ({summary.loc[col, 'null_pct']:.1f}%)"
            )

        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] tables.summary_statistics completed in {duration:.4f}s[/dim]")
        return table

    @staticmethod
    def group_comparison(df: pd.DataFrame, group_col: str, numeric_cols: list = None, show_timing: bool = False) -> Tuple[RichTable, dict]:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        df = _to_pandas(df)
        # === ORIGINAL CODE (100% unchanged) ===
        if numeric_cols is None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        table = RichTable(title=f"Group Comparison — {group_col}", show_header=True, header_style="bold blue")
        table.add_column("Column", style="cyan")
        groups = sorted(df[group_col].unique())
        for group in groups:
            table.add_column(f"{group} (Mean ± Std)", justify="right")

        anova_results = {}
        for col in numeric_cols:
            table.add_row(col, end_section=False)
            group_data = [df[df[group_col] == g][col].dropna().values for g in groups]
            f_stat, p_value = stats.f_oneway(*group_data)
            anova_results[col] = {'f_stat': f_stat, 'p_value': p_value, 'significant': p_value < 0.05}

            row_data = [col]
            for group in groups:
                group_vals = df[df[group_col] == group][col].dropna()
                mean = group_vals.mean()
                std = group_vals.std()
                row_data.append(f"{mean:.2f} ± {std:.2f}")
            table.add_row(*row_data)

        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] tables.group_comparison completed in {duration:.4f}s[/dim]")
        return table, anova_results

    @staticmethod
    def distribution_fit(series: pd.Series, show_timing: bool = False) -> Tuple[RichTable, dict]:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        series = pd.Series(_to_pandas(series))
        # === ORIGINAL CODE (100% unchanged) ===
        data = series.dropna()
        distributions_to_test = {'Normal': stats.norm, 'Exponential': stats.expon, 'Lognormal': stats.lognorm}
        results = {}
        for dist_name, dist in distributions_to_test.items():
            try:
                params = dist.fit(data)
                ks_stat, p_value = stats.kstest(data, lambda x: dist.cdf(x, *params))
                results[dist_name] = {'ks_stat': ks_stat, 'p_value': p_value, 'params': params}
            except:
                results[dist_name] = {'ks_stat': np.nan, 'p_value': 0}

        table = RichTable(title="Distribution Fit Test", show_header=True, header_style="bold blue")
        table.add_column("Distribution", style="cyan")
        table.add_column("KS Statistic", justify="right")
        table.add_column("P-value", justify="right")
        table.add_column("Fit", style="green")

        best_dist = min(results.items(), key=lambda x: x[1]['ks_stat'])
        for dist_name, result in results.items():
            fit_qual = "✓ Best Fit" if dist_name == best_dist[0] else ""
            table.add_row(dist_name, f"{result['ks_stat']:.4f}", f"{result['p_value']:.4f}", fit_qual)

        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] tables.distribution_fit completed in {duration:.4f}s[/dim]")
        return table, {'best_fit': best_dist[0], 'results': results}

    @staticmethod
    def descriptive_comparison(df1: pd.DataFrame, df2: pd.DataFrame,
                               label1: str = "Data 1", label2: str = "Data 2", show_timing: bool = False) -> RichTable:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        df1 = _to_pandas(df1)
        df2 = _to_pandas(df2)
        # === ORIGINAL CODE (100% unchanged) ===
        numeric_cols = df1.select_dtypes(include=[np.number]).columns
        table = RichTable(title=f"{label1} vs {label2} Comparison", show_header=True, header_style="bold blue")
        table.add_column("Metric", style="cyan")
        table.add_column(label1, justify="right", style="magenta")
        table.add_column(label2, justify="right", style="green")
        table.add_column("Difference", justify="right", style="yellow")

        for col in numeric_cols:
            d1 = df1[col].dropna()
            d2 = df2[col].dropna()
            mean1 = d1.mean()
            mean2 = d2.mean()
            table.add_row(f"{col} (mean)", f"{mean1:.4f}".rstrip('0').rstrip('.'), f"{mean2:.4f}".rstrip('0').rstrip('.'), f"{(mean1 - mean2):.4f}".rstrip('0').rstrip('.'))
            std1 = d1.std()
            std2 = d2.std()
            table.add_row(f"{col} (std)", f"{std1:.4f}".rstrip('0').rstrip('.'), f"{std2:.4f}".rstrip('0').rstrip('.'), f"{(std1 - std2):.4f}".rstrip('0').rstrip('.'))
            table.add_row(f"{col} (N)", str(len(d1)), str(len(d2)), str(len(d1) - len(d2)))
            table.add_row("", "", "", "")

        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] tables.descriptive_comparison completed in {duration:.4f}s[/dim]")
        return table