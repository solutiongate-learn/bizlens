"""
BizLens v2.2.12 — Complete Datasets & Event Log Repository
Enhanced: Performance timing on all load/generate functions + version bump.
"""

import polars as pl
import numpy as np
import seaborn as sns
import warnings
import time
from datetime import datetime, timedelta
from rich.console import Console
from . import ENABLE_PROFILING   # global flag from __init__.py

warnings.filterwarnings("ignore")
console = Console()


def _to_pandas(df):
    """Internal helper (for consistency with other modules)."""
    if isinstance(df, pl.DataFrame):
        return df.to_pandas()
    return df


# ─────────────────────────────────────────────────────────────────────────────
# CLASSIC TEACHING DATASETS
# ─────────────────────────────────────────────────────────────────────────────
def load_dataset(name: str, show_timing: bool = False) -> pl.DataFrame:
    if ENABLE_PROFILING or show_timing:
        start = time.perf_counter()

    try:
        if name == "tips":
            df_pd = sns.load_dataset("tips")
            console.print(f"[green]✅ Loaded 'tips' ({len(df_pd)} rows × {len(df_pd.columns)} columns)[/green]")
            console.print("Restaurant tips — classic for correlation, categorical comparison")
            df = pl.from_pandas(df_pd)
        elif name == "iris":
            df_pd = sns.load_dataset("iris")
            console.print(f"[green]✅ Loaded 'iris' ({len(df_pd)} rows)[/green]")
            console.print("Classic iris flower measurements — beginner classification")
            df = pl.from_pandas(df_pd)
        elif name == "titanic":
            df_pd = sns.load_dataset("titanic")
            console.print(f"[green]✅ Loaded 'titanic' ({len(df_pd)} rows)[/green]")
            console.print("Passenger survival data — beginner classification & missing values")
            df = pl.from_pandas(df_pd)
        elif name == "penguins":
            df_pd = sns.load_dataset("penguins")
            console.print(f"[green]✅ Loaded 'penguins' ({len(df_pd)} rows)[/green]")
            console.print("Palmer penguins — modern alternative to iris")
            df = pl.from_pandas(df_pd)
        elif name == "diamonds":
            df_pd = sns.load_dataset("diamonds")
            console.print(f"[green]✅ Loaded 'diamonds' ({len(df_pd)} rows)[/green]")
            console.print("Diamond prices — regression & large dataset example")
            df = pl.from_pandas(df_pd)
        elif name == "mpg":
            df_pd = sns.load_dataset("mpg")
            console.print(f"[green]✅ Loaded 'mpg' ({len(df_pd)} rows)[/green]")
            df = pl.from_pandas(df_pd)
        elif name == "flights":
            df_pd = sns.load_dataset("flights")
            console.print(f"[green]✅ Loaded 'flights' ({len(df_pd)} rows)[/green]")
            df = pl.from_pandas(df_pd)
        else:
            df_pd = sns.load_dataset(name)
            console.print(f"[green]✅ Loaded '{name}' via seaborn[/green]")
            df = pl.from_pandas(df_pd)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] datasets.load_dataset('{name}') completed in {duration:.4f}s[/dim]")

        return df

    except Exception as e:
        console.print(f"[red]Error loading {name}: {e}[/red]")
        console.print("Available: tips, iris, titanic, penguins, diamonds, mpg, flights")
        raise


def list_datasets():
    """List all available datasets and event logs (unchanged)."""
    return {
        "Classic Teaching Datasets": ["tips", "iris", "titanic", "penguins", "diamonds", "mpg", "flights"],
        "Process Mining Event Logs (2026)": [
            "generate_hr_onboarding_event_log()",
            "generate_healthcare_event_log()",
            "generate_manufacturing_event_log()",
            "generate_tech_support_event_log()"
        ],
        "Business": "generate_sample_data()",
        "Custom": "load_event_log_from_csv('your_file.csv')"
    }


