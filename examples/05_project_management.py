"""
BizLens — Example 05: Project Management Analytics
====================================================
Topics covered
--------------
• project.gantt()    — Gantt chart with resources and progress (dates + numeric)
• project.network()  — Network diagram with Critical Path Method (CPM)
• project.pert()     — PERT analysis with uncertainty estimates
• CPM interpretation — ES, EF, LS, LF, Slack, Critical Path
• PERT statistics    — Expected duration, variance, confidence intervals

Run anywhere
------------
  Google Colab : paste into a code cell and run
  VSCode / Jupyter / Terminal : python 05_project_management.py
"""

# ── Auto-install ──────────────────────────────────────────────────────────────
import subprocess, sys

def _install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

for pkg in ["bizlens", "numpy", "pandas", "matplotlib", "networkx"]:
    try:
        __import__(pkg)
    except ImportError:
        print(f"Installing {pkg}...")
        _install(pkg)

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # Safe for Colab / headless; remove for pop-up windows
import matplotlib.pyplot as plt
import bizlens as bl

print(f"BizLens version: {bl.__version__}\n")

# ── 1. Gantt Chart — Software Development Project (calendar dates) ────────────
print("="*60)
print("1. Gantt Chart — Software Development Project (calendar dates):")
software_tasks = [
    {"task": "Requirements gathering",  "start": "2024-01-01", "end": "2024-01-07",
     "resource": "BA Team",    "progress": 100},
    {"task": "System design",           "start": "2024-01-05", "end": "2024-01-15",
     "resource": "Architects", "progress": 100},
    {"task": "Database design",         "start": "2024-01-10", "end": "2024-01-20",
     "resource": "DBAs",       "progress": 85},
    {"task": "Backend development",     "start": "2024-01-15", "end": "2024-02-15",
     "resource": "Dev Team",   "progress": 60},
    {"task": "Frontend development",    "start": "2024-01-20", "end": "2024-02-20",
     "resource": "Dev Team",   "progress": 40},
    {"task": "API integration",         "start": "2024-02-10", "end": "2024-02-25",
     "resource": "Dev Team",   "progress": 0},
    {"task": "Unit testing",            "start": "2024-02-15", "end": "2024-03-01",
     "resource": "QA Team",    "progress": 0},
    {"task": "System testing",          "start": "2024-02-25", "end": "2024-03-10",
     "resource": "QA Team",    "progress": 0},
    {"task": "User acceptance testing", "start": "2024-03-05", "end": "2024-03-18",
     "resource": "BA Team",    "progress": 0},
    {"task": "Deployment & go-live",    "start": "2024-03-18", "end": "2024-03-22",
     "resource": "DevOps",     "progress": 0},
]
gantt_df = bl.project.gantt(software_tasks, title="Software Development Gantt Chart")
print(f"   Software project: {len(software_tasks)} tasks scheduled")
print(f"   Start: 2024-01-01  |  End: 2024-03-22")

# ── 2. Gantt Chart — Construction Project (numeric day numbers) ───────────────
print("\n" + "="*60)
print("2. Gantt Chart — Construction Project (day numbers, multi-team):")
construction_tasks = [
    {"task": "Site preparation",      "start": 0,  "end": 5,  "resource": "Civil"},
    {"task": "Foundation",            "start": 3,  "end": 15, "resource": "Civil"},
    {"task": "Structural frame",      "start": 12, "end": 35, "resource": "Structural"},
    {"task": "Roof & exterior",       "start": 30, "end": 50, "resource": "Structural"},
    {"task": "Electrical wiring",     "start": 40, "end": 60, "resource": "Electrical"},
    {"task": "Plumbing",              "start": 40, "end": 58, "resource": "Plumbing"},
    {"task": "Interior finishing",    "start": 55, "end": 75, "resource": "Interior"},
    {"task": "Inspection & handover", "start": 73, "end": 80, "resource": "Civil"},
]
bl.project.gantt(construction_tasks, title="Construction Project Schedule (80-day build)")
project_duration = max(t["end"] for t in construction_tasks)
parallel_tasks = sum(1 for i, t1 in enumerate(construction_tasks)
                     for t2 in construction_tasks[i+1:]
                     if t1["start"] < t2["end"] and t2["start"] < t1["end"])
