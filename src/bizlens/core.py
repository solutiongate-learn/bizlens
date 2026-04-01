import narwhals as nw
from narwhals.typing import IntoFrame
import polars as pl
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
from rich.console import Console
from rich.table import Table
from rich.prompt import IntPrompt
from pathlib import Path
from typing import List, Dict, Any, Union
import warnings

warnings.filterwarnings("ignore")
console = Console()

class BizDesc:
    """
    Business Descriptive Analytics engine with Polars-first design.
    Analyzes data distributions, compares against normality, and generates insights.
    """
    def __init__(self, data: Union[IntoFrame, str, Path]):
        """
        Initialize BizDesc with data from DataFrame or file path.

        Args:
            data: Polars/Pandas DataFrame, or path to CSV/Excel/Parquet file
        """
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
        self._last_result = None

    def summary(self, include_plots: bool = False, export: str | None = None,
                bins: int = 30, norm_compare: bool = True, save_plots: bool = False) -> Dict[str, Any]:
        """
        Generate comprehensive descriptive statistics summary.

        Args:
            include_plots: Whether to generate visualizations
            export: Path to export data (CSV, Excel, etc.)
            bins: Number of histogram bins
            norm_compare: Compare distributions against standard normal
            save_plots: Save plots to files instead of displaying

        Returns:
            Dictionary with shape, numeric stats, and missing values
        """
        nw_df = self.df
        numeric_cols = nw_df.select(nw.col(nw.NUMERIC_DTYPES)).columns
        cat_cols = nw_df.select(nw.col(nw.CATEGORICAL_DTYPES)).columns

        stats_list = []
        for col in numeric_cols:
            col_data = np.array(nw_df[col].to_numpy())
            col_data = col_data[~np.isnan(col_data)]  # Filter NaNs for stats

            if len(col_data) == 0:
                continue

            q1, q3 = np.percentile(col_data, [25, 75])

            # Mode calculation
            m = stats.mode(col_data, keepdims=True)
            mode_val = m[0][0] if len(m[0]) > 0 else np.nan

            stats_list.append({
                "Column": col,
                "Mean": round(float(np.mean(col_data)), 2),
                "Median": round(float(np.median(col_data)), 2),
                "Mode": round(float(mode_val), 2) if not np.isnan(mode_val) else "N/A",
                "Std_Dev": round(float(np.std(col_data)), 2),
                "Range": round(float(np.max(col_data) - np.min(col_data)), 2),
                "IQR": round(float(q3 - q1), 2),
                "Skewness": round(float(stats.skew(col_data)), 2),
            })

        missing = {col: int(nw_df[col].null_count()) for col in nw_df.columns}

        result = {
            "shape": (nw_df.shape[0], nw_df.shape[1]),
            "numeric_stats": stats_list,
            "missing_values": missing,
        }

        self._last_result = result
        self._print_rich_summary(result)

        if include_plots and numeric_cols:
            self._generate_charts(numeric_cols, cat_cols, bins, norm_compare, save_plots)

        if export:
            self._auto_export(export)

        return result

    def _generate_charts(self, numeric_cols: List[str], cat_cols: List[str],
                        bins: int, norm_compare: bool, save_plots: bool = False):
        """Generate distribution and normality comparison charts."""
        sns.set_theme(style="whitegrid")
        native_pd = self.df.to_native()
        if isinstance(native_pd, pl.DataFrame):
            native_pd = native_pd.to_pandas()

        console.print(f"\n[bold cyan]📊 Generating visual analytics...[/bold cyan]")

        for idx, col in enumerate(numeric_cols[:5]):  # Limit to first 5 for speed
            data = native_pd[col].dropna().values

            if len(data) == 0:
                continue

            mean_v, med_v = np.mean(data), np.median(data)

            fig, axes = plt.subplots(1, 2, figsize=(14, 5))

            # Subplot 1: Distribution with mean/median overlay
            sns.histplot(data, bins=bins, kde=True, ax=axes[0], color="#3498db")
            axes[0].axvline(mean_v, color='r', linestyle='--', linewidth=2, label=f'Mean: {mean_v:.1f}')
            axes[0].axvline(med_v, color='g', linestyle='-', linewidth=2, label=f'Median: {med_v:.1f}')
            axes[0].set_title(f"Distribution: {col}", fontsize=12, fontweight='bold')
            axes[0].set_xlabel("Value")
            axes[0].set_ylabel("Frequency")
            axes[0].legend()
            axes[0].grid(alpha=0.3)

            # Subplot 2: Normality Comparison (Z-score vs Standard Normal)
            if norm_compare:
                std_v = np.std(data)
                if std_v > 0:
                    z_data = (data - mean_v) / std_v
                else:
                    z_data = data - mean_v

                sns.histplot(z_data, bins=bins, kde=True, ax=axes[1],
                            color="#e74c3c", stat="density")
                x = np.linspace(-4, 4, 100)
                axes[1].plot(x, stats.norm.pdf(x), 'k--', linewidth=2, label="Std Normal")
                axes[1].set_title("Z-Score vs Standard Normal", fontsize=12, fontweight='bold')
                axes[1].set_xlabel("Z-Score")
                axes[1].set_ylabel("Density")
                axes[1].legend()
                axes[1].grid(alpha=0.3)

            plt.tight_layout()

            if save_plots:
                plot_path = f"bizlens_analysis_{col}_{idx}.png"
                plt.savefig(plot_path, dpi=300, bbox_inches='tight')
                console.print(f"[green]✅ Saved: {plot_path}[/green]")
                plt.close()
            else:
                plt.show()

    def _print_rich_summary(self, result):
        """Print formatted summary tables using Rich."""
        table = Table(title="🚀 BizLens v0.5.0 Analysis", header_style="bold magenta")
        table.add_column("Metric", style="dim")
        table.add_row("Dataset Shape", f"{result['shape'][0]} rows × {result['shape'][1]} cols")
        table.add_row("Total Missing Cells", str(sum(result["missing_values"].values())))
        console.print(table)

        # Display stats as a clean table
        if result["numeric_stats"]:
            stats_table = Table(title="📈 Numeric Column Breakdown")
            keys = result["numeric_stats"][0].keys()
            for key in keys:
                stats_table.add_column(key, justify="right")
            for row in result["numeric_stats"]:
                stats_table.add_row(*[str(v) for v in row.values()])
            console.print(stats_table)

    def _auto_export(self, filepath: str):
        """Export data to file (CSV, Excel, etc.)."""
        native = self.df.to_native()
        if filepath.endswith(".csv"):
            if hasattr(native, "write_csv"):
                native.write_csv(filepath)
            else:
                native.to_csv(filepath, index=False)
        elif filepath.endswith(".xlsx"):
            if hasattr(native, "write_excel"):
                native.write_excel(filepath)
            else:
                native.to_excel(filepath, index=False)
        console.print(f"[bold green]✅ Data exported to {filepath}[/bold green]")

    @staticmethod
    def create_interactive_demo() -> pl.DataFrame:
        """
        Generate realistic business dataset with skewed distributions.
        Interactive prompt for number of rows.
        """
        console.print("\n[bold yellow]🛠️  Building Interactive Demo Dataset...[/bold yellow]")
        rows = IntPrompt.ask("Enter number of rows", default=1000)

        np.random.seed(42)
        data = {
            "transaction_id": np.arange(rows),
            "region": np.random.choice(["East", "West", "North", "South"], rows),
            "revenue": np.random.exponential(scale=1000, size=rows),  # Skewed distribution
            "customer_satisfaction": np.random.normal(loc=7, scale=1.5, size=rows).clip(1, 10),
            "units_sold": np.random.poisson(lam=20, size=rows),
            "priority": np.random.choice(["Low", "Medium", "High"], rows, p=[0.5, 0.3, 0.2])
        }

        df = pl.DataFrame(data)
        console.print(f"[green]✅ Generated {rows} rows of business data[/green]")
        return df

    @staticmethod
    def load_sample_business_data() -> pl.DataFrame:
        """Load a pre-built sample dataset for quick demos."""
        np.random.seed(42)
        rows = 500
        data = {
            "transaction_id": np.arange(rows),
            "region": np.random.choice(["East", "West", "North", "South"], rows),
            "revenue": np.random.exponential(scale=1000, size=rows),
            "customer_satisfaction": np.random.normal(loc=7, scale=1.5, size=rows).clip(1, 10),
            "units_sold": np.random.poisson(lam=20, size=rows),
            "priority": np.random.choice(["Low", "Medium", "High"], rows, p=[0.5, 0.3, 0.2])
        }
        return pl.DataFrame(data)


# ============================================================================
# API Shortcuts - High-level interface
# ============================================================================

def describe(data, plots=False, export=None, bins=30, norm_compare=True, save_plots=False):
    """
    Quick-start function for business analytics.

    Args:
        data: DataFrame or file path
        plots: Generate visualizations
        export: Export to file path
        bins: Histogram bins
        norm_compare: Compare against standard normal
        save_plots: Save plots instead of displaying

    Returns:
        Dictionary with descriptive statistics
    """
    bd = BizDesc(data)
    return bd.summary(include_plots=plots, export=export, bins=bins,
                     norm_compare=norm_compare, save_plots=save_plots)
