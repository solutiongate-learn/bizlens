"""
BizLens v0.6.0 — Educational Analytics Platform
Descriptive Statistics + Interactive Visualizations

Key Functions:
- describe() → Summary statistics + visuals
- load_dataset() → Educational datasets
- analyze() → Interactive exploration
"""

import numpy as np
import pandas as pd
import polars as pl
import narwhals as nw
from narwhals.typing import IntoFrame
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
import warnings

warnings.filterwarnings("ignore")

# ============================================================================
# FORMULAS USED (Transparent Calculations)
# ============================================================================

"""
DESCRIPTIVE STATISTICS FORMULAS:

1. MEAN (Average)
   μ = (Σ x) / n
   where Σ x = sum of all values, n = count

2. MEDIAN (Middle Value)
   - Sort data
   - If odd count: middle value
   - If even count: average of two middle values

3. MODE (Most Frequent)
   Value that appears most often in dataset

4. STANDARD DEVIATION (Spread)
   σ = √(Σ(x - μ)² / (n-1))
   Measures how far values deviate from mean

5. QUARTILES (Q1, Q2, Q3)
   Q1 = 25th percentile (25% below)
   Q2 = 50th percentile (median)
   Q3 = 75th percentile (75% below)

6. IQR (Interquartile Range)
   IQR = Q3 - Q1
   Middle 50% of data spread

7. SKEWNESS
   γ = (3(μ - median)) / σ
   Measures asymmetry of distribution
   Positive = right-skewed
   Negative = left-skewed
   Zero = symmetric (normal)

8. KURTOSIS
   κ = (Σ(x - μ)⁴ / n) / σ⁴
   Measures tail heaviness
   High = fat tails, outlier-prone
   Low = thin tails, normal-like

9. CORRELATION (Pearson)
   r = Σ((x - μₓ)(y - μᵧ)) / √(Σ(x - μₓ)² × Σ(y - μᵧ)²)
   Range: -1 to +1
   Measures linear relationship

10. OUTLIERS (IQR Method)
    Lower bound = Q1 - 1.5 × IQR
    Upper bound = Q3 + 1.5 × IQR
    Values outside bounds = outliers
"""

# ============================================================================
# CORE ANALYTICS ENGINE
# ============================================================================

