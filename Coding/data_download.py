"""Lightweight dataset fetcher for Neural PK-PD modeling.

This script pulls small, representative slices so you can start prototyping
without bulk downloads. Expand or swap endpoints as needed when you are ready
for full-scale ingestion.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import requests

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "raw"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def download_file(url: str, dest: Path, *, overwrite: bool = False) -> Optional[Path]:
    if dest.exists() and not overwrite:
        print(f"[skip] {dest} exists")
        return dest
    try:
        with requests.get(url, stream=True, timeout=60) as r:
            r.raise_for_status()
            ensure_dir(dest.parent)
            with open(dest, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        print(f"[ok] downloaded {dest}")
        return dest
    except Exception as e:  # noqa: BLE001
        print(f"[fail] {url} -> {dest}: {e}")
        return None


def fetch_pubchem_assay(aid: int, label: str) -> None:
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/{aid}/CSV"
    dest = DATA_DIR / "pubchem" / f"assay_{label}_aid{aid}.csv"
    download_file(url, dest)


def fetch_pubchem_compound(name: str) -> None:
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/SDF?record_type=3d"
    dest = DATA_DIR / "pubchem" / f"compound_{name.lower()}.sdf"
    download_file(url, dest)


def fetch_pkdb_studies(limit: int = 50) -> None:
    """Fetch a slice of PK-DB studies (metadata only) for quick inspection."""

    ensure_dir(DATA_DIR / "pkdb")
    url = "https://pk-db.com/api/v1/studies/?format=json"
    dest = DATA_DIR / "pkdb" / "studies.json"
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        dest.write_bytes(r.content)
        print(f"[ok] downloaded {dest}")
        
        data = r.json()
        # Extract data from nested structure: data.data.data is the array
        studies_list = []
        if "data" in data:
            inner = data["data"]
            if isinstance(inner, dict) and "data" in inner:
                studies_list = inner["data"]
            elif isinstance(inner, list):
                studies_list = inner
        
        # Create trimmed version
        trimmed_studies = studies_list[:limit] if studies_list else []
        trimmed = {"data": trimmed_studies}
        dest_trim = DATA_DIR / "pkdb" / f"studies_top{limit}.json"
        dest_trim.write_text(json.dumps(trimmed, indent=2))
        print(f"[ok] wrote trimmed list ({len(trimmed_studies)} studies) to {dest_trim}")
    except Exception as e:  # noqa: BLE001
        print(f"[fail] {url} -> {dest}: {e}")


def fetch_pkdb_outputs_by_ids(output_ids: list[int], page_size: int = 50) -> None:
    """Fetch specific PK parameter outputs by their IDs.
    
    Outputs include:
    - CL (Clearance)
    - Vd (Volume of Distribution)
    - t½ (Half-life)
    - AUC (Area Under Curve)
    - Cmax, Tmax, etc.
    """
    ensure_dir(DATA_DIR / "pkdb")
    
    # Fetch in batches
    for i, oid in enumerate(output_ids[:50]):  # Limit to first 50 for initial download
        url = f"https://pk-db.com/api/v1/outputs/{oid}/?format=json"
        dest = DATA_DIR / "pkdb" / f"output_{oid}.json"
        
        if dest.exists():
            print(f"[skip] {dest} exists")
            continue
        
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            dest.write_bytes(r.content)
            if i % 10 == 0:
                print(f"[ok] downloaded output {i+1}/{min(50, len(output_ids))}")
        except Exception as e:  # noqa: BLE001
            print(f"[fail] output {oid}: {e}")


def fetch_pkdb_timecourses_by_ids(subset_ids: list[int]) -> None:
    """Fetch timecourses linked to dataset subsets.
    
    Each subset contains timecourse_count indicating time-concentration curves.
    """
    ensure_dir(DATA_DIR / "pkdb")
    
    for i, subset_id in enumerate(subset_ids[:20]):  # Limit to first 20 subsets
        url = f"https://pk-db.com/api/v1/subsets/{subset_id}/?format=json"
        dest = DATA_DIR / "pkdb" / f"subset_{subset_id}.json"
        
        if dest.exists():
            print(f"[skip] {dest} exists")
            continue
        
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            dest.write_bytes(r.content)
            if i % 5 == 0:
                print(f"[ok] downloaded subset {i+1}/{min(20, len(subset_ids))}")
        except Exception as e:  # noqa: BLE001
            print(f"[fail] subset {subset_id}: {e}")


def fetch_pkdb_timecourses(page_size: int = 100) -> None:
    """Fetch paginated timecourse data from PK-DB API.
    
    The /pkdata/timecourses/ endpoint returns time-concentration curves
    with measurements for individual subjects or groups.
    """
    ensure_dir(DATA_DIR / "pkdb")
    url = f"https://pk-db.com/api/v1/pkdata/timecourses/?page_size={page_size}&format=json"
    dest = DATA_DIR / "pkdb" / f"timecourses_page1.json"
    
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        dest.write_bytes(r.content)
        print(f"[ok] downloaded timecourses (page 1) to {dest}")
        
        # Get metadata to show what we have
        data = r.json()
        if "count" in data:
            print(f"[info] Total timecourses available: {data['count']}")
        if "results" in data:
            print(f"[info] Retrieved {len(data['results'])} records in page 1")
    except Exception as e:  # noqa: BLE001
        print(f"[fail] {url} -> {dest}: {e}")


def fetch_pkdb_outputs(page_size: int = 100) -> None:
    """Fetch pharmacokinetic parameter outputs from PK-DB API.
    
    Outputs include derived PK parameters like:
    - CL (Clearance)
    - Vd (Volume of Distribution)
    - t½ (Half-life)
    - AUC (Area Under Curve)
    - Cmax, Tmax, etc.
    """
    ensure_dir(DATA_DIR / "pkdb")
    url = f"https://pk-db.com/api/v1/pkdata/outputs/?page_size={page_size}&format=json"
    dest = DATA_DIR / "pkdb" / f"outputs_page1.json"
    
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        dest.write_bytes(r.content)
        print(f"[ok] downloaded outputs (page 1) to {dest}")
        
        # Get metadata
        data = r.json()
        if "count" in data:
            print(f"[info] Total outputs available: {data['count']}")
        if "results" in data:
            print(f"[info] Retrieved {len(data['results'])} records in page 1")
    except Exception as e:  # noqa: BLE001
        print(f"[fail] {url} -> {dest}: {e}")


def fetch_pkdb_paginated(endpoint: str, num_pages: int = 5, page_size: int = 100) -> None:
    """Generic function to fetch multiple pages from any PK-DB API endpoint.
    
    Args:
        endpoint: API endpoint name (e.g., 'timecourses', 'outputs', 'individuals')
        num_pages: Number of pages to fetch
        page_size: Records per page
    """
    ensure_dir(DATA_DIR / "pkdb")
    
    for page_num in range(1, num_pages + 1):
        url = f"https://pk-db.com/api/v1/pkdata/{endpoint}/?page={page_num}&page_size={page_size}&format=json"
        dest = DATA_DIR / "pkdb" / f"{endpoint}_page{page_num}.json"
        
        if dest.exists():
            print(f"[skip] {dest} exists")
            continue
        
        try:
            r = requests.get(url, timeout=60)
            r.raise_for_status()
            dest.write_bytes(r.content)
            print(f"[ok] downloaded {endpoint} page {page_num} to {dest}")
            
            data = r.json()
            if "count" in data:
                total = data["count"]
                print(f"[info] Total {endpoint}: {total}, page {page_num}/{(total + page_size - 1) // page_size}")
        except Exception as e:  # noqa: BLE001
            print(f"[fail] {url} -> {dest}: {e}")
            if "404" in str(e):
                print(f"[info] Endpoint /pkdata/{endpoint}/ may not exist or be accessible")


def main() -> None:
    ensure_dir(DATA_DIR)

    # PubChem: small assay slices (hERG and CYP3A4) and a few exemplar compounds.
    fetch_pubchem_assay(588834, label="herg_qhts")
    fetch_pubchem_assay(54772, label="cyp3a4_inhibition")
    for compound in ["warfarin", "midazolam", "caffeine"]:
        fetch_pubchem_compound(compound)

    # PK-DB: studies metadata and extract IDs for time-course/output data
    print("\n=== PK-DB DATA DOWNLOAD ===\n")
    
    print("--- Fetching PK-DB Studies Metadata ---")
    fetch_pkdb_studies(limit=100)
    
    # Extract output and subset IDs from studies
    print("\n--- Extracting Data IDs from Studies ---")
    studies_file = DATA_DIR / "pkdb" / "studies.json"
    if studies_file.exists():
        try:
            studies_data = json.loads(studies_file.read_text())
            # Handle nested data structure
            if "data" in studies_data and isinstance(studies_data["data"], dict):
                studies = studies_data["data"].get("data", [])[:100]
            elif "data" in studies_data and isinstance(studies_data["data"], list):
                studies = studies_data["data"][:100]
            else:
                studies = []
            
            # Collect all output IDs and subset IDs
            output_ids = []
            subset_ids = []
            
            for study in studies:
                output_ids.extend(study.get("outputset", {}).get("outputs", []))
                subset_ids.extend(study.get("dataset", {}).get("subsets", []))
            
            output_ids = list(set(output_ids))[:100]  # Unique IDs, limit to 100
            subset_ids = list(set(subset_ids))[:20]   # Unique IDs, limit to 20
            
            print(f"[info] Found {len(studies)} studies")
            print(f"[info] Found {len(output_ids)} unique output IDs (CL, Vd, t½, AUC, etc.)")
            print(f"[info] Found {len(subset_ids)} unique subset IDs (timecourse containers)")
            
            # Fetch individual outputs
            if output_ids:
                print(f"\n--- Fetching {min(50, len(output_ids))} PK Parameters ---")
                fetch_pkdb_outputs_by_ids(output_ids, page_size=50)
            
            # Fetch subset data (which contains timecourses)
            if subset_ids:
                print(f"\n--- Fetching {min(20, len(subset_ids))} Timecourse Subsets ---")
                fetch_pkdb_timecourses_by_ids(subset_ids)
        except Exception as e:
            print(f"[warn] Could not extract IDs from studies: {e}")
    
    print("\n✓ Data download complete!")
    print(f"✓ All files saved to: {DATA_DIR}")


if __name__ == "__main__":
    main()
