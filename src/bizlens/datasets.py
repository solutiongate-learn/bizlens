"""
BizLens v2.3.2 — Datasets & Event Log Repository
"""

import pandas as pd
import numpy as np
import seaborn as sns
import warnings
import time
from rich.console import Console
from . import ENABLE_PROFILING
from .utils import to_pandas

warnings.filterwarnings("ignore")
console = Console()


def load_dataset(name: str, show_timing: bool = False) -> pd.DataFrame:
    if ENABLE_PROFILING or show_timing:
        t0 = time.perf_counter()

    try:
        df = sns.load_dataset(name)
        console.print(f"[green]✅ Loaded '{name}' ({len(df)} rows)[/green]")
        if ENABLE_PROFILING or show_timing:
            console.print(f"[dim][Profiling] load_dataset in {time.perf_counter()-t0:.4f}s[/dim]")
        return df
    except Exception as e:
        console.print(f"[red]Error loading '{name}': {e}[/red]")
        raise


def list_datasets() -> dict:
    return {
        "Classic Datasets": ["tips", "iris", "titanic", "penguins", "diamonds", "mpg", "flights"],
        "Process Mining Event Logs": [
            "generate_hr_onboarding_event_log()",
            "generate_healthcare_event_log()",
            "generate_manufacturing_event_log()",
            "generate_tech_support_event_log()",
            "generate_clean_ecommerce_data()",
        ],
        "Helpers": [
            "as_pandas(df) → Best for visualization",
            "as_polars(df) → Best for speed"
        ]
    }


def _simulate_process(process_def, n_cases, start_date='2023-01-01', seed=42):
    np.random.seed(seed)
    data = []
    base_time = pd.to_datetime(start_date)
    case_ids = [f"CASE_{i:04d}" for i in range(1, n_cases + 1)]
    
    for cid in case_ids:
        current_time = base_time + pd.Timedelta(seconds=np.random.randint(0, 30*24*3600))
        for act in process_def:
            if np.random.rand() > act.get('prob', 1.0): continue
            data.append({
                'case_id': cid,
                'activity': act['name'],
                'timestamp': current_time,
                'resource': np.random.choice(act.get('resources', ['System']))
            })
            current_time += pd.Timedelta(minutes=np.random.gamma(act.get('dur_shape', 2), act.get('dur_scale', 60)))
    return pd.DataFrame(data).sort_values('timestamp').reset_index(drop=True)

def generate_hr_onboarding_event_log(n_cases: int = 500, seed: int = 42, show_timing: bool = False) -> pd.DataFrame:
    if ENABLE_PROFILING or show_timing: t0 = time.perf_counter()
    process = [
        {'name': 'Application Received', 'prob': 1.0, 'resources': ['System']},
        {'name': 'Screening', 'prob': 1.0, 'resources': ['HR_Alice', 'HR_Bob'], 'dur_scale': 1440},
        {'name': 'Interview 1', 'prob': 0.7, 'resources': ['Mgr_X', 'Mgr_Y'], 'dur_scale': 2880},
        {'name': 'Interview 2', 'prob': 0.4, 'resources': ['Dir_Z']},
        {'name': 'Offer Extended', 'prob': 0.2, 'resources': ['HR_Alice', 'HR_Bob'], 'dur_scale': 120},
        {'name': 'Offer Accepted', 'prob': 0.18},
        {'name': 'Onboarding Completed', 'prob': 0.17, 'dur_scale': 4320}
    ]
    df = _simulate_process(process, n_cases, seed=seed)
    console.print(f"[green]✅ Generated HR Onboarding log ({len(df)} events)[/green]")
    if ENABLE_PROFILING or show_timing: console.print(f"[dim][Profiling] in {time.perf_counter()-t0:.4f}s[/dim]")
    return df

def generate_healthcare_event_log(n_cases: int = 500, seed: int = 42, show_timing: bool = False) -> pd.DataFrame:
    if ENABLE_PROFILING or show_timing: t0 = time.perf_counter()
    process = [
        {'name': 'Registration', 'prob': 1.0, 'resources': ['Receptionist']},
        {'name': 'Triage', 'prob': 1.0, 'resources': ['Nurse'], 'dur_scale': 30},
        {'name': 'Doctor Consultation', 'prob': 0.95, 'resources': ['Dr_Smith', 'Dr_Jones'], 'dur_scale': 60},
        {'name': 'X-Ray', 'prob': 0.4, 'resources': ['Radiology']},
        {'name': 'Blood Test', 'prob': 0.6, 'resources': ['Lab'], 'dur_scale': 120},
        {'name': 'Prescription', 'prob': 0.8, 'resources': ['Dr_Smith', 'Dr_Jones']},
        {'name': 'Discharge', 'prob': 1.0, 'resources': ['Receptionist'], 'dur_scale': 15}
    ]
    df = _simulate_process(process, n_cases, seed=seed)
    console.print(f"[green]✅ Generated Healthcare log ({len(df)} events)[/green]")
    if ENABLE_PROFILING or show_timing: console.print(f"[dim][Profiling] in {time.perf_counter()-t0:.4f}s[/dim]")
    return df