# ─────────────────────────────────────────────────────────────────────────────
# PROCESS MINING EVENT LOGS
# ─────────────────────────────────────────────────────────────────────────────
def generate_sample_data(n_rows: int = 1000, seed: int = 42, show_timing: bool = False) -> pl.DataFrame:
    if ENABLE_PROFILING or show_timing:
        start = time.perf_counter()
    np.random.seed(seed)
    data = {
        "customer_id": [f"C{str(i).zfill(5)}" for i in range(n_rows)],
        "revenue": np.random.lognormal(mean=8, sigma=1.2, size=n_rows).round(2),
        "profit_margin": (np.random.beta(2, 5, size=n_rows) * 100).round(2),
        "customer_satisfaction": np.clip(np.random.normal(75, 12, size=n_rows), 0, 100).round(1),
        "units_sold": np.random.poisson(lam=45, size=n_rows),
        "region": np.random.choice(["North", "South", "East", "West"], size=n_rows),
    }
    df = pl.DataFrame(data)
    console.print(f"[bold green]✅ Generated classic business dataset ({n_rows} rows)[/bold green]")

    if ENABLE_PROFILING or show_timing:
        duration = time.perf_counter() - start
        console.print(f"[dim][Profiling] datasets.generate_sample_data completed in {duration:.4f}s[/dim]")
    return df


def generate_hr_onboarding_event_log(num_cases: int = 300, seed: int = 42, show_timing: bool = False) -> pl.DataFrame:
    if ENABLE_PROFILING or show_timing:
        start = time.perf_counter()
    # === ORIGINAL CODE (100% unchanged) ===
    np.random.seed(seed)
    activities = ["Initial Check-in", "Welcome & Orientation Session", "Documentation Completion",
                  "IT & Access Setup", "Core Training - Module 1", "Core Training - Module 2",
                  "Welcome Package Delivery", "Feedback & Review Session"]
    events = []
    start = datetime(2026, 1, 1)
    for case in range(1, num_cases + 1):
        current = start + timedelta(days=np.random.randint(0, 85))
        for act in np.random.choice(activities, np.random.randint(5, 9), replace=False):
            events.append({
                "case_id": f"EMP{str(case).zfill(5)}",
                "activity": act,
                "timestamp": current,
                "cost": round(np.random.uniform(50, 500), 2),
                "co2_impact": round(np.random.uniform(0.05, 2.5), 2),
                "resource": np.random.choice(["Alice", "Bob", "Charlie", "Diana"])
            })
            current += timedelta(minutes=np.random.randint(30, 2880))
    df = pl.DataFrame(events)
    console.print(f"[green]✅ HR Onboarding Event Log ({num_cases} cases)[/green]")

    if ENABLE_PROFILING or show_timing:
        duration = time.perf_counter() - start
        console.print(f"[dim][Profiling] datasets.generate_hr_onboarding_event_log completed in {duration:.4f}s[/dim]")
    return df


# (The other three generators — generate_healthcare_event_log, generate_manufacturing_event_log, generate_tech_support_event_log — follow the exact same pattern: add timing start/end around your original code.)

def generate_healthcare_event_log(num_cases: int = 200, seed: int = 42, show_timing: bool = False) -> pl.DataFrame:
    if ENABLE_PROFILING or show_timing:
        start = time.perf_counter()
    np.random.seed(seed)
    activities = ["Admission", "Triage", "Diagnosis", "Lab Test", "Treatment", "Surgery", "Discharge"]
    events = []
    start = datetime(2026, 1, 1)
    for case in range(1, num_cases + 1):
        current = start + timedelta(days=np.random.randint(0, 60))
        for act in np.random.choice(activities, np.random.randint(4, 7), replace=False):
            events.append({
                "case_id": f"PAT{str(case).zfill(5)}",
                "activity": act,
                "timestamp": current,
                "cost": round(np.random.uniform(200, 5000), 2),
                "length_of_stay_hours": np.random.randint(4, 240),
                "resource": np.random.choice(["Dr.Smith", "Nurse.Jones", "Dr.Lee"])
            })
            current += timedelta(hours=np.random.randint(2, 48))
    df = pl.DataFrame(events)
    console.print(f"[green]✅ Healthcare Event Log ({num_cases} patients)[/green]")

    if ENABLE_PROFILING or show_timing:
        duration = time.perf_counter() - start
        console.print(f"[dim][Profiling] datasets.generate_healthcare_event_log completed in {duration:.4f}s[/dim]")
    return df


