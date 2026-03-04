# Project Status (Canonical)

**Project**: Neural PK-PD Modeling with Physics-Informed Neural ODEs  
**Last Updated**: March 4, 2026  
**Owner**: Subrat  
**Lifecycle State**: Phase 3 active (optimization + benchmarking)

---

## Current Status

- Phase 1–2 pipeline is complete and reproducible.
- Phase 2→3 feature handoff is complete via processed artifact:
  - [Coding/data/processed/phase2_multitask_features_with_fingerprints.csv](../Coding/data/processed/phase2_multitask_features_with_fingerprints.csv)
- Phase 3 model pipeline executes end-to-end with timeline logging and benchmark comparability.
- Multiple controlled model variants have been benchmarked (deep-head, focal, logits).

---

## Latest Benchmark Snapshot

| Task | Metric | Latest Result | Target | Status |
|------|--------|---------------|--------|--------|
| Binding Affinity | R² | -0.029 | > 0.60 | ✗ |
| hERG Inhibition | AUROC | 0.482 | > 0.80 | ✗ |
| Caco-2 Permeability | AUROC | 0.518 | > 0.75 | ✗ |
| Hepatocyte Clearance | RMSE | 0.969 | < 1.00 | ✓ |

---

## Active Feature/Model Configuration

- Input features: **258** (`2 physico + 256 fingerprint`)
- Core architecture: shared encoder + task heads + Neural ODE PK component
- Classification path: logits-based variants tested with focal/BCE-with-logits and threshold tuning

---

## What Was Completed Recently

1. Fixed missing fingerprint integration in Phase 2 matrix generation.
2. Migrated Phase 3 to consume processed Phase 2 matrix directly.
3. Aligned Caco-2 objective/metric reporting with current benchmark track.
4. Executed and compared multiple controlled training variants.

---

## Next Planned Step

- Run task-specific fine-tuning for hERG/Caco-2 with frozen shared encoder and compare AUROC/F1/threshold behavior against current benchmark.

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
