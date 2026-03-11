# Slides Generation Guide

## Current Canonical Generator (Section 15 — All Targets Met)

Use `generate_presentation_v2.py` as the primary script.

Run from workspace root:

`python Slides/generate_presentation_v2.py`

Output: `Phase3_Sections12to15_Deck.pptx` — 31-slide deck covering the Section 12→15 journey.

---

## Legacy Generator (pre-Section-12 baseline)

`generate_presentation.py` — retained for historical reference.  
Output: `Phase2_Phase3_Stakeholder_Deck.pptx`

---

## Oldest Version

`v1_make_presentation.py` — earliest draft.  
Output: `Phase2_Phase3_Stakeholder_Deck_v1.pptx`

---

## Dependency

Install once in your active environment:

`pip install python-pptx`

---

## Current Content Basis (generate_presentation_v2.py)

Locked to Section 15 final results — March 8, 2026:

| Task                | Metric | Result | Target | Status |
|---------------------|--------|--------|--------|--------|
| hERG Inhibition     | AUROC  | 0.8206 | > 0.80 | ✅ Met |
| Caco-2 Permeability | AUROC  | 0.8635 | > 0.75 | ✅ Met |
| Clearance           | R²     | 0.3478 | > 0.20 | ✅ Met |
| Binding Affinity    | R²     | 0.4521 | > 0.40 | ✅ Met |

- Model: `model_15` — `hidden_dim=256`, `pos_weight=1.5`, `input_dim=2050` (2048-bit Morgan FP radius=2)
- Parameters: 623,078
- Dataset: `phase2_multitask_features_with_binding_fps.csv` — 12,289 rows × 2,053 cols
- Locked thresholds: hERG=0.49, Caco-2=0.50
- Next: Section 16 — Neural ODE PK/PD integration (`torchdiffeq`)

- https://teams.microsoft.com/l/message/19:1ca21585-37d5-465c-bfd3-e2a5024dfdce_c5e61a9c-c484-4404-a8db-a24eea1cfe99@unq.gbl.spaces/1772542642575?context=%7B%22contextType%22%3A%22chat%22%7D
