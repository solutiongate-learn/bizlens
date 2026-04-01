"""
BizLens — Example 05: Project Management Analytics
====================================================
Covers:
  • project.gantt()    — Gantt chart with resources and progress
  • project.network()  — Network diagram with Critical Path Method (CPM)
  • project.pert()     — PERT analysis with uncertainty estimates

Run:   python 05_project_management.py
       pip install bizlens networkx
"""

import bizlens as bl

# ──────────────────────────────────────────────────────────────────────────────
# 1. Gantt Chart — Software Development Project
# ──────────────────────────────────────────────────────────────────────────────
print("="*60)
print("1. Gantt Chart — Software Development Project:")
software_tasks = [
    {"task": "Requirements gathering",  "start": "2024-01-01", "end": "2024-01-07",  "resource": "BA Team",    "progress": 100},
    {"task": "System design",           "start": "2024-01-05", "end": "2024-01-15",  "resource": "Architects", "progress": 100},
    {"task": "Database design",         "start": "2024-01-10", "end": "2024-01-20",  "resource": "DBAs",       "progress": 85},
    {"task": "Backend development",     "start": "2024-01-15", "end": "2024-02-15",  "resource": "Dev Team",   "progress": 60},
    {"task": "Frontend development",    "start": "2024-01-20", "end": "2024-02-20",  "resource": "Dev Team",   "progress": 40},
    {"task": "API integration",         "start": "2024-02-10", "end": "2024-02-25",  "resource": "Dev Team",   "progress": 0},
    {"task": "Unit testing",            "start": "2024-02-15", "end": "2024-03-01",  "resource": "QA Team",    "progress": 0},
    {"task": "System testing",          "start": "2024-02-25", "end": "2024-03-10",  "resource": "QA Team",    "progress": 0},
    {"task": "User acceptance testing", "start": "2024-03-05", "end": "2024-03-18",  "resource": "BA Team",    "progress": 0},
    {"task": "Deployment & go-live",    "start": "2024-03-18", "end": "2024-03-22",  "resource": "DevOps",     "progress": 0},
]
gantt_df = bl.project.gantt(software_tasks, title="Software Development Gantt Chart")

# ──────────────────────────────────────────────────────────────────────────────
# 2. Gantt Chart — Construction Project (numeric days)
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("2. Gantt Chart — Construction Project (day numbers):")
construction_tasks = [
    {"task": "Site preparation",   "start": 0,  "end": 5,  "resource": "Civil"},
    {"task": "Foundation",         "start": 3,  "end": 15, "resource": "Civil"},
    {"task": "Structural frame",   "start": 12, "end": 35, "resource": "Structural"},
    {"task": "Roof & exterior",    "start": 30, "end": 50, "resource": "Structural"},
    {"task": "Electrical wiring",  "start": 40, "end": 60, "resource": "Electrical"},
    {"task": "Plumbing",           "start": 40, "end": 58, "resource": "Plumbing"},
    {"task": "Interior finishing", "start": 55, "end": 75, "resource": "Interior"},
    {"task": "Inspection & handover","start": 73,"end": 80,"resource": "Civil"},
]
bl.project.gantt(construction_tasks, title="Construction Project Schedule")

# ──────────────────────────────────────────────────────────────────────────────
# 3. Network Diagram — Critical Path Method (CPM)
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("3. CPM Network Diagram — Product Launch Project:")
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
print(f"   Slack per task: {cpm_result['slack']}")

# ──────────────────────────────────────────────────────────────────────────────
# 4. PERT Analysis — with uncertainty estimates
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("4. PERT Analysis — construction project with uncertainty:")
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

# Print summary
total_te  = pert_df["Expected (te)"].sum()
total_std = pert_df["Variance (σ²)"].sum() ** 0.5
print(f"\n   Expected project duration: {total_te:.1f} days")
print(f"   Standard deviation: ±{total_std:.1f} days")
print(f"   90th percentile estimate: {total_te + 1.28*total_std:.1f} days")

print("\n✅ Example 05 complete.")
