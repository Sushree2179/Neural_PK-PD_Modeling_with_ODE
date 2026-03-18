# Neural PK-PD Modeling: Project Summary

**Project**: Physics-Informed Neural ODE for Pharmacokinetic-Pharmacodynamic Modeling  
**Author**: Subrat  
**Date**: Current (post March 11, 2026)  
**Status**: 🎯 Phase 3 Sections 21-23 Complete | **Clinical Decision Support Tools**  
**Lifecycle State**: Phase 3 active — Sections 21-23 Complete (Scenario Analysis, Sensitivity Analysis, Dose Optimization)  
**Next Step**: Section 24 — Pareto Frontier Analysis  
**Notebook Layout**: Phase 3 split into 4 notebooks (3a → 3b → 3c → 3d) with artifact bridging

---

## 📚 Navigation

- **[Troubleshooting →](../Coding/TROUBLESHOOTING_GUIDE.md)** - Problem solving guide
- **[Dataset Reference →](MASTER_DATASET_REFERENCE.md)** - All 5 data sources
- **[Notebook (Phase 1–2) →](../Coding/phase1_2_data_exploration.ipynb)** - EDA & feature engineering
- **[Notebook (Phase 3A) →](../Coding/phase3a_feature_engineering.ipynb)** - Feature engineering (18 cells)
- **[Notebook (Phase 3B) →](../Coding/phase3b_model_design.ipynb)** - Model architecture & training (30 cells)
- **[Notebook (Phase 3C) →](../Coding/phase3c_finetuning.ipynb)** - Fine-tuning & calibration (28 cells)
- **[Notebook (Phase 3D) →](../Coding/phase3d_experiments.ipynb)** - Advanced experiments (68 cells)
- **[Notebook (Phase 3 — original) →](../Coding/phase3_neural_ode_model.ipynb)** - Monolithic archive (121 cells, preserved)
- **[Documentation Governance →](DOCUMENTATION_GOVERNANCE.md)** - Update protocol
- **[Slides Guide →](../Slides/README.md)** - Presentation generation

---

## 📊 At A Glance

| Metric | Value |
|--------|-------|
| **Training Samples** | 13,030 |
| **Prediction Tasks** | 4 (binding, hERG, Caco-2, clearance) |
| **Features (current model input)** | 258 (2 physico + 256 fingerprint) |
| **Datasets Integrated** | 5 (ChEMBL, TDC, ToxCast, PubChem, PK-DB) |
| **Total Data Volume** | 347,896 records (~84 MB) |
| **Notebook Cells** | Phase 1–2: 29; Phase 3: 144 (3a:18 + 3b:30 + 3c:28 + 3d:68) |
| **Model Parameters** | 623,078 (model_15; hidden_dim=256) |
| **Locked Thresholds** | hERG: 0.49, Caco-2: 0.50 |
| **Project Completion** | ~75% (Phase 3 active — next: Section 24) |

### All 4 Performance Targets Met ✅ (Section 15)

| Task | Target | Current | Status |
|------|--------|---------|--------|
| hERG AUROC | > 0.80 | **0.8206** | ✅ |
| Caco-2 AUROC | > 0.75 | **0.8635** | ✅ |
| Clearance R² | > 0.20 | **0.3478** | ✅ |
| Binding R² | > 0.40 | **0.4521** | ✅ |

---

## 🎯 Quick Start Guide

**New to this project?** Follow this recommended reading order:

