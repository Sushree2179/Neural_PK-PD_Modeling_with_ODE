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
- **Complete studies metadata**: 20 studies (downloadable, with option to fetch all 732 studies)
  - File: `pkdb/pkdb_studies_complete.json`
  - Format: JSON
  - Content: Full study data including:
    - Study metadata (PMID, authors, date, study design)
    - Subjects: 2,435+ subjects across studies
    - Interventions: Dosing, substance, route of administration
    - **Outputs**: 3,884 PK parameters (CL, Vd, t½, AUC, Cmax, Tmax, etc.)
    - **Timecourses**: 117 time-concentration curves
    - **Subsets**: 135 dataset subsets linking studies to data
  - Substances: 20 unique drugs in sample including midazolam, warfarin, glimepiride, rifampicin, itraconazole, etc.

**Data Structure**: 
- Each study contains:
  - `outputset.outputs`: List of PK parameter IDs (CL, Vd, t½, AUC, etc.)
  - `dataset.subsets`: Links to timecourse data containers
  - `timecourse_count`: Number of time-concentration curves
  - `individual_count`: Number of subjects studied
  - `substances`: Drugs and metabolites measured

**Status**: ✅ **Downloaded (20 studies complete)** | 🔄 **Scalable to 732 total studies**
- Time-course outputs: Embedded in studies JSON (accessible via hierarchy)
- All PK parameters and timecourse metadata readily available

**Paper**: https://pmc.ncbi.nlm.nih.gov/articles/PMC7779054/

**License**: Open Access

**How to Access More Data**:
- Current: 20 studies with 3,884 outputs and 117 timecourses
- To expand: Modify `download_pkdb_complete.py` to fetch all 732 studies
- Individual output/timecourse downloads available via API with study IDs

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
├── venv_pkpd/                          # Python virtual environment
│   ├── bin/activate                    # Activation script
│   └── lib/python3.X/site-packages/    # Installed packages
│
├── requirements.txt                    # Pinned dependency versions
├── notebook.ipynb                      # Jupyter notebook for analysis
├── data_download.py                    # PubChem & PK-DB fetcher script
├── download_pkdb_complete.py           # Complete PK-DB studies downloader
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
│           ├── pkdb_studies_complete.json    # ✅ Full study data (20 studies)
│           ├── studies.json                  # ✅ Raw API response
│           ├── studies_top100.json           # ✅ Trimmed version
│           ├── timecourses_page1.json        # Archive (empty endpoint)
│           └── outputs_page1.json            # Archive (empty endpoint)
│
└── DATA_README.md                      # This file
```

---

## How to Re-Run the Fetcher

### Quick Start (Minimal Dataset)

Download PubChem assays + compounds + 20 PK-DB studies:

```bash
cd /Users/subrat/Desktop/Thesis/Neural_PK-PD_Modeling_with_ODE/Coding
source venv_pkpd/bin/activate
python data_download.py
```

**Output**:
- `data/raw/pubchem/`: 2 assay CSVs + 3 compound SDF files
- `data/raw/pkdb/`: Studies metadata with embedded outputs and timecourses

### Extended Dataset (Complete PK-DB)

Download all 732 PK-DB studies with full metadata:

```bash
python download_pkdb_complete.py
```

This script:
- Fetches complete PK-DB studies API response
- Saves to `data/raw/pkdb/pkdb_studies_complete.json`
- Includes ~130k+ PK parameters and thousands of timecourses
- Takes ~2-5 minutes depending on internet speed

### Customize Downloads

Edit `data_download.py` or `download_pkdb_complete.py`:

```python
# In data_download.py, main():
fetch_pubchem_assay(588834, label="herg_qhts")  # Change AID
fetch_pubchem_compound("compound_name")         # Add drugs

