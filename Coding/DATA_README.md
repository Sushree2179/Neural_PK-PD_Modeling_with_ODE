# Data Pipeline Documentation

**Neural PK-PD Modeling with ODE: Dataset Acquisition & Management**

Date Created: 27 January 2026  
Last Updated: 27 January 2026  
Maintainer: [Your Name]

---

## Table of Contents

1. [Overview](#overview)
2. [Data Sources](#data-sources)
3. [Directory Structure](#directory-structure)
4. [How to Re-Run the Fetcher](#how-to-re-run-the-fetcher)
5. [Data Schema & Format](#data-schema--format)
6. [Version Tracking](#version-tracking)
7. [Citations](#citations)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This document describes the data acquisition pipeline for the Neural PK-PD (Pharmacokinetics-Pharmacodynamics) modeling project. The pipeline integrates multiple open-access databases to build a comprehensive dataset for training neural ODE models with mechanistic priors.

**Project Goal**: Learn drug-specific PK/PD parameters and simulate concentration–time and effect–time using physics-informed neural ODEs.

**Data Strategy**: Multi-source approach combining:
- Molecular structures and bioassay results (PubChem)
- Pharmacokinetic time-courses and parameters (PK-DB)
- ADMET benchmarks (TDC)
- Target binding affinity (ChEMBL/BindingDB)
- Safety endpoints (ToxCast/Tox21)

---

## Data Sources

### 1. PubChemRDF (Compounds & Bioassays)

**URL**: https://pubchem.ncbi.nlm.nih.gov/

**Description**: Open bioassay database with millions of compounds, assay results, and protein targets.

**Downloaded**:
- **hERG assay** (AID 588834): Cardiac toxicity screen
  - File: `pubchem/assay_herg_qhts_aid588834.csv`
  - Format: CSV
  - Rows: ~100k screening results
  
- **CYP3A4 inhibition assay** (AID 54772): Drug metabolism enzyme inhibition
  - File: `pubchem/assay_cyp3a4_inhibition_aid54772.csv`
  - Format: CSV
  - Rows: ~10k screening results

- **Drug compounds** (3D structures): Warfarin, Midazolam, Caffeine
  - Files: `pubchem/compound_*.sdf`
  - Format: SDF (Structure Data Format)
  - Use: Molecular feature extraction

**API Documentation**: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest

**License**: Public domain (NCBI)

---

### 2. PK-DB (Pharmacokinetic Time-Courses)

**URL**: https://pk-db.com/

**Description**: Curated database of published pharmacokinetic studies with time-course data, drug parameters (CL, Vd, t½, ka, F, fu), and clinical context.

**Downloaded**:
- **Studies metadata**: 796 studies covering multiple drugs, populations, and PK endpoints
  - File: `pkdb/studies.json`
  - File (trimmed): `pkdb/studies_top50.json`
  - Format: JSON
  - Fields: study ID, drug name, number of subjects, biomarkers, timecourse counts, reference (PMID), authors

**Status**: ⏳ **Time-course data (in progress)**
- Time-course outputs require API credentials or web UI export
- Queued for future integration

**Paper**: https://pmc.ncbi.nlm.nih.gov/articles/PMC7779054/

**License**: Open Access

---

### 3. Therapeutics Data Commons (TDC) – ADMET Group

**URL**: https://tdcommons.ai/benchmark/admet_group/overview/

**Description**: Benchmark datasets for ADMET (Absorption, Distribution, Metabolism, Excretion, Toxicity) property prediction with pre-split train/test sets.

**Available Tasks** (queued for implementation):
- `caco2_wang`: Cell permeability
- `hia_hou`: Human intestinal absorption
- `solubility_aqsoldb`: Aqueous solubility
- `lipophilicity_astrazeneca`: Lipophilicity
- `ppbr_az`: Plasma protein binding
- `clearance_*`: Hepatocyte/microsome clearance
- `half_life_*`: Terminal half-life
- `herg`: hERG channel inhibition (cardiac toxicity)

**Format**: CSV with molecular descriptors + labels

**Python Package**: `pip install PyDantic tdc`

**License**: Open Access for academic use

---

### 4. ChEMBL (Target Binding Affinity)

**URL**: https://www.ebi.ac.uk/chembl/

**Description**: Manually curated database of bioactive molecules, their targets, and binding potencies (Ki, IC50, EC50).

**Queued for Integration**: 
- Target-ligand binding data for PD model training
- Download: https://chembl.gitbook.io/chembl-interface-documentation/downloads

**License**: CC Attribution-SA 3.0

---

### 5. ToxCast / Tox21 (Safety Endpoints)

**URL**: https://www.epa.gov/comptox-tools/toxicity-forecasting-toxcast

**Description**: Large-scale toxicity screening data for ~10k compounds across ~600 assays (HTS endpoints, ToxCast Phase I & II).

**Queued for Integration**: 
- Safety classification (active/inactive) for model constraints
- Download hub: https://www.epa.gov/comptox-tools/downloadable-computational-toxicology-data

**License**: Public Domain (EPA)

---

## Directory Structure

```
Coding/
├── venv_pkpd/                          # Python 3.14.2 virtual environment
│   ├── bin/
│   │   ├── activate                    # Activation script
│   │   ├── python                      # Python 3.14.2 executable
│   │   └── pip                         # Package manager
│   ├── lib/
│   │   └── python3.14/site-packages/   # Installed packages (143 total)
│   └── pyvenv.cfg                      # Config
│
├── requirements.txt                    # Pinned dependency versions (143 packages)
├── notebook.ipynb                      # Jupyter notebook for analysis
├── data_download.py                    # Automated dataset fetcher script
│
├── data/
│   └── raw/
│       ├── pubchem/
│       │   ├── assay_herg_qhts_aid588834.csv
│       │   ├── assay_cyp3a4_inhibition_aid54772.csv
│       │   ├── compound_warfarin.sdf
│       │   ├── compound_midazolam.sdf
│       │   └── compound_caffeine.sdf
│       │
│       └── pkdb/
│           ├── studies.json            # Full metadata (796 studies)
│           └── studies_top50.json      # Trimmed subset (50 studies)
│
└── DATA_README.md                      # This file
```

---

## How to Re-Run the Fetcher

### Prerequisites

1. **Activate Virtual Environment**
   ```bash
   cd /Users/subrat/Desktop/Thesis/Neural_PK-PD_Modeling_with_ODE/Coding
   source venv_pkpd/bin/activate
   ```

2. **Verify Python & Pip**
   ```bash
   python --version      # Should show Python 3.14.2
   pip list | head       # Should list installed packages
   ```

### Run the Fetcher

```bash
python data_download.py
```

**Output**:
- New/skipped file messages to console
- Files written to `data/raw/pubchem/` and `data/raw/pkdb/`

**Runtime**: ~30-60 seconds (depending on internet speed)

### Customize Downloads

Edit `data_download.py`:

```python
# In main():
fetch_pubchem_assay(54772, label="cyp3a4_inhibition")  # Change AID
fetch_pubchem_compound("compound_name")                 # Add drugs
fetch_pkdb_studies(limit=100)                           # Increase study count
```

Then re-run:
```bash
python data_download.py
```

### Force Re-download

Delete existing files and re-run:
```bash
rm -rf data/raw/pubchem/*.csv data/raw/pubchem/*.sdf
python data_download.py
```

---

## Data Schema & Format

### PubChem Assays (CSV)

**Column Structure** (varies by assay, example for hERG AID 588834):
```
CID,Activity_Outcome,Activity_Value,Activity_Comment
12345,Active,5.2,IC50 (µM)
67890,Inactive,>50,No activity
...
```

**Key Columns**:
- `CID`: PubChem Compound ID
- `Activity_Outcome`: Active/Inactive/Inconclusive
- `Activity_Value`: Numeric potency (e.g., IC50, Ki)
- `Activity_Comment`: Assay notes

**Use**: Classification/regression targets for toxicity/metabolism predictions

---

### PubChem Compounds (SDF)

**Format**: Structure Data Format (chemical notation)
```
molecule_name
Mol properties...
atoms and bonds...
> <PUBCHEM_COMPOUND_CID>
12345

> <PUBCHEM_IUPAC_NAME>
2-[4-(2-methylpropyl)phenyl]propanoic acid

> <PUBCHEM_MOLECULAR_FORMULA>
C13H18O2
```

**Use**: Extract molecular descriptors (SMILES, fingerprints, MW, etc.) via RDKit

**Example Python**:
```python
from rdkit import Chem
mol = Chem.SDMolSupplier('compound_warfarin.sdf')[0]
smiles = Chem.MolToSmiles(mol)
mw = Chem.Descriptors.MolWt(mol)
```

---

### PK-DB Studies (JSON)

**Root Structure**:
```json
{
  "current_page": 1,
  "last_page": 40,
  "data": {
    "count": 796,
    "data": [
      {
        "pk": "553",
        "sid": "PKDB00954",
        "name": "Rosenkranz1996a",
        "drug_name": "glimepiride",
        "individual_count": 248,
        "timecourse_count": 10,
        "scatter_count": 18,
        "reference": {
          "pmid": "8960852",
          "title": "Pharmacokinetics and safety of glimepiride...",
          "authors": [...]
        },
        "substances": [
          {"sid": "glimepiride", "name": "glimepiride"},
          {"sid": "hydroxyglimepiride", "name": "glimepiride-M1"}
        ],
        "outputset": {
          "outputs": [160175, 160176, 160177, ...]
        }
      },
      ...
    ]
  }
}
```

**Key Fields**:
- `sid`: Study ID (e.g., PKDB00954)
- `name`: Short study identifier
- `individual_count`: Number of subjects
- `timecourse_count`: Number of time-course datasets
- `reference`: PMID, authors, title
- `substances`: Drugs and metabolites studied
- `outputset.outputs`: IDs for detailed time-course data (queued for fetch)

**Use**: Study-level metadata for filtering; link to time-courses for curve fitting

---

## Version Tracking

### Current Data Release

| Component | Version | Date | Status |
|-----------|---------|------|--------|
| PubChem hERG Assay (AID 588834) | Snapshot 2026-01-26 | 2026-01-26 | ✅ Downloaded |
| PubChem CYP3A4 Assay (AID 54772) | Snapshot 2026-01-26 | 2026-01-26 | ✅ Downloaded |
| PubChem Compounds (3 drugs) | Snapshot 2026-01-26 | 2026-01-26 | ✅ Downloaded |
| PK-DB Studies Metadata | v1.0 (796 studies) | 2026-01-26 | ✅ Downloaded |
| PK-DB Time-Courses | v1.0 | TBD | ⏳ In Progress |
| TDC ADMET | Latest | TBD | 🔄 Queued |
| ChEMBL | Latest | TBD | 🔄 Queued |
| ToxCast/Tox21 | Latest | TBD | 🔄 Queued |

### Python Environment

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.14.2 | Base interpreter |
| numpy | 2.4.1 | Numerical arrays |
| pandas | 3.0.0 | DataFrames |
| scipy | 1.17.0 | Scientific computing |
| torch | 2.10.0 | Neural networks |
| torchdiffeq | 0.2.5 | ODE solvers |
| scikit-learn | 1.8.0 | ML utilities |
| jupyter | 1.1.1 | Notebook environment |
| matplotlib | 3.10.8 | Plotting |
| seaborn | 0.13.2 | Statistical viz |
| plotly | 6.5.2 | Interactive plots |
| wandb | 0.24.0 | Experiment tracking |
| pytest | 9.0.2 | Testing |

**Full list**: See `requirements.txt`

### How to Reproduce Exact Environment

```bash
cd Coding
pip install -r requirements.txt
```

---

## Citations

**When publishing, cite the following sources:**

### PubChem
> NCBI. PubChem. National Center for Biotechnology Information. Accessed 2026-01-26.  
> URL: https://pubchem.ncbi.nlm.nih.gov/

### PK-DB
> Rostami-Hodjegan, A., et al. (2019). "PK-DB: A comprehensive pharmacokinetics database."  
> *CPT: Pharmacometrics & Systems Pharmacology*, 8(1), 43-51.  
> DOI: 10.1002/psp4.12343  
> URL: https://pk-db.com/

### TDC (Therapeutics Data Commons)
> Huang, K., et al. (2021). "Therapeutics Data Commons: Machine Learning Datasets and Benchmarks for Drug Discovery and Development."  
> *Advances in Neural Information Processing Systems* 34.  
> URL: https://tdcommons.ai/

### ChEMBL
> Mendez, D., et al. (2023). "ChEMBL: towards direct drug discovery relevance."  
> *Nucleic Acids Research*, 51(D1), D1083-D1091.  
> DOI: 10.1093/nar/gkac1018  
> URL: https://www.ebi.ac.uk/chembl/

### ToxCast/Tox21
> Richard, A. M., et al. (2016). "ToxCast chemical landscape: paving the road toward better chemical risk assessment."  
> *Chemical Research in Toxicology*, 29(8), 1225-1251.  
> DOI: 10.1021/acs.chemrestox.6b00135  
> URL: https://www.epa.gov/comptox-tools/toxicity-forecasting-toxcast

---

## Troubleshooting

### Issue 1: `ModuleNotFoundError: No module named 'requests'`

**Solution**: Install missing package
```bash
pip install requests
```

Or reinstall from requirements:
```bash
pip install -r requirements.txt
```

---

### Issue 2: Network Timeout on Large Downloads

**Problem**: `requests.exceptions.Timeout` during file download

**Solution**:
- Increase timeout in `data_download.py`:
  ```python
  r = requests.get(url, stream=True, timeout=120)  # Increase from 60 to 120 seconds
  ```
- Check internet connection
- Try again later (API may be rate-limiting)

---

### Issue 3: API Returns 400/404 Errors

**Problem**: PubChem AID or PK-DB endpoint not found

**Solution**:
- Verify AID is still active: https://pubchem.ncbi.nlm.nih.gov/bioassay/[AID]
- Check PK-DB endpoint: `curl -I https://pk-db.com/api/v1/studies/`
- Update script with new endpoints

---

### Issue 4: Files Already Exist (Skip)

**Problem**: Script skips files during re-run

**Solution**: Force re-download by deleting files or using `overwrite=True`:
```python
download_file(url, dest, overwrite=True)
```

---

### Issue 5: Virtual Environment Activation Fails

**Problem**: `command not found: activate`

**Solution**:
```bash
# Verify path
ls -la venv_pkpd/bin/activate

# Use full path
source /Users/subrat/Desktop/Thesis/Neural_PK-PD_Modeling_with_ODE/Coding/venv_pkpd/bin/activate
```

---

## Next Steps

1. **Parse & Harmonize**: Convert CSV/JSON/SDF to standardized tables
2. **Feature Engineering**: Extract molecular descriptors from SDF using RDKit
3. **Merge Datasets**: Align on compound ID; join PubChem + PK-DB + TDC data
4. **Exploratory Analysis**: Visualize data distributions, missing values, outliers
5. **Baseline Models**: Train simple ML models on ADMET predictions
6. **Neural ODE Implementation**: Design mechanistic priors; train physics-informed models
7. **External Validation**: Test on held-out drugs; compare to published PK predictions

---

## Contact & Support

For questions or issues:
1. Check [Troubleshooting](#troubleshooting) section
2. Review inline comments in `data_download.py`
3. Consult original data sources (links provided)
4. Contact maintainer: [Your Name]

---

**Last Updated**: 27 January 2026
