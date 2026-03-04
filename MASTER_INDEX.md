# 📚 Neural PK-PD Modeling Project - Master Index

**Project**: Physics-Informed Neural ODE for Pharmacokinetic-Pharmacodynamic Modeling  
**Author**: Subrat  
**Last Updated**: March 4, 2026  
**Current Status**: 🔬 Phase 3 In Progress | Phase 2→3 Integration Complete, Multi-Variant Benchmarks Executed

---

## 🎯 Quick Start Guide

**New to this project?** Start here:

1. 📌 [PROJECT_STATUS.md](Documentation/PROJECT_STATUS.md) - **Canonical live status** (phase, latest metrics, next action)
2. 📖 [EXECUTIVE_SUMMARY.md](Coding/EXECUTIVE_SUMMARY.md) - **One-page overview** (2 min read)
3. 📋 [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md) - **Complete documentation** (15 min read)
4. 🔧 [TROUBLESHOOTING_GUIDE.md](Coding/TROUBLESHOOTING_GUIDE.md) - **Problem solving** (reference)
5. 📓 [phase1_2_data_exploration.ipynb](Coding/phase1_2_data_exploration.ipynb) - **Phase 1–2 EDA & feature engineering** (interactive)
6. 🧭 [DOCUMENTATION_GOVERNANCE.md](Documentation/DOCUMENTATION_GOVERNANCE.md) - **Update protocol** (how to keep docs in sync)
7. 🎞️ [Slides/README.md](Slides/README.md) - **Slides generation guide** (canonical PPTX commands)

### Canonical vs Historical

- **Canonical live status source**: [Documentation/PROJECT_STATUS.md](Documentation/PROJECT_STATUS.md)
- **Historical snapshots retained for traceability**:
   - [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md)
   - [Coding/INDEX.md](Coding/INDEX.md)

---

## 📅 Project Timeline & Documentation

### **Phase 0: Initial Setup** (January 21, 2026)

#### 📄 [README.md](README.md)
**Purpose**: Project initialization and environment setup  
**Key Topics**:
- Python 3.14.2 virtual environment creation
- Package installation (143 packages)
- Initial project structure
- Setup troubleshooting

**When to Read**: First document for understanding project foundation

---

### **Phase 1: Data Collection** (January-February 2026)

#### 1️⃣ Data Source Documentation (Read in Order)

##### 📄 [DATA_README.md](Coding/DATA_README.md)
**Date**: Early February 2026  
**Purpose**: Complete data pipeline overview  
**Key Topics**:
- Overview of all 5 data sources
- Download scripts and usage
- Data directory structure
- File formats and sizes

**When to Read**: Before exploring individual datasets

---

##### 📄 [PKDB_DOWNLOAD_SUMMARY.md](Coding/PKDB_DOWNLOAD_SUMMARY.md)
**Date**: February 2026  
**Purpose**: PK-DB pharmacokinetic studies  
**Key Topics**:
- 20 drug substances with PK parameters
- Time-course concentration data
- API access methods
- Integration with PD models

**Dataset Size**: 508 KB

---

##### 📄 [TDC_ADMET_SUMMARY.md](Coding/TDC_ADMET_SUMMARY.md)
**Date**: February 2026  
**Purpose**: TDC ADMET benchmark datasets  
**Key Topics**:
- 8 ADMET property datasets
- hERG, Caco-2, clearance, solubility, HIA
- Train/test splits and metrics
- Therapeutic Data Commons integration

**Dataset Size**: 1.2 MB

---

##### 📄 [CHEMBL_BINDING_SUMMARY.md](Coding/CHEMBL_BINDING_SUMMARY.md)
**Date**: February 2026  
**Purpose**: ChEMBL binding affinity data  
**Key Topics**:
- 2,000 compound binding records
- pIC50/pKi values
- Target protein information
- Pharmacodynamic endpoint modeling

**Dataset Size**: 528 KB

---

