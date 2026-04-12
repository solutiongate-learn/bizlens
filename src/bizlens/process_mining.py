"""
BizLens Process Mining Module — Event Log & Business Process Analysis
Version: 2.3.2
"""

import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from rich.table import Table as RichTable
from rich.console import Console
from typing import Dict, List, Tuple, Optional
from . import ENABLE_PROFILING
from .utils import to_pandas

# Optional plotly
try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False
    go = None

console = Console()


class process_mining:
    """
    Process mining and business process analysis.
    """

    @staticmethod
    def case_metrics(event_log, case_id_col: str = 'case_id', timestamp_col: str = 'timestamp',
                     cost_col: Optional[str] = None, show_timing: bool = False) -> RichTable:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        event_log = to_pandas(event_log)
        event_log[timestamp_col] = pd.to_datetime(event_log[timestamp_col])

        agg_dict = {timestamp_col: ['min', 'max', 'count']}
        if cost_col:
            agg_dict[cost_col] = 'sum'

        case_metrics = event_log.groupby(case_id_col).agg(agg_dict).reset_index()
        case_metrics.columns = ['_'.join(map(str, col)).strip('_') for col in case_metrics.columns.values]
        case_metrics = case_metrics.rename(columns={
            f'{timestamp_col}_min': 'start_time',
            f'{timestamp_col}_max': 'end_time',
            f'{timestamp_col}_count': 'activity_count'
        })
        case_metrics['duration_hours'] = (case_metrics['end_time'] - case_metrics['start_time']).dt.total_seconds() / 3600

        table = RichTable(title="Case-Level Metrics Summary", header_style="bold blue")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right", style="magenta")
        table.add_row("Total Cases", str(len(case_metrics)))
        table.add_row("Avg Duration (hrs)", f"{case_metrics['duration_hours'].mean():.2f}")
        table.add_row("Avg Activities", f"{case_metrics['activity_count'].mean():.1f}")
        if cost_col:
            table.add_row("Avg Cost/Case", f"${case_metrics[cost_col].mean():.2f}")

        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] process_mining.case_metrics completed in {duration:.4f}s[/dim]")

        return table


    @staticmethod
    def variant_discovery(event_log, case_id_col: str = 'case_id', activity_col: str = 'activity',
                         top_n: int = 10, show_timing: bool = False):
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        event_log = to_pandas(event_log)
        variants = event_log.groupby(case_id_col)[activity_col].apply(
            lambda x: ' → '.join(x.values)
        ).value_counts()

        table = RichTable(title=f"Top {top_n} Process Variants", header_style="bold blue")
        table.add_column("Variant", style="cyan")
        table.add_column("Cases", justify="right", style="magenta")
        table.add_column("% of Total", justify="right", style="green")

        total_cases = len(event_log[case_id_col].unique())
        for i, (variant, count) in enumerate(variants.head(top_n).items(), 1):
            pct = (count / total_cases) * 100
            table.add_row(f"{i}. {variant[:60]}{'...' if len(variant) > 60 else ''}", str(count), f"{pct:.1f}%")

        console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] process_mining.variant_discovery completed in {duration:.4f}s[/dim]")

        return table, list(variants.head(top_n).index)


    @staticmethod
    def bottleneck_analysis(event_log, activity_col: str = 'activity',
                           timestamp_col: str = 'timestamp', case_id_col: str = 'case_id',
                           show_timing: bool = False) -> RichTable:
        if ENABLE_PROFILING or show_timing:
            start = time.perf_counter()

        event_log = to_pandas(event_log)
        event_log[timestamp_col] = pd.to_datetime(event_log[timestamp_col])
        event_log_sorted = event_log.sort_values([case_id_col, timestamp_col])

        waiting_times = []
        for case_id in event_log[case_id_col].unique():
            case_events = event_log_sorted[event_log_sorted[case_id_col] == case_id]
            for i in range(len(case_events) - 1):
                wait_time = (case_events.iloc[i+1][timestamp_col] - case_events.iloc[i][timestamp_col]).total_seconds() / 3600
                waiting_times.append({'activity': case_events.iloc[i][activity_col], 'wait_hours': wait_time})

        waiting_df = pd.DataFrame(waiting_times)
        if len(waiting_df) > 0:
            bottlenecks = waiting_df.groupby('activity')['wait_hours'].agg(['mean', 'max', 'count']).sort_values('mean', ascending=False)

            table = RichTable(title="Bottleneck Analysis (Waiting Times)", header_style="bold blue")
            table.add_column("Activity", style="cyan")
            table.add_column("Avg Wait (hrs)", justify="right", style="red")
            table.add_column("Max Wait (hrs)", justify="right", style="yellow")
            table.add_column("Occurrences", justify="right", style="magenta")

            for activity, row in bottlenecks.head(10).iterrows():
                severity = "🔴 Critical" if row['mean'] > 24 else "🟠 High" if row['mean'] > 8 else "🟡 Medium"
                table.add_row(activity, f"{row['mean']:.2f}", f"{row['max']:.2f}", str(int(row['count'])), severity)

            console.print(table)

        if ENABLE_PROFILING or show_timing:
            duration = time.perf_counter() - start
            console.print(f"[dim][Profiling] process_mining.bottleneck_analysis completed in {duration:.4f}s[/dim]")

        return table


    # Advanced Process Mining Methods (new in v2.2.16)
    @staticmethod
    def petri_net_from_log(event_log, case_id_col: str = 'case_id', activity_col: str = 'activity'):
        """Generate basic Petri net structure from event log."""
        df = to_pandas(event_log)
        transitions = df[activity_col].unique().tolist()
        places = [f'p{i}' for i in range(len(transitions) + 1)]
        return {
            'places': places,
            'transitions': transitions,
            'initial_marking': {places[0]: 1},
            'final_marking': {places[-1]: 1}
        }


    @staticmethod
    def alpha_algorithm(event_log, case_id_col: str = 'case_id', activity_col: str = 'activity'):
        """Simplified Alpha Algorithm for process discovery."""
        df = to_pandas(event_log)
        T = set(df[activity_col])
        direct_succession = set()
        for case in df[case_id_col].unique():
            case_log = df[df[case_id_col] == case].sort_values('timestamp' if 'timestamp' in df.columns else df.columns[0])
            activities = case_log[activity_col].tolist()
            for i in range(len(activities) - 1):
                direct_succession.add((activities[i], activities[i+1]))

        causality = {(a, b) for a, b in direct_succession if (b, a) not in direct_succession}
        start_activities = T - {b for a, b in direct_succession}
        end_activities = T - {a for a, b in direct_succession}

        return {
            'activities': list(T),
            'causality_relations': list(causality),
            'start_activities': list(start_activities),
            'end_activities': list(end_activities)
        }