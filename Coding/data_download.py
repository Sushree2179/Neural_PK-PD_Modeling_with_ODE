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
    url = "https://pk-db.com/api/v1/studies/"
    dest = DATA_DIR / "pkdb" / "studies.json"
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        dest.write_bytes(r.content)
        print(f"[ok] downloaded {dest}")
        data = r.json()
        if "results" in data and isinstance(data["results"], list):
            trimmed = {"results": data["results"][:limit]}
            dest_trim = DATA_DIR / "pkdb" / f"studies_top{limit}.json"
            dest_trim.write_text(json.dumps(trimmed, indent=2))
            print(f"[ok] wrote trimmed list to {dest_trim}")
    except Exception as e:  # noqa: BLE001
        print(f"[fail] {url} -> {dest}: {e}")


def fetch_pkdb_timecourses(max_studies: int = 1, max_outputs_per_study: int = 5) -> None:
    """Attempt to pull a few time-course outputs for quick inspection.

    Note: PK-DB output endpoints sometimes require auth or may differ; this tries a
    handful of known URL shapes and saves any successful JSON responses.
    """

    studies_path = DATA_DIR / "pkdb" / "studies.json"
    if not studies_path.exists():
        print(f"[skip] missing {studies_path}; run studies fetch first")
        return

    try:
        studies = json.loads(studies_path.read_text()).get("data", {}).get("data", [])
    except Exception as e:  # noqa: BLE001
        print(f"[warn] could not parse studies for timecourses: {e}")
        return

    attempts = [
        "https://pk-db.com/api/v1/outputs/{oid}",
        "https://pk-db.com/api/v1/outputs/{oid}/",
        "https://pk-db.com/api/outputs/{oid}",
        "https://pk-db.com/api/outputs/{oid}/",
    ]

    for study in studies[:max_studies]:
        outputs = study.get("outputset", {}).get("outputs", [])
        for oid in outputs[:max_outputs_per_study]:
            dest = DATA_DIR / "pkdb" / f"output_{oid}.json"
            if dest.exists():
                print(f"[skip] {dest} exists")
                continue
            ok = False
            for tmpl in attempts:
                url = tmpl.format(oid=oid)
                try:
                    r = requests.get(url, timeout=30)
                    if r.status_code == 200 and r.headers.get("content-type", "").startswith("application/json"):
                        ensure_dir(dest.parent)
                        dest.write_bytes(r.content)
                        print(f"[ok] downloaded {dest} from {url}")
                        ok = True
                        break
                except Exception:
                    continue
            if not ok:
                print(f"[fail] could not fetch output {oid} (auth or endpoint mismatch)")


def main() -> None:
    ensure_dir(DATA_DIR)

    # PubChem: small assay slices (hERG and CYP3A4) and a few exemplar compounds.
    fetch_pubchem_assay(588834, label="herg_qhts")
    fetch_pubchem_assay(54772, label="cyp3a4_inhibition")
    for compound in ["warfarin", "midazolam", "caffeine"]:
        fetch_pubchem_compound(compound)

    # PK-DB: studies metadata (trim to first 50 entries for quick inspection) + sample outputs.
    fetch_pkdb_studies(limit=50)
    fetch_pkdb_timecourses(max_studies=1, max_outputs_per_study=5)

    print("\nDone. Files are under", DATA_DIR)


if __name__ == "__main__":
    main()