##### 📄 [TOXCAST_TOX21_SUMMARY.md](Coding/TOXCAST_TOX21_SUMMARY.md)
**Date**: February 2026  
**Purpose**: ToxCast toxicity screening data  
**Key Topics**:
- 332,507 toxicity results
- 7 safety categories (nuclear receptor, cardiac, hepatic, etc.)
- Risk level stratification (CRITICAL/HIGH/MEDIUM/LOW)
- EPA data access methods

**Dataset Size**: 80 MB

---

##### 📄 [TOXCAST_TOX21_RESEARCH.md](Coding/TOXCAST_TOX21_RESEARCH.md)
**Date**: February 2026  
**Purpose**: ToxCast research background  
**Key Topics**:
- Assay methodology
- Risk assessment framework
- Literature references
- Use cases in drug safety

**Documentation Type**: Research notes

---

#### 2️⃣ Integration Documentation

##### 📄 [DATASET_INTEGRATION_SUMMARY.md](Coding/DATASET_INTEGRATION_SUMMARY.md)
**Date**: February 4, 2026  
**Purpose**: Multi-source data integration strategy  
**Key Topics**:
- Cross-dataset linking on SMILES
- Feature engineering workflow
- Combined dataset structure
- Integration examples

**When to Read**: After understanding individual datasets

---

##### 📄 [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md)
**Date**: February 4, 2026  
**Purpose**: Integration progress tracking (**historical snapshot**)  
**Key Topics**:
- Completion status by dataset
- Known issues and resolutions
- Next steps for integration

**When to Read**: For historical context only (for current status use [Documentation/PROJECT_STATUS.md](Documentation/PROJECT_STATUS.md))

---

##### 📄 [TOXCAST_INTEGRATION_COMPLETE.md](Coding/TOXCAST_INTEGRATION_COMPLETE.md)
**Date**: February 2026  
**Purpose**: ToxCast integration completion report  
**Key Topics**:
- Final integration results
- Data quality verification
- Coverage statistics
- Usage examples

**When to Read**: For ToxCast-specific integration details

---

### **Phase 2: Data Exploration & Feature Engineering** (February 17, 2026)

#### 📓 [phase1_2_data_exploration.ipynb](Coding/phase1_2_data_exploration.ipynb)
**Date**: February 17, 2026 (Latest)  
**Purpose**: Complete data analysis and feature engineering pipeline  
**Structure**:
- **Cells 1-4**: Data loading (5 datasets, 347,896 records)
- **Cells 5-7**: Data inspection (ChEMBL, ToxCast)
- **Cells 8-11**: Visualizations (binding affinity, toxicity, ADMET)
- **Cells 12-14**: PK-DB analysis
- **Cell 14**: Visualization interpretation and conclusions
- **Cells 15**: Phase 1 summary
- **Cells 16-20**: Phase 2 - RDKit setup and descriptor extraction
- **Cells 21-24**: Feature preparation (ChEMBL, TDC)
- **Cells 25-26**: Multi-task feature matrix creation
- **Cells 27-28**: Feature normalization
- **Cell 29**: Phase 2 summary

**Key Results**:
- 13,030 training samples prepared
- 4 prediction tasks (binding, hERG, Caco-2, clearance)
- Features normalized (mean=0, std=1)

**When to Read**: For hands-on analysis and code reference (Phase 1–2 EDA; for Phase 3 model see phase3_neural_ode_model.ipynb)

---

#### 📄 [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md) ⭐ **MAIN DOCUMENTATION**
**Date**: February 17, 2026  
**Purpose**: Complete project documentation (18 pages)  
**Key Sections**:
1. Executive Summary
2. Project Overview & Objectives
3. Dataset Descriptions (all 5 sources)
4. **Phase 1: Data Exploration** (completed)
   - Visualizations and insights
   - Statistical analysis
5. **Phase 2: Feature Engineering** (completed)
   - RDKit setup and validation
   - Multi-task learning architecture
   - Feature preprocessing
6. **Issues Encountered & Resolutions**
   - RDKit descriptor extraction failure
   - Feature column mismatches
   - Dataset schema incompatibility
