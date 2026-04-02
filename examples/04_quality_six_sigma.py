"""
BizLens — Example 04: Quality Analytics & Six Sigma
====================================================
Topics covered
--------------
• quality.process_capability()  — Cp, Cpk, Pp, Ppk, sigma level, DPMO, yield
• quality.control_chart()       — X-bar, R, IMR, p control charts
• quality.pareto()              — Pareto 80/20 analysis (count + value)
• quality.fishbone()            — Cause-and-Effect (Ishikawa) diagram
• Six Sigma grade thresholds    — World class / Capable / Marginal / Incapable

Run anywhere
------------
  Google Colab : paste into a code cell and run
  VSCode / Jupyter / Terminal : python 04_quality_six_sigma.py
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
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import bizlens as bl

np.random.seed(42)
print(f"BizLens version: {bl.__version__}\n")

# ── 1. Process Capability — bolt diameter (capable process) ──────────────────
print("="*60)
print("1. Process Capability — bolt diameter")
print("   Spec: LSL=9.95mm, USL=10.05mm, Target=10.0mm")
print("   Process: mean=10.005, σ=0.012  (slightly off-centre but capable)")
bolt_df = pd.DataFrame({
    "diameter": np.random.normal(loc=10.005, scale=0.012, size=200)
})
cap1 = bl.quality.process_capability(
    data=bolt_df, column="diameter",
    lsl=9.95, usl=10.05, target=10.0, show_plot=True
)
print(f"\n   Cp={cap1['Cp']:.3f}   Cpk={cap1['Cpk']:.3f}")
print(f"   Sigma level={cap1['sigma_level']:.2f}  DPMO={cap1['DPMO']:,.1f}  Yield={cap1['yield_pct']:.4f}%")

# ── 2. Process Capability — incapable process ─────────────────────────────────
print("\n" + "="*60)
print("2. Process Capability — incapable process")
print("   Same specs but process is wide and off-centre: mean=10.02, σ=0.035")
bad_df = pd.DataFrame({
    "diameter": np.random.normal(loc=10.02, scale=0.035, size=200)
})
cap2 = bl.quality.process_capability(
    data=bad_df, column="diameter",
    lsl=9.95, usl=10.05, target=10.0, show_plot=True
)
print(f"\n   Cp={cap2['Cp']:.3f}   Cpk={cap2['Cpk']:.3f}")
print(f"   Sigma level={cap2['sigma_level']:.2f}  DPMO={cap2['DPMO']:,.1f}  Yield={cap2['yield_pct']:.4f}%")
print(f"\n   Six Sigma Grade Thresholds:")
print("   Cpk ≥ 1.67 → World Class ⭐⭐⭐")
print("   Cpk ≥ 1.33 → Capable ✅")
print("   Cpk ≥ 1.00 → Marginal ⚠️")
print("   Cpk < 1.00 → Incapable ❌ — process must be improved")

# ── 3. Pharmaceutical tablet weight ──────────────────────────────────────────
print("\n" + "="*60)
print("3. Pharmaceutical tablet weight")
print("   Spec: 498mg – 502mg (tight tolerance for drug dosing)")
tablet_df = pd.DataFrame({
    "weight_mg": np.random.normal(loc=499.8, scale=0.5, size=300)
})
cap3 = bl.quality.process_capability(
    data=tablet_df, column="weight_mg",
    lsl=498.0, usl=502.0, show_plot=True
)
print(f"   Cpk={cap3['Cpk']:.3f}  Yield={cap3['yield_pct']:.4f}%")

# ── 4. X-bar Chart — in-control process ──────────────────────────────────────
print("\n" + "="*60)
print("4. X-bar Control Chart — in-control process (n=5 per subgroup):")
in_ctrl = np.random.normal(loc=10.0, scale=0.01, size=100)
in_ctrl_df = pd.DataFrame({"diameter": in_ctrl})
xbar_ok = bl.quality.control_chart(in_ctrl_df, column="diameter",
                                    chart_type="xbar", subgroup_size=5, show_plot=True)
print(f"   UCL={xbar_ok['UCL']:.5f}  CL={xbar_ok['CL']:.5f}  LCL={xbar_ok['LCL']:.5f}")
print(f"   Points out of control: {xbar_ok['n_out']}  ({'Process stable ✅' if xbar_ok['n_out'] == 0 else 'Process unstable ❌'})")

# ── 5. X-bar Chart — process shift ───────────────────────────────────────────
print("\n" + "="*60)
print("5. X-bar Control Chart — with deliberate process shift at subgroup 16:")
shifted = np.concatenate([
    np.random.normal(10.0,  0.01, 75),   # Stable
    np.random.normal(10.03, 0.01, 25),   # Shift (mean jumps)
])
shifted_df = pd.DataFrame({"diameter": shifted})
xbar_shift = bl.quality.control_chart(shifted_df, column="diameter",
                                       chart_type="xbar", subgroup_size=5, show_plot=True)
print(f"   Points out of control: {xbar_shift['n_out']}  ← shift detected!")
print(f"   Out-of-control subgroups: {xbar_shift['points_out_of_control']}")

# ── 6. I-MR Chart — individual measurements ──────────────────────────────────
print("\n" + "="*60)
print("6. I-MR (Individuals) Chart — daily customer wait time (minutes):")
wait_times = pd.DataFrame({
    "wait_min": np.abs(np.random.normal(loc=8.5, scale=2.0, size=30))
})
imr = bl.quality.control_chart(wait_times, column="wait_min",
                                chart_type="imr", show_plot=True)
print(f"   UCL={imr['UCL']:.3f}  CL={imr['CL']:.3f}  LCL={imr['LCL']:.3f}")

# ── 7. Pareto by count ────────────────────────────────────────────────────────
print("\n" + "="*60)
print("7. Pareto Chart — factory defect analysis (count-based):")
defect_data = pd.DataFrame({
    "defect_type": np.random.choice(
        ["Surface scratch", "Dimension error", "Paint defect", "Assembly error",
         "Missing part", "Wrong label", "Electrical fault", "Packaging damage"],
        size=500,
        p=[0.35, 0.25, 0.15, 0.10, 0.06, 0.04, 0.03, 0.02]
    )
})
pareto1 = bl.quality.pareto(defect_data, category_col="defect_type", show_plot=True)
print("\n   80/20 insight:")
cum80 = pareto1[pareto1["Cumulative %"] >= 80].index[0] + 1
print(f"   {cum80} defect types account for ≥80% of all defects")
print("   → Focus improvement effort on these categories first")

# ── 8. Pareto by cost ─────────────────────────────────────────────────────────
print("\n" + "="*60)
print("8. Pareto Chart — by warranty cost (value-based prioritisation):")
warranty = pd.DataFrame({
    "defect_type": ["Electrical fault", "Surface scratch", "Dimension error",
                    "Assembly error", "Paint defect", "Missing part", "Wrong label"],
    "cost_usd":    [45000, 18000, 12000, 9500, 7200, 3000, 1200],
})
pareto2 = bl.quality.pareto(warranty, category_col="defect_type",
                             value_col="cost_usd", show_plot=True)

# ── 9. Fishbone Diagram ───────────────────────────────────────────────────────
print("\n" + "="*60)
print("9. Fishbone (Ishikawa) Diagram — root cause analysis:")
bl.quality.fishbone(
    categories={
        "Machine":      ["Worn tooling", "Poor calibration",
                         "Vibration", "Old equipment"],
        "Method":       ["No SOP defined", "Inconsistent steps",
                         "Operator discretion"],
        "Material":     ["Wrong alloy grade", "High moisture content",
                         "Supplier variation"],
        "Man":          ["Operator fatigue", "Insufficient training",
                         "High staff turnover"],
        "Measurement":  ["Wrong gauge", "Calibration expired",
                         "Human reading error"],
        "Environment":  ["Temperature swing", "High humidity", "Contamination"],
    },
    effect="High Defect Rate (>3%)",
    color_scheme="academic",
)

# ── 10. Six Sigma interpretation table ────────────────────────────────────────
print("\n" + "="*60)
print("10. Six Sigma DPMO and Yield reference:")
print("""
  ┌─────────────┬──────────┬───────────────┬──────────────┐
  │ Sigma Level │   DPMO   │    Yield %    │    Grade     │
  ├─────────────┼──────────┼───────────────┼──────────────┤
  │     1σ      │ 691,462  │    30.854%    │  Incapable   │
  │     2σ      │ 308,538  │    69.146%    │  Incapable   │
  │     3σ      │  66,807  │    93.319%    │  Marginal    │
  │     4σ      │   6,210  │    99.379%    │  Capable     │
  │     5σ      │     233  │   99.977%     │  Very Good   │
  │     6σ      │     3.4  │   99.9997%    │  World Class │
  └─────────────┴──────────┴───────────────┴──────────────┘
  Note: figures include the standard ±1.5σ long-term shift
""")

print("✅ Example 04 complete — Quality Analytics & Six Sigma")
