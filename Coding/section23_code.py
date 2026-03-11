# ===== CELL 117 =====
# ============================================================================
# SECTION 23 - CELL A: Dose Optimization Setup
# ============================================================================
# Multi-objective dose optimization:
# - Maximize efficacy (AUC_E)
# - Minimize toxicity (hERG risk, Caco-2 issues)
# - Constrain Cmax to safe range
# - Search optimal dose and IIV combinations
# ============================================================================

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize, differential_evolution
from pathlib import Path
import matplotlib.pyplot as plt

print("=" * 70)
print("  SECTION 23: DOSE OPTIMIZATION")
print("=" * 70)
print()

# Verify previous sections
if 'calibration_22' not in globals():
    raise RuntimeError("Section 22 incomplete. Run Section 22 cells first.")

# Define optimization objectives and constraints
optimization_config_23 = {
    'objectives': {
        'maximize_efficacy': True,      # Maximize AUC_E
        'minimize_herg_risk': True,     # Minimize hERG block rate
        'minimize_caco_risk': True,     # Minimize poor permeability rate
    },
    'constraints': {
        'min_AUC_E': 12.0,             # Minimum efficacy threshold
        'max_herg_rate': 0.30,         # Max 30% hERG risk
        'max_caco_rate': 0.50,         # Max 50% poor permeability
        'max_Cmax': 150.0,             # Max Cmax (mg/L)
        'min_Cmax': 50.0,              # Min Cmax for efficacy
    },
    'search_space': {
        'dose_range': (50.0, 200.0),   # mg
        'cv_iiv_range': (0.15, 0.50),  # Coefficient of variation
    },
}

# Objective function: composite score
def evaluate_dose_regimen(dose, cv_iiv, return_details=False):
    """
    Evaluate a dose regimen using scaling from Section 21 baseline.
    Returns negative composite score (for minimization) or full details.
    """
    # Scale from baseline (Section 21 approach)
    dose_factor = dose / base_dose
    cv_factor = cv_iiv / max(base_cv, 1e-8)
    
    # Predicted metrics (power-law scaling from Section 21)
    AUC_E_pred = base_auc_med * (dose_factor ** 0.95)
    Cmax_pred = base_cmax_med * (dose_factor ** 1.00)
    herg_rate = np.clip(base_herg * (dose_factor ** 0.75) * (cv_factor ** 0.40), 0.0, 1.0)
    caco_rate = np.clip(base_caco * (dose_factor ** -0.30) * (cv_factor ** 0.20), 0.0, 1.0)
    
    # Check constraints
    constraints_met = (
        AUC_E_pred >= optimization_config_23['constraints']['min_AUC_E'] and
        herg_rate <= optimization_config_23['constraints']['max_herg_rate'] and
        caco_rate <= optimization_config_23['constraints']['max_caco_rate'] and
        Cmax_pred <= optimization_config_23['constraints']['max_Cmax'] and
        Cmax_pred >= optimization_config_23['constraints']['min_Cmax']
    )
    
    # Composite score (maximize efficacy, minimize risks)
    # Higher score is better, but we'll negate for minimization
    efficacy_score = AUC_E_pred / 15.0  # Normalize
    safety_score = 1.0 - (herg_rate + caco_rate) / 2.0
    composite = efficacy_score * 0.6 + safety_score * 0.4
    
    # Heavy penalty if constraints violated
    if not constraints_met:
        penalty = 10.0
        composite -= penalty
    
    if return_details:
        return {
            'dose': dose,
            'cv_iiv': cv_iiv,
            'AUC_E': AUC_E_pred,
            'Cmax': Cmax_pred,
            'herg_rate': herg_rate,
            'caco_rate': caco_rate,
            'composite_score': composite,
            'constraints_met': constraints_met,
            'efficacy_score': efficacy_score,
            'safety_score': safety_score,
        }
    else:
        # Return negative for minimization
        return -composite

print("✅ Optimization configuration loaded")
print(f"   Objectives: {len(optimization_config_23['objectives'])}")
print(f"   Constraints: {len(optimization_config_23['constraints'])}")
print(f"   Dose range: {optimization_config_23['search_space']['dose_range']} mg")
print(f"   CV IIV range: {optimization_config_23['search_space']['cv_iiv_range']}")
print()
print("=" * 70)


# ===== CELL 118 =====
# ============================================================================
# SECTION 23 - CELL B: Grid Search & Optimization
# ============================================================================
# Perform comprehensive search for optimal dose regimen
# ============================================================================

print("🔍 Running grid search...")

# Grid search for visualization
dose_grid = np.linspace(
    optimization_config_23['search_space']['dose_range'][0],
    optimization_config_23['search_space']['dose_range'][1],
    20
)
cv_grid = np.linspace(
    optimization_config_23['search_space']['cv_iiv_range'][0],
    optimization_config_23['search_space']['cv_iiv_range'][1],
    15
)

grid_results_23 = []
for dose in dose_grid:
    for cv in cv_grid:
        result = evaluate_dose_regimen(dose, cv, return_details=True)
        grid_results_23.append(result)

grid_df_23 = pd.DataFrame(grid_results_23)