7. Final Dataset Characteristics
8. **Phase 3 Roadmap: Neural ODE Model**
9. Technical Stack & Environment
10. Code Quality Standards
11. References

**When to Read**: For comprehensive understanding of entire project

---

#### 📄 [EXECUTIVE_SUMMARY.md](Coding/EXECUTIVE_SUMMARY.md) ⭐ **QUICK REFERENCE**
**Date**: February 17, 2026  
**Purpose**: One-page project overview  
**Key Sections**:
- At-a-glance metrics table
- Completed work checklist
- Major issues resolved (summary only)
- Final dataset structure
- Next phase overview
- Progress timeline (50% complete)
- Deliverables status

**When to Read**: For quick status check or stakeholder briefing

---

#### 📄 [TROUBLESHOOTING_GUIDE.md](Coding/TROUBLESHOOTING_GUIDE.md) 🔧 **PROBLEM SOLVING**
**Date**: February 17, 2026  
**Purpose**: Issue resolution reference (8 pages)  
**Key Sections**:
1. **Common Issues & Quick Fixes**
   - RDKit not available after installation
   - AttributeError - FractionCsp3
   - KeyError - columns not in index
   - Kernel shows wrong environment
   - Cannot merge datasets on SMILES
   - Cells show errors after kernel restart
2. **Environment Setup Issues**
3. **Data Loading Issues**
4. **Data Processing Issues**
5. **Visualization Issues**
6. **Machine Learning Issues**
7. **Debugging Tips**
8. **Best Practices**
9. **Nuclear Option: Fresh Start**

**When to Read**: When encountering errors or problems

---

### **Phase 3: Neural ODE Model Development** (February 24, 2026 → March 4, 2026 updates)

#### 📓 [phase3_neural_ode_model.ipynb](Coding/phase3_neural_ode_model.ipynb) ⭐ **ACTIVE DEVELOPMENT**
**Date**: February 24, 2026 (Active; updated March 4, 2026)  
**Purpose**: Multi-task Neural ODE model for simultaneous ADMET and PK/PD prediction  
**Structure** (36 cells, all executed):
- **Cells 1-2**: Project header and setup
- **Cell 3**: Imports (torch, torchdiffeq, rdkit, sklearn, scipy)
- **Cells 4-5**: Configuration dict (input_dim resolved from processed features; hidden_dim=128, latent_dim=64)
- **Cells 6-8**: Data loading — 4 tasks, 13,030 total samples
- **Cells 9-10**: Feature engineering helper (`prepare_task_data()`)
- **Cell 11**: Task heads and architecture modules
- **Cell 12**: Feature-space setup from Phase 2 processed matrix (2 physico + 256 fingerprints)
- **Cell 13**: Per-task DataLoaders with target normalization
- **Cell 15**: `MultiTaskDataset` class
- **Cell 17**: `SharedEncoder` (LayerNorm, 128→64 latent)
- **Cell 19**: `RegressionHead` and `ClassificationHead`
- **Cell 21**: `PKODEFunc` (Neural ODE dynamics)
- **Cell 23**: `MultiTaskPKPDModel` (4 tasks unified)
- **Cell 24**: Model instantiation (~73,190 trainable params in current variant)
- **Cell 26**: `MultiTaskLoss` (MSE + weighted BCE, pos_weight=2.5)
- **Cells 28-30**: Training pipeline — interleaved, early stopping, gradient clipping
- **Cells 32-33**: Visualization (`plot_training_history`, `plot_pk_curves`)
- **Cell 35**: Training execution (multiple benchmark variants)
- **Cell 36**: PK curve demo + comprehensive status summary

**Current Results** (historical Feb 24 baseline):
| Task | Metric | Result | Target | Status |
|------|--------|--------|--------|--------|
| Binding Affinity | R² | −0.025 | >0.60 | ✗ |
| hERG Inhibition | AUROC | 0.507 | >0.80 | ✗ |
| Caco-2 Permeability | R² | −0.118 | >0.60 | ✗ |
| Hepatocyte Clearance | RMSE | 0.968 | <1.00 | ✓ |

