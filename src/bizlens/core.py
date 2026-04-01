"""
BizLens v2.1.0 — Integrated Analytics Platform
Descriptive · Diagnostic · Predictive · Optimization

Core module providing unified analytics with:
- Sample vs Population distinction (n-1 vs n)
- Narwhals-based DataFrame support (Polars + Pandas)
- Educational output with formulas and interpretation
- Professional visualizations with multiple color schemes
"""

import warnings
import numpy as np
import pandas as pd
import polars as pl
import narwhals as nw
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
# HELPER: Load native data as numpy array
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
# DESCRIPTIVE ANALYTICS
# ─────────────────────────────────────────────────────────────────────────────

def describe(
    data,
    calculation_level: str = "sample",
    show_formula: bool = True,
    color_scheme: str = "academic",
    include_plots: bool = False,
) -> Dict[str, Any]:
    """
    Comprehensive descriptive statistics with sample vs population distinction.

    Args:
        data: 1D array, pandas Series, polars Series, or list of numbers
        calculation_level: 'sample' (n-1, default) or 'population' (n)
        show_formula: Display mathematical formulas in output
        color_scheme: 'academic', 'pastel', or 'vibrant'
        include_plots: Generate histogram and boxplot

    Returns:
        Dictionary with all statistics and interpretation

    Example:
        >>> import bizlens as bl
        >>> stats = bl.describe([10, 20, 30, 40, 50], calculation_level='sample')
        >>> print(stats['mean'], stats['std'])

    Formula:
        Sample std: s = sqrt(Σ(xi - x̄)² / (n-1))   ← Corrects for bias
        Population std: σ = sqrt(Σ(xi - μ)² / n)    ← When you have ALL data
    """
    if calculation_level not in ("sample", "population"):
        raise ValueError("calculation_level must be 'sample' or 'population'")

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

    # Distribution shape interpretation
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

    # Rich console output
    colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])
    table = Table(title=f"📊 BizLens Descriptive Statistics [{calculation_level.upper()}]",
                  style="bold", show_lines=True)
    table.add_column("Statistic", style="cyan", width=22)
    table.add_column("Value", style="green", justify="right", width=14)
    table.add_column("Formula / Note", style="dim", width=40)

    rows = [
        ("Count (n)", str(n), "Number of valid observations"),
        ("Mean (x̄ / μ)", f"{mean_val:.4f}", "Σxᵢ / n"),
        ("Median", f"{median_val:.4f}", "Middle value when sorted"),
        ("Mode", f"{mode_val:.4f}", "Most frequently occurring value"),
        (f"Std Dev ({symbol})", f"{std_val:.4f}",
         f"√(Σ(xᵢ-x̄)² / (n-{ddof}))  ← {'n-1 corrects bias' if ddof==1 else 'population formula'}"),
        (f"Variance ({var_symbol})", f"{var_val:.4f}", f"Σ(xᵢ-x̄)² / (n-{ddof})"),
        ("Min / Max", f"{np.min(arr):.4f} / {np.max(arr):.4f}", "Minimum and maximum values"),
        ("Range", f"{result['range']:.4f}", "Max − Min"),
        ("Q1 / Q3", f"{q1:.4f} / {q3:.4f}", "25th and 75th percentiles"),
        ("IQR", f"{iqr_val:.4f}", "Q3 − Q1 (middle 50% spread)"),
        ("Skewness", f"{skew_val:.4f}", shape),
        ("Kurtosis", f"{kurt_val:.4f}", ">0 heavy tails, <0 light tails"),
        ("CV (%)", f"{cv_val:.2f}%", "(std / mean) × 100 — relative spread"),
    ]
    for stat, val, note in rows:
        table.add_row(stat, val, note)

    console.print(table)

    if show_formula:
        console.print(f"\n[bold yellow]📐 Formula Used ({calculation_level}):[/bold yellow]")
        if calculation_level == "sample":
            console.print("  s = √( Σ(xᵢ − x̄)² / (n−1) )")
            console.print("  [dim]Using n−1 (Bessel's correction) because we are estimating from a SAMPLE[/dim]")
        else:
            console.print("  σ = √( Σ(xᵢ − μ)² / n )")
            console.print("  [dim]Using n because we have the FULL POPULATION[/dim]")

    if include_plots:
        _plot_describe(arr, result, color_scheme)

    return result


def compare_sample_population(data) -> Dict[str, Any]:
    """
    Show side-by-side comparison of sample vs population statistics.
    Key educational tool demonstrating why n-1 matters.

    Example:
        >>> bl.compare_sample_population([10, 20, 30, 40, 50])
    """
    arr = _to_numpy(data)
    sample = describe(arr, calculation_level="sample", show_formula=False)
    pop = describe(arr, calculation_level="population", show_formula=False)

    table = Table(title="⚖️  Sample vs Population Comparison", show_lines=True)
    table.add_column("Statistic", style="cyan", width=18)
    table.add_column("Sample (n-1)", style="green", justify="right", width=14)
    table.add_column("Population (n)", style="yellow", justify="right", width=14)
    table.add_column("Difference", style="red", justify="right", width=12)

    for key in ("std", "variance", "cv_percent"):
        s_val = sample[key]
        p_val = pop[key]
        diff = round(s_val - p_val, 6)
        table.add_row(key, str(s_val), str(p_val), f"+{diff}" if diff > 0 else str(diff))

    console.print(table)
    console.print("\n[bold]💡 Why n-1?[/bold] A sample underestimates spread. Dividing by n-1 corrects this bias.")
    return {"sample": sample, "population": pop}


def _plot_describe(arr: np.ndarray, result: Dict, color_scheme: str = "academic"):
    """Internal: generate histogram and boxplot."""
    colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Histogram
    axes[0].hist(arr, bins="auto", color=colors["primary"], edgecolor="white", alpha=0.85)
    axes[0].axvline(result["mean"], color=colors["danger"], linestyle="--", linewidth=2, label=f"Mean: {result['mean']:.2f}")
    axes[0].axvline(result["median"], color=colors["secondary"], linestyle="-.", linewidth=2, label=f"Median: {result['median']:.2f}")
    axes[0].set_title(f"Distribution ({result['distribution_shape']})", fontsize=12, fontweight="bold")
    axes[0].legend()
    axes[0].set_xlabel("Value")
    axes[0].set_ylabel("Frequency")

    # Boxplot
    bp = axes[1].boxplot(arr, patch_artist=True, notch=False)
    bp["boxes"][0].set_facecolor(colors["primary"])
    axes[1].set_title(f"Boxplot  |  IQR: {result['iqr']:.2f}  |  Skew: {result['skewness']:.2f}", fontsize=12, fontweight="bold")
    axes[1].set_ylabel("Value")

    plt.suptitle(f"BizLens Descriptive Analytics [{result['calculation_level'].upper()}]", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# DATAFRAME DESCRIBE (for full datasets)
# ─────────────────────────────────────────────────────────────────────────────

class BizDesc:
    """
    Full-DataFrame descriptive analytics engine.
    Accepts Polars, Pandas, or any narwhals-compatible frame.

    Example:
        >>> import pandas as pd
        >>> import bizlens as bl
        >>> df = pd.read_csv('sales.csv')
        >>> bd = bl.BizDesc(df)
        >>> bd.summary(calculation_level='sample', include_plots=True)
    """

    def __init__(self, data: Union[IntoFrame, str, Path]):
        if isinstance(data, (str, Path)):
            path = Path(data)
            if path.suffix == ".csv":
                native = pl.read_csv(path)
            elif path.suffix in (".xlsx", ".xls"):
                native = pd.read_excel(path)
            elif path.suffix == ".parquet":
                native = pl.read_parquet(path)
            else:
                raise ValueError(f"Unsupported file type: {path.suffix}")
            self.df = nw.from_native(native, eager_only=True)
        else:
            self.df = nw.from_native(data, eager_only=True)

    def summary(
        self,
        calculation_level: str = "sample",
        include_plots: bool = False,
        color_scheme: str = "academic",
    ) -> Dict[str, Any]:
        """
        Generate descriptive statistics for all numeric columns.

        Args:
            calculation_level: 'sample' (n-1) or 'population' (n)
            include_plots: Generate plots for each numeric column
            color_scheme: 'academic', 'pastel', or 'vibrant'
        """
        ddof = 1 if calculation_level == "sample" else 0
        numeric_cols = self.df.select(nw.col(nw.NUMERIC_DTYPES)).columns
        results = {}

        table = Table(
            title=f"📊 BizLens DataFrame Summary [{calculation_level.upper()}]",
            show_lines=True
        )
        table.add_column("Column", style="cyan", width=18)
        table.add_column("n", justify="right", width=6)
        table.add_column("Mean", justify="right", width=10)
        table.add_column("Median", justify="right", width=10)
        table.add_column("Std Dev", justify="right", width=10)
        table.add_column("Min", justify="right", width=10)
        table.add_column("Max", justify="right", width=10)
        table.add_column("Skew", justify="right", width=8)
        table.add_column("Missing", justify="right", width=8)

        for col in numeric_cols:
            arr = _to_numpy(self.df[col].to_numpy())
            n = len(arr)
            if n == 0:
                continue
            missing = int(self.df[col].null_count())
            mean_v = round(float(np.mean(arr)), 3)
            median_v = round(float(np.median(arr)), 3)
            std_v = round(float(np.std(arr, ddof=ddof)), 3)
            min_v = round(float(np.min(arr)), 3)
            max_v = round(float(np.max(arr)), 3)
            skew_v = round(float(sp_stats.skew(arr)), 3)

            table.add_row(col, str(n), str(mean_v), str(median_v),
                          str(std_v), str(min_v), str(max_v),
                          str(skew_v), str(missing))

            results[col] = {
                "n": n, "mean": mean_v, "median": median_v, "std": std_v,
                "min": min_v, "max": max_v, "skewness": skew_v, "missing": missing,
            }

        console.print(table)
        console.print(f"\n[dim]Std Dev calculated using {'n-1 (sample)' if ddof==1 else 'n (population)'} denominator.[/dim]")

        if include_plots:
            colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])
            for col in numeric_cols[:6]:  # limit to 6 plots
                arr = _to_numpy(self.df[col].to_numpy())
                if len(arr) == 0:
                    continue
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(arr, bins="auto", color=colors["primary"], edgecolor="white", alpha=0.85)
                ax.axvline(np.mean(arr), color=colors["danger"], linestyle="--", label="Mean")
                ax.axvline(np.median(arr), color=colors["secondary"], linestyle="-.", label="Median")
                ax.set_title(f"{col} Distribution [{calculation_level}]", fontweight="bold")
                ax.legend()
                plt.tight_layout()
                plt.show()

        return results


# ─────────────────────────────────────────────────────────────────────────────
# DIAGNOSTIC ANALYTICS
# ─────────────────────────────────────────────────────────────────────────────

