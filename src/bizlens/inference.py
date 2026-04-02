"""
BizLens Inference Module — Statistical Inference & Hypothesis Testing
Version: 2.2.11
Purpose: Perform hypothesis tests, confidence intervals, and statistical comparisons
Teaching Focus: Understanding p-values, effect sizes, statistical significance,
                parametric vs non-parametric tests

Dependencies:
- pandas, numpy (data manipulation)
- scipy.stats (statistical distributions and tests)
- statsmodels.stats (advanced statistical inference)
- rich (console output)
"""

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.proportion import proportions_ztest
from rich.table import Table as RichTable
from rich.console import Console
from typing import Union, Tuple, Dict, List

console = Console()


class inference:
    """
    Statistical inference and hypothesis testing.

    **Purpose (Educational):**
    Inference answers: "Can I generalize from my sample to the population?"
    These methods help you:
    - Estimate population parameters from samples
    - Test hypotheses about populations
    - Quantify uncertainty with confidence intervals
    - Assess practical significance with effect sizes

    **Key Principle (Critical for Learning):**
    p-value ≠ probability of hypothesis being true!
    p-value = probability of observing this data IF null hypothesis were true.
    If p < 0.05, we reject the null hypothesis, but we never "accept" it.
    """

    @staticmethod
    def confidence_interval(series: pd.Series, confidence: float = 0.95,
                           method: str = 't') -> Tuple[float, float, float]:
        """
        Calculate confidence interval for the mean.

        **What this does (Educational):**
        A confidence interval gives a range of plausible values for the population mean.
        "95% confidence" means: if we repeated sampling 100 times, 95 intervals would contain
        the true population mean.

        **Parameters:**
        -----------
        series : pd.Series
            Sample data
        confidence : float, default=0.95
            Confidence level (0.90, 0.95, or 0.99)
        method : str, default='t'
            't' (t-distribution, for samples < 30) or 'z' (normal, for large samples)

        **Returns:**
        --------
        Tuple[float, float, float]
            (lower_bound, mean, upper_bound)

        **Example:**
        -----------
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> data = pd.Series([1, 2, 3, 4, 5])
        >>> lower, mean, upper = bl.inference.confidence_interval(data)

        **Educational Notes:**
        - Wider confidence interval = more uncertainty
        - Narrower interval = more precision (larger sample size helps)
        - 95% CI uses different multiplier than 99% CI
        """
        data = series.dropna()
        n = len(data)
        mean = data.mean()
        std_err = data.std() / np.sqrt(n)

        # LEARNING POINT: t-distribution used for small samples, z for large
        if method == 't':
            df = n - 1
            alpha = 1 - confidence
            t_crit = stats.t.ppf(1 - alpha/2, df)
            margin_of_error = t_crit * std_err
        else:  # z method
            z_crit = stats.norm.ppf(1 - (1 - confidence) / 2)
            margin_of_error = z_crit * std_err

        lower = mean - margin_of_error
        upper = mean + margin_of_error

        # Display results
        table = RichTable(title=f"{int(confidence*100)}% Confidence Interval for Mean",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right", style="magenta")

        table.add_row("Sample Mean", f"{mean:.4f}")
        table.add_row("Standard Error", f"{std_err:.4f}")
        table.add_row("Margin of Error", f"{margin_of_error:.4f}")
        table.add_row("[bold]Lower Bound[/bold]", f"{lower:.4f}")
        table.add_row("[bold]Upper Bound[/bold]", f"{upper:.4f}")
        table.add_row("[bold]Confidence Interval[/bold]", f"[{lower:.4f}, {upper:.4f}]")

        console.print(table)
        console.print(f"[dim]Interpretation: We are {int(confidence*100)}% confident the true population mean")
        console.print(f"is between {lower:.4f} and {upper:.4f}[/dim]")

        return lower, mean, upper

    @staticmethod
    def one_sample_ttest(sample: pd.Series, pop_mean: float) -> Dict[str, Union[float, str, bool]]:
        """
        One-sample t-test: Compare sample mean to a known population mean.

        **What this does (Educational):**
        Tests if a sample's mean is significantly different from a population mean.
        Example: "Is the average weight of our sample different from 70 kg (population)?"

        **Parameters:**
        -----------
        sample : pd.Series
            Sample data
        pop_mean : float
            Population mean to compare against (null hypothesis)

        **Returns:**
        --------
        dict
            Test results with interpretation

        **Example:**
        -----------
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> sample = pd.Series([72, 68, 70, 75, 69])
        >>> results = bl.inference.one_sample_ttest(sample, pop_mean=70)

        **Educational Notes:**
        - **Null Hypothesis (H0):** Sample mean = population mean
        - **Alternative (H1):** Sample mean ≠ population mean
        - **p-value < 0.05:** Reject H0, means are significantly different
        - **Cohen's d:** Effect size (0.2=small, 0.5=medium, 0.8=large)
        """
        data = sample.dropna()

        # LEARNING POINT: One-sample t-test compares one group to a known value
        t_stat, p_value = stats.ttest_1samp(data, pop_mean)

        # Calculate Cohen's d (effect size)
        # LEARNING POINT: Effect size tells us practical significance (not just statistical)
        sample_std = data.std()
        cohens_d = (data.mean() - pop_mean) / sample_std

        # Effect size interpretation
        if abs(cohens_d) < 0.2:
            effect = "negligible"
        elif abs(cohens_d) < 0.5:
            effect = "small"
        elif abs(cohens_d) < 0.8:
            effect = "medium"
        else:
            effect = "large"

        # Display results
        table = RichTable(title="One-Sample T-Test",
                         show_header=True,
                         header_style="bold blue")
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
                        equal_var: bool = True) -> Dict[str, Union[float, str, bool]]:
        """
        Two-sample t-test: Compare means between two independent groups.

        **What this does (Educational):**
        Tests if two groups have significantly different means.
        Example: "Is treatment group different from control group?"

        **Parameters:**
        -----------
        group1, group2 : pd.Series
            Two independent samples
        equal_var : bool, default=True
            Assume equal variances (homogeneity of variance)

        **Returns:**
        --------
        dict
            Test results and recommendations

        **Example:**
        -----------
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> control = pd.Series([1, 2, 3, 4])
        >>> treatment = pd.Series([2, 3, 4, 5])
        >>> results = bl.inference.two_sample_ttest(control, treatment)

        **Educational Notes:**
        - Parametric test: assumes normal distributions
        - Checks homogeneity of variance (Levene's test)
        - If variance unequal, uses Welch's t-test
        - Non-parametric fallback: Mann-Whitney U test
        """
        g1 = group1.dropna()
        g2 = group2.dropna()

        # Test for equal variances (Levene's test)
        # LEARNING POINT: Homogeneity of variance is assumption of t-test
        levene_stat, levene_p = stats.levene(g1, g2)

        # Perform appropriate t-test
        if levene_p < 0.05:
            # Variances are unequal, use Welch's t-test
            t_stat, p_value = stats.ttest_ind(g1, g2, equal_var=False)
            test_type = "Welch's t-test (unequal variances)"
        else:
            t_stat, p_value = stats.ttest_ind(g1, g2, equal_var=True)
            test_type = "Student's t-test (equal variances)"

        # Non-parametric alternative (Mann-Whitney U)
        u_stat, u_pval = stats.mannwhitneyu(g1, g2)

        # Calculate Cohen's d (effect size)
        pooled_std = np.sqrt((g1.std()**2 + g2.std()**2) / 2)
        cohens_d = (g1.mean() - g2.mean()) / pooled_std

        # Display results
        table = RichTable(title="Two-Sample T-Test",
                         show_header=True,
                         header_style="bold blue")
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
    def paired_ttest(before: pd.Series, after: pd.Series) -> Dict[str, Union[float, str, bool]]:
        """
        Paired t-test: Compare means for dependent samples (same subjects measured twice).

        **What this does (Educational):**
        Tests if a variable changed significantly from before to after treatment.
        Example: "Did blood pressure decrease after medication?"

        **Parameters:**
        -----------
        before, after : pd.Series
            Measurements before and after (same subjects)

        **Returns:**
        --------
        dict
            Test results and interpretation
        """
        # Match rows and calculate differences
        paired_data = pd.DataFrame({'before': before, 'after': after}).dropna()
        differences = paired_data['after'] - paired_data['before']

        # LEARNING POINT: Paired t-test uses differences, not raw values
        # This makes it more powerful (removes individual variation)
        t_stat, p_value = stats.ttest_1samp(differences, 0)

        # Calculate Cohen's d based on differences
        cohens_d = differences.mean() / differences.std()

        # Display results
        table = RichTable(title="Paired T-Test",
                         show_header=True,
                         header_style="bold blue")
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
    def anova_test(groups_dict: Dict[str, pd.Series]) -> Dict[str, Union[float, str, bool]]:
        """
        One-way ANOVA: Compare means across 3+ groups.

        **What this does (Educational):**
        Tests if 3 or more groups have significantly different means.
        More efficient than multiple t-tests (avoids multiple comparison problem).

        **Parameters:**
        -----------
        groups_dict : Dict[str, pd.Series]
            Dictionary of group_name: series pairs

        **Returns:**
        --------
        dict
            ANOVA results with effect size

        **Example:**
        -----------
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> results = bl.inference.anova_test({
        ...     'A': pd.Series([1, 2, 3]),
        ...     'B': pd.Series([4, 5, 6]),
        ...     'C': pd.Series([7, 8, 9])
        ... })

        **Educational Notes:**
        - **Null Hypothesis:** All group means are equal
        - **F-statistic:** Ratio of between-group to within-group variation
        - **Eta-squared (η²):** Effect size (0.01=small, 0.06=medium, 0.14=large)
        """
        # Extract groups and calculate ANOVA
        groups = [series.dropna().values for series in groups_dict.values()]
        f_stat, p_value = stats.f_oneway(*groups)

        # Calculate eta-squared (effect size)
        # LEARNING POINT: η² = between-group SS / total SS
        all_data = np.concatenate(groups)
        grand_mean = all_data.mean()
        ss_between = sum(len(g) * (g.mean() - grand_mean)**2 for g in groups)
        ss_total = sum((all_data - grand_mean)**2)
        eta_squared = ss_between / ss_total

        # Effect size interpretation
        if eta_squared < 0.01:
            effect = "negligible"
        elif eta_squared < 0.06:
            effect = "small"
        elif eta_squared < 0.14:
            effect = "medium"
        else:
            effect = "large"

        # Display results
        table = RichTable(title="One-Way ANOVA",
                         show_header=True,
                         header_style="bold blue")
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

        return {
            'f_statistic': f_stat,
            'p_value': p_value,
            'eta_squared': eta_squared,
            'effect_size': effect,
            'significant': p_value < 0.05,
            'num_groups': len(groups_dict)
        }

    @staticmethod
    def correlation_test(x: pd.Series, y: pd.Series) -> Dict[str, Union[float, str]]:
        """
        Test significance of correlation and calculate confidence interval.

        **What this does (Educational):**
        Tests if correlation between two variables is statistically significant.
        Provides both Pearson (parametric) and Spearman (non-parametric) tests.

        **Parameters:**
        -----------
        x, y : pd.Series
            Two variables to correlate

        **Returns:**
        --------
        dict
            Correlation test results
        """
        # Remove missing values
        valid_data = pd.DataFrame({'x': x, 'y': y}).dropna()
        x_clean = valid_data['x']
        y_clean = valid_data['y']

        # Pearson correlation
        r, p_pearson = stats.pearsonr(x_clean, y_clean)

        # Spearman correlation
        rho, p_spearman = stats.spearmanr(x_clean, y_clean)

        # Fisher's z-transformation for confidence interval
        # LEARNING POINT: Z = 0.5 * ln((1+r)/(1-r)), used to calculate CI
        if len(x_clean) > 3:
            se = 1 / np.sqrt(len(x_clean) - 3)
            z = 0.5 * np.log((1 + r) / (1 - r))
            ci_lower_z = z - 1.96 * se
            ci_upper_z = z + 1.96 * se
            ci_lower = (np.exp(2 * ci_lower_z) - 1) / (np.exp(2 * ci_lower_z) + 1)
            ci_upper = (np.exp(2 * ci_upper_z) - 1) / (np.exp(2 * ci_upper_z) + 1)
        else:
            ci_lower = ci_upper = np.nan

        # Display results
        table = RichTable(title="Correlation Test",
                         show_header=True,
                         header_style="bold blue")
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
    def effect_size_interpreter(effect_size: float, test_type: str = "cohens_d") -> str:
        """
        Interpret effect size magnitude.

        **What this does (Educational):**
        Effect size indicates practical significance (not just statistical significance).
        p-value can be significant but effect can be negligible.

        **Parameters:**
        -----------
        effect_size : float
            The effect size value
        test_type : str
            Type of effect size: 'cohens_d', 'eta_squared', 'cramers_v'

        **Returns:**
        --------
        str
            Interpretation of effect size magnitude
        """
        abs_effect = abs(effect_size)

        if test_type == "cohens_d":
            if abs_effect < 0.2:
                return "Negligible (d < 0.2)"
            elif abs_effect < 0.5:
                return "Small (0.2 ≤ d < 0.5)"
            elif abs_effect < 0.8:
                return "Medium (0.5 ≤ d < 0.8)"
            else:
                return "Large (d ≥ 0.8)"

        elif test_type == "eta_squared":
            if effect_size < 0.01:
                return "Negligible (η² < 0.01)"
            elif effect_size < 0.06:
                return "Small (0.01 ≤ η² < 0.06)"
            elif effect_size < 0.14:
                return "Medium (0.06 ≤ η² < 0.14)"
            else:
                return "Large (η² ≥ 0.14)"

        elif test_type == "cramers_v":
            if effect_size < 0.1:
                return "Negligible (V < 0.1)"
            elif effect_size < 0.3:
                return "Small (0.1 ≤ V < 0.3)"
            elif effect_size < 0.5:
                return "Medium (0.3 ≤ V < 0.5)"
            else:
                return "Large (V ≥ 0.5)"

        return "Unknown"