class BizDesc:
    """
    Educational Analytics Engine

    Usage:
        bd = BizDesc(data)
        bd.describe(plots=True)
        bd.visualize(column='column_name')
        bd.correlations()
    """

    def __init__(self, data: Union[IntoFrame, str, Path]):
        """Initialize with DataFrame or file path."""
        if isinstance(data, (str, Path)):
            path = Path(data)
            if path.suffix == ".csv":
                self.df = nw.from_native(pl.read_csv(path), eager_only=True)
            elif path.suffix in [".xlsx", ".xls"]:
                self.df = nw.from_native(pd.read_excel(path), eager_only=True)
            else:
                self.df = nw.from_native(pl.read_parquet(path), eager_only=True)
        else:
            self.df = nw.from_native(data, eager_only=True)

        self.numeric_cols = self.df.select(nw.col(nw.NUMERIC_DTYPES)).columns
        self.cat_cols = self.df.select(nw.col(nw.CATEGORICAL_DTYPES)).columns

    def describe(self, include_plots: bool = True, bins: int = 30,
                 figsize: tuple = (14, 5)) -> Dict[str, Any]:
        """
        Generate descriptive statistics with optional visualizations.

        FORMULAS USED:
        - Mean: Σx / n
        - Median: 50th percentile
        - Std Dev: √(Σ(x-μ)² / n-1)
        - Skewness: (3(μ - median)) / σ

        Args:
            include_plots: Show matplotlib visualizations
            bins: Number of histogram bins
            figsize: Figure size (width, height)

        Returns:
            Dictionary with statistics
        """
        stats_list = []

        for col in self.numeric_cols:
            col_data = np.array(self.df[col].to_numpy())
            col_data = col_data[~np.isnan(col_data)]

            if len(col_data) == 0:
                continue

            # FORMULAS: Calculate statistics
            mean_val = float(np.mean(col_data))
            median_val = float(np.median(col_data))
            std_val = float(np.std(col_data, ddof=1))
            q1, q3 = float(np.percentile(col_data, 25)), float(np.percentile(col_data, 75))
            iqr_val = q3 - q1
            skew_val = float(stats.skew(col_data))  # Formula: (3(μ - median)) / σ
            min_val, max_val = float(np.min(col_data)), float(np.max(col_data))

            # Mode
            mode_result = stats.mode(col_data, keepdims=True)
            mode_val = float(mode_result[0][0]) if len(mode_result[0]) > 0 else np.nan

            stats_list.append({
                "Column": col,
                "Count": len(col_data),
                "Mean": round(mean_val, 2),
                "Median": round(median_val, 2),
                "Mode": round(mode_val, 2) if not np.isnan(mode_val) else "N/A",
                "Std Dev": round(std_val, 2),
                "Min": round(min_val, 2),
                "Max": round(max_val, 2),
                "Q1 (25%)": round(q1, 2),
                "Q3 (75%)": round(q3, 2),
                "IQR": round(iqr_val, 2),
                "Skewness": round(skew_val, 2),
            })

        result = {
            "shape": (self.df.shape[0], self.df.shape[1]),
            "numeric_stats": stats_list,
            "numeric_columns": self.numeric_cols,
            "categorical_columns": self.cat_cols,
        }

        print(f"\n{'='*80}")
        print(f"📊 BizLens v0.6.0 Descriptive Analytics")
        print(f"{'='*80}")
        print(f"Dataset Shape: {result['shape'][0]} rows × {result['shape'][1]} columns")
        print(f"Numeric Columns: {len(self.numeric_cols)}")
        print(f"Categorical Columns: {len(self.cat_cols)}")

        # Print statistics table
        if stats_list:
            df_stats = pd.DataFrame(stats_list)
            print(f"\n{df_stats.to_string(index=False)}")

        if include_plots and self.numeric_cols:
            self._plot_distributions(bins, figsize)

        return result

    def _plot_distributions(self, bins: int = 30, figsize: tuple = (14, 5)):
        """Plot histograms for numeric columns."""
        numeric_data = self.df.select(self.numeric_cols[:4])  # Limit to 4 plots
        native_df = numeric_data.to_native()

        if isinstance(native_df, pl.DataFrame):
            native_df = native_df.to_pandas()

        n_cols = min(len(self.numeric_cols), 4)
        fig, axes = plt.subplots(1, n_cols, figsize=(4*n_cols, 4))

        if n_cols == 1:
            axes = [axes]

        for idx, col in enumerate(self.numeric_cols[:4]):
            data = native_df[col].dropna()

            # FORMULA: Create histogram with KDE
            axes[idx].hist(data, bins=bins, alpha=0.7, color='skyblue', edgecolor='black')

            # Add mean line
            mean_val = data.mean()
            axes[idx].axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.1f}')
            axes[idx].axvline(data.median(), color='green', linestyle='-', linewidth=2, label=f'Median: {data.median():.1f}')

            axes[idx].set_title(f"Distribution: {col}", fontsize=12, fontweight='bold')
            axes[idx].set_xlabel("Value")
            axes[idx].set_ylabel("Frequency")
            axes[idx].legend()
            axes[idx].grid(alpha=0.3)

        plt.tight_layout()
        plt.show()

    def visualize(self, column: str, plot_type: str = "histogram", **kwargs):
        """
        Create custom visualizations.

        plot_type options:
        - "histogram" → Distribution with mean/median lines
        - "boxplot" → Show quartiles and outliers
        - "violin" → Distribution shape + density
        - "density" → Smooth distribution curve
        """
        native_df = self.df.to_native()
        if isinstance(native_df, pl.DataFrame):
            native_df = native_df.to_pandas()

        data = native_df[column].dropna()

        plt.figure(figsize=(10, 6))

        if plot_type == "histogram":
            bins = kwargs.get('bins', 30)
            plt.hist(data, bins=bins, alpha=0.7, color='skyblue', edgecolor='black')
            plt.axvline(data.mean(), color='red', linestyle='--', label=f'Mean: {data.mean():.2f}')
            plt.axvline(data.median(), color='green', linestyle='-', label=f'Median: {data.median():.2f}')

        elif plot_type == "boxplot":
            plt.boxplot(data, vert=True)
            plt.ylabel(column)

        elif plot_type == "violin":
            parts = plt.violinplot(data)
            plt.ylabel(column)

        elif plot_type == "density":
            data.plot(kind='density', figsize=(10, 6))

        plt.title(f"{column} - {plot_type.capitalize()}", fontsize=14, fontweight='bold')
        plt.grid(alpha=0.3)
        plt.legend()
        plt.show()

    def correlations(self, method: str = "pearson") -> pd.DataFrame:
        """
        Calculate correlations between numeric columns.

        FORMULA (Pearson):
        r = Σ((x - μₓ)(y - μᵧ)) / √(Σ(x - μₓ)² × Σ(y - μᵧ)²)

        Returns:
            Correlation matrix
        """
        native_df = self.df.to_native()
        if isinstance(native_df, pl.DataFrame):
            native_df = native_df.to_pandas()

        numeric_df = native_df[self.numeric_cols]
        corr_matrix = numeric_df.corr(method=method)

        # Visualize
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                    fmt='.2f', square=True, cbar_kws={'label': 'Correlation'})
        plt.title(f"Correlation Matrix ({method})", fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()

        return corr_matrix

    def outliers(self, method: str = "iqr") -> Dict[str, Any]:
        """
        Detect outliers using IQR method.

        FORMULA:
        Lower bound = Q1 - 1.5 × IQR
        Upper bound = Q3 + 1.5 × IQR

        Values outside bounds = outliers
        """
        results = {}

        for col in self.numeric_cols:
            col_data = np.array(self.df[col].to_numpy())
            col_data = col_data[~np.isnan(col_data)]

            Q1 = np.percentile(col_data, 25)
            Q3 = np.percentile(col_data, 75)
            IQR = Q3 - Q1

            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR

            outlier_mask = (col_data < lower) | (col_data > upper)
            outlier_count = int(outlier_mask.sum())
            outlier_pct = 100 * outlier_count / len(col_data)

            results[col] = {
                "count": outlier_count,
                "percentage": round(outlier_pct, 2),
                "bounds": {"lower": round(lower, 2), "upper": round(upper, 2)}
            }

        print("\n" + "="*60)
        print("🔍 OUTLIER DETECTION (IQR Method)")
        print("="*60)
        for col, info in results.items():
            print(f"\n{col}:")
            print(f"  Outliers: {info['count']} ({info['percentage']}%)")
            print(f"  Valid range: [{info['bounds']['lower']:.2f}, {info['bounds']['upper']:.2f}]")

        return results

    def normality_test(self) -> Dict[str, Any]:
        """
        Shapiro-Wilk test for normality.

        FORMULA:
        H0: Data is normally distributed
        If p-value > 0.05: Likely normal
        If p-value < 0.05: Likely NOT normal
        """
        results = {}

        for col in self.numeric_cols:
            col_data = np.array(self.df[col].to_numpy())
            col_data = col_data[~np.isnan(col_data)]

            if len(col_data) < 3:
                continue

            stat, p_value = stats.shapiro(col_data)
            is_normal = p_value > 0.05

            results[col] = {
                "statistic": round(float(stat), 4),
                "p_value": round(float(p_value), 6),
                "is_normal": is_normal,
                "interpretation": "Normal ✓" if is_normal else "Not Normal ✗"
            }

        print("\n" + "="*60)
        print("📈 NORMALITY TEST (Shapiro-Wilk)")
        print("="*60)
        for col, info in results.items():
            print(f"\n{col}:")
            print(f"  p-value: {info['p_value']}")
            print(f"  Conclusion: {info['interpretation']}")

        return results


# ============================================================================
# EDUCATIONAL DATASETS
# ============================================================================

def load_dataset(name: str, n_rows: int = None) -> pl.DataFrame:
    """Load educational dataset."""

    if name == "school_cafeteria":
        return generate_school_cafeteria(n_rows or 200)
    elif name == "test_scores":
        return generate_test_scores(n_rows or 100)
    else:
        raise ValueError(f"Unknown dataset: {name}")


def generate_school_cafeteria(n: int = 200, seed: int = 42) -> pl.DataFrame:
    """
    School cafeteria spending data.

    Concepts:
    - Skewed distribution (spending)
    - Categorical relationships (lunch type → satisfaction)
    - Realistic distributions
    """
    np.random.seed(seed)

    return pl.DataFrame({
        "student_id": np.arange(1, n + 1),
        "age": np.random.choice([14, 15, 16, 17, 18], n, p=[0.2, 0.25, 0.25, 0.2, 0.1]),
        "lunch_type": np.random.choice(["hot_meal", "packed_lunch", "salad", "pizza"], n, p=[0.35, 0.25, 0.2, 0.2]),
        "spending": np.minimum(np.random.exponential(4.5, n), 25).round(2),  # Skewed
        "satisfaction": np.clip(np.random.normal(6.5, 1.5, n), 1, 10).round(1),
    })


def generate_test_scores(n: int = 100, seed: int = 42) -> pl.DataFrame:
    """
    Student test scores across subjects.

    Concepts:
    - Different distributions (normal, bimodal)
    - Group comparison
    - Outlier detection
    """
    np.random.seed(seed)

    ability = np.random.normal(70, 15, n)

    data = []
    for i in range(n):
        data.append({"student_id": i+1, "subject": "Math", "score": np.clip(ability[i] + np.random.normal(0, 8), 0, 100).round(1)})
        data.append({"student_id": i+1, "subject": "English", "score": np.clip(np.random.choice([np.random.normal(65, 10), np.random.normal(85, 8)]), 0, 100).round(1)})
        data.append({"student_id": i+1, "subject": "Science", "score": np.clip(ability[i] + np.random.normal(0, 10), 0, 100).round(1)})

    return pl.DataFrame(data)


# ============================================================================
# QUICK API
# ============================================================================

def describe(data, plots=True, **kwargs) -> Dict:
    """Quick one-liner for analysis."""
    bd = BizDesc(data)
    return bd.describe(include_plots=plots, **kwargs)
