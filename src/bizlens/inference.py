"""
BizLens Inference Module — Statistical Inference & Hypothesis Testing
Version: 2.3.2
"""

import pandas as pd
import numpy as np
import time
from scipy import stats
from rich.table import Table as RichTable
from rich.console import Console
from typing import Union, Tuple, Dict
from . import ENABLE_PROFILING
from .utils import to_pandas

console = Console()


class inference:
    """
    Statistical inference and hypothesis testing.
    """

    @staticmethod
    def confidence_interval(series, confidence: float = 0.95, method: str = 't', show_timing: bool = False):
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        series = pd.Series(to_pandas(series)).dropna()
        n = len(series)
        mean = series.mean()
        std_err = series.std() / np.sqrt(n)

        if method == 't':
            df = n - 1
            alpha = 1 - confidence
            t_crit = stats.t.ppf(1 - alpha/2, df)
            margin = t_crit * std_err
        else:
            z_crit = stats.norm.ppf(1 - (1 - confidence) / 2)
            margin = z_crit * std_err

        lower = mean - margin
        upper = mean + margin

        table = RichTable(title=f"{int(confidence*100)}% Confidence Interval", header_style="bold blue")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right", style="magenta")
        table.add_row("Sample Mean", f"{mean:.4f}")
        table.add_row("Lower Bound", f"{lower:.4f}")
        table.add_row("Upper Bound", f"{upper:.4f}")
        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] inference.confidence_interval completed in {duration:.4f}s[/dim]")

        return lower, mean, upper


    @staticmethod
    def one_sample_ttest(sample, pop_mean: float, show_timing: bool = False):
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        sample = pd.Series(to_pandas(sample)).dropna()
        t_stat, p_value = stats.ttest_1samp(sample, pop_mean)
        cohens_d = (sample.mean() - pop_mean) / sample.std()

        table = RichTable(title="One-Sample T-Test", header_style="bold blue")
        table.add_column("Statistic", style="cyan")
        table.add_column("Value", justify="right", style="magenta")
        table.add_row("Sample Mean", f"{sample.mean():.4f}")
        table.add_row("Population Mean (H0)", f"{pop_mean:.4f}")
        table.add_row("T-Statistic", f"{t_stat:.4f}")
        table.add_row("P-Value", f"{p_value:.4f}")
        table.add_row("Cohen's d", f"{cohens_d:.4f}")
        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] inference.one_sample_ttest completed in {duration:.4f}s[/dim]")

        return {
            'sample_mean': sample.mean(),
            'p_value': p_value,
            'significant': p_value < 0.05,
            'effect_size': 'large' if abs(cohens_d) > 0.8 else 'medium' if abs(cohens_d) > 0.5 else 'small'
        }


    @staticmethod
    def two_sample_ttest(group1, group2, show_timing: bool = False):
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        g1 = pd.Series(to_pandas(group1)).dropna()
        g2 = pd.Series(to_pandas(group2)).dropna()

        t_stat, p_value = stats.ttest_ind(g1, g2, equal_var=False)
        cohens_d = (g1.mean() - g2.mean()) / np.sqrt((g1.std()**2 + g2.std()**2) / 2)

        table = RichTable(title="Two-Sample T-Test", header_style="bold blue")
        table.add_column("Group", style="cyan")
        table.add_column("Mean", justify="right", style="magenta")
        table.add_row("Group 1", f"{g1.mean():.4f}")
        table.add_row("Group 2", f"{g2.mean():.4f}")
        table.add_row("Difference", f"{g1.mean() - g2.mean():.4f}")
        table.add_row("T-Statistic", f"{t_stat:.4f}")
        table.add_row("P-Value", f"{p_value:.4f}")
        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] inference.two_sample_ttest completed in {duration:.4f}s[/dim]")

        return {'p_value': p_value, 'significant': p_value < 0.05}


    @staticmethod
    def anova_test(groups_dict: dict, show_timing: bool = False):
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        groups = [pd.Series(to_pandas(v)).dropna().values for v in groups_dict.values()]
        f_stat, p_value = stats.f_oneway(*groups)

        table = RichTable(title="One-Way ANOVA", header_style="bold blue")
        table.add_column("Statistic", style="cyan")
        table.add_column("Value", justify="right", style="magenta")
        table.add_row("F-Statistic", f"{f_stat:.4f}")
        table.add_row("P-Value", f"{p_value:.4f}")
        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] inference.anova_test completed in {duration:.4f}s[/dim]")

        return {'p_value': p_value, 'significant': p_value < 0.05}


    @staticmethod
    def correlation_test(x, y, show_timing: bool = False):
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        x = pd.Series(to_pandas(x)).dropna()
        y = pd.Series(to_pandas(y)).dropna()
        valid = pd.concat([x, y], axis=1).dropna()
        x_clean, y_clean = valid.iloc[:,0], valid.iloc[:,1]

        r, p_pearson = stats.pearsonr(x_clean, y_clean)
        rho, p_spearman = stats.spearmanr(x_clean, y_clean)

        table = RichTable(title="Correlation Test", header_style="bold blue")
        table.add_column("Test", style="cyan")
        table.add_column("Coefficient", justify="right", style="magenta")
        table.add_column("P-Value", justify="right", style="yellow")
        table.add_row("Pearson r", f"{r:.4f}", f"{p_pearson:.4f}")
        table.add_row("Spearman ρ", f"{rho:.4f}", f"{p_spearman:.4f}")
        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] inference.correlation_test completed in {duration:.4f}s[/dim]")

        return {'pearson_r': r, 'p_value': p_pearson}