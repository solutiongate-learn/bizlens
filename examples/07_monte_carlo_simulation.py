"""
BizLens — Example 07: Monte Carlo Simulation
=============================================
Topics covered
--------------
• simulate.run()         — Generic MC engine (any Python model function)
• simulate.npv()         — Project NPV under uncertainty
• simulate.bootstrap()   — Bootstrap confidence intervals (mean, median, std)
• simulate.risk_matrix() — Risk register simulation & tornado chart

Distributions supported
-----------------------
  normal, uniform, triangular, lognormal, poisson, binomial,
  exponential, beta, fixed

Run anywhere
------------
  Google Colab : paste into a code cell and run
  VSCode / Jupyter / Terminal : python 07_monte_carlo_simulation.py
"""

# ── Auto-install ──────────────────────────────────────────────────────────────
import subprocess, sys

def _install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

for pkg in ["bizlens", "numpy", "pandas", "matplotlib", "scipy"]:
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

np.random.seed(42)
print(f"BizLens version: {bl.__version__}\n")

# ── 1. Generic Monte Carlo — Profit model ────────────────────────────────────
print("="*60)
print("1. Monte Carlo Profit Simulation (10,000 trials):")
print("   Model: Profit = Revenue × Units − Variable Cost × Units − Fixed Cost")

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
print(f"\n   Mean Profit:        ${result['mean']:>12,.0f}")
print(f"   Std Deviation:      ${result['std']:>12,.0f}")
print(f"   P5  (downside):     ${result['P5']:>12,.0f}")
print(f"   P50 (median):       ${result['P50']:>12,.0f}")
print(f"   P95 (upside):       ${result['P95']:>12,.0f}")
print(f"   P(Profit > 0):       {result['P(>0)%']:>11.1f}%")
risk_flag = "Low ✅" if result['P(>0)%'] > 90 else "Medium ⚠️" if result['P(>0)%'] > 70 else "High ❌"
print(f"   Risk assessment:     {risk_flag}")

# ── 2. Break-even simulation ──────────────────────────────────────────────────
print("\n" + "="*60)
print("2. Break-even Units Simulation:")
print("   Model: Break-even = Fixed Cost / (Price − Variable Cost)")

def breakeven(fixed_cost, price, var_cost):
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
print(f"\n   P10 break-even (best case):    {be_result['P10']:>8,.0f} units")
print(f"   P50 break-even (median):       {be_result['P50']:>8,.0f} units")
print(f"   P90 break-even (worst case):   {be_result['P90']:>8,.0f} units")
print(f"   Uncertainty range (P90−P10):   {be_result['P90']-be_result['P10']:>8,.0f} units")

# ── 3. NPV Simulation — Capital investment ────────────────────────────────────
print("\n" + "="*60)
print("3. NPV Simulation — 5-year capital project ($1M investment):")
print("   Each future cash flow has its own uncertainty distribution")

npv_result = bl.simulate.npv(
    cash_flows_dist=[
        {"dist": "fixed",      "value": -1_000_000},                               # Y0
        {"dist": "triangular", "low": 150_000, "mode": 250_000, "high": 350_000},  # Y1
        {"dist": "normal",     "mean": 300_000, "std": 60_000},                    # Y2
        {"dist": "normal",     "mean": 350_000, "std": 70_000},                    # Y3
        {"dist": "triangular", "low": 200_000, "mode": 400_000, "high": 600_000},  # Y4
        {"dist": "lognormal",  "mean": 12.8,   "sigma": 0.4},                     # Y5
    ],
    discount_rate_dist={"dist": "normal", "mean": 0.10, "std": 0.02},
    n_trials=10_000,
    seed=42,
    show_plot=True,
)
print(f"\n   Mean NPV:             ${npv_result['mean_npv']:>12,.2f}")
print(f"   P(NPV > 0):           {npv_result['P(NPV>0)%']:>11.1f}%  ({'Invest ✅' if npv_result['P(NPV>0)%'] > 70 else 'Review ⚠️'})")
print(f"   P10 NPV (downside):   ${npv_result['P10']:>12,.2f}")
print(f"   P90 NPV (upside):     ${npv_result['P90']:>12,.2f}")
print(f"   Value at Risk (P10):  ${abs(min(npv_result['P10'], 0)):>12,.2f}")

