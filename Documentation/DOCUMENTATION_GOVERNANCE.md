# Documentation Governance Checklist

**Purpose**: Keep project documentation synchronized after each experiment/update.

---

## Source of Truth

1. Update [Documentation/PROJECT_STATUS.md](PROJECT_STATUS.md) first.
2. Treat all other summaries as downstream views of the canonical status.

---

## Required Update Order (After Every New Benchmark Cycle)

1. [Documentation/PROJECT_STATUS.md](PROJECT_STATUS.md)
   - Last updated date
   - Latest benchmark table
   - Current configuration notes
   - Next planned step

2. [MASTER_INDEX.md](../MASTER_INDEX.md)
   - Top-level status line/date
   - Any quick-start text that references current phase

3. [Coding/EXECUTIVE_SUMMARY.md](../Coding/EXECUTIVE_SUMMARY.md)
   - Add or refresh top addendum only
   - Do not overwrite historical milestone sections

4. [Coding/PROJECT_SUMMARY.md](../Coding/PROJECT_SUMMARY.md)
   - Add or refresh top addendum only
   - Preserve historical content with explicit snapshot labels

5. [Documentation/Working_Progress.txt](Working_Progress.txt)
   - Append concise run log with date, experiment tag, and outcomes

---

## Historical Document Rules

- Keep [INTEGRATION_STATUS.md](../INTEGRATION_STATUS.md) and [Coding/INDEX.md](../Coding/INDEX.md) as historical snapshots.
- If editing historical docs, keep a notice at the top that redirects to [Documentation/PROJECT_STATUS.md](PROJECT_STATUS.md).
- Do not replace old historical metrics; annotate them as snapshots when needed.

---

## Consistency Checks (Quick Pass)

- "Current status" phrasing appears only in canonical/top-level current docs.
- Any old dates in summaries are labeled "Historical Snapshot".
- Latest benchmark numbers are consistent between:
   - [Documentation/PROJECT_STATUS.md](PROJECT_STATUS.md)
   - [MASTER_INDEX.md](../MASTER_INDEX.md) (current-status sections)
  - Top addenda in summary docs

---

## Suggested Commit Message Format

`docs(status): sync March 4 benchmark + refresh canonical status and summaries`
