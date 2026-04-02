"""
BizLens v2.2.11 Example 2: Process Mining with Event Logs
=========================================================
Self-Contained: YES (auto-install, all imports, event log generation)
Environments: Colab, VSCode, Terminal, Jupyter

Demonstrates:
- Event log auto-detection
- Case metrics (duration, activity count)
- Activity frequency analysis
- Resource utilization
- Process variant discovery
- Bottleneck analysis
- Interactive timeline visualization
"""

import subprocess
import sys

try:
    import bizlens as bl
except ImportError:
    print("Installing BizLens v2.2.11...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "bizlens==2.2.11", "-q"])
    import bizlens as bl

import matplotlib
matplotlib.use("Agg")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(f"\n{'='*70}")
print(f"BizLens v{bl.__version__} — Process Mining Example")
print(f"{'='*70}")

# ════════════════════════════════════════════════════════════════════════════
# GENERATE HR ONBOARDING EVENT LOG
# ════════════════════════════════════════════════════════════════════════════

print("\n[Step 1/5] Generating HR onboarding event log...")
event_log = bl.generate_hr_onboarding_event_log(num_cases=100, seed=42)
event_log = pd.DataFrame(event_log)

print(f"✓ Generated {len(event_log)} events for {event_log['case_id'].nunique()} cases")
print(f"  Columns: {', '.join(event_log.columns.tolist())}")
print(f"\nSample events:")
print(event_log.head(10).to_string())

# ════════════════════════════════════════════════════════════════════════════
# SMART DESCRIBE (Auto-detects event log)
# ════════════════════════════════════════════════════════════════════════════

print("\n[Step 2/5] Descriptive analytics with event log detection...")
bl.describe(event_log)

# ════════════════════════════════════════════════════════════════════════════
# PROCESS MINING ANALYSIS
# ════════════════════════════════════════════════════════════════════════════

print("\n[Step 3/5] Process mining analytics...")

print("\n" + "─" * 70)
print("CASE METRICS: Duration, Activity Count, Cost")
print("─" * 70)
bl.process_mining.case_metrics(event_log)

print("\n" + "─" * 70)
print("ACTIVITY METRICS: Frequency and Cost")
print("─" * 70)
bl.process_mining.activity_metrics(event_log, cost_col='cost' if 'cost' in event_log.columns else None)

print("\n" + "─" * 70)
print("RESOURCE ANALYSIS: Workload Distribution")
print("─" * 70)
if 'resource' in event_log.columns:
    bl.process_mining.resource_analysis(event_log)
else:
    print("(Resource column not available in this event log)")

# ════════════════════════════════════════════════════════════════════════════
# VARIANT DISCOVERY
# ════════════════════════════════════════════════════════════════════════════

print("\n[Step 4/5] Process variant discovery...")

print("\n" + "─" * 70)
print("TOP PROCESS VARIANTS (Activity Sequences)")
print("─" * 70)
variant_table, variant_list = bl.process_mining.variant_discovery(event_log, top_n=5)

print("\n" + "─" * 70)
print("BOTTLENECK ANALYSIS: Waiting Times")
print("─" * 70)
bl.process_mining.bottleneck_analysis(event_log)

# ════════════════════════════════════════════════════════════════════════════
# REWORK DETECTION
# ════════════════════════════════════════════════════════════════════════════

print("\n[Step 5/5] Rework and quality metrics...")

print("\n" + "─" * 70)
print("REWORK DETECTION: Cases with Repeated Activities")
print("─" * 70)
rework_count, rework_table = bl.process_mining.rework_detection(event_log)

# ════════════════════════════════════════════════════════════════════════════
# VISUALIZATION: TIMELINE
# ════════════════════════════════════════════════════════════════════════════

print("\nGenerating timeline visualization...")
try:
    timeline_path = bl.process_mining.timeline_visualization(event_log, top_cases=3)
    print(f"✓ Timeline saved to: {timeline_path}")
except Exception as e:
    print(f"(Timeline visualization requires plotly: pip install plotly)")

# ════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("✓ EXAMPLE 2 COMPLETE — Process Mining")
print("=" * 70)
print("\nKey Topics Covered:")
print("  ✓ Event log auto-detection")
print("  ✓ Case metrics (duration, activity count)")
print("  ✓ Activity frequency analysis")
print("  ✓ Resource workload distribution")
print("  ✓ Process variant (path) discovery")
print("  ✓ Bottleneck identification")
print("  ✓ Rework and quality detection")
print("  ✓ Interactive timeline visualization")
print("\n" + "=" * 70)
