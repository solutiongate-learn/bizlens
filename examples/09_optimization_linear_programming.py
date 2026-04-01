"""
BizLens — Example 09: Optimization (Linear Programming)
=========================================================
Covers:
  • optimize.linear_program() — Core LP wrapper (PuLP)
  • prescriptive.lp()         — Enhanced LP with shadow prices & feasibility plot
  • prescriptive.integer_lp() — Mixed-Integer Linear Programming

Classic OR problems:
  1. Production planning
  2. Diet / nutritional optimisation
  3. Staff scheduling (integer)
  4. Facility location (binary)

Run:   python 09_optimization_linear_programming.py
       pip install bizlens PuLP
"""

import bizlens as bl

# ──────────────────────────────────────────────────────────────────────────────
# 1. Production Planning — classic LP
#    Factory makes tables and chairs.
#    Profit: Table=$25, Chair=$15
#    Constraints:
#      Carpentry: 3T + 2C ≤ 120  hours
#      Finishing: 2T + 3C ≤ 100  hours
# ──────────────────────────────────────────────────────────────────────────────
print("="*60)
print("1. Production Planning — Tables and Chairs:")
prod = bl.prescriptive.lp(
    objective=[25, 15],
    constraints=[[3, 2], [2, 3]],
    rhs=[120, 100],
    variable_names=["Tables", "Chairs"],
    maximize=True,
    show_plot=True,
)
print(f"   Optimal: Tables={prod['variables']['Tables']}, Chairs={prod['variables']['Chairs']}")
print(f"   Max profit: ${prod['objective_value']:,.2f}")

# ──────────────────────────────────────────────────────────────────────────────
# 2. Resource Allocation — 3 products, 3 resource constraints
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("2. Resource Allocation — 3 Products:")
resource = bl.prescriptive.lp(
    objective=[10, 6, 4],
    constraints=[
        [1, 1, 1],          # Machine hours
        [10, 4, 5],         # Capital
        [2, 2, 6],          # Labour
    ],
    rhs=[100, 600, 300],
    variable_names=["Product_X", "Product_Y", "Product_Z"],
    constraint_types=["<=", "<=", "<="],
    maximize=True,
    show_plot=False,
)
print(f"   Allocation: {resource['variables']}")
print(f"   Max revenue: {resource['objective_value']}")
print(f"   Shadow prices: {resource['shadow_prices']}")

# ──────────────────────────────────────────────────────────────────────────────
# 3. Staff Scheduling — Integer LP
#    Hospital needs minimum nurses per shift
#    Nurse works 2 consecutive shifts. Minimise total nurses hired.
#    Shifts: Morning, Afternoon, Evening (each 8 hrs)
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("3. Staff Scheduling (Integer LP):")
# x1 = nurses starting in Morning, x2 = Afternoon, x3 = Evening
# Availability matrix: nurse starting shift i is available for shift i and i+1
# Min nurses required per shift: Morning≥10, Afternoon≥15, Evening≥8
scheduling = bl.prescriptive.integer_lp(
    objective=[1, 1, 1],               # Minimise total nurses
    constraints=[
        [1, 0, 1],    # Morning shift available (starts morning + evening)
        [1, 1, 0],    # Afternoon available (starts morning + afternoon)
        [0, 1, 1],    # Evening available
    ],
    rhs=[10, 15, 8],
    constraint_types=[">=", ">=", ">="],
    integer_vars=["NursesA", "NursesB", "NursesC"],
    variable_names=["NursesA", "NursesB", "NursesC"],
    maximize=False,
)
print(f"   Minimum staff: {scheduling['variables']}")
print(f"   Total nurses hired: {scheduling['objective_value']:.0f}")

# ──────────────────────────────────────────────────────────────────────────────
# 4. Portfolio Selection — Binary IP
#    Select at most 3 investments within $1M budget to maximise expected return
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("4. Portfolio Selection (Binary Integer LP):")
investments  = ["Tech ETF", "Bond Fund", "Real Estate", "Gold ETF",
                "Startup A", "Infrastructure", "Healthcare"]
returns      = [0.18, 0.06, 0.12, 0.08, 0.30, 0.10, 0.15]   # Expected return
costs_m      = [0.25, 0.40, 0.35, 0.20, 0.15, 0.45, 0.30]   # Cost in $M
max_picks    = 3

portfolio = bl.prescriptive.integer_lp(
    objective=returns,
    constraints=[
        costs_m,                                              # Budget ≤ 1.0M
        [1] * len(investments),                              # Max 3 picks
    ],
    rhs=[1.0, max_picks],
    constraint_types=["<=", "<="],
    binary_vars=investments,
    variable_names=investments,
    maximize=True,
)
selected = [inv for inv, v in portfolio["variables"].items() if v >= 0.5]
total_invested = sum(costs_m[investments.index(inv)] for inv in selected)
print(f"   Selected: {selected}")
print(f"   Expected return: {portfolio['objective_value']*100:.1f}%")
print(f"   Capital invested: ${total_invested:.2f}M")

# ──────────────────────────────────────────────────────────────────────────────
# 5. Sensitivity Analysis — break-even price point
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("5. Sensitivity — break-even profit contribution for Product X:")
bl.prescriptive.sensitivity(
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

print("\n✅ Example 09 complete.")
