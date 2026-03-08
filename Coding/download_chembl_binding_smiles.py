"""
download_chembl_binding_smiles.py
---------------------------------
Fetch canonical SMILES for all compound_ids in chembl_binding_affinity.csv
using the ChEMBL REST molecule endpoint (batched, up to 50 IDs per request).

Output: data/raw/chembl/chembl_binding_affinity_with_smiles.csv
        Same as input + 'smiles' column; rows with no structure are dropped.
"""

import time
import requests
import pandas as pd
from pathlib import Path

BASE_DIR  = Path(__file__).parent
IN_CSV    = BASE_DIR / "data/raw/chembl/chembl_binding_affinity.csv"
OUT_CSV   = BASE_DIR / "data/raw/chembl/chembl_binding_affinity_with_smiles.csv"
BATCH     = 50          # ChEMBL molecule API handles ~50 IDs per request reliably
DELAY     = 0.5         # seconds between requests (be a good citizen)
CHEMBL_MOLECULE_URL = "https://www.ebi.ac.uk/chembl/api/data/molecule"


def fetch_smiles_batch(chembl_ids: list[str]) -> dict[str, str]:
    """Return {chembl_id: canonical_smiles} for one batch. Missing → absent."""
    params = {
        "chembl_id__in": ",".join(chembl_ids),
        "format": "json",
        "limit": len(chembl_ids),
    }
    try:
        r = requests.get(CHEMBL_MOLECULE_URL, params=params, timeout=30)
        r.raise_for_status()
        molecules = r.json().get("molecules", [])
    except Exception as exc:
        print(f"  ⚠  batch error ({exc}), skipping batch")
        return {}

    result = {}
    for mol in molecules:
        cid = mol.get("molecule_chembl_id", "")
        structs = mol.get("molecule_structures") or {}
        smi = structs.get("canonical_smiles", "")
        if cid and smi:
            result[cid] = smi
    return result


def main():
    df = pd.read_csv(IN_CSV)
    compound_ids = df["compound_id"].unique().tolist()
    print(f"Loaded {len(df)} rows, {len(compound_ids)} unique compound IDs")

    smiles_map: dict[str, str] = {}
    batches = [compound_ids[i : i + BATCH] for i in range(0, len(compound_ids), BATCH)]
    print(f"Fetching SMILES in {len(batches)} batches of ≤{BATCH} …")

    for bid, batch in enumerate(batches, 1):
        if bid % 5 == 0 or bid == 1:
            print(f"  batch {bid}/{len(batches)}  (resolved so far: {len(smiles_map)})")
        batch_result = fetch_smiles_batch(batch)
        smiles_map.update(batch_result)
        time.sleep(DELAY)

    df["smiles"] = df["compound_id"].map(smiles_map)
    n_missing = df["smiles"].isna().sum()
    n_found   = len(df) - n_missing
    print(f"\nSMILES resolved: {n_found}/{len(df)}  ({n_missing} missing → dropped)")

    df_out = df.dropna(subset=["smiles"]).reset_index(drop=True)
    # reorder: smiles right after compound_id
    cols = df_out.columns.tolist()
    cols.remove("smiles")
    cols.insert(1, "smiles")
    df_out = df_out[cols]

    df_out.to_csv(OUT_CSV, index=False)
    print(f"Saved {len(df_out)} rows → {OUT_CSV}")


if __name__ == "__main__":
    main()