print(f"   Total project duration: {project_duration} days")
print(f"   Parallel task pairs: {parallel_tasks}")

# ── 3. CPM Network Diagram — Product Launch ───────────────────────────────────
print("\n" + "="*60)
print("3. CPM Network Diagram — Product Launch Project:")
print("   (CPM = Critical Path Method — determines minimum project duration)")
tasks_cpm = [
    {"id": "A", "name": "Market Research",    "duration": 5},
    {"id": "B", "name": "Product Design",     "duration": 8},
    {"id": "C", "name": "Prototype Build",    "duration": 6},
    {"id": "D", "name": "Testing",            "duration": 4},
    {"id": "E", "name": "Marketing Plan",     "duration": 7},
    {"id": "F", "name": "Production Setup",   "duration": 10},
    {"id": "G", "name": "Launch Campaign",    "duration": 3},
    {"id": "H", "name": "Product Launch",     "duration": 2},
]
dependencies_cpm = {
    "A": [],
    "B": ["A"],
    "C": ["B"],
    "D": ["C"],
    "E": ["A"],
    "F": ["C"],
    "G": ["E", "D"],
    "H": ["F", "G"],
}
cpm_result = bl.project.network(
    tasks=tasks_cpm,
    dependencies=dependencies_cpm,
    title="Product Launch Network (CPM)"
)
print(f"\n   Critical Path: {' → '.join(cpm_result['critical_path'])}")
print(f"   Project Duration: {cpm_result['project_duration']} days")
print(f"\n   Task slack (total float):")
for task_id, slack_val in sorted(cpm_result['slack'].items()):
    critical = "⭐ CRITICAL" if slack_val == 0 else f"  {slack_val} days float"
    task_name = next(t['name'] for t in tasks_cpm if t['id'] == task_id)
    print(f"     {task_id}: {task_name:20s}  slack={slack_val}d  {critical}")

# ── 4. CPM — IT Infrastructure migration (larger network) ────────────────────
print("\n" + "="*60)
print("4. CPM — IT Infrastructure Migration (10 tasks, multiple paths):")
tasks_it = [
    {"id": "P", "name": "Project planning",    "duration": 3},
    {"id": "A", "name": "Audit current systems","duration": 5},
    {"id": "B", "name": "Procurement",          "duration": 8},
    {"id": "C", "name": "Network setup",        "duration": 6},
    {"id": "D", "name": "Server build",         "duration": 7},
    {"id": "E", "name": "Data migration",       "duration": 10},
    {"id": "F", "name": "App deployment",       "duration": 5},
    {"id": "G", "name": "Security hardening",   "duration": 4},
    {"id": "H", "name": "User training",        "duration": 3},
    {"id": "Z", "name": "Go-live",              "duration": 1},
]
deps_it = {
    "P": [],
    "A": ["P"],
    "B": ["A"],
    "C": ["B"],
    "D": ["B"],
    "E": ["D", "C"],
    "F": ["E"],
    "G": ["F"],
    "H": ["F"],
    "Z": ["G", "H"],
}
cpm_it = bl.project.network(
    tasks=tasks_it, dependencies=deps_it,
    title="IT Migration Network (CPM)"
)
print(f"\n   Critical Path: {' → '.join(cpm_it['critical_path'])}")
print(f"   Minimum project duration: {cpm_it['project_duration']} days")
n_critical = sum(1 for v in cpm_it['slack'].values() if v == 0)
n_float    = len(tasks_it) - n_critical
print(f"   Critical tasks: {n_critical}  |  Tasks with float: {n_float}")

