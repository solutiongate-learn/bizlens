"""
BizLens — Example 07: Monte Carlo Simulation
=============================================
Covers:
  • simulate.run()         — Generic MC engine (any model function)
  • simulate.npv()         — Project NPV under uncertainty
  • simulate.bootstrap()   — Bootstrap confidence intervals
  • simulate.risk_matrix() — Risk register simulation & tornado chart

Distributions supported: normal, uniform, triangular, lognormal,
                          poisson, binomial, exponential, beta, fixed

Run:   python 07_monte_carlo_simulation.py
"""

import numpy as np
import pandas as pd
import bizlens as bl

# ──────────────────────────────────────────────────────────────────────────────
# 1. Generic Monte Carlo — Profit model
#    Profit = Revenue - Fixed Cost - Variable Cost × Units
# ──────────────────────────────────────────────────────────────────────────────
print("="*60)
print("1. Monte Carlo Profit Simulation (10,000 trials):")

def profit_model(revenue, units, var_cost, fixed_cost):
    return revenue * units - var_cost * units - fixed_cost

result = bl.simulate.run(
    model_fn=profit_model,
    n_trials=10_000,
    inputs={
        "revenue":    {"dist": "triangular", "low": 80,    "mode": 100,  "high": 130},
        "units":      {"dist": "normal",     "mean": 5000, "std": 600},
        "var_cost":   {"dist": "uniform",    "low": 35,    "high": 55},
        "fixed_cost": {"dist": "fixed",      "value": 150_000},
    },
    seed=42,
    show_plot=True,
)
print(f"   Mean Profit: ${result['mean']:,.0f}")
print(f"   P(Profit > 0): {result['P(>0)%']:.1f}%")
print(f"   P5–P95 range: ${result['P5']:,.0f} to ${result['P95']:,.0f}")

# ──────────────────────────────────────────────────────────────────────────────
# 2. Monte Carlo — Break-even analysis
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("2. Break-even Units Simulation:")

def breakeven(fixed_cost, price, var_cost):
    """Break-even = Fixed Cost / (Price - Variable Cost)"""
    margin = price - var_cost
    return fixed_cost / margin if margin > 0 else np.nan

be_result = bl.simulate.run(
    model_fn=breakeven,
    n_trials=10_000,
    inputs={
        "fixed_cost": {"dist": "triangular", "low": 80_000, "mode": 100_000, "high": 140_000},
        "price":      {"dist": "normal",     "mean": 150,   "std": 10},
        "var_cost":   {"dist": "normal",     "mean": 95,    "std": 8},
    },
    seed=42,
    show_plot=True,
)
print(f"   Median break-even units: {be_result['P50']:,.0f}")
print(f"   90th percentile (worst case): {be_result['P90']:,.0f} units")

# ──────────────────────────────────────────────────────────────────────────────
# 3. NPV Simulation — Capital investment decision
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("3. NPV Simulation — 5-year capital project ($1M investment):")

npv_result = bl.simulate.npv(
    cash_flows_dist=[
        {"dist": "fixed",      "value": -1_000_000},          # Year 0: investment
        {"dist": "triangular", "low": 150_000, "mode": 250_000, "high": 350_000},  # Year 1
        {"dist": "normal",     "mean": 300_000, "std": 60_000},                    # Year 2
        {"dist": "normal",     "mean": 350_000, "std": 70_000},                    # Year 3
        {"dist": "triangular", "low": 200_000, "mode": 400_000, "high": 600_000},  # Year 4
        {"dist": "lognormal",  "mean": 12.8,   "sigma": 0.4},                     # Year 5
    ],
    discount_rate_dist={"dist": "normal", "mean": 0.10, "std": 0.02},
    n_trials=10_000,
    seed=42,
    show_plot=True,
)
print(f"   Mean NPV: ${npv_result['mean_npv']:,.2f}")
print(f"   P(NPV > 0): {npv_result['P(NPV>0)%']:.1f}%")
print(f"   P10 NPV (downside): ${npv_result['P10']:,.2f}")
print(f"   P90 NPV (upside):   ${npv_result['P90']:,.2f}")

# ──────────────────────────────────────────────────────────────────────────────
# 4. Bootstrap Confidence Intervals
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("4. Bootstrap — 95% CI for the median of customer spend:")
customer_spend = pd.DataFrame({
    "spend_usd": np.random.lognormal(mean=4.0, sigma=0.8, size=120)
})

boot_mean = bl.simulate.bootstrap(
    data=customer_spend, column="spend_usd",
    statistic=np.mean, n_trials=10_000, confidence=0.95, show_plot=True
)
boot_median = bl.simulate.bootstrap(
    data=customer_spend, column="spend_usd",
    statistic=np.median, n_trials=10_000, confidence=0.95, show_plot=True
)
print(f"   Mean:   {boot_mean['observed']:.2f}  CI: [{boot_mean['CI_95%_lower']:.2f}, {boot_mean['CI_95%_upper']:.2f}]")
print(f"   Median: {boot_median['observed']:.2f}  CI: [{boot_median['CI_95%_lower']:.2f}, {boot_median['CI_95%_upper']:.2f}]")

# ──────────────────────────────────────────────────────────────────────────────
# 5. Risk Register Simulation
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("5. Risk Register — project risk portfolio:")

risk_result = bl.simulate.risk_matrix(
    risks=[
        {
            "name": "Supplier delay",
            "probability": 0.40,
            "impact": {"dist": "triangular", "low": 20_000, "mode": 50_000, "high": 120_000},
        },
        {
            "name": "Regulatory fine",
            "probability": 0.10,
            "impact": {"dist": "uniform", "low": 50_000, "high": 300_000},
        },
        {
            "name": "Cyber security breach",
            "probability": 0.05,
            "impact": {"dist": "lognormal", "mean": 12.5, "sigma": 0.5},
        },
        {
            "name": "Key staff departure",
            "probability": 0.20,
            "impact": {"dist": "normal", "mean": 30_000, "std": 10_000},
        },
        {
            "name": "Exchange rate fluctuation",
            "probability": 0.60,
            "impact": {"dist": "triangular", "low": 5_000, "mode": 15_000, "high": 40_000},
        },
        {
            "name": "Technology failure",
            "probability": 0.15,
            "impact": {"dist": "triangular", "low": 10_000, "mode": 25_000, "high": 80_000},
        },
    ],
    n_trials=10_000,
    seed=42,
    show_plot=True,
)

print("\n✅ Example 07 complete.")