**Key Decisions Made**:
- LayerNorm (not BatchNorm) for multi-task training stability
- Min-step interleaved sampling to prevent large-task dominance
- Target normalization (StandardScaler) on all regression outputs
- Caco-2 corrected to regression (was incorrectly binary classification)
- ChEMBL zero-padded for Morgan fingerprints (no SMILES column)
- Gradient clipping at 1.0; LR scheduling with ReduceLROnPlateau

**March 4, 2026 Update (supersedes Feb 24 snapshot):**
- Phase 2 missing component fixed: fingerprints are now included in the unified matrix and exported.
- Phase 3 now consumes processed Phase 2 features directly from:
   - [data/processed/phase2_multitask_features_with_fingerprints.csv](Coding/data/processed/phase2_multitask_features_with_fingerprints.csv)
- Current feature space: **258 dims** (2 physico + 256 fingerprints).
- Caco-2 objective aligned to classification with AUROC reporting.
- Additional controlled experiments completed:
   1. Deep-head + task-loss reweighting
   2. Focal loss + auto class-weighting
   3. Logits-based classification + validation threshold tuning

**Latest Benchmark (March 4, 2026):**
| Task | Metric | Result | Target | Status |
|------|--------|--------|--------|--------|
| Binding Affinity | R² | -0.029 | > 0.60 | ✗ |
| hERG Inhibition | AUROC | 0.482 | > 0.80 | ✗ |
| Caco-2 Permeability | AUROC | 0.518 | > 0.75 | ✗ |
| Clearance | RMSE | 0.969 | < 1.00 | ✓ |

**When to Read**: For Neural ODE architecture, training pipeline, and multi-task ADMET results

---

## 📊 Documentation by Category

### 🎯 Start Here (Ordered for New Users)

1. [EXECUTIVE_SUMMARY.md](Coding/EXECUTIVE_SUMMARY.md) - Quick overview
2. [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md) - Complete story
3. [DATA_README.md](Coding/DATA_README.md) - Data sources
4. [phase1_2_data_exploration.ipynb](Coding/phase1_2_data_exploration.ipynb) - Phase 1–2 EDA & feature engineering

### 📚 Dataset Documentation (By Data Source)

| Dataset | Document | Size | Records |
|---------|----------|------|---------|
| **PK-DB** | [PKDB_DOWNLOAD_SUMMARY.md](Coding/PKDB_DOWNLOAD_SUMMARY.md) | 508 KB | 20 studies |
| **TDC ADMET** | [TDC_ADMET_SUMMARY.md](Coding/TDC_ADMET_SUMMARY.md) | 1.2 MB | 11,030 samples |
| **ChEMBL** | [CHEMBL_BINDING_SUMMARY.md](Coding/CHEMBL_BINDING_SUMMARY.md) | 528 KB | 2,000 compounds |
| **ToxCast** | [TOXCAST_TOX21_SUMMARY.md](Coding/TOXCAST_TOX21_SUMMARY.md) | 80 MB | 332,507 results |
| **PubChem** | [DATA_README.md](Coding/DATA_README.md) | 1.8 MB | 5,392 assays |

### 🔬 Research & Background

- [TOXCAST_TOX21_RESEARCH.md](Coding/TOXCAST_TOX21_RESEARCH.md) - ToxCast methodology
- [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md) - References section

### 🔧 Technical Reference

- [TROUBLESHOOTING_GUIDE.md](Coding/TROUBLESHOOTING_GUIDE.md) - Problem solving
- [README.md](README.md) - Environment setup
- [phase1_2_data_exploration.ipynb](Coding/phase1_2_data_exploration.ipynb) - Phase 1–2 code implementation

### 📈 Progress Tracking

- [EXECUTIVE_SUMMARY.md](Coding/EXECUTIVE_SUMMARY.md) - Current status
- [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md) - Integration progress (historical)
- [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md) - Complete timeline

### 🔗 Integration Documentation

