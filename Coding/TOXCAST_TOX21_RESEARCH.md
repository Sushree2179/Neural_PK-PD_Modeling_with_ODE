# ToxCast and Tox21 Toxicity Screening Database Research

**Date:** February 4, 2026  
**Source:** EPA CompTox and Tox21 official documentation

---

## 1. ASSAY TYPES AND SAFETY ENDPOINTS

### Overview
ToxCast is a US EPA high-throughput screening (HTS) program that provides **publicly available bioactivity data** from assays evaluating chemical effects on diverse biological targets. Data is aggregated from **20+ assay sources** including the **Tox21 program** (multi-agency federal collaboration: EPA, NCATS/NIH, NIEHS, FDA).

### Safety Endpoint Categories

#### **Nuclear Receptors & Endocrine Disruption**
- **Estrogen Receptor (ER)**: Agonist and antagonist activity
- **Androgen Receptor (AR)**: Agonist and antagonist activity
- **Thyroid Hormone Receptor (TSHR)**: 
  - TSHR 2D agonist/antagonist
  - TSHR 3D agonist/antagonist (T4 hormone activity)
- **GnRH Receptor (GNRHR)**: Agonist activity
- **Glucocorticoid Receptor (GR)**
- **Other nuclear receptors**: Measured in standard formats

#### **Cardiac/Cardiovascular Safety**
- **hERG (human Ether-a-go-go Related Gene) Channel**: Cardiac action potential
  - Example: AEID3210_TOX21_hERG_U2OS_Antagonist
- **Cardiovascular developmental endpoints**

#### **Developmental & Reproductive Toxicity**
- **Zebrafish developmental assays** (Tanguay):
  - CRAN (Craniofacial abnormalities)
  - BRN (Brain development)
  - LTRK (Locomotor/Trunk development)
  - TCHR (Tail/Chorion abnormalities)
- **Developmental pathway disruption**
- **Reproductive development assessment**

#### **Liver & Metabolic Function**
- **Liver binding assays**: e.g., AEID2808_UTOR_hL-FABP (Fatty Acid Binding Protein)
- **Hepatocyte toxicity markers**

#### **Cell Cycle & Stress Response**
- **p53 pathway**: DNA damage response (e.g., AEID3331_TOX21_p53_BLA - Beta-lactamase assay)
- **Cell cycle function**
- **Apoptosis markers**

#### **Mitochondrial Function**
- **Mitochondrial toxicity endpoints**
- **ATP depletion**: AEID3247_CCTE_Deisenroth_TSHR_3D_Ag_CTOX_ATP
- **Mitochondrial membrane potential**

#### **Transcriptional & Gene Expression**
- **Transcriptional response profiling**
- **Target binding assays**
- **Co-activator recruitment**: e.g., AEID3318_ERF_TW_NR_COA_hNR1I2

#### **Ecotoxicity**
- **Aquatic organism toxicity**: 
  - Example: AEID3149_ATG_M_06_EcoTox2
- **Environmental species impact assessment**

#### **Cytotoxicity & Cell Viability**
- **General cytotoxicity burst assays**
- **Cell survival markers**
- **Morphological changes**

---

## 2. DATABASE STATISTICS & COMPOUND COVERAGE

### Key Numbers
- **~9,403 unique substances (DTXSIDs)** evaluated through ToxCast/Tox21
- **1,647 assay endpoints** documented (invitrodb v4.3, August 2025)
- **20+ assay source organizations** contributing data
- **~10,000 chemicals** screened in various assays
- **Multiple testing organizations**: Universities, contract research organizations, EPA internal labs

---

## 3. DATA STRUCTURES AND FORMATS

### Recommended Data Organization
Data is available in multiple formats through the **invitrodb (in vitro database)** - a relational MySQL database:

#### **Primary Format: MySQL Database**
- **Database Name**: invitrodb (latest: v4.3, released September 2024)
- **Contains**: 
  - Raw concentration-response data
  - Curve-fitted parameters
  - Assay metadata
  - Quality control metrics
  - Chemical structure information

#### **File Format Options Available**
1. **CSV/Text Summary Files**:
   - Assay annotations
   - Assay target mappings
   - Cytotoxicity burst output
   - Analytical QC reports
   - Chemical information spreadsheets

2. **Structured Data Components**:
   - Chemical structures (SDF format)
   - DSSTox standard fields:
     - Chemical names
     - CAS Registry Numbers (CASRN)
     - InChI strings and keys
     - SMILES notation
     - Structures
     - DTXSIDs (EPA chemical identifiers)

### Data Structure Example
```
Typical ToxCast Record Fields:
- Compound ID (DTXSID, CAS, SMILES)
- Assay Endpoint ID (AEID)
- Assay Name
- Organism/Cell Type
- Measurement Type (concentration-response)
- Hit Call (Active/Inactive)
- Potency (AC50 - activity concentration at 50% effect)
- Relative Efficacy (efficacy measure)
- Quality Metrics
- Concentration range tested
- Response direction
- Confidence/Fit quality
```

---

## 4. DATA ACCESS METHODS

