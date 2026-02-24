# Neural_PK-PD_Modeling_with_ODE
Neural PK-PD Modeling: Integrating Mechanistic Priors with Neural ODEs

---

## 📚 **[→ MASTER INDEX - Complete Project Navigation](MASTER_INDEX.md)** ⭐

**New to this project?** The [MASTER_INDEX.md](MASTER_INDEX.md) provides complete navigation to all 14 documentation files, organized by date and reading order.

**Quick Links**:
- [📄 Executive Summary](Coding/EXECUTIVE_SUMMARY.md) - One-page overview
- [📋 Complete Project Documentation](Coding/PROJECT_SUMMARY.md) - Full story with issues & solutions
- [🔧 Troubleshooting Guide](Coding/TROUBLESHOOTING_GUIDE.md) - Problem solving reference
- [📓 Phase 1–2 Notebook](Coding/phase1_2_data_exploration.ipynb) - EDA & feature engineering (29 cells)

---

## Summary of Setup & Data Download Process

**Note**: This document covers initial setup (January 21, 2026). For current project status, see [MASTER_INDEX.md](MASTER_INDEX.md).

### **Initial Setup Steps**

1. **Created Python Virtual Environment**
   - Created `venv_pkpd` in the Coding folder
   - Initial Python version: 3.9.13

2. **Created Empty Jupyter Notebook**
   - Created `notebook.ipynb` in Coding folder (later renamed to `phase1_2_data_exploration.ipynb`)

3. **Python Version Upgrade**
   - **Problem**: System had Python 3.8.10, needed latest version
   - **Solution**: 
     - Downloaded Python 3.14.2 from python.org
     - Removed old Python 3.8 from `/Library/Frameworks/Python.framework/Versions/3.8`
     - Recreated `venv_pkpd` explicitly with Python 3.14: `/usr/local/bin/python3.14 -m venv`
   - **Final Result**: Python 3.14.2 in `venv_pkpd`

4. **Package Installation**
   - **Installed Core Packages** (143 total):
     - Scientific: numpy 2.4.1, scipy 1.17.0, pandas 3.0.0
     - Deep Learning: torch 2.10.0, torchdiffeq 0.2.5
     - ML: scikit-learn 1.8.0, tensorboard 2.20.0
     - Visualization: matplotlib 3.10.8, seaborn 0.13.2, plotly 6.5.2
     - Notebooks: jupyter 1.1.1, jupyterlab 4.5.3, ipython 9.9.0
     - Testing: pytest 9.0.2
     - Tracking: wandb 0.24.0
   - **Created**: requirements.txt with all dependencies

---

### **Dataset Download Implementation**

5. **Extracted Dataset Instructions**
   - Read PDF guide from Documentation folder
   - Identified primary sources:
     - PubChemRDF (compounds, assays, proteins)
     - PK-DB (PK time-courses & parameters)
     - TDC (ADMET benchmarks)
     - ChEMBL/BindingDB (target pharmacology)
     - ToxCast/Tox21 (safety endpoints)

6. **Created Data Download Script**
   - **File**: data_download.py
   - **Initial Implementation**: PubChem assays + compounds, PK-DB substances

7. **Problem #1: PubChem CYP3A4 Assay Failed**
   - **Issue**: AID 884 returned 400 BadRequest (legacy/disabled)
   - **Fix**: Updated to live AID 54772
   - **Result**: ✅ Downloaded assay_cyp3a4_inhibition_aid54772.csv

8. **Problem #2: PK-DB Substances Endpoint 404**
   - **Issue**: `/api/v1/substances/` returned 404 Not Found
   - **Investigation**: Probed API structure, found `/api/v1/studies/` working (200 OK)
   - **Fix**: Rewrote `fetch_pkdb_substances()` → `fetch_pkdb_studies()`
   - **Result**: ✅ Downloaded:
     - studies.json (796 studies, full metadata)
     - studies_top50.json (trimmed subset)

9. **Problem #3: PK-DB Time-Course Outputs Inaccessible**
   - **Issue**: Output endpoints require authentication or use different URL structure
   - **Attempted**: Multiple endpoint patterns (`/api/v1/outputs/{id}`, `/api/outputs/{id}`, etc.)
   - **Result**: ❌ All attempts failed (likely need credentials or web UI export)
   - **Added**: Helper function `fetch_pkdb_timecourses()` for future use

---

### **Final Downloaded Data**

**✅ Successfully Downloaded:**
- PubChem hERG assay: assay_herg_qhts_aid588834.csv
- PubChem CYP3A4 assay: assay_cyp3a4_inhibition_aid54772.csv
- PubChem compounds (3D SDF): warfarin, midazolam, caffeine
- PK-DB studies metadata: 796 studies with rich annotations

**❌ Unable to Download:**
- PK-DB time-course data (authentication/endpoint issues)

---

### **Key Files Created**

1. venv_pkpd - Python 3.14.2 virtual environment
2. requirements.txt - Package dependencies
3. phase1_2_data_exploration.ipynb - Jupyter notebook (originally created as notebook.ipynb)
4. data_download.py - Automated dataset fetcher
5. raw - Downloaded data directory structure

---

### **Next Steps Recommended**

1. **For PK-DB time-courses**: Export from web UI or obtain API credentials
2. **For bulk downloads**: Implement TDC tasks, ToxCast, ChEMBL fetchers
3. **Data preprocessing**: Parse SDF/CSV files into unified format for modeling