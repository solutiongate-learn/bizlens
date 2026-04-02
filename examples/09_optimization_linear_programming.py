"""
BizLens — Example 09: Optimization (Linear Programming Deep Dive)
==================================================================
Topics covered
--------------
• prescriptive.lp()         — LP with shadow prices & feasibility plot
• prescriptive.integer_lp() — Mixed-Integer LP: integer vars & binary vars
• prescriptive.sensitivity() — Parametric analysis of objective & RHS
• Classic OR problems:
    1. Production planning (tables & chairs)
    2. Multi-resource allocation (3 products, 3 constraints)
    3. Staff scheduling (integer LP — shift coverage)
    4. Portfolio selection (binary IP — capital allocation)
    5. Sensitivity — break-even price point

Run anywhere
------------
  Google Colab : paste into a code cell and run
  VSCode / Jupyter / Terminal : python 09_optimization_linear_programming.py
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

# ── 1. Production Planning — classic LP ──────────────────────────────────────
print("="*60)
print("1. Production Planning — Tables and Chairs (classic textbook LP):")
print("""
   Factory manufactures tables and chairs:
     Profit per unit:  Table = $25,  Chair = $15
     Carpentry hours:  3T + 2C ≤ 120  hours/week
     Finishing hours:  2T + 3C ≤ 100  hours/week
   Question: How many of each to maximise weekly profit?
""")
prod = bl.prescriptive.lp(
    objective=[25, 15],
    constraints=[[3, 2], [2, 3]],
    rhs=[120, 100],
    variable_names=["Tables", "Chairs"],
    constraint_types=["<=", "<="],
    maximize=True,
    show_plot=True,
)
tables_opt = prod['variables']['Tables']
chairs_opt = prod['variables']['Chairs']
print(f"   Optimal mix: Tables = {tables_opt:.0f},  Chairs = {chairs_opt:.0f}")
print(f"   Maximum weekly profit: ${prod['objective_value']:,.2f}")
print(f"   Carpentry used: {3*tables_opt + 2*chairs_opt:.0f}/120 hrs  "
      f"({(3*tables_opt + 2*chairs_opt)/120:.0%})")
print(f"   Finishing used: {2*tables_opt + 3*chairs_opt:.0f}/100 hrs  "
      f"({(2*tables_opt + 3*chairs_opt)/100:.0%})")
if prod.get("shadow_prices"):
    print(f"   Shadow prices: {prod['shadow_prices']}")

# ── 2. Multi-resource allocation — 3 products ────────────────────────────────
print("\n" + "="*60)
print("2. Multi-Resource Allocation — 3 Products, 3 Constraints:")
print("""
   Revenue:  10x₁ + 6x₂ + 4x₃
   Machine hours:    x₁ +  x₂ +  x₃ ≤ 100
   Capital (×$10):  10x₁ + 4x₂ + 5x₃ ≤ 600
   Labour:           2x₁ + 2x₂ + 6x₃ ≤ 300
""")
resource = bl.prescriptive.lp(
    objective=[10, 6, 4],
    constraints=[
        [1,  1,  1],
        [10, 4,  5],
        [2,  2,  6],
    ],
    rhs=[100, 600, 300],
    variable_names=["Product_X", "Product_Y", "Product_Z"],
    constraint_types=["<=", "<=", "<="],
    maximize=True,
    show_plot=False,
)
print(f"   Optimal allocation: {resource['variables']}")
print(f"   Maximum revenue: ${resource['objective_value']:,.2f}")
if resource.get("shadow_prices"):
    print(f"   Shadow prices: {resource['shadow_prices']}")
    for constraint, sp in resource['shadow_prices'].items():
        if sp and sp > 0:
            print(f"     {constraint}: ${sp:.4f}/unit (this resource is binding — "
                  "investing in it increases revenue)")

# ── 3. Staff Scheduling — Integer LP ─────────────────────────────────────────
print("\n" + "="*60)
print("3. Staff Scheduling (Integer LP) — Hospital Nurses:")
print("""
   3 shifts: Morning (6am–2pm), Afternoon (2pm–10pm), Evening (10pm–6am)
   A nurse starting a shift covers that shift AND the next shift.
   Minimum nurses required: Morning ≥ 10, Afternoon ≥ 15, Evening ≥ 8
   Objective: Minimise total nurses hired.
