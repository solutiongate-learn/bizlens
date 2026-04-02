"""
BizLens — Example 12: Time-Series Forecasting
==============================================
Topics covered — Basics to Advanced
-------------------------------------
• forecast.moving_average()      — Simple & Weighted Moving Average (SMA, WMA)
• forecast.exponential_smoothing()— Simple ES, Holt's (trend), Holt-Winters (seasonal)
• forecast.decompose()           — Trend + Seasonal + Residual decomposition
• forecast.arima()               — ARIMA and SARIMA modelling
• forecast.accuracy()            — MAE, RMSE, MAPE, SMAPE, MASE, R²
• forecast.compare()             — Side-by-side method horse race

Method selection guide:
  Stationary (no trend/season) → SMA or SES
  Trend, no season             → Holt's Double ES
  Trend + seasonality          → Holt-Winters Triple ES
  Complex patterns             → ARIMA / SARIMA
  Unknown structure            → compare() to benchmark all methods

Run anywhere
------------
  Google Colab : paste into a code cell and run
  VSCode / Jupyter / Terminal : python 12_forecasting.py
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

try:
    import statsmodels  # noqa: F401
except ImportError:
    print("Installing statsmodels (required for ARIMA, decomposition)...")
    _install("statsmodels")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # Safe for Colab / headless
import matplotlib.pyplot as plt
import bizlens as bl

np.random.seed(42)
print(f"BizLens version: {bl.__version__}\n")

# ── Build realistic time-series datasets ─────────────────────────────────────
n = 60  # 5 years of monthly data

# 1. Stationary series (no trend, no season) — suitable for SMA/SES
stationary = 100 + np.random.normal(0, 5, n)

# 2. Trending series — suitable for Holt's Double ES
trend_only = np.linspace(80, 160, n) + np.random.normal(0, 6, n)

# 3. Monthly seasonal + trend — suitable for Holt-Winters / SARIMA
t_idx = np.arange(n)
seasonal_trend = (
    80 + 1.2 * t_idx                          # upward trend
    + 20 * np.sin(2 * np.pi * t_idx / 12)    # 12-month cycle
    + np.random.normal(0, 5, n)
)

# 4. Monthly retail sales — realistic (trend + holiday spikes)
base_sales = np.linspace(10000, 18000, n)
seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * t_idx / 12 - np.pi)
holiday_spike = np.array([1.4 if (i % 12) in [10, 11] else 1.0 for i in range(n)])
retail_sales = base_sales * seasonal_factor * holiday_spike + np.random.normal(0, 500, n)

print("Datasets prepared:")
print(f"  stationary:    n={n}, mean={np.mean(stationary):.1f}")
print(f"  trend_only:    n={n}, trend {trend_only[0]:.0f}→{trend_only[-1]:.0f}")
print(f"  seasonal_trend:n={n}, mean={np.mean(seasonal_trend):.1f}")
print(f"  retail_sales:  n={n}, range ${retail_sales.min():,.0f}–${retail_sales.max():,.0f}\n")

# ── 1. Simple Moving Average ──────────────────────────────────────────────────
print("="*60)
print("1. Simple Moving Average (SMA) — Stationary series:")
print("   Window=3: fast-adapting  |  Window=6: smoother, lags more")
for window in [3, 6, 12]:
    sma = bl.forecast.moving_average(
        data=stationary, window=window, h=6, show_plot=(window == 3)
    )
    print(f"   SMA({window}): MAE={sma['MAE']:.3f}  RMSE={sma['RMSE']:.3f}  "
          f"MAPE={sma['MAPE']:.1f}%  Forecast: {[round(v,1) for v in sma['forecast_sma'][:3]]}...")

# ── 2. Simple Exponential Smoothing ──────────────────────────────────────────
print("\n" + "="*60)
print("2. Simple Exponential Smoothing (SES) — Stationary series:")
print("   α=0.1: heavy smoothing (slow)  |  α=0.5: balanced  |  α=0.9: tracks closely")
for alpha in [0.1, 0.3, 0.7]:
    ses = bl.forecast.exponential_smoothing(
        data=stationary, alpha=alpha, h=6, show_plot=(alpha == 0.3)
    )
    print(f"   SES(α={alpha}): MAE={ses['MAE']:.3f}  RMSE={ses['RMSE']:.3f}  "
          f"MAPE={ses['MAPE']:.1f}%")

print("\n   Key: Larger α → more weight to recent observations (reacts faster)")

# ── 3. Holt's Double ES — Trend ───────────────────────────────────────────────
print("\n" + "="*60)
print("3. Holt's Double Exponential Smoothing — Trending series:")
print("   Captures linear trend. α=level smoothing, β=trend smoothing")
holt = bl.forecast.exponential_smoothing(
    data=trend_only,
    alpha=0.3,
    beta=0.1,        # β > 0 activates trend component
    h=12,
    show_plot=True,
)
print(f"\n   MAE={holt['MAE']:.3f}  RMSE={holt['RMSE']:.3f}  MAPE={holt['MAPE']:.1f}%")
print(f"   12-period forecast: {[round(v,1) for v in holt['forecast']]}")

# ── 4. Holt-Winters Triple ES — Trend + Seasonality ──────────────────────────
print("\n" + "="*60)
print("4. Holt-Winters Triple ES — Trend + Seasonal series:")
print("   α=level, β=trend, γ=seasonality (m=12 for monthly data)")
hw = bl.forecast.exponential_smoothing(
    data=seasonal_trend,
    alpha=0.4,
    beta=0.1,
    gamma=0.2,       # γ > 0 activates seasonality component
    seasonal_periods=12,
    h=12,
    show_plot=True,
)
print(f"\n   MAE={hw['MAE']:.3f}  RMSE={hw['RMSE']:.3f}  MAPE={hw['MAPE']:.1f}%")

# ── 5. Seasonal Decomposition ─────────────────────────────────────────────────
print("\n" + "="*60)
print("5. Classical Time-Series Decomposition — Retail sales:")
print("   Additive:  y = Trend + Seasonal + Residual")
print("   Multiplicative: y = Trend × Seasonal × Residual")
try:
    decomp_add = bl.forecast.decompose(
        data=retail_sales, period=12, model="additive", show_plot=True
    )
    decomp_mul = bl.forecast.decompose(
        data=retail_sales, period=12, model="multiplicative", show_plot=False
    )
    print(f"\n   Additive:      Trend strength={decomp_add['trend_strength']:.3f}  "
          f"Seasonality strength={decomp_add['seasonality_strength']:.3f}")
    print(f"   Multiplicative: Trend strength={decomp_mul['trend_strength']:.3f}  "
          f"Seasonality strength={decomp_mul['seasonality_strength']:.3f}")
    print("   Rule: If seasonality_strength > 0.6 → seasonal model required")
    print("         If trend_strength > 0.6 → trend model required")
except Exception as e:
    print(f"   (Decomposition requires statsmodels: {e})")

# ── 6. ARIMA — AutoRegressive Integrated Moving Average ──────────────────────
print("\n" + "="*60)
print("6. ARIMA(p, d, q) — Trend series with no seasonality:")
print("   p=1: uses 1 lag (AR)  d=1: first difference (remove trend)  q=1: MA lag")
try:
    arima_result = bl.forecast.arima(
        data=trend_only,
        order=(1, 1, 1),
        h=12,
        show_plot=True,
    )
    print(f"\n   ARIMA(1,1,1): AIC={arima_result['AIC']:.2f}  BIC={arima_result['BIC']:.2f}")
    print(f"   MAE={arima_result['MAE']:.3f}  RMSE={arima_result['RMSE']:.3f}  "
          f"MAPE={arima_result['MAPE']:.1f}%")
    print(f"   12-step forecast: {[round(v,1) for v in arima_result['forecast']]}")
except Exception as e:
    print(f"   (ARIMA requires statsmodels: {e})")

# ── 7. SARIMA — Seasonal ARIMA ────────────────────────────────────────────────
print("\n" + "="*60)
print("7. SARIMA(1,1,1)(1,1,1,12) — Seasonal series:")
print("   Handles both non-seasonal and seasonal differencing")
try:
    sarima_result = bl.forecast.arima(
        data=seasonal_trend,
        order=(1, 1, 1),
        seasonal_order=(1, 1, 1, 12),
        h=12,
        show_plot=True,
    )
    print(f"\n   SARIMA: AIC={sarima_result['AIC']:.2f}  BIC={sarima_result['BIC']:.2f}")
    print(f"   MAE={sarima_result['MAE']:.3f}  MAPE={sarima_result['MAPE']:.1f}%")
except Exception as e:
    print(f"   (SARIMA requires statsmodels: {e})")

# ── 8. Forecast Accuracy Metrics ─────────────────────────────────────────────
print("\n" + "="*60)
print("8. Forecast Accuracy — comparing two forecasts on the same actual data:")
actual   = retail_sales[-12:]   # Last 12 months as held-out test
naive_f  = np.full(12, retail_sales[-13])   # Naïve: last known value
avg_f    = np.full(12, np.mean(retail_sales[:-12]))  # Average of training
print("\n   Naïve forecast accuracy:")
naive_acc = bl.forecast.accuracy(actual, naive_f, "Naïve (last value)")
print("\n   Mean forecast accuracy:")
mean_acc  = bl.forecast.accuracy(actual, avg_f,   "Mean (training average)")
print(f"\n   MASE < 1 means the method beats the naïve forecast")
print(f"   Naïve MASE={naive_acc['MASE']:.4f}  |  Mean MASE={mean_acc['MASE']:.4f}")

# ── 9. Method Comparison (horse race) ────────────────────────────────────────
print("\n" + "="*60)
print("9. Forecast Method Comparison — hold out last 12 months as test set:")
print("   All methods trained on same data, evaluated on same test set")
try:
    comparison_df = bl.forecast.compare(
        data=seasonal_trend,
        h=6,
        test_size=12,
        show_plot=True,
    )
    print("\n   Best method (lowest RMSE):", comparison_df.iloc[0]["Method"])
    print("   Compare methods across MAE, RMSE, MAPE to choose the best fit.")
except Exception as e:
    print(f"   Method comparison failed: {e}")

# ── 10. Key forecasting concepts ─────────────────────────────────────────────
print("\n" + "="*60)
print("10. Forecasting method selection guide:")
print("""
  ┌──────────────────────────┬────────────────┬───────────────────────────────┐
  │ Series pattern           │ Recommended    │ Notes                         │
  ├──────────────────────────┼────────────────┼───────────────────────────────┤
  │ Stationary (flat)        │ SMA or SES     │ No trend, no seasonality      │
  │ Linear trend             │ Holt's ES      │ Captures slope only           │
  │ Trend + seasonality      │ Holt-Winters   │ Additive or multiplicative    │
  │ Complex autocorrelation  │ ARIMA(p,d,q)   │ Use ACF/PACF to choose orders │
  │ Seasonal + complex       │ SARIMA         │ Add (P,D,Q,m) seasonal terms  │
  │ Unknown / baseline       │ forecast.compare()│ Always benchmark first      │
  └──────────────────────────┴────────────────┴───────────────────────────────┘

  Accuracy metric guide:
  ──────────────────────
  MAE   : Easy to interpret (same unit as data); sensitive to scale
  RMSE  : Penalises large errors more; good for production monitoring
  MAPE  : Scale-free (%), easy to explain; fails if actual ≈ 0
  SMAPE : Symmetric MAPE; handles near-zero values better
  MASE  : Scaled by naïve — < 1 means you beat the random-walk baseline
  R²    : 1.0 = perfect; 0 = no better than predicting the mean

  Stationarity:
  ─────────────
  ARIMA requires a stationary series (constant mean & variance).
  d=1 or d=2 differencing typically removes trend.
  Use ADF test (Augmented Dickey-Fuller) to check stationarity formally.

  ARIMA order selection:
  ──────────────────────
  p (AR)  : Look at PACF — significant spikes at lag 1, 2, ...
  q (MA)  : Look at ACF  — significant spikes at lag 1, 2, ...
  d (I)   : Number of differences needed to achieve stationarity
  Try auto_arima (pmdarima library) for automated order selection.
""")

print("✅ Example 12 complete — Time-Series Forecasting")
