"""
Quick start guide for working with downloaded PK-DB time-course data.

Run this script to explore the data structure.
"""
import json
from pathlib import Path
from collections import Counter

# Load the PK-DB studies
DATA_FILE = Path("data/raw/pkdb/pkdb_studies_complete.json")

def explore_pkdb_data():
    """Explore the structure and content of downloaded PK-DB data."""
    
    print("=" * 70)
    print("PK-DB PHARMACOKINETIC TIME-COURSES & PARAMETERS")
    print("=" * 70)
    
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    studies = data['studies']
    
    # === OVERVIEW ===
    print(f"\n📊 DATASET OVERVIEW")
    print(f"-" * 70)
    print(f"Total studies: {len(studies)}")
    print(f"Total subjects: {sum(s.get('individual_count', 0) for s in studies)}")
    
    total_outputs = sum(len(s['outputset']['outputs']) for s in studies)
    total_timecourses = sum(s.get('timecourse_count', 0) for s in studies)
    total_subsets = sum(len(s['dataset']['subsets']) for s in studies)
    
    print(f"Total PK outputs (parameters): {total_outputs}")
    print(f"Total timecourses: {total_timecourses}")
    print(f"Total dataset subsets: {total_subsets}")
    
    # === DRUGS ===
    print(f"\n💊 DRUGS & SUBSTANCES")
    print(f"-" * 70)
    all_drugs = Counter()
    for study in studies:
        for substance in study.get('substances', []):
            all_drugs[substance['name']] += 1
    
    print(f"Unique substances: {len(all_drugs)}")
    for drug, count in all_drugs.most_common(15):
        print(f"  • {drug:30s} ({count} studies)")
    
    # === STUDIES ===
    print(f"\n📚 STUDIES")
    print(f"-" * 70)
    for i, study in enumerate(studies[:5], 1):
        print(f"\n{i}. {study['name']} (PMID: {study['reference']['pmid']})")
        print(f"   Title: {study['reference']['title'][:60]}...")
        print(f"   Subjects: {study['individual_count']}")
        print(f"   PK outputs: {len(study['outputset']['outputs'])}")
        print(f"   Timecourses: {study['timecourse_count']}")
        drugs = [s['name'] for s in study['substances']]
        print(f"   Drugs: {', '.join(drugs[:3])}")
    
    # === PARAMETERS ===
    print(f"\n📈 AVAILABLE PK PARAMETERS")
    print(f"-" * 70)
    print("""
    The outputs include pharmacokinetic parameters such as:
    
    • CLEARANCE PARAMETERS
      - CL: Systemic clearance
      - CLrenal: Renal clearance
      - CLhepatic: Hepatic clearance
      - CL/F: Apparent clearance
    
    • VOLUME PARAMETERS
      - Vd: Volume of distribution
      - Vdss: Volume of distribution at steady state
      - Vcentral: Central compartment volume
    
    • HALF-LIFE & ELIMINATION
      - t½: Terminal half-life
      - λz: Elimination rate constant
      - MRT: Mean residence time
    
    • EXPOSURE PARAMETERS
      - AUC: Area under the concentration curve
      - AUC₀₋∞: AUC to infinity
      - AUC₀₋₂₄: AUC over 24 hours
      - Cmax: Maximum concentration
      - Tmax: Time to maximum concentration
    
    • ABSORPTION PARAMETERS
      - ka: Absorption rate constant
      - F: Bioavailability
      - Lag: Absorption lag time
    
    • PROTEIN BINDING
      - fu: Fraction unbound
      - PPB: Plasma protein binding
    """)
    
    # === TIMECOURSE DATA ===
    print(f"\n⏱️  TIMECOURSE DATA STRUCTURE")
    print(f"-" * 70)
    study_with_timecourses = max(studies, key=lambda s: s['timecourse_count'])
    print(f"Study with most timecourses: {study_with_timecourses['name']}")
    print(f"Number of timecourses: {study_with_timecourses['timecourse_count']}")
    print(f"Dataset subsets (containers): {len(study_with_timecourses['dataset']['subsets'])}")
    print(f"\nTimecourse data includes:")
    print(f"  • Time points of measurement")
    print(f"  • Measured concentrations")
    print(f"  • Individual or group averages")
    print(f"  • Associated metadata (sampling location, units, etc.)")
    
    # === USAGE EXAMPLES ===
    print(f"\n🔧 USAGE EXAMPLES")
    print(f"-" * 70)
    
    print("\n1. Filter studies for a specific drug:")
    print("""
    midazolam_studies = [
        s for s in studies 
        if any(sub['name'] == 'midazolam' for sub in s['substances'])
    ]
    """)
    
    print("\n2. Extract all PK parameters from a study:")
    print("""
    study = studies[0]
    output_ids = study['outputset']['outputs']
    print(f"Study {study['name']} has {len(output_ids)} PK parameters")
    """)
    
    print("\n3. Convert to pandas DataFrame:")
    print("""
    import pandas as pd
    
    # Flatten studies data
    rows = []
    for study in studies:
        for substance in study['substances']:
            rows.append({
                'study_id': study['sid'],
                'study_name': study['name'],
                'drug_name': substance['name'],
                'pmid': study['reference']['pmid'],
                'subjects': study['individual_count'],
                'num_outputs': len(study['outputset']['outputs']),
                'num_timecourses': study['timecourse_count']
            })
    
    df = pd.DataFrame(rows)
    """)
    
    print("\n4. Group by drug:")
    print("""
    drug_studies = {}
    for study in studies:
        for substance in study['substances']:
            drug = substance['name']
            if drug not in drug_studies:
                drug_studies[drug] = []
            drug_studies[drug].append(study['name'])
    
    for drug, study_list in drug_studies.items():
        print(f"{drug}: {len(study_list)} studies")
    """)
    
    # === FILES ===
    print(f"\n📁 RELATED FILES")
    print(f"-" * 70)
    print(f"Main data: {DATA_FILE}")
    print(f"Documentation: data_download.py, DATA_README.md")
    print(f"PubChem data: data/raw/pubchem/*.csv, *.sdf")
    
    print("\n" + "=" * 70)
    print("✅ Ready for analysis!")
    print("=" * 70)

if __name__ == "__main__":
    explore_pkdb_data()
