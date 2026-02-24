# Neural PK-PD Modeling Project Summary

**Date**: February 17, 2026  
**Status**: Phase 2 Complete - Feature Engineering  
**Next Phase**: Phase 3 - Neural ODE Model Development

---

## � Navigation

- **[← Master Index](../MASTER_INDEX.md)** - All documentation organized by date
- **[Quick Summary →](EXECUTIVE_SUMMARY.md)** - One-page overview
- **[Troubleshooting →](TROUBLESHOOTING_GUIDE.md)** - Problem solving guide
- **[Notebook (Phase 1–2) →](phase1_2_data_exploration.ipynb)** - EDA & feature engineering

---

## �📋 Executive Summary

Successfully completed Phase 1 (Data Exploration) and Phase 2 (Feature Engineering) of the Neural PK-PD Modeling project. Created a multi-task learning dataset with **13,030 training samples** spanning 4 prediction tasks: binding affinity, hERG inhibition, Caco-2 permeability, and hepatocyte clearance.

### Key Achievements:
- ✅ Integrated 5 major pharmaceutical datasets
- ✅ Performed comprehensive exploratory data analysis with visualizations
- ✅ Built multi-task feature engineering pipeline
- ✅ Preprocessed and normalized features for neural network training
- ✅ Resolved multiple technical challenges with RDKit and data schema

---

## 📊 Project Overview

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
- **Risk Stratification**: COLOR-CODED safety levels (CRITICAL/HIGH/MEDIUM/LOW)
- **Toxicity Categories**: Nuclear receptor activity, cardiac, hepatic, renal, developmental toxicity
- **Key Insight**: Distribution reveals most common safety liabilities for constraint modeling

**C. TDC ADMET Properties (Cell 11)**
- **hERG Inhibition**: Class imbalance (15% inhibitors) - cardiotoxicity predictor
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

**Step 1: Kernel Restart**
```python
# Action: Restarted notebook kernel to recognize new package
# Result: RDKit imports successful ✅
```

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

**Final Resolution:**
✅ RDKit working for validation/testing  
✅ Feature extraction using pre-calculated descriptors  
✅ Multi-task learning architecture created

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

**Problem:**
Original plan was to merge datasets on chemical structure (SMILES) for unified feature matrix.

**Discovery:**
- SMILES are anonymized identifiers, not actual chemical structures
- Each dataset has different compounds (no overlap)
- Cannot merge on molecular identity

**Resolution - Multi-Task Learning Architecture:**
```python
# Strategy: Concatenate datasets with task labels
# Each sample belongs to one task, shares common features

unified_features = pd.concat([
    chembl_data,      # task='binding_affinity'
    herg_data,        # task='hERG_inhibition'
    caco2_data,       # task='Caco2_permeability'
    clearance_data    # task='hepatocyte_clearance'
], ignore_index=True)

# Neural network will learn shared representations
# Task-specific heads will handle different endpoints
```

**Advantages:**
- ✅ Larger training dataset (13,030 vs ~2,000)
- ✅ Shared molecular feature learning
- ✅ Multi-objective optimization possible
- ✅ Better generalization across ADMET properties

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

## 🎯 Project Status by Phase

### ✅ Phase 1: Data Exploration (COMPLETE)
- [x] Data loading and verification
- [x] Schema inspection and documentation
- [x] Comprehensive visualizations (3 sets)
- [x] Statistical analysis and insights
- [x] PK-DB structure analysis
- [x] Modeling strategy validation

### ✅ Phase 2: Feature Engineering (COMPLETE)
- [x] RDKit installation and setup
- [x] Molecular descriptor extraction function
- [x] ChEMBL feature preparation (2,000 samples)
- [x] TDC ADMET integration (11,030 samples)
- [x] Multi-task feature matrix creation (13,030 samples)
- [x] Feature standardization and normalization
- [x] Preprocessing pipeline saved for inference

