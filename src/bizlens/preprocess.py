"""
BizLens Preprocessing Module v2.3.2
Creates realistic messy data and provides cleaning pipeline.
Designed to be better than textbook examples.
"""

import pandas as pd
import numpy as np
import time
from rich.console import Console
from . import ENABLE_PROFILING
from .utils import to_pandas
from .quality import quality
from .diagnostic import diagnostic

console = Console()


class preprocess:
    """
    Controlled messy data generation + cleaning tools for teaching real-world workflow.
    """

    @staticmethod
    def make_clean_data(base_df, show_timing: bool = False):
        """Return a guaranteed clean copy."""
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        clean = to_pandas(base_df).copy()
        console.print("[green]✅ Created clean baseline dataset[/green]")
        if ENABLE_PROFILING or show_timing:
            console.print(f"[dim][Profiling] preprocess.make_clean_data in {time.perf_counter()-start:.4f}s[/dim]")
        return clean


    @staticmethod
    def add_outliers(df, columns=None, rate=0.05, severity=3.0, show_timing: bool = False):
        """Inject realistic outliers."""
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        df = to_pandas(df).copy()
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        for col in columns:
            if col in df.columns:
                mask = np.random.rand(len(df)) < rate
                df.loc[mask, col] = df[col].mean() + severity * df[col].std() * np.random.randn(mask.sum())
        console.print(f"[yellow]⚠️ Injected outliers in {len(columns)} columns ({rate*100:.1f}% rate)[/yellow]")
        if ENABLE_PROFILING or show_timing:
            console.print(f"[dim][Profiling] preprocess.add_outliers completed in {time.perf_counter()-start:.4f}s[/dim]")
        return df


    @staticmethod
    def add_duplicates(df, rate=0.03, show_timing: bool = False):
        """Inject duplicate rows."""
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        df = to_pandas(df).copy()
        n_duplicates = int(len(df) * rate)
        duplicates = df.sample(n_duplicates, replace=True)
        df = pd.concat([df, duplicates], ignore_index=True)
        console.print(f"[yellow]⚠️ Injected {n_duplicates} duplicate rows ({rate*100:.1f}% rate)[/yellow]")
        if ENABLE_PROFILING or show_timing:
            console.print(f"[dim][Profiling] preprocess.add_duplicates completed in {time.perf_counter()-start:.4f}s[/dim]")
        return df


    @staticmethod
    def add_missing_values(df, rate=0.08, columns=None, show_timing: bool = False):
        """Inject missing values."""
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()
        df = to_pandas(df).copy()
        if columns is None:
            columns = df.columns.tolist()
        for col in columns:
            if col in df.columns:
                mask = np.random.rand(len(df)) < rate
                df.loc[mask, col] = np.nan
        console.print(f"[yellow]⚠️ Injected missing values ({rate*100:.1f}% rate)[/yellow]")
        if ENABLE_PROFILING or show_timing:
            console.print(f"[dim][Profiling] preprocess.add_missing_values completed in {time.perf_counter()-start:.4f}s[/dim]")
        return df


    @staticmethod
    def make_messy_data(clean_df, outlier_rate=0.05, duplicate_rate=0.03, missing_rate=0.08, show_timing: bool = False):
        """One-command function to create realistic messy data for teaching."""
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        messy = to_pandas(clean_df).copy()
        messy = preprocess.add_outliers(messy, rate=outlier_rate)
        messy = preprocess.add_duplicates(messy, rate=duplicate_rate)
        messy = preprocess.add_missing_values(messy, rate=missing_rate)

        console.print(f"[bold yellow]📦 Created messy dataset with realistic issues — ready for preprocessing practice![/bold yellow]")

        if ENABLE_PROFILING or show_timing:
            console.print(f"[dim][Profiling] preprocess.make_messy_data completed in {time.perf_counter()-start:.4f}s[/dim]")

        return messy


    @staticmethod
    def clean_data(df, show_timing: bool = False):
        """Full automated cleaning pipeline with educational reports."""
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        df = to_pandas(df).copy()

        console.print("[bold cyan]🧹 Starting Data Cleaning Pipeline[/bold cyan]")

        quality.data_profile(df)

        # Remove duplicates
        before = len(df)
        df = df.drop_duplicates()
        console.print(f"[green]✓ Removed {before - len(df)} duplicate rows[/green]")

        # Simple median imputation for teaching
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].median())
                console.print(f"[green]✓ Imputed missing values in {col} with median[/green]")

        quality.data_profile(df)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] preprocess.clean_data completed in {duration:.4f}s[/dim]")

        console.print("[bold green]✅ Data is now clean and ready for analysis![/bold green]")
        return df