### **Method 1: Direct Database Download** ✅ PREFERRED FOR BULK ANALYSIS
- **Source**: EPA Figshare
- **Database Package**: ToxCast Database (invitrodb v4.3)
- **Contents**: 
  - Full MySQL database
  - R packages (tcpl, tcplFit2, ctxR)
  - Release notes
  - Summary files
  - Assay information
  - Concentration-response plots
- **Link**: https://doi.org/10.23645/epacomptox.6062623
- **Format**: Compressed database package (downloadable)

### **Method 2: CompTox Chemicals Dashboard**
- **Access**: https://comptox.epa.gov/dashboard
- **Coverage**: 760,000+ chemicals
- **Features**:
  - Query ToxCast bioactivity by compound
  - View potency metrics across endpoints
  - Relative efficacy comparisons
  - Interactive visualization
  - SMILES-based search

### **Method 3: CTX Bioactivity API**
- **Endpoint**: https://comptox.epa.gov/ctx-api/docs/bioactivity.html
- **Access**: Programmatic REST API
- **Capabilities**:
  - Query bioactivity data
  - Batch chemical lookups
  - Filter by assay, endpoint, or compound
- **Use Cases**: Web applications, research tools, integration systems

### **Method 4: Tox21 Data Browser**
- **Platform**: https://tripod.nih.gov/tox21/
- **Features**:
  - Chemical structure access
  - Annotations and metadata
  - QC information
  - Tox21-specific screening results

### **Method 5: PubChem Integration**
- **Access**: https://www.ncbi.nlm.nih.gov/pcsubstance/?term=tox21
- **Data**: Large-scale Tox21 qHTS screening results
- **Format**: PubChem BioAssay records
- **Integration**: Cross-linked with medicinal chemistry data

---

## 5. ASSAY IDENTIFIER SYSTEM

### **AEID (Assay Endpoint ID)**
Standard 4-5 digit identifier system:
```
Examples:
- AEID2808: UTOR_hL-FABP_binding_Kd (liver fatty acid binding)
- AEID2386: UPITT_HCI_U2OS_AR_TIF2_Nucleoli_Antagonist (androgen antagonist)
- AEID2387: UPITT_HCI_U2OS_AR_TIF2_Nucleoli_Agonist (androgen agonist)
- AEID3210: TOX21_hERG_U2OS_Antagonist (cardiac potassium channel)
- AEID3334: TOX21_GNRHR_HEK293_Agonist (reproductive hormone)
- AEID3331: TOX21_p53_BLA_ms_human_ch2 (DNA damage response)
```

### **Naming Convention**:
`AEID[NUMBER]_[Source]_[CellType/Organism]_[Target]_[Direction]`

---

## 6. HIT RATE AND ACTIVITY DISTRIBUTIONS

### Expected Activity Profiles

**Typical Characteristics** (from ToxCast documentation):
- **Hit calls**: Binary classification (Active/Inactive)
- **Activity threshold**: Depends on assay type
  - Receptor binding: Typically 10-50 µM AC50
  - Functional assays: Variable by endpoint
  - Gene expression: Depends on fold-change

**Distribution Patterns**:
- **Nuclear receptor assays**: 15-40% hit rate typical (ligand-binding dependent)
- **Developmental assays**: 5-25% hit rate
- **Metabolic/Stress assays**: 10-30% hit rate
- **High-sensitivity binding**: Can reach 50-60% hits (less selective compounds)

### Hit Metric Data Available:
- **AC50 (Activity Concentration)**: Concentration causing 50% effect
- **Relative Efficacy**: Magnitude of maximum response
- **Window of Activity**: Quality metric for assay performance
- **Potency Categories**: Classifications by concentration ranges
- **Confidence Scores**: Based on curve-fitting quality

---

## 7. COMPOUND STRUCTURE INTEGRATION

### **Molecular Identifier Integration**

