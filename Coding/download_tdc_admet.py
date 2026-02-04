"""Download ADMET benchmark datasets from Therapeutics Data Commons (TDC).

This script fetches open-access ADMET datasets from TDC including:
- Absorption: caco2, hia, solubility
- Distribution: lipophilicity, ppbr
- Metabolism: clearance, half_life
- Toxicity: herg

Datasets are saved as CSV files with molecular descriptors + labels.

Reference: https://tdcommons.ai/benchmark/admet_group/overview/
License: Open Access for academic use
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "raw" / "tdc"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def download_tdc_dataset(dataset_name: str, label: str = "") -> Optional[tuple[pd.DataFrame, dict]]:
    """Download a single TDC dataset.
    
    Args:
        dataset_name: Name of TDC dataset (e.g., 'caco2_wang', 'hia_hou')
        label: Custom label for output file
        
    Returns:
        Tuple of (DataFrame, metadata) or None if failed
    """
    try:
        from tdc.benchmark_group import admet_group
        
        # Initialize dataset
        print(f"  ⏳ Downloading {dataset_name}...", end="", flush=True)
        group = admet_group(name=dataset_name)
        
        # Get train and test data
        train_val, test = group.get_train_valid_test(seed=42)
        
        # Combine train+val for full dataset
        data = pd.concat([train_val, test], ignore_index=True)
        
        # Get metadata
        metadata = {
            "name": dataset_name,
            "label": label,
            "rows": len(data),
            "columns": list(data.columns),
            "train_size": len(train_val),
            "test_size": len(test),
        }
        
        print(f" ✅ ({len(data)} samples)")
        return data, metadata
        
    except ImportError:
        print(f"  ❌ TDC not installed. Run: pip install PyDantic tdc")
        return None
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None


def save_tdc_dataset(data: pd.DataFrame, name: str, label: str) -> Path:
    """Save TDC dataset to CSV file.
    
    Args:
        data: Dataset DataFrame
        name: Dataset name (for filename)
        label: Human-readable label
        
    Returns:
        Path to saved file
    """
    ensure_dir(DATA_DIR)
    
    filename = f"tdc_{name}.csv"
    filepath = DATA_DIR / filename
    
    data.to_csv(filepath, index=False)
    return filepath


def main() -> None:
    """Download all ADMET datasets from TDC."""
    
    print("\n" + "=" * 70)
    print("TDC ADMET BENCHMARK DATASETS DOWNLOADER")
    print("=" * 70)
    
    # Define ADMET tasks to download
    # Format: (dataset_name, label, category)
    admet_tasks = [
        # ABSORPTION
        ("caco2_wang", "Caco-2 Cell Permeability", "Absorption"),
        ("hia_hou", "Human Intestinal Absorption", "Absorption"),
        ("solubility_aqsoldb", "Aqueous Solubility", "Absorption"),
        
        # DISTRIBUTION
        ("lipophilicity_astrazeneca", "Lipophilicity (LogP)", "Distribution"),
        ("ppbr_az", "Plasma Protein Binding", "Distribution"),
        
        # METABOLISM
        ("clearance_hepatocyte_az", "Hepatocyte Clearance", "Metabolism"),
        ("half_life_obach", "Terminal Half-Life", "Metabolism"),
        
        # TOXICITY
        ("herg", "hERG Channel Inhibition (Cardiac Toxicity)", "Toxicity"),
    ]
    
    # Download datasets by category
    metadata_all = {}
    success_count = 0
    
    categories_done = set()
    
    for dataset_name, label, category in admet_tasks:
        # Print category header
        if category not in categories_done:
            print(f"\n📚 {category}")
            print("-" * 70)
            categories_done.add(category)
        
        # Download dataset
        result = download_tdc_dataset(dataset_name, label)
        
        if result is not None:
            data, metadata = result
            
            # Save to CSV
            filepath = save_tdc_dataset(data, dataset_name, label)
            print(f"     Saved to: {filepath.name}")
            
            metadata_all[dataset_name] = metadata
            success_count += 1
        else:
            print(f"  ⚠️  Skipped {dataset_name}")
    
    # Save metadata summary
    if metadata_all:
        ensure_dir(DATA_DIR)
        metadata_file = DATA_DIR / "tdc_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata_all, f, indent=2)
        print(f"\n✅ Metadata saved to: {metadata_file}")
    
    # Print summary
    print("\n" + "=" * 70)
    print(f"DOWNLOAD SUMMARY: {success_count}/{len(admet_tasks)} datasets")
    print("=" * 70)
    
    if metadata_all:
        total_samples = sum(m["rows"] for m in metadata_all.values())
        print(f"Total samples: {total_samples}")
        print(f"Datasets saved to: {DATA_DIR}")
        
        print("\n📊 DATASETS:")
        for dataset_name, metadata in metadata_all.items():
            print(f"  • {metadata['label']:35s} - {metadata['rows']:6d} samples")
    else:
        print("⚠️  No datasets downloaded. Please install TDC: pip install PyDantic tdc")
    
    print()


if __name__ == "__main__":
    main()
