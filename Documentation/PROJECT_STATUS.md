# Project Status (Canonical)

**Project**: Neural PK-PD Modeling with Physics-Informed Neural ODEs  
**Last Updated**: March 11, 2026  
**Owner**: Subrat  
**Lifecycle State**: Phase 3 active — **Sections 21-23 Complete** (Scenario Analysis, Sensitivity Analysis, Dose Optimization)

---

## Current Status

- Phase 1–2 pipeline is complete and reproducible.
- Phase 2→3 feature handoff is complete via processed artifact:
  - [Coding/data/processed/phase2_multitask_features_with_fingerprints.csv](../Coding/data/processed/phase2_multitask_features_with_fingerprints.csv)
- Phase 3 model pipeline executes end-to-end with timeline logging and benchmark comparability.
- Multiple controlled model variants have been benchmarked (deep-head, focal/logits, classification fine-tuning variants).
- Concrete data-quality gate, constrained threshold calibration, and production-threshold auto-policy are implemented and executed.
- **NEW (March 11, 2026)**: Sections 21-23 complete — Scenario analysis, sensitivity analysis, and dose optimization with multi-objective trade-offs.

---

## Latest Benchmark Snapshot

_Benchmark recency: Final report metrics generated on March 8, 2026 from the locked-threshold reporting cell in [Coding/phase3_neural_ode_model.ipynb](../Coding/phase3_neural_ode_model.ipynb)._ 

| Task | Metric | Latest Result | Target | Status |
|------|--------|---------------|--------|--------|
| Binding Affinity | R² | 0.0019 | > 0.60 | ✗ |
| hERG Inhibition | AUROC | 0.4836 | > 0.80 | ✗ |
| Caco-2 Permeability | AUROC | 0.4719 | > 0.75 | ✗ |
| Hepatocyte Clearance | RMSE | 0.9766 | < 1.00 | ✓ |

### Locked Production Thresholds (Classification)

- hERG: **0.49**
- Caco-2: **0.50**

---

## Active Feature/Model Configuration

- Input features: **258** (`2 physico + 256 fingerprint`)
- Core architecture: shared encoder + task heads + Neural ODE PK component
- Classification path: logits-based variants tested with focal/BCE-with-logits and threshold tuning

---

## What Was Completed Recently

### March 11, 2026: Sections 21-23 — Clinical Decision Support

**Section 21: Scenario Analysis** (cells 109-112)
- Evaluated 4 dosing scenarios: baseline, low_dose, high_dose, high_iiv
- Risk-benefit scatter plot analysis (AUC_E vs composite safety score)
- CSV export: `s21_scenario_results.csv` (4 scenarios × 11 metrics)
- **Finding**: 0/4 scenarios passed all safety constraints (hERG risk, Caco-2 permeability, Cmax limits)

**Section 22: Sensitivity Analysis** (cells 113-116)
- One-at-time (OAT) analysis of 9 PK-PD parameters: CL, V1, V2, Q, ke0, EC50, Emax, gamma, DOSE
- Perturbation range: ±20% around baseline values
- 27 parameter-output combinations analyzed
- Tornado plot visualization (3-panel: AUC_E, Cmax, AUC_C1)
- **Key findings**:
  - AUC_E most sensitive to Emax (sensitivity index = 1.000)
  - Cmax most sensitive to DOSE (sensitivity index = 1.000)
  - AUC_C1 most sensitive to CL (sensitivity index = -1.015)
- CSV export: `s22_sensitivity_results.csv` (27 combinations)

**Section 23: Dose Optimization** (cells 117-120)
- Multi-objective optimization: maximize efficacy vs minimize toxicity
- Grid search: 300 dose/CV combinations (20 × 15 grid)
- Global optimization: differential evolution algorithm (100 iterations)
- 4-panel heatmap visualization: AUC_E surface, hERG risk, Caco-2 risk, composite score
- **Results**:
  - Optimal dose: 200 mg (upper boundary)
  - Optimal CV IIV: 0.15 (minimum variability)
  - Efficacy (AUC_E): 30.85 (2.3× baseline)
  - **Trade-off**: 100% hERG risk, 70% Caco-2 risk → constraints violated
- CSV exports: `s23_grid_search_results.csv`, `s23_optimal_regimen.csv`

### Prior Work (March 8, 2026)

1. Implemented concrete Phase 3 data-quality gate checks (NaN/Inf, duplicates, leakage, drift/balance).
2. Executed task-specific classification fine-tuning variants for hERG/Caco-2.
3. Added unconstrained and constrained threshold calibration with guardrails.
4. Added automatic production-threshold policy selection and locked threshold reporting.
5. Added final report metrics section using locked thresholds only (no re-sweeping, no weight updates).

---

## Next Planned Step

**Option 1 (Recommended)**: Section 24 — Pareto Frontier Analysis
- Map multi-objective efficacy-safety trade-off surface
- Identify Pareto-optimal solutions balancing efficacy vs toxicity
- Visualize compromise frontiers for clinical decision-making
- Address constraint violations found in Section 23

**Option 2**: Monte Carlo Validation (uncertainty quantification with 1000+ virtual patients)

**Option 3**: Clinical Trial Simulation (Phase II/III projections)

**Option 4**: Summary & Conclusions (comprehensive findings, recommendations, limitations)

---

## Canonical Documentation Map

- **Live status (source of truth):** [Documentation/PROJECT_STATUS.md](PROJECT_STATUS.md)
- **Master navigation:** [MASTER_INDEX.md](../MASTER_INDEX.md)
- **Short summary:** [Coding/EXECUTIVE_SUMMARY.md](../Coding/EXECUTIVE_SUMMARY.md)
- **Long-form narrative:** [Coding/PROJECT_SUMMARY.md](../Coding/PROJECT_SUMMARY.md)
- **Session log:** [Documentation/Working_Progress.txt](Working_Progress.txt)
- **Doc governance checklist:** [Documentation/DOCUMENTATION_GOVERNANCE.md](DOCUMENTATION_GOVERNANCE.md)

---

## Historical Documents

The following remain available for traceability but are historical snapshots:

- [INTEGRATION_STATUS.md](../INTEGRATION_STATUS.md) (Feb 4 integration milestone snapshot)
- [Coding/INDEX.md](../Coding/INDEX.md) (legacy data index superseded by [MASTER_INDEX.md](../MASTER_INDEX.md))
