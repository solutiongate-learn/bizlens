"""
BizLens Tables Module — Educational Statistical Tables & Summaries
Version: 2.3.2
"""

import pandas as pd
import numpy as np
import time
from scipy import stats
from rich.table import Table as RichTable
from rich.console import Console
from . import ENABLE_PROFILING
from .utils import to_pandas

console = Console()


class tables:
    """
    Professional statistical tables for data exploration.
    """

    @staticmethod
    def frequency_table(series, top_n: int = 10, show_timing: bool = False) -> RichTable:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        series = pd.Series(to_pandas(series)).dropna()
        value_counts = series.value_counts().head(top_n)
        total = len(series)
        percentages = (value_counts / total * 100).round(2)

        table = RichTable(title=f"Frequency Table — {series.name or 'Series'}", header_style="bold blue")
        table.add_column("Value", style="cyan")
        table.add_column("Count", justify="right", style="magenta")
        table.add_column("Percentage", justify="right", style="green")

        for value, count in value_counts.items():
            table.add_row(str(value), str(count), f"{percentages[value]:.2f}%")

        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] tables.frequency_table completed in {duration:.4f}s[/dim]")

        return table


    @staticmethod
    def summary_statistics(df, show_timing: bool = False) -> RichTable:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        df = to_pandas(df)
        numeric_df = df.select_dtypes(include=[np.number])

        summary = numeric_df.describe().T.round(4)
        summary['null_pct'] = (df[numeric_df.columns].isnull().sum() / len(df) * 100).round(2)

        table = RichTable(title="Summary Statistics", header_style="bold blue")
        table.add_column("Column", style="cyan")
        table.add_column("Mean", justify="right")
        table.add_column("Std", justify="right")
        table.add_column("Min", justify="right")
        table.add_column("Max", justify="right")
        table.add_column("Null %", justify="right", style="red")

        for col in summary.index:
            table.add_row(
                col,
                f"{summary.loc[col, 'mean']:.4f}",
                f"{summary.loc[col, 'std']:.4f}",
                f"{summary.loc[col, 'min']:.4f}",
                f"{summary.loc[col, 'max']:.4f}",
                f"{summary.loc[col, 'null_pct']:.1f}%"
            )

        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] tables.summary_statistics completed in {duration:.4f}s[/dim]")

        return table


    @staticmethod
    def contingency_table(df, row_col: str, col_col: str, show_timing: bool = False):
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        df = to_pandas(df)
        crosstab = pd.crosstab(df[row_col], df[col_col], margins=True)
        chi2, p_value, dof, expected = stats.chi2_contingency(pd.crosstab(df[row_col], df[col_col]))

        table = RichTable(title=f"Contingency Table — {row_col} × {col_col}", header_style="bold blue")
        table.add_column(row_col, style="cyan")
        for col in crosstab.columns:
            table.add_column(str(col), justify="right")
        for idx, row in crosstab.iterrows():
            table.add_row(str(idx), *[str(int(val)) for val in row])

        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] tables.contingency_table completed in {duration:.4f}s[/dim]")

        return table, {'p_value': p_value}