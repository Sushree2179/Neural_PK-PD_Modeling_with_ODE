"""Download ADMET benchmark datasets from Therapeutics Data Commons (TDC).

Alternative approach: Fetch datasets via TDC web API and GitHub.
Reference: https://github.com/mims-harvard/TDC
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional
import io

import pandas as pd
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "raw" / "tdc"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def download_csv_from_url(url: str, dataset_name: str) -> Optional[pd.DataFrame]:
    """Download CSV file from URL using requests library.
    
    Args:
        url: Direct URL to CSV or compressed file
        dataset_name: Name for logging
        
    Returns:
        DataFrame or None if failed
    """
    try:
        print(f"  ⏳ Downloading {dataset_name}...", end="", flush=True)
        
        # Use requests with SSL verification disabled
        response = requests.get(url, timeout=30, verify=False)
        response.raise_for_status()
        
        # Parse CSV from response
        data = pd.read_csv(io.StringIO(response.text))
        
        print(f" ✅ ({len(data)} samples)")
        return data
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None


def download_tdc_datasets_via_api() -> dict[str, tuple[pd.DataFrame, dict]]:
    """Download ADMET datasets using direct URLs.
    
    Note: These URLs are based on TDC data repository.
    """
    
    # Datasets with their URLs (from various sources)
    datasets = {
        "caco2_wang": {
            "label": "Caco-2 Cell Permeability",
            "category": "Absorption",
            "url": "https://raw.githubusercontent.com/mims-harvard/TDC/master/data/admet_group/caco2_wang.csv",
            "description": "Prediction of drug transport through caco-2 cells"
        },
        "hia_hou": {
            "label": "Human Intestinal Absorption",
            "category": "Absorption",
            "url": "https://raw.githubusercontent.com/mims-harvard/TDC/master/data/admet_group/hia_hou.csv",
            "description": "Binary prediction of human intestinal absorption"
        },
        "solubility_aqsoldb": {
            "label": "Aqueous Solubility",
            "category": "Absorption",
            "url": "https://raw.githubusercontent.com/mims-harvard/TDC/master/data/admet_group/solubility_aqsoldb.csv",
            "description": "Regression prediction of aqueous solubility"
        },
        "lipophilicity_astrazeneca": {
            "label": "Lipophilicity (LogP)",
            "category": "Distribution",
            "url": "https://raw.githubusercontent.com/mims-harvard/TDC/master/data/admet_group/lipophilicity_astrazeneca.csv",
            "description": "Prediction of lipophilicity"
        },
        "ppbr_az": {
            "label": "Plasma Protein Binding",
            "category": "Distribution",
            "url": "https://raw.githubusercontent.com/mims-harvard/TDC/master/data/admet_group/ppbr_az.csv",
            "description": "Prediction of plasma protein binding"
        },
        "clearance_hepatocyte_az": {
            "label": "Hepatocyte Clearance",
            "category": "Metabolism",
            "url": "https://raw.githubusercontent.com/mims-harvard/TDC/master/data/admet_group/clearance_hepatocyte_az.csv",
            "description": "Prediction of hepatocyte clearance"
        },
        "half_life_obach": {
            "label": "Terminal Half-Life",
            "category": "Metabolism",
            "url": "https://raw.githubusercontent.com/mims-harvard/TDC/master/data/admet_group/half_life_obach.csv",
            "description": "Prediction of terminal half-life"
        },
        "herg": {
            "label": "hERG Channel Inhibition",
            "category": "Toxicity",
            "url": "https://raw.githubusercontent.com/mims-harvard/TDC/master/data/admet_group/herg.csv",
            "description": "Prediction of hERG channel inhibition (cardiac toxicity)"
        },
    }
    
    results = {}
    
    # Group by category
    categories = {}
    for name, info in datasets.items():
        cat = info["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((name, info))
    
    # Download by category
    for category, items in sorted(categories.items()):
        print(f"\n📚 {category}")
        print("-" * 70)
        
        for dataset_name, info in items:
            data = download_csv_from_url(info["url"], info["label"])
            
            if data is not None:
                metadata = {
                    "name": dataset_name,
                    "label": info["label"],
                    "category": info["category"],
                    "description": info["description"],
                    "rows": len(data),
                    "columns": list(data.columns),
                    "dtypes": {col: str(dtype) for col, dtype in data.dtypes.items()},
                }
                
                results[dataset_name] = (data, metadata)
                print(f"     Saved metadata for {dataset_name}")
    
    return results


def save_dataset(data: pd.DataFrame, name: str, metadata: dict) -> Path:
    """Save dataset to CSV file."""
    ensure_dir(DATA_DIR)
    
    filename = f"tdc_{name}.csv"
    filepath = DATA_DIR / filename
    
    data.to_csv(filepath, index=False)
    return filepath


def main() -> None:
    """Download all ADMET datasets."""
    
    print("\n" + "=" * 70)
    print("TDC ADMET BENCHMARK DATASETS DOWNLOADER")
    print("=" * 70)
    print("\nFetching from TDC GitHub repository...")
    
    # Download datasets
    datasets = download_tdc_datasets_via_api()
    
    # Save datasets
    metadata_all = {}
    
    ensure_dir(DATA_DIR)
    
    for dataset_name, (data, metadata) in datasets.items():
        filepath = save_dataset(data, dataset_name, metadata)
        metadata_all[dataset_name] = metadata
        print(f"✅ Saved: {filepath.name}")
    
    # Save metadata summary
    if metadata_all:
        metadata_file = DATA_DIR / "tdc_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata_all, f, indent=2)
        print(f"\n✅ Metadata saved to: {metadata_file}")
    
    # Print summary
    print("\n" + "=" * 70)
    print(f"DOWNLOAD SUMMARY: {len(datasets)} datasets")
    print("=" * 70)
    
    if metadata_all:
        total_samples = sum(m["rows"] for m in metadata_all.values())
        print(f"Total samples: {total_samples:,}")
        print(f"Datasets saved to: {DATA_DIR}\n")
        
        print("📊 DATASETS DOWNLOADED:")
        
        # Group by category
        by_category = {}
        for name, meta in metadata_all.items():
            cat = meta["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append((name, meta))
        
        for category in sorted(by_category.keys()):
            print(f"\n  {category}:")
            for name, meta in sorted(by_category[category]):
                print(f"    • {meta['label']:35s} - {meta['rows']:6,d} samples, {len(meta['columns']):2d} features")
    else:
        print("⚠️  No datasets downloaded.")
    
    print()


if __name__ == "__main__":
    main()
