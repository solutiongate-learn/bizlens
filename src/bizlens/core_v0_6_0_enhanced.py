"""
BizLens v0.6.0 ENHANCED — Educational Analytics Platform
Descriptive Statistics + Advanced Visualizations with Central Tendency

Key Enhancements:
- Central Tendency Statistics (Mean, Median, Mode with detailed analysis)
- 9 Visualization Types (histogram, boxplot, violin, bar, line, pie, density, scatter, heatmap)
- Professional Color Schemes & Labels
- Dynamic Formatting
"""

import numpy as np
import pandas as pd
import polars as pl
import narwhals as nw
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
import warnings
import sys

# Type alias for dataframe input
IntoFrame = Union[pd.DataFrame, pl.DataFrame, dict, list]

warnings.filterwarnings("ignore")

# ============================================================================
# COLOR SCHEMES FOR PROFESSIONAL VISUALIZATIONS
# ============================================================================

COLOR_SCHEMES = {
    "academic": {
        "primary": "#2E86AB",      # Deep blue
        "secondary": "#A23B72",     # Purple
        "accent": "#F18F01",        # Orange
        "success": "#06A77D",       # Green
        "danger": "#D62828",        # Red
        "palette": ["#2E86AB", "#A23B72", "#F18F01", "#06A77D", "#D62828"]
    },
    "pastel": {
        "primary": "#8ECAE6",       # Light blue
        "secondary": "#FFB4A2",     # Light pink
        "accent": "#E5989B",        # Mauve
        "success": "#90E0EF",       # Cyan
        "danger": "#F77F88",        # Light red
        "palette": ["#8ECAE6", "#FFB4A2", "#E5989B", "#90E0EF", "#F77F88"]
    },
    "vibrant": {
        "primary": "#FF6B6B",       # Red
        "secondary": "#4ECDC4",     # Teal
        "accent": "#FFE66D",        # Yellow
        "success": "#95E1D3",       # Mint
        "danger": "#C9184A",        # Dark red
        "palette": ["#FF6B6B", "#4ECDC4", "#FFE66D", "#95E1D3", "#C9184A"]
    }
}

# ============================================================================
# FORMULAS FOR CENTRAL TENDENCY (Enhanced)
# ============================================================================

"""
CENTRAL TENDENCY STATISTICS:

1. MEAN (Arithmetic Average)
   μ = (Σ x) / n
   What: Average of all values
   When: Use when distribution is symmetric
   Sensitive to: Outliers (can be misleading if skewed)

2. MEDIAN (Middle Value)
   - Sort all values
   - If n is odd: middle value
   - If n is even: average of two middle values
   What: Middle value when sorted
   When: Use when distribution is skewed or has outliers
   Robust: Not affected by extreme values

3. MODE (Most Frequent Value)
   Value that appears most often
   What: Most common value
   When: Use for categorical or discrete data
   Insight: Shows peaks in distribution

4. RANGE
   Range = Max - Min
   What: Spread from lowest to highest
   Limitation: Very sensitive to outliers

5. QUARTILES (Q1, Q2, Q3)
   Q1 = 25th percentile (25% below)
   Q2 = 50th percentile (median)
   Q3 = 75th percentile (75% below)
   What: Divides data into 4 equal parts
   Use: Understand distribution spread

6. INTERQUARTILE RANGE (IQR)
   IQR = Q3 - Q1
   What: Middle 50% of data spread
   Use: More robust than range
   Related: Outlier detection uses 1.5 × IQR

7. VARIANCE & STANDARD DEVIATION
   Variance: σ² = Σ(x - μ)² / (n - 1)
   Std Dev: σ = √σ²
   What: Average squared deviation from mean
   Use: Measure spread/variability
   Interpretation: 68% within ±1σ (normal data)
                   95% within ±2σ
                   99.7% within ±3σ
"""

# ============================================================================
# ENHANCED ANALYTICS ENGINE
# ============================================================================