- [DATASET_INTEGRATION_SUMMARY.md](Coding/DATASET_INTEGRATION_SUMMARY.md) - Integration strategy
- [TOXCAST_INTEGRATION_COMPLETE.md](Coding/TOXCAST_INTEGRATION_COMPLETE.md) - ToxCast integration

---

## 🎓 Reading Paths by Role

### 👨‍🎓 For Students/Beginners

**Recommended Order**:
1. [EXECUTIVE_SUMMARY.md](Coding/EXECUTIVE_SUMMARY.md) - Understand what was built
2. [README.md](README.md) - Learn about setup
3. [DATA_README.md](Coding/DATA_README.md) - Explore data sources
4. [phase1_2_data_exploration.ipynb](Coding/phase1_2_data_exploration.ipynb) - See the Phase 1–2 code
5. [TROUBLESHOOTING_GUIDE.md](Coding/TROUBLESHOOTING_GUIDE.md) - Learn from issues

**Time**: ~2 hours

---

### 👨‍🔬 For Researchers

**Recommended Order**:
1. [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md) - Complete methodology
2. [DATASET_INTEGRATION_SUMMARY.md](Coding/DATASET_INTEGRATION_SUMMARY.md) - Data integration approach
3. Individual dataset docs:
   - [CHEMBL_BINDING_SUMMARY.md](Coding/CHEMBL_BINDING_SUMMARY.md)
   - [TOXCAST_TOX21_SUMMARY.md](Coding/TOXCAST_TOX21_SUMMARY.md)
   - [TDC_ADMET_SUMMARY.md](Coding/TDC_ADMET_SUMMARY.md)
   - [PKDB_DOWNLOAD_SUMMARY.md](Coding/PKDB_DOWNLOAD_SUMMARY.md)
4. [phase1_2_data_exploration.ipynb](Coding/phase1_2_data_exploration.ipynb) - Implementation details

**Time**: ~4 hours

---

### 👨‍💼 For Stakeholders/Advisors

**Recommended Order**:
1. [EXECUTIVE_SUMMARY.md](Coding/EXECUTIVE_SUMMARY.md) - Quick overview (5 min)
2. [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md) - Key sections:
   - Executive Summary
   - Issues & Resolutions
   - Next Steps (Phase 3 Roadmap)

**Time**: ~20 minutes

---

### 👨‍💻 For Developers (Continuing the Work)

**Recommended Order**:
1. [EXECUTIVE_SUMMARY.md](Coding/EXECUTIVE_SUMMARY.md) - Current status
2. [TROUBLESHOOTING_GUIDE.md](Coding/TROUBLESHOOTING_GUIDE.md) - Known issues
3. [README.md](README.md) - Environment setup
4. [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md) - Section: "Phase 3 Roadmap"
5. [phase1_2_data_exploration.ipynb](Coding/phase1_2_data_exploration.ipynb) - Phase 1–2 working code
6. Check variables in notebook:
   - `X_normalized` - Features
   - `y_targets` - Targets
   - `preprocessing_objects` - Scaler

**Time**: ~1 hour to get started

---

## 📁 Project Structure

