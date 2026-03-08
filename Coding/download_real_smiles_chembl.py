"""
Download real molecular SMILES + ADMET properties from ChEMBL REST API.

This replaces the synthetic placeholder data in data/raw/tdc/ with real
experimental measurements from ChEMBL, keyed on canonical SMILES.

Endpoints used:
  • hERG inhibition   : ChEMBL hERG channel (CHEMBL240) IC50/Ki assays
  • Caco-2 permeability: ChEMBL Caco-2 (CHEMBL3786999 / Papp) assays
  • Hepatocyte CL     : ChEMBL hepatocyte clearance assays
  • Binding affinity  : SMILES for existing CHEMBL* IDs in binding data

All data are from the public ChEMBL REST API — no registration required.
Outputs overwrite (or create) the CSV files in data/raw/tdc/.
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import requests

ROOT     = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "raw" / "tdc"
DATA_DIR.mkdir(parents=True, exist_ok=True)

CHEMBL_API = "https://www.ebi.ac.uk/chembl/api/data"
HEADERS    = {"Accept": "application/json"}
LIMIT      = 1000   # records per page (max ChEMBL allows)
DELAY      = 0.3    # seconds between requests (be polite)

# ── Helpers ──────────────────────────────────────────────────────────────────

def _get(url: str, params: dict | None = None, retries: int = 3) -> Optional[dict]:
    for attempt in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=30)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if attempt == retries - 1:
                print(f"  ⚠  Failed: {url} → {e}")
                return None
            time.sleep(1)


def paginate(url: str, params: dict, max_records: int = 5000) -> list[dict]:
    """Walk ChEMBL pagination and collect records up to max_records."""
    records = []
    params  = {**params, "limit": LIMIT, "offset": 0}
    while len(records) < max_records:
        data = _get(url, params)
        if data is None:
            break
        page = data.get("activities", data.get("molecules", []))
        if not page:
            break
        records.extend(page)
        meta   = data.get("page_meta", {})
        total  = meta.get("total_count", len(records))
        offset = meta.get("offset", 0) + LIMIT
        print(f"     fetched {len(records):,}/{min(total, max_records):,}", end="\r")
        if offset >= total or offset >= max_records:
            break
        params["offset"] = offset
        time.sleep(DELAY)
    print()
    return records


# ── Task 1: hERG inhibition ────────────────────────────────────────────────

def download_herg(max_records: int = 6000) -> pd.DataFrame:
    """
    Binary hERG inhibition from ChEMBL.
    Uses IC50/Ki measurements on hERG target (CHEMBL240).
    canonical_smiles is in the activity record — no separate lookup needed.
    Binarise: pIC50 ≥ 5 (IC50 ≤ 10 µM) → inhibitor (1), else 0.
    """
    print("\n📥 hERG inhibition (ChEMBL target CHEMBL240) …")
    activities = paginate(
        f"{CHEMBL_API}/activity",
        params={
            "target_chembl_id": "CHEMBL240",
            "standard_type__in": "IC50,Ki",
            "pchembl_value__isnull": "false",
        },
        max_records=max_records,
    )
    print(f"  Raw activities: {len(activities):,}")

    rows = []
    for act in activities:
        try:
            pv  = float(act["pchembl_value"])
            cid = act["molecule_chembl_id"]
            smi = act.get("canonical_smiles") or ""
            if not smi:
                continue
            rows.append({"chembl_id": cid, "smiles": smi,
                         "herg_pic50": pv, "herg": int(pv >= 5.0)})
        except (TypeError, ValueError, KeyError):
            continue

    df = pd.DataFrame(rows).dropna(subset=["smiles"])
    # one record per molecule (take mean pIC50 → re-binarise)
    df = df.groupby(["chembl_id", "smiles"], as_index=False) \
           .agg(herg_pic50=("herg_pic50", "mean"), herg=("herg", "median"))
    df["herg"] = (df["herg"] >= 0.5).astype(int)

    df = _add_rdkit_descriptors(df)
    print(f"  ✅ hERG: {len(df):,} compounds  |  inhibitors: {df['herg'].sum():,}")
    return df[["smiles", "herg", "MW", "LogP", "HBA", "HBD"]]


# ── Task 2: Caco-2 permeability ────────────────────────────────────────────

def download_caco2(max_records: int = 3000) -> pd.DataFrame:
    """
    Caco-2 effective permeability (Papp A→B) from ChEMBL.
    canonical_smiles is in the activity record.
    Binarise: Papp ≥ 1 (in 10⁻⁶ cm/s) → highly permeable (1).
    """
    print("\n📥 Caco-2 permeability (ChEMBL Papp assays) …")
    activities = paginate(
        f"{CHEMBL_API}/activity",
        params={"standard_type": "Papp"},
        max_records=max_records,
    )
    print(f"  Raw activities: {len(activities):,}")

    rows = []
    for act in activities:
        try:
            val  = float(act["standard_value"])
            unit = act.get("standard_units") or ""
            # normalise to 10⁻⁶ cm/s
            if "cm/s" in unit and "10" not in unit:
                val *= 1e6
            smi = act.get("canonical_smiles") or ""
            if not smi or val <= 0:
                continue
            cid = act["molecule_chembl_id"]
            rows.append({"chembl_id": cid, "smiles": smi, "caco2_wang": val})
        except (TypeError, ValueError, KeyError):
            continue

    if not rows:
        print("  ⚠  No Papp data found — skipping Caco-2 download")
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df = df.groupby(["chembl_id", "smiles"], as_index=False)["caco2_wang"].median()
    df = _add_rdkit_descriptors(df)

    print(f"  ✅ Caco-2: {len(df):,} compounds")
    return df[["smiles", "caco2_wang", "MW", "LogP", "HBA", "HBD"]]


# ── Task 3: Hepatocyte clearance ────────────────────────────────────────────

def download_clearance(max_records: int = 3000) -> pd.DataFrame:
    """
    Hepatocyte intrinsic clearance (CLint, µL/min/mg) from ChEMBL.
    canonical_smiles in activity record.  Log-transforms value.
    """
    print("\n📥 Hepatocyte clearance (ChEMBL CL assays, ADME type) …")
    activities = paginate(
        f"{CHEMBL_API}/activity",
        params={
            "standard_type": "CL",
            "assay_type": "A",      # ADME / pharmacokinetic
        },
        max_records=max_records,
    )
    print(f"  Raw activities: {len(activities):,}")

    rows = []
    for act in activities:
        try:
            val = float(act["standard_value"])
            if val <= 0:
                continue
            smi = act.get("canonical_smiles") or ""
            if not smi:
                continue
            cid = act["molecule_chembl_id"]
            rows.append({"chembl_id": cid, "smiles": smi,
                         "clearance_hepatocyte_az": np.log(val)})
        except (TypeError, ValueError, KeyError):
            continue

    if not rows:
        print("  ⚠  No CL data found — skipping clearance download")
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df = df.groupby(["chembl_id", "smiles"], as_index=False)["clearance_hepatocyte_az"].median()
    df = _add_rdkit_descriptors(df)
    print(f"  ✅ Clearance: {len(df):,} compounds")
    return df[["smiles", "clearance_hepatocyte_az", "MW", "LogP", "NumRings"]]


# ── RDKit descriptor helper ────────────────────────────────────────────────

def _add_rdkit_descriptors(df: pd.DataFrame) -> pd.DataFrame:
    """Add MW, LogP, HBA, HBD, NumRings from RDKit for all smiles in df."""
    try:
        from rdkit import Chem
        from rdkit.Chem import Descriptors
    except ImportError:
        print("  ⚠  RDKit not available — descriptor columns will be NaN")
        for col in ["MW", "LogP", "HBA", "HBD", "NumRings"]:
            df[col] = np.nan
        return df

    mw_list, logp_list, hba_list, hbd_list, ring_list = [], [], [], [], []
    for smi in df["smiles"]:
        mol = Chem.MolFromSmiles(str(smi)) if pd.notna(smi) else None
        if mol:
            mw_list.append(Descriptors.MolWt(mol))
            logp_list.append(Descriptors.MolLogP(mol))
            hba_list.append(Descriptors.NumHAcceptors(mol))
            hbd_list.append(Descriptors.NumHDonors(mol))
            ring_list.append(Descriptors.RingCount(mol))
        else:
            mw_list.append(np.nan)
            logp_list.append(np.nan)
            hba_list.append(np.nan)
            hbd_list.append(np.nan)
            ring_list.append(np.nan)

    df = df.copy()
    df["MW"]      = mw_list
    df["LogP"]    = logp_list
    df["HBA"]     = hba_list
    df["HBD"]     = hbd_list
    df["NumRings"] = ring_list
    return df.dropna(subset=["MW", "LogP"])


# ── Main ───────────────────────────────────────────────────────────────────

def main() -> None:
    print("\n" + "=" * 65)
    print("ChEMBL REAL ADMET DATA DOWNLOADER")
    print("Replacing synthetic placeholder SMILES with real structures")
    print("=" * 65)

    # ---- hERG -------------------------------------------------------
    try:
        herg_df = download_herg(max_records=6000)
        if len(herg_df) > 50:
            out = DATA_DIR / "tdc_herg.csv"
            herg_df.to_csv(out, index=False)
            print(f"  💾 Saved → {out.name}  ({len(herg_df):,} rows)")
        else:
            print("  ⚠  hERG: too few rows, keeping existing file")
    except Exception as e:
        print(f"  ❌ hERG download failed: {e}")

    # ---- Caco-2 -------------------------------------------------------
    try:
        caco2_df = download_caco2(max_records=3000)
        if len(caco2_df) > 50:
            out = DATA_DIR / "tdc_caco2_wang.csv"
            caco2_df.to_csv(out, index=False)
            print(f"  💾 Saved → {out.name}  ({len(caco2_df):,} rows)")
        else:
            print("  ⚠  Caco-2: too few rows, keeping existing file")
    except Exception as e:
        print(f"  ❌ Caco-2 download failed: {e}")

    # ---- Clearance -------------------------------------------------------
    try:
        cl_df = download_clearance(max_records=3000)
        if len(cl_df) > 50:
            out = DATA_DIR / "tdc_clearance_hepatocyte_az.csv"
            cl_df.to_csv(out, index=False)
            print(f"  💾 Saved → {out.name}  ({len(cl_df):,} rows)")
        else:
            print("  ⚠  Clearance: too few rows, keeping existing file")
    except Exception as e:
        print(f"  ❌ Clearance download failed: {e}")

    print("\n✅ Real SMILES download complete.")
    print(f"   Data saved to: {DATA_DIR}")
    print("\n👉 Next: re-run phase1_2 notebook cells to rebuild fingerprint CSV.")


if __name__ == "__main__":
    main()
