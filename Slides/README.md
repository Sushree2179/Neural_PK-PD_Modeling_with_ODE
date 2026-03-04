# Slides Generation Guide

## Canonical Generator

Use [generate_presentation.py](generate_presentation.py) as the primary script.

Run from workspace root:

`python Slides/generate_presentation.py`

Output:

- [Phase2_Phase3_Stakeholder_Deck.pptx](Phase2_Phase3_Stakeholder_Deck.pptx)

---

## Legacy / Alternate Generator

[v1_make_presentation.py](v1_make_presentation.py) is retained as an alternate version.

Run from workspace root:

`python Slides/v1_make_presentation.py`

Output:

- [Phase2_Phase3_Stakeholder_Deck_v1.pptx](Phase2_Phase3_Stakeholder_Deck_v1.pptx)

---

## Dependency

Install once in your active environment:

`pip install python-pptx`

---

## Current Content Basis

Both generators are aligned to the March 4, 2026 status update:

- Binding R²: -0.029
- hERG AUROC: 0.482
- Caco-2 AUROC: 0.518
- Clearance RMSE: 0.969
