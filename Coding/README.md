# Coding Folder Guide

This folder contains the notebooks, scripts, artifacts, and data used to build the thesis workflow.

## Recommended Notebook Order

1. `data_download_pipeline.ipynb`
   Download and consolidate raw public-source datasets.

2. `phase1_2_data_exploration.ipynb`
   Exploratory analysis, source inspection, and initial dataset understanding.

3. `phase3a_feature_engineering.ipynb`
   Build harmonized features, quality checks, and Phase 3A artifacts.

4. `phase3b_model_design.ipynb`
   Define the baseline multi-task Neural ODE architecture and run initial training.

5. `phase3c_finetuning.ipynb`
   Fine-tuning, threshold calibration, and leakage-mitigation work.

6. `phase3d_experiments.ipynb`
   Full experimental program: PK-PD simulation, sensitivity analysis, Pareto studies, Monte Carlo validation, clinical trial simulation, and interpretation.

## Auxiliary / Prototype Notebooks

- `rapid_dock_paper_aligned_prototype.ipynb`
   Prototype branch aligned with the RapidDock-style geometry workflow and the thesis narrative.

- `prototypes/rapid_dock_transformer_demo.ipynb`
   Early legacy demonstration notebook. Useful for experimentation and historical reference, but not part of the main thesis execution path.

## Supporting Scripts

- `generate_thesis_figures.py`
- `export_thesis_figures.py`

Use these for exporting figures outside the notebook flow.

## Artifacts and Data

- `data/raw/`
  Downloaded and source-level files.

- `data/processed/`
  Harmonized features and saved artifacts for later phases.

- `data/outputs/`
  Result tables, exported summaries, and downstream analysis outputs.

## Cleanup Notes

- Presentation-only cells were removed from `phase3b_model_design.ipynb` so the notebook remains focused on model design, training, and artifact generation.
- `phase1_2_data_exploration.ipynb` now resolves the nearest `Coding/data` root dynamically, which makes later notebook reorganization safer.
- `phase3a_feature_engineering.ipynb` now resolves Phase 2 inputs and Phase 3A artifact output paths from the nearest `Coding/data` root.
- `phase3b_model_design.ipynb` now resolves Phase 3A artifacts, bridge inputs, checkpoints, figure exports, and Phase 3B artifact outputs from the nearest `Coding/data` root.
- `phase3c_finetuning.ipynb` now resolves Phase 3A/3B artifact inputs, fine-tuning checkpoints, and Phase 3C artifact outputs from the nearest `Coding/data` root.
- `phase3d_experiments.ipynb` now resolves Phase 3A/3B/3C artifacts, rebuilt training checkpoints, and the main figure/CSV export destinations from the nearest `Coding/data` root.
- Execution-timeline summary sections were removed from `phase3c_finetuning.ipynb` and `phase3d_experiments.ipynb` because they were debug-oriented rather than part of the thesis workflow.
- `prototypes/rapid_dock_transformer_demo.ipynb` was relabeled in-notebook as a legacy exploratory reference so it is less likely to be confused with the thesis-aligned execution path.
- Stored outputs were cleared from `prototypes/rapid_dock_transformer_demo.ipynb` to reduce notebook weight while preserving all source cells.
- Generated images such as `training_history.png` and `pk_curves.png` are runtime artifacts from Phase 3B and can be regenerated from the notebook if needed.
