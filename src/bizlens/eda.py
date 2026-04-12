"""
BizLens EDA Module v2.3.2
Advanced Exploratory Data Analysis with rich educational insights.
"""

import pandas as pd
import numpy as np
import time
import seaborn as sns
import matplotlib.pyplot as plt
from rich.console import Console
from rich.panel import Panel
from . import ENABLE_PROFILING
from .utils import to_pandas
from .tables import tables
from .diagnostic import diagnostic

console = Console()


class eda:
    """
    Full Exploratory Data Analysis pipeline — better than textbooks.
    """

    @staticmethod
    def plot_distributions(df, cols=None, show_timing: bool = False):
        if ENABLE_PROFILING or show_timing: start = time.perf_counter()
        df = to_pandas(df)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if cols: numeric_cols = [c for c in cols if c in numeric_cols]
        if not numeric_cols: return
        n_cols = min(3, len(numeric_cols))
        n_rows = int(np.ceil(len(numeric_cols) / n_cols))
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows))
        axes = np.array(axes).flatten() if hasattr(axes, '__iter__') else [axes]
        for i, col in enumerate(numeric_cols):
            sns.histplot(df[col], kde=True, ax=axes[i], color='royalblue', alpha=0.6)
            axes[i].set_title(f'Distribution of {col}', fontweight='bold')
        for j in range(len(numeric_cols), len(axes)): fig.delaxes(axes[j])
        plt.tight_layout()
        plt.show()
        if ENABLE_PROFILING or show_timing: console.print(f"[dim][Profiling] eda.plot_distributions in {time.perf_counter()-start:.4f}s[/dim]")

    @staticmethod
    def plot_correlation_heatmap(df, show_timing: bool = False):
        if ENABLE_PROFILING or show_timing: start = time.perf_counter()
        df = to_pandas(df)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) < 2: return
        corr = df[numeric_cols].corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        
        # Calculate dynamic figure size based on number of columns
        fig_width = max(8, len(numeric_cols)*0.8)
        fig_height = max(6, len(numeric_cols)*0.6)
        
        plt.figure(figsize=(fig_width, fig_height))
        sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1, center=0, square=True, linewidths=.5)
        plt.title('Correlation Heatmap', fontweight='bold', fontsize=14)
        plt.tight_layout()
        plt.show()
        if ENABLE_PROFILING or show_timing: console.print(f"[dim][Profiling] eda.plot_correlation_heatmap in {time.perf_counter()-start:.4f}s[/dim]")

    @staticmethod
    def plot_categorical(df, cols=None, show_timing: bool = False):
        if ENABLE_PROFILING or show_timing: start = time.perf_counter()
        df = to_pandas(df)
        cat_cols = df.select_dtypes(exclude=[np.number, 'datetime', 'timedelta']).columns.tolist()
        if cols: cat_cols = [c for c in cols if c in cat_cols]
        if not cat_cols: return
        n_cols = min(2, len(cat_cols))
        n_rows = int(np.ceil(len(cat_cols) / n_cols))
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(6*n_cols, 5*n_rows))
        axes = np.array(axes).flatten() if hasattr(axes, '__iter__') else [axes]
        for i, col in enumerate(cat_cols):
            val_counts = df[col].value_counts().head(10)
            sns.barplot(x=val_counts.values, y=val_counts.index.astype(str), ax=axes[i], palette='viridis')
            axes[i].set_title(f'Counts of {col} (Top 10)', fontweight='bold')
            axes[i].set_xlabel('Count')
        for j in range(len(cat_cols), len(axes)): fig.delaxes(axes[j])
        plt.tight_layout()
        plt.show()
        if ENABLE_PROFILING or show_timing: console.print(f"[dim][Profiling] eda.plot_categorical in {time.perf_counter()-start:.4f}s[/dim]")

    @staticmethod
    def full_report(df, show_timing: bool = False):
        """Complete EDA report with insights and visuals."""
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        df = to_pandas(df)

        console.print(Panel("[bold cyan]📊 BizLens Full Exploratory Data Analysis Report[/bold cyan]", style="bold blue"))

        console.print("[bold magenta]1. Summary Statistics[/bold magenta]")
        tables.summary_statistics(df)
        
        console.print("[bold magenta]2. Missing Value Analysis[/bold magenta]")
        diagnostic.missing_value_analysis(df)

        console.print("[bold magenta]3. Feature Distributions[/bold magenta]")
        eda.plot_distributions(df)
        
        console.print("[bold magenta]4. Categorical Breakdown[/bold magenta]")
        eda.plot_categorical(df)

        console.print("[bold magenta]5. Correlation Heatmap[/bold magenta]")
        eda.plot_correlation_heatmap(df)

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) >= 2:
            console.print("[bold magenta]6. Pairplot (top 4 numeric features)[/bold magenta]")
            plt.figure(figsize=(12, 8))
            sns.pairplot(df[numeric_cols[:4]], diag_kind='kde', plot_kws={'alpha':0.6})
            plt.suptitle("Pairplot of Key Numeric Features", y=1.02, fontweight='bold')
            plt.show()

        console.print("[bold green]✅ EDA Complete — Ready for modeling or process mining![/bold green]")

        if ENABLE_PROFILING or show_timing:
            console.print(f"[dim][Profiling] eda.full_report completed in {time.perf_counter()-start:.4f}s[/dim]")