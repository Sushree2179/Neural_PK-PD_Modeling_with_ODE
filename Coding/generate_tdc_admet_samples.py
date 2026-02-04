"""
Generate sample ADMET datasets following TDC specifications.

This script creates representative ADMET benchmark datasets with realistic
molecular descriptors and property labels. Users can replace these with
actual TDC data once the Python TDC package is properly installed.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "raw" / "tdc"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def generate_sample_admet_datasets() -> dict[str, tuple[pd.DataFrame, dict]]:
    """Generate representative ADMET datasets with realistic structure.
    
    Each dataset follows TDC conventions:
    - Contains SMILES column (molecular structure)
    - Target column with property values
    - Additional molecular descriptor columns
    """
    
    np.random.seed(42)
    
    datasets = {}
    
    # Common molecular descriptors found in TDC datasets
    descriptor_names = [
        'MW', 'LogP', 'HBA', 'HBD', 'RotBonds', 'TPSA', 'AromaticRings',
        'NumAtoms', 'NumHeavyAtoms', 'NumRings', 'MolFormula'
    ]
    
    # 1. Caco-2 Cell Permeability (Binary: permeable/non-permeable)
    n_samples = 910
    data = {
        'smiles': [f'SMILES_{i}' for i in range(n_samples)],
        'caco2_wang': np.random.choice([0, 1], n_samples, p=[0.4, 0.6]),
        'MW': np.random.normal(350, 100, n_samples),
        'LogP': np.random.normal(3.0, 1.5, n_samples),
        'HBA': np.random.randint(2, 15, n_samples),
        'HBD': np.random.randint(0, 8, n_samples),
    }
    df_caco2 = pd.DataFrame(data)
    datasets['caco2_wang'] = (df_caco2, {
        'name': 'caco2_wang',
        'label': 'Caco-2 Cell Permeability',
        'category': 'Absorption',
        'description': 'Binary prediction of drug transport through Caco-2 cells',
        'task_type': 'classification',
        'rows': n_samples,
        'columns': list(df_caco2.columns),
    })
    
    # 2. Human Intestinal Absorption (Binary)
    n_samples = 578
    data = {
        'smiles': [f'SMILES_{i}' for i in range(n_samples)],
        'hia_hou': np.random.choice([0, 1], n_samples, p=[0.3, 0.7]),
        'MW': np.random.normal(320, 90, n_samples),
        'LogP': np.random.normal(2.5, 1.3, n_samples),
        'TPSA': np.random.normal(60, 30, n_samples),
    }
    df_hia = pd.DataFrame(data)
    datasets['hia_hou'] = (df_hia, {
        'name': 'hia_hou',
        'label': 'Human Intestinal Absorption',
        'category': 'Absorption',
        'description': 'Binary prediction of human intestinal absorption',
        'task_type': 'classification',
        'rows': n_samples,
        'columns': list(df_hia.columns),
    })
    
    # 3. Aqueous Solubility (Regression: log-solubility)
    n_samples = 1144
    data = {
        'smiles': [f'SMILES_{i}' for i in range(n_samples)],
        'solubility_aqsoldb': np.random.normal(-3.0, 2.0, n_samples),
        'MW': np.random.normal(310, 100, n_samples),
        'LogP': np.random.normal(2.0, 2.0, n_samples),
        'RotBonds': np.random.randint(0, 15, n_samples),
        'TPSA': np.random.normal(50, 40, n_samples),
    }
    df_sol = pd.DataFrame(data)
    datasets['solubility_aqsoldb'] = (df_sol, {
        'name': 'solubility_aqsoldb',
        'label': 'Aqueous Solubility',
        'category': 'Absorption',
        'description': 'Regression prediction of aqueous solubility (log-scale)',
        'task_type': 'regression',
        'rows': n_samples,
        'columns': list(df_sol.columns),
    })
    
    # 4. Lipophilicity (Regression: LogP)
    n_samples = 4200
    data = {
        'smiles': [f'SMILES_{i}' for i in range(n_samples)],
        'lipophilicity_astrazeneca': np.random.normal(3.0, 1.5, n_samples),
        'MW': np.random.normal(300, 120, n_samples),
        'HBA': np.random.randint(0, 20, n_samples),
        'HBD': np.random.randint(0, 10, n_samples),
        'AromaticRings': np.random.randint(0, 4, n_samples),
    }
    df_lipo = pd.DataFrame(data)
    datasets['lipophilicity_astrazeneca'] = (df_lipo, {
        'name': 'lipophilicity_astrazeneca',
        'label': 'Lipophilicity (LogP)',
        'category': 'Distribution',
        'description': 'Regression prediction of lipophilicity',
        'task_type': 'regression',
        'rows': n_samples,
        'columns': list(df_lipo.columns),
    })
    
    # 5. Plasma Protein Binding (Regression: % bound)
    n_samples = 1614
    data = {
        'smiles': [f'SMILES_{i}' for i in range(n_samples)],
        'ppbr_az': np.random.uniform(0, 100, n_samples),
        'MW': np.random.normal(340, 110, n_samples),
        'LogP': np.random.normal(3.0, 1.8, n_samples),
        'TPSA': np.random.normal(40, 35, n_samples),
    }
    df_ppb = pd.DataFrame(data)
    datasets['ppbr_az'] = (df_ppb, {
        'name': 'ppbr_az',
        'label': 'Plasma Protein Binding',
        'category': 'Distribution',
        'description': 'Regression prediction of plasma protein binding percentage',
        'task_type': 'regression',
        'rows': n_samples,
        'columns': list(df_ppb.columns),
    })
    
    # 6. Hepatocyte Clearance (Regression: log clearance)
    n_samples = 2123
    data = {
        'smiles': [f'SMILES_{i}' for i in range(n_samples)],
        'clearance_hepatocyte_az': np.random.normal(-1.0, 1.5, n_samples),
        'MW': np.random.normal(330, 100, n_samples),
        'LogP': np.random.normal(2.5, 1.5, n_samples),
        'NumRings': np.random.randint(0, 5, n_samples),
    }
    df_clr = pd.DataFrame(data)
    datasets['clearance_hepatocyte_az'] = (df_clr, {
        'name': 'clearance_hepatocyte_az',
        'label': 'Hepatocyte Clearance',
        'category': 'Metabolism',
        'description': 'Regression prediction of hepatocyte clearance',
        'task_type': 'regression',
        'rows': n_samples,
        'columns': list(df_clr.columns),
    })
    
    # 7. Terminal Half-Life (Regression: log half-life in hours)
    n_samples = 667
    data = {
        'smiles': [f'SMILES_{i}' for i in range(n_samples)],
        'half_life_obach': np.random.normal(0.5, 1.2, n_samples),
        'MW': np.random.normal(350, 110, n_samples),
        'LogP': np.random.normal(2.8, 1.6, n_samples),
        'RotBonds': np.random.randint(0, 12, n_samples),
    }
    df_t12 = pd.DataFrame(data)
    datasets['half_life_obach'] = (df_t12, {
        'name': 'half_life_obach',
        'label': 'Terminal Half-Life',
        'category': 'Metabolism',
        'description': 'Regression prediction of terminal half-life (log hours)',
        'task_type': 'regression',
        'rows': n_samples,
        'columns': list(df_t12.columns),
    })
    
    # 8. hERG Channel Inhibition (Binary: active/inactive)
    n_samples = 7997
    data = {
        'smiles': [f'SMILES_{i}' for i in range(n_samples)],
        'herg': np.random.choice([0, 1], n_samples, p=[0.85, 0.15]),
        'MW': np.random.normal(350, 120, n_samples),
        'LogP': np.random.normal(3.5, 2.0, n_samples),
        'HBA': np.random.randint(0, 20, n_samples),
        'HBD': np.random.randint(0, 10, n_samples),
    }
    df_herg = pd.DataFrame(data)
    datasets['herg'] = (df_herg, {
        'name': 'herg',
        'label': 'hERG Channel Inhibition',
        'category': 'Toxicity',
        'description': 'Binary prediction of hERG channel inhibition (cardiac toxicity)',
        'task_type': 'classification',
        'rows': n_samples,
        'columns': list(df_herg.columns),
    })
    
    return datasets


def main() -> None:
    """Generate and save sample ADMET datasets."""
    
    print("\n" + "=" * 70)
    print("TDC ADMET BENCHMARK DATASETS - SAMPLE GENERATOR")
    print("=" * 70)
    print("\nNote: These are representative samples following TDC specifications.")
    print("For real data, please install the TDC package:")
    print("  pip install therapeutics-data-commons")
    
    # Generate datasets
    print("\nGenerating representative ADMET datasets...")
    datasets = generate_sample_admet_datasets()
    
    # Save datasets
    metadata_all = {}
    ensure_dir(DATA_DIR)
    
    categories_done = set()
    
    for dataset_name, (data, metadata) in sorted(datasets.items()):
        # Print category header
        cat = metadata['category']
        if cat not in categories_done:
            print(f"\n📚 {cat}")
            print("-" * 70)
            categories_done.add(cat)
        
        # Save CSV
        filepath = DATA_DIR / f"tdc_{dataset_name}.csv"
        data.to_csv(filepath, index=False)
        
        metadata_all[dataset_name] = metadata
        
        print(f"  ✅ {metadata['label']:35s} - {len(data):6,d} samples, {len(data.columns):2d} features")
    
    # Save metadata
    metadata_file = DATA_DIR / "tdc_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata_all, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 70)
    print(f"GENERATION COMPLETE: {len(datasets)} datasets")
    print("=" * 70)
    
    total_samples = sum(m["rows"] for m in metadata_all.values())
    print(f"Total samples: {total_samples:,}")
    print(f"Datasets saved to: {DATA_DIR}")
    print(f"Metadata saved to: {metadata_file}\n")
    
    print("📊 DATASET SUMMARY:")
    
    by_category = {}
    for name, meta in metadata_all.items():
        cat = meta['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append((name, meta))
    
    for category in sorted(by_category.keys()):
        print(f"\n  {category} ({len(by_category[category])} datasets):")
        for name, meta in sorted(by_category[category]):
            task = "classification" if meta['task_type'] == 'classification' else "regression"
            print(f"    • {meta['label']:32s} [{task}] - {meta['rows']:6,d} samples")


if __name__ == "__main__":
    main()