class diagnostic:
    """
    Diagnostic analytics: hypothesis testing, correlations, assumptions.

    Example:
        >>> bl.diagnostic.ttest(group1, group2)
        >>> bl.diagnostic.correlation(df, method='pearson')
        >>> bl.diagnostic.chi_square(df, col1, col2)
    """

    @staticmethod
    def ttest(
        group1,
        group2,
        alternative: str = "two-sided",
        alpha: float = 0.05,
    ) -> Dict[str, Any]:
        """
        Independent samples t-test comparing two groups.

        Args:
            group1: First group data
            group2: Second group data
            alternative: 'two-sided', 'less', or 'greater'
            alpha: Significance level (default 0.05)

        Returns:
            Dict with t-statistic, p-value, conclusion, effect size (Cohen's d)

        Formula:
            t = (x̄₁ - x̄₂) / √(s₁²/n₁ + s₂²/n₂)
            Cohen's d = |x̄₁ - x̄₂| / pooled_std
        """
        a = _to_numpy(group1)
        b = _to_numpy(group2)
        t_stat, p_val = sp_stats.ttest_ind(a, b, alternative=alternative)

        pooled_std = np.sqrt((np.std(a, ddof=1)**2 + np.std(b, ddof=1)**2) / 2)
        cohens_d = abs(np.mean(a) - np.mean(b)) / pooled_std if pooled_std > 0 else 0

        significant = p_val < alpha
        conclusion = (
            f"SIGNIFICANT (p={p_val:.4f} < α={alpha}): Groups differ meaningfully."
            if significant else
            f"NOT significant (p={p_val:.4f} ≥ α={alpha}): No strong evidence of difference."
        )

        result = {
            "t_statistic": round(float(t_stat), 4),
            "p_value": round(float(p_val), 6),
            "significant": significant,
            "alpha": alpha,
            "cohens_d": round(float(cohens_d), 4),
            "effect_size": "large" if cohens_d > 0.8 else "medium" if cohens_d > 0.5 else "small",
            "group1_mean": round(float(np.mean(a)), 4),
            "group2_mean": round(float(np.mean(b)), 4),
            "group1_n": len(a),
            "group2_n": len(b),
            "conclusion": conclusion,
        }

        table = Table(title="🔬 Independent Samples t-Test", show_lines=True)
        table.add_column("Metric", style="cyan", width=22)
        table.add_column("Value", style="green", justify="right", width=16)
        for k, v in [
            ("Group 1: n / Mean", f"{len(a)} / {np.mean(a):.4f}"),
            ("Group 2: n / Mean", f"{len(b)} / {np.mean(b):.4f}"),
            ("t-statistic", f"{t_stat:.4f}"),
            ("p-value", f"{p_val:.6f}"),
            ("Cohen's d (effect)", f"{cohens_d:.4f} ({result['effect_size']})"),
            ("Significant?", "✅ YES" if significant else "❌ NO"),
        ]:
            table.add_row(k, str(v))
        console.print(table)
        console.print(f"\n[bold]📌 Conclusion:[/bold] {conclusion}")
        return result

    @staticmethod
    def anova(*groups, alpha: float = 0.05) -> Dict[str, Any]:
        """One-way ANOVA for comparing 3+ groups."""
        arrays = [_to_numpy(g) for g in groups]
        f_stat, p_val = sp_stats.f_oneway(*arrays)
        significant = p_val < alpha
        result = {
            "f_statistic": round(float(f_stat), 4),
            "p_value": round(float(p_val), 6),
            "significant": significant,
            "conclusion": "Significant group differences" if significant else "No significant differences",
        }
        console.print(f"[bold]ANOVA[/bold]: F={f_stat:.4f}, p={p_val:.6f} — {'✅ Significant' if significant else '❌ Not significant'}")
        return result

    @staticmethod
    def chi_square(data: Union[pd.DataFrame, pl.DataFrame], col1: str, col2: str,
                   alpha: float = 0.05) -> Dict[str, Any]:
        """Chi-square test of independence for two categorical variables."""
        if isinstance(data, pl.DataFrame):
            df = data.to_pandas()
        else:
            df = data
        contingency = pd.crosstab(df[col1], df[col2])
        chi2, p_val, dof, expected = sp_stats.chi2_contingency(contingency)
        significant = p_val < alpha
        result = {
            "chi2_statistic": round(float(chi2), 4),
            "p_value": round(float(p_val), 6),
            "degrees_of_freedom": int(dof),
            "significant": significant,
            "conclusion": f"{'✅ Significant' if significant else '❌ Not significant'} association (p={p_val:.4f})",
        }
        console.print(f"[bold]Chi-Square[/bold]: χ²={chi2:.4f}, df={dof}, p={p_val:.6f} — {result['conclusion']}")
        return result

    @staticmethod
    def correlation(
        data,
        method: str = "pearson",
        target: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Correlation matrix or target correlations.

        Args:
            data: DataFrame (pandas or polars)
            method: 'pearson', 'spearman', or 'kendall'
            target: If set, show correlations with this column only

        Returns:
            Correlation DataFrame
        """
        if isinstance(data, pl.DataFrame):
            df = data.to_pandas()
        elif isinstance(data, pd.DataFrame):
            df = data
        else:
            raise ValueError("data must be a pandas or polars DataFrame")

        numeric_df = df.select_dtypes(include=np.number)
        corr_matrix = numeric_df.corr(method=method)

        if target:
            result = corr_matrix[[target]].drop(target).sort_values(target, ascending=False)
            console.print(f"[bold]🔗 {method.capitalize()} Correlations with '{target}':[/bold]")
            console.print(result.to_string())
            return result

        console.print(f"[bold]🔗 {method.capitalize()} Correlation Matrix:[/bold]")
        console.print(corr_matrix.round(3).to_string())
        return corr_matrix

    @staticmethod
    def normality_test(data, alpha: float = 0.05) -> Dict[str, Any]:
        """Shapiro-Wilk normality test."""
        arr = _to_numpy(data)
        stat, p_val = sp_stats.shapiro(arr[:5000])  # Shapiro max 5000
        normal = p_val > alpha
        result = {
            "statistic": round(float(stat), 4),
            "p_value": round(float(p_val), 6),
            "is_normal": normal,
            "conclusion": f"{'✅ Normal' if normal else '❌ Not normal'} distribution (p={p_val:.4f})",
        }
        console.print(f"[bold]Shapiro-Wilk[/bold]: W={stat:.4f}, p={p_val:.6f} — {result['conclusion']}")
        return result


# ─────────────────────────────────────────────────────────────────────────────
# PREDICTIVE ANALYTICS
# ─────────────────────────────────────────────────────────────────────────────

class predict:
    """
    Predictive analytics: regression, forecasting, classification.

    Example:
        >>> bl.predict.linear_regression(x, y)
        >>> bl.predict.logistic_regression(X, y)
    """

    @staticmethod
    def linear_regression(
        x,
        y,
        calculation_level: str = "sample",
        confidence: float = 0.95,
        show_plot: bool = True,
    ) -> Dict[str, Any]:
        """
        Simple linear regression with confidence intervals.

        Args:
            x: Predictor variable
            y: Target variable
            calculation_level: 'sample' or 'population' (affects std error interpretation)
            confidence: Confidence interval level (default 0.95)
            show_plot: Show scatter plot with regression line

        Returns:
            Dict with equation, r_squared, p_value, predictions, confidence_intervals

        Formula:
            ŷ = β₀ + β₁x
            β₁ = Σ(xᵢ-x̄)(yᵢ-ȳ) / Σ(xᵢ-x̄)²
            β₀ = ȳ - β₁x̄
        """
        x_arr = _to_numpy(x)
        y_arr = _to_numpy(y)

        slope, intercept, r_value, p_val, std_err = sp_stats.linregress(x_arr, y_arr)
        r_sq = r_value ** 2
        predictions = intercept + slope * x_arr
        residuals = y_arr - predictions

        result = {
            "equation": f"ŷ = {intercept:.4f} + {slope:.4f}x",
            "intercept": round(float(intercept), 4),
            "slope": round(float(slope), 4),
            "r_squared": round(float(r_sq), 4),
            "r": round(float(r_value), 4),
            "p_value": round(float(p_val), 6),
            "std_error": round(float(std_err), 4),
            "significant": p_val < 0.05,
            "predictions": predictions.tolist(),
            "residuals": residuals.tolist(),
            "rmse": round(float(np.sqrt(np.mean(residuals**2))), 4),
            "mae": round(float(np.mean(np.abs(residuals))), 4),
        }

        table = Table(title="📈 Simple Linear Regression", show_lines=True)
        table.add_column("Metric", style="cyan", width=22)
        table.add_column("Value", style="green", justify="right", width=18)
        for k, v in [
            ("Equation", result["equation"]),
            ("R² (Explained Variance)", f"{r_sq:.4f} ({r_sq*100:.1f}%)"),
            ("Pearson r", f"{r_value:.4f}"),
            ("p-value", f"{p_val:.6f}"),
            ("Std Error", f"{std_err:.4f}"),
            ("RMSE", f"{result['rmse']:.4f}"),
            ("MAE", f"{result['mae']:.4f}"),
            ("Significant?", "✅ YES" if p_val < 0.05 else "❌ NO"),
        ]:
            table.add_row(k, str(v))
        console.print(table)

        if show_plot:
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            axes[0].scatter(x_arr, y_arr, alpha=0.6, color="#2E86AB", s=40, label="Data")
            x_sorted = np.sort(x_arr)
            axes[0].plot(x_sorted, intercept + slope * x_sorted, color="#D62828",
                         linewidth=2, label=f"ŷ = {intercept:.2f} + {slope:.2f}x")
            axes[0].set_title(f"Regression  |  R²={r_sq:.3f}", fontweight="bold")
            axes[0].legend()
            axes[1].scatter(predictions, residuals, alpha=0.6, color="#A23B72", s=40)
            axes[1].axhline(0, color="#D62828", linestyle="--", linewidth=1.5)
            axes[1].set_title("Residual Plot (check linearity)", fontweight="bold")
            axes[1].set_xlabel("Fitted values")
            axes[1].set_ylabel("Residuals")
            plt.tight_layout()
            plt.show()

        return result

    @staticmethod
    def multiple_regression(
        X: Union[pd.DataFrame, pl.DataFrame],
        y,
        calculation_level: str = "sample",
    ) -> Dict[str, Any]:
        """
        Multiple linear regression using scikit-learn.

        Args:
            X: Feature DataFrame (pandas or polars)
            y: Target variable
            calculation_level: 'sample' or 'population'

        Returns:
            Dict with coefficients, R², feature importance
        """
        try:
            from sklearn.linear_model import LinearRegression
            from sklearn.model_selection import cross_val_score
            from sklearn.metrics import mean_squared_error, r2_score
        except ImportError:
            raise ImportError("scikit-learn required: pip install scikit-learn")

        if isinstance(X, pl.DataFrame):
            X_df = X.to_pandas()
        else:
            X_df = X
        y_arr = _to_numpy(y)

        model = LinearRegression()
        model.fit(X_df, y_arr)
        predictions = model.predict(X_df)
        r_sq = r2_score(y_arr, predictions)
        rmse = np.sqrt(mean_squared_error(y_arr, predictions))

        cv_scores = cross_val_score(model, X_df, y_arr, cv=5, scoring="r2")

        result = {
            "intercept": round(float(model.intercept_), 4),
            "coefficients": {col: round(float(coef), 4)
                             for col, coef in zip(X_df.columns, model.coef_)},
            "r_squared": round(float(r_sq), 4),
            "rmse": round(float(rmse), 4),
            "cv_r2_mean": round(float(cv_scores.mean()), 4),
            "cv_r2_std": round(float(cv_scores.std()), 4),
        }

        console.print(f"[bold]📈 Multiple Regression[/bold]: R²={r_sq:.4f}, RMSE={rmse:.4f}")
        console.print(f"[bold]Cross-validation R²[/bold]: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
        for col, coef in result["coefficients"].items():
            console.print(f"  {col}: {coef:+.4f}")
        return result

    @staticmethod
    def logistic_regression(
        X: Union[pd.DataFrame, pl.DataFrame],
        y,
        threshold: float = 0.5,
    ) -> Dict[str, Any]:
        """
        Binary logistic regression with confusion matrix and ROC-AUC.

        Args:
            X: Feature DataFrame
            y: Binary target variable (0/1)
            threshold: Classification threshold (default 0.5)

        Returns:
            Dict with accuracy, AUC, confusion matrix, feature coefficients
        """
        try:
            from sklearn.linear_model import LogisticRegression
            from sklearn.metrics import (accuracy_score, roc_auc_score,
                                         confusion_matrix, classification_report)
        except ImportError:
            raise ImportError("scikit-learn required: pip install scikit-learn")

        if isinstance(X, pl.DataFrame):
            X_df = X.to_pandas()
        else:
            X_df = X
        y_arr = _to_numpy(y).astype(int)

        model = LogisticRegression(max_iter=1000)
        model.fit(X_df, y_arr)
        y_prob = model.predict_proba(X_df)[:, 1]
        y_pred = (y_prob >= threshold).astype(int)

        acc = accuracy_score(y_arr, y_pred)
        auc = roc_auc_score(y_arr, y_prob)
        cm = confusion_matrix(y_arr, y_pred)
        report = classification_report(y_arr, y_pred, output_dict=True)

        result = {
            "accuracy": round(float(acc), 4),
            "auc_roc": round(float(auc), 4),
            "confusion_matrix": cm.tolist(),
            "coefficients": {col: round(float(coef), 4)
                             for col, coef in zip(X_df.columns, model.coef_[0])},
            "classification_report": report,
        }

        console.print(f"[bold]🎯 Logistic Regression[/bold]: Accuracy={acc:.4f}, AUC-ROC={auc:.4f}")
        console.print(f"Confusion Matrix:\n{cm}")
        for col, coef in result["coefficients"].items():
            console.print(f"  {col}: {coef:+.4f}")
        return result

    @staticmethod
    def confusion_matrix_plot(
        y_true,
        y_pred,
        labels: Optional[List] = None,
        title: str = "Confusion Matrix",
        color_scheme: str = "academic",
    ) -> Dict[str, Any]:
        """
        Plot a confusion matrix with accuracy metrics.

        Args:
            y_true: Actual labels
            y_pred: Predicted labels
            labels: Class label names (e.g. ['No', 'Yes'])
            title: Plot title
            color_scheme: 'academic', 'pastel', or 'vibrant'

        Returns:
            Dict with accuracy, precision, recall, f1

        Example:
            >>> y_true = [0, 1, 0, 1, 1, 0, 1, 0]
            >>> y_pred = [0, 1, 0, 0, 1, 0, 1, 1]
            >>> bl.predict.confusion_matrix_plot(y_true, y_pred, labels=['No', 'Yes'])
        """
        try:
            from sklearn.metrics import (confusion_matrix, accuracy_score,
                                         precision_score, recall_score, f1_score,
                                         ConfusionMatrixDisplay)
        except ImportError:
            raise ImportError("scikit-learn required: pip install scikit-learn")

        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        cm = confusion_matrix(y_true, y_pred)
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, average="weighted", zero_division=0)
        rec = recall_score(y_true, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)

        fig, axes = plt.subplots(1, 2, figsize=(13, 5))

        # Confusion matrix heatmap
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
        disp.plot(ax=axes[0], cmap="Blues", colorbar=False)
        axes[0].set_title(f"{title}", fontweight="bold", fontsize=12)

        # Metrics bar chart
        metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]
        values = [acc, prec, rec, f1]
        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])["palette"]
        bars = axes[1].bar(metrics, values, color=colors[:4], alpha=0.85, edgecolor="white")
        axes[1].set_ylim(0, 1.1)
        axes[1].axhline(0.8, color="gray", linestyle="--", alpha=0.5, label="0.8 threshold")
        for bar, val in zip(bars, values):
            axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                         f"{val:.3f}", ha="center", fontweight="bold")
        axes[1].set_title("Classification Metrics", fontweight="bold", fontsize=12)
        axes[1].legend()

        plt.tight_layout()
        plt.show()

        result = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "confusion_matrix": cm.tolist(),
        }
        console.print(f"[bold]Accuracy:[/bold] {acc:.4f}  [bold]Precision:[/bold] {prec:.4f}  [bold]Recall:[/bold] {rec:.4f}  [bold]F1:[/bold] {f1:.4f}")
        return result

    @staticmethod
    def decision_tree(
        X: Union[pd.DataFrame, pl.DataFrame],
        y,
        task: str = "classification",
        max_depth: Optional[int] = 4,
        show_plot: bool = True,
        feature_names: Optional[List[str]] = None,
        class_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Decision Tree for classification or regression.

        Args:
            X: Feature DataFrame (pandas or polars)
            y: Target variable
            task: 'classification' or 'regression'
            max_depth: Maximum tree depth (default 4, None = unlimited)
            show_plot: Visualize the tree and feature importance
            feature_names: Names for features (uses column names if DataFrame)
            class_names: Names for classes (classification only)

        Returns:
            Dict with accuracy/R², feature_importance, tree depth

        Example:
            >>> # Classification
            >>> df = bl.load_dataset('titanic')
            >>> clean = df[['pclass','age','fare','survived']].dropna()
            >>> X = clean[['pclass','age','fare']]
            >>> y = clean['survived']
            >>> result = bl.predict.decision_tree(X, y, task='classification', class_names=['No','Yes'])

            >>> # Regression
            >>> df = bl.load_dataset('tips')
            >>> X = df[['total_bill','size']]
            >>> y = df['tip']
            >>> result = bl.predict.decision_tree(X, y, task='regression')

        How it works:
            At each node, the tree asks a yes/no question (e.g. 'age > 30?')
            It picks the question that best separates the data (using Gini/MSE)
            Repeat until max_depth or pure leaf nodes
            Feature importance = how much each feature reduces impurity
        """
        try:
            from sklearn.tree import (DecisionTreeClassifier, DecisionTreeRegressor,
                                      plot_tree, export_text)
            from sklearn.metrics import accuracy_score, r2_score
            from sklearn.model_selection import cross_val_score
        except ImportError:
            raise ImportError("scikit-learn required: pip install scikit-learn")

        if isinstance(X, pl.DataFrame):
            X_df = X.to_pandas()
        else:
            X_df = X.copy()

        feat_names = feature_names or list(X_df.columns)
        y_arr = np.array(y)

        if task == "classification":
            model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
            model.fit(X_df, y_arr)
            y_pred = model.predict(X_df)
            score = accuracy_score(y_arr, y_pred)
            cv = cross_val_score(model, X_df, y_arr, cv=5, scoring="accuracy")
            score_label = "Accuracy"
            cm = confusion_matrix(y_arr, y_pred) if hasattr(y_arr, '__len__') else None
        else:
            model = DecisionTreeRegressor(max_depth=max_depth, random_state=42)
            model.fit(X_df, y_arr)
            y_pred = model.predict(X_df)
            score = r2_score(y_arr, y_pred)
            cv = cross_val_score(model, X_df, y_arr, cv=5, scoring="r2")
            score_label = "R²"
            cm = None

        importance = dict(zip(feat_names, model.feature_importances_))
        importance_sorted = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))

        result = {
            "task": task,
            score_label.lower().replace("²", "2"): round(float(score), 4),
            "cv_mean": round(float(cv.mean()), 4),
            "cv_std": round(float(cv.std()), 4),
            "tree_depth": model.get_depth(),
            "n_leaves": model.get_n_leaves(),
            "feature_importance": {k: round(float(v), 4) for k, v in importance_sorted.items()},
        }

        # Rich output
        table = Table(title=f"🌳 Decision Tree ({task.capitalize()})", show_lines=True)
        table.add_column("Metric", style="cyan", width=24)
        table.add_column("Value", style="green", justify="right", width=16)
        for k, v in [
            (score_label, f"{score:.4f}"),
            (f"Cross-val {score_label} (5-fold)", f"{cv.mean():.4f} ± {cv.std():.4f}"),
            ("Tree Depth", str(model.get_depth())),
            ("Leaf Nodes", str(model.get_n_leaves())),
        ]:
            table.add_row(k, str(v))
        console.print(table)

        # Feature importance
        console.print("\n[bold]🏆 Feature Importance:[/bold]")
        for feat, imp in importance_sorted.items():
            bar = "█" * int(imp * 30)
            console.print(f"  {feat:<20} {bar:<30} {imp:.4f}")

        if show_plot:
            if len(feat_names) <= 10:
                fig, axes = plt.subplots(1, 2, figsize=(16, 6))
                # Tree visualization
                plot_tree(model, feature_names=feat_names,
                          class_names=class_names,
                          filled=True, rounded=True, ax=axes[0],
                          max_depth=min(3, max_depth or 4))
                axes[0].set_title(f"Decision Tree (max_depth={max_depth})", fontweight="bold")

                # Feature importance bar chart
                feats = list(importance_sorted.keys())
                imps = list(importance_sorted.values())
                axes[1].barh(feats[::-1], imps[::-1], color="#2E86AB", alpha=0.85)
                axes[1].set_title("Feature Importance", fontweight="bold")
                axes[1].set_xlabel("Importance Score")
                plt.tight_layout()
                plt.show()
            else:
                # Just feature importance
                fig, ax = plt.subplots(figsize=(9, 5))
                feats = list(importance_sorted.keys())[:12]
                imps = list(importance_sorted.values())[:12]
                ax.barh(feats[::-1], imps[::-1], color="#2E86AB", alpha=0.85)
                ax.set_title("Feature Importance (Top 12)", fontweight="bold")
                ax.set_xlabel("Importance Score")
                plt.tight_layout()
                plt.show()

            if cm is not None:
                fig2, ax2 = plt.subplots(figsize=(6, 5))
                from sklearn.metrics import ConfusionMatrixDisplay
                disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
                disp.plot(ax=ax2, cmap="Blues", colorbar=False)
                ax2.set_title("Decision Tree — Confusion Matrix", fontweight="bold")
                plt.tight_layout()
                plt.show()

        return result


# ─────────────────────────────────────────────────────────────────────────────
# OPTIMIZATION
# ─────────────────────────────────────────────────────────────────────────────

class optimize:
    """
    Business optimization using linear programming.
    Requires: pip install pulp pyomo

    Example:
        >>> # Maximize profit given resource constraints
        >>> prob, result = bl.optimize.linear_program(
        ...     objective=[25, 30],
        ...     constraints=[[2, 1], [1, 3]],
        ...     rhs=[100, 90],
        ...     maximize=True
        ... )
    """

    @staticmethod
    def linear_program(
        objective: List[float],
        constraints: List[List[float]],
        rhs: List[float],
        variable_names: Optional[List[str]] = None,
        maximize: bool = True,
        constraint_types: Optional[List[str]] = None,
    ) -> Tuple[Any, Dict]:
        """
        Solve a linear programming problem using PuLP.

        Args:
            objective: Coefficients for objective function
            constraints: List of constraint coefficient rows
            rhs: Right-hand side values for each constraint
            variable_names: Names for decision variables (optional)
            maximize: True to maximize, False to minimize
            constraint_types: List of '<=', '>=', '=' for each constraint

        Returns:
            Tuple of (problem, result_dict)

        Example:
            Maximize: 25x₁ + 30x₂
            Subject to: 2x₁ + x₂ ≤ 100
                        x₁ + 3x₂ ≤ 90
            >>> prob, res = bl.optimize.linear_program(
            ...     objective=[25, 30],
            ...     constraints=[[2,1],[1,3]],
            ...     rhs=[100, 90],
            ...     maximize=True
            ... )
        """
        try:
            import pulp
        except ImportError:
            raise ImportError("PuLP required: pip install pulp")

        n_vars = len(objective)
        names = variable_names or [f"x{i+1}" for i in range(n_vars)]
        c_types = constraint_types or ["<="] * len(constraints)

        sense = pulp.LpMaximize if maximize else pulp.LpMinimize
        prob = pulp.LpProblem("BizLens_LP", sense)
        vars_ = [pulp.LpVariable(name, lowBound=0) for name in names]

        prob += pulp.lpSum(obj * v for obj, v in zip(objective, vars_))

        for i, (row, rhs_val, ct) in enumerate(zip(constraints, rhs, c_types)):
            expr = pulp.lpSum(coef * v for coef, v in zip(row, vars_))
            if ct == "<=":
                prob += expr <= rhs_val, f"c{i+1}"
            elif ct == ">=":
                prob += expr >= rhs_val, f"c{i+1}"
            else:
                prob += expr == rhs_val, f"c{i+1}"

        prob.solve(pulp.PULP_CBC_CMD(msg=0))

        result = {
            "status": pulp.LpStatus[prob.status],
            "objective_value": round(float(pulp.value(prob.objective)), 4),
            "variables": {name: round(float(pulp.value(v)), 4)
                          for name, v in zip(names, vars_)},
            "maximize": maximize,
        }

        console.print(f"[bold]🎯 LP Result[/bold]: Status={result['status']}, "
                      f"Objective={'Max' if maximize else 'Min'}={result['objective_value']}")
        for name, val in result["variables"].items():
            console.print(f"  {name} = {val}")
        return prob, result


