# Project Status (Canonical)

**Project**: Neural PK-PD Modeling with Physics-Informed Neural ODEs  
**Last Updated**: March 8, 2026  
**Owner**: Subrat  
**Lifecycle State**: Phase 3 active (quality-gated optimization + threshold policy)

---

## Current Status

- Phase 1–2 pipeline is complete and reproducible.
- Phase 2→3 feature handoff is complete via processed artifact:
  - [Coding/data/processed/phase2_multitask_features_with_fingerprints.csv](../Coding/data/processed/phase2_multitask_features_with_fingerprints.csv)
- Phase 3 model pipeline executes end-to-end with timeline logging and benchmark comparability.
- Multiple controlled model variants have been benchmarked (deep-head, focal/logits, classification fine-tuning variants).
- Concrete data-quality gate, constrained threshold calibration, and production-threshold auto-policy are implemented and executed.
- Latest reportable benchmark snapshot refreshed on March 8 using locked production thresholds.

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

1. Implemented concrete Phase 3 data-quality gate checks (NaN/Inf, duplicates, leakage, drift/balance).
2. Executed task-specific classification fine-tuning variants for hERG/Caco-2.
3. Added unconstrained and constrained threshold calibration with guardrails.
4. Added automatic production-threshold policy selection and locked threshold reporting.
5. Added final report metrics section using locked thresholds only (no re-sweeping, no weight updates).

---

## Next Planned Step

- Mitigate split leakage in the Phase 3 data-quality gate (starting with binding), rerun benchmarking with the same locked-threshold reporting flow, and compare against the current March 8 snapshot.

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
