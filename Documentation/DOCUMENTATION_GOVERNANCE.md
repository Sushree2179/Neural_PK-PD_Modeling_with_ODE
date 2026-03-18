# Documentation Governance Checklist

**Purpose**: Keep project documentation synchronized after each experiment/update.

---

## Source of Truth

1. Update [Documentation/PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) first.
2. Treat all other documents as downstream views of the canonical status.

---

## Required Update Order (After Every New Benchmark Cycle)

1. [Documentation/PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
   - Last updated date
   - Latest benchmark table
   - Current configuration notes
   - Next planned step
   - Quick-start text that references current phase

2. [Coding/TROUBLESHOOTING_GUIDE.md](../Coding/TROUBLESHOOTING_GUIDE.md)
   - Update only if new issues/solutions arise

3. [Slides/README.md](../Slides/README.md)
   - Update only when new presentations are generated

---

## Historical Document Rules

- All dataset and integration documentation is consolidated in [MASTER_DATASET_REFERENCE.md](MASTER_DATASET_REFERENCE.md).
- Phase 3 is split into 4 notebooks: `phase3a` (features) → `phase3b` (model) → `phase3c` (fine-tuning) → `phase3d` (experiments). The original monolithic `phase3_neural_ode_model.ipynb` is preserved as an archive.
- Do not replace old historical metrics; annotate them as snapshots when needed.

---

## Consistency Checks (Quick Pass)

- "Current status" phrasing appears only in [Documentation/PROJECT_SUMMARY.md](PROJECT_SUMMARY.md).
- Any old dates in summaries are labeled "Historical Snapshot".
- Latest benchmark numbers are consistent between:
  - [Documentation/PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) (canonical)
  - Top addenda in downstream docs

---

## Suggested Commit Message Format

`docs(status): sync <date> benchmark + refresh canonical status and summaries`