# ─────────────────────────────────────────────────────────────────────────────
# STATISTICAL TABLES
# ─────────────────────────────────────────────────────────────────────────────

class tables:
    """
    Statistical tables for comparison and analysis.

    Methods
    -------
    frequency(data, column, bins=None, show_plot=True)
        Frequency distribution table (count, %, cumulative %)
    descriptive_comparison(data, columns=None, calculation_level='sample')
        Side-by-side descriptive stats for multiple columns
    crosstab(data, row_col, col_col, normalize=None, show_plot=True)
        Cross-tabulation / contingency table
    correlation_matrix(data, columns=None, method='pearson', show_plot=True)
        Full correlation matrix with significance stars
    group_comparison(data, group_col, value_col, stats=None)
        Compare descriptive stats across groups
    percentile_table(data, column, percentiles=None)
        Percentile / quantile table with z-scores
    distribution_fit(data, column, distributions=None)
        Fit multiple distributions and compare goodness-of-fit
    """

    # ── Frequency Distribution ─────────────────────────────────────────────
    @staticmethod
    def frequency(
        data,
        column: str,
        bins: Optional[int] = None,
        show_plot: bool = True,
        color_scheme: str = "academic",
    ) -> pd.DataFrame:
        """
        Build a frequency distribution table for a column.

        Parameters
        ----------
        data : DataFrame (pandas or polars)
        column : str  — column to analyse
        bins : int or None — for numeric data, number of bins (auto if None)
        show_plot : bool — show bar chart alongside the table
        color_scheme : str — 'academic', 'pastel', or 'vibrant'

        Returns
        -------
        pd.DataFrame with columns: Value/Bin, Count, Relative %, Cumulative %
        """
        frame = nw.from_native(data)
        series = frame[column].to_native() if hasattr(frame[column], "to_native") else np.array(frame[column])
        if hasattr(series, "values"):
            arr = series.values
        else:
            arr = np.array(series)

        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])

        # Determine whether numeric or categorical
        is_numeric = np.issubdtype(arr.dtype, np.number)

        if is_numeric:
            n_bins = bins or min(int(np.ceil(np.sqrt(len(arr)))), 20)
            counts, edges = np.histogram(arr, bins=n_bins)
            labels = [f"{edges[i]:.2f}–{edges[i+1]:.2f}" for i in range(len(counts))]
        else:
            unique, counts = np.unique(arr.astype(str), return_counts=True)
            labels = unique.tolist()

        total = counts.sum()
        rel_pct = counts / total * 100
        cum_pct = np.cumsum(rel_pct)

        df = pd.DataFrame({
            "Value/Bin": labels,
            "Count": counts,
            "Relative %": np.round(rel_pct, 2),
            "Cumulative %": np.round(cum_pct, 2),
        })

        # Rich table
        tbl = Table(title=f"[bold]Frequency Distribution — {column}[/bold]",
                    header_style="bold cyan")
        for col in df.columns:
            tbl.add_column(col, justify="right" if col != "Value/Bin" else "left")
        for _, row in df.iterrows():
            tbl.add_row(*[str(v) for v in row])
        console.print(tbl)

        if show_plot:
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            fig.suptitle(f"Frequency Distribution — {column}", fontsize=14, fontweight="bold")

            # Bar chart
            axes[0].bar(range(len(labels)), counts, color=colors["primary"], edgecolor="white", linewidth=0.5)
            axes[0].set_xticks(range(len(labels)))
            axes[0].set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
            axes[0].set_ylabel("Count")
            axes[0].set_title("Frequency")

            # Cumulative %
            axes[1].plot(range(len(labels)), cum_pct, marker="o",
                         color=colors["secondary"], linewidth=2)
            axes[1].fill_between(range(len(labels)), cum_pct,
                                 alpha=0.15, color=colors["secondary"])
            axes[1].axhline(80, ls="--", color=colors["accent"], linewidth=1, label="80%")
            axes[1].set_xticks(range(len(labels)))
            axes[1].set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
            axes[1].set_ylabel("Cumulative %")
            axes[1].set_title("Cumulative Frequency")
            axes[1].legend(fontsize=8)

            plt.tight_layout()
            plt.show()

        return df

    # ── Descriptive Comparison ──────────────────────────────────────────────
    @staticmethod
    def descriptive_comparison(
        data,
        columns: Optional[List[str]] = None,
        calculation_level: str = "sample",
        color_scheme: str = "academic",
    ) -> pd.DataFrame:
        """
        Side-by-side descriptive statistics for multiple numeric columns.

        Parameters
        ----------
        data : DataFrame (pandas or polars)
        columns : list of str or None (all numeric columns)
        calculation_level : 'sample' (n-1) or 'population' (n)
        color_scheme : str

        Returns
        -------
        pd.DataFrame — rows=stats, columns=variables
        """
        frame = nw.from_native(data)
        pdf = frame.to_native() if hasattr(frame, "to_native") else pd.DataFrame(data)
        if not isinstance(pdf, pd.DataFrame):
            pdf = pd.DataFrame(pdf)

        ddof = 1 if calculation_level == "sample" else 0
        cols = columns or [c for c in pdf.columns if pd.api.types.is_numeric_dtype(pdf[c])]

        stats_rows = {}
        for col in cols:
            arr = pdf[col].dropna().values.astype(float)
            n = len(arr)
            mean_ = np.mean(arr)
            std_ = np.std(arr, ddof=ddof)
            var_ = np.var(arr, ddof=ddof)
            skew_ = float(sp_stats.skew(arr))
            kurt_ = float(sp_stats.kurtosis(arr))
            stats_rows[col] = {
                "N": n,
                "Mean": round(mean_, 4),
                "Std Dev": round(std_, 4),
                "Variance": round(var_, 4),
                "Min": round(float(np.min(arr)), 4),
                "Q1 (25%)": round(float(np.percentile(arr, 25)), 4),
                "Median": round(float(np.median(arr)), 4),
                "Q3 (75%)": round(float(np.percentile(arr, 75)), 4),
                "Max": round(float(np.max(arr)), 4),
                "IQR": round(float(np.percentile(arr, 75) - np.percentile(arr, 25)), 4),
                "Skewness": round(skew_, 4),
                "Kurtosis": round(kurt_, 4),
                "CV %": round(std_ / mean_ * 100 if mean_ != 0 else float("nan"), 2),
            }

        result = pd.DataFrame(stats_rows)
        result.index.name = f"Statistic ({calculation_level}, ddof={ddof})"

        # Rich table
        tbl = Table(
            title=f"[bold]Descriptive Statistics Comparison ({calculation_level.capitalize()})[/bold]",
            header_style="bold cyan"
        )
        tbl.add_column("Statistic", style="bold")
        for col in result.columns:
            tbl.add_column(col, justify="right")
        for stat, row in result.iterrows():
            tbl.add_row(str(stat), *[str(v) for v in row])
        console.print(tbl)
        console.print(f"[dim]📌 Std Dev uses ddof={ddof} ({'Bessel correction' if ddof==1 else 'population n'})[/dim]")

        return result

    # ── Cross-Tabulation ────────────────────────────────────────────────────
    @staticmethod
    def crosstab(
        data,
        row_col: str,
        col_col: str,
        normalize: Optional[str] = None,
        show_plot: bool = True,
        color_scheme: str = "academic",
    ) -> pd.DataFrame:
        """
        Cross-tabulation (contingency table) between two categorical columns.

        Parameters
        ----------
        data : DataFrame
        row_col : str — row variable
        col_col : str — column variable
        normalize : None | 'index' | 'columns' | 'all'
        show_plot : bool

        Returns
        -------
        pd.DataFrame — cross-tabulation
        """
        frame = nw.from_native(data)
        pdf = frame.to_native() if hasattr(frame, "to_native") else pd.DataFrame(data)
        if not isinstance(pdf, pd.DataFrame):
            pdf = pd.DataFrame(pdf)

        ct = pd.crosstab(pdf[row_col], pdf[col_col], margins=True,
                          margins_name="Total", normalize=normalize)

        if normalize:
            ct = ct.round(3)

        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])

        # Rich table
        title = f"Cross-Tabulation: {row_col} × {col_col}"
        if normalize:
            title += f" (normalized by {normalize})"
        tbl = Table(title=f"[bold]{title}[/bold]", header_style="bold cyan")
        tbl.add_column(row_col, style="bold")
        for c in ct.columns:
            tbl.add_column(str(c), justify="right")
        for idx, row in ct.iterrows():
            tbl.add_row(str(idx), *[str(v) for v in row])
        console.print(tbl)

        # Chi-square test
        ct_no_margins = pd.crosstab(pdf[row_col], pdf[col_col])
        chi2, p, dof, expected = sp_stats.chi2_contingency(ct_no_margins.values)
        sig = "✅ Significant" if p < 0.05 else "❌ Not Significant"
        console.print(f"[bold]χ² Test:[/bold] χ²={chi2:.3f}, df={dof}, p={p:.4f} → {sig}")

        if show_plot:
            ct_plot = pd.crosstab(pdf[row_col], pdf[col_col])
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            fig.suptitle(title, fontsize=13, fontweight="bold")

            ct_plot.plot(kind="bar", ax=axes[0], color=colors["palette"][:len(ct_plot.columns)],
                         edgecolor="white", linewidth=0.5)
            axes[0].set_title("Grouped Bar Chart")
            axes[0].set_xlabel(row_col)
            axes[0].tick_params(axis="x", rotation=30)
            axes[0].legend(title=col_col, fontsize=8)

            sns.heatmap(ct_no_margins, annot=True, fmt="d", cmap="Blues", ax=axes[1],
                        linewidths=0.5, cbar_kws={"shrink": 0.8})
            axes[1].set_title("Heatmap")

            plt.tight_layout()
            plt.show()

        return ct

    # ── Correlation Matrix ──────────────────────────────────────────────────
    @staticmethod
    def correlation_matrix(
        data,
        columns: Optional[List[str]] = None,
        method: str = "pearson",
        show_plot: bool = True,
        color_scheme: str = "academic",
    ) -> pd.DataFrame:
        """
        Full correlation matrix with significance stars.

        Parameters
        ----------
        data : DataFrame
        columns : list of str or None (all numeric)
        method : 'pearson' | 'spearman' | 'kendall'
        show_plot : bool

        Returns
        -------
        pd.DataFrame — correlation matrix
        """
        frame = nw.from_native(data)
        pdf = frame.to_native() if hasattr(frame, "to_native") else pd.DataFrame(data)
        if not isinstance(pdf, pd.DataFrame):
            pdf = pd.DataFrame(pdf)

        cols = columns or [c for c in pdf.columns if pd.api.types.is_numeric_dtype(pdf[c])]
        sub = pdf[cols].dropna()

        corr = sub.corr(method=method).round(3)

        # Compute p-values for pearson/spearman
        n = len(sub)
        pval_methods = {"pearson": sp_stats.pearsonr, "spearman": sp_stats.spearmanr}
        pvals = pd.DataFrame(np.nan, index=cols, columns=cols)
        if method in pval_methods:
            for c1 in cols:
                for c2 in cols:
                    if c1 != c2:
                        _, p = pval_methods[method](sub[c1], sub[c2])
                        pvals.loc[c1, c2] = p
                    else:
                        pvals.loc[c1, c2] = 0.0

        def stars(p):
            if np.isnan(p) or p == 0:
                return ""
            if p < 0.001: return "***"
            if p < 0.01:  return "**"
            if p < 0.05:  return "*"
            return ""

        # Rich table with stars
        tbl = Table(
            title=f"[bold]Correlation Matrix ({method.capitalize()}) — n={n}[/bold]",
            header_style="bold cyan"
        )
        tbl.add_column("Variable", style="bold")
        for c in cols:
            tbl.add_column(c, justify="right")
        for r in cols:
            row_vals = []
            for c in cols:
                val = corr.loc[r, c]
                s = stars(pvals.loc[r, c])
                row_vals.append(f"{val:.3f}{s}")
            tbl.add_row(r, *row_vals)
        console.print(tbl)
        console.print("[dim]* p<0.05  ** p<0.01  *** p<0.001[/dim]")

        if show_plot:
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            fig.suptitle(f"Correlation Matrix ({method.capitalize()})", fontsize=13, fontweight="bold")

            # Heatmap
            mask = np.triu(np.ones_like(corr, dtype=bool))
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r",
                        center=0, mask=mask, ax=axes[0],
                        linewidths=0.5, vmin=-1, vmax=1, cbar_kws={"shrink": 0.8})
            axes[0].set_title("Lower Triangle Heatmap")

            # Cluster map alternative — clustermap needs its own figure, so do bar chart of top pairs
            pairs = []
            for i, c1 in enumerate(cols):
                for j, c2 in enumerate(cols):
                    if j > i:
                        pairs.append((abs(corr.loc[c1, c2]), corr.loc[c1, c2], f"{c1}↔{c2}"))
            pairs.sort(reverse=True)
            if pairs:
                top_pairs = pairs[:min(10, len(pairs))]
                bar_cols = [p[2] for p in top_pairs]
                bar_vals = [p[1] for p in top_pairs]
                bar_colors = ["#2E86AB" if v >= 0 else "#D62828" for v in bar_vals]
                axes[1].barh(bar_cols, bar_vals, color=bar_colors, edgecolor="white")
                axes[1].axvline(0, color="black", linewidth=0.8)
                axes[1].set_xlabel("Correlation Coefficient")
                axes[1].set_title("Top Pair Correlations")
                axes[1].set_xlim(-1, 1)

            plt.tight_layout()
            plt.show()

        return corr

    # ── Group Comparison ────────────────────────────────────────────────────
    @staticmethod
    def group_comparison(
        data,
        group_col: str,
        value_col: str,
        stats: Optional[List[str]] = None,
        show_plot: bool = True,
        color_scheme: str = "academic",
    ) -> pd.DataFrame:
        """
        Compare descriptive statistics across groups.

        Parameters
        ----------
        data : DataFrame
        group_col : str — categorical grouping column
        value_col : str — numeric column to compare
        stats : list of stat names or None (all)
        show_plot : bool

        Returns
        -------
        pd.DataFrame — rows=groups, columns=stats
        """
        frame = nw.from_native(data)
        pdf = frame.to_native() if hasattr(frame, "to_native") else pd.DataFrame(data)
        if not isinstance(pdf, pd.DataFrame):
            pdf = pd.DataFrame(pdf)

        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])
        default_stats = ["count", "mean", "std", "min", "25%", "50%", "75%", "max", "skew", "cv%"]
        wanted = stats or default_stats

        rows = []
        for grp, sub in pdf.groupby(group_col, sort=True):
            arr = sub[value_col].dropna().values.astype(float)
            n = len(arr)
            mean_ = np.mean(arr)
            std_ = np.std(arr, ddof=1)
            row = {
                "Group": grp,
                "count": n,
                "mean": round(mean_, 4),
                "std": round(std_, 4),
                "min": round(float(np.min(arr)), 4),
                "25%": round(float(np.percentile(arr, 25)), 4),
                "50%": round(float(np.median(arr)), 4),
                "75%": round(float(np.percentile(arr, 75)), 4),
                "max": round(float(np.max(arr)), 4),
                "skew": round(float(sp_stats.skew(arr)), 4),
                "cv%": round(std_ / mean_ * 100 if mean_ != 0 else float("nan"), 2),
            }
            rows.append(row)

        result = pd.DataFrame(rows).set_index("Group")
        available = [c for c in wanted if c in result.columns]
        result = result[available]

        # One-way ANOVA across groups
        groups_data = [pdf[pdf[group_col] == g][value_col].dropna().values
                       for g in pdf[group_col].unique()]
        if len(groups_data) >= 2:
            f_stat, p_val = sp_stats.f_oneway(*groups_data)
            anova_note = f"One-Way ANOVA: F={f_stat:.3f}, p={p_val:.4f} → {'✅ Significant' if p_val < 0.05 else '❌ Not Significant'}"
        else:
            anova_note = ""

        tbl = Table(
            title=f"[bold]Group Comparison: {value_col} by {group_col}[/bold]",
            header_style="bold cyan"
        )
        tbl.add_column("Group", style="bold")
        for col in result.columns:
            tbl.add_column(col, justify="right")
        for grp, row in result.iterrows():
            tbl.add_row(str(grp), *[str(v) for v in row])
        console.print(tbl)
        if anova_note:
            console.print(f"[bold]{anova_note}[/bold]")

        if show_plot:
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            fig.suptitle(f"{value_col} by {group_col}", fontsize=13, fontweight="bold")

            # Box plot
            groups_list = sorted(pdf[group_col].unique().tolist())
            box_data = [pdf[pdf[group_col] == g][value_col].dropna().values for g in groups_list]
            bp = axes[0].boxplot(box_data, labels=groups_list, patch_artist=True,
                                 medianprops={"color": "white", "linewidth": 2})
            for patch, color in zip(bp["boxes"], colors["palette"] * 10):
                patch.set_facecolor(color)
            axes[0].set_title("Box Plot by Group")
            axes[0].tick_params(axis="x", rotation=30)

            # Mean ± std bar
            means = result["mean"] if "mean" in result.columns else result.iloc[:, 0]
            stds = result["std"] if "std" in result.columns else pd.Series(0, index=result.index)
            axes[1].bar(range(len(means)), means.values,
                        yerr=stds.values, capsize=5,
                        color=colors["palette"][:len(means)], edgecolor="white", linewidth=0.5)
            axes[1].set_xticks(range(len(means)))
            axes[1].set_xticklabels(means.index.tolist(), rotation=30, ha="right")
            axes[1].set_title("Mean ± Std Dev by Group")
            axes[1].set_ylabel(value_col)

            plt.tight_layout()
            plt.show()

        return result

    # ── Percentile Table ────────────────────────────────────────────────────
    @staticmethod
    def percentile_table(
        data,
        column: str,
        percentiles: Optional[List[float]] = None,
    ) -> pd.DataFrame:
        """
        Percentile / quantile table with z-scores and IQR flags.

        Parameters
        ----------
        data : DataFrame
        column : str — numeric column
        percentiles : list of floats 0-100 or None (default set)

        Returns
        -------
        pd.DataFrame with Percentile, Value, Z-score, IQR Flag
        """
        frame = nw.from_native(data)
        pdf = frame.to_native() if hasattr(frame, "to_native") else pd.DataFrame(data)
        if not isinstance(pdf, pd.DataFrame):
            pdf = pd.DataFrame(pdf)

        arr = pdf[column].dropna().values.astype(float)
        pcts = percentiles or [1, 5, 10, 25, 50, 75, 90, 95, 99]

        mean_ = np.mean(arr)
        std_ = np.std(arr, ddof=1)
        q1 = np.percentile(arr, 25)
        q3 = np.percentile(arr, 75)
        iqr = q3 - q1
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr

        rows = []
        for p in pcts:
            val = np.percentile(arr, p)
            z = (val - mean_) / std_ if std_ > 0 else 0
            flag = "⚠️ Outlier" if val < lower_fence or val > upper_fence else "✅ Normal"
            rows.append({
                "Percentile": f"P{int(p)}",
                "Value": round(val, 4),
                "Z-Score": round(z, 3),
                "IQR Flag": flag,
            })

        result = pd.DataFrame(rows)

        tbl = Table(
            title=f"[bold]Percentile Table — {column}[/bold]",
            header_style="bold cyan"
        )
        for col in result.columns:
            tbl.add_column(col, justify="right" if col != "IQR Flag" else "left")
        for _, row in result.iterrows():
            tbl.add_row(*[str(v) for v in row])
        console.print(tbl)
        console.print(
            f"[dim]Mean={mean_:.4f} | Std={std_:.4f} | IQR={iqr:.4f} | "
            f"Fences: [{lower_fence:.4f}, {upper_fence:.4f}][/dim]"
        )

        return result

    # ── Distribution Fit Comparison ─────────────────────────────────────────
    @staticmethod
    def distribution_fit(
        data,
        column: str,
        distributions: Optional[List[str]] = None,
        show_plot: bool = True,
        color_scheme: str = "academic",
    ) -> pd.DataFrame:
        """
        Fit multiple distributions to a column and compare goodness-of-fit.

        Parameters
        ----------
        data : DataFrame
        column : str
        distributions : list of scipy.stats distribution names or None
        show_plot : bool

        Returns
        -------
        pd.DataFrame — ranked by AIC: Distribution, Params, AIC, BIC, KS stat, p-value
        """
        frame = nw.from_native(data)
        pdf = frame.to_native() if hasattr(frame, "to_native") else pd.DataFrame(data)
        if not isinstance(pdf, pd.DataFrame):
            pdf = pd.DataFrame(pdf)

        arr = pdf[column].dropna().values.astype(float)
        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])

        dist_names = distributions or [
            "norm", "lognorm", "expon", "gamma", "beta",
            "weibull_min", "uniform", "t",
        ]

        results = []
        for name in dist_names:
            try:
                dist = getattr(sp_stats, name)
                params = dist.fit(arr)
                # Log-likelihood
                loglik = np.sum(dist.logpdf(arr, *params))
                k = len(params)
                n = len(arr)
                aic = 2 * k - 2 * loglik
                bic = k * np.log(n) - 2 * loglik
                # KS test
                ks_stat, ks_p = sp_stats.kstest(arr, name, args=params)
                results.append({
                    "Distribution": name,
                    "Params": str(tuple(round(p, 4) for p in params)),
                    "AIC": round(aic, 2),
                    "BIC": round(bic, 2),
                    "KS Stat": round(ks_stat, 4),
                    "KS p-value": round(ks_p, 4),
                    "Fit": "✅ Good" if ks_p > 0.05 else "❌ Poor",
                })
            except Exception:
                pass

        result = pd.DataFrame(results).sort_values("AIC").reset_index(drop=True)

        tbl = Table(
            title=f"[bold]Distribution Fit Comparison — {column}[/bold]",
            header_style="bold cyan"
        )
        for col in result.columns:
            tbl.add_column(col, justify="left" if col in ("Distribution","Params","Fit") else "right")
        for _, row in result.iterrows():
            tbl.add_row(*[str(v) for v in row])
        console.print(tbl)
        best = result.iloc[0]["Distribution"]
        console.print(f"[bold green]🏆 Best fit (lowest AIC): {best}[/bold green]")

        if show_plot:
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            fig.suptitle(f"Distribution Fit — {column}", fontsize=13, fontweight="bold")

            # Histogram + top 3 fits
            axes[0].hist(arr, bins="auto", density=True, alpha=0.4,
                         color=colors["primary"], label="Data")
            x = np.linspace(arr.min(), arr.max(), 300)
            for i, row in result.head(3).iterrows():
                try:
                    dist = getattr(sp_stats, row["Distribution"])
                    params = dist.fit(arr)
                    axes[0].plot(x, dist.pdf(x, *params),
                                 color=colors["palette"][i % len(colors["palette"])],
                                 label=row["Distribution"], linewidth=2)
                except Exception:
                    pass
            axes[0].set_title("PDF Overlay (Top 3 fits)")
            axes[0].legend(fontsize=8)
            axes[0].set_xlabel(column)
            axes[0].set_ylabel("Density")

            # AIC bar chart
            top = result.head(min(6, len(result)))
            axes[1].barh(top["Distribution"], top["AIC"],
                         color=colors["palette"][:len(top)], edgecolor="white")
            axes[1].set_xlabel("AIC (lower = better)")
            axes[1].set_title("AIC Comparison")
            axes[1].invert_yaxis()

            plt.tight_layout()
            plt.show()

        return result