# ── 4. Bootstrap Confidence Intervals ────────────────────────────────────────
print("\n" + "="*60)
print("4. Bootstrap — Confidence Intervals for customer spend statistics:")
print("   (Bootstrap resamples the observed data 10,000× to estimate CI)")
np.random.seed(42)
customer_spend = pd.DataFrame({
    "spend_usd": np.random.lognormal(mean=4.0, sigma=0.8, size=120)
})
print(f"   Sample: n={len(customer_spend)}, "
      f"mean=${customer_spend['spend_usd'].mean():.2f}, "
      f"median=${customer_spend['spend_usd'].median():.2f}")

boot_mean = bl.simulate.bootstrap(
    data=customer_spend, column="spend_usd",
    statistic=np.mean, n_trials=10_000, confidence=0.95, show_plot=True
)
boot_median = bl.simulate.bootstrap(
    data=customer_spend, column="spend_usd",
    statistic=np.median, n_trials=10_000, confidence=0.95, show_plot=True
)
boot_std = bl.simulate.bootstrap(
    data=customer_spend, column="spend_usd",
    statistic=np.std, n_trials=10_000, confidence=0.95, show_plot=False
)
print(f"\n   Statistic   Observed    95% CI Lower    95% CI Upper")
print(f"   ─────────────────────────────────────────────────────")
print(f"   Mean      {boot_mean['observed']:>10.2f}    "
      f"{boot_mean['CI_95%_lower']:>12.2f}    {boot_mean['CI_95%_upper']:>12.2f}")
print(f"   Median    {boot_median['observed']:>10.2f}    "
      f"{boot_median['CI_95%_lower']:>12.2f}    {boot_median['CI_95%_upper']:>12.2f}")
print(f"   Std Dev   {boot_std['observed']:>10.2f}    "
      f"{boot_std['CI_95%_lower']:>12.2f}    {boot_std['CI_95%_upper']:>12.2f}")

# ── 5. Risk Register Simulation ───────────────────────────────────────────────
print("\n" + "="*60)
print("5. Risk Register — project risk portfolio (tornado chart):")
print("   Each risk = probability × uncertain impact distribution")

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

# ── 6. Sensitivity (tornado) manual check ─────────────────────────────────────
print("\n" + "="*60)
print("6. Custom revenue model — tornado chart (which input drives most variance?):")

def revenue_model(price, volume, discount, churn_rate):
    """Annual recurring revenue model"""
    net_volume = volume * (1 - churn_rate)
    net_price  = price * (1 - discount)
    return net_volume * net_price * 12  # monthly → annual

tornado = bl.simulate.run(
    model_fn=revenue_model,
    n_trials=10_000,
    inputs={
        "price":      {"dist": "triangular", "low": 45,   "mode": 60,   "high": 80},
        "volume":     {"dist": "normal",     "mean": 2000, "std": 300},
        "discount":   {"dist": "uniform",    "low": 0.05,  "high": 0.20},
        "churn_rate": {"dist": "beta",       "alpha": 2,   "beta": 18},
    },
    seed=42,
    show_plot=True,
)
print(f"\n   Mean Annual Revenue:  ${tornado['mean']:>12,.0f}")
print(f"   P5  (downside):       ${tornado['P5']:>12,.0f}")
print(f"   P95 (upside):         ${tornado['P95']:>12,.0f}")

# ── 7. Interpretation guide ───────────────────────────────────────────────────
print("\n" + "="*60)
print("7. Monte Carlo interpretation guide:")
print("""
  Distribution choice guide
  ─────────────────────────────────────────────────────────────────────
  normal      : Measurements around a known mean (errors, variations)
  triangular  : Expert estimates with min/mode/max (common in projects)
  uniform     : All values equally likely in a range (unknown parameters)
  lognormal   : Always positive, right-skewed (costs, asset prices)
  beta        : Proportions and rates (0–1), flexible shape
  poisson     : Count of rare events per time period
  binomial    : Number of successes in n trials
  fixed       : Known constant (no uncertainty)

  Key output percentiles
  ─────────────────────
  P5  / P10  → Downside / pessimistic scenario
  P50        → Median (most likely outcome)
  P90 / P95  → Upside / optimistic scenario
  P(>0)%     → Probability of a positive outcome

  Bootstrap vs parametric CI
  ──────────────────────────
  Bootstrap : No distribution assumed — works on any statistic
  Parametric: Assumes normality — faster but less robust for small n
""")

print("✅ Example 07 complete — Monte Carlo Simulation")