print(f"   Grid points evaluated: {len(grid_df_23)}")
print(f"   Feasible solutions: {grid_df_23['constraints_met'].sum()}")
print()

# Find best grid solution
feasible_grid = grid_df_23[grid_df_23['constraints_met']]
if len(feasible_grid) > 0:
    best_grid = feasible_grid.nlargest(1, 'composite_score').iloc[0]
    print("📊 Best Grid Solution:")
    print(f"   Dose: {best_grid['dose']:.1f} mg")
    print(f"   CV IIV: {best_grid['cv_iiv']:.3f}")
    print(f"   AUC_E: {best_grid['AUC_E']:.3f}")
    print(f"   Cmax: {best_grid['Cmax']:.1f} mg/L")
    print(f"   hERG rate: {best_grid['herg_rate']:.2%}")
    print(f"   Caco-2 rate: {best_grid['caco_rate']:.2%}")
    print(f"   Composite score: {best_grid['composite_score']:.4f}")
else:
    print("⚠️  No feasible solutions found in grid search")
    best_grid = None

print()
print("🎯 Running numerical optimization...")

# Differential evolution for global optimization
bounds_23 = [
    optimization_config_23['search_space']['dose_range'],
    optimization_config_23['search_space']['cv_iiv_range'],
]

def objective_wrapper(x):
    return evaluate_dose_regimen(x[0], x[1], return_details=False)

opt_result_23 = differential_evolution(
    objective_wrapper,
    bounds=bounds_23,
    seed=42,
    maxiter=100,
    popsize=15,
    tol=1e-4,
    atol=1e-6,
)

optimal_dose_23 = opt_result_23.x[0]
optimal_cv_23 = opt_result_23.x[1]
optimal_details_23 = evaluate_dose_regimen(optimal_dose_23, optimal_cv_23, return_details=True)

print()
print("=" * 70)
print("  🏆 OPTIMAL DOSE REGIMEN")
print("=" * 70)
print(f"Dose:             {optimal_dose_23:.2f} mg")
print(f"CV IIV:           {optimal_cv_23:.3f}")
print()
print("Predicted Outcomes:")
print(f"  AUC_E:          {optimal_details_23['AUC_E']:.3f}")
print(f"  Cmax:           {optimal_details_23['Cmax']:.2f} mg/L")
print(f"  hERG risk:      {optimal_details_23['herg_rate']:.2%}")
print(f"  Caco-2 issue:   {optimal_details_23['caco_rate']:.2%}")
print()
print(f"Composite Score:  {optimal_details_23['composite_score']:.4f}")
print(f"Constraints Met:  {'✅ YES' if optimal_details_23['constraints_met'] else '❌ NO'}")
print("=" * 70)


# ===== CELL 119 =====
# ============================================================================
# SECTION 23 - CELL C: Dose Optimization Visualization
# ============================================================================
# Create heatmaps and dose-response curves
# ============================================================================

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

fig23, axes23 = plt.subplots(2, 2, figsize=(14, 12))

# Prepare grid for contour plots
dose_mesh, cv_mesh = np.meshgrid(
    np.linspace(*optimization_config_23['search_space']['dose_range'], 50),
    np.linspace(*optimization_config_23['search_space']['cv_iiv_range'], 40)
)

# Evaluate on fine grid
AUC_E_mesh = np.zeros_like(dose_mesh)
herg_mesh = np.zeros_like(dose_mesh)
caco_mesh = np.zeros_like(dose_mesh)
composite_mesh = np.zeros_like(dose_mesh)

for i in range(dose_mesh.shape[0]):
    for j in range(dose_mesh.shape[1]):
        res = evaluate_dose_regimen(dose_mesh[i,j], cv_mesh[i,j], return_details=True)
        AUC_E_mesh[i,j] = res['AUC_E']
        herg_mesh[i,j] = res['herg_rate']
        caco_mesh[i,j] = res['caco_rate']
        composite_mesh[i,j] = res['composite_score']

# Panel 1: AUC_E heatmap
ax = axes23[0, 0]
im1 = ax.contourf(dose_mesh, cv_mesh, AUC_E_mesh, levels=15, cmap='viridis')
ax.scatter(optimal_dose_23, optimal_cv_23, color='red', s=200, marker='*', 
           edgecolors='white', linewidths=2, label='Optimal', zorder=5)
ax.set_xlabel('Dose (mg)', fontsize=10)
ax.set_ylabel('CV IIV', fontsize=10)
ax.set_title('Efficacy (AUC_E)', fontsize=11, fontweight='bold')
plt.colorbar(im1, ax=ax)
ax.legend(loc='upper right')

# Panel 2: hERG risk heatmap
ax = axes23[0, 1]
im2 = ax.contourf(dose_mesh, cv_mesh, herg_mesh*100, levels=15, cmap='Reds')
ax.scatter(optimal_dose_23, optimal_cv_23, color='blue', s=200, marker='*', 
           edgecolors='white', linewidths=2, label='Optimal', zorder=5)