# ─────────────────────────────────────────────────────────────────────────────
# QUALITY / SIX SIGMA
# ─────────────────────────────────────────────────────────────────────────────

class quality:
    """
    Quality control and Six Sigma analytics.

    Methods
    -------
    process_capability(data, column, lsl, usl, target=None)
        Cp, Cpk, Pp, Ppk, sigma level, DPMO, yield
    control_chart(data, column, chart_type='xbar', subgroup_size=5)
        X-bar, R, S, p, c, u control charts with control limits
    pareto(data, category_col, value_col=None)
        Pareto chart — 80/20 analysis
    fishbone(categories)
        Cause-and-effect (Ishikawa) diagram
    """

    @staticmethod
    def process_capability(
        data,
        column: str,
        lsl: float,
        usl: float,
        target: Optional[float] = None,
        show_plot: bool = True,
        color_scheme: str = "academic",
    ) -> Dict:
        """
        Compute process capability indices: Cp, Cpk, Pp, Ppk, sigma level, DPMO.

        Parameters
        ----------
        data : DataFrame or array-like
        column : str (if DataFrame) or use data directly
        lsl : float — Lower Specification Limit
        usl : float — Upper Specification Limit
        target : float or None — target value (defaults to midpoint)

        Returns
        -------
        dict with Cp, Cpk, Pp, Ppk, sigma, DPMO, yield_pct
        """
        if hasattr(data, '__iter__') and not hasattr(data, 'columns'):
            arr = np.array(data, dtype=float)
        else:
            frame = nw.from_native(data)
            pdf = frame.to_native() if hasattr(frame, "to_native") else pd.DataFrame(data)
            if not isinstance(pdf, pd.DataFrame):
                pdf = pd.DataFrame(pdf)
            arr = pdf[column].dropna().values.astype(float)

        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])
        n = len(arr)
        mean_ = np.mean(arr)
        std_sample = np.std(arr, ddof=1)
        std_pop = np.std(arr, ddof=0)
        tgt = target if target is not None else (lsl + usl) / 2
        spec_width = usl - lsl

        # Capability indices (short-term, using sample std)
        Cp  = spec_width / (6 * std_sample) if std_sample > 0 else float("inf")
        Cpu = (usl - mean_) / (3 * std_sample) if std_sample > 0 else float("inf")
        Cpl = (mean_ - lsl) / (3 * std_sample) if std_sample > 0 else float("inf")
        Cpk = min(Cpu, Cpl)
        Cpm = spec_width / (6 * np.sqrt(std_sample**2 + (mean_ - tgt)**2)) if std_sample > 0 else float("inf")

        # Performance indices (long-term, using population std)
        Pp  = spec_width / (6 * std_pop) if std_pop > 0 else float("inf")
        Ppu = (usl - mean_) / (3 * std_pop) if std_pop > 0 else float("inf")
        Ppl = (mean_ - lsl) / (3 * std_pop) if std_pop > 0 else float("inf")
        Ppk = min(Ppu, Ppl)

        # Sigma level and DPMO
        sigma_level = Cpk * 3 + 1.5  # with 1.5σ shift
        defect_rate_upper = sp_stats.norm.sf(usl, loc=mean_, scale=std_sample)
        defect_rate_lower = sp_stats.norm.cdf(lsl, loc=mean_, scale=std_sample)
        total_defect_rate = defect_rate_upper + defect_rate_lower
        dpmo = total_defect_rate * 1_000_000
        yield_pct = (1 - total_defect_rate) * 100

        result = {
            "n": n, "mean": round(mean_, 4), "std_sample": round(std_sample, 4),
            "LSL": lsl, "USL": usl, "target": tgt,
            "Cp": round(Cp, 4), "Cpk": round(Cpk, 4),
            "Cpu": round(Cpu, 4), "Cpl": round(Cpl, 4), "Cpm": round(Cpm, 4),
            "Pp": round(Pp, 4), "Ppk": round(Ppk, 4),
            "sigma_level": round(sigma_level, 2),
            "DPMO": round(dpmo, 1),
            "yield_pct": round(yield_pct, 4),
        }

        def _grade(cpk):
            if cpk >= 1.67: return "World Class ⭐⭐⭐"
            if cpk >= 1.33: return "Capable ✅"
            if cpk >= 1.00: return "Marginal ⚠️"
            return "Incapable ❌"

        tbl = Table(title="[bold]Process Capability Analysis[/bold]", header_style="bold cyan")
        tbl.add_column("Metric", style="bold")
        tbl.add_column("Value", justify="right")
        tbl.add_column("Interpretation", justify="left")

        rows_disp = [
            ("N",            str(n),                        ""),
            ("Mean",         str(round(mean_, 4)),           ""),
            ("Std Dev (s)",  str(round(std_sample, 4)),      "Short-term"),
            ("LSL",          str(lsl),                       "Lower Spec Limit"),
            ("USL",          str(usl),                       "Upper Spec Limit"),
            ("Target",       str(tgt),                       ""),
            ("Cp",           str(round(Cp, 4)),              "Potential capability"),
            ("Cpk",          str(round(Cpk, 4)),             _grade(Cpk)),
            ("Cpm",          str(round(Cpm, 4)),             "Taguchi index"),
            ("Pp",           str(round(Pp, 4)),              "Long-term potential"),
            ("Ppk",          str(round(Ppk, 4)),             _grade(Ppk)),
            ("Sigma Level",  str(round(sigma_level, 2)),     "with 1.5σ shift"),
            ("DPMO",         f"{dpmo:,.1f}",                 "Defects per million opportunities"),
            ("Yield",        f"{yield_pct:.4f}%",            ""),
        ]
        for label, val, interp in rows_disp:
            tbl.add_row(label, val, interp)
        console.print(tbl)

        if show_plot:
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            fig.suptitle("Process Capability Analysis", fontsize=13, fontweight="bold")

            # Histogram with spec limits
            axes[0].hist(arr, bins="auto", density=True, alpha=0.5,
                         color=colors["primary"], label="Data")
            x_range = np.linspace(min(arr.min(), lsl) - std_sample,
                                  max(arr.max(), usl) + std_sample, 400)
            axes[0].plot(x_range, sp_stats.norm.pdf(x_range, mean_, std_sample),
                         color=colors["secondary"], linewidth=2, label="Normal fit")
            axes[0].axvline(lsl, color=colors["danger"], linewidth=2, ls="--", label=f"LSL={lsl}")
            axes[0].axvline(usl, color=colors["danger"], linewidth=2, ls="--", label=f"USL={usl}")
            axes[0].axvline(mean_, color=colors["success"], linewidth=1.5, ls="-", label=f"Mean={mean_:.3f}")
            axes[0].axvline(tgt, color=colors["accent"], linewidth=1, ls=":", label=f"Target={tgt}")
            axes[0].set_title("Process Distribution vs Spec Limits")
            axes[0].legend(fontsize=8)

            # Capability gauge
            indices = ["Cp", "Cpk", "Pp", "Ppk"]
            vals    = [Cp, Cpk, Pp, Ppk]
            bar_colors = [colors["success"] if v >= 1.33 else
                          colors["accent"] if v >= 1.0 else
                          colors["danger"] for v in vals]
            axes[1].bar(indices, vals, color=bar_colors, edgecolor="white", linewidth=0.5)
            axes[1].axhline(1.00, ls="--", color=colors["accent"],  linewidth=1, label="Min (1.00)")
            axes[1].axhline(1.33, ls="--", color=colors["success"], linewidth=1, label="Good (1.33)")
            axes[1].axhline(1.67, ls="--", color="green",            linewidth=1, label="World class (1.67)")
            axes[1].set_title("Capability Indices")
            axes[1].legend(fontsize=8)
            axes[1].set_ylabel("Index Value")

            plt.tight_layout()
            plt.show()

        return result

    @staticmethod
    def control_chart(
        data,
        column: str,
        chart_type: str = "xbar",
        subgroup_size: int = 5,
        show_plot: bool = True,
        color_scheme: str = "academic",
    ) -> Dict:
        """
        Statistical Process Control chart.

        Parameters
        ----------
        chart_type : 'xbar' | 'r' | 's' | 'p' | 'c' | 'imr'
        subgroup_size : int — for xbar/r/s charts

        Returns
        -------
        dict with UCL, LCL, CL, points_out_of_control
        """
        frame = nw.from_native(data)
        pdf = frame.to_native() if hasattr(frame, "to_native") else pd.DataFrame(data)
        if not isinstance(pdf, pd.DataFrame):
            pdf = pd.DataFrame(pdf)
        arr = pdf[column].dropna().values.astype(float)
        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])

        # SPC constants for subgroup size
        d2 = {2:1.128,3:1.693,4:2.059,5:2.326,6:2.534,7:2.704,8:2.847,9:2.970,10:3.078}
        D3 = {2:0,3:0,4:0,5:0,6:0,7:0.076,8:0.136,9:0.184,10:0.223}
        D4 = {2:3.267,3:2.574,4:2.282,5:2.114,6:2.004,7:1.924,8:1.864,9:1.816,10:1.777}
        A2 = {2:1.880,3:1.023,4:0.729,5:0.577,6:0.483,7:0.419,8:0.373,9:0.337,10:0.308}

        n = subgroup_size
        if chart_type in ("xbar", "r", "s"):
            # Reshape into subgroups
            n_subgroups = len(arr) // n
            arr = arr[:n_subgroups * n].reshape(n_subgroups, n)
            subgroup_means = arr.mean(axis=1)
            subgroup_ranges = arr.max(axis=1) - arr.min(axis=1)
            subgroup_stds = arr.std(axis=1, ddof=1)

            grand_mean = subgroup_means.mean()
            mean_R = subgroup_ranges.mean()
            mean_S = subgroup_stds.mean()

            if chart_type == "xbar":
                CL = grand_mean
                UCL = grand_mean + A2.get(n, 0.577) * mean_R
                LCL = grand_mean - A2.get(n, 0.577) * mean_R
                points = subgroup_means
                title = f"X̄ (X-bar) Chart  n={n}"
                ylabel = "Subgroup Mean"
            elif chart_type == "r":
                CL = mean_R
                UCL = D4.get(n, 2.114) * mean_R
                LCL = D3.get(n, 0) * mean_R
                points = subgroup_ranges
                title = "R Chart (Range)"
                ylabel = "Subgroup Range"
            else:  # s
                c4 = {2:0.7979,3:0.8862,4:0.9213,5:0.9400,6:0.9515,7:0.9594,8:0.9650,9:0.9693,10:0.9727}
                B3 = {2:0,3:0,4:0,5:0,6:0.030,7:0.118,8:0.185,9:0.239,10:0.284}
                B4 = {2:3.267,3:2.568,4:2.266,5:2.089,6:1.970,7:1.882,8:1.815,9:1.761,10:1.716}
                CL = mean_S
                UCL = B4.get(n, 2.089) * mean_S
                LCL = B3.get(n, 0) * mean_S
                points = subgroup_stds
                title = "S Chart (Standard Deviation)"
                ylabel = "Subgroup Std Dev"

        elif chart_type == "imr":  # Individuals and Moving Range
            moving_ranges = np.abs(np.diff(arr))
            mean_MR = moving_ranges.mean()
            CL = arr.mean()
            UCL = CL + 3 * mean_MR / d2[2]
            LCL = CL - 3 * mean_MR / d2[2]
            points = arr
            title = "I (Individuals) Chart"
            ylabel = "Individual Value"
        else:  # p or c — attribute charts
            rate = arr.mean()
            CL = rate
            if chart_type == "p":
                UCL = rate + 3 * np.sqrt(rate * (1 - rate) / n)
                LCL = max(0, rate - 3 * np.sqrt(rate * (1 - rate) / n))
                title = "p Chart (Proportion)"
                ylabel = "Proportion Defective"
            else:  # c
                UCL = rate + 3 * np.sqrt(rate)
                LCL = max(0, rate - 3 * np.sqrt(rate))
                title = "c Chart (Count of Defects)"
                ylabel = "Defect Count"
            points = arr

        out_of_control = np.where((points > UCL) | (points < LCL))[0].tolist()

        result = {
            "CL": round(float(CL), 4), "UCL": round(float(UCL), 4), "LCL": round(float(LCL), 4),
            "points_out_of_control": out_of_control,
            "n_out": len(out_of_control),
            "chart_type": chart_type,
        }

        console.print(f"[bold]📊 {title}[/bold]")
        console.print(f"  CL={CL:.4f}  UCL={UCL:.4f}  LCL={LCL:.4f}")
        console.print(f"  Points out of control: {len(out_of_control)} → {out_of_control[:10]}")

        if show_plot:
            fig, ax = plt.subplots(figsize=(14, 5))
            x = range(len(points))
            ax.plot(x, points, color=colors["primary"], marker="o", markersize=5,
                    linewidth=1.5, label="Data")
            ax.axhline(CL,  color=colors["success"], linewidth=2, ls="-",  label=f"CL={CL:.3f}")
            ax.axhline(UCL, color=colors["danger"],  linewidth=1.5, ls="--", label=f"UCL={UCL:.3f}")
            ax.axhline(LCL, color=colors["danger"],  linewidth=1.5, ls="--", label=f"LCL={LCL:.3f}")
            ax.fill_between(x, LCL, UCL, alpha=0.05, color=colors["success"])

            for idx in out_of_control:
                ax.scatter(idx, points[idx], color=colors["danger"], s=80, zorder=5)

            ax.set_title(title, fontsize=13, fontweight="bold")
            ax.set_xlabel("Subgroup / Observation")
            ax.set_ylabel(ylabel)
            ax.legend(fontsize=9)
            plt.tight_layout()
            plt.show()

        return result

    @staticmethod
    def pareto(
        data,
        category_col: str,
        value_col: Optional[str] = None,
        show_plot: bool = True,
        color_scheme: str = "academic",
        top_n: int = 20,
    ) -> pd.DataFrame:
        """
        Pareto chart — identify the vital few causes (80/20 rule).

        Parameters
        ----------
        data : DataFrame
        category_col : str — categorical column (defect types, etc.)
        value_col : str or None (counts each row if None)
        top_n : int — show top N categories

        Returns
        -------
        pd.DataFrame with Category, Count/Value, Cumulative %
        """
        frame = nw.from_native(data)
        pdf = frame.to_native() if hasattr(frame, "to_native") else pd.DataFrame(data)
        if not isinstance(pdf, pd.DataFrame):
            pdf = pd.DataFrame(pdf)

        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])

        if value_col:
            grouped = pdf.groupby(category_col)[value_col].sum().sort_values(ascending=False)
        else:
            grouped = pdf[category_col].value_counts()

        grouped = grouped.head(top_n)
        total = grouped.sum()
        cum_pct = (grouped.cumsum() / total * 100)

        result = pd.DataFrame({
            "Category": grouped.index,
            "Count": grouped.values,
            "Relative %": (grouped.values / total * 100).round(2),
            "Cumulative %": cum_pct.values.round(2),
        })

        tbl = Table(title="[bold]Pareto Analysis[/bold]", header_style="bold cyan")
        for col in result.columns:
            tbl.add_column(col, justify="right" if col != "Category" else "left")
        for _, row in result.iterrows():
            tbl.add_row(*[str(v) for v in row])
        console.print(tbl)

        # Find 80% cutoff
        cutoff_idx = (result["Cumulative %"] >= 80).idxmax()
        console.print(f"[bold]80% of issues covered by first {cutoff_idx + 1} categories[/bold]")

        if show_plot:
            fig, ax1 = plt.subplots(figsize=(12, 5))
            ax2 = ax1.twinx()

            bars = ax1.bar(result["Category"], result["Count"],
                           color=colors["primary"], edgecolor="white", linewidth=0.5)
            ax2.plot(result["Category"], result["Cumulative %"],
                     color=colors["danger"], marker="o", linewidth=2, label="Cumulative %")
            ax2.axhline(80, ls="--", color=colors["accent"], linewidth=1, label="80%")

            ax1.set_xlabel("Category")
            ax1.set_ylabel("Count / Value", color=colors["primary"])
            ax2.set_ylabel("Cumulative %", color=colors["danger"])
            ax1.tick_params(axis="x", rotation=45)
            ax2.set_ylim(0, 110)
            ax2.legend(fontsize=9, loc="center right")
            plt.title("Pareto Chart", fontsize=13, fontweight="bold")
            plt.tight_layout()
            plt.show()

        return result

    @staticmethod
    def fishbone(
        categories: Dict[str, List[str]],
        effect: str = "Problem / Effect",
        color_scheme: str = "academic",
    ) -> None:
        """
        Draw a Cause-and-Effect (Ishikawa / Fishbone) diagram.

        Parameters
        ----------
        categories : dict — {category: [cause1, cause2, ...]}
            e.g. {"Machine": ["Worn tool", "Vibration"],
                  "Method": ["No SOP", "Poor training"]}
        effect : str — the effect (head of the fish)

        Example
        -------
        quality.fishbone({
            "Machine": ["Worn tool", "Calibration"],
            "Method":  ["No SOP", "Training gaps"],
            "Material": ["Wrong grade", "Moisture"],
            "Man":     ["Fatigue", "Skill gap"],
            "Measurement": ["Wrong gauge", "Human error"],
            "Environment": ["Temperature", "Humidity"],
        }, effect="High Defect Rate")
        """
        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])
        cat_list = list(categories.keys())
        n_cats = len(cat_list)

        fig, ax = plt.subplots(figsize=(16, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis("off")
        fig.patch.set_facecolor("white")

        # Spine (horizontal arrow)
        ax.annotate("", xy=(9.5, 3), xytext=(0.5, 3),
                    arrowprops=dict(arrowstyle="->", lw=2, color="black"))

        # Effect box
        ax.text(9.7, 3, effect, ha="left", va="center", fontsize=11, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.4", facecolor=colors["danger"], alpha=0.8),
                color="white")

        # Categories alternate above/below spine
        positions = np.linspace(1.5, 8.5, n_cats)
        above = [i % 2 == 0 for i in range(n_cats)]

        for i, (cat, pos, up) in enumerate(zip(cat_list, positions, above)):
            color = colors["palette"][i % len(colors["palette"])]
            y_bone = 4.5 if up else 1.5
            # Diagonal bone
            ax.annotate("", xy=(pos + 0.4, 3), xytext=(pos, y_bone),
                        arrowprops=dict(arrowstyle="->", lw=1.5, color=color))
            # Category label
            ax.text(pos, y_bone + (0.3 if up else -0.3), cat, ha="center", va="bottom" if up else "top",
                    fontsize=10, fontweight="bold", color=color)

            # Sub-causes
            causes = categories[cat]
            for j, cause in enumerate(causes):
                x_off = pos - 0.15 - j * 0.3
                y_cause = y_bone + (0.8 + j * 0.35) if up else y_bone - (0.8 + j * 0.35)
                ax.text(x_off, y_cause, f"→ {cause}", ha="right" if up else "left",
                        va="center", fontsize=7.5, color="gray")

        ax.set_title(f"Cause-and-Effect Diagram: {effect}", fontsize=13, fontweight="bold", pad=15)
        plt.tight_layout()
        plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# PROJECT MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────

class project:
    """
    Project management charts and network analysis.

    Methods
    -------
    gantt(tasks)                     — Gantt chart from list of task dicts
    network(tasks, dependencies)     — Network diagram with critical path (CPM)
    pert(tasks)                      — PERT analysis with optimistic/most-likely/pessimistic
    """

    @staticmethod
    def gantt(
        tasks: List[Dict],
        title: str = "Project Gantt Chart",
        color_scheme: str = "academic",
        date_format: str = "%Y-%m-%d",
    ) -> pd.DataFrame:
        """
        Draw a Gantt chart.

        Parameters
        ----------
        tasks : list of dicts with keys:
            - 'task'    : str — task name
            - 'start'   : str or int — start date/day
            - 'end'     : str or int — end date/day
            - 'resource': str (optional) — owner/resource
            - 'progress': float 0-100 (optional) — completion %

        Example
        -------
        project.gantt([
            {"task": "Design",    "start": "2024-01-01", "end": "2024-01-10", "resource": "Alice"},
            {"task": "Dev",       "start": "2024-01-08", "end": "2024-01-25", "resource": "Bob"},
            {"task": "Testing",   "start": "2024-01-22", "end": "2024-02-01", "resource": "Alice"},
        ])
        """
        import datetime
        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])

        df = pd.DataFrame(tasks)

        # Determine if dates or numeric
        use_dates = isinstance(df["start"].iloc[0], str)
        if use_dates:
            df["start_dt"] = pd.to_datetime(df["start"])
            df["end_dt"]   = pd.to_datetime(df["end"])
            min_date = df["start_dt"].min()
            df["start_num"] = (df["start_dt"] - min_date).dt.days
            df["end_num"]   = (df["end_dt"]   - min_date).dt.days
        else:
            df["start_num"] = df["start"].astype(float)
            df["end_num"]   = df["end"].astype(float)
            min_date = None

        df["duration"] = df["end_num"] - df["start_num"]
        df = df.reset_index(drop=True)
        n_tasks = len(df)

        # Print table
        tbl = Table(title=f"[bold]{title}[/bold]", header_style="bold cyan")
        for col in ["task", "start", "end", "duration"] + (["resource"] if "resource" in df.columns else []):
            tbl.add_column(col.capitalize(), justify="right" if col == "duration" else "left")
        for _, row in df.iterrows():
            vals = [str(row["task"]), str(row["start"]), str(row["end"]), str(row["duration"])]
            if "resource" in df.columns:
                vals.append(str(row.get("resource", "")))
            tbl.add_row(*vals)
        console.print(tbl)

        # Plot
        fig, ax = plt.subplots(figsize=(14, max(5, n_tasks * 0.6 + 2)))
        resources = df.get("resource", pd.Series([""] * n_tasks)) if "resource" in df.columns else pd.Series([""] * n_tasks)
        resource_list = resources.unique().tolist()

        for i, (_, row) in enumerate(df.iterrows()):
            res = row.get("resource", "") if "resource" in df.columns else ""
            res_idx = resource_list.index(res) if res in resource_list else 0
            color = colors["palette"][res_idx % len(colors["palette"])]
            y = n_tasks - 1 - i
            ax.barh(y, row["duration"], left=row["start_num"], height=0.6,
                    color=color, edgecolor="white", linewidth=0.5, alpha=0.85)
            # Progress bar overlay
            if "progress" in row and not pd.isna(row.get("progress")):
                prog_width = row["duration"] * row["progress"] / 100
                ax.barh(y, prog_width, left=row["start_num"], height=0.6,
                        color="white", alpha=0.25)
                ax.text(row["start_num"] + row["duration"] / 2, y,
                        f"{row['progress']:.0f}%", ha="center", va="center",
                        fontsize=7, color="white", fontweight="bold")

            task_label = row["task"] + (f" ({res})" if res else "")
            ax.text(row["start_num"] - 0.2, y, task_label, ha="right", va="center", fontsize=9)

        ax.set_yticks([])
        ax.set_xlabel("Days" if not use_dates else "Days from project start")
        ax.set_title(title, fontsize=13, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        plt.show()

        return df

    @staticmethod
    def network(
        tasks: List[Dict],
        dependencies: Dict[str, List[str]],
        title: str = "Project Network (CPM)",
        color_scheme: str = "academic",
    ) -> Dict:
        """
        Network diagram with Critical Path Method (CPM) analysis.

        Parameters
        ----------
        tasks : list of dicts with 'id', 'name', 'duration'
        dependencies : dict — {task_id: [predecessor_ids]}

        Example
        -------
        tasks = [
            {"id":"A","name":"Design","duration":5},
            {"id":"B","name":"Coding","duration":8},
            {"id":"C","name":"Testing","duration":4},
        ]
        deps = {"A":[], "B":["A"], "C":["B"]}
        project.network(tasks, deps)

        Returns
        -------
        dict with critical_path, project_duration, slack per task
        """
        try:
            import networkx as nx
        except ImportError:
            console.print("[red]networkx not installed. Run: pip install networkx[/red]")
            return {}

        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])
        task_map = {t["id"]: t for t in tasks}

        G = nx.DiGraph()
        for t in tasks:
            G.add_node(t["id"], name=t["name"], duration=t["duration"])
        for tid, preds in dependencies.items():
            for pred in preds:
                G.add_edge(pred, tid)

        # Forward pass
        ES = {}; EF = {}
        for node in nx.topological_sort(G):
            preds = list(G.predecessors(node))
            ES[node] = max((EF[p] for p in preds), default=0)
            EF[node] = ES[node] + task_map[node]["duration"]

        project_duration = max(EF.values())

        # Backward pass
        LS = {}; LF = {}
        for node in reversed(list(nx.topological_sort(G))):
            succs = list(G.successors(node))
            LF[node] = min((LS[s] for s in succs), default=project_duration)
            LS[node] = LF[node] - task_map[node]["duration"]

        slack = {n: LS[n] - ES[n] for n in G.nodes}
        critical_path = [n for n in G.nodes if slack[n] == 0]

        # Print results table
        tbl = Table(title="[bold]CPM Network Analysis[/bold]", header_style="bold cyan")
        for col in ["ID", "Name", "Duration", "ES", "EF", "LS", "LF", "Slack", "Critical"]:
            tbl.add_column(col, justify="right" if col not in ("ID","Name","Critical") else "left")
        for n in nx.topological_sort(G):
            t = task_map[n]
            is_crit = "✅" if n in critical_path else ""
            tbl.add_row(n, t["name"], str(t["duration"]),
                        str(ES[n]), str(EF[n]), str(LS[n]), str(LF[n]),
                        str(slack[n]), is_crit)
        console.print(tbl)
        console.print(f"[bold]🔴 Critical Path: {' → '.join(critical_path)}[/bold]")
        console.print(f"[bold]📅 Project Duration: {project_duration} days[/bold]")

        # Plot
        try:
            fig, ax = plt.subplots(figsize=(14, 7))
            ax.set_title(f"{title}\nCritical Path: {' → '.join(critical_path)} | Duration: {project_duration}d",
                         fontsize=11, fontweight="bold")

            pos = nx.spring_layout(G, seed=42, k=2)
            node_colors = [colors["danger"] if n in critical_path else colors["primary"] for n in G.nodes]
            labels = {n: f"{n}\n{task_map[n]['name']}\n({task_map[n]['duration']}d)" for n in G.nodes}

            nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=2000, alpha=0.9)
            nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=7, font_color="white", font_weight="bold")
            edge_colors = [colors["danger"] if (u in critical_path and v in critical_path) else "gray"
                           for u, v in G.edges()]
            nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors,
                                   arrows=True, arrowsize=20, width=2, connectionstyle="arc3,rad=0.1")
            ax.axis("off")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            console.print(f"[yellow]Plot skipped: {e}[/yellow]")

        return {
            "critical_path": critical_path,
            "project_duration": project_duration,
            "slack": slack,
            "ES": ES, "EF": EF, "LS": LS, "LF": LF,
        }

    @staticmethod
    def pert(
        tasks: List[Dict],
        title: str = "PERT Analysis",
    ) -> pd.DataFrame:
        """
        PERT (Program Evaluation and Review Technique) analysis.

        Parameters
        ----------
        tasks : list of dicts with:
            - 'id'       : str
            - 'name'     : str
            - 'optimistic': float (o)
            - 'likely'   : float (m) — most likely
            - 'pessimistic': float (p)
            - predecessors: list of str (optional)

        Returns
        -------
        pd.DataFrame with PERT expected time, variance, std dev
        """
        rows = []
        for t in tasks:
            o, m, p = t["optimistic"], t["likely"], t["pessimistic"]
            te = (o + 4 * m + p) / 6
            var = ((p - o) / 6) ** 2
            std = var ** 0.5
            rows.append({
                "ID": t["id"],
                "Name": t["name"],
                "Optimistic": o,
                "Most Likely": m,
                "Pessimistic": p,
                "Expected (te)": round(te, 3),
                "Variance (σ²)": round(var, 4),
                "Std Dev (σ)": round(std, 4),
            })

        result = pd.DataFrame(rows)

        tbl = Table(title=f"[bold]{title}[/bold]", header_style="bold cyan")
        for col in result.columns:
            tbl.add_column(col, justify="right" if col not in ("ID","Name") else "left")
        for _, row in result.iterrows():
            tbl.add_row(*[str(v) for v in row])
        console.print(tbl)

        total_te  = result["Expected (te)"].sum()
        total_var = result["Variance (σ²)"].sum()
        total_std = total_var ** 0.5
        console.print(f"[bold]Total Expected Duration: {total_te:.2f} | σ²={total_var:.4f} | σ={total_std:.4f}[/bold]")

        return result