class BizDesc:
    """
    Enhanced Educational Analytics Engine

    Features:
    - Central tendency statistics (mean, median, mode)
    - 9 visualization types
    - Professional color schemes
    - Detailed labels and formatting
    """

    def __init__(self, data: Union[IntoFrame, str, Path], color_scheme: str = "academic"):
        """Initialize with DataFrame or file path."""
        if isinstance(data, (str, Path)):
            path = Path(data)
            if path.suffix == ".csv":
                df_native = pd.read_csv(path)
            elif path.suffix in [".xlsx", ".xls"]:
                df_native = pd.read_excel(path)
            elif path.suffix == ".parquet":
                df_native = pd.read_parquet(path)
            else:
                raise ValueError(f"Unsupported file format: {path.suffix}")
        else:
            # Convert to pandas if not already
            if isinstance(data, pd.DataFrame):
                df_native = data
            elif isinstance(data, dict):
                df_native = pd.DataFrame(data)
            elif isinstance(data, list):
                df_native = pd.DataFrame(data)
            else:
                # Try to convert anything else to DataFrame
                df_native = pd.DataFrame(data)

        self.df_pandas = df_native
        self.df = nw.from_native(df_native, eager_only=True)

        # Detect numeric and categorical columns
        numeric_dtypes = ['int64', 'int32', 'float64', 'float32', 'int16', 'int8', 'float16']
        self.numeric_cols = [col for col in self.df_pandas.columns
                           if str(self.df_pandas[col].dtype) in numeric_dtypes or
                           pd.api.types.is_numeric_dtype(self.df_pandas[col])]
        self.cat_cols = [col for col in self.df_pandas.columns
                        if col not in self.numeric_cols]

        self.colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["academic"])

        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['axes.facecolor'] = '#F8F9FA'

    def central_tendency(self) -> Dict[str, Dict[str, Any]]:
        """
        Calculate comprehensive central tendency statistics.

        FORMULAS:
        - Mean: μ = Σx / n
        - Median: 50th percentile
        - Mode: Most frequent value
        - Range: Max - Min
        """
        results = {}

        for col in self.numeric_cols:
            col_data = np.array(self.df_pandas[col].values)
            col_data = col_data[~np.isnan(col_data)]

            if len(col_data) == 0:
                continue

            # FORMULA: Central tendency
            mean_val = float(np.mean(col_data))
            median_val = float(np.median(col_data))

            # Mode calculation
            mode_result = stats.mode(col_data, keepdims=True)
            mode_val = float(mode_result[0][0]) if len(mode_result[0]) > 0 else np.nan

            # Range
            min_val = float(np.min(col_data))
            max_val = float(np.max(col_data))
            range_val = max_val - min_val

            # Distribution characteristics
            std_val = float(np.std(col_data, ddof=1))
            skew_val = float(stats.skew(col_data))

            # Determine distribution type
            if abs(skew_val) < 0.5:
                dist_type = "Symmetric (Normal-like)"
            elif skew_val > 0:
                dist_type = "Right-Skewed (Positive tail)"
            else:
                dist_type = "Left-Skewed (Negative tail)"

            results[col] = {
                "mean": round(mean_val, 3),
                "median": round(median_val, 3),
                "mode": round(mode_val, 3) if not np.isnan(mode_val) else None,
                "min": round(min_val, 3),
                "max": round(max_val, 3),
                "range": round(range_val, 3),
                "std_dev": round(std_val, 3),
                "skewness": round(skew_val, 3),
                "distribution_type": dist_type,
                "mean_vs_median": "Mean > Median (Right-skewed)" if mean_val > median_val else "Median > Mean (Left-skewed)" if median_val > mean_val else "Equal (Symmetric)"
            }

        # Print formatted output
        print(f"\n{'='*90}")
        print(f"📊 CENTRAL TENDENCY ANALYSIS")
        print(f"{'='*90}\n")

        for col, stats_dict in results.items():
            print(f"🔍 {col.upper()}")
            print(f"  Mean (μ)            : {stats_dict['mean']:>10}  (Average value)")
            print(f"  Median              : {stats_dict['median']:>10}  (Middle value when sorted)")
            print(f"  Mode                : {stats_dict['mode']:>10}  (Most frequent value)")
            print(f"  Range               : {stats_dict['range']:>10}  (Max - Min)")
            print(f"  Std Dev (σ)         : {stats_dict['std_dev']:>10}  (Spread around mean)")
            print(f"  Skewness            : {stats_dict['skewness']:>10}  ({stats_dict['distribution_type']})")
            print(f"  Relationship        : {stats_dict['mean_vs_median']}")
            print()

        return results

    def describe(self, include_plots: bool = True, bins: int = 30,
                 figsize: tuple = (15, 6)) -> Dict[str, Any]:
        """
        Enhanced descriptive statistics with visualizations.
        """
        # Get central tendency
        cent_tend = self.central_tendency()

        # Additional statistics
        stats_list = []
        for col in self.numeric_cols:
            col_data = np.array(self.df_pandas[col].values)
            col_data = col_data[~np.isnan(col_data)]

            if len(col_data) == 0:
                continue

            q1, q3 = float(np.percentile(col_data, 25)), float(np.percentile(col_data, 75))
            iqr_val = q3 - q1

            stats_list.append({
                "Column": col,
                "Count": len(col_data),
                "Mean": cent_tend[col]["mean"],
                "Median": cent_tend[col]["median"],
                "Q1": round(q1, 2),
                "Q3": round(q3, 2),
                "IQR": round(iqr_val, 2),
                "Std Dev": cent_tend[col]["std_dev"],
            })

        result = {
            "shape": self.df_pandas.shape,
            "numeric_stats": stats_list,
            "numeric_columns": self.numeric_cols,
            "categorical_columns": self.cat_cols,
            "central_tendency": cent_tend
        }

        print(f"\n{'='*90}")
        print(f"📈 DESCRIPTIVE STATISTICS SUMMARY")
        print(f"{'='*90}")
        print(f"Dataset: {result['shape'][0]} rows × {result['shape'][1]} columns")
        print(f"Numeric Columns: {len(self.numeric_cols)} | Categorical: {len(self.cat_cols)}\n")

        if stats_list:
            df_stats = pd.DataFrame(stats_list)
            print(df_stats.to_string(index=False))

        if include_plots and self.numeric_cols:
            self._plot_distributions(bins, figsize)

        return result

    def _plot_distributions(self, bins: int = 30, figsize: tuple = (15, 6)):
        """Plot histograms with mean/median lines."""
        n_cols = min(len(self.numeric_cols), 3)
        fig, axes = plt.subplots(1, n_cols, figsize=(5*n_cols, 4))

        if n_cols == 1:
            axes = [axes]

        for idx, col in enumerate(self.numeric_cols[:3]):
            data = self.df_pandas[col].dropna()

            axes[idx].hist(data, bins=bins, alpha=0.7, color=self.colors["primary"],
                          edgecolor='black', linewidth=0.5, label='Data')

            mean_val = data.mean()
            median_val = data.median()

            axes[idx].axvline(mean_val, color=self.colors["accent"], linestyle='--',
                            linewidth=2.5, label=f'Mean: {mean_val:.2f}')
            axes[idx].axvline(median_val, color=self.colors["success"], linestyle='-',
                            linewidth=2.5, label=f'Median: {median_val:.2f}')

            axes[idx].set_title(f"Distribution: {col}", fontsize=13, fontweight='bold', pad=10)
            axes[idx].set_xlabel("Value", fontweight='bold')
            axes[idx].set_ylabel("Frequency", fontweight='bold')
            axes[idx].legend(loc='upper right', framealpha=0.95)
            axes[idx].grid(alpha=0.3, linestyle='--')

        plt.suptitle("Histogram with Central Tendency Lines", fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.show()

    def visualize(self, column: str, plot_type: str = "histogram", **kwargs):
        """
        Create 9 types of visualizations.

        plot_type options:
        - "histogram" → Distribution with mean/median + distribution type annotation
        - "boxplot" → Quartiles and outliers
        - "violin" → Distribution density
        - "density" → Smooth curve
        - "bar" → Categorical counts with value labels
        - "line" → Trend over index
        - "pie" → Proportions with percentages
        - "scatter" → Two variables
        - "heatmap" → All correlations
        """
        native_df = self.df_pandas

        data = native_df[column].dropna()

        fig, ax = plt.subplots(figsize=(12, 6))

        if plot_type == "histogram":
            bins = kwargs.get('bins', 30)
            ax.hist(data, bins=bins, alpha=0.7, color=self.colors["primary"],
                   edgecolor='black', linewidth=0.5)

            # Calculate statistics
            mean_val = data.mean()
            median_val = data.median()
            mode_val = data.mode()[0] if len(data.mode()) > 0 else None
            min_val = data.min()
            max_val = data.max()
            range_val = max_val - min_val

            # Plot lines
            ax.axvline(mean_val, color=self.colors["accent"], linestyle='--',
                      linewidth=2.5, label=f'Mean: {mean_val:.2f}')
            ax.axvline(median_val, color=self.colors["success"], linestyle='-',
                      linewidth=2.5, label=f'Median: {median_val:.2f}')
            if mode_val and not np.isnan(mode_val):
                ax.axvline(mode_val, color=self.colors["danger"], linestyle=':',
                          linewidth=2, alpha=0.7, label=f'Mode: {mode_val:.2f}')

            # Determine distribution type
            skewness = float(stats.skew(data.dropna()))
            if abs(skewness) < 0.5:
                dist_type = "SYMMETRIC (Normal-like)"
            elif skewness > 0:
                dist_type = "RIGHT-SKEWED (Positive tail)"
            else:
                dist_type = "LEFT-SKEWED (Negative tail)"

            # Add distribution annotation
            ax.text(0.98, 0.97, f"Distribution: {dist_type}\nSkewness: {skewness:.3f}",
                   transform=ax.transAxes, fontsize=11, fontweight='bold',
                   verticalalignment='top', horizontalalignment='right',
                   bbox=dict(boxstyle='round', facecolor=self.colors["accent"], alpha=0.8, pad=0.8))

            # Add statistics box
            stats_text = f"Range: [{min_val:.2f}, {max_val:.2f}]\nRange Width: {range_val:.2f}\nStd Dev: {data.std():.2f}"
            ax.text(0.02, 0.97, stats_text,
                   transform=ax.transAxes, fontsize=10, fontweight='bold',
                   verticalalignment='top', horizontalalignment='left',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, pad=0.8))

            ax.set_ylabel("Frequency", fontweight='bold')
            ax.legend(loc='upper center', framealpha=0.95)

        elif plot_type == "boxplot":
            bp = ax.boxplot(data, vert=True, patch_artist=True, widths=0.5,
                           boxprops=dict(facecolor=self.colors["primary"], alpha=0.7),
                           medianprops=dict(color=self.colors["danger"], linewidth=2),
                           whiskerprops=dict(linewidth=1.5),
                           capprops=dict(linewidth=1.5))
            ax.set_ylabel(column, fontweight='bold')
            ax.grid(alpha=0.3, axis='y')

        elif plot_type == "violin":
            parts = ax.violinplot(data, vert=True, showmeans=True, showmedians=True)
            for pc in parts['bodies']:
                pc.set_facecolor(self.colors["primary"])
                pc.set_alpha(0.7)
            ax.set_ylabel(column, fontweight='bold')

        elif plot_type == "density":
            data.plot(kind='density', ax=ax, color=self.colors["primary"], linewidth=2.5)
            ax.fill_between(ax.get_lines()[0].get_xdata(), ax.get_lines()[0].get_ydata(),
                           alpha=0.3, color=self.colors["primary"])
            ax.set_ylabel("Density", fontweight='bold')

        elif plot_type == "bar":
            value_counts = data.value_counts().sort_index().head(15)
            bars = ax.bar(range(len(value_counts)), value_counts.values,
                         color=self.colors["palette"], edgecolor='black', linewidth=1)

            # Add value labels on bars
            for i, bar in enumerate(bars):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}',
                       ha='center', va='bottom', fontweight='bold', fontsize=9)

            ax.set_xticks(range(len(value_counts)))
            ax.set_xticklabels(value_counts.index, rotation=45, ha='right')
            ax.set_ylabel("Count", fontweight='bold')
            ax.set_xlabel(column, fontweight='bold')
            ax.grid(alpha=0.3, axis='y')

        elif plot_type == "line":
            ax.plot(data.values, color=self.colors["primary"], linewidth=2, marker='o',
                   markersize=4, alpha=0.7)
            ax.fill_between(range(len(data)), data.values, alpha=0.3, color=self.colors["primary"])
            ax.set_ylabel(column, fontweight='bold')
            ax.set_xlabel("Index", fontweight='bold')
            ax.grid(alpha=0.3)

        elif plot_type == "pie":
            value_counts = data.value_counts().head(10)
            wedges, texts, autotexts = ax.pie(value_counts, labels=value_counts.index,
                                              autopct='%1.1f%%', colors=self.colors["palette"],
                                              startangle=90, textprops={'fontweight': 'bold'})
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(10)
                autotext.set_fontweight('bold')

        ax.set_title(f"{column} - {plot_type.capitalize()}", fontsize=14, fontweight='bold', pad=15)
        ax.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()

    def compare_categorical(self, cat_column: str, numeric_column: str = None):
        """
        Compare numeric values across categories.
        Shows box plots + bar charts with labels.
        """
        native_df = self.df_pandas

        fig, axes = plt.subplots(1, 2, figsize=(15, 5))

        # Boxplot by category
        categories = native_df[cat_column].unique()
        box_data = [native_df[native_df[cat_column] == cat][numeric_column or self.numeric_cols[0]].dropna()
                   for cat in categories]

        bp = axes[0].boxplot(box_data, labels=categories, patch_artist=True, widths=0.6)
        for patch, color in zip(bp['boxes'], self.colors["palette"]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        axes[0].set_xlabel(cat_column, fontweight='bold')
        axes[0].set_ylabel(numeric_column or self.numeric_cols[0], fontweight='bold')
        axes[0].set_title(f"Distribution by {cat_column}", fontweight='bold', fontsize=12)
        axes[0].grid(alpha=0.3, axis='y')

        # Mean by category
        means = native_df.groupby(cat_column)[numeric_column or self.numeric_cols[0]].mean()
        bars = axes[1].bar(range(len(means)), means.values, color=self.colors["palette"],
                          edgecolor='black', linewidth=1.5)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.2f}',
                        ha='center', va='bottom', fontweight='bold', fontsize=10)

        axes[1].set_xticks(range(len(means)))
        axes[1].set_xticklabels(means.index, rotation=45)
        axes[1].set_xlabel(cat_column, fontweight='bold')
        axes[1].set_ylabel(f"Average {numeric_column or self.numeric_cols[0]}", fontweight='bold')
        axes[1].set_title(f"Mean by {cat_column}", fontweight='bold', fontsize=12)
        axes[1].grid(alpha=0.3, axis='y')

        plt.tight_layout()
        plt.show()

    def correlations(self, method: str = "pearson") -> pd.DataFrame:
        """
        Calculate and visualize correlations with enhanced formatting.

        FORMULA (Pearson):
        r = Σ((x - μₓ)(y - μᵧ)) / √(Σ(x - μₓ)² × Σ(y - μᵧ)²)
        """
        native_df = self.df_pandas

        numeric_df = native_df[self.numeric_cols]
        corr_matrix = numeric_df.corr(method=method)

        # Visualize with enhanced heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='RdBu_r', center=0,
                   square=True, linewidths=1.5, cbar_kws={'label': 'Correlation Coefficient'},
                   vmin=-1, vmax=1, ax=ax, annot_kws={'fontweight': 'bold', 'fontsize': 10})

        ax.set_title(f"Correlation Matrix ({method})", fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.show()

        print(f"\n{'='*70}")
        print(f"📊 CORRELATION ANALYSIS (Pearson)")
        print(f"{'='*70}\n{corr_matrix}\n")

        return corr_matrix

    def outliers(self, method: str = "iqr") -> Dict[str, Any]:
        """
        Detect outliers with visualization.

        FORMULA:
        Lower = Q1 - 1.5 × IQR
        Upper = Q3 + 1.5 × IQR
        """
        results = {}
        native_df = self.df_pandas

        fig, axes = plt.subplots(len(self.numeric_cols), 1, figsize=(12, 4*len(self.numeric_cols)))
        if len(self.numeric_cols) == 1:
            axes = [axes]

        for idx, col in enumerate(self.numeric_cols):
            col_data = np.array(self.df_pandas[col].values)
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
                "bounds": {"lower": round(lower, 2), "upper": round(upper, 2)},
                "Q1": round(Q1, 2),
                "Q3": round(Q3, 2),
                "IQR": round(IQR, 2)
            }

            # Boxplot visualization
            bp = axes[idx].boxplot(col_data, vert=False, patch_artist=True,
                                  boxprops=dict(facecolor=self.colors["primary"], alpha=0.7),
                                  medianprops=dict(color=self.colors["danger"], linewidth=2),
                                  flierprops=dict(marker='o', markerfacecolor=self.colors["danger"],
                                                markersize=8, alpha=0.7))

            axes[idx].set_xlabel(col, fontweight='bold')
            axes[idx].text(0.02, 0.95, f"Outliers: {outlier_count} ({outlier_pct:.1f}%)",
                          transform=axes[idx].transAxes, fontweight='bold',
                          bbox=dict(boxstyle='round', facecolor=self.colors["accent"], alpha=0.7),
                          verticalalignment='top')
            axes[idx].grid(alpha=0.3, axis='x')

        plt.suptitle("Outlier Detection (IQR Method)", fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()

        print(f"\n{'='*70}")
        print(f"🔍 OUTLIER DETECTION (IQR Method)")
        print(f"{'='*70}\n")
        for col, info in results.items():
            print(f"{col}:")
            print(f"  Q1: {info['Q1']} | Q3: {info['Q3']} | IQR: {info['IQR']}")
            print(f"  Valid Range: [{info['bounds']['lower']:.2f}, {info['bounds']['upper']:.2f}]")
            print(f"  Outliers: {info['count']} ({info['percentage']}%)\n")

        return results

    def normality_test(self) -> Dict[str, Any]:
        """
        Shapiro-Wilk test for normality.
        """
        results = {}

        for col in self.numeric_cols:
            col_data = np.array(self.df_pandas[col].values)
            col_data = col_data[~np.isnan(col_data)]

            if len(col_data) < 3:
                continue

            stat, p_value = stats.shapiro(col_data)
            is_normal = p_value > 0.05

            results[col] = {
                "statistic": round(float(stat), 4),
                "p_value": round(float(p_value), 6),
                "is_normal": is_normal,
                "interpretation": "✓ Normal" if is_normal else "✗ NOT Normal"
            }

        print(f"\n{'='*70}")
        print(f"📈 NORMALITY TEST (Shapiro-Wilk)")
        print(f"{'='*70}\n")
        for col, info in results.items():
            print(f"{col}:")
            print(f"  p-value: {info['p_value']}")
            print(f"  Result: {info['interpretation']}\n")

        return results


# ============================================================================
# EDUCATIONAL DATASETS
# ============================================================================

def load_dataset(name: str, n_rows: int = None) -> pd.DataFrame:
    """
    Load educational dataset (internal or external).

    Internal datasets:
    - 'school_cafeteria' → School spending data
    - 'test_scores' → Student test scores

    External datasets (seaborn, sklearn, scipy):
    - 'iris', 'titanic', 'tips', 'penguins', 'diamonds', 'flights', 'mpg', etc.

    Use list_sample_datasets() to see all available external datasets.

    Returns: pandas DataFrame
    """
    # Try internal datasets first
    if name == "school_cafeteria":
        return generate_school_cafeteria(n_rows or 200)
    elif name == "test_scores":
        return generate_test_scores(n_rows or 100)

    # Try external datasets
    try:
        from .datasets import load_sample_dataset
        return load_sample_dataset(name)
    except ImportError:
        raise ValueError(f"Unknown dataset: {name}")
    except Exception as e:
        raise ValueError(f"Error loading dataset '{name}': {str(e)}")


def generate_school_cafeteria(n: int = 200, seed: int = 42) -> pd.DataFrame:
    """School cafeteria data with realistic patterns."""
    np.random.seed(seed)

    return pd.DataFrame({
        "student_id": np.arange(1, n + 1),
        "age": np.random.choice([14, 15, 16, 17, 18], n, p=[0.2, 0.25, 0.25, 0.2, 0.1]),
        "lunch_type": np.random.choice(
            ["Hot Meal", "Packed Lunch", "Salad", "Pizza"],
            n,
            p=[0.35, 0.25, 0.2, 0.2]
        ),
        "spending": np.minimum(np.random.exponential(4.5, n), 25).round(2),
        "satisfaction": np.clip(np.random.normal(6.5, 1.5, n), 1, 10).round(1),
    })


def generate_test_scores(n: int = 100, seed: int = 42) -> pd.DataFrame:
    """Student test scores across subjects."""
    np.random.seed(seed)

    ability = np.random.normal(70, 15, n)

    data = []
    for i in range(n):
        data.append({
            "student_id": i+1,
            "subject": "Mathematics",
            "score": np.clip(ability[i] + np.random.normal(0, 8), 0, 100).round(1)
        })
        data.append({
            "student_id": i+1,
            "subject": "English",
            "score": np.clip(np.random.choice(
                [np.random.normal(65, 10), np.random.normal(85, 8)]), 0, 100).round(1)
        })
        data.append({
            "student_id": i+1,
            "subject": "Science",
            "score": np.clip(ability[i] + np.random.normal(0, 10), 0, 100).round(1)
        })

    return pd.DataFrame(data)


# ============================================================================
# DATASET DISCOVERY & UTILITIES
# ============================================================================

def list_sample_datasets() -> pd.DataFrame:
    """
    List all available sample datasets.

    Returns:
        DataFrame with dataset information
    """
    try:
        from .datasets import list_available_datasets
        df = list_available_datasets()
        print("\n" + "="*100)
        print("📚 AVAILABLE SAMPLE DATASETS")
        print("="*100 + "\n")
        print(df.to_string(index=False))
        print("\n" + "="*100)
        print("Usage: df = bl.load_dataset('iris')")
        print("="*100 + "\n")
        return df
    except ImportError:
        print("❌ datasets module not available")
        return pd.DataFrame()


def dataset_info(name: str):
    """
    Print detailed information about a sample dataset.

    Args:
        name: Dataset name
    """
    try:
        from .datasets import print_dataset_info
        print_dataset_info(name)
    except ImportError:
        print("❌ datasets module not available")


# ============================================================================
# QUICK API
# ============================================================================

def describe(data, plots=True, color_scheme="academic", **kwargs) -> Dict:
    """One-liner for complete analysis."""
    bd = BizDesc(data, color_scheme=color_scheme)
    return bd.describe(include_plots=plots, **kwargs)