ax.set_xlabel('Dose (mg)', fontsize=10)
ax.set_ylabel('CV IIV', fontsize=10)
ax.set_title('hERG Risk (%)', fontsize=11, fontweight='bold')
plt.colorbar(im2, ax=ax)
ax.legend(loc='upper right')

# Panel 3: Caco-2 rate heatmap
ax = axes23[1, 0]
im3 = ax.contourf(dose_mesh, cv_mesh, caco_mesh*100, levels=15, cmap='Oranges')
ax.scatter(optimal_dose_23, optimal_cv_23, color='blue', s=200, marker='*', 
           edgecolors='white', linewidths=2, label='Optimal', zorder=5)
ax.set_xlabel('Dose (mg)', fontsize=10)
ax.set_ylabel('CV IIV', fontsize=10)
ax.set_title('Caco-2 Poor Permeability (%)', fontsize=11, fontweight='bold')
plt.colorbar(im3, ax=ax)
ax.legend(loc='upper right')

# Panel 4: Composite score heatmap
ax = axes23[1, 1]
im4 = ax.contourf(dose_mesh, cv_mesh, composite_mesh, levels=15, cmap='RdYlGn')
ax.scatter(optimal_dose_23, optimal_cv_23, color='darkblue', s=200, marker='*', 
           edgecolors='white', linewidths=2, label='Optimal', zorder=5)
ax.set_xlabel('Dose (mg)', fontsize=10)
ax.set_ylabel('CV IIV', fontsize=10)
ax.set_title('Composite Score', fontsize=11, fontweight='bold')
plt.colorbar(im4, ax=ax)
ax.legend(loc='upper right')

plt.tight_layout()

# Save figure
out_path_23 = Path("data/raw/s23_dose_optimization.png")
fig23.savefig(out_path_23, dpi=150, bbox_inches='tight')
print(f"✅ Dose optimization heatmaps saved: {out_path_23}")
plt.show()

# Export optimization results
opt_summary_23 = pd.DataFrame([optimal_details_23])
csv_path_23 = Path("data/raw/s23_optimal_regimen.csv")
opt_summary_23.to_csv(csv_path_23, index=False)
print(f"✅ Optimal regimen exported: {csv_path_23}")

# Also save grid search results
grid_csv_23 = Path("data/raw/s23_grid_search_results.csv")
grid_df_23.to_csv(grid_csv_23, index=False)
print(f"✅ Grid search results exported: {grid_csv_23}")


# ===== CELL 120 =====
# ============================================================================
# SECTION 23 - CELL D: Wrap-Up
# ============================================================================
# Summary of dose optimization and clinical recommendations
# ============================================================================

print("=" * 70)
print("  SECTION 23 COMPLETE: Dose Optimization")
print("=" * 70)
print()
print("📊 Artifacts Generated:")
print(f"   1. Optimization heatmaps: data/raw/s23_dose_optimization.png")
print(f"   2. Optimal regimen CSV: data/raw/s23_optimal_regimen.csv")
print(f"   3. Grid search results: data/raw/s23_grid_search_results.csv")
print()

print("💊 Clinical Recommendations:")
print(f"   Recommended Dose: {optimal_dose_23:.0f} mg")
print()
print("   Risk-Benefit Assessment:")
improvement_vs_baseline = (
    (optimal_details_23['composite_score'] - 
     evaluate_dose_regimen(base_dose, base_cv, return_details=True)['composite_score']) /
    evaluate_dose_regimen(base_dose, base_cv, return_details=True)['composite_score'] * 100
)
print(f"   - Improvement vs baseline: {improvement_vs_baseline:+.1f}%")
print(f"   - Efficacy score: {optimal_details_23['efficacy_score']:.3f}")
print(f"   - Safety score: {optimal_details_23['safety_score']:.3f}")
print()

# Comparison table
comparison_23 = pd.DataFrame([
    {
        'Regimen': 'Baseline',
        'Dose (mg)': base_dose,
        'CV IIV': base_cv,
        'AUC_E': base_auc_med,
        'Cmax (mg/L)': base_cmax_med,
        'hERG risk': f"{base_herg:.2%}",
        'Caco-2 issue': f"{base_caco:.2%}",
    },
    {
        'Regimen': 'Optimized',
        'Dose (mg)': optimal_dose_23,
        'CV IIV': optimal_cv_23,
        'AUC_E': optimal_details_23['AUC_E'],
        'Cmax (mg/L)': optimal_details_23['Cmax'],
        'hERG risk': f"{optimal_details_23['herg_rate']:.2%}",
        'Caco-2 issue': f"{optimal_details_23['caco_rate']:.2%}",
    },
])

print("📋 Baseline vs Optimized Comparison:")
display(comparison_23)

# Store results
calibration_23 = {
    'section': 23,
    'optimal_dose': optimal_dose_23,
    'optimal_cv': optimal_cv_23,
    'optimal_details': optimal_details_23,
    'grid_results': grid_df_23.copy(),
    'optimization_config': optimization_config_23,
    'heatmap_path': str(out_path_23),
    'optimal_csv': str(csv_path_23),
    'section23_complete': True,
}

print()
print("✅ Section 23 calibration dict created")
print("✅ Dose optimization complete")
print("=" * 70)


