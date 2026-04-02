"""
BizLens — Example 08: Prescriptive Analytics & Operations Research
===================================================================
Topics covered
--------------
• prescriptive.packages()       — OR ecosystem overview
• prescriptive.lp()             — Linear Programming with shadow prices
• prescriptive.integer_lp()     — MILP / Integer Programming (binary & integer)
• prescriptive.transportation() — Transportation problem (min shipping cost)
• prescriptive.assignment()     — Assignment problem (Hungarian method)
• prescriptive.sensitivity()    — RHS and objective coefficient sensitivity
• optimize.linear_program()     — Core LP wrapper (low-level)

Classic problems covered
------------------------
  Product mix, diet optimisation, capital budgeting, knapsack,
  transportation, assignment, sensitivity analysis

Run anywhere
------------
  Google Colab : paste into a code cell and run
  VSCode / Jupyter / Terminal : python 08_prescriptive_analytics.py
"""

# ── Auto-install ──────────────────────────────────────────────────────────────
import subprocess, sys

def _install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

for pkg in ["bizlens", "numpy", "pandas", "matplotlib"]:
    try:
        __import__(pkg)
    except ImportError:
        print(f"Installing {pkg}...")
        _install(pkg)

# PuLP is required for LP/MILP optimisation
try:
    import pulp  # noqa: F401
except ImportError:
    print("Installing PuLP (LP solver)...")
    _install("PuLP")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # Safe for Colab / headless; remove for pop-up windows
import matplotlib.pyplot as plt
import bizlens as bl

print(f"BizLens version: {bl.__version__}\n")

# ── 0. OR Ecosystem overview ──────────────────────────────────────────────────
print("="*60)
print("0. Operations Research & Optimization Ecosystem:")
bl.prescriptive.packages()

# ── 1. LP — Product Mix Optimisation ─────────────────────────────────────────
print("\n" + "="*60)
print("1. LP — Product Mix Optimisation (maximise profit):")
print("   Profit: 5x₁ + 4x₂    (Product A @ $5, Product B @ $4)")
print("   Constraints:  6x₁ + 4x₂ ≤ 24 (labour hours)")
print("                  x₁ + 2x₂ ≤  6 (materials)")
lp_result = bl.prescriptive.lp(
    objective=[5, 4],
    constraints=[[6, 4], [1, 2]],
    rhs=[24, 6],
    variable_names=["ProductA", "ProductB"],
    constraint_types=["<=", "<="],
    maximize=True,
    show_plot=True,
)
print(f"\n   Optimal: ProductA = {lp_result['variables']['ProductA']:.1f}  "
      f"ProductB = {lp_result['variables']['ProductB']:.1f}")
print(f"   Maximum Profit: ${lp_result['objective_value']:.2f}")
if lp_result.get("shadow_prices"):
    print(f"   Shadow prices (dual values): {lp_result['shadow_prices']}")
    print("   → Shadow price = extra profit for 1 more unit of that constraint")

# ── 2. LP — Diet / Cost Minimisation ─────────────────────────────────────────
print("\n" + "="*60)
print("2. LP — Diet Cost Minimisation:")
print("   Minimise: 3x₁ + 5x₂ + 2x₃  (cost per serving)")
print("   Nutritional minimums:  Protein ≥ 8,  Vitamins ≥ 6,  Calories ≥ 9")
diet = bl.prescriptive.lp(
    objective=[3, 5, 2],
    constraints=[
        [2, 1, 1],   # Protein
        [1, 1, 2],   # Vitamins
        [1, 3, 1],   # Calories
    ],
    rhs=[8, 6, 9],
    variable_names=["Food_A", "Food_B", "Food_C"],
    constraint_types=[">=", ">=", ">="],
    maximize=False,
    show_plot=False,
)
print(f"\n   Minimum daily cost: ${diet['objective_value']:.4f}")
print(f"   Optimal servings: {diet['variables']}")

# ── 3. MILP — Capital Budgeting (Knapsack) ────────────────────────────────────
print("\n" + "="*60)
print("3. MILP — Capital Budgeting (project selection within $500K budget):")
projects = ["CRM system", "New factory", "R&D lab", "Marketing campaign", "ERP upgrade"]
npvs    = [120, 310,  85,  60, 180]   # NPV in $000s
budgets = [150, 400, 120,  80, 220]   # Cost in $000s
total_budget = 500

print(f"\n   Projects available:")
for p, n, b in zip(projects, npvs, budgets):
    print(f"     {p:22s}  NPV=${n}K  Cost=${b}K  ROI={n/b:.2f}")

milp = bl.prescriptive.integer_lp(
    objective=npvs,
    constraints=[budgets],
    rhs=[total_budget],
    binary_vars=projects,
    variable_names=projects,
    maximize=True,
)
selected = [p for p, v in milp["variables"].items() if v >= 0.5]
total_spend = sum(budgets[i] for i, p in enumerate(projects) if p in selected)
total_npv   = sum(npvs[i]   for i, p in enumerate(projects) if p in selected)
print(f"\n   ✅ Selected projects: {selected}")
print(f"   Total NPV: ${total_npv}K  |  Budget used: ${total_spend}K / ${total_budget}K")
print(f"   Budget utilisation: {total_spend/total_budget:.0%}")