```
Neural_PK-PD_Modeling_with_ODE/
│
├── MASTER_INDEX.md                    ⭐ THIS FILE - Start here
├── README.md                          📄 Project setup (Jan 21)
├── INTEGRATION_STATUS.md              📊 Integration progress (Feb 4)
│
├── Coding/
│   ├── EXECUTIVE_SUMMARY.md           ⭐ Quick overview (Feb 17)
│   ├── PROJECT_SUMMARY.md             ⭐ Complete docs (Feb 17)
│   ├── TROUBLESHOOTING_GUIDE.md       🔧 Problem solving (Feb 17)
│   │
│   ├── phase3_neural_ode_model.ipynb  📓 ACTIVE: Neural ODE model (36 cells, Feb 24)
│   ├── phase1_2_data_exploration.ipynb 📓 EDA & feature engineering (29 cells)
│   ├── requirements.txt               📦 143 packages
│   │
│   ├── DATA_README.md                 📄 Data overview
│   ├── DATASET_INTEGRATION_SUMMARY.md 📄 Integration strategy
│   ├── INDEX.md                       📄 Old index (superseded)
│   │
│   ├── PKDB_DOWNLOAD_SUMMARY.md       📄 PK-DB details
│   ├── TDC_ADMET_SUMMARY.md           📄 TDC ADMET details
│   ├── CHEMBL_BINDING_SUMMARY.md      📄 ChEMBL details
│   ├── TOXCAST_TOX21_SUMMARY.md       📄 ToxCast details
│   ├── TOXCAST_TOX21_RESEARCH.md      📄 ToxCast research
│   ├── TOXCAST_INTEGRATION_COMPLETE.md 📄 ToxCast integration
│   │
│   ├── data/
│   │   └── raw/
│   │       ├── chembl/                (528 KB)
│   │       ├── tdc/                   (1.2 MB)
│   │       ├── toxcast/               (80 MB)
│   │       ├── pubchem/               (1.8 MB)
│   │       └── pkdb/                  (508 KB)
│   │
│   └── venv_pkpd/                     🐍 Python 3.14 environment
│
└── Documentation/                      📂 Additional docs
    └── Working_Progress.txt
```

---

## 🔍 Quick Search Guide

Looking for specific information? Use this guide:

| Topic | Document(s) |
|-------|------------|
| **Current project status** | [EXECUTIVE_SUMMARY.md](Coding/EXECUTIVE_SUMMARY.md) |
| **Complete timeline** | [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md) |
| **Environment setup** | [README.md](README.md), [TROUBLESHOOTING_GUIDE.md](Coding/TROUBLESHOOTING_GUIDE.md) |
| **Data sources** | [DATA_README.md](Coding/DATA_README.md) |
| **RDKit issues** | [TROUBLESHOOTING_GUIDE.md](Coding/TROUBLESHOOTING_GUIDE.md) |
| **Feature engineering** | [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md) - Phase 2, [phase1_2_data_exploration.ipynb](Coding/phase1_2_data_exploration.ipynb) cells 16-28 |
| **Visualizations** | [phase1_2_data_exploration.ipynb](Coding/phase1_2_data_exploration.ipynb) cells 9-11, [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md) - Phase 1 |
| **Multi-task learning** | [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md) - Phase 2, [phase3_neural_ode_model.ipynb](Coding/phase3_neural_ode_model.ipynb) |
| **Neural ODE model** | [phase3_neural_ode_model.ipynb](Coding/phase3_neural_ode_model.ipynb) cells 17-35 |
| **PK curve generation** | [phase3_neural_ode_model.ipynb](Coding/phase3_neural_ode_model.ipynb) cell 33, `PKODEFunc` |
| **Training issues & fixes** | See Phase 3 section in this index above |
| **ChEMBL binding data** | [CHEMBL_BINDING_SUMMARY.md](Coding/CHEMBL_BINDING_SUMMARY.md) |
| **ToxCast safety data** | [TOXCAST_TOX21_SUMMARY.md](Coding/TOXCAST_TOX21_SUMMARY.md) |
| **ADMET properties** | [TDC_ADMET_SUMMARY.md](Coding/TDC_ADMET_SUMMARY.md) |
| **PK parameters** | [PKDB_DOWNLOAD_SUMMARY.md](Coding/PKDB_DOWNLOAD_SUMMARY.md) |
| **Integration strategy** | [DATASET_INTEGRATION_SUMMARY.md](Coding/DATASET_INTEGRATION_SUMMARY.md) |
| **Known issues** | [TROUBLESHOOTING_GUIDE.md](Coding/TROUBLESHOOTING_GUIDE.md), [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md) - Issues section |
| **Next steps** | [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md) - Phase 3 Roadmap |

---

## 📊 Key Metrics Summary

