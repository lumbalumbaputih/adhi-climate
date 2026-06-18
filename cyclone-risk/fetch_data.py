"""
fetch_data.py
=============
Downloads the authoritative source datasets for the Western Australia
Tropical Cyclone Climate Risk Analysis.

All three sources are official primary sources:

  1. IBTrACS v04r01, Southern Indian Ocean subset (NOAA NCEI)
     International Best Track Archive for Climate Stewardship.
  2. ERSSTv5 monthly sea surface temperature (NOAA Physical Sciences Lab)
     Extended Reconstructed Sea Surface Temperature, version 5.
  3. Bureau of Meteorology Southern Hemisphere tropical cyclone database
     (cross reference for Australian naming and WA landfall flags).

Run once before opening the analysis notebook:

    python fetch_data.py

Files are written to data/raw/. They are git-ignored because they are large;
the notebook reads them from there and writes the cleaned, committed outputs
to data/.

Network note: these hosts must be reachable. In a restricted egress
environment, add www.ncei.noaa.gov, downloads.psl.noaa.gov and
www.bom.gov.au to the allowed hosts first.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import requests

RAW_DIR = Path(__file__).resolve().parent / "data" / "raw"

# Each source: key -> (url, output filename, minimum plausible size in bytes,
#                       whether the run should fail if this one cannot be fetched)
SOURCES = {
    "ibtracs": (
        "https://www.ncei.noaa.gov/data/"
        "international-best-track-archive-for-climate-stewardship-ibtracs/"
        "v04r01/access/csv/ibtracs.SI.list.v04r01.csv",
        "ibtracs.SI.list.v04r01.csv",
        5_000_000,   # the SI subset is tens of MB
        True,        # required
    ),
    "ersst": (
        "https://downloads.psl.noaa.gov/Datasets/noaa.ersst.v5/sst.mnmean.nc",
        "ersst.v5.sst.mnmean.nc",
        10_000_000,  # single global monthly NetCDF, ~tens of MB
        True,        # required for the SST correlation step
    ),
    "bom": (
        # BOM Southern Hemisphere tropical cyclone database (all-seasons CSV).
        # Secondary cross-reference only; the run continues if it is missing.
        "http://www.bom.gov.au/clim_data/IDCKMSTM0S.csv",
        "bom_IDCKMSTM0S.csv",
        100_000,
        False,       # optional cross-reference
    ),
}

HEADERS = {
    # A descriptive UA; NCEI rejects some default client agents.
    "User-Agent": "adhi-climate-research/1.0 (portfolio analysis; contact via github)"
}


def _download(url: str, dest: Path, min_size: int, retries: int = 4) -> bool:
    """Stream a URL to dest with exponential backoff. Returns True on success."""
    for attempt in range(retries):
        try:
            with requests.get(url, headers=HEADERS, stream=True, timeout=120) as r:
                r.raise_for_status()
                tmp = dest.with_suffix(dest.suffix + ".part")
                size = 0
                with open(tmp, "wb") as fh:
                    for chunk in r.iter_content(chunk_size=1 << 20):
                        if chunk:
                            fh.write(chunk)
                            size += len(chunk)
                if size < min_size:
                    tmp.unlink(missing_ok=True)
                    raise ValueError(
                        f"downloaded {size:,} bytes, below expected minimum "
                        f"{min_size:,}; treating as a bad/blocked response"
                    )
                tmp.replace(dest)
                print(f"  ok  {dest.name}  ({size:,} bytes)")
                return True
        except Exception as exc:  # noqa: BLE001  (report and back off)
            wait = 2 ** (attempt + 1)
            print(f"  attempt {attempt + 1}/{retries} failed: {exc}")
            if attempt < retries - 1:
                print(f"  retrying in {wait}s ...")
                time.sleep(wait)
    return False


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Saving raw source data to: {RAW_DIR}\n")

    failed_required = []
    for key, (url, fname, min_size, required) in SOURCES.items():
        dest = RAW_DIR / fname
        tag = "required" if required else "optional"
        print(f"[{key}] ({tag})\n  {url}")
        if dest.exists() and dest.stat().st_size >= min_size:
            print(f"  ok  already present: {dest.name} "
                  f"({dest.stat().st_size:,} bytes)")
            continue
        if not _download(url, dest, min_size) and required:
            failed_required.append(key)
        print()

    if failed_required:
        print("ERROR: could not fetch required source(s): "
              f"{', '.join(failed_required)}")
        print("Check that the official hosts are reachable "
              "(egress allowlist) and retry.")
        return 1

    print("All required sources are present. You can run the notebook now.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