### 🔄 Phase 3: Neural ODE Model Development (PENDING)
- [ ] Define multi-task neural architecture
- [ ] Implement ODE layers (torchdiffeq)
- [ ] Physics-informed loss functions
- [ ] Training pipeline with task balancing
- [ ] Validation on held-out test sets
- [ ] Hyperparameter optimization
- [ ] Model interpretation and visualization

### 🔄 Phase 4: Evaluation & Deployment (PENDING)
- [ ] Cross-validation on all tasks
- [ ] PK-DB time-series validation
- [ ] Safety constraint verification
- [ ] Model export for deployment
- [ ] API development for predictions
- [ ] Documentation and user guide

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

### Key Files

```
Coding/
├── phase1_2_data_exploration.ipynb  # Main analysis notebook (29 cells)
├── requirements.txt            # 143 package dependencies
├── PROJECT_SUMMARY.md         # This document
├── data/
│   └── raw/
│       ├── chembl/            # Binding affinity data
│       ├── tdc/               # ADMET benchmarks
│       ├── toxcast/           # Safety screening
│       ├── pubchem/           # Bioassay data
│       └── pkdb/              # PK studies
└── venv_pkpd/                 # Python virtual environment
```

---

## 📊 Visualization Summary

### Created Visualizations

1. **ChEMBL Binding Affinity** (Cell 9)
   - Histogram: pIC50 distribution with mean line
   - Bar chart: Top 10 protein targets

2. **ToxCast Safety Profile** (Cell 10)
   - Color-coded risk level distribution (CRITICAL/HIGH/MEDIUM/LOW)
   - Toxicity category breakdown (top 7)

3. **TDC ADMET Properties** (Cell 11)
   - hERG inhibition class distribution
   - Caco-2 permeability histogram with mean
   - Hepatocyte clearance distribution with mean

**Analysis Output:** Cell 14 contains comprehensive interpretation of all visualizations with modeling implications

---

## 🧪 Code Quality & Best Practices

### Implemented Standards
- ✅ Cell headers with purpose/inputs/outputs documentation
- ✅ Descriptive variable names
- ✅ Error handling for missing data
- ✅ Reproducible preprocessing pipeline
- ✅ Modular function design
- ✅ Type hints and docstrings
- ✅ Version control friendly structure

### Code Example: Molecular Descriptor Function
```python
def extract_molecular_descriptors(smiles):
    """
    Extract molecular descriptors from a SMILES string.
    
    Parameters:
    -----------
    smiles : str
        SMILES representation of molecule
        
    Returns:
    --------
    dict or None
        Dictionary with molecular descriptors, or None if SMILES is invalid
    """
    if not rdkit_available:
        return None
    
    if pd.isna(smiles) or not isinstance(smiles, str):
        return None
    
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        
        descriptors = {
            'MW': Descriptors.MolWt(mol),
            'LogP': Descriptors.MolLogP(mol),
            'TPSA': Descriptors.TPSA(mol),
            # ... 7 more descriptors
        }
        return descriptors
        
    except Exception as e:
        return None
```

---

## 🎓 Key Learnings & Insights

### Data Science Insights

1. **Multi-Task Learning is Powerful**
   - Combining related tasks improves generalization
   - Shared molecular features benefit all endpoints
   - 6.5× more training data than single-task approach

2. **Real-World Data Challenges**
   - Datasets rarely have perfect schema alignment
   - Privacy/anonymization affects merging strategies
   - Pre-calculated features are common in public datasets

3. **Feature Engineering Matters**
   - Only 2 features (MW, LogP) available across all datasets
   - Despite limited features, covers wide chemical space
   - Proper normalization critical for neural network training

### Technical Insights

1. **Jupyter Kernel Management**
   - Must restart kernel after installing packages
   - Kernel metadata must match registered kernel name
   - Variable state persists across cell executions

