# Documentation Governance Checklist

**Purpose**: Keep project documentation synchronized after each experiment/update.

Last Updated: 22 Mar 2026

---

## Canonical Structure

Use the following structure as the stable documentation layout:

1. [README.md](README.md) - Documentation index and reading order
2. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Canonical status and milestone tracking
3. [MASTER_DATASET_REFERENCE.md](MASTER_DATASET_REFERENCE.md) - Data-source and schema reference
4. [DOCUMENTATION_GOVERNANCE.md](DOCUMENTATION_GOVERNANCE.md) - Process and quality rules

---

## Source of Truth

1. Update [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) first.
2. Treat all other documents as downstream views of the canonical status.

---

## Required Update Order (After Every New Benchmark Cycle)

1. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
   - Last updated date
   - Latest benchmark table
   - Current configuration notes
   - Next planned step
   - Quick-start text that references current phase
   - RapidDock prototype state (if changed)

2. [README.md](README.md)
   - Ensure links and reading order still match current project flow

3. [Coding/TROUBLESHOOTING_GUIDE.md](../Coding/TROUBLESHOOTING_GUIDE.md)
   - Update only if new issues/solutions arise

4. [Slides/README.md](../Slides/README.md)
   - Update only when new presentations are generated

---

## Historical Document Rules

- All dataset and integration documentation is consolidated in [MASTER_DATASET_REFERENCE.md](MASTER_DATASET_REFERENCE.md).
- Phase 3 is split into 4 notebooks: `phase3a` (features) → `phase3b` (model) → `phase3c` (fine-tuning) → `phase3d` (experiments). The original monolithic `phase3_neural_ode_model.ipynb` is preserved as an archive.
- RapidDock prototype documentation should point to `Coding/rapid_dock_transformer_demo.ipynb` and indicate whether it is exploratory or production-ready.
- Do not replace old historical metrics; annotate them as snapshots when needed.

---

## Style Conventions

- Use `Last Updated: DD Mon YYYY` near the top of each markdown document.
- Keep one canonical "current status" section in [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md).
- Prefer concise section titles and consistent separator usage (`---`).
- Preserve historical result tables; append addenda instead of overwriting prior milestones.

---

## Consistency Checks (Quick Pass)

- "Current status" phrasing appears only in [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md).
- Any old dates in summaries are labeled "Historical Snapshot".
- Latest benchmark numbers are consistent between:
   - [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) (canonical)
  - Top addenda in downstream docs
- Documentation Hub links in [README.md](README.md) resolve without path errors.

---

## Suggested Commit Message Format

`docs(status): sync <date> benchmark + refresh canonical status and summaries`

---

## Change Log

- 22 Mar 2026: Added daily execution summary to [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) and added hub-level "Latest Update" note in [README.md](README.md) to reflect completed Phase 3B/3C/3D run coverage.