#### **Available Identifiers per Compound**:
1. **DTXSID** (EPA's unique identifier)
2. **CAS Registry Number**
3. **SMILES** (Simplified Molecular Input Line Entry Specification)
4. **InChI** (International Chemical Identifier)
5. **InChI Key** (Hashed InChI for faster lookup)
6. **Chemical Name** (Preferred IUPAC/Common names)

#### **Structure Files**:
- **SDF (Structure Data File)**: Contains full 2D/3D structures
- **Archive**: ToxCast chemicals SDF with 9,403 compound structures
- **Download**: Available in chemical information packages

#### **Integration Example**:
```
Compound Record:
├─ DTXSID10019885
├─ CAS: 50-00-0 (Formaldehyde)
├─ SMILES: C=O
├─ InChI: InChI=1S/CH2O/c1-2/h1H2
├─ Name: Formaldehyde
├─ Bioactivity Data:
│  ├─ AEID2386 (AR agonist): Inactive
│  ├─ AEID3210 (hERG antagonist): Inactive
│  ├─ AEID3331 (p53): Active (AC50 = 15 µM)
│  └─ [1,600+ additional assay results]
```

---

## 8. PHASE I AND PHASE II SCREENING OVERVIEW

### **Phase I - Exploratory Screening**
- **Scope**: Wide-range chemical screening
- **Assays**: Cell-based and biochemical assays
- **Chemicals**: Thousands of environmental and industrial chemicals
- **Goals**: Initial hazard identification, endpoint prioritization
- **Endpoints**: Receptor binding, cell viability, basic toxicity

### **Phase II - Focused Screening**
- **Scope**: Chemicals of interest from Phase I
- **Assays**: Expanded pathway-level assays
- **Goals**: Mechanistic pathway understanding
- **Endpoints**:
  - Reproductive/developmental pathways
  - Stress response pathways
  - Metabolic pathways
  - Organ-specific toxicity markers
  - Integrated pathway models

### **Integrated Approach**:
- **Estrogen Receptor Pathway Model**: Combines 18+ assays to predict ER activity
- **Androgen Receptor Pathway Model**: Combines multiple AR-related assays
- **Endocrine-Disrupting Chemical Screening**: Uses pathway integration

---

## 9. QUALITY ASSURANCE & DOCUMENTATION

### **Assay Documentation Standard**
- **Format**: OECD Guidance Document 211 (GD211)
- **Coverage**: 1,647 individual assay endpoint descriptions
- **Content**: 
  - Assay principle and rationale
  - Cell/organism systems used
  - Quality control metrics
  - Data interpretation guidelines
  - Relevance for toxicology assessment
  - Reproducibility information

### **Analytical QC Available**:
- Cytotoxicity burst analysis
- Data quality assessments
- Positive/negative control performance
- Plate uniformity metrics
- Concentration-response curve fit quality

---

## 10. PRACTICAL DATA INTEGRATION RECOMMENDATIONS

### **For Your PK-PD Modeling Project**:

1. **Data Download Strategy**:
   ```
   Primary: Download invitrodb v4.3 database package
   - Contains MySQL database with all data
   - Use R packages (tcpl) for programmatic access
   - Alternative: CompTox API for real-time queries
   ```

2. **Recommended Assays for PK-PD Integration**:
   - **Liver function**: Fatty acid binding, CYP450 interactions
   - **Cardiac safety**: hERG channel antagonism
   - **Developmental**: Reproductive/endocrine disruption markers
   - **Metabolic**: Mitochondrial function, stress response

3. **Compound Matching**:
   - Search by SMILES in CompTox Dashboard
   - Download chemical properties alongside bioactivity
   - Ensure CASRN/DTXSID mapping for consistency

4. **Data Format for Integration**:
   ```
   Expected CSV structure:
   Compound_ID | SMILES | AC50_hERG | hERG_Hit | AC50_ER | 
   ER_Agonist | AC50_p53 | p53_Active | ... [1600+ endpoints]
   ```

5. **Access Cost**: **FREE** - All ToxCast/Tox21 data is public domain

---

## 11. KEY REFERENCE RESOURCES

### **Official Links**:
- **ToxCast Overview**: https://www.epa.gov/comptox-tools/toxicity-forecasting-toxcast
- **Data Downloads**: https://www.epa.gov/comptox-tools/exploring-toxcast-data
- **CompTox Data Portal**: https://www.epa.gov/comptox-tools/downloadable-computational-toxicology-data
- **Tox21 Program**: https://tox21.gov
- **CompTox Dashboard**: https://comptox.epa.gov/dashboard

### **Technical Documentation**:
- **R Package Documentation**: https://cran.r-project.org/web/packages/tcpl/
- **Assay Descriptions**: https://clowder.edap-cluster.com/datasets/6894f2dae4b025654d12b716
- **APIs**: https://comptox.epa.gov/ctx-api/docs/
- **Tox21 Data Browser**: https://tripod.nih.gov/tox21/

### **Database Citation Format**:
```
U.S. EPA. 2025. ToxCast & Tox21 Data from invitrodb v4.3. 
Retrieved from https://www.epa.gov/chemical-research/toxicity-forecaster-toxcasttm-data
Data released August 2025.
```

---

## 12. SUMMARY TABLE

| Feature | Details |
|---------|---------|
| **Compounds** | ~9,403 unique substances (DTXSIDs) |
| **Assay Endpoints** | 1,647 endpoints (invitrodb v4.3) |
| **Safety Classes** | Endocrine, Cardiac, Liver, Kidney, Reproductive, Developmental, Metabolic, Ecotoxic |
| **Data Formats** | MySQL database, CSV summaries, SDF structures, API access |
| **Access Methods** | Direct download, CompTox Dashboard, REST API, PubChem, Tox21 browser |
| **Hit Rates** | 15-40% for receptor assays, 5-25% developmental, variable by endpoint |
| **Identifiers** | DTXSID, CAS, SMILES, InChI, AEID (assay IDs) |
| **Cost** | FREE - Public domain (EPA open data) |
| **Latest Version** | invitrodb v4.3 (Released August 2025) |
| **Standardization** | OECD GD211 documentation for all assays |

---

**Document Prepared:** February 4, 2026  
**Research Status:** Complete - Ready for Dataset Integration
