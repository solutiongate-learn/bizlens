"""
BizLens Inference Module — Statistical Inference & Hypothesis Testing
Version: 2.2.12
Enhanced: Full pandas + polars support + optional performance timing.
"""

import pandas as pd
import numpy as np
import time
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.proportion import proportions_ztest
from rich.table import Table as RichTable
from rich.console import Console
from typing import Union, Tuple, Dict, List
from . import ENABLE_PROFILING   # global flag from __init__.py

console = Console()


def _to_pandas(data):
    """Internal helper – ensures all methods receive pandas objects."""
    if isinstance(data, pd.DataFrame):
        return data
    elif isinstance(data, pd.Series):
        return data
    elif isinstance(data, (list, np.ndarray)):
        return pd.Series(data)
    elif hasattr(data, 'to_pandas'):   # polars DataFrame / Series
        return data.to_pandas()
    return pd.DataFrame(data)


class inference:
    """
    Statistical inference and hypothesis testing.
    All original methods preserved + timing + pandas/polars compatibility.
    """

    @staticmethod
    def confidence_interval(series: pd.Series, confidence: float = 0.95,
                           method: str = 't', show_timing: bool = False) -> Tuple[float, float, float]:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        series = pd.Series(_to_pandas(series))
        # === ORIGINAL CODE (100% unchanged) ===
        data = series.dropna()
        n = len(data)
        mean = data.mean()
        std_err = data.std() / np.sqrt(n)

        if method == 't':
            df = n - 1
            alpha = 1 - confidence
            t_crit = stats.t.ppf(1 - alpha/2, df)
            margin_of_error = t_crit * std_err
        else:
            z_crit = stats.norm.ppf(1 - (1 - confidence) / 2)
            margin_of_error = z_crit * std_err

        lower = mean - margin_of_error
        upper = mean + margin_of_error

        table = RichTable(title=f"{int(confidence*100)}% Confidence Interval for Mean",
                         show_header=True, header_style="bold blue")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right", style="magenta")
        table.add_row("Sample Mean", f"{mean:.4f}")
        table.add_row("Standard Error", f"{std_err:.4f}")
        table.add_row("Margin of Error", f"{margin_of_error:.4f}")
        table.add_row("[bold]Lower Bound[/bold]", f"{lower:.4f}")
        table.add_row("[bold]Upper Bound[/bold]", f"{upper:.4f}")
        table.add_row("[bold]Confidence Interval[/bold]", f"[{lower:.4f}, {upper:.4f}]")
        console.print(table)
        console.print(f"[dim]Interpretation: We are {int(confidence*100)}% confident the true population mean is between {lower:.4f} and {upper:.4f}[/dim]")

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] inference.confidence_interval completed in {duration:.4f}s[/dim]")
        return lower, mean, upper

    @staticmethod
    def one_sample_ttest(sample: pd.Series, pop_mean: float, show_timing: bool = False) -> Dict[str, Union[float, str, bool]]:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        sample = pd.Series(_to_pandas(sample))
        # === ORIGINAL CODE (100% unchanged) ===
        data = sample.dropna()
        t_stat, p_value = stats.ttest_1samp(data, pop_mean)
        sample_std = data.std()
        cohens_d = (data.mean() - pop_mean) / sample_std

        if abs(cohens_d) < 0.2:
            effect = "negligible"
        elif abs(cohens_d) < 0.5:
            effect = "small"
        elif abs(cohens_d) < 0.8:
            effect = "medium"
        else:
            effect = "large"

        table = RichTable(title="One-Sample T-Test", show_header=True, header_style="bold blue")
        table.add_column("Statistic", style="cyan")
        table.add_column("Value", justify="right", style="magenta")
        table.add_row("Sample Mean", f"{data.mean():.4f}")
        table.add_row("Population Mean (H0)", f"{pop_mean:.4f}")
        table.add_row("Sample Size (N)", str(len(data)))
        table.add_row("T-Statistic", f"{t_stat:.4f}")
        table.add_row("P-Value (two-tailed)", f"{p_value:.4f}")
        table.add_row("Cohen's d", f"{cohens_d:.4f} ({effect})")
        console.print(table)

        if p_value < 0.05:
            console.print(f"[bold red]✗ REJECT H0: Sample mean is [bold]significantly different[/bold] from {pop_mean} (p={p_value:.4f})[/bold red]")
        else:
            console.print(f"[bold green]✓ FAIL TO REJECT H0: Sample mean is [bold]NOT significantly different[/bold] from {pop_mean} (p={p_value:.4f})[/bold green]")

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] inference.one_sample_ttest completed in {duration:.4f}s[/dim]")
        return {
            'sample_mean': data.mean(),
            'pop_mean': pop_mean,
            't_statistic': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'effect_size': effect,
            'significant': p_value < 0.05,
            'sample_size': len(data)
        }

    @staticmethod
    def two_sample_ttest(group1: pd.Series, group2: pd.Series,
                        equal_var: bool = True, show_timing: bool = False) -> Dict[str, Union[float, str, bool]]:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        group1 = pd.Series(_to_pandas(group1))
        group2 = pd.Series(_to_pandas(group2))
        # === ORIGINAL CODE (100% unchanged) ===
        g1 = group1.dropna()
        g2 = group2.dropna()
        levene_stat, levene_p = stats.levene(g1, g2)

        if levene_p < 0.05:
            t_stat, p_value = stats.ttest_ind(g1, g2, equal_var=False)
            test_type = "Welch's t-test (unequal variances)"
        else:
            t_stat, p_value = stats.ttest_ind(g1, g2, equal_var=True)
            test_type = "Student's t-test (equal variances)"

        u_stat, u_pval = stats.mannwhitneyu(g1, g2)
        pooled_std = np.sqrt((g1.std()**2 + g2.std()**2) / 2)
        cohens_d = (g1.mean() - g2.mean()) / pooled_std

        table = RichTable(title="Two-Sample T-Test", show_header=True, header_style="bold blue")
        table.add_column("Group/Test", style="cyan")
        table.add_column("Value", justify="right", style="magenta")
        table.add_row("Group 1 Mean", f"{g1.mean():.4f}")
        table.add_row("Group 2 Mean", f"{g2.mean():.4f}")
        table.add_row("Mean Difference", f"{(g1.mean() - g2.mean()):.4f}")
        table.add_row("", "")
        table.add_row("[bold]Parametric (T-Test)[/bold]", "")
        table.add_row("T-Statistic", f"{t_stat:.4f}")
        table.add_row("P-Value", f"{p_value:.4f}")
        table.add_row("Cohen's d", f"{cohens_d:.4f}")
        table.add_row("", "")
        table.add_row("[bold]Non-Parametric (Mann-Whitney U)[/bold]", "")
        table.add_row("U-Statistic", f"{u_stat:.4f}")
        table.add_row("P-Value", f"{u_pval:.4f}")
        console.print(table)

        if p_value < 0.05:
            console.print(f"[bold red]✗ REJECT H0: Groups have [bold]significantly different[/bold] means (p={p_value:.4f})[/bold red]")
        else:
            console.print(f"[bold green]✓ FAIL TO REJECT H0: Groups have [bold]NOT significantly different[/bold] means (p={p_value:.4f})[/bold green]")
        console.print(f"[dim]Using {test_type}[/dim]")

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] inference.two_sample_ttest completed in {duration:.4f}s[/dim]")
        return {
            'mean1': g1.mean(),
            'mean2': g2.mean(),
            'mean_diff': g1.mean() - g2.mean(),
            't_statistic': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'u_statistic': u_stat,
            'u_pvalue': u_pval,
            'significant': p_value < 0.05,
            'test_type': test_type
        }

    @staticmethod
    def paired_ttest(before: pd.Series, after: pd.Series, show_timing: bool = False) -> Dict[str, Union[float, str, bool]]:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        before = pd.Series(_to_pandas(before))
        after = pd.Series(_to_pandas(after))
        # === ORIGINAL CODE (100% unchanged) ===
        paired_data = pd.DataFrame({'before': before, 'after': after}).dropna()
        differences = paired_data['after'] - paired_data['before']
        t_stat, p_value = stats.ttest_1samp(differences, 0)
        cohens_d = differences.mean() / differences.std()

        table = RichTable(title="Paired T-Test", show_header=True, header_style="bold blue")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right", style="magenta")
        table.add_row("Mean Before", f"{paired_data['before'].mean():.4f}")
        table.add_row("Mean After", f"{paired_data['after'].mean():.4f}")
        table.add_row("Mean Difference", f"{differences.mean():.4f}")
        table.add_row("T-Statistic", f"{t_stat:.4f}")
        table.add_row("P-Value", f"{p_value:.4f}")
        table.add_row("Cohen's d", f"{cohens_d:.4f}")
        console.print(table)

        if p_value < 0.05:
            console.print(f"[bold red]✗ REJECT H0: Significant change from before to after (p={p_value:.4f})[/bold red]")
        else:
            console.print(f"[bold green]✓ FAIL TO REJECT H0: No significant change (p={p_value:.4f})[/bold green]")

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] inference.paired_ttest completed in {duration:.4f}s[/dim]")
        return {
            'mean_before': paired_data['before'].mean(),
            'mean_after': paired_data['after'].mean(),
            'mean_difference': differences.mean(),
            't_statistic': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'significant': p_value < 0.05,
            'sample_size': len(paired_data)
        }

    @staticmethod
    def anova_test(groups_dict: Dict[str, pd.Series], show_timing: bool = False) -> Dict[str, Union[float, str, bool]]:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        # Convert all series
        groups_dict = {k: pd.Series(_to_pandas(v)) for k, v in groups_dict.items()}
        # === ORIGINAL CODE (100% unchanged) ===
        groups = [series.dropna().values for series in groups_dict.values()]
        f_stat, p_value = stats.f_oneway(*groups)

        all_data = np.concatenate(groups)
        grand_mean = all_data.mean()
        ss_between = sum(len(g) * (g.mean() - grand_mean)**2 for g in groups)
        ss_total = sum((all_data - grand_mean)**2)
        eta_squared = ss_between / ss_total

        if eta_squared < 0.01:
            effect = "negligible"
        elif eta_squared < 0.06:
            effect = "small"
        elif eta_squared < 0.14:
            effect = "medium"
        else:
            effect = "large"

        table = RichTable(title="One-Way ANOVA", show_header=True, header_style="bold blue")
        table.add_column("Group", style="cyan")
        table.add_column("N", justify="right")
        table.add_column("Mean", justify="right", style="magenta")
        table.add_column("Std Dev", justify="right")
        for name, series in groups_dict.items():
            s = series.dropna()
            table.add_row(name, str(len(s)), f"{s.mean():.4f}", f"{s.std():.4f}")
        table.add_row("", "", "", "")
        table.add_row("[bold]F-Statistic[/bold]", f"{f_stat:.4f}", "", "")
        table.add_row("[bold]P-Value[/bold]", f"{p_value:.4f}", "", "")
        table.add_row("[bold]Eta-Squared[/bold]", f"{eta_squared:.4f} ({effect})", "", "")
        console.print(table)

        if p_value < 0.05:
            console.print(f"[bold red]✗ REJECT H0: At least one group mean is [bold]significantly different[/bold] (p={p_value:.4f})[/bold red]")
            console.print("[dim]Post-hoc test (Tukey) recommended to identify which groups differ[/dim]")
        else:
            console.print(f"[bold green]✓ FAIL TO REJECT H0: No significant difference among groups (p={p_value:.4f})[/bold green]")

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] inference.anova_test completed in {duration:.4f}s[/dim]")
        return {
            'f_statistic': f_stat,
            'p_value': p_value,
            'eta_squared': eta_squared,
            'effect_size': effect,
            'significant': p_value < 0.05,
            'num_groups': len(groups_dict)
        }

    @staticmethod
    def correlation_test(x: pd.Series, y: pd.Series, show_timing: bool = False) -> Dict[str, Union[float, str]]:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        x = pd.Series(_to_pandas(x))
        y = pd.Series(_to_pandas(y))
        # === ORIGINAL CODE (100% unchanged) ===
        valid_data = pd.DataFrame({'x': x, 'y': y}).dropna()
        x_clean = valid_data['x']
        y_clean = valid_data['y']

        r, p_pearson = stats.pearsonr(x_clean, y_clean)
        rho, p_spearman = stats.spearmanr(x_clean, y_clean)

        if len(x_clean) > 3:
            se = 1 / np.sqrt(len(x_clean) - 3)
            z = 0.5 * np.log((1 + r) / (1 - r))
            ci_lower_z = z - 1.96 * se
            ci_upper_z = z + 1.96 * se
            ci_lower = (np.exp(2 * ci_lower_z) - 1) / (np.exp(2 * ci_lower_z) + 1)
            ci_upper = (np.exp(2 * ci_upper_z) - 1) / (np.exp(2 * ci_upper_z) + 1)
        else:
            ci_lower = ci_upper = np.nan

        table = RichTable(title="Correlation Test", show_header=True, header_style="bold blue")
        table.add_column("Test", style="cyan")
        table.add_column("Coefficient", justify="right", style="magenta")
        table.add_column("P-Value", justify="right", style="yellow")
        table.add_column("Significant", style="green")

        sig_p = "✓ Yes" if p_pearson < 0.05 else "✗ No"
        sig_s = "✓ Yes" if p_spearman < 0.05 else "✗ No"

        table.add_row("Pearson r", f"{r:.4f}", f"{p_pearson:.4f}", sig_p)
        table.add_row("Spearman ρ", f"{rho:.4f}", f"{p_spearman:.4f}", sig_s)
        table.add_row("95% CI (Pearson)", f"[{ci_lower:.4f}, {ci_upper:.4f}]", "", "")

        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] inference.correlation_test completed in {duration:.4f}s[/dim]")
        return {
            'pearson_r': r,
            'pearson_p': p_pearson,
            'spearman_rho': rho,
            'spearman_p': p_spearman,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'significant': p_pearson < 0.05,
            'sample_size': len(x_clean)
        }

    @staticmethod
    def effect_size_interpreter(effect_size: float, test_type: str = "cohens_d", show_timing: bool = False) -> str:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        # === ORIGINAL CODE (100% unchanged) ===
        abs_effect = abs(effect_size)
        if test_type == "cohens_d":
            if abs_effect < 0.2:
                result = "Negligible (d < 0.2)"
            elif abs_effect < 0.5:
                result = "Small (0.2 ≤ d < 0.5)"
            elif abs_effect < 0.8:
                result = "Medium (0.5 ≤ d < 0.8)"
            else:
                result = "Large (d ≥ 0.8)"
        elif test_type == "eta_squared":
            if effect_size < 0.01:
                result = "Negligible (η² < 0.01)"
            elif effect_size < 0.06:
                result = "Small (0.01 ≤ η² < 0.06)"
            elif effect_size < 0.14:
                result = "Medium (0.06 ≤ η² < 0.14)"
            else:
                result = "Large (η² ≥ 0.14)"
        elif test_type == "cramers_v":
            if effect_size < 0.1:
                result = "Negligible (V < 0.1)"
            elif effect_size < 0.3:
                result = "Small (0.1 ≤ V < 0.3)"
            elif effect_size < 0.5:
                result = "Medium (0.3 ≤ V < 0.5)"
            else:
                result = "Large (V ≥ 0.5)"
        else:
            result = "Unknown"

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] inference.effect_size_interpreter completed in {duration:.4f}s[/dim]")
        return result