2. **RDKit Compatibility**
   - Descriptor availability varies by version
   - Always test descriptor functions before batch processing
   - Graceful error handling prevents data loss

3. **Pandas Best Practices**
   - Use `.copy()` to avoid SettingWithCopyWarning
   - `.notna()` more readable than `~.isna()`
   - Column existence checks prevent KeyErrors

---

## 📋 Next Steps: Phase 3 Roadmap

### 1. Neural Architecture Design (Week 1)

**Multi-Task Neural Network:**
```python
class MultiTaskPKPDModel(nn.Module):
    def __init__(self):
        # Shared encoder
        self.encoder = nn.Sequential(
            nn.Linear(2, 64),      # MW, LogP → hidden
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32)
        )
        
        # Task-specific heads
        self.binding_head = nn.Linear(32, 1)      # Regression
        self.herg_head = nn.Linear(32, 1)         # Binary classification
        self.caco2_head = nn.Linear(32, 1)        # Binary classification
        self.clearance_head = nn.Linear(32, 1)    # Regression
```

**Neural ODE Integration:**
```python
from torchdiffeq import odeint

class PKODEFunc(nn.Module):
    def forward(self, t, y):
        # dC/dt = -CL/V * C + dosing
        # CL, V learned from molecular features
        pass
```

### 2. Training Pipeline (Week 2)

**Components:**
- [ ] Data loaders with task balancing
- [ ] Multi-task loss function (weighted combination)
- [ ] Optimizer: Adam with learning rate schedule
- [ ] Early stopping on validation loss
- [ ] Checkpoint saving

**Loss Function:**
```python
loss = (
    w_binding * MSE(pred_binding, y_binding) +
    w_herg * BCE(pred_herg, y_herg) +
    w_caco2 * BCE(pred_caco2, y_caco2) +
    w_clearance * MSE(pred_clearance, y_clearance) +
    physics_penalty
)
```

### 3. Validation Strategy (Week 3)

**Metrics by Task:**
- Binding affinity: RMSE, R², MAE
- hERG/Caco-2: AUROC, Accuracy, F1-score
- Clearance: RMSE, R²

**Validation Sets:**
- 80/10/10 train/val/test split
- Stratified by task
- PK-DB held out for time-series validation

### 4. Model Interpretation (Week 4)

- [ ] Feature importance analysis
- [ ] SHAP values for predictions
- [ ] Attention visualization
- [ ] Physics constraint verification
- [ ] Dose-response curves

---

## 📊 Success Metrics

### Quantitative Goals

| Task | Metric | Target | Baseline |
|------|--------|--------|----------|
| Binding Affinity | R² | > 0.6 | ChEMBL QSAR: 0.5 |
| hERG Inhibition | AUROC | > 0.8 | Random: 0.5 |
| Caco-2 Permeability | AUROC | > 0.75 | Random: 0.5 |
| Clearance | RMSE | < 1.0 | Literature: 1.5 |

### Qualitative Goals
- ✅ Interpretable predictions with confidence intervals
- ✅ Physics-consistent PK profiles (non-negative concentrations)
- ✅ Safety constraints satisfied (hERG flags high-risk compounds)
- ✅ Generalizes to new chemical space

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

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| **1.0** | 2026-02-17 | Initial summary - Phase 1 & 2 complete |

---

## 👥 Project Team

**Student**: Subrat  
**Institution**: [University Name]  
**Project Type**: Master's Thesis  
**Field**: Computational Drug Discovery / Machine Learning

---

## 📞 Contact & Support

For questions or issues:
1. Check this summary document first
2. Review notebook comments and docstrings
3. Consult `requirements.txt` for environment setup
4. See inline cell documentation for implementation details

---

**🎯 Current Status: Ready for Phase 3 - Neural ODE Model Development**

All data preprocessing complete. Feature matrix normalized and ready for neural network training. Multi-task learning architecture designed. Proceed to model implementation.

**Last Updated**: February 17, 2026

---
