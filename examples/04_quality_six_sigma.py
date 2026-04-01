"""
BizLens — Example 04: Quality Analytics & Six Sigma
====================================================
Covers:
  • quality.process_capability()  — Cp, Cpk, Pp, Ppk, DPMO, yield, sigma level
  • quality.control_chart()       — X-bar, R, IMR, p charts
  • quality.pareto()              — Pareto / 80-20 analysis
  • quality.fishbone()            — Cause-and-Effect (Ishikawa) diagram

Run:   python 04_quality_six_sigma.py
"""

import numpy as np
import pandas as pd
import bizlens as bl

np.random.seed(42)

# ──────────────────────────────────────────────────────────────────────────────
# 1. Process Capability — manufacturing bolt diameter
# ──────────────────────────────────────────────────────────────────────────────
print("="*60)
print("1. Process Capability — bolt diameter (LSL=9.95mm, USL=10.05mm, Target=10.0mm):")
# Simulate bolt diameters (mean slightly off-target)
bolt_diameters = pd.DataFrame({
    "diameter": np.random.normal(loc=10.005, scale=0.012, size=200)
})

cap = bl.quality.process_capability(
    data=bolt_diameters,
    column="diameter",
    lsl=9.95,
    usl=10.05,
    target=10.0,
    show_plot=True,
)
print(f"   Cp={cap['Cp']:.3f}  Cpk={cap['Cpk']:.3f}  Sigma={cap['sigma_level']:.2f}  DPMO={cap['DPMO']:.1f}")

# ──────────────────────────────────────────────────────────────────────────────
# 2. Process Capability — pharmaceutical tablet weight
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("2. Process Capability — tablet weight (LSL=498mg, USL=502mg):")
tablet_weights = pd.DataFrame({
    "weight_mg": np.random.normal(loc=499.8, scale=0.5, size=300)
})
cap2 = bl.quality.process_capability(
    data=tablet_weights,
    column="weight_mg",
    lsl=498.0,
    usl=502.0,
    show_plot=True,
)
print(f"   Cpk={cap2['Cpk']:.3f}  Yield={cap2['yield_pct']:.4f}%")

# ──────────────────────────────────────────────────────────────────────────────
# 3. X-bar Control Chart — monitor mean with subgroups of 5
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("3. X-bar Control Chart — bolt diameter (subgroup size=5):")
# Add a process shift after observation 75
process_data = np.concatenate([
    np.random.normal(10.0, 0.01, 75),   # In control
    np.random.normal(10.02, 0.01, 25),  # Process shift
])
process_df = pd.DataFrame({"diameter": process_data})
xbar = bl.quality.control_chart(process_df, column="diameter",
                                chart_type="xbar", subgroup_size=5, show_plot=True)
print(f"   UCL={xbar['UCL']:.4f}  CL={xbar['CL']:.4f}  LCL={xbar['LCL']:.4f}")
print(f"   Points out of control: {xbar['n_out']}")

# ──────────────────────────────────────────────────────────────────────────────
# 4. I-MR (Individuals & Moving Range) Chart
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("4. Individuals (I-MR) Control Chart — daily defect rate:")
daily_defects = pd.DataFrame({
    "defects": np.abs(np.random.normal(4, 1.2, 30))
})
imr = bl.quality.control_chart(daily_defects, column="defects",
                                chart_type="imr", show_plot=True)

# ──────────────────────────────────────────────────────────────────────────────
# 5. Pareto Chart — defect types in a factory
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("5. Pareto Chart — factory defect analysis:")
defect_data = pd.DataFrame({
    "defect_type": np.random.choice(
        ["Surface scratch","Dimension error","Paint defect","Assembly error",
         "Missing part","Wrong label","Electrical fault","Packaging damage"],
        size=500,
        p=[0.35, 0.25, 0.15, 0.10, 0.06, 0.04, 0.03, 0.02]
    )
})
pareto = bl.quality.pareto(defect_data, category_col="defect_type", show_plot=True)

# ──────────────────────────────────────────────────────────────────────────────
# 6. Pareto with value column — warranty cost by defect
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("6. Pareto by warranty cost:")
warranty_data = pd.DataFrame({
    "defect_type": ["Electrical fault","Surface scratch","Dimension error",
                    "Assembly error","Paint defect","Missing part","Wrong label"],
    "cost_usd":    [45000, 18000, 12000, 9500, 7200, 3000, 1200],
})
pareto2 = bl.quality.pareto(warranty_data, category_col="defect_type",
                             value_col="cost_usd", show_plot=True)

# ──────────────────────────────────────────────────────────────────────────────
# 7. Fishbone / Ishikawa Diagram
# ──────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("7. Fishbone Diagram — Root cause analysis for high defect rate:")
bl.quality.fishbone(
    categories={
        "Machine":      ["Worn tooling", "Poor calibration", "Vibration", "Old equipment"],
        "Method":       ["No SOP defined", "Inconsistent process", "Operator discretion"],
        "Material":     ["Wrong alloy grade", "High moisture content", "Supplier variation"],
        "Man":          ["Operator fatigue", "Insufficient training", "High turnover"],
        "Measurement":  ["Wrong gauge type", "Calibration expired", "Human reading error"],
        "Environment":  ["Temperature fluctuation", "High humidity", "Contamination"],
    },
    effect="High Defect Rate (>3%)",
    color_scheme="academic",
)

print("\n✅ Example 04 complete.")