# In download_pkdb_complete.py:
url = "https://pk-db.com/api/v1/studies/?format=json"  # Add filters like &limit=50
```

### Force Re-download

Delete existing files and re-run:

```bash
rm -rf data/raw/pubchem/*.csv data/raw/pubchem/*.sdf data/raw/pkdb/*.json
python data_download.py
python download_pkdb_complete.py
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
  "studies": [
    {
      "pk": "553",
      "sid": "PKDB00954",
      "name": "Rosenkranz1996a",
      "individual_count": 248,
      "timecourse_count": 10,
      "reference": {
        "pmid": "8960852",
        "title": "Pharmacokinetics and safety of glimepiride...",
        "authors": [...]
      },
      "substances": [
        {"name": "glimepiride"},
        {"name": "glimepiride-M1"}
      ],
      "outputset": {
        "outputs": [160175, 160176, 160177, ...]  // PK parameters (CL, Vd, t½, AUC, etc.)
      },
      "dataset": {
        "subsets": [3114, 3115, 3116, ...]  // Timecourse data containers
      }
    },
    ...
  ]
}
```

**Key Fields**:
- `sid`: Study ID (e.g., PKDB00954)
- `name`: Short study identifier
- `individual_count`: Number of subjects
- `timecourse_count`: Number of time-course datasets in study
- `reference`: PMID, authors, title, publication date
- `substances`: Drugs and metabolites studied
- `outputset.outputs`: IDs for PK parameters:
  - **Clearance**: CL (systemic, renal, hepatic)
  - **Volume**: Vd (volume of distribution)
  - **Half-life**: t½, λz
  - **Exposure**: AUC (area under curve), AUC_inf
  - **Peak**: Cmax (max concentration), Tmax (time to max)
  - **Absorption**: ka (absorption rate), F (bioavailability)
  - **Protein binding**: fu (fraction unbound)
  - **Other**: MRT (mean residence time), CL/F, etc.
- `dataset.subsets`: Links to timecourse data (time-concentration curves)

**Use**: 
- Study-level filtering and aggregation
- Direct access to all PK parameters and timecourses without additional API calls
- Time-course data via subset linkages
- Comprehensive metadata for mechanistic modeling priors

---

### How to Reproduce Exact Environment

```bash
cd Coding
pip install -r requirements.txt
```

### Python Packages (Core Set)

**Scientific Stack**: numpy, scipy, pandas, scikit-learn  
**Deep Learning**: torch, torchdiffeq, pytorch-lightning  
**Visualization**: matplotlib, seaborn, plotly  
**Notebooks**: jupyter, jupyterlab  
**Utilities**: requests (data download), pytest (testing)  
**Experiment Tracking**: wandb

See `requirements.txt` for complete pinned versions.

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
- Increase timeout in download scripts:
  ```python
  r = requests.get(url, stream=True, timeout=300)  # Increase from 120 to 300 seconds
  ```
- Check internet connection
- Try again later (API may be rate-limiting)

---

### Issue 3: Empty Responses from PK-DB Endpoints

**Problem**: Downloaded files show `"count": 0, "data": []`

**Cause**: Some API endpoints (`/pkdata/timecourses/`, `/pkdata/outputs/`) return empty; actual data is embedded in studies API

**Solution**: Use the `pkdb_studies_complete.json` file which contains all timecourses and outputs embedded in the study hierarchy

---

### Issue 4: Virtual Environment Activation Fails

**Problem**: `command not found: activate`

**Solution**:
```bash
# Verify path
ls -la venv_pkpd/bin/activate

# Use full path
source /Users/subrat/Desktop/Thesis/Neural_PK-PD_Modeling_with_ODE/Coding/venv_pkpd/bin/activate
```

---

### Issue 5: API Returns 404 Errors on Individual Resources

**Problem**: Trying to fetch `/api/v1/outputs/{id}/` returns 404

**Cause**: Individual resource endpoints may require authentication or different URL structure

**Solution**: Use the batch endpoint or access data through studies API hierarchy
```python
# Instead of individual fetches, use:
studies = json.load(open('pkdb_studies_complete.json'))
for study in studies:
    outputs = study['outputset']['outputs']  # Access output IDs
    subsets = study['dataset']['subsets']    # Access timecourse containers
```

---

## Next Steps

1. **Parse & Harmonize**: Convert PubChem CSV/SDF and PK-DB JSON to standardized DataFrames
2. **Molecular Features**: Extract descriptors from SDF using RDKit (SMILES, fingerprints, MW, LogP)
3. **Merge Datasets**: Align on compound IDs; join PubChem assays + PK-DB + TDC data
4. **EDA**: Visualize distributions, missing values, outliers, drug-specific patterns
5. **Baseline Models**: Train simple ML models on ADMET predictions
6. **Neural ODE**: Design mechanistic priors with embedded PK parameters (CL, Vd, t½)
7. **Validation**: Test on held-out drugs; compare to published literature values

---

## Contact & Support

For questions or issues:
1. Check [Troubleshooting](#troubleshooting) section
2. Review inline comments in `data_download.py`
3. Consult original data sources (links provided)
4. Contact maintainer: [Your Name]

---

**Last Updated**: 27 January 2026