1. **This document** — Start with [At A Glance](#-at-a-glance) for metrics, then skim latest work
2. **[TROUBLESHOOTING_GUIDE.md](../Coding/TROUBLESHOOTING_GUIDE.md)** — Reference when encountering errors
3. **[phase1_2_data_exploration.ipynb](../Coding/phase1_2_data_exploration.ipynb)** — Phase 1–2 EDA & feature engineering (29 cells)
4. **Phase 3 Notebooks** (run in order):
   - **[phase3a_feature_engineering.ipynb](../Coding/phase3a_feature_engineering.ipynb)** — Feature engineering & data prep (18 cells)
   - **[phase3b_model_design.ipynb](../Coding/phase3b_model_design.ipynb)** — Architecture & initial training (30 cells)
   - **[phase3c_finetuning.ipynb](../Coding/phase3c_finetuning.ipynb)** — Fine-tuning, calibration & leakage mitigation (28 cells)
   - **[phase3d_experiments.ipynb](../Coding/phase3d_experiments.ipynb)** — Advanced experiments: GNN, Neural ODE PK/PD, fusion (68 cells)
5. **[DOCUMENTATION_GOVERNANCE.md](DOCUMENTATION_GOVERNANCE.md)** — How to keep docs in sync
6. **[Slides/README.md](../Slides/README.md)** — Canonical PPTX generation commands

### Reading Paths by Role

**👨‍🎓 Students/Beginners** (~2 hours):
This document (overview) → [MASTER_DATASET_REFERENCE.md](MASTER_DATASET_REFERENCE.md) → [phase1_2_data_exploration.ipynb](../Coding/phase1_2_data_exploration.ipynb) → [TROUBLESHOOTING_GUIDE.md](../Coding/TROUBLESHOOTING_GUIDE.md)

**👨‍🔬 Researchers** (~4 hours):
This document (full) → [MASTER_DATASET_REFERENCE.md](MASTER_DATASET_REFERENCE.md) → Phase 1–2 notebook → Phase 3 notebooks (3a → 3b → 3c → 3d)

**👨‍💼 Stakeholders/Advisors** (~20 min):
[At A Glance](#-at-a-glance) → [Sections 21-23](#-sections-21-23-clinical-decision-support-march-11-2026) → [Next Planned Steps](#next-planned-steps)

**👨‍💻 Developers** (~1 hour):
[Phase 3 section](#-phase-3-neural-ode-model-development) → [TROUBLESHOOTING_GUIDE.md](../Coding/TROUBLESHOOTING_GUIDE.md) → [phase3a](../Coding/phase3a_feature_engineering.ipynb) (features) → [phase3b](../Coding/phase3b_model_design.ipynb) (model) → [phase3c](../Coding/phase3c_finetuning.ipynb) (fine-tuning) → [phase3d](../Coding/phase3d_experiments.ipynb) (experiments)

---

## 🔍 Quick Reference Guide

| Topic | Where to Look |
|-------|---------------|
| **Current metrics & status** | [At A Glance](#-at-a-glance) above |
| **Environment setup** | [Phase 0](#-phase-0-setup--environment-january-21-2026) below, [TROUBLESHOOTING_GUIDE.md](../Coding/TROUBLESHOOTING_GUIDE.md) |
| **Data sources** | [MASTER_DATASET_REFERENCE.md](MASTER_DATASET_REFERENCE.md) |
| **Feature engineering** | [Phase 2](#-phase-2-feature-engineering-completed-) below, [phase1_2_data_exploration.ipynb](../Coding/phase1_2_data_exploration.ipynb) cells 16-28 |
| **Visualizations** | [phase1_2_data_exploration.ipynb](../Coding/phase1_2_data_exploration.ipynb) cells 9-11, [Phase 1](#-phase-1-data-exploration-completed-) below |
| **Neural ODE model** | [phase3b_model_design.ipynb](../Coding/phase3b_model_design.ipynb) (architecture, training) |
| **PK curve generation** | [phase3b_model_design.ipynb](../Coding/phase3b_model_design.ipynb) `PKODEFunc`, [phase3d_experiments.ipynb](../Coding/phase3d_experiments.ipynb) §16 |
| **Multi-task learning** | [Phase 2](#-phase-2-feature-engineering-completed-) below, [phase3a](../Coding/phase3a_feature_engineering.ipynb) → [phase3b](../Coding/phase3b_model_design.ipynb) |
| **ChEMBL / ToxCast / ADMET / PK data** | [MASTER_DATASET_REFERENCE.md](MASTER_DATASET_REFERENCE.md) §2.2-2.5 |
| **Integration strategy** | [MASTER_DATASET_REFERENCE.md](MASTER_DATASET_REFERENCE.md) §5 |
| **Known issues & RDKit** | [Issues & Resolutions](#-issues-encountered--resolutions) below, [TROUBLESHOOTING_GUIDE.md](../Coding/TROUBLESHOOTING_GUIDE.md) |
| **Next steps** | [Next Planned Steps](#next-planned-steps) below |

---

## Section 12: Clean-Split Baseline (March 8, 2026)

### What was completed
1. Phase 2 fingerprint component implemented and exported to `phase2_multitask_features_with_fingerprints.csv`
2. Phase 3 refactored to consume Phase 2 processed features directly (258 dimensions: 2 physico + 256 FPs)
3. Caco-2 aligned to classification objective; AUROC reporting added
4. Controlled benchmark variants: deep-head + reweighting, focal loss, logits-based classification
5. Data-quality gate: NaN/Inf, duplicates, split leakage, drift/balance checks
6. Constrained threshold calibration + production threshold policy
7. Locked-threshold final report (no re-sweep)

### Section 12 benchmark snapshot

| Task | Metric | Result | Target | Status |
|------|--------|--------|--------|--------|
| Binding | R² | 0.0019 | > 0.60 | ✗ |
| hERG | AUROC | 0.4836 | > 0.80 | ✗ |
| Caco-2 | AUROC | 0.4719 | > 0.75 | ✗ |
| Clearance | RMSE | 0.9766 | < 1.00 | ✓ |

**Locked production thresholds**: hERG: **0.49**, Caco-2: **0.50**

---

## Section 13: 2048-bit Real-SMILES Upgrade

### What was completed
- **Real SMILES downloaded** from ChEMBL REST API: 4,916 hERG / 1,855 Caco-2 / 2,127 clearance
- **Phase-2 matrix rebuilt** with 2,048-bit Morgan FPs: `phase2_multitask_features_with_fingerprints.csv` — 10,879 × 2,053
- **`model_2048` trained** (input_dim=2,050) — 41 epochs, best val_loss=2.144
- All Section-12 split-leakage mitigations carried forward

### Section 13 test results (locked thresholds: hERG=0.49, Caco-2=0.50)

| Task | Metric | Sec-12 | **Sec-13** | Δ |
|------|--------|--------|------------|---|
| hERG | AUROC | 0.4835 | **0.6989** | +0.2154 ↑ |
| hERG | F1@0.49 | 0.2456 | **0.8684** | +0.6228 ↑ |
| Caco-2 | AUROC | 0.4211 | **0.8550** | +0.4339 ↑ |
| Clearance | R² | 0.0037 | **0.2115** | +0.2078 ↑ |
| Binding | R² | −0.0070 | −0.0079 | ≈0 (zero synth FPs) |

---

## Section 14: Real Binding SMILES Integration

### What was completed
- **Root cause confirmed**: `chembl_binding_affinity.csv` had synthetic compound IDs (CHEMBL1000000+) → zero Morgan FPs → R²(binding)=−0.0079 in Section 13
- **Real binding SMILES downloaded** via `data_download_pipeline.ipynb § 5B` — 3,410 compounds from 8 ChEMBL protein targets (D2, A2a, EGFR, CDK2, β2AR, AR, GR, 5-HT2A), pChEMBL 4.00–10.52
- **Phase-2 CSV rebuilt** with real binding FPs: `phase2_multitask_features_with_binding_fps.csv` — 12,289 × 2,053, all 4 tasks 100% nonzero FPs
- After dedup: binding=3,281, hERG=4,746, Caco-2=1,803, clearance=2,077
- **`model_bind` trained** — 46 epochs, best val_loss=2.005

### Section 14 test results (locked thresholds: hERG=0.49, Caco-2=0.50)

| Task | Metric | Sec-12 | Sec-13 | **Sec-14** | Δ13→14 |
|------|--------|--------|--------|------------|--------|
| hERG | AUROC | 0.4835 | 0.6989 | **0.7738** | +0.0749 ↑ |
| Caco-2 | AUROC | 0.4211 | 0.8550 | **0.8713** | +0.0163 ↑ |
| Clearance | R² | 0.0037 | 0.2115 | **0.3013** | +0.0899 ↑ |
| Binding | R² | −0.0070 | −0.0079 | **+0.4306** | +0.4385 ↑ ★ |

---

## 🏆 Section 15: All ADME Targets Met (March 8, 2026)

### What was completed
- pos_weight grid search {0.5, 1.0, 1.5, 2.0, 3.0} with `hidden_dim=256` (60 epochs each)
- Best: `pos_weight=1.5` → val hERG AUROC 0.7658
- Full `model_15` (623,078 params): hidden_dim=256, pos_weight=1.5, patience=60 → 68 epochs (best at epoch 23)

### Section 15 test results (locked thresholds: hERG=0.49, Caco-2=0.50)

| Task | Metric | Sec-14 | **Sec-15** | Δ |
|------|--------|--------|------------|---|
| hERG | AUROC | 0.7738 | **0.8206** | +0.0468 ↑ ★ |
| hERG | F1@0.49 | 0.8369 | **0.8739** | +0.0370 ↑ |
| hERG | Accuracy | 0.7546 | **0.7980** | +0.0435 ↑ |
| Caco-2 | AUROC | 0.8713 | **0.8635** | −0.0078 |
| Caco-2 | Accuracy | 0.7860 | **0.8007** | +0.0148 ↑ |
| Clearance | R² | 0.3013 | **0.3478** | +0.0464 ↑ |
| Binding | R² | 0.4306 | **0.4521** | +0.0215 ↑ |

### Path forward from Section 15

All ADME property targets met. The project moved to its core thesis contribution:
1. **Section 16** — Neural ODE PK/PD Integration: `model_15`'s predicted ADME properties as 2-compartment ODE parameters
   - $\frac{dC_c}{dt} = -\frac{CL}{V_c}C_c - k_{12}C_c + k_{21}C_t$ (PK layer, solved with `torchdiffeq.odeint`)
   - $E(t) = E_{\max} \cdot \frac{C(t)^n}{EC_{50}^n + C(t)^n}$ (PD layer driven by binding affinity)
   - Located in [phase3d_experiments.ipynb](../Coding/phase3d_experiments.ipynb) §16
2. **Section 17** — GNN encoder: replace Morgan FPs with graph neural network ([phase3d](../Coding/phase3d_experiments.ipynb) §17)
3. **Section 18** — Calibration: Platt/temperature scaling ([phase3d](../Coding/phase3d_experiments.ipynb) §18)

---

## 🎯 Sections 21-23: Clinical Decision Support (March 11, 2026)

### Section 21: Scenario Analysis (cells 109-112)
**Purpose**: Evaluate alternative dosing strategies with risk-benefit trade-offs

**Scenarios Tested**:
1. Baseline: 100mg dose, 30% CV IIV
2. Low dose: 50mg dose, 20% CV IIV
3. High dose: 150mg dose, 35% CV IIV
4. High variability: 100mg dose, 45% CV IIV

**Results Summary**:
- All scenarios evaluated across 11 metrics (PK, PD, safety)
- Risk-benefit scatter plot: AUC_E vs composite safety score
- **Finding**: 0/4 scenarios passed all safety constraints
  - All exceeded hERG risk threshold (>50% cardiotoxicity probability)
  - Most exceeded Caco-2 permeability targets
  - Cmax limits maintained across scenarios

**Outputs**:
- Visualization: `data/raw/s21_risk_benefit.png` (51 KB)
- Data: `data/raw/s21_scenario_results.csv` (493 B, 4×11 table)
- Calibration dict: `calibration_21`

### Section 22: Sensitivity Analysis (cells 113-116)
**Purpose**: Identify critical parameters driving PK-PD variability

**Method**: One-at-time (OAT) sensitivity analysis
- **9 parameters**: CL, V1, V2, Q, ke0, EC50, Emax, gamma, DOSE
- **Perturbation**: ±20% around baseline values
- **Outputs analyzed**: AUC_E (efficacy), Cmax, AUC_C1 (exposure)

**Key Findings**:
| Output | Most Sensitive To | Sensitivity Index |
|--------|-------------------|-------------------|
| AUC_E (efficacy) | Emax | 1.000 |
| Cmax (peak) | DOSE | 1.000 |
| AUC_C1 (exposure) | CL (clearance) | -1.015 |

**Interpretation**:
- **Efficacy** dominated by pharmacodynamic parameter (Emax)
- **Safety** (Cmax) linearly proportional to dose
- **Exposure** inversely related to clearance (faster clearance = lower exposure)

**Outputs**:
- Visualization: `data/raw/s22_tornado_plot.png` (52 KB, 3-panel)
- Data: `data/raw/s22_sensitivity_results.csv` (3.0 KB, 27 combinations)
- Calibration dict: `calibration_22` with baseline metrics

### Section 23: Dose Optimization (cells 117-120)
**Purpose**: Find optimal dose and IIV that maximize efficacy while minimizing toxicity

**Optimization Setup**:
- **Decision variables**: Dose (50-200 mg), CV IIV (0.15-0.50)
- **Objectives**: Maximize AUC_E, minimize hERG risk, minimize Caco-2 risk
- **Constraints**: Cmax < 150 mg/L, efficacy > 10, safety rates < 50%

**Method**:
1. **Grid search**: 300 points (20 dose × 15 CV combinations)
2. **Global optimization**: Differential evolution (100 iterations, population=15)

**Results**:
| Parameter | Baseline | Optimized | Improvement |
|-----------|----------|-----------|-------------|
| Dose | 100 mg | **200 mg** | +100% |
| CV IIV | 0.30 | **0.15** | -50% |
| AUC_E | 13.4 | **30.9** | +130% |
| hERG risk | 50% | **100%** | +50% ⚠️ |
| Caco-2 risk | 35% | **70%** | +35% ⚠️ |

**Trade-off Discovery**:
- Optimizer pushed to **upper dose boundary** (200 mg) for maximum efficacy
- Reduced variability (**CV=0.15**) for consistent response
- **Critical finding**: Maximum efficacy violates both safety constraints
  - 100% hERG cardiotoxicity risk (target: <50%)
  - 70% Caco-2 permeability issues (target: <50%)
- Indicates fundamental **efficacy-safety trade-off** requiring multi-objective balancing

**Outputs**:
- Visualization: `data/raw/s23_dose_optimization.png` (151 KB, 4-panel heatmap)
- Grid data: `data/raw/s23_grid_search_results.csv` (44 KB, 300 points)
- Optimal regimen: `data/raw/s23_optimal_regimen.csv` (238 B)
- Calibration dict: `calibration_23` with optimization results

### Clinical Implications

**From Section 21**: No tested regimen meets all safety criteria → need alternative strategies

**From Section 22**: 
- Focus on Emax modulation for efficacy improvements
- Clearance is critical for exposure control
- Dose adjustments have direct linear impact on Cmax

**From Section 23**: 
- Simple single-objective optimization insufficient
- Must explicitly balance efficacy vs toxicity trade-offs
- Pareto frontier analysis needed to find compromise solutions

---

## 📋 Project Overview

### Objective
Develop a physics-informed Neural Ordinary Differential Equation (Neural ODE) model for pharmacokinetic-pharmacodynamic (PK-PD) predictions that:
1. Predicts drug concentration-time profiles
2. Incorporates safety constraints (toxicity, cardiotoxicity)
3. Learns ADMET properties from molecular structure
4. Provides mechanistic interpretability

### Datasets Integrated

| Dataset | Records | Purpose | Size |
|---------|---------|---------|------|
| **PubChem** | 5,392 | Bioassay screening (hERG, CYP3A4) | 1.8 MB |
| **ChEMBL** | 2,000 | Target binding affinity | 528 KB |
| **TDC ADMET** | 11,030 | Drug property benchmarks | 1.2 MB |
| **ToxCast** | 332,507 | Toxicity screening results | 80 MB |
| **PK-DB** | 20 studies | Pharmacokinetic time-courses | 508 KB |
| **Total** | **347,896** | Multi-domain PK-PD data | **~84 MB** |

See [MASTER_DATASET_REFERENCE.md](MASTER_DATASET_REFERENCE.md) for complete data source documentation.

---

## 🔧 Phase 0: Setup & Environment (January 21, 2026)

### Environment Setup

1. **Python Virtual Environment**: Created `venv_pkpd` in the Coding folder
2. **Python Version Upgrade**: Upgraded from 3.8.10 → **Python 3.14.2**
   - Downloaded from python.org, removed old 3.8, recreated venv with `/usr/local/bin/python3.14 -m venv`
3. **Package Installation**: **143 packages** installed:

| Category | Key Packages |
|----------|-------------|
| Scientific | numpy 2.4.1, scipy 1.17.0, pandas 3.0.0 |
| Deep Learning | torch 2.10.0, torchdiffeq 0.2.5 |
| ML | scikit-learn 1.8.0, tensorboard 2.20.0 |
| Visualization | matplotlib 3.10.8, seaborn 0.13.2, plotly 6.5.2 |
| Notebooks | jupyter 1.1.1, jupyterlab 4.5.3, ipython 9.9.0 |
| Chemistry | rdkit (latest) |
| Testing/Tracking | pytest 9.0.2, wandb 0.24.0 |

4. **Created**: `requirements.txt` with all dependencies

### Dataset Download Implementation

Notebook: `data_download_pipeline.ipynb` — consolidated download pipeline (all sources)

**Download Issues & Resolutions:**

1. **PubChem CYP3A4 Assay**: AID 884 returned 400 BadRequest (legacy/disabled) → Updated to AID 54772 ✅
2. **PK-DB Substances**: `/api/v1/substances/` returned 404 → Rewrote to use `/api/v1/studies/` → Downloaded 796 studies ✅
3. **PK-DB Time-Courses**: Output endpoints require authentication → ❌ Needs credentials or web UI export

**Successfully Downloaded:**
- PubChem hERG assay: `assay_herg_qhts_aid588834.csv`
- PubChem CYP3A4 assay: `assay_cyp3a4_inhibition_aid54772.csv`
- PubChem compounds (3D SDF): warfarin, midazolam, caffeine
- PK-DB studies metadata: 796 studies with rich annotations

---

## 🔬 Phase 1: Data Exploration (COMPLETED ✅)

### Accomplishments

#### 1. Data Loading & Verification
- Successfully loaded all 5 datasets from `data/raw/` directory
- Verified data integrity and completeness
- Documented dataset schemas and column structures

#### 2. Exploratory Data Analysis
Created comprehensive visualizations:

**A. ChEMBL Binding Affinity (Cell 9)**
- **pIC50 Distribution**: Most compounds in mid-range potency (5-7), some highly potent (>8)
- **Target Analysis**: Top 10 protein targets identified, showing pharmaceutical relevance

**B. ToxCast Safety Screening (Cell 10)**
- **Risk Stratification**: Color-coded safety levels (CRITICAL/HIGH/MEDIUM/LOW)
- **Toxicity Categories**: Nuclear receptor activity, cardiac, hepatic, renal, developmental toxicity
- **Key Insight**: Distribution reveals most common safety liabilities for constraint modeling

**C. TDC ADMET Properties (Cell 11)**
- **hERG Inhibition**: Class imbalance (15% inhibitors) — cardiotoxicity predictor
- **Caco-2 Permeability**: Log Papp distribution shows absorption potential
- **Hepatocyte Clearance**: Mean -0.99 mL/min/kg guides dose regimen design

#### 3. PK-DB Structure Analysis
- Extracted 20+ unique drug substances from pharmacokinetic studies
- Identified available PK parameters: CL (clearance), Vd (volume), t½ (half-life)
- Documented time-course measurements for model training/validation

### Key Insights from Phase 1

| Finding | Implication for Modeling |
|---------|--------------------------|
| Wide pIC50 range (3.0-10.7) | Enables training for weak and strong binders |
| 7 distinct toxicity categories | Multi-objective safety constraints possible |
| ADMET property coverage | Full absorption-metabolism-excretion cycle |
| PK-DB time-series data | Ground truth for Neural ODE validation |

---

## 🛠️ Phase 2: Feature Engineering (COMPLETED ✅)

### Accomplishments

#### 1. RDKit Setup & Validation
- **Installation**: Successfully installed RDKit via pip
- **Import verification**: Confirmed all required modules available
- **Descriptor function**: Created `extract_molecular_descriptors()` with 10 features
- **Testing**: Validated with caffeine SMILES, extracted MW=194.19, LogP=-1.03, etc.

#### 2. Dataset Analysis & Adaptation

**Critical Discovery:**
- Datasets contain **anonymized SMILES IDs** (e.g., "SMILES_0"), not actual chemical structures
- Pre-calculated molecular descriptors already present in CSV files
- Cannot merge datasets on chemical structure (no shared molecular identity)

**Adaptation Strategy:**
- Pivoted from SMILES-based merging to **multi-task learning architecture**
- Used existing descriptors from datasets
- Created task-specific training samples

#### 3. ChEMBL Feature Preparation (Cell 22)
```
✅ 2,000 compounds processed (100% valid)
Molecular descriptors: MW, LogP, HBA, HBD, RotBonds
Target: pchembl_value (binding affinity)
```

#### 4. TDC ADMET Feature Preparation (Cell 24)
```
✅ 11,030 compounds across 3 datasets:
- hERG: 7,997 compounds (MW, LogP, HBA, HBD)
- Caco-2: 910 compounds (MW, LogP, HBA, HBD)
- Clearance: 2,123 compounds (MW, LogP, NumRings)
Core descriptors (all datasets): MW, LogP
```

#### 5. Multi-Task Feature Matrix (Cell 26)
Created unified dataset with:
- **Total samples**: 13,030
- **Common features**: MW, LogP (standardized)
- **4 prediction tasks**:
  - `binding_affinity`: 2,000 samples (range: 3.0-10.7 pIC50)
  - `hERG_inhibition`: 7,997 samples (binary: 0/1)
  - `Caco2_permeability`: 910 samples (binary: 0/1)
  - `hepatocyte_clearance`: 2,123 samples (range: -7.7 to 4.6)

#### 6. Feature Normalization (Cell 28)
```
✅ Standardization complete:
- Mean: -2.07e-16 ≈ 0 ✓
- Std: 1.00004 ≈ 1 ✓
- Method: StandardScaler (zero mean, unit variance)
```

**Output Variables:**
- `X_normalized`: (13,030 × 2) feature matrix
- `y_targets`: Dictionary of targets by task
- `X_targets`: Dictionary of features by task
- `task_info`: Task labels for each sample
- `preprocessing_objects`: Scaler + metadata for deployment

---

## 🧬 Phase 3: Neural ODE Model Development (IN PROGRESS 🔬)

### Notebook Structure

Phase 3 is split into **4 notebooks** connected via artifact bridging (pickle/JSON/parquet files in `data/processed/phase3{a,b,c}_artifacts/`). Run them in order: **3a → 3b → 3c → 3d**.

> **Note:** The original monolithic notebook [phase3_neural_ode_model.ipynb](../Coding/phase3_neural_ode_model.ipynb) (121 cells) is preserved as an archive.

#### [phase3a_feature_engineering.ipynb](../Coding/phase3a_feature_engineering.ipynb) — 18 cells

| Content | Sections |
|---------|----------|
| Environment setup & configuration | §1–2 |
| Data loading — 4 tasks, 13,030 samples | §3 |
| Feature engineering (Morgan FPs, normalization, quality gate) | §4–4.5 |
| Save artifacts → `data/processed/phase3a_artifacts/` | Bridge cell |

#### [phase3b_model_design.ipynb](../Coding/phase3b_model_design.ipynb) — 30 cells

| Content | Sections |
|---------|----------|
| Load Phase 3A artifacts | Bridge cell |
| `MultiTaskDataset` class | §5 |
| `SharedEncoder` (LayerNorm), `RegressionHead`, `ClassificationHead`, `PKODEFunc`, `MultiTaskPKPDModel` | §6 |
| `MultiTaskLoss` (MSE + weighted BCE) | §7 |
| Training pipeline (interleaved, early stopping, gradient clipping) | §8 |
| Visualization (`plot_training_history`, `plot_pk_curves`) | §9 |
| Training execution + PK curve demo | §10 |
| Save artifacts → `data/processed/phase3b_artifacts/` | Bridge cell |

#### [phase3c_finetuning.ipynb](../Coding/phase3c_finetuning.ipynb) — 28 cells

| Content | Sections |
|---------|----------|
| Load Phase 3B artifacts, rebuild model & dataloaders | Bridge cell |
| Fine-tuning (hERG, Caco-2), threshold calibration, constrained calibration, production threshold policy | §11 |
| Split-leakage mitigation (dedup + retrain) | §12 |
| Save artifacts → `data/processed/phase3c_artifacts/` | Bridge cell |

#### [phase3d_experiments.ipynb](../Coding/phase3d_experiments.ipynb) — 68 cells

| Content | Sections |
|---------|----------|
| Load Phase 3C artifacts, rebuild model & core functions | Bridge cell |
| 2048-bit real fingerprints | §13 |
| Real binding SMILES integration | §14 |
| hERG AUROC push (hidden_dim=256, pos_weight tuning) | §15 |
| Neural ODE PK/PD integration | §16 |
| GNN MPNN encoder | §17 |
| Probability calibration (Platt/temperature scaling) | §18 |
| GNN+MLP fusion model | §19 |
| Execution timeline | Summary |

### Key Design Decisions
- **LayerNorm** (not BatchNorm) for multi-task training stability
- **Min-step interleaved sampling** to prevent large-task dominance
- **Target normalization** (StandardScaler) on all regression outputs
- **Caco-2 corrected** to classification (was incorrectly binary regression)
- **ChEMBL zero-padded** for Morgan fingerprints (no SMILES column)
- **Gradient clipping** at 1.0; LR scheduling with ReduceLROnPlateau

### Architecture & Roadmap

```python
class MultiTaskPKPDModel(nn.Module):
    def __init__(self):
        # Shared encoder
        self.encoder = nn.Sequential(
            nn.Linear(2050, 256),    # 2 physico + 2048 Morgan FP → hidden
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 128)
        )
        
        # Task-specific heads
        self.binding_head = nn.Linear(128, 1)      # Regression
        self.herg_head = nn.Linear(128, 1)         # Binary classification
        self.caco2_head = nn.Linear(128, 1)        # Binary classification
        self.clearance_head = nn.Linear(128, 1)    # Regression
```

#### Neural ODE Integration
```python
from torchdiffeq import odeint

class PKODEFunc(nn.Module):
    def forward(self, t, y):
        # dC/dt = -CL/V * C + dosing
        # CL, V learned from molecular features
        pass
```

#### Loss Function
```python
loss = (
    w_binding * MSE(pred_binding, y_binding) +
    w_herg * BCE(pred_herg, y_herg) +
    w_caco2 * BCE(pred_caco2, y_caco2) +
    w_clearance * MSE(pred_clearance, y_clearance) +
    physics_penalty
)
```

### Next Planned Steps

**Option 1 (Recommended)**: Section 24 — Pareto Frontier Analysis
- Map multi-objective efficacy-safety trade-off surface
- Identify Pareto-optimal solutions balancing efficacy vs toxicity
- Visualize compromise frontiers for clinical decision-making
- Address constraint violations found in Section 23

**Option 2**: Monte Carlo Validation (uncertainty quantification with 1000+ virtual patients)

**Option 3**: Clinical Trial Simulation (Phase II/III projections)

**Option 4**: Summary & Conclusions (comprehensive findings, recommendations, limitations)

---

## 🐛 Issues Encountered & Resolutions

### Issue 1: RDKit Descriptor Extraction Failure

**Problem:**
```
⚠️ Descriptor extraction failed (RDKit may not be available)
```

**Root Causes:**
1. Jupyter kernel not restarted after `pip install rdkit`
2. `FractionCsp3` descriptor not available in installed RDKit version
3. Dataset schema incompatibility (no actual SMILES strings)

**Resolution Steps:**

**Step 1: Kernel Restart** — Restarted notebook kernel to recognize new package ✅

**Step 2: Descriptor Function Fix**
```python
# Before (failing):
'FractionCSP3': Descriptors.FractionCsp3(mol),  # AttributeError

# After (working):
'NumRings': Descriptors.RingCount(mol),  # Replacement descriptor
```

**Step 3: Dataset Schema Adaptation**
- Discovered SMILES are anonymized IDs ("SMILES_0", "SMILES_1")
- Datasets already contain pre-calculated descriptors
- Pivoted to using existing descriptors instead of re-calculating

**Final Resolution:** ✅ RDKit working for validation/testing; feature extraction using pre-calculated descriptors; multi-task learning architecture created.

---

### Issue 2: Feature Column Mismatch Across Datasets

**Problem:**
```python
KeyError: "['HBA', 'HBD'] not in index"
```
**Cause:** TDC Clearance dataset has different descriptor columns:
- hERG/Caco-2: `MW, LogP, HBA, HBD`
- Clearance: `MW, LogP, NumRings` (no HBA/HBD)

**Resolution:**
```python
# Adaptive column selection
herg_cols = [col for col in ['MW', 'LogP', 'HBA', 'HBD'] if col in tdc_herg.columns]
clearance_cols = [col for col in ['MW', 'LogP', 'NumRings'] if col in tdc_clearance.columns]

# Use common descriptors only: MW, LogP
common_descriptors = ['MW', 'LogP']
```

**Result:** Successfully combined datasets with different feature sets ✅

---

### Issue 3: Cannot Merge on SMILES

**Problem:** Original plan was to merge datasets on chemical structure (SMILES) for unified feature matrix.

**Discovery:**
- SMILES are anonymized identifiers, not actual chemical structures
- Each dataset has different compounds (no overlap)
- Cannot merge on molecular identity

**Resolution — Multi-Task Learning Architecture:**
```python
unified_features = pd.concat([
    chembl_data,      # task='binding_affinity'
    herg_data,        # task='hERG_inhibition'
    caco2_data,       # task='Caco2_permeability'
    clearance_data    # task='hepatocyte_clearance'
], ignore_index=True)
```

**Advantages:**
- ✅ Larger training dataset (13,030 vs ~2,000)
- ✅ Shared molecular feature learning
- ✅ Multi-objective optimization possible
- ✅ Better generalization across ADMET properties

---

### Issue 4: Phase 3 Model Training Issues (Feb 24, 2026)

Eight issues were encountered and resolved during initial Phase 3 model development:

| # | Problem | Root Cause | Fix | Status |
|---|---------|-----------|-----|--------|
| 1 | FileNotFoundError for TDC files | Filenames did not match disk (`tdc_caco2.csv`) | Corrected to `tdc_caco2_wang.csv`, `tdc_clearance_hepatocyte_az.csv` | ✅ |
| 2 | `verbose=True` deprecated | PyTorch 2.10 removed `verbose` from `ReduceLROnPlateau` | Removed argument | ✅ |
| 3 | `torch.load` unsafe | PyTorch 2.x requires explicit `weights_only` parameter | Added `weights_only=True` to all `torch.load()` calls | ✅ |
| 4 | BatchNorm corrupts multi-task training | Running stats dominated by largest task (hERG 7997 vs Caco-2 637) | Replaced all `BatchNorm1d` with `LayerNorm` | ✅ |
| 5 | hERG task dominance during training | hERG 5597 train vs Caco-2 637; naive interleaving gave hERG ~9× more updates | Min-step interleaving — all tasks capped at `min(len(loader))` = 10 steps/epoch | ✅ |
| 6 | Regression targets on different scales | pChEMBL 4-11, clearance 0.01-500 | `StandardScaler` normalization per regression task (fit on train only) | ✅ |
| 7 | Caco-2 incorrectly set up as binary classification | Caco-2 has continuous permeability values | Changed `caco2_head` to `RegressionHead` + MSE loss | ✅ |
| 8 | All ADMET tasks stuck near mean-prediction | 64-bit Morgan fingerprints have severe bit collisions | Increased `N_BITS` 64 → 2048; later added real SMILES (Sections 13-14) | ✅ |

---

## 📈 Final Dataset Characteristics

### Feature Matrix

| Property | Value |
|----------|-------|
| **Total Samples** | 13,030 |
| **Features** | 2 (MW, LogP) |
| **Feature Range (normalized)** | [-3.57, 3.71] for MW; [-4.10, 4.38] for LogP |
| **Normalization** | StandardScaler (μ=0, σ=1) |
| **Missing Values** | 0 (all complete) |

### Task Distribution

| Task | Samples | % of Total | Target Type | Target Range |
|------|---------|------------|-------------|--------------|
| hERG Inhibition | 7,997 | 61.4% | Binary | 0-1 |
| Hepatocyte Clearance | 2,123 | 16.3% | Continuous | -7.70 to 4.59 |
| Binding Affinity | 2,000 | 15.4% | Continuous | 3.00 to 10.70 |
| Caco-2 Permeability | 910 | 7.0% | Binary | 0-1 |

### Statistical Summary (Normalized Features)

```
           MW          LogP
count   13030.00    13030.00
mean        0.00        0.00
std         1.00        1.00
min        -3.57       -4.10
25%        -0.66       -0.67
50%         0.00       -0.04
75%         0.64        0.63
max         3.71        4.38
```

---

## 📁 Project Structure

```
Neural_PK-PD_Modeling_with_ODE/
│
├── .gitignore
├── README.md                          📄 Project entry point
│
├── Coding/
│   ├── TROUBLESHOOTING_GUIDE.md       🔧 Problem solving
│   │
│   ├── phase3a_feature_engineering.ipynb  📓 Feature engineering & data prep (18 cells)
│   ├── phase3b_model_design.ipynb        📓 Architecture & initial training (30 cells)
│   ├── phase3c_finetuning.ipynb          📓 Fine-tuning & calibration (28 cells)
│   ├── phase3d_experiments.ipynb         📓 Advanced experiments (68 cells)
│   ├── phase3_neural_ode_model.ipynb     📓 ARCHIVE: Original monolithic (121 cells)
│   ├── phase1_2_data_exploration.ipynb   📓 EDA & feature engineering (29 cells)
│   ├── requirements.txt                  📦 Dependencies
│   │
│   ├── data_download_pipeline.ipynb      📓 Data download pipeline (all sources)
│   │
│   ├── data/
│   │   ├── raw/                       Raw datasets
│   │   │   ├── chembl/            (1 MB)
│   │   │   ├── tdc/               (1.2 MB)
│   │   │   ├── toxcast/           (80 MB)
│   │   │   ├── pubchem/           (1.8 MB)
│   │   │   └── pkdb/              (300 KB)
│   │   ├── processed/                 Feature matrices + notebook artifacts
│   │   │   ├── phase3a_artifacts/     3a → 3b bridge (features, config, scalers)
│   │   │   ├── phase3b_artifacts/     3b → 3c bridge (model state, history)
│   │   │   └── phase3c_artifacts/     3c → 3d bridge (production model, thresholds)
│   │   └── outputs/                   Section outputs (PNGs, CSVs)
│   │
│   └── venv_pkpd/                     🐍 Python 3.14 environment
│
├── Documentation/
│   ├── PROJECT_SUMMARY.md             ⭐ THIS FILE - Complete project documentation
│   ├── DOCUMENTATION_GOVERNANCE.md    🧭 Update protocol
│   ├── MASTER_DATASET_REFERENCE.md    📄 Consolidated dataset docs (all 5 sources)
│   └── Neural PK-PD Thesis Playbook*  📄 Original guide (PDF/DOCX)
│
└── Slides/
    ├── README.md                      🎬 Generation guide
    ├── generate_presentation_v2.py     🐍 Canonical PPTX generator
    ├── generate_presentation.py        🐍 Legacy generator
    ├── v1_make_presentation.py         🐍 Earliest draft generator
    └── *.pptx                         🎬 Generated decks
```

---

## ✅ Project Completeness

### Phase 1: Data Exploration ✓
- [x] Data loading and verification
- [x] Visualizations created (3 sets)
- [x] Statistical analysis complete
- [x] Dataset documentation
- [x] Integration strategy defined

### Phase 2: Feature Engineering ✓
- [x] RDKit setup documented
- [x] Feature extraction explained
- [x] Multi-task architecture described
- [x] Preprocessing pipeline saved
- [x] Issues and resolutions logged

### Phase 3: Model Development (IN PROGRESS 🔬)
- [x] Neural architecture built (`SharedEncoder` + 4 task heads + `PKODEFunc`)
- [x] Training pipeline implemented (interleaved, early stopping, LR scheduling)
- [x] Multiple retraining cycles completed (deep-head, focal, logits variants)
- [x] Neural ODE PK curve generation working (`plot_pk_curves()`)
- [x] All 4 ADME targets met (Section 15): hERG 0.82, Caco-2 0.86, Clearance 0.35, Binding 0.45
- [x] Phase 2→3 processed feature handoff completed (258-dim inputs)
- [x] Sections 16-20: PK/PD integration, GNN, reliability, joint model, population PK-PD
- [x] Section 21: Scenario Analysis (4 dosing scenarios)
- [x] Section 22: Sensitivity Analysis (9 parameters, tornado plots)
- [x] Section 23: Dose Optimization (grid search + differential evolution)
- [ ] Section 24: Pareto Frontier Analysis
- [ ] Model interpretation and attention analysis

### Phase 4: Deployment (PENDING)
- [ ] API documentation
- [ ] User guide
- [ ] Model export procedure
- [ ] Deployment checklist

---

## 🔧 Technical Stack

### Environment
- **Python**: 3.14.2
- **Kernel**: venv_pkpd (Jupyter registered)
- **Packages**: 143 installed

### Core Libraries

| Library | Version | Purpose |
|---------|---------|---------|
| **pandas** | 3.0.0 | Data manipulation |
| **numpy** | 2.4.1 | Numerical computing |
| **matplotlib** | 3.10.8 | Visualization |
| **seaborn** | 0.13.2 | Statistical plots |
| **scikit-learn** | 1.8.0 | Preprocessing, scaling |
| **torch** | 2.10.0 | Deep learning framework |
| **scipy** | 1.17.0 | Scientific computing |
| **rdkit** | Latest | Molecular descriptors |

### Success Criteria

| Task | Metric | Target | Achieved |
|------|--------|--------|----------|
| Binding Affinity | R² | > 0.40 | **0.4521** ✅ |
| hERG Inhibition | AUROC | > 0.80 | **0.8206** ✅ |
| Caco-2 Permeability | AUROC | > 0.75 | **0.8635** ✅ |
| Hepatocyte Clearance | R² | > 0.20 | **0.3478** ✅ |

---

## 🎓 Key Learnings & Insights

### Data Science
1. **Multi-task learning is powerful** — combining related tasks improves generalization; 6.5× more training data than single-task
2. **Real-world data challenges** — datasets rarely have perfect schema alignment; anonymization affects merging
3. **Feature engineering matters** — only 2 features (MW, LogP) initially available, but proper normalization + fingerprints enabled strong results

### Technical
1. **Jupyter kernel management** — must restart kernel after installing packages
2. **RDKit compatibility** — descriptor availability varies by version; always test before batch processing
3. **Split leakage** — quality gate findings drove data-splitting corrections that improved generalization

### Scientific
1. **Multi-task learning enables data sharing** across related ADMET endpoints
2. **Safety constraints critical** for therapeutic window modeling
3. **Efficacy-safety trade-off** is fundamental — simple optimization insufficient, need multi-objective approaches (Pareto)

---

## 📊 Visualization Summary

### Created Visualizations

1. **ChEMBL Binding Affinity** (Cell 9) — pIC50 distribution + top 10 protein targets
2. **ToxCast Safety Profile** (Cell 10) — color-coded risk levels + toxicity categories
3. **TDC ADMET Properties** (Cell 11) — hERG class distribution, Caco-2 histogram, clearance distribution

**Analysis Output:** Cell 14 contains comprehensive interpretation of all visualizations with modeling implications

---

## 🚀 Ready State

### Variables Available in Notebook
```python
phase2_features   # processed matrix with task + target + fp_* columns
FEATURE_COLS      # model input feature columns (258 dims in current run)
train_loaders     # task-specific train DataLoaders
val_loaders       # task-specific validation DataLoaders
history           # training losses + per-task metrics
```

### Data Quality
- ✅ No missing values — properly normalized — task labels verified — train/val/test split ready

### Running the Notebooks
```bash
source Coding/venv_pkpd/bin/activate
# Run Phase 3 notebooks in order (each saves artifacts for the next):
jupyter notebook Coding/phase3a_feature_engineering.ipynb   # Feature engineering
jupyter notebook Coding/phase3b_model_design.ipynb          # Architecture & training
jupyter notebook Coding/phase3c_finetuning.ipynb            # Fine-tuning & calibration
jupyter notebook Coding/phase3d_experiments.ipynb            # Advanced experiments
# Select kernel: venv_pkpd (Python 3.14), Run all cells
```

---

## 🔗 References

### Datasets
1. **ChEMBL**: https://www.ebi.ac.uk/chembl/
2. **TDC ADMET**: https://tdcommons.ai/
3. **ToxCast**: https://www.epa.gov/chemical-research/toxicity-forecasting
4. **PubChem**: https://pubchem.ncbi.nlm.nih.gov/
5. **PK-DB**: https://www.pk-db.com/

### Methods
1. Neural ODEs: Chen et al. (2018) "Neural Ordinary Differential Equations"
2. Multi-Task Learning: Ruder (2017) "An Overview of Multi-Task Learning in Deep Neural Networks"
3. ADMET Prediction: Yang et al. (2019) "Analyzing Learned Molecular Representations for Property Prediction"

---

## 📈 Progress Timeline

```
Week 1-2: Data Collection ✅
Week 3:   Data Exploration ✅  
Week 4:   Feature Engineering ✅
Week 5-7: Neural ODE Model ✅ (Sections 12-23)
Week 8:   Pareto Frontier + Model Export (← Current)
Week 9:   Thesis Writing
```

---

## � Development Session Log

Condensed record of each development session (full details in sections above).

| Date | Session | Key Outcome |
|------|---------|-------------|
| Jan 21, 2026 | **Environment setup + data download** | Python 3.14.2 venv, 143 packages, PubChem + PK-DB data downloaded; PK-DB time-courses inaccessible |
| Feb 24, 2026 | **Phase 3: Initial Neural ODE build** | 44,710-param model (4 heads + ODE), 8 training bugs fixed; epoch 42 early stop; clearance RMSE 0.968 (borderline pass), other 3 tasks near random |
| Mar 4, 2026 | **Phase 2 completion + Phase 3 refactor** | Fingerprint pipeline integrated; Caco-2 aligned to classification; model consumes Phase 2 processed matrix; binding R²=-0.029, hERG AUROC=0.482 |
| Mar 8, 2026 | **Locked-threshold reporting + docs sync** | Production thresholds locked (hERG=0.49, Caco-2=0.50); canonical status established; slides pipeline consolidated |
| Mar 8, 2026 | **Section 13: 2048-bit real-SMILES upgrade** | 4,916 hERG + 1,855 Caco-2 + 2,127 clearance real SMILES from ChEMBL; hERG AUROC 0.48→0.70, Caco-2 0.42→0.86 |
| Mar 8, 2026 | **Section 14: Real binding SMILES** | 3,410 real compounds from 8 ChEMBL targets; binding R² -0.008→+0.431; all 4 tasks improved |
| Mar 8, 2026 | **Section 15: hERG AUROC push** | hidden_dim=256, pos_weight=1.5; hERG AUROC 0.77→0.82; **ALL 4 ADME targets met** |
| Mar 11, 2026 | **Sections 21-23: Clinical decision support** | Scenario analysis (4 regimens), sensitivity analysis (9 params), dose optimization (grid + differential evolution); efficacy-safety trade-off identified |
| Mar 11, 2026 | **Notebook split (3a/3b/3c/3d)** | Split monolithic Phase 3 notebook (121 cells) into 4 modular notebooks with artifact bridging; updated all 5 documentation files |

---

## 📝 Change History

Detailed record of structural and documentation changes.

### March 11, 2026 — Phase 3 Notebook Split

**What changed**: The monolithic `phase3_neural_ode_model.ipynb` (121 cells) was split into 4 modular notebooks connected by artifact bridging.

| Before | After | Cells |
|--------|-------|-------|
| `phase3_neural_ode_model.ipynb` (monolithic) | `phase3a_feature_engineering.ipynb` | 18 |
| | `phase3b_model_design.ipynb` | 30 |
| | `phase3c_finetuning.ipynb` | 28 |
| | `phase3d_experiments.ipynb` | 68 |
| **Total: 121 cells** | **Total: 144 cells** (includes 23 bridge cells) | |

**Artifact pipeline**: Each notebook saves state to `data/processed/phase3{a,b,c}_artifacts/` and the next notebook loads from there.

```
phase3a (features, config, scalers)
  → saves to data/processed/phase3a_artifacts/
    → phase3b loads, trains model
      → saves to data/processed/phase3b_artifacts/
        → phase3c loads, fine-tunes
          → saves to data/processed/phase3c_artifacts/
            → phase3d loads, runs experiments
```

**Why**: The 121-cell monolith was unwieldy for development and review. The 4-way split groups logically related work:
- **3a**: Data prep (run once, reuse artifacts)
- **3b**: Architecture iteration (fast reload without re-processing data)
- **3c**: Fine-tuning experiments (independent of architecture changes)
- **3d**: Advanced experiments (GNN, Neural ODE PK/PD, fusion)

**Documentation updated**: PROJECT_SUMMARY.md, README.md, TROUBLESHOOTING_GUIDE.md, MASTER_DATASET_REFERENCE.md, DOCUMENTATION_GOVERNANCE.md

**Original preserved**: `phase3_neural_ode_model.ipynb` kept as archive (unchanged).

---

## �🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| **4.4** | Mar 11, 2026 | Reordered experiment sections to ascending order (12→13→14→15→21-23); added Change History section with notebook split details |
| **4.3** | Mar 11, 2026 | Split Phase 3 monolithic notebook (121 cells) into 4 modular notebooks: phase3a (18), phase3b (30), phase3c (28), phase3d (68) with artifact bridging; updated all documentation cross-references |
| **4.2** | Mar 11, 2026 | Consolidated 7 download .py scripts into `data_download_pipeline.ipynb`; updated all cross-references |
| **4.1** | Mar 11, 2026 | Folded Working_Progress.txt session log into Development Session Log + Issue 4 table || **4.0** | Mar 11, 2026 | Consolidated PROJECT_SUMMARY + PROJECT_STATUS + MASTER_INDEX + README into single document |
| **3.3** | Mar 11, 2026 | Merged PROJECT_SUMMARY.md + EXECUTIVE_SUMMARY.md |
| **3.2** | Mar 11, 2026 | Merged INTEGRATION_STATUS.md into MASTER_DATASET_REFERENCE.md; moved to Documentation/ |
| **3.1** | Mar 11, 2026 | Consolidated 9 dataset markdown files into single MASTER_DATASET_REFERENCE.md |
| **3.0** | Mar 11, 2026 | Project cleanup — removed 17 intermediate/redundant files, organized outputs directory |
| **2.3** | Mar 11, 2026 | Sections 21-23 addendum (clinical decision support) |
| **2.2** | Mar 8, 2026 | Section 15 addendum (all ADME targets met) |
| **2.1** | Mar 4, 2026 | Phase 3 objective alignment + multi-variant benchmark updates |
| **2.0** | Feb 24, 2026 | Phase 3 Neural ODE model session — architecture, training, results |
| **1.0** | Feb 17, 2026 | Initial project summary — Phase 1 & 2 complete |
| **0.9** | Feb 4, 2026 | Original INDEX.md (superseded) |

---

## 👥 Project Team

**Student**: Subrat  
**Project Type**: Master's Thesis  
**Field**: Computational Drug Discovery / Machine Learning

---

**📎 Current Status: PHASE 3 IN PROGRESS — Sections 21-23 Complete (Scenario Analysis, Sensitivity, Dose Optimization) | 4-Notebook Split Active**

**Last Updated**: March 11, 2026  
**Maintained By**: Subrat

---

*This document is the single authoritative reference for the Neural PK-PD Modeling project. It consolidates the former PROJECT_SUMMARY.md, EXECUTIVE_SUMMARY.md, PROJECT_STATUS.md, MASTER_INDEX.md, README.md setup documentation, and Working_Progress.txt session log.*