# ── 5. PERT Analysis — Construction with uncertainty ─────────────────────────
print("\n" + "="*60)
print("5. PERT Analysis — Construction Project (optimistic/likely/pessimistic):")
print("   PERT formula:  te = (o + 4m + p) / 6     σ² = ((p - o) / 6)²")
tasks_pert = [
    {"id": "A", "name": "Foundation",         "optimistic": 8,  "likely": 10, "pessimistic": 15},
    {"id": "B", "name": "Framing",            "optimistic": 12, "likely": 15, "pessimistic": 25},
    {"id": "C", "name": "Roofing",            "optimistic": 5,  "likely": 7,  "pessimistic": 12},
    {"id": "D", "name": "Electrical",         "optimistic": 6,  "likely": 8,  "pessimistic": 14},
    {"id": "E", "name": "Plumbing",           "optimistic": 5,  "likely": 7,  "pessimistic": 11},
    {"id": "F", "name": "Interior finishing", "optimistic": 10, "likely": 14, "pessimistic": 20},
    {"id": "G", "name": "Inspection",         "optimistic": 2,  "likely": 3,  "pessimistic": 5},
]
pert_df = bl.project.pert(tasks_pert, title="Construction PERT Analysis")

# Summary statistics using the returned DataFrame
total_te  = pert_df["Expected (te)"].sum()
total_var = pert_df["Variance (σ²)"].sum()
total_std = total_var ** 0.5

print(f"\n   Expected project duration: {total_te:.1f} days")
print(f"   Total variance: {total_var:.2f}  |  Std deviation: ±{total_std:.1f} days")
print(f"\n   Confidence intervals (Normal approximation):")
from scipy import stats as sp
z_vals = [(0.50, 0.00, "50%"), (0.80, 0.842, "80%"),
          (0.90, 1.282, "90%"), (0.95, 1.645, "95%")]
for conf, z, label in z_vals:
    upper = total_te + z * total_std
    print(f"     P(complete within {upper:.1f} days) = {label}")

# ── 6. PERT — Software project uncertainty ────────────────────────────────────
print("\n" + "="*60)
print("6. PERT — Software Sprint (agile uncertainty modelling):")
sprint_tasks = [
    {"id": "1", "name": "Feature A",      "optimistic": 2, "likely": 4,  "pessimistic": 8},
    {"id": "2", "name": "Feature B",      "optimistic": 3, "likely": 5,  "pessimistic": 10},
    {"id": "3", "name": "Bug fixes",      "optimistic": 1, "likely": 3,  "pessimistic": 7},
    {"id": "4", "name": "Code review",    "optimistic": 1, "likely": 2,  "pessimistic": 4},
    {"id": "5", "name": "Testing",        "optimistic": 2, "likely": 4,  "pessimistic": 8},
    {"id": "6", "name": "Documentation",  "optimistic": 1, "likely": 2,  "pessimistic": 5},
]
sprint_df = bl.project.pert(sprint_tasks, title="Sprint PERT Estimate")
sprint_te  = sprint_df["Expected (te)"].sum()
sprint_std = sprint_df["Variance (σ²)"].sum() ** 0.5
sprint_days = 10  # typical sprint
prob_on_time = sp.norm.cdf(sprint_days, loc=sprint_te, scale=sprint_std)
print(f"\n   Sequential (worst-case) total: {sprint_te:.1f} days ± {sprint_std:.1f}")
print(f"   P(complete within {sprint_days}-day sprint): {prob_on_time:.1%}")

# ── 7. Interpretation guide ───────────────────────────────────────────────────
print("\n" + "="*60)
print("7. CPM vs PERT — When to use which:")
print("""
  ┌─────────┬──────────────────────────────────┬────────────────────────────────┐
  │ Method  │ Best for                         │ Key output                     │
  ├─────────┼──────────────────────────────────┼────────────────────────────────┤
  │ Gantt   │ Visual scheduling + tracking     │ Timeline, resource, progress   │
  │ CPM     │ Deterministic durations          │ Critical path, float/slack     │
  │ PERT    │ Uncertain durations              │ te, σ², confidence intervals   │
  └─────────┴──────────────────────────────────┴────────────────────────────────┘

  Slack / Float = LS − ES = LF − EF
  • Zero slack  → task is on the critical path (any delay → project delay)
  • Positive slack → task has scheduling flexibility

  PERT 3-point estimate rule of thumb:
  • (pessimistic − optimistic) / 6  ≈ one standard deviation
  • Use the 90th percentile (te + 1.28σ) for realistic schedule targets
""")

print("✅ Example 05 complete — Project Management Analytics")