| Metric | Value |
|--------|-------|
| **Total Documentation Files** | 14 markdown files |
| **Total Code Files** | 2 notebooks (29 + 36 cells) |
| **Datasets Integrated** | 5 sources |
| **Total Data Records** | 347,896 |
| **Training Samples** | 13,030 (4 tasks) |
| **Prediction Tasks** | 4 (binding, hERG, Caco-2, clearance) |
| **Feature Dimensions** | 258 (2 physico + 256 Morgan ECFP4) |
| **Model Parameters** | 73,190 (current MultiTaskPKPDModel variant) |
| **Documentation Pages** | ~50 pages total |
| **Project Completion** | 65% (Phase 3 in progress) |

---

## ✅ Documentation Completeness Checklist

### Phase 1: Data Exploration ✓
- [x] Data loading documented
- [x] Visualizations created
- [x] Statistical analysis complete
- [x] Individual dataset docs
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
- [ ] Hit target metrics (binding R²>0.6, hERG AUROC>0.8, Caco-2 AUROC>0.75)
- [x] Phase 2→3 processed feature handoff completed (258-dim inputs)
- [ ] Task-specific fine-tuning for hERG/Caco-2 on frozen shared encoder
- [ ] Model interpretation and attention analysis

### Phase 4: Deployment (PENDING)
- [ ] API documentation
- [ ] User guide
- [ ] Model export procedure
- [ ] Deployment checklist

---

## 🔄 Version History

| Version | Date | Changes |
|---------|------|---------|
| **2.1** | Mar 4, 2026 | Phase 3 objective alignment + multi-variant benchmark updates (processed-feature ingestion, Caco-2 classification, focal/logits trials) |
| **2.0** | Feb 24, 2026 | Phase 3 Neural ODE model session — architecture, training, results |
| **1.0** | Feb 17, 2026 | Initial master index creation |
| **0.9** | Feb 4, 2026 | Original INDEX.md (superseded) |

---

## 📞 Navigation Tips

### Links Not Working?
All links use **relative paths** from the project root. If a link doesn't work:
1. Make sure you're viewing this file from project root
2. Check that the target file exists
3. File paths are case-sensitive

### Want to Add a New Document?
1. Create your markdown file in the appropriate directory
2. Update this MASTER_INDEX.md with:
   - Entry in timeline section (by date)
   - Entry in category section
   - Entry in quick search guide
   - Update metrics summary

### Printing Documentation?
For a complete documentation package:
1. [EXECUTIVE_SUMMARY.md](Coding/EXECUTIVE_SUMMARY.md) - 4 pages
2. [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md) - 18 pages
3. [TROUBLESHOOTING_GUIDE.md](Coding/TROUBLESHOOTING_GUIDE.md) - 8 pages

**Total**: ~30 pages

---

## 🎯 Next Actions

### For Continuing Development:
1. ✅ Open [phase3_neural_ode_model.ipynb](Coding/phase3_neural_ode_model.ipynb) — model is built and trained
2. ⏭️ Run task-specific fine-tuning for hERG/Caco-2 with frozen shared encoder
3. ⏭️ Evaluate: binding R²>0.6, hERG AUROC>0.8, Caco-2 AUROC>0.75
4. ⏭️ If targets met → Phase 4: deployment/API documentation

### For Understanding What Was Done:
1. ✅ Read [EXECUTIVE_SUMMARY.md](Coding/EXECUTIVE_SUMMARY.md)
2. ✅ Review visualizations in [phase1_2_data_exploration.ipynb](Coding/phase1_2_data_exploration.ipynb) cells 9-14
3. ✅ Read issues section in [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md)

### For Troubleshooting:
1. ✅ Check [TROUBLESHOOTING_GUIDE.md](Coding/TROUBLESHOOTING_GUIDE.md)
2. ✅ Search for error message in [PROJECT_SUMMARY.md](Coding/PROJECT_SUMMARY.md)
3. ✅ Review environment setup in [README.md](README.md)

---

**� Current Status: PHASE 3 IN PROGRESS — NEURAL ODE MODEL TRAINED, OPTIMIZING ADMET METRICS**

**Last Updated**: March 4, 2026  
**Maintained By**: Subrat  
**Project Progress**: 65% Complete (Phase 3 active — architecture done, metric targets pending)

---

_This master index supersedes the original INDEX.md and provides comprehensive navigation for all project documentation._