""")
scheduling = bl.prescriptive.integer_lp(
    objective=[1, 1, 1],               # Minimise total nurses
    constraints=[
        [1, 0, 1],    # Morning coverage
        [1, 1, 0],    # Afternoon coverage
        [0, 1, 1],    # Evening coverage
    ],
    rhs=[10, 15, 8],
    constraint_types=[">=", ">=", ">="],
    integer_vars=["NursesA", "NursesB", "NursesC"],
    variable_names=["NursesA", "NursesB", "NursesC"],
    maximize=False,
)
assignments = scheduling['variables']
total_nurses = int(scheduling['objective_value'])
print(f"   Optimal staffing:")
for shift, n in assignments.items():
    print(f"     {shift} (starts {['Morning','Afternoon','Evening'][['NursesA','NursesB','NursesC'].index(shift)]}): "
          f"{int(n)} nurses")
print(f"   Total nurses hired: {total_nurses}")
print(f"   (Integer constraint ensures whole-number staffing levels ✅)")

# ── 4. Portfolio Selection — Binary IP ───────────────────────────────────────
print("\n" + "="*60)
print("4. Portfolio Selection (Binary Integer LP):")
print("   Select investments within $1M budget to maximise expected return.")
print("   Each investment is all-or-nothing (binary: invest or skip).")
investments = ["Tech ETF", "Bond Fund", "Real Estate", "Gold ETF",
               "Startup A", "Infrastructure", "Healthcare"]
exp_returns = [0.18, 0.06, 0.12, 0.08, 0.30, 0.10, 0.15]
costs_m     = [0.25, 0.40, 0.35, 0.20, 0.15, 0.45, 0.30]
max_picks   = 3

print(f"\n   Investment universe:")
for inv, ret, cost in zip(investments, exp_returns, costs_m):
    print(f"     {inv:18s}  Return={ret:.0%}  Cost=${cost:.2f}M")

portfolio = bl.prescriptive.integer_lp(
    objective=exp_returns,
    constraints=[
        costs_m,
        [1] * len(investments),   # Max 3 picks
    ],
    rhs=[1.0, max_picks],
    constraint_types=["<=", "<="],
    binary_vars=investments,
    variable_names=investments,
    maximize=True,
)
selected = [inv for inv, v in portfolio["variables"].items() if v >= 0.5]
total_invested = sum(costs_m[investments.index(inv)] for inv in selected)
total_return   = sum(exp_returns[investments.index(inv)] for inv in selected)
print(f"\n   Optimal portfolio: {selected}")
print(f"   Blended return: {portfolio['objective_value']*100:.1f}%")
print(f"   Capital invested: ${total_invested:.2f}M / $1.00M budget")
not_selected = [i for i in investments if i not in selected]
print(f"   Not selected: {not_selected}")

# ── 5. Sensitivity — break-even price ────────────────────────────────────────
print("\n" + "="*60)
print("5. Sensitivity Analysis — break-even profit contribution for Product X:")
print("   How does optimal revenue change as Product X's contribution varies?")
sens_results = bl.prescriptive.sensitivity(
    objective=[10, 6, 4],
    constraints=[[1, 1, 1], [10, 4, 5], [2, 2, 6]],
    rhs=[100, 600, 300],
    param="obj",
    param_idx=0,               # Vary Product_X coefficient
    delta_range=(2, 20),
    n_points=30,
    maximize=True,
    variable_names=["Product_X", "Product_Y", "Product_Z"],
)
print(f"   Tested obj coefficients for Product_X: $2 → $20")
print(f"   Revenue range: ${sens_results['objective'].min():.2f} to ${sens_results['objective'].max():.2f}")
# Find approximate break-even vs current solution
baseline_rev = resource['objective_value']
sens_at_current = sens_results[sens_results['param_value'].between(9.9, 10.1)]['objective']
if len(sens_at_current) > 0:
    print(f"   At current price ($10): revenue = ${sens_at_current.values[0]:.2f}")

# ── 6. LP interpretation guide ───────────────────────────────────────────────
print("\n" + "="*60)
print("6. LP key concepts and interpretation:")
print("""
  Binding vs Non-binding constraints
  ────────────────────────────────────
  Binding     → constraint is exactly met at optimum (shadow price > 0)
  Non-binding → constraint has slack (shadow price = 0)
  More of a binding resource → increases objective value

  Shadow price (dual value)
  ──────────────────────────
  = increase in objective for 1 additional unit of a constrained resource
  Example: shadow price of labour = $0.50 → hire 1 more hour → +$0.50 profit

  Integer vs Continuous LP
  ─────────────────────────
  Continuous LP : Variables can be fractional (e.g. 3.7 tables — not physical)
  Integer LP    : Variables must be whole numbers (e.g. nurses, machines)
  Binary LP     : Variables are 0/1 (yes/no decisions: invest or skip)
  MILP          : Mix of continuous and integer variables

  Feasibility
  ────────────
  Feasible region: set of all (x₁, x₂) that satisfy ALL constraints
  Optimal solution: always at a corner of the feasible region (simplex)
  Infeasible      : constraints contradict each other (no solution exists)
  Unbounded       : objective can grow forever (missing upper constraint)
""")

print("✅ Example 09 complete — Optimization & Linear Programming")