# ── 4. Transportation Problem ─────────────────────────────────────────────────
print("\n" + "="*60)
print("4. Transportation Problem — Warehouse to Retail (minimise shipping cost):")
print("   3 warehouses, 4 stores — find optimal routing")
supply_labels = ["Warehouse A", "Warehouse B", "Warehouse C"]
demand_labels = ["Store 1",     "Store 2",     "Store 3",     "Store 4"]
supply_vals   = [300, 400, 500]
demand_vals   = [250, 350, 400, 200]
cost_matrix   = [[2, 3, 1, 5], [4, 1, 3, 2], [3, 5, 2, 4]]

print(f"\n   Supply: {dict(zip(supply_labels, supply_vals))}")
print(f"   Demand: {dict(zip(demand_labels, demand_vals))}")
print(f"   Total supply: {sum(supply_vals)}  |  Total demand: {sum(demand_vals)}")

transport = bl.prescriptive.transportation(
    supply=supply_vals,
    demand=demand_vals,
    costs=cost_matrix,
    supply_names=supply_labels,
    demand_names=demand_labels,
)
print(f"\n   Minimum total shipping cost: ${transport['total_cost']:,.2f}")

# ── 5. Assignment Problem ─────────────────────────────────────────────────────
print("\n" + "="*60)
print("5. Assignment Problem — Assign Engineers to Projects (Hungarian method):")
print("   One engineer per project. Minimise total completion days.")
agent_names = ["Alice", "Bob", "Carol", "Dave"]
task_names  = ["Project Alpha", "Project Beta", "Project Gamma", "Project Delta"]
cost_matrix_assign = [
    [15, 18, 20, 25],   # Alice
    [20, 12, 22, 18],   # Bob
    [25, 20, 10, 15],   # Carol
    [18, 25, 15, 12],   # Dave
]
print(f"\n   Cost matrix (days to complete):")
header = f"   {'':8s}" + "".join(f"{t:>14s}" for t in task_names)
print(header)
for agent, row in zip(agent_names, cost_matrix_assign):
    print(f"   {agent:8s}" + "".join(f"{c:>14d}" for c in row))

assignment = bl.prescriptive.assignment(
    cost_matrix=cost_matrix_assign,
    agent_names=agent_names,
    task_names=task_names,
    maximize=False,
)
print(f"\n   Optimal assignments: {assignment['assignments']}")
print(f"   Total completion time: {assignment['total']} days")
naive_total = sum(min(row) for row in cost_matrix_assign)
print(f"   Naive (each picks easiest): {naive_total} days  (same as optimal here)")

# ── 6. Sensitivity — RHS variation ────────────────────────────────────────────
print("\n" + "="*60)
print("6. Sensitivity Analysis — vary labour hours (constraint RHS):")
print("   Question: How does optimal profit change as labour supply varies?")
sens = bl.prescriptive.sensitivity(
    objective=[5, 4],
    constraints=[[6, 4], [1, 2]],
    rhs=[24, 6],
    param="rhs",
    param_idx=0,               # Vary constraint 1 (labour)
    delta_range=(10, 40),      # Test 10 to 40 labour hours
    n_points=30,
    maximize=True,
    variable_names=["ProductA", "ProductB"],
)
print(f"   Tested {len(sens)} labour-hour scenarios (10 → 40 hours)")
print(f"   Profit range: ${sens['objective'].min():.2f}  to  ${sens['objective'].max():.2f}")
shadow_est = (sens['objective'].max() - sens['objective'].min()) / (40 - 10)
print(f"   Approximate shadow price of labour: ${shadow_est:.4f}/hour")

# ── 7. Sensitivity — objective coefficient variation ──────────────────────────
print("\n" + "="*60)
print("7. Sensitivity — vary Product A profit contribution:")
print("   Question: At what price does the optimal mix change?")
sens2 = bl.prescriptive.sensitivity(
    objective=[5, 4],
    constraints=[[6, 4], [1, 2]],
    rhs=[24, 6],
    param="obj",
    param_idx=0,               # Vary coefficient of ProductA
    delta_range=(1, 10),
    n_points=20,
    maximize=True,
    variable_names=["ProductA", "ProductB"],
)
print(f"   Tested profit contributions $1 → $10 for Product A")
print(f"   Objective value range: ${sens2['objective'].min():.2f} to ${sens2['objective'].max():.2f}")

# ── 8. Prescriptive vs Predictive ─────────────────────────────────────────────
print("\n" + "="*60)
print("8. The Analytics Pyramid — where prescriptive fits:")
print("""
  Level 4: Prescriptive  — "What SHOULD we do?"  ← You are here
  ─────────────────────────────────────────────────────────────
  Linear Programming (LP)        : Continuous decisions, linear constraints
  Mixed-Integer LP (MILP)        : Integer/binary decisions (yes/no choices)
  Transportation / Assignment    : Special-structure network problems
  Sensitivity Analysis           : How robust is the optimal solution?

  Level 3: Predictive   — "What WILL happen?"
  Level 2: Diagnostic   — "WHY did it happen?"
  Level 1: Descriptive  — "WHAT happened?"

  OR Solver Ecosystem:
  ────────────────────
  PuLP       : Free, Python-native LP/MILP (CBC solver)
  PyOMO      : Modelling language for complex OR
  OR-Tools   : Google's CP-SAT and network flow solvers
  SciPy      : linprog / milp for quick unconstrained problems
  Gurobi     : Commercial grade, fastest (requires licence)
""")

print("✅ Example 08 complete — Prescriptive Analytics & Operations Research")
print("\n💡 Also explore: bl.optimize.linear_program() for the low-level LP wrapper.")