def generate_manufacturing_event_log(n_cases: int = 500, seed: int = 42, show_timing: bool = False) -> pd.DataFrame:
    if ENABLE_PROFILING or show_timing: t0 = time.perf_counter()
    process = [
        {'name': 'Order Received', 'prob': 1.0, 'resources': ['System']},
        {'name': 'Material Gathered', 'prob': 1.0, 'resources': ['Warehouse'], 'dur_scale': 240},
        {'name': 'Assembly', 'prob': 1.0, 'resources': ['Line_1', 'Line_2'], 'dur_scale': 480},
        {'name': 'Quality Check', 'prob': 1.0, 'resources': ['QC_Team'], 'dur_scale': 60},
        {'name': 'Rework', 'prob': 0.15, 'resources': ['Line_1', 'Line_2'], 'dur_scale': 240},
        {'name': 'Packaging', 'prob': 1.0, 'resources': ['Shipping_Dept'], 'dur_scale': 30},
        {'name': 'Dispatched', 'prob': 1.0, 'resources': ['Logistics']}
    ]
    df = _simulate_process(process, n_cases, seed=seed)
    console.print(f"[green]✅ Generated Manufacturing log ({len(df)} events)[/green]")
    if ENABLE_PROFILING or show_timing: console.print(f"[dim][Profiling] in {time.perf_counter()-t0:.4f}s[/dim]")
    return df

def generate_tech_support_event_log(n_cases: int = 500, seed: int = 42, show_timing: bool = False) -> pd.DataFrame:
    if ENABLE_PROFILING or show_timing: t0 = time.perf_counter()
    process = [
        {'name': 'Ticket Created', 'prob': 1.0, 'resources': ['System']},
        {'name': 'Assigned L1', 'prob': 1.0, 'resources': ['L1_Agent'], 'dur_scale': 15},
        {'name': 'L1 Investigation', 'prob': 1.0, 'resources': ['L1_Agent'], 'dur_scale': 60},
        {'name': 'Escalated to L2', 'prob': 0.3, 'resources': ['L2_Expert'], 'dur_scale': 120},
        {'name': 'L2 Investigation', 'prob': 0.3, 'resources': ['L2_Expert'], 'dur_scale': 240},
        {'name': 'Waiting for Customer', 'prob': 0.4, 'resources': ['System'], 'dur_scale': 1440},
        {'name': 'Resolved', 'prob': 0.95, 'resources': ['L1_Agent', 'L2_Expert']},
        {'name': 'Ticket Closed', 'prob': 1.0, 'resources': ['System'], 'dur_scale': 10}
    ]
    df = _simulate_process(process, n_cases, seed=seed)
    console.print(f"[green]✅ Generated Tech Support log ({len(df)} events)[/green]")
    if ENABLE_PROFILING or show_timing: console.print(f"[dim][Profiling] in {time.perf_counter()-t0:.4f}s[/dim]")
    return df

def generate_clean_ecommerce_data(n_rows: int = 10000, completion_rate: float = 0.85, include_web_data: bool = True, seed: int = 42, show_timing: bool = False) -> pd.DataFrame:
    if ENABLE_PROFILING or show_timing: t0 = time.perf_counter()
    np.random.seed(seed)
    n_cases = max(1, n_rows // 6)
    process = [
        {'name': 'Visit Homepage', 'prob': 1.0, 'resources': ['Web_Server']},
        {'name': 'Search Product', 'prob': 0.9, 'dur_scale': 5, 'resources': ['Search_Engine']},
        {'name': 'View Product Detail', 'prob': 0.8, 'dur_scale': 10, 'resources': ['Web_Server']},
        {'name': 'Add to Cart', 'prob': 0.6, 'dur_scale': 15, 'resources': ['Cart_Service']},
        {'name': 'Checkout Started', 'prob': 0.4, 'dur_scale': 5, 'resources': ['Checkout_API']},
        {'name': 'Payment Processed', 'prob': 0.4 * completion_rate, 'dur_scale': 2, 'resources': ['Payment_Gateway']},
        {'name': 'Order Confirmed', 'prob': 0.4 * completion_rate, 'dur_scale': 1, 'resources': ['Order_Service']}
    ]
    df = _simulate_process(process, n_cases, seed=seed)
    # Add e-commerce specific columns
    df['device'] = np.random.choice(['Mobile', 'Desktop', 'Tablet'], size=len(df), p=[0.6, 0.3, 0.1])
    if include_web_data:
        df['browser'] = np.random.choice(['Chrome', 'Safari', 'Edge', 'Firefox'], size=len(df), p=[0.5, 0.3, 0.1, 0.1])
        df['session_duration_sec'] = np.random.gamma(2, 60, size=len(df)).astype(int)
    console.print(f"[green]✅ Generated e-commerce event log ({len(df)} events, {n_cases} users)[/green]")
    if ENABLE_PROFILING or show_timing: console.print(f"[dim][Profiling] in {time.perf_counter()-t0:.4f}s[/dim]")
    return df