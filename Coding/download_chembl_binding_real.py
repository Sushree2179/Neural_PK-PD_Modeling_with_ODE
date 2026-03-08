"""
download_chembl_binding_real.py
--------------------------------
Download real binding-affinity data (pChEMBL values + canonical SMILES)
from the ChEMBL REST activity endpoint for a curated set of pharmacologically
important protein targets.

Strategy
--------
- For each target, fetch all IC50/Ki activities that have both pchembl_value
  and canonical_smiles  (these are embedded in the activity record).
- Deduplicate by SMILES (keep mean pchembl_value across assays/replicates).
- Cap at MAX_PER_TARGET compounds per target to keep diversity balanced.
- Concatenate, global deduplicate, save.

Output
------
  data/raw/chembl/chembl_binding_affinity_with_smiles.csv
  Columns: smiles, pchembl_value, target_chembl_id, target_name, MW, LogP

The old synthetic-placeholder chembl_binding_affinity.csv is left untouched.
"""

from __future__ import annotations
import time
from pathlib import Path
import numpy as np
import pandas as pd
import requests

try:
    from rdkit import Chem
    from rdkit.Chem import Descriptors, rdMolDescriptors
    HAS_RDKIT = True
except ImportError:
    HAS_RDKIT = False
    print("⚠  RDKit not available — MW/LogP will be NaN")

ROOT     = Path(__file__).resolve().parent
OUT_CSV  = ROOT / "data" / "raw" / "chembl" / "chembl_binding_affinity_with_smiles.csv"
API      = "https://www.ebi.ac.uk/chembl/api/data/activity"
HEADERS  = {"Accept": "application/json"}
LIMIT    = 1000          # records per API page (ChEMBL max)
DELAY    = 0.35          # seconds between requests
MAX_PER_TARGET = 600     # cap per target for diversity balance

# Each entry: (chembl_target_id, human-readable name)
TARGETS = [
    ("CHEMBL217",  "Dopamine D2 receptor"),
    ("CHEMBL251",  "Adenosine A2a receptor"),
    ("CHEMBL203",  "EGFR"),
    ("CHEMBL301",  "CDK2"),
    ("CHEMBL210",  "Beta-2 adrenergic receptor"),
    ("CHEMBL1871", "Androgen receptor"),
    ("CHEMBL2034", "Glucocorticoid receptor"),
    ("CHEMBL325",  "Serotonin 5-HT2A receptor"),
]


# ── Helpers ──────────────────────────────────────────────────────────────────

def _get(url: str, params: dict, retries: int = 3) -> dict | None:
    for attempt in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if attempt == retries - 1:
                print(f"    ⚠  GET failed: {e}")
                return None
            time.sleep(1.5)


def fetch_target_activities(target_id: str, max_records: int = MAX_PER_TARGET) -> list[dict]:
    """Fetch activity records (with SMILES + pChEMBL) for one target."""
    records: list[dict] = []
    params = {
        "target_chembl_id": target_id,
        "standard_type__in": "IC50,Ki",
        "pchembl_value__isnull": "false",
        "limit": LIMIT,
        "offset": 0,
    }
    while len(records) < max_records:
        data = _get(API, params)
        if data is None:
            break
        page = data.get("activities", [])
        if not page:
            break
        records.extend(page)
        meta   = data.get("page_meta", {})
        total  = meta.get("total_count", len(records))
        offset = params["offset"] + LIMIT
        if offset >= total or len(records) >= max_records:
            break
        params["offset"] = offset
        time.sleep(DELAY)
    return records[:max_records]


def _rdkit_descriptors(smiles: str) -> dict:
    if not HAS_RDKIT:
        return {"MW": np.nan, "LogP": np.nan}
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {"MW": np.nan, "LogP": np.nan}
    return {
        "MW":   round(Descriptors.MolWt(mol), 3),
        "LogP": round(Descriptors.MolLogP(mol), 3),
    }


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    all_dfs: list[pd.DataFrame] = []

    for target_id, target_name in TARGETS:
        print(f"\n📥 {target_name} ({target_id}) …")
        activities = fetch_target_activities(target_id)
        print(f"   Raw records fetched: {len(activities)}")

        rows = []
        for act in activities:
            smi = (act.get("canonical_smiles") or "").strip()
            if not smi or "." in smi:   # skip mixtures / salts
                continue
            try:
                pv = float(act["pchembl_value"])
            except (TypeError, ValueError, KeyError):
                continue
            rows.append({
                "smiles": smi,
                "pchembl_value": pv,
                "chembl_id": act.get("molecule_chembl_id", ""),
                "target_chembl_id": target_id,
                "target_name": target_name,
            })

        if not rows:
            print(f"   ⚠  No valid rows for {target_id}")
            continue

        df = pd.DataFrame(rows)
        # per-SMILES de-dup within this target
        df = (df.groupby("smiles", as_index=False)
                .agg(pchembl_value=("pchembl_value", "mean"),
                     chembl_id=("chembl_id", "first"),
                     target_chembl_id=("target_chembl_id", "first"),
                     target_name=("target_name", "first")))

        print(f"   Unique compounds: {len(df)}")
        all_dfs.append(df)

    if not all_dfs:
        print("❌ No data downloaded.")
        return

    combined = pd.concat(all_dfs, ignore_index=True)
    print(f"\nCombined pre-dedup: {len(combined)} rows")

    # Global dedup: if same SMILES appears in multiple targets, keep mean pchembl
    combined = (combined.groupby("smiles", as_index=False)
                        .agg(pchembl_value=("pchembl_value", "mean"),
                             chembl_id=("chembl_id", "first"),
                             target_chembl_id=("target_chembl_id", "first"),
                             target_name=("target_name", "first")))
    print(f"After global SMILES dedup: {len(combined)} rows")

    # Validate SMILES with RDKit and add descriptors
    if HAS_RDKIT:
        valid = []
        for _, row in combined.iterrows():
            mol = Chem.MolFromSmiles(row["smiles"])
            if mol is None:
                continue
            desc = _rdkit_descriptors(row["smiles"])
            valid.append({**row.to_dict(), **desc})
        combined = pd.DataFrame(valid)
        n_invalid = len(pd.concat(all_dfs, ignore_index=True).drop_duplicates("smiles")) - len(combined)
        print(f"RDKit-valid compounds: {len(combined)}  ({n_invalid} invalid SMILES dropped)")
    else:
        combined["MW"]   = np.nan
        combined["LogP"] = np.nan

    # Final column order
    out_cols = ["smiles", "pchembl_value", "chembl_id",
                "target_chembl_id", "target_name", "MW", "LogP"]
    combined = combined[[c for c in out_cols if c in combined.columns]]

    print(f"\npChEMBL range: {combined['pchembl_value'].min():.2f} – {combined['pchembl_value'].max():.2f}")
    print(f"Mean: {combined['pchembl_value'].mean():.2f}  |  Std: {combined['pchembl_value'].std():.2f}")
    print(f"Target breakdown:\n{combined['target_name'].value_counts().to_string()}")

    combined.to_csv(OUT_CSV, index=False)
    print(f"\n✅ Saved {len(combined)} rows → {OUT_CSV}")


if __name__ == "__main__":
    main()
