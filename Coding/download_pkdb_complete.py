"""Download complete PK-DB studies dataset with all embedded timecourses and outputs."""
import requests
import json
from pathlib import Path

DATA_DIR = Path("data/raw/pkdb")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Download full studies data
url = "https://pk-db.com/api/v1/studies/?format=json"
print("Downloading complete PK-DB studies dataset...")

try:
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    
    data = r.json()
    
    # Get the actual studies list
    if "data" in data and isinstance(data["data"], dict):
        inner_data = data["data"]
        studies = inner_data.get("data", [])
    else:
        studies = data.get("results", [])
    
    print(f"✓ Downloaded {len(studies)} studies")
    
    # Save comprehensive metadata
    output_file = DATA_DIR / "pkdb_studies_complete.json"
    with open(output_file, 'w') as f:
        json.dump({"studies": studies}, f, indent=2)
    
    print(f"✓ Saved to {output_file}")
    
    # Collect statistics
    total_outputs = sum(len(s.get("outputset", {}).get("outputs", [])) for s in studies)
    total_subsets = sum(len(s.get("dataset", {}).get("subsets", [])) for s in studies)
    total_timecourses = sum(s.get("timecourse_count", 0) for s in studies)
    
    print(f"\n=== DOWNLOAD SUMMARY ===")
    print(f"Total studies: {len(studies)}")
    print(f"Total outputs (PK parameters): {total_outputs}")
    print(f"Total subsets: {total_subsets}")
    print(f"Total timecourses: {total_timecourses}")
    
    # Sample drugs
    drugs = set()
    for s in studies[:100]:
        for sub in s.get("substances", []):
            drugs.add(sub.get("name", "unknown"))
    print(f"\nSample drugs in dataset ({len(drugs)} unique):")
    for drug in sorted(drugs)[:20]:
        print(f"  - {drug}")
    
    # Sample study
    if studies:
        sample = studies[0]
        print(f"\nSample study: {sample.get('name', 'N/A')}")
        print(f"  Drug: {sample.get('drug_name', 'N/A') if 'drug_name' in sample else 'N/A'}")
        print(f"  Subjects: {sample.get('individual_count', 0)}")
        print(f"  Outputs: {len(sample.get('outputset', {}).get('outputs', []))}")
        print(f"  Timecourses: {sample.get('timecourse_count', 0)}")
    
except Exception as e:
    print(f"✗ Error: {e}")
