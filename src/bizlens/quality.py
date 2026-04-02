"""
BizLens Quality Module — Data Quality Assessment
Version: 2.2.12
Enhanced: Full pandas + polars support + optional performance timing.
"""

import pandas as pd
import numpy as np
import time
from rich.table import Table as RichTable
from rich.console import Console
from typing import Dict, Tuple, Union
from . import ENABLE_PROFILING   # global flag from __init__.py

console = Console()


def _to_pandas(df):
    """Internal helper – ensures all methods receive pandas DataFrame."""
    if isinstance(df, pd.DataFrame):
        return df
    elif isinstance(df, pl.DataFrame):   # polars support
        return df.to_pandas()
    return df


class quality:
    """
    Data quality assessment and validation.
    All original methods preserved + timing + pandas/polars compatibility.
    """

    @staticmethod
    def completeness_report(df, show_timing: bool = False) -> RichTable:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        df = _to_pandas(df)

        # === ORIGINAL CODE (100% unchanged) ===
        table = RichTable(title="Data Completeness Report",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Column", style="cyan")
        table.add_column("Non-Null", justify="right", style="green")
        table.add_column("Null Count", justify="right", style="red")
        table.add_column("Null %", justify="right", style="yellow")
        table.add_column("Status", style="magenta")

        total_rows = len(df)
        overall_null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100

        null_counts = df.isnull().sum().sort_values(ascending=False)
        null_pcts = (null_counts / total_rows * 100)

        for col in null_counts.index:
            null_pct = null_pcts[col]
            non_null = total_rows - null_counts[col]

            if null_pct == 0:
                status = "✓ Complete"
            elif null_pct < 5:
                status = "✓ Good"
            elif null_pct < 20:
                status = "⚠️ Moderate"
            elif null_pct < 50:
                status = "🔴 High"
            else:
                status = "🔴 Critical"

            table.add_row(
                col,
                str(non_null),
                str(null_counts[col]),
                f"{null_pct:.1f}%",
                status
            )

        console.print(table)
        console.print(f"\n[bold]Overall Completeness: {100 - overall_null_pct:.1f}%[/bold]")

        if overall_null_pct > 10:
            console.print("[yellow]⚠️ Overall data completeness is low (<90%)[/yellow]")

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] quality.completeness_report completed in {duration:.4f}s[/dim]")

        return table

    @staticmethod
    def consistency_check(df, show_timing: bool = False) -> RichTable:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        df = _to_pandas(df)

        # === ORIGINAL CODE (100% unchanged) ===
        table = RichTable(title="Data Consistency Check",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Column", style="cyan")
        table.add_column("Expected Type", style="magenta")
        table.add_column("Issues Found", style="red")
        table.add_column("Severity", style="yellow")

        consistency_issues = []

        for col in df.columns:
            non_null_values = df[col].dropna()
            if len(non_null_values) > 0:
                unique_types = non_null_values.apply(type).nunique()
                expected_type = str(df[col].dtype)

                if unique_types > 1:
                    issues = f"Mixed types (found {unique_types})"
                    severity = "🔴 Critical"
                    consistency_issues.append(col)
                elif df[col].dtype == 'object':
                    issues = "Mixed or unexpected format"
                    severity = "⚠️ Warning"
                else:
                    issues = "✓ Consistent"
                    severity = "✓ OK"

                table.add_row(col, expected_type, issues, severity)

        console.print(table)

        if consistency_issues:
            console.print(f"\n[bold yellow]⚠️ Found {len(consistency_issues)} columns with type inconsistencies[/bold yellow]")
            console.print("[dim]Recommendation: Investigate and clean these columns[/dim]")

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] quality.consistency_check completed in {duration:.4f}s[/dim]")

        return table

    @staticmethod
    def uniqueness_analysis(df, show_timing: bool = False) -> Tuple[int, RichTable]:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        df = _to_pandas(df)

        # === ORIGINAL CODE (100% unchanged) ===
        duplicate_count = len(df) - len(df.drop_duplicates())
        duplicate_pct = (duplicate_count / len(df)) * 100

        table = RichTable(title="Uniqueness Analysis",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Column", style="cyan")
        table.add_column("Unique Values", justify="right", style="magenta")
        table.add_column("Uniqueness %", justify="right", style="green")
        table.add_column("Type", style="yellow")

        for col in df.columns:
            unique_count = df[col].nunique()
            uniqueness_pct = (unique_count / len(df)) * 100

            if uniqueness_pct < 5:
                col_type = "Low (Categorical)"
            elif uniqueness_pct > 95:
                col_type = "High (ID-like)"
            else:
                col_type = "Medium"

            table.add_row(
                col,
                str(unique_count),
                f"{uniqueness_pct:.1f}%",
                col_type
            )

        console.print(table)

        console.print(f"\n[bold]Duplicate Rows: {duplicate_count} ({duplicate_pct:.1f}%)[/bold]")
        if duplicate_count > 0:
            console.print(f"[yellow]⚠️ Found {duplicate_count} duplicate rows[/yellow]")
            console.print("[dim]Recommendation: Investigate and remove duplicates[/dim]")
        else:
            console.print("[green]✓ No duplicate rows found[/green]")

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] quality.uniqueness_analysis completed in {duration:.4f}s[/dim]")

        return duplicate_count, table

    @staticmethod
    def data_profile(df, show_timing: bool = False) -> Dict[str, Union[float, str, int]]:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        df = _to_pandas(df)

        # === ORIGINAL CODE (100% unchanged) ===
        completeness = 100 - (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100)

        consistency_issues = 0
        for col in df.columns:
            if df[col].dtype == 'object':
                unique_types = df[col].apply(type).nunique()
                if unique_types > 1:
                    consistency_issues += 1

        consistency = max(0, 100 - (consistency_issues / len(df.columns) * 50))

        uniqueness_issues = 0
        for col in df.columns:
            unique_pct = (df[col].nunique() / len(df)) * 100
            if unique_pct > 99 or unique_pct < 1:
                uniqueness_issues += 1

        uniqueness = max(0, 100 - (uniqueness_issues / len(df.columns) * 30))

        duplicate_pct = (1 - len(df.drop_duplicates()) / len(df)) * 100
        duplicates = 100 - min(duplicate_pct, 100)

        overall_score = (
            completeness * 0.4 +
            consistency * 0.3 +
            uniqueness * 0.2 +
            duplicates * 0.1
        )

        table = RichTable(title="Data Quality Profile",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Dimension", style="cyan")
        table.add_column("Score", justify="right", style="magenta")
        table.add_column("Assessment", style="green")

        def get_assessment(score):
            if score >= 90:
                return "✓ Excellent"
            elif score >= 70:
                return "✓ Good"
            elif score >= 50:
                return "⚠️ Fair"
            else:
                return "🔴 Poor"

        table.add_row("Completeness", f"{completeness:.1f}", get_assessment(completeness))
        table.add_row("Consistency", f"{consistency:.1f}", get_assessment(consistency))
        table.add_row("Uniqueness", f"{uniqueness:.1f}", get_assessment(uniqueness))
        table.add_row("Duplicate-Free", f"{duplicates:.1f}", get_assessment(duplicates))
        table.add_row("[bold]Overall Score[/bold]", f"{overall_score:.1f}", get_assessment(overall_score))

        console.print(table)

        if overall_score >= 85:
            console.print("[bold green]✓ Data quality is GOOD — ready for analysis[/bold green]")
        elif overall_score >= 70:
            console.print("[bold yellow]⚠️ Data quality is FAIR — minor cleaning recommended[/bold yellow]")
        else:
            console.print("[bold red]🔴 Data quality is POOR — significant cleaning needed[/bold red]")

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] quality.data_profile completed in {duration:.4f}s[/dim]")

        return {
            'overall_score': overall_score,
            'completeness': completeness,
            'consistency': consistency,
            'uniqueness': uniqueness,
            'duplicates': duplicates,
            'assessment': get_assessment(overall_score)
        }

    @staticmethod
    def outlier_summary(df, show_timing: bool = False) -> RichTable:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        df = _to_pandas(df)

        # === ORIGINAL CODE (100% unchanged) ===
        numeric_df = df.select_dtypes(include=[np.number])

        table = RichTable(title="Outlier Summary",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Column", style="cyan")
        table.add_column("Min", justify="right", style="green")
        table.add_column("Max", justify="right", style="red")
        table.add_column("Range", justify="right", style="magenta")
        table.add_column("Potential Issues", style="yellow")

        for col in numeric_df.columns:
            min_val = numeric_df[col].min()
            max_val = numeric_df[col].max()
            range_val = max_val - min_val

            Q1 = numeric_df[col].quantile(0.25)
            Q3 = numeric_df[col].quantile(0.75)
            IQR = Q3 - Q1
            outlier_threshold = 1.5 * IQR
            outlier_count = (
                ((numeric_df[col] < Q1 - outlier_threshold) |
                 (numeric_df[col] > Q3 + outlier_threshold)).sum()
            )

            issue = "⚠️ Possible outliers" if outlier_count > 0 else "✓ OK"

            table.add_row(
                col,
                f"{min_val:.2f}".rstrip('0').rstrip('.'),
                f"{max_val:.2f}".rstrip('0').rstrip('.'),
                f"{range_val:.2f}".rstrip('0').rstrip('.'),
                f"{issue} ({outlier_count})"
            )

        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] quality.outlier_summary completed in {duration:.4f}s[/dim]")

        return table