# ─────────────────────────────────────────────────────────────────────────────
# TEXT ANALYTICS
# ─────────────────────────────────────────────────────────────────────────────

class text:
    """
    Text analytics — word cloud, frequency, sentiment, TF-IDF.

    Methods
    -------
    wordcloud(texts, ...)             — Word cloud visualization
    frequency(texts, n=1, top_n=20)  — Word/n-gram frequency table + bar chart
    sentiment(texts, ...)            — Sentence-level sentiment scores
    tfidf(texts, top_n=10, ...)      — TF-IDF keyword extraction per document
    """

    @staticmethod
    def _tokenize(text_str: str, stopwords_extra: Optional[List[str]] = None) -> List[str]:
        import re
        STOP = {
            "the","a","an","and","or","but","in","on","at","to","for","of","with",
            "is","it","its","was","are","be","been","being","have","has","had",
            "do","does","did","will","would","could","should","may","might","shall",
            "that","this","these","those","i","we","you","he","she","they","my",
            "our","your","his","her","their","not","no","nor","so","yet","both",
            "either","neither","as","if","then","than","because","while","although",
            "though","since","after","before","when","where","how","what","which","who",
        }
        if stopwords_extra:
            STOP.update(stopwords_extra)
        words = re.findall(r"\b[a-zA-Z]{2,}\b", text_str.lower())
        return [w for w in words if w not in STOP]

    @staticmethod
    def wordcloud(
        texts,
        column: Optional[str] = None,
        stopwords: Optional[List[str]] = None,
        max_words: int = 100,
        title: str = "Word Cloud",
        color_scheme: str = "academic",
    ) -> None:
        """
        Generate a word cloud from text data.

        Parameters
        ----------
        texts : str | list of str | DataFrame
        column : str — if DataFrame, which column contains text
        stopwords : list of additional stop words
        max_words : int
        """
        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])

        # Gather all text
        if isinstance(texts, str):
            all_text = texts
        elif isinstance(texts, (list, tuple)):
            all_text = " ".join(str(t) for t in texts)
        else:
            frame = nw.from_native(texts)
            pdf = frame.to_native() if hasattr(frame, "to_native") else pd.DataFrame(texts)
            if not isinstance(pdf, pd.DataFrame):
                pdf = pd.DataFrame(pdf)
            col = column or pdf.select_dtypes(include="object").columns[0]
            all_text = " ".join(pdf[col].dropna().astype(str).tolist())

        try:
            from wordcloud import WordCloud as WC
            wc = WC(
                max_words=max_words,
                background_color="white",
                width=1200, height=600,
                colormap="Blues",
                stopwords=set(stopwords or []),
                prefer_horizontal=0.9,
                collocations=False,
            )
            wc.generate(all_text)
            fig, ax = plt.subplots(figsize=(14, 6))
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
            plt.tight_layout()
            plt.show()
        except ImportError:
            # Fallback: frequency bar chart
            console.print("[yellow]wordcloud not installed — showing frequency bar chart instead.[/yellow]")
            console.print("[dim]Install with: pip install wordcloud[/dim]")
            tokens = text._tokenize(all_text, stopwords)
            from collections import Counter
            freq = Counter(tokens).most_common(30)
            words_list = [f[0] for f in freq]
            counts_list = [f[1] for f in freq]
            colors_bar = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.barh(words_list[::-1], counts_list[::-1], color=colors_bar["primary"])
            ax.set_title(f"{title} (Word Frequency)", fontsize=13, fontweight="bold")
            ax.set_xlabel("Frequency")
            plt.tight_layout()
            plt.show()

    @staticmethod
    def frequency(
        texts,
        column: Optional[str] = None,
        n: int = 1,
        top_n: int = 20,
        stopwords: Optional[List[str]] = None,
        show_plot: bool = True,
        color_scheme: str = "academic",
    ) -> pd.DataFrame:
        """
        Word (unigram) or n-gram frequency analysis.

        Parameters
        ----------
        texts : str | list | DataFrame
        column : str (if DataFrame)
        n : int — 1=unigram, 2=bigram, 3=trigram
        top_n : int — return top N terms

        Returns
        -------
        pd.DataFrame — Term, Count, Relative %
        """
        from collections import Counter
        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])

        if isinstance(texts, str):
            all_text = texts
        elif isinstance(texts, (list, tuple)):
            all_text = " ".join(str(t) for t in texts)
        else:
            frame = nw.from_native(texts)
            pdf = frame.to_native() if hasattr(frame, "to_native") else pd.DataFrame(texts)
            if not isinstance(pdf, pd.DataFrame):
                pdf = pd.DataFrame(pdf)
            col = column or pdf.select_dtypes(include="object").columns[0]
            all_text = " ".join(pdf[col].dropna().astype(str).tolist())

        tokens = text._tokenize(all_text, stopwords)

        if n == 1:
            grams = tokens
        else:
            grams = [" ".join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

        counts = Counter(grams).most_common(top_n)
        total = sum(c for _, c in counts)
        result = pd.DataFrame(counts, columns=["Term", "Count"])
        result["Relative %"] = (result["Count"] / total * 100).round(2)

        gram_label = {1:"Unigram (Word)", 2:"Bigram", 3:"Trigram"}.get(n, f"{n}-gram")
        tbl = Table(title=f"[bold]{gram_label} Frequency — Top {top_n}[/bold]", header_style="bold cyan")
        for col in result.columns:
            tbl.add_column(col, justify="right" if col != "Term" else "left")
        for _, row in result.iterrows():
            tbl.add_row(*[str(v) for v in row])
        console.print(tbl)

        if show_plot:
            fig, ax = plt.subplots(figsize=(12, max(5, top_n * 0.35)))
            ax.barh(result["Term"][::-1], result["Count"][::-1],
                    color=colors["primary"], edgecolor="white", linewidth=0.3)
            ax.set_xlabel("Frequency")
            ax.set_title(f"{gram_label} Frequency — Top {top_n}", fontsize=13, fontweight="bold")
            plt.tight_layout()
            plt.show()

        return result

    @staticmethod
    def sentiment(
        texts,
        column: Optional[str] = None,
        show_plot: bool = True,
        color_scheme: str = "academic",
    ) -> pd.DataFrame:
        """
        Sentence-level sentiment analysis.

        Uses VADER (fast, lexicon-based) if available, else rule-based fallback.

        Parameters
        ----------
        texts : list of str | DataFrame
        column : str (if DataFrame)

        Returns
        -------
        pd.DataFrame — Text, Positive, Negative, Neutral, Compound, Sentiment
        """
        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])

        if isinstance(texts, (list, tuple)):
            text_list = [str(t) for t in texts]
        elif isinstance(texts, str):
            text_list = [texts]
        else:
            frame = nw.from_native(texts)
            pdf = frame.to_native() if hasattr(frame, "to_native") else pd.DataFrame(texts)
            if not isinstance(pdf, pd.DataFrame):
                pdf = pd.DataFrame(pdf)
            col = column or pdf.select_dtypes(include="object").columns[0]
            text_list = pdf[col].dropna().astype(str).tolist()

        rows = []
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            sia = SentimentIntensityAnalyzer()
            for t in text_list:
                scores = sia.polarity_scores(t)
                label = "Positive" if scores["compound"] >= 0.05 else \
                        "Negative" if scores["compound"] <= -0.05 else "Neutral"
                rows.append({
                    "Text": t[:60] + ("..." if len(t) > 60 else ""),
                    "Positive": round(scores["pos"], 3),
                    "Negative": round(scores["neg"], 3),
                    "Neutral":  round(scores["neu"], 3),
                    "Compound": round(scores["compound"], 3),
                    "Sentiment": label,
                })
            method_note = "VADER"
        except ImportError:
            try:
                from textblob import TextBlob
                for t in text_list:
                    tb = TextBlob(t)
                    pol = tb.sentiment.polarity
                    sub = tb.sentiment.subjectivity
                    label = "Positive" if pol > 0.05 else "Negative" if pol < -0.05 else "Neutral"
                    rows.append({
                        "Text": t[:60] + ("..." if len(t) > 60 else ""),
                        "Polarity": round(pol, 3),
                        "Subjectivity": round(sub, 3),
                        "Compound": round(pol, 3),
                        "Sentiment": label,
                    })
                method_note = "TextBlob"
            except ImportError:
                # Simple rule-based fallback
                POS_WORDS = {"good","great","excellent","best","wonderful","amazing","love","happy","positive","success"}
                NEG_WORDS = {"bad","worst","terrible","hate","poor","awful","negative","fail","sad","wrong"}
                for t in text_list:
                    words = set(t.lower().split())
                    pos = len(words & POS_WORDS)
                    neg = len(words & NEG_WORDS)
                    compound = (pos - neg) / max(len(words), 1)
                    label = "Positive" if compound > 0 else "Negative" if compound < 0 else "Neutral"
                    rows.append({"Text": t[:60]+"..." if len(t)>60 else t,
                                 "Positive": pos, "Negative": neg,
                                 "Compound": round(compound, 3), "Sentiment": label})
                method_note = "Rule-based (install vaderSentiment or textblob for better results)"

        result = pd.DataFrame(rows)

        tbl = Table(title=f"[bold]Sentiment Analysis ({method_note})[/bold]", header_style="bold cyan")
        for col in result.columns:
            tbl.add_column(col, justify="left" if col in ("Text","Sentiment") else "right")
        for _, row in result.iterrows():
            tbl.add_row(*[str(v) for v in row])
        console.print(tbl)

        if show_plot and "Sentiment" in result.columns:
            sentiment_counts = result["Sentiment"].value_counts()
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))
            fig.suptitle(f"Sentiment Distribution ({method_note})", fontsize=13, fontweight="bold")

            bar_cols = [colors["success"] if s == "Positive" else
                        colors["danger"] if s == "Negative" else
                        colors["accent"] for s in sentiment_counts.index]
            axes[0].bar(sentiment_counts.index, sentiment_counts.values,
                        color=bar_cols, edgecolor="white", linewidth=0.5)
            axes[0].set_title("Sentiment Count")
            axes[0].set_ylabel("Count")

            axes[1].pie(sentiment_counts.values, labels=sentiment_counts.index,
                        colors=bar_cols, autopct="%1.1f%%", startangle=90)
            axes[1].set_title("Sentiment Proportion")

            plt.tight_layout()
            plt.show()

        return result

    @staticmethod
    def tfidf(
        texts,
        column: Optional[str] = None,
        top_n: int = 10,
        max_features: int = 1000,
        show_plot: bool = True,
        color_scheme: str = "academic",
    ) -> pd.DataFrame:
        """
        TF-IDF keyword extraction across a corpus.

        Parameters
        ----------
        texts : list of str | DataFrame
        column : str (if DataFrame)
        top_n : int — top keywords per document shown in summary
        max_features : int

        Returns
        -------
        pd.DataFrame — overall TF-IDF scores (term, score)
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
        except ImportError:
            console.print("[red]scikit-learn required. Run: pip install scikit-learn[/red]")
            return pd.DataFrame()

        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])

        if isinstance(texts, (list, tuple)):
            corpus = [str(t) for t in texts]
        elif isinstance(texts, str):
            corpus = [texts]
        else:
            frame = nw.from_native(texts)
            pdf = frame.to_native() if hasattr(frame, "to_native") else pd.DataFrame(texts)
            if not isinstance(pdf, pd.DataFrame):
                pdf = pd.DataFrame(pdf)
            col = column or pdf.select_dtypes(include="object").columns[0]
            corpus = pdf[col].dropna().astype(str).tolist()

        vectorizer = TfidfVectorizer(max_features=max_features, stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(corpus)
        feature_names = vectorizer.get_feature_names_out()

        # Mean TF-IDF across corpus
        mean_scores = np.asarray(tfidf_matrix.mean(axis=0)).flatten()
        top_idx = mean_scores.argsort()[-top_n:][::-1]
        result = pd.DataFrame({
            "Term": feature_names[top_idx],
            "TF-IDF Score": np.round(mean_scores[top_idx], 5),
        })

        tbl = Table(title=f"[bold]TF-IDF Top {top_n} Keywords (corpus mean)[/bold]", header_style="bold cyan")
        for col in result.columns:
            tbl.add_column(col, justify="left" if col == "Term" else "right")
        for _, row in result.iterrows():
            tbl.add_row(*[str(v) for v in row])
        console.print(tbl)

        if show_plot:
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.barh(result["Term"][::-1], result["TF-IDF Score"][::-1],
                    color=colors["primary"], edgecolor="white", linewidth=0.3)
            ax.set_xlabel("Mean TF-IDF Score")
            ax.set_title(f"Top {top_n} Keywords by TF-IDF", fontsize=13, fontweight="bold")
            plt.tight_layout()
            plt.show()

        # Per-document top keywords
        if len(corpus) > 1:
            console.print("\n[bold]Per-document top keywords:[/bold]")
            for i, doc in enumerate(corpus[:min(5, len(corpus))]):
                doc_scores = np.asarray(tfidf_matrix[i].todense()).flatten()
                top_doc = doc_scores.argsort()[-5:][::-1]
                kws = ", ".join(feature_names[top_doc])
                short = doc[:50] + "..." if len(doc) > 50 else doc
                console.print(f"  Doc {i+1} [{short}]: {kws}")

        return result


# ─────────────────────────────────────────────────────────────────────────────
# MONTE CARLO SIMULATION
# ─────────────────────────────────────────────────────────────────────────────

class simulate:
    """
    Monte Carlo simulation and stochastic modelling.

    Methods
    -------
    run(model_fn, n_trials, inputs, ...)
        Generic Monte Carlo engine: run any Python function with random inputs
    npv(cash_flows_dist, discount_rate_dist, n_trials, ...)
        Project NPV simulation with uncertainty
    inventory(demand_dist, lead_time_dist, order_qty, reorder_point, ...)
        Inventory simulation: stockouts, service level
    risk_matrix(risks, ...)
        Risk register: probability × impact simulation
    bootstrap(data, column, statistic, n_trials, ...)
        Bootstrap confidence intervals for any statistic
    """

    @staticmethod
    def _sample_dist(dist_spec: Dict, n: int) -> np.ndarray:
        """
        Sample n values from a distribution specification dict.

        Supported specs:
            {"dist": "normal",   "mean": 100, "std": 10}
            {"dist": "uniform",  "low": 50,  "high": 150}
            {"dist": "triangular","low": 80, "mode": 100, "high": 130}
            {"dist": "lognormal","mean": 4.5, "sigma": 0.3}
            {"dist": "poisson",  "lam": 20}
            {"dist": "binomial", "n": 100, "p": 0.3}
            {"dist": "fixed",    "value": 42}
        """
        d = dist_spec.get("dist", "normal").lower()
        if d in ("normal", "gaussian"):
            return np.random.normal(dist_spec.get("mean", 0), dist_spec.get("std", 1), n)
        elif d == "uniform":
            return np.random.uniform(dist_spec.get("low", 0), dist_spec.get("high", 1), n)
        elif d in ("triangular", "triangle"):
            return np.random.triangular(dist_spec["low"], dist_spec["mode"], dist_spec["high"], n)
        elif d == "lognormal":
            return np.random.lognormal(dist_spec.get("mean", 0), dist_spec.get("sigma", 1), n)
        elif d == "poisson":
            return np.random.poisson(dist_spec.get("lam", 1), n).astype(float)
        elif d in ("binomial", "binom"):
            return np.random.binomial(dist_spec.get("n", 10), dist_spec.get("p", 0.5), n).astype(float)
        elif d in ("exponential", "expon"):
            return np.random.exponential(dist_spec.get("scale", 1), n)
        elif d == "fixed":
            return np.full(n, dist_spec.get("value", 0), dtype=float)
        elif d in ("beta",):
            return np.random.beta(dist_spec.get("a", 2), dist_spec.get("b", 5), n)
        else:
            raise ValueError(f"Unknown distribution: {d}. Supported: normal, uniform, triangular, "
                             "lognormal, poisson, binomial, exponential, beta, fixed")

    @staticmethod
    def run(
        model_fn,
        n_trials: int = 10_000,
        inputs: Optional[Dict[str, Dict]] = None,
        seed: Optional[int] = 42,
        percentiles: Optional[List[float]] = None,
        show_plot: bool = True,
        color_scheme: str = "academic",
    ) -> Dict:
        """
        Generic Monte Carlo simulation engine.

        Parameters
        ----------
        model_fn : callable — accepts **kwargs of sampled inputs, returns float
        n_trials : int — number of simulation trials (default 10,000)
        inputs : dict of {param_name: dist_spec_dict}
        seed : int or None

        Example
        -------
        # Profit = Revenue - Cost with uncertain inputs
        simulate.run(
            model_fn = lambda revenue, cost: revenue - cost,
            n_trials  = 10000,
            inputs    = {
                "revenue": {"dist": "normal",   "mean": 500, "std": 50},
                "cost":    {"dist": "triangular","low": 300, "mode": 350, "high": 450},
            }
        )

        Returns
        -------
        dict with results array, mean, std, percentiles, P(>0), etc.
        """
        if seed is not None:
            np.random.seed(seed)
        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])
        inputs = inputs or {}
        pcts   = percentiles or [5, 10, 25, 50, 75, 90, 95]

        # Sample all inputs
        sampled = {k: simulate._sample_dist(v, n_trials) for k, v in inputs.items()}

        # Run model
        results = np.array([model_fn(**{k: sampled[k][i] for k in sampled})
                             for i in range(n_trials)], dtype=float)

        mean_  = np.mean(results)
        std_   = np.std(results, ddof=1)
        p_gt0  = np.mean(results > 0) * 100
        p_lt0  = np.mean(results < 0) * 100
        pct_vals = {f"P{int(p)}": round(np.percentile(results, p), 4) for p in pcts}

        output = {
            "n_trials": n_trials,
            "mean": round(mean_, 4),
            "std":  round(std_, 4),
            "min":  round(float(results.min()), 4),
            "max":  round(float(results.max()), 4),
            "P(>0)%": round(p_gt0, 2),
            "P(<0)%": round(p_lt0, 2),
            **pct_vals,
            "_results": results,
        }

        tbl = Table(title=f"[bold]Monte Carlo Simulation (n={n_trials:,})[/bold]", header_style="bold cyan")
        tbl.add_column("Metric", style="bold")
        tbl.add_column("Value", justify="right")
        for k, v in output.items():
            if k != "_results":
                tbl.add_row(k, f"{v:,.4f}" if isinstance(v, float) else str(v))
        console.print(tbl)

        if show_plot:
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            fig.suptitle(f"Monte Carlo Results  n={n_trials:,}", fontsize=13, fontweight="bold")

            axes[0].hist(results, bins=60, density=True, alpha=0.6,
                         color=colors["primary"], edgecolor="white", linewidth=0.3)
            axes[0].axvline(mean_, color=colors["secondary"], linewidth=2, label=f"Mean={mean_:.2f}")
            axes[0].axvline(pct_vals.get("P5", np.percentile(results, 5)),
                            color=colors["danger"], ls="--", linewidth=1, label="P5")
            axes[0].axvline(pct_vals.get("P95", np.percentile(results, 95)),
                            color=colors["danger"], ls="--", linewidth=1, label="P95")
            axes[0].set_title("Output Distribution")
            axes[0].set_xlabel("Output Value")
            axes[0].legend(fontsize=8)

            # CDF
            sorted_r = np.sort(results)
            cdf = np.arange(1, n_trials + 1) / n_trials
            axes[1].plot(sorted_r, cdf * 100, color=colors["secondary"], linewidth=2)
            axes[1].axhline(50, ls="--", color="gray", linewidth=0.8, label="P50")
            axes[1].axhline(90, ls="--", color=colors["accent"], linewidth=0.8, label="P90")
            axes[1].set_title("Cumulative Distribution (S-Curve)")
            axes[1].set_xlabel("Output Value")
            axes[1].set_ylabel("Cumulative Probability %")
            axes[1].legend(fontsize=8)
            axes[1].grid(alpha=0.3)

            plt.tight_layout()
            plt.show()

        return output

    @staticmethod
    def npv(
        cash_flows_dist: List[Dict],
        discount_rate_dist: Dict,
        n_trials: int = 10_000,
        seed: int = 42,
        show_plot: bool = True,
        color_scheme: str = "academic",
    ) -> Dict:
        """
        Monte Carlo NPV (Net Present Value) simulation.

        Parameters
        ----------
        cash_flows_dist : list of dist_spec dicts (one per period, period 0 = initial investment)
        discount_rate_dist : dist_spec dict for discount rate (e.g. {"dist":"normal","mean":0.1,"std":0.02})
        n_trials : int

        Example
        -------
        simulate.npv(
            cash_flows_dist=[
                {"dist":"fixed", "value":-1000},       # Year 0 investment
                {"dist":"normal","mean":300,"std":50},  # Year 1
                {"dist":"normal","mean":350,"std":60},  # Year 2
                {"dist":"triangular","low":200,"mode":400,"high":600},  # Year 3
            ],
            discount_rate_dist={"dist":"normal","mean":0.10,"std":0.02},
        )
        """
        if seed is not None:
            np.random.seed(seed)
        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])

        rates = simulate._sample_dist(discount_rate_dist, n_trials)
        cf_samples = [simulate._sample_dist(cf, n_trials) for cf in cash_flows_dist]

        npv_vals = np.zeros(n_trials)
        for t, cfs in enumerate(cf_samples):
            npv_vals += cfs / (1 + rates) ** t

        mean_npv = np.mean(npv_vals)
        irr_approx = None  # IRR requires iterative solve per trial; skip for speed

        p_positive = np.mean(npv_vals > 0) * 100
        pcts = {f"P{p}": round(float(np.percentile(npv_vals, p)), 2) for p in [5,25,50,75,95]}

        tbl = Table(title="[bold]NPV Monte Carlo Simulation[/bold]", header_style="bold cyan")
        tbl.add_column("Metric", style="bold")
        tbl.add_column("Value", justify="right")
        rows_disp = [
            ("Trials", f"{n_trials:,}"),
            ("Mean NPV", f"{mean_npv:,.2f}"),
            ("Std Dev NPV", f"{np.std(npv_vals):,.2f}"),
            ("Min NPV", f"{npv_vals.min():,.2f}"),
            ("Max NPV", f"{npv_vals.max():,.2f}"),
            ("P(NPV>0)", f"{p_positive:.1f}%"),
            *[(k, f"{v:,.2f}") for k, v in pcts.items()],
        ]
        for label, val in rows_disp:
            tbl.add_row(label, val)
        console.print(tbl)
        recommendation = "✅ Invest" if p_positive >= 70 else "⚠️ Risky" if p_positive >= 50 else "❌ Do Not Invest"
        console.print(f"[bold]Recommendation: {recommendation} (P(NPV>0) = {p_positive:.1f}%)[/bold]")

        if show_plot:
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            fig.suptitle("NPV Simulation", fontsize=13, fontweight="bold")

            axes[0].hist(npv_vals, bins=60, density=True, alpha=0.6, color=colors["primary"])
            axes[0].axvline(0, color=colors["danger"], linewidth=2, label="Break-even")
            axes[0].axvline(mean_npv, color=colors["success"], linewidth=2, label=f"Mean={mean_npv:,.0f}")
            axes[0].set_title("NPV Distribution")
            axes[0].set_xlabel("NPV")
            axes[0].legend(fontsize=9)

            sorted_npv = np.sort(npv_vals)
            cdf = np.arange(1, n_trials+1) / n_trials * 100
            axes[1].plot(sorted_npv, cdf, color=colors["secondary"], linewidth=2)
            axes[1].axvline(0, color=colors["danger"], ls="--", linewidth=1.5, label="NPV=0")
            axes[1].set_title("NPV Cumulative Distribution")
            axes[1].set_xlabel("NPV")
            axes[1].set_ylabel("Cumulative %")
            axes[1].legend(fontsize=9)
            axes[1].grid(alpha=0.3)

            plt.tight_layout()
            plt.show()

        return {"mean_npv": round(mean_npv, 2), "P(NPV>0)%": round(p_positive, 2),
                **pcts, "_results": npv_vals}

    @staticmethod
    def bootstrap(
        data,
        column: str,
        statistic=np.mean,
        n_trials: int = 10_000,
        confidence: float = 0.95,
        seed: int = 42,
        show_plot: bool = True,
        color_scheme: str = "academic",
    ) -> Dict:
        """
        Bootstrap confidence interval for any statistic.

        Parameters
        ----------
        data : DataFrame or array-like
        column : str (if DataFrame)
        statistic : callable — e.g. np.mean, np.median, np.std, custom fn
        n_trials : int
        confidence : float — e.g. 0.95 for 95% CI

        Returns
        -------
        dict with observed, bootstrap_mean, ci_lower, ci_upper, bias
        """
        if seed is not None:
            np.random.seed(seed)
        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])

        if hasattr(data, "columns"):
            frame = nw.from_native(data)
            pdf = frame.to_native() if hasattr(frame, "to_native") else pd.DataFrame(data)
            if not isinstance(pdf, pd.DataFrame):
                pdf = pd.DataFrame(pdf)
            arr = pdf[column].dropna().values.astype(float)
        else:
            arr = np.array(data, dtype=float)

        observed = statistic(arr)
        boot_stats = np.array([statistic(np.random.choice(arr, size=len(arr), replace=True))
                               for _ in range(n_trials)])

        alpha = (1 - confidence) / 2
        ci_lower = np.percentile(boot_stats, alpha * 100)
        ci_upper = np.percentile(boot_stats, (1 - alpha) * 100)
        bias = np.mean(boot_stats) - observed
        se = np.std(boot_stats, ddof=1)

        result = {
            "observed": round(float(observed), 6),
            "bootstrap_mean": round(float(np.mean(boot_stats)), 6),
            "bias": round(float(bias), 6),
            "std_error": round(float(se), 6),
            f"CI_{int(confidence*100)}%_lower": round(float(ci_lower), 6),
            f"CI_{int(confidence*100)}%_upper": round(float(ci_upper), 6),
            "n_trials": n_trials,
        }

        tbl = Table(title=f"[bold]Bootstrap ({n_trials:,} trials, {int(confidence*100)}% CI)[/bold]",
                    header_style="bold cyan")
        tbl.add_column("Metric", style="bold")
        tbl.add_column("Value", justify="right")
        for k, v in result.items():
            tbl.add_row(k, str(v))
        console.print(tbl)

        if show_plot:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.hist(boot_stats, bins=60, density=True, alpha=0.6, color=colors["primary"])
            ax.axvline(observed, color=colors["secondary"], linewidth=2, label=f"Observed={observed:.4f}")
            ax.axvline(ci_lower, color=colors["danger"], ls="--", linewidth=1.5,
                       label=f"{int(confidence*100)}% CI lower={ci_lower:.4f}")
            ax.axvline(ci_upper, color=colors["danger"], ls="--", linewidth=1.5,
                       label=f"upper={ci_upper:.4f}")
            ax.set_title(f"Bootstrap Distribution of {statistic.__name__ if hasattr(statistic,'__name__') else 'Statistic'}",
                         fontsize=12, fontweight="bold")
            ax.legend(fontsize=8)
            ax.set_xlabel("Statistic Value")
            plt.tight_layout()
            plt.show()

        return result

    @staticmethod
    def risk_matrix(
        risks: List[Dict],
        n_trials: int = 10_000,
        seed: int = 42,
        show_plot: bool = True,
        color_scheme: str = "academic",
    ) -> pd.DataFrame:
        """
        Simulate a risk register: probability × impact Monte Carlo.

        Parameters
        ----------
        risks : list of dicts with:
            - 'name'        : str
            - 'probability' : dist_spec or float 0-1
            - 'impact'      : dist_spec or float (monetary or score)

        Example
        -------
        simulate.risk_matrix([
            {"name":"Supply disruption","probability":0.3,"impact":{"dist":"triangular","low":50,"mode":150,"high":400}},
            {"name":"Regulatory fine",  "probability":0.1,"impact":{"dist":"uniform","low":200,"high":1000}},
        ])
        """
        if seed is not None:
            np.random.seed(seed)
        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])

        rows = []
        total_exposure = np.zeros(n_trials)

        for risk in risks:
            name = risk["name"]
            prob_spec = risk["probability"]
            impact_spec = risk["impact"]

            # Probability: fixed float or distribution
            if isinstance(prob_spec, (int, float)):
                probs = np.full(n_trials, float(prob_spec))
            else:
                probs = np.clip(simulate._sample_dist(prob_spec, n_trials), 0, 1)

            # Impact
            if isinstance(impact_spec, (int, float)):
                impacts = np.full(n_trials, float(impact_spec))
            else:
                impacts = simulate._sample_dist(impact_spec, n_trials)

            # Occurrence: Bernoulli draw
            occurred = (np.random.uniform(0, 1, n_trials) < probs)
            exposure = occurred * impacts
            total_exposure += exposure

            mean_exp = np.mean(exposure)
            p90 = np.percentile(exposure, 90)
            rows.append({
                "Risk": name,
                "Prob (mean)": round(float(probs.mean()), 3),
                "Impact (mean)": round(float(impacts.mean()), 2),
                "Expected Exposure": round(mean_exp, 2),
                "P90 Exposure": round(p90, 2),
                "Occurrence %": round(occurred.mean() * 100, 1),
            })

        result = pd.DataFrame(rows).sort_values("Expected Exposure", ascending=False)

        tbl = Table(title="[bold]Risk Simulation Results[/bold]", header_style="bold cyan")
        for col in result.columns:
            tbl.add_column(col, justify="right" if col != "Risk" else "left")
        for _, row in result.iterrows():
            tbl.add_row(*[str(v) for v in row])
        console.print(tbl)
        console.print(f"[bold]Total Portfolio Exposure — Mean: {np.mean(total_exposure):,.2f} | "
                      f"P90: {np.percentile(total_exposure, 90):,.2f}[/bold]")

        if show_plot:
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            fig.suptitle(f"Risk Portfolio Simulation (n={n_trials:,})", fontsize=13, fontweight="bold")

            axes[0].hist(total_exposure, bins=60, density=True, alpha=0.6, color=colors["danger"])
            axes[0].axvline(np.mean(total_exposure), color=colors["secondary"],
                            linewidth=2, label=f"Mean={np.mean(total_exposure):,.0f}")
            axes[0].axvline(np.percentile(total_exposure, 90), color=colors["primary"],
                            ls="--", linewidth=1.5, label=f"P90={np.percentile(total_exposure, 90):,.0f}")
            axes[0].set_title("Total Portfolio Exposure Distribution")
            axes[0].set_xlabel("Exposure")
            axes[0].legend(fontsize=8)

            # Tornado chart: rank risks by expected exposure
            axes[1].barh(result["Risk"][::-1], result["Expected Exposure"][::-1],
                         color=colors["danger"], edgecolor="white", linewidth=0.3)
            axes[1].set_title("Tornado Chart: Expected Exposure by Risk")
            axes[1].set_xlabel("Expected Exposure")

            plt.tight_layout()
            plt.show()

        return result


# ─────────────────────────────────────────────────────────────────────────────
# PRESCRIPTIVE ANALYTICS
# ─────────────────────────────────────────────────────────────────────────────

class prescriptive:
    """
    Prescriptive Analytics — Operations Research & Optimization.

    Builds on optimize.linear_program() with advanced methods:

    Methods
    -------
    lp(...)                   — Linear Programming (PuLP wrapper with richer output)
    integer_lp(...)           — Integer / Mixed-Integer Linear Programming (MILP)
    transportation(...)       — Transportation problem (supply/demand)
    assignment(...)           — Assignment problem (Hungarian method)
    goal_programming(...)     — Multi-objective goal programming
    sensitivity(...)          — Sensitivity / what-if analysis on LP
    recommend(...)            — Decision recommendation engine
    packages()                — Show OR ecosystem packages
    """

    @staticmethod
    def lp(
        objective: List[float],
        constraints: List[List[float]],
        rhs: List[float],
        variable_names: Optional[List[str]] = None,
        constraint_types: Optional[List[str]] = None,
        maximize: bool = True,
        bounds: Optional[List[Tuple]] = None,
        show_plot: bool = True,
        color_scheme: str = "academic",
    ) -> Dict:
        """
        Solve a Linear Program with rich output and sensitivity analysis.

        Parameters
        ----------
        objective   : list of objective coefficients [c1, c2, ...]
        constraints : list of constraint rows [[a11, a12,...], [a21, a22,...], ...]
        rhs         : list of right-hand-side values [b1, b2, ...]
        variable_names: list of variable names or None
        constraint_types: list of '<=', '>=', or '==' (default all '<=')
        maximize    : bool (True=maximize, False=minimize)
        bounds      : list of (lower, upper) per variable; default (0, None)

        Returns
        -------
        dict: status, objective_value, variables, shadow_prices (if available)
        """
        try:
            import pulp
        except ImportError:
            console.print("[red]PuLP not installed. Run: pip install PuLP[/red]")
            return {}

        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])
        names = variable_names or [f"x{i+1}" for i in range(len(objective))]
        c_types = constraint_types or ["<="] * len(constraints)
        var_bounds = bounds or [(0, None)] * len(objective)

        sense = pulp.LpMaximize if maximize else pulp.LpMinimize
        prob = pulp.LpProblem("BizLens_LP", sense)

        vars_ = [pulp.LpVariable(n, lowBound=lb, upBound=ub)
                 for n, (lb, ub) in zip(names, var_bounds)]

        prob += pulp.lpSum(obj * v for obj, v in zip(objective, vars_))

        for i, (row, rhs_val, ct) in enumerate(zip(constraints, rhs, c_types)):
            expr = pulp.lpSum(coef * v for coef, v in zip(row, vars_))
            if ct == "<=":
                prob += expr <= rhs_val, f"c{i+1}"
            elif ct == ">=":
                prob += expr >= rhs_val, f"c{i+1}"
            else:
                prob += expr == rhs_val, f"c{i+1}"

        prob.solve(pulp.PULP_CBC_CMD(msg=0))

        result = {
            "status": pulp.LpStatus[prob.status],
            "objective_value": round(float(pulp.value(prob.objective)), 4),
            "maximize": maximize,
            "variables": {n: round(float(pulp.value(v)), 4) for n, v in zip(names, vars_)},
            "shadow_prices": {f"c{i+1}": round(float(c.pi or 0), 4)
                              for i, c in enumerate(prob.constraints.values())},
        }

        tbl = Table(title="[bold]Linear Program Solution[/bold]", header_style="bold cyan")
        tbl.add_column("Item", style="bold")
        tbl.add_column("Value", justify="right")
        tbl.add_row("Status", result["status"])
        tbl.add_row("Objective (" + ("Max" if maximize else "Min") + ")",
                    f"{result['objective_value']:,.4f}")
        for n, v in result["variables"].items():
            tbl.add_row(f"  {n}", f"{v:,.4f}")
        console.print(tbl)

        # Shadow prices
        if any(v != 0 for v in result["shadow_prices"].values()):
            sp_tbl = Table(title="[bold]Shadow Prices (Dual Values)[/bold]", header_style="bold cyan")
            sp_tbl.add_column("Constraint", style="bold")
            sp_tbl.add_column("Shadow Price", justify="right")
            sp_tbl.add_column("Interpretation")
            for c, val in result["shadow_prices"].items():
                interp = f"Objective improves by {abs(val):.4f} per unit relaxation of RHS"
                sp_tbl.add_row(c, str(val), interp if val != 0 else "Non-binding")
            console.print(sp_tbl)

        if show_plot and len(names) == 2:
            # 2-variable feasible region plot
            try:
                colors_s = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])
                x_max = max(v for v in result["variables"].values()) * 2 + 10
                x = np.linspace(0, x_max, 400)
                fig, ax = plt.subplots(figsize=(9, 7))

                for i, (row, rhs_val, ct) in enumerate(zip(constraints, rhs, c_types)):
                    if row[1] != 0:
                        y = (rhs_val - row[0] * x) / row[1]
                        ax.plot(x, y, label=f"Constraint {i+1}", linewidth=1.5)

                opt_x = result["variables"][names[0]]
                opt_y = result["variables"][names[1]]
                ax.scatter(opt_x, opt_y, color=colors_s["danger"], s=200, zorder=5,
                           label=f"Optimal ({opt_x:.2f}, {opt_y:.2f})")
                ax.set_xlim(0, x_max)
                ax.set_ylim(0, x_max)
                ax.set_xlabel(names[0])
                ax.set_ylabel(names[1])
                ax.set_title("Feasible Region (2-variable LP)", fontsize=12, fontweight="bold")
                ax.legend(fontsize=9)
                ax.grid(alpha=0.3)
                plt.tight_layout()
                plt.show()
            except Exception:
                pass

        return result

    @staticmethod
    def integer_lp(
        objective: List[float],
        constraints: List[List[float]],
        rhs: List[float],
        integer_vars: Optional[List[str]] = None,
        binary_vars: Optional[List[str]] = None,
        variable_names: Optional[List[str]] = None,
        constraint_types: Optional[List[str]] = None,
        maximize: bool = True,
    ) -> Dict:
        """
        Mixed-Integer Linear Program (MILP).

        Parameters
        ----------
        integer_vars : list of variable names to constrain as integers
        binary_vars  : list of variable names to constrain as 0/1 binary

        Example (Knapsack)
        ------------------
        prescriptive.integer_lp(
            objective=[60, 100, 120],
            constraints=[[10, 20, 30]],
            rhs=[50],
            binary_vars=["x1","x2","x3"],
            variable_names=["x1","x2","x3"],
            maximize=True,
        )
        """
        try:
            import pulp
        except ImportError:
            console.print("[red]PuLP not installed. Run: pip install PuLP[/red]")
            return {}

        names = variable_names or [f"x{i+1}" for i in range(len(objective))]
        c_types = constraint_types or ["<="] * len(constraints)
        int_set = set(integer_vars or [])
        bin_set = set(binary_vars or [])

        sense = pulp.LpMaximize if maximize else pulp.LpMinimize
        prob = pulp.LpProblem("BizLens_MILP", sense)

        vars_ = []
        for n in names:
            if n in bin_set:
                vars_.append(pulp.LpVariable(n, cat="Binary"))
            elif n in int_set:
                vars_.append(pulp.LpVariable(n, lowBound=0, cat="Integer"))
            else:
                vars_.append(pulp.LpVariable(n, lowBound=0, cat="Continuous"))

        prob += pulp.lpSum(obj * v for obj, v in zip(objective, vars_))

        for i, (row, rhs_val, ct) in enumerate(zip(constraints, rhs, c_types)):
            expr = pulp.lpSum(coef * v for coef, v in zip(row, vars_))
            if ct == "<=":
                prob += expr <= rhs_val, f"c{i+1}"
            elif ct == ">=":
                prob += expr >= rhs_val, f"c{i+1}"
            else:
                prob += expr == rhs_val, f"c{i+1}"

        prob.solve(pulp.PULP_CBC_CMD(msg=0))

        result = {
            "status": pulp.LpStatus[prob.status],
            "objective_value": round(float(pulp.value(prob.objective)), 4),
            "variables": {n: round(float(pulp.value(v)), 4) for n, v in zip(names, vars_)},
        }

        tbl = Table(title="[bold]MILP Solution[/bold]", header_style="bold cyan")
        tbl.add_column("Variable", style="bold")
        tbl.add_column("Value", justify="right")
        tbl.add_column("Type")
        for n, v_val in result["variables"].items():
            vtype = "Binary" if n in bin_set else "Integer" if n in int_set else "Continuous"
            tbl.add_row(n, str(v_val), vtype)
        console.print(tbl)
        console.print(f"[bold]Status: {result['status']} | Objective: {result['objective_value']:,.4f}[/bold]")

        return result

    @staticmethod
    def transportation(
        supply: List[float],
        demand: List[float],
        costs: List[List[float]],
        supply_names: Optional[List[str]] = None,
        demand_names: Optional[List[str]] = None,
    ) -> Dict:
        """
        Solve a Transportation Problem (minimize total shipping cost).

        Parameters
        ----------
        supply       : list of supply quantities at each origin
        demand       : list of demand quantities at each destination
        costs        : 2D list [origin][destination] of unit shipping costs

        Returns
        -------
        dict with optimal allocation, total cost
        """
        try:
            import pulp
        except ImportError:
            console.print("[red]PuLP not installed. Run: pip install PuLP[/red]")
            return {}

        m, n = len(supply), len(demand)
        src = supply_names or [f"S{i+1}" for i in range(m)]
        dst = demand_names or [f"D{j+1}" for j in range(n)]

        # Balance: add dummy if needed
        total_supply = sum(supply)
        total_demand = sum(demand)
        supply_ = list(supply)
        demand_ = list(demand)
        costs_  = [list(row) for row in costs]
        src_ = list(src); dst_ = list(dst)

        if total_supply > total_demand:
            demand_.append(total_supply - total_demand)
            dst_.append("Dummy")
            for row in costs_:
                row.append(0)
        elif total_demand > total_supply:
            supply_.append(total_demand - total_supply)
            src_.append("Dummy")
            costs_.append([0] * len(demand_))

        m_, n_ = len(supply_), len(demand_)
        prob = pulp.LpProblem("Transportation", pulp.LpMinimize)
        x = [[pulp.LpVariable(f"x_{i}_{j}", lowBound=0)
              for j in range(n_)] for i in range(m_)]

        prob += pulp.lpSum(costs_[i][j] * x[i][j] for i in range(m_) for j in range(n_))

        for i in range(m_):
            prob += pulp.lpSum(x[i][j] for j in range(n_)) <= supply_[i], f"supply_{i}"
        for j in range(n_):
            prob += pulp.lpSum(x[i][j] for i in range(m_)) >= demand_[j], f"demand_{j}"

        prob.solve(pulp.PULP_CBC_CMD(msg=0))

        allocation = pd.DataFrame(
            [[round(float(pulp.value(x[i][j])), 2) for j in range(n_)] for i in range(m_)],
            index=src_, columns=dst_
        )
        total_cost = round(float(pulp.value(prob.objective)), 4)

        tbl = Table(title="[bold]Transportation — Optimal Allocation[/bold]", header_style="bold cyan")
        tbl.add_column("Origin \\ Dest", style="bold")
        for d in dst_:
            tbl.add_column(d, justify="right")
        tbl.add_column("Supply", justify="right", style="dim")
        for i, s in enumerate(src_):
            row_vals = [str(allocation.iloc[i, j]) for j in range(n_)]
            tbl.add_row(s, *row_vals, str(supply_[i]))
        tbl.add_row("Demand", *[str(d) for d in demand_], "")
        console.print(tbl)
        console.print(f"[bold green]✅ Total Minimum Cost: {total_cost:,.4f}[/bold green]")

        return {"status": pulp.LpStatus[prob.status], "total_cost": total_cost, "allocation": allocation}

    @staticmethod
    def assignment(
        cost_matrix: List[List[float]],
        agent_names: Optional[List[str]] = None,
        task_names: Optional[List[str]] = None,
        maximize: bool = False,
    ) -> Dict:
        """
        Solve an Assignment Problem using the Hungarian algorithm (scipy).

        Parameters
        ----------
        cost_matrix : 2D list [agents][tasks] — can be cost or profit matrix
        maximize    : bool — if True, convert to maximization

        Returns
        -------
        dict with assignments, total cost/profit
        """
        from scipy.optimize import linear_sum_assignment

        C = np.array(cost_matrix, dtype=float)
        if maximize:
            C_solve = -C
        else:
            C_solve = C

        row_idx, col_idx = linear_sum_assignment(C_solve)
        total = C[row_idx, col_idx].sum()

        agents = agent_names or [f"Agent {i+1}" for i in range(len(cost_matrix))]
        tasks  = task_names  or [f"Task {j+1}" for j in range(len(cost_matrix[0]))]

        tbl = Table(title="[bold]Assignment Problem — Optimal Assignments[/bold]", header_style="bold cyan")
        tbl.add_column("Agent", style="bold")
        tbl.add_column("Assigned Task")
        tbl.add_column("Cost/Profit", justify="right")
        for r, c in zip(row_idx, col_idx):
            tbl.add_row(agents[r], tasks[c], f"{C[r, c]:.4f}")
        console.print(tbl)
        console.print(f"[bold green]Total {'Profit' if maximize else 'Cost'}: {total:.4f}[/bold green]")

        return {
            "assignments": {agents[r]: tasks[c] for r, c in zip(row_idx, col_idx)},
            "total": round(float(total), 4),
            "maximize": maximize,
        }

    @staticmethod
    def sensitivity(
        objective: List[float],
        constraints: List[List[float]],
        rhs: List[float],
        param: str = "rhs",
        param_idx: int = 0,
        delta_range: Optional[Tuple[float, float]] = None,
        n_points: int = 50,
        maximize: bool = True,
        variable_names: Optional[List[str]] = None,
        color_scheme: str = "academic",
    ) -> pd.DataFrame:
        """
        Sensitivity / what-if analysis: vary one parameter and see objective change.

        Parameters
        ----------
        param     : 'rhs' (vary a constraint RHS) or 'obj' (vary an objective coefficient)
        param_idx : index of the constraint/variable to vary
        delta_range : (min_value, max_value) to test; default ±50% of original
        """
        try:
            import pulp
        except ImportError:
            console.print("[red]PuLP not installed. Run: pip install PuLP[/red]")
            return pd.DataFrame()

        colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])
        names = variable_names or [f"x{i+1}" for i in range(len(objective))]

        if param == "rhs":
            original = rhs[param_idx]
            label = f"RHS constraint {param_idx+1}"
        else:
            original = objective[param_idx]
            label = f"Objective coefficient {names[param_idx]}"

        if delta_range is None:
            lo = original * 0.5 if original != 0 else -10
            hi = original * 1.5 if original != 0 else 10
            delta_range = (lo, hi)

        test_vals = np.linspace(delta_range[0], delta_range[1], n_points)
        rows = []
        for val in test_vals:
            obj_   = list(objective)
            rhs_   = list(rhs)
            if param == "rhs":
                rhs_[param_idx] = val
            else:
                obj_[param_idx] = val

            sense  = pulp.LpMaximize if maximize else pulp.LpMinimize
            prob_  = pulp.LpProblem("Sensitivity", sense)
            vars_  = [pulp.LpVariable(n, lowBound=0) for n in names]
            prob_ += pulp.lpSum(o * v for o, v in zip(obj_, vars_))
            for i, (row, r, ct) in enumerate(zip(constraints, rhs_, ["<="]*len(rhs_))):
                prob_ += pulp.lpSum(c * v for c, v in zip(row, vars_)) <= r
            prob_.solve(pulp.PULP_CBC_CMD(msg=0))
            obj_val = float(pulp.value(prob_.objective)) if prob_.status == 1 else np.nan
            rows.append({"param_value": round(val, 4), "objective": round(obj_val, 4) if not np.isnan(obj_val) else np.nan})

        result = pd.DataFrame(rows)
        console.print(f"[bold]Sensitivity Analysis: {label}[/bold]")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(result["param_value"], result["objective"],
                color=colors["primary"], linewidth=2)
        ax.axvline(original, color=colors["danger"], ls="--", linewidth=1.5, label=f"Original={original}")
        ax.set_xlabel(label)
        ax.set_ylabel(f"Objective ({'Max' if maximize else 'Min'})")
        ax.set_title(f"Sensitivity: {label}", fontsize=12, fontweight="bold")
        ax.legend(fontsize=9)
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()

        return result

    @staticmethod
    def packages() -> None:
        """
        Show the full Operations Research package ecosystem.
        """
        tbl = Table(title="[bold]Operations Research & Optimization Packages[/bold]",
                    header_style="bold cyan")
        tbl.add_column("Package", style="bold")
        tbl.add_column("Purpose")
        tbl.add_column("Install")
        tbl.add_column("Free?")

        or_packages = [
            ("PuLP",       "LP/MILP modelling (CBC solver built-in)",           "pip install PuLP",     "✅ Yes"),
            ("SciPy",      "LP (linprog), NLP, assignment, root finding",        "pip install scipy",    "✅ Yes"),
            ("CVXPY",      "Convex optimization (LP, QP, SOCP, SDP)",            "pip install cvxpy",    "✅ Yes"),
            ("OR-Tools",   "Google's CP-SAT, routing, scheduling",              "pip install ortools",  "✅ Yes"),
            ("Pyomo",      "Algebraic modelling for LP/MILP/NLP/MIP",            "pip install pyomo",    "✅ Yes"),
            ("GEKKO",      "Dynamic optimization, ODE/DAE, NLP",                "pip install gekko",    "✅ Yes"),
            ("Optuna",     "Hyperparameter & black-box optimization",            "pip install optuna",   "✅ Yes"),
            ("Pymoo",      "Multi-objective evolutionary optimization (NSGA-II)","pip install pymoo",    "✅ Yes"),
            ("NetworkX",   "Graph algorithms, shortest path, network flow",      "pip install networkx", "✅ Yes"),
            ("SimPy",      "Discrete-event simulation (queues, manufacturing)",  "pip install simpy",    "✅ Yes"),
            ("mesa",       "Agent-based modelling & simulation",                 "pip install mesa",     "✅ Yes"),
            ("Gurobi",     "Commercial state-of-the-art MILP/NLP solver",        "pip install gurobipy", "💰 License"),
            ("CPLEX",      "IBM commercial MILP/QP solver",                      "pip install cplex",    "💰 License"),
            ("MOSEK",      "Large-scale SOCP/SDP solver",                        "pip install mosek",    "💰 License"),
        ]
        for row in or_packages:
            tbl.add_row(*row)
        console.print(tbl)

        console.print("\n[bold]💡 Analytics Pyramid:[/bold]")
        console.print("  📊 Descriptive  → What happened? (describe, tables)")
        console.print("  🔍 Diagnostic   → Why did it happen? (diagnostic, ttest, anova)")
        console.print("  🔮 Predictive   → What will happen? (predict, simulate)")
        console.print("  🎯 Prescriptive → What should we do? (prescriptive, optimize)")