def generate_manufacturing_event_log(num_cases: int = 250, seed: int = 42, show_timing: bool = False) -> pl.DataFrame:
    if ENABLE_PROFILING or show_timing:
        start = time.perf_counter()
    np.random.seed(seed)
    activities = ["Order Received", "Raw Material Issued", "Production Start", "Quality Inspection", "Packaging", "Shipping"]
    events = []
    start = datetime(2026, 1, 1)
    for case in range(1, num_cases + 1):
        current = start + timedelta(days=np.random.randint(0, 70))
        for act in activities:
            events.append({
                "case_id": f"ORD{str(case).zfill(5)}",
                "activity": act,
                "timestamp": current,
                "cost": round(np.random.uniform(300, 8000), 2),
                "defect_rate": round(np.random.uniform(0, 5), 2),
                "resource": np.random.choice(["LineA", "LineB", "LineC"])
            })
            current += timedelta(hours=np.random.randint(4, 72))
    df = pl.DataFrame(events)
    console.print(f"[green]✅ Manufacturing Event Log ({num_cases} orders)[/green]")

    if ENABLE_PROFILING or show_timing:
        duration = time.perf_counter() - start
        console.print(f"[dim][Profiling] datasets.generate_manufacturing_event_log completed in {duration:.4f}s[/dim]")
    return df


def generate_tech_support_event_log(num_cases: int = 400, seed: int = 42, show_timing: bool = False) -> pl.DataFrame:
    if ENABLE_PROFILING or show_timing:
        start = time.perf_counter()
    np.random.seed(seed)
    activities = ["Ticket Created", "Initial Triage", "Remote Diagnosis", "Escalation", "Resolution", "Customer Feedback"]
    events = []
    start = datetime(2026, 1, 1)
    for case in range(1, num_cases + 1):
        current = start + timedelta(days=np.random.randint(0, 90))
        for act in activities:
            events.append({
                "case_id": f"TKT{str(case).zfill(5)}",
                "activity": act,
                "timestamp": current,
                "resolution_time_minutes": np.random.randint(15, 480),
                "satisfaction_score": np.random.randint(1, 6),
                "resource": np.random.choice(["Agent1", "Agent2", "SeniorTech"])
            })
            current += timedelta(minutes=np.random.randint(10, 360))
    df = pl.DataFrame(events)
    console.print(f"[green]✅ Technical Support Event Log ({num_cases} tickets)[/green]")

    if ENABLE_PROFILING or show_timing:
        duration = time.perf_counter() - start
        console.print(f"[dim][Profiling] datasets.generate_tech_support_event_log completed in {duration:.4f}s[/dim]")
    return df


def load_event_log_from_csv(path: str, show_timing: bool = False) -> pl.DataFrame:
    if ENABLE_PROFILING or show_timing:
        start = time.perf_counter()
    df = pl.read_csv(path)
    console.print(f"[green]✅ Loaded external event log from {path} ({len(df):,} events)[/green]")

    if ENABLE_PROFILING or show_timing:
        duration = time.perf_counter() - start
        console.print(f"[dim][Profiling] datasets.load_event_log_from_csv completed in {duration:.4f}s[/dim]")
    return df


def list_datasets():
    return {
        "Classic": ["tips", "iris", "titanic", "penguins", "diamonds", "mpg", "flights"],
        "Event Logs": ["hr_onboarding", "healthcare", "manufacturing", "tech_support"],
        "Business": "generate_sample_data()"
    }


__all__ = [
    "load_dataset", "list_datasets",
    "generate_sample_data",
    "generate_hr_onboarding_event_log",
    "generate_healthcare_event_log",
    "generate_manufacturing_event_log",
    "generate_tech_support_event_log",
    "load_event_log_from_csv"
]