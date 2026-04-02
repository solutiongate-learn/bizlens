"""
BizLens Process Mining Module — Event Log & Business Process Analysis
Version: 2.2.11
Purpose: Analyze business processes using event logs
Teaching Focus: Understanding process flows, case duration, bottlenecks, variants

Dependencies:
- pandas, numpy (data manipulation)
- plotly (interactive Gantt charts)
- rich (console output)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from rich.table import Table as RichTable
from rich.console import Console
from typing import Dict, List, Tuple, Optional

# Optional: plotly for Gantt charts (graceful fallback if not installed)
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

    **Purpose (Educational):**
    Process mining analyzes event logs to understand how processes work in practice.
    It answers questions like:
    - What variants (paths) do cases take through the process?
    - How long does each case typically take?
    - Which activities take the longest?
    - Who is overloaded with work?
    - Where are the bottlenecks?

    **Key Concepts:**
    - Case: A single instance (order, claim, patient, employee)
    - Activity: A step in the process (order placed, approved, shipped)
    - Resource: Who/what performed the activity (person, system)
    - Timestamp: When the activity occurred
    """

    @staticmethod
    def case_metrics(event_log: pd.DataFrame, case_id_col: str = 'case_id',
                    timestamp_col: str = 'timestamp',
                    cost_col: Optional[str] = None) -> RichTable:
        """
        Analyze metrics at the case level (duration, cost, activity count).

        **What this does (Educational):**
        Shows statistics for each case: how long it took, how many activities,
        and optionally the cost. Useful for identifying slow or expensive cases.

        **Parameters:**
        -----------
        event_log : pd.DataFrame
            Event log with case, timestamp, and optional cost columns
        case_id_col : str
            Column name for case identifier
        timestamp_col : str
            Column name for timestamp
        cost_col : str, optional
            Column name for cost data

        **Returns:**
        --------
        RichTable
            Case-level metrics
        """
        # Ensure timestamp is datetime
        event_log[timestamp_col] = pd.to_datetime(event_log[timestamp_col])

        # Calculate case metrics
        # LEARNING POINT: Group by case to get case-level metrics
        case_metrics = event_log.groupby(case_id_col).agg({
            timestamp_col: ['min', 'max', 'count'],
            cost_col: 'sum' if cost_col else 'count'
        }).reset_index()

        # Flatten column names
        case_metrics.columns = ['case_id', 'start_time', 'end_time', 'activity_count', 'cost']

        # Calculate duration
        case_metrics['duration_hours'] = (
            (case_metrics['end_time'] - case_metrics['start_time']).dt.total_seconds() / 3600
        )

        # Create table showing summary statistics
        table = RichTable(title="Case-Level Metrics Summary",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right", style="magenta")

        table.add_row("Total Cases", str(len(case_metrics)))
        table.add_row("Avg Duration", f"{case_metrics['duration_hours'].mean():.2f} hours")
        table.add_row("Min Duration", f"{case_metrics['duration_hours'].min():.2f} hours")
        table.add_row("Max Duration", f"{case_metrics['duration_hours'].max():.2f} hours")
        table.add_row("Avg Activities", f"{case_metrics['activity_count'].mean():.1f}")
        if cost_col:
            table.add_row("Total Cost", f"${case_metrics['cost'].sum():.2f}")
            table.add_row("Avg Cost/Case", f"${case_metrics['cost'].mean():.2f}")

        console.print(table)

        return table

    @staticmethod
    def activity_metrics(event_log: pd.DataFrame,
                        activity_col: str = 'activity',
                        timestamp_col: str = 'timestamp',
                        cost_col: Optional[str] = None) -> RichTable:
        """
        Analyze metrics at the activity level (frequency, duration, cost).

        **What this does (Educational):**
        Shows which activities occur most frequently, how long they take,
        and their cost. Helps identify high-impact activities.

        **Parameters:**
        -----------
        event_log : pd.DataFrame
            Event log with activity and timestamp columns
        activity_col : str
            Column name for activity
        timestamp_col : str
            Column name for timestamp
        cost_col : str, optional
            Column name for cost

        **Returns:**
        --------
        RichTable
            Activity-level analysis
        """
        event_log[timestamp_col] = pd.to_datetime(event_log[timestamp_col])

        # Count occurrences and calculate metrics
        # LEARNING POINT: Group by activity to see what's most frequent
        activity_stats = event_log.groupby(activity_col).agg({
            activity_col: 'count',  # frequency
            cost_col: 'sum' if cost_col else activity_col
        }).reset_index()

        activity_stats.columns = ['activity', 'frequency', 'cost']
        activity_stats['percentage'] = (activity_stats['frequency'] / activity_stats['frequency'].sum() * 100).round(2)
        activity_stats = activity_stats.sort_values('frequency', ascending=False)

        # Create table
        table = RichTable(title="Activity-Level Metrics",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Activity", style="cyan")
        table.add_column("Count", justify="right", style="magenta")
        table.add_column("% of Total", justify="right", style="green")
        if cost_col:
            table.add_column("Cost", justify="right", style="yellow")

        for _, row in activity_stats.head(15).iterrows():
            row_data = [
                row['activity'],
                str(int(row['frequency'])),
                f"{row['percentage']:.1f}%"
            ]
            if cost_col:
                row_data.append(f"${row['cost']:.2f}")
            table.add_row(*row_data)

        console.print(table)

        return table

    @staticmethod
    def resource_analysis(event_log: pd.DataFrame,
                         resource_col: str = 'resource',
                         activity_col: str = 'activity') -> RichTable:
        """
        Analyze resource utilization (who does what, workload distribution).

        **What this does (Educational):**
        Shows which resources (people, systems) performed which activities,
        and workload distribution. Identifies overloaded or underutilized resources.

        **Parameters:**
        -----------
        event_log : pd.DataFrame
            Event log with resource and activity columns
        resource_col : str
            Column name for resource
        activity_col : str
            Column name for activity

        **Returns:**
        --------
        RichTable
            Resource workload analysis
        """
        # Calculate workload per resource
        # LEARNING POINT: Workload distribution shows if resources are balanced
        resource_workload = event_log[resource_col].value_counts()

        table = RichTable(title="Resource Utilization",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Resource", style="cyan")
        table.add_column("Activities", justify="right", style="magenta")
        table.add_column("% of Total", justify="right", style="green")
        table.add_column("Workload", style="yellow")

        total = resource_workload.sum()
        for resource, count in resource_workload.head(10).items():
            pct = (count / total) * 100
            # Visual workload indicator
            workload_bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            table.add_row(
                str(resource),
                str(int(count)),
                f"{pct:.1f}%",
                workload_bar
            )

        console.print(table)

        # Show activity breakdown for top resource
        if len(resource_workload) > 0:
            top_resource = resource_workload.index[0]
            top_resource_activities = event_log[event_log[resource_col] == top_resource][activity_col].value_counts()
            console.print(f"\n[cyan]Top resource ({top_resource}) activities:[/cyan]")
            for activity, count in top_resource_activities.head(5).items():
                console.print(f"  • {activity}: {count}")

        return table

    @staticmethod
    def variant_discovery(event_log: pd.DataFrame,
                         case_id_col: str = 'case_id',
                         activity_col: str = 'activity',
                         top_n: int = 10) -> Tuple[RichTable, List[str]]:
        """
        Discover most common process variants (activity sequences).

        **What this does (Educational):**
        Shows the different paths (sequences of activities) that cases can take.
        Most processes have only a few dominant variants, with many rare paths.

        **Parameters:**
        -----------
        event_log : pd.DataFrame
            Event log with case and activity columns
        case_id_col : str
            Column name for case
        activity_col : str
            Column name for activity
        top_n : int
            Number of top variants to show

        **Returns:**
        --------
        Tuple[RichTable, List[str]]
            Variants table and list of top variant sequences
        """
        # Create variants: sequence of activities per case
        # LEARNING POINT: Variant = sequence of activities for one case
        variants = event_log.groupby(case_id_col)[activity_col].apply(
            lambda x: ' → '.join(x.values)
        ).value_counts()

        # Create table
        table = RichTable(title=f"Top {top_n} Process Variants",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Variant", style="cyan")
        table.add_column("Cases", justify="right", style="magenta")
        table.add_column("% of Total", justify="right", style="green")

        total_cases = len(event_log[case_id_col].unique())
        variant_list = []

        for i, (variant, count) in enumerate(variants.head(top_n).items(), 1):
            pct = (count / total_cases) * 100
            table.add_row(
                f"{i}. {variant[:60]}{'...' if len(variant) > 60 else ''}",
                str(count),
                f"{pct:.1f}%"
            )
            variant_list.append(variant)

        # Add summary row
        shown_pct = variants.head(top_n).sum() / total_cases * 100
        other_pct = 100 - shown_pct
        table.add_row(
            f"[Other {len(variants) - top_n} variants]",
            str(total_cases - variants.head(top_n).sum()),
            f"{other_pct:.1f}%"
        )

        console.print(table)

        return table, variant_list

    @staticmethod
    def timeline_visualization(event_log: pd.DataFrame,
                              case_id_col: str = 'case_id',
                              activity_col: str = 'activity',
                              timestamp_col: str = 'timestamp',
                              top_cases: int = 5) -> str:
        """
        Create interactive Gantt chart timeline of top cases.

        **What this does (Educational):**
        Visualizes the timeline of cases showing when each activity occurred.
        Useful for identifying bottlenecks and understanding case flow.

        **Parameters:**
        -----------
        event_log : pd.DataFrame
            Event log with case, activity, and timestamp columns
        case_id_col, activity_col, timestamp_col : str
            Column names for case, activity, timestamp
        top_cases : int
            Number of cases to visualize

        **Returns:**
        --------
        str
            Path to saved HTML visualization

        **Note:**
        Requires plotly to be installed. Install with: pip install plotly
        """
        if not HAS_PLOTLY:
            console.print("[yellow]⚠️ Plotly not installed. Install with: pip install plotly[/yellow]")
            return "/tmp/timeline_unavailable.html"

        event_log[timestamp_col] = pd.to_datetime(event_log[timestamp_col])

        # Get top cases by duration
        case_duration = event_log.groupby(case_id_col)[timestamp_col].agg(['min', 'max'])
        case_duration['duration'] = case_duration['max'] - case_duration['min']
        top_case_ids = case_duration.nlargest(top_cases, 'duration').index.tolist()

        # Filter to top cases
        viz_data = event_log[event_log[case_id_col].isin(top_case_ids)].copy()
        viz_data = viz_data.sort_values([case_id_col, timestamp_col])

        # Create Gantt chart
        # LEARNING POINT: Gantt charts show temporal sequence of activities
        fig = go.Figure()

        for case_id in top_case_ids:
            case_activities = viz_data[viz_data[case_id_col] == case_id].sort_values(timestamp_col)

            for i, (_, row) in enumerate(case_activities.iterrows()):
                # Duration from this activity to next (or end)
                if i < len(case_activities) - 1:
                    next_time = case_activities.iloc[i + 1][timestamp_col]
                    duration = next_time - row[timestamp_col]
                else:
                    duration = timedelta(hours=1)  # Dummy duration for last activity

                fig.add_trace(go.Bar(
                    x=[duration],
                    y=[str(case_id)],
                    name=row[activity_col],
                    orientation='h',
                    hovertemplate=f"<b>{row[activity_col]}</b><br>Duration: " +
                                 f"{duration}<br>Case: {case_id}<extra></extra>",
                    marker=dict(line=dict(width=0.5))
                ))

        fig.update_layout(
            title=f"Process Timeline — Top {top_cases} Cases by Duration",
            xaxis_title="Duration",
            yaxis_title="Case ID",
            barmode='stack',
            height=300 + (top_cases * 30),
            showlegend=True
        )

        output_path = '/tmp/process_timeline.html'
        fig.write_html(output_path)
        console.print(f"[dim]Timeline saved to {output_path}[/dim]")

        return output_path

    @staticmethod
    def bottleneck_analysis(event_log: pd.DataFrame,
                           activity_col: str = 'activity',
                           timestamp_col: str = 'timestamp',
                           case_id_col: str = 'case_id') -> RichTable:
        """
        Identify bottleneck activities (slow or high-frequency).

        **What this does (Educational):**
        Bottlenecks are activities that slow down the overall process.
        Can be due to long duration or many cases waiting.

        **Parameters:**
        -----------
        event_log : pd.DataFrame
            Event log with activity and timestamp columns
        activity_col : str
            Column name for activity
        timestamp_col : str
            Column name for timestamp
        case_id_col : str
            Column name for case

        **Returns:**
        --------
        RichTable
            Bottleneck analysis
        """
        event_log[timestamp_col] = pd.to_datetime(event_log[timestamp_col])

        # Calculate time between consecutive activities
        # LEARNING POINT: Waiting time = time between end of one activity and start of next
        event_log_sorted = event_log.sort_values([case_id_col, timestamp_col])

        # For each case, calculate waiting times
        waiting_times = []
        for case_id in event_log[case_id_col].unique():
            case_events = event_log_sorted[event_log_sorted[case_id_col] == case_id]
            for i in range(len(case_events) - 1):
                current_time = case_events.iloc[i][timestamp_col]
                next_time = case_events.iloc[i + 1][timestamp_col]
                current_activity = case_events.iloc[i][activity_col]
                wait_time = (next_time - current_time).total_seconds() / 3600  # in hours
                waiting_times.append({
                    'activity': current_activity,
                    'wait_hours': wait_time
                })

        waiting_df = pd.DataFrame(waiting_times)

        if len(waiting_df) > 0:
            bottlenecks = waiting_df.groupby('activity')['wait_hours'].agg(['mean', 'max', 'count']).sort_values('mean', ascending=False)

            table = RichTable(title="Bottleneck Analysis (Waiting Times)",
                             show_header=True,
                             header_style="bold blue")
            table.add_column("Activity", style="cyan")
            table.add_column("Avg Wait (hrs)", justify="right", style="red")
            table.add_column("Max Wait (hrs)", justify="right", style="yellow")
            table.add_column("Occurrences", justify="right", style="magenta")
            table.add_column("Severity", style="green")

            for activity, row in bottlenecks.head(10).iterrows():
                severity = "🔴 Critical" if row['mean'] > 24 else "🟠 High" if row['mean'] > 8 else "🟡 Medium" if row['mean'] > 1 else "✓ Low"
                table.add_row(
                    activity,
                    f"{row['mean']:.2f}",
                    f"{row['max']:.2f}",
                    str(int(row['count'])),
                    severity
                )

            console.print(table)
        else:
            console.print("[yellow]No waiting time data available[/yellow]")

        return table

    @staticmethod
    def rework_detection(event_log: pd.DataFrame,
                        case_id_col: str = 'case_id',
                        activity_col: str = 'activity') -> Tuple[int, RichTable]:
        """
        Detect cases with rework (repeated activities).

        **What this does (Educational):**
        Rework = when a case goes back to an earlier activity (repair, rejection).
        Indicates quality issues or complex decision logic.

        **Parameters:**
        -----------
        event_log : pd.DataFrame
            Event log with case and activity columns
        case_id_col : str
            Column name for case
        activity_col : str
            Column name for activity

        **Returns:**
        --------
        Tuple[int, RichTable]
            Count of rework cases and analysis table
        """
        rework_cases = []

        # LEARNING POINT: Rework = activity occurs > 1 time in same case
        for case_id in event_log[case_id_col].unique():
            case_activities = event_log[event_log[case_id_col] == case_id][activity_col].tolist()

            # Count activities
            activity_counts = pd.Series(case_activities).value_counts()

            # Check for rework
            if (activity_counts > 1).any():
                rework_activities = activity_counts[activity_counts > 1]
                rework_cases.append({
                    'case_id': case_id,
                    'rework_activities': ', '.join(rework_activities.index),
                    'total_activities': len(case_activities)
                })

        rework_df = pd.DataFrame(rework_cases)
        rework_count = len(rework_df)
        rework_pct = (rework_count / len(event_log[case_id_col].unique())) * 100

        table = RichTable(title=f"Rework Detection ({rework_pct:.1f}% of cases)",
                         show_header=True,
                         header_style="bold blue")
        table.add_column("Case ID", style="cyan")
        table.add_column("Rework Activities", style="red")
        table.add_column("Total Activities", justify="right", style="magenta")

        for _, row in rework_df.head(10).iterrows():
            table.add_row(
                str(row['case_id']),
                row['rework_activities'],
                str(int(row['total_activities']))
            )

        if rework_count > 10:
            table.add_row(f"[...{rework_count - 10} more]", "", "")

        console.print(table)

        return rework_count, table

    @staticmethod
    def transition_matrix(event_log: pd.DataFrame,
                         case_id_col: str = 'case_id',
                         activity_col: str = 'activity') -> Tuple[pd.DataFrame, RichTable]:
        """
        Create activity transition matrix (which activities follow which).

        **What this does (Educational):**
        Shows the flow between activities: "After Activity A, what happens next?"
        Useful for understanding process structure and finding loops.

        **Parameters:**
        -----------
        event_log : pd.DataFrame
            Event log with case and activity columns
        case_id_col : str
            Column name for case
        activity_col : str
            Column name for activity

        **Returns:**
        --------
        Tuple[pd.DataFrame, RichTable]
            Transition matrix and formatted table
        """
        # Build transitions
        # LEARNING POINT: Track activity-to-activity transitions
        transitions = []

        event_log_sorted = event_log.sort_values([case_id_col, 'timestamp'] if 'timestamp' in event_log.columns else case_id_col)

        for case_id in event_log[case_id_col].unique():
            case_activities = event_log_sorted[event_log_sorted[case_id_col] == case_id][activity_col].tolist()
            for i in range(len(case_activities) - 1):
                transitions.append({
                    'from': case_activities[i],
                    'to': case_activities[i + 1]
                })

        transitions_df = pd.DataFrame(transitions)

        if len(transitions_df) > 0:
            # Create transition matrix
            transition_matrix = pd.crosstab(transitions_df['from'], transitions_df['to'])

            # Show top transitions
            table = RichTable(title="Activity Transitions",
                             show_header=True,
                             header_style="bold blue")
            table.add_column("From Activity", style="cyan")
            table.add_column("To Activity", style="magenta")
            table.add_column("Count", justify="right", style="green")

            for _, row in transitions_df.value_counts().head(15).items():
                table.add_row(row[0], row[1], str(transitions_df.value_counts()[row]))

            console.print(table)

            return transition_matrix, table
        else:
            return pd.DataFrame(), RichTable()
