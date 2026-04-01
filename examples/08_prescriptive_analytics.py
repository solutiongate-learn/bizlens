"""
BizLens — Example 08: Prescriptive Analytics & Operations Research
===================================================================
Covers:
  • prescriptive.lp()             — Linear Programming with shadow prices
  • prescriptive.integer_lp()     — MILP / Integer Programming (knapsack)
  • prescriptive.transportation() — Transportation problem
  • prescriptive.assignment()     — Assignment problem (Hungarian method)
  • prescriptive.sensitivity()    — Sensitivity / what-if analysis
  • prescriptive.packages()       — OR ecosystem overview
  • optimize.linear_program()     — Core LP wrapper

Run:   python 08_prescriptive_analytics.py
       pip install bizlens PuLP
"""

import bizlens as bl

# ──────────────────────────────────────────────────────────────────────────────
# Show the Analytics Pyramid + OR ecosystem
# ──────────────────────────────────────────────────────────────────────────────
print("="*60)
print("Operations Research & Optimization Ecosystem:")
bl.prescriptive.packages()

# ──────────────────────────────────────────────────────────────────────────────
# 1. Linear Program — Product mix optimisation
#    Maximise profit: 5x1 + 4x2 (two products)
#    Subject to:
#      Labour:    6x1 + 4x2 ≤ 24   (hours/week)
#      Materials: x1  + 2x2 ≤ 6    (units)
#      x1, x2 ≥ 0
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("1. LP — Product Mix Optimisation (maximise profit):")
lp_result = bl.prescriptive.lp(
    objective=[5, 4],
    constraints=[[6, 4], [1, 2]],
    rhs=[24, 6],
    variable_names=["ProductA", "ProductB"],
    constraint_types=["<=", "<="],
    maximize=True,
    show_plot=True,
)
print(f"   Optimal: ProductA={lp_result['variables']['ProductA']}, "
      f"ProductB={lp_result['variables']['ProductB']}")
print(f"   Max Profit: {lp_result['objective_value']}")

# ──────────────────────────────────────────────────────────────────────────────
# 2. LP — Diet / Cost minimisation
#    Minimise cost: 3x1 + 5x2 + 2x3
#    Subject to nutritional minimums:
#      Protein:  2x1 + x2  + x3  ≥ 8
#      Vitamins: x1  + x2  + 2x3 ≥ 6
#      Calories: x1  + 3x2 + x3  ≥ 9
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("2. LP — Diet Cost Minimisation:")
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
print(f"   Min cost: {diet['objective_value']}")
print(f"   Food mix: {diet['variables']}")

# ──────────────────────────────────────────────────────────────────────────────
# 3. Integer LP — Capital budgeting (Knapsack problem)
#    Select projects to maximise NPV within $500K budget
#    Binary decision: 1 = invest, 0 = skip
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("3. MILP — Capital Budgeting (project selection):")
projects = ["CRM system", "New factory", "R&D lab", "Marketing campaign", "ERP upgrade"]
npvs    = [120, 310,  85,  60, 180]   # NPV in $000s
budgets = [150, 400, 120,  80, 220]   # Cost in $000s
total_budget = 500

milp = bl.prescriptive.integer_lp(
    objective=npvs,
    constraints=[budgets],
    rhs=[total_budget],
    binary_vars=projects,
    variable_names=projects,
    maximize=True,
)
selected = [p for p, v in milp["variables"].items() if v >= 0.5]
print(f"   Selected projects: {selected}")
print(f"   Max NPV: ${milp['objective_value']:,.0f}K")
total_spend = sum(budgets[i] for i, p in enumerate(projects) if p in selected)
print(f"   Total spend: ${total_spend:,.0f}K (budget: ${total_budget:,.0f}K)")

# ──────────────────────────────────────────────────────────────────────────────
# 4. Transportation Problem — minimise shipping cost
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("4. Transportation Problem — Warehouse to Retail:")
# Cost matrix [warehouse][store] — cost per unit
transport = bl.prescriptive.transportation(
    supply=[300, 400, 500],
    demand=[250, 350, 400, 200],
    costs=[
        [2, 3, 1, 5],   # Warehouse A
        [4, 1, 3, 2],   # Warehouse B
        [3, 5, 2, 4],   # Warehouse C
    ],
    supply_names=["Warehouse A", "Warehouse B", "Warehouse C"],
    demand_names=["Store 1", "Store 2", "Store 3", "Store 4"],
)
print(f"   Total minimum shipping cost: ${transport['total_cost']:,.2f}")

# ──────────────────────────────────────────────────────────────────────────────
# 5. Assignment Problem — assign engineers to projects
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("5. Assignment Problem — Engineer to Project (minimise total days):")
# Cost matrix: estimated completion days [engineer][project]
assignment = bl.prescriptive.assignment(
    cost_matrix=[
        [15, 18, 20, 25],   # Engineer 1
        [20, 12, 22, 18],   # Engineer 2
        [25, 20, 10, 15],   # Engineer 3
        [18, 25, 15, 12],   # Engineer 4
    ],
    agent_names=["Alice", "Bob", "Carol", "Dave"],
    task_names=["Project Alpha", "Project Beta", "Project Gamma", "Project Delta"],
    maximize=False,
)
print(f"   Optimal assignments: {assignment['assignments']}")
print(f"   Total days: {assignment['total']}")

# ──────────────────────────────────────────────────────────────────────────────
# 6. Sensitivity Analysis — what happens if labour supply changes?
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("6. Sensitivity Analysis — vary labour hours (RHS of constraint 1):")
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
print(f"   Tested {len(sens)} labour hour scenarios.")
print(f"   Objective range: [{sens['objective'].min():.2f}, {sens['objective'].max():.2f}]")

# ──────────────────────────────────────────────────────────────────────────────
# 7. Sensitivity — vary objective coefficient (price of Product A)
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("7. Sensitivity — vary Product A profit contribution:")
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

print("\n✅ Example 08 complete.")
print("\n💡 Also try:  bl.optimize.linear_program() for the core LP wrapper.")
