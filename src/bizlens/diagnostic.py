"""
BizLens Diagnostic Module — Data Quality & Statistical Diagnostics
Version: 2.3.2
"""

import pandas as pd
import numpy as np
import time
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from rich.table import Table as RichTable
from rich.console import Console
from typing import Union, Tuple, List, Dict
from . import ENABLE_PROFILING
from .utils import to_pandas

console = Console()


class diagnostic:
    """
    Data quality checks and diagnostic analytics.
    """

    @staticmethod
    def detect_outliers(series, method: str = 'iqr', contamination: float = 0.1, show_timing: bool = False):
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        df = to_pandas(series)
        if isinstance(series, pd.Series):
            data = series.dropna()
        else:
            data = df.iloc[:, 0].dropna() if len(df.columns) > 0 else pd.Series()

        if method == 'iqr':
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outlier_mask = (data < lower) | (data > upper)
        elif method == 'zscore':
            z_scores = np.abs(stats.zscore(data))
            outlier_mask = z_scores > 3
        elif method == 'isolation':
            scaler = StandardScaler()
            data_scaled = scaler.fit_transform(data.values.reshape(-1, 1))
            iso = IsolationForest(contamination=contamination, random_state=42)
            predictions = iso.fit_predict(data_scaled)
            outlier_mask = predictions == -1
        else:
            raise ValueError(f"Unknown method: {method}")

        outlier_indices = data[outlier_mask].index.tolist()

        table = RichTable(title=f"Outlier Detection ({method.upper()})", header_style="bold blue")
        table.add_column("Index", style="cyan")
        table.add_column("Value", justify="right", style="red")
        table.add_column("Z-Score", justify="right", style="yellow")

        for idx, value in zip(outlier_indices[:15], data[outlier_mask].values[:15]):
            zscore = abs(stats.zscore([value])[0])
            table.add_row(str(idx), f"{value:.4f}", f"{zscore:.2f}")

        console.print(table)
        console.print(f"[bold cyan]Found {len(outlier_indices)} outliers[/bold cyan]")

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] diagnostic.detect_outliers completed in {duration:.4f}s[/dim]")

        return outlier_indices, table


    @staticmethod
    def normality_test(series, show_timing: bool = False):
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        series = pd.Series(to_pandas(series)) if not isinstance(series, pd.Series) else series
        data = series.dropna()

        sw_stat, sw_p = stats.shapiro(data)
        ad = stats.anderson(data)
        ks_stat, ks_p = stats.kstest(data, 'norm', args=(data.mean(), data.std()))

        table = RichTable(title="Normality Tests", header_style="bold blue")
        table.add_column("Test", style="cyan")
        table.add_column("Statistic", justify="right")
        table.add_column("P-Value", justify="right")
        table.add_column("Result", style="green")

        table.add_row("Shapiro-Wilk", f"{sw_stat:.4f}", f"{sw_p:.4f}", "✓ Normal" if sw_p > 0.05 else "✗ Not Normal")
        table.add_row("Anderson-Darling", f"{ad.statistic:.4f}", f"{ad.significance_level[2]/100:.4f}", 
                      "✓ Normal" if ad.statistic < ad.critical_values[2] else "✗ Not Normal")
        table.add_row("Kolmogorov-Smirnov", f"{ks_stat:.4f}", f"{ks_p:.4f}", "✓ Normal" if ks_p > 0.05 else "✗ Not Normal")

        console.print(table)

        is_normal = sum([sw_p > 0.05, ks_p > 0.05]) >= 1

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] diagnostic.normality_test completed in {duration:.4f}s[/dim]")

        return {
            'is_normal': is_normal,
            'recommendation': 'parametric' if is_normal else 'non-parametric'
        }


    @staticmethod
    def correlation_analysis(df, show_timing: bool = False):
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        df = to_pandas(df)
        numeric_df = df.select_dtypes(include=[np.number])

        pearson_corr = numeric_df.corr(method='pearson')

        table = RichTable(title="Correlation Analysis", header_style="bold blue")
        table.add_column("Variable Pair", style="cyan")
        table.add_column("Pearson r", justify="right", style="magenta")
        table.add_column("Strength", style="green")

        for i in range(len(pearson_corr.columns)):
            for j in range(i + 1, len(pearson_corr.columns)):
                col1 = pearson_corr.columns[i]
                col2 = pearson_corr.columns[j]
                corr = pearson_corr.loc[col1, col2]
                if abs(corr) > 0.3:
                    strength = "Strong" if abs(corr) > 0.7 else "Moderate"
                    table.add_row(f"{col1} ↔ {col2}", f"{corr:.3f}", strength)

        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] diagnostic.correlation_analysis completed in {duration:.4f}s[/dim]")

        return table, pearson_corr


    @staticmethod
    def missing_value_analysis(df, show_timing: bool = False) -> RichTable:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        df = to_pandas(df)

        table = RichTable(title="Missing Value Analysis", header_style="bold blue")
        table.add_column("Column", style="cyan")
        table.add_column("Missing Count", justify="right", style="red")
        table.add_column("Missing %", justify="right", style="yellow")
        table.add_column("Data Type", style="magenta")

        total_rows = len(df)
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            missing_pct = (missing_count / total_rows) * 100
            severity = "🔴 Critical" if missing_pct > 50 else "🟠 High" if missing_pct > 20 else "🟡 Medium" if missing_pct > 5 else "✓ Low"
            table.add_row(col, str(missing_count), f"{missing_pct:.1f}%", str(df[col].dtype))

        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] diagnostic.missing_value_analysis completed in {duration:.4f}s[/dim]")

        return table