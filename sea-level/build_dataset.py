"""
build_dataset.py: turn the raw Fremantle tide-gauge download into the clean
CSVs the analysis uses.

Data provenance
---------------
PSMSL (Permanent Service for Mean Sea Level) monthly Revised Local Reference
(RLR) data for Fremantle, PSMSL station 111, one of the longest tide-gauge
records in the Southern Hemisphere (from 1897). Download the "monthly RLR
data" file from the station page at psmsl.org (Data > Obtaining monthly
means > Fremantle) and drop it into ../dropzone/sea-level/ or
sea-level/data/raw/.

The RLR file is semicolon-separated: decimal year; height (mm, RLR datum);
days missing flag; quality flag; missing values are -99999. A plain CSV with
year/month/msl_mm columns is also accepted. Files are detected by content.

The RLR datum places sea level around 7000 mm to keep values positive; the
level itself is arbitrary, so the outputs carry both the raw RLR height and
an anomaly against the station's 1990-2009 mean.

Definitions
-----------
Annual mean  = mean of monthly means, kept only if 10 or more months of the
               year are present (documented in the completeness column).
Anomaly      = annual mean minus the 1990-2009 mean of annual means.

Usage
-----
    python3 build_dataset.py [source_dir] [out_dir]
"""
import os
import sys
import numpy as np
import pandas as pd

REF_START, REF_END = 1990, 2009
MIN_MONTHS = 10
MISSING = -99999


def parse_rlr_monthly(path):
    """PSMSL monthly RLR: 'decimal_year; height_mm; missing_flag; quality'."""
    rows = []
    with open(path, errors="replace") as f:
        for ln in f:
            parts = [p.strip() for p in ln.split(";")]
            if len(parts) < 2:
                return None
            try:
                t = float(parts[0])
                h = float(parts[1])
            except ValueError:
                return None
            rows.append((t, h))
    if len(rows) < 120:                      # need at least 10 years
        return None
    df = pd.DataFrame(rows, columns=["decimal_year", "msl_mm"])
    df.loc[df.msl_mm <= MISSING, "msl_mm"] = np.nan
    # RLR heights are defined to sit roughly 7000 mm above the datum; PSMSL's
    # "metric" files sit near local datum (hundreds of mm) and can contain
    # datum shifts, so they must not be analysed as a time series
    med = float(df.msl_mm.median())
    if med < 3000:
        raise SystemExit(
            f"This looks like a PSMSL METRIC file (median height {med:.0f} mm), "
            "not the RLR file. Metric data can contain datum shifts and is not "
            "safe for trend analysis. Download the 'monthly RLR data' file "
            "(e.g. 111.rlrdata) from the same PSMSL station page instead.")
    df["year"] = df.decimal_year.astype(int)
    # PSMSL encodes month k as year + (k - 0.5)/12
    df["month"] = (np.round((df.decimal_year - df.year) * 12 + 0.5)
                   .astype(int).clip(1, 12))
    return df[["year", "month", "msl_mm"]]


def parse_csv_monthly(path):
    """Generic CSV with year, month and an msl/sea-level column (mm)."""
    head = open(path, errors="replace").readline().lower()
    cells = [c.strip().strip('"') for c in head.split(",")]
    if not ("year" in cells and "month" in cells
            and any("msl" in c or "sea" in c for c in cells)):
        return None
    df = pd.read_csv(path, comment="#")
    df.columns = [c.strip().lower() for c in df.columns]
    mcol = next(c for c in df.columns if "msl" in c or "sea" in c)
    out = pd.DataFrame({
        "year": pd.to_numeric(df.year, errors="coerce"),
        "month": pd.to_numeric(df.month, errors="coerce"),
        "msl_mm": pd.to_numeric(df[mcol], errors="coerce"),
    }).dropna(subset=["year", "month"])
    out["year"] = out.year.astype(int)
    out["month"] = out.month.astype(int)
    out.loc[out.msl_mm <= MISSING, "msl_mm"] = np.nan
    return out if len(out) >= 120 else None


def to_annual(monthly):
    rows = []
    for y, g in monthly.groupby("year"):
        vals = g.msl_mm.dropna()
        rows.append({
            "year": int(y), "msl_mm": float(vals.mean()) if len(vals) else np.nan,
            "n_months": int(len(vals)),
            "complete": len(vals) >= MIN_MONTHS,
        })
    annual = pd.DataFrame(rows).sort_values("year").reset_index(drop=True)
    ref = annual[(annual.year >= REF_START) & (annual.year <= REF_END)
                 & annual.complete]
    if len(ref) < 10:
        raise SystemExit(f"Fewer than 10 complete years inside the "
                         f"{REF_START}-{REF_END} reference period; check the input.")
    annual["anom_mm"] = annual.msl_mm - ref.msl_mm.mean()
    return annual


def main(source_dir=None, out_dir="data"):
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [source_dir] if source_dir else [
        os.path.join(here, "..", "dropzone", "sea-level"),
        os.path.join(here, "..", "dropzone"),      # back-compat: flat dropzone
        os.path.join(here, "data", "raw")]
    files = []
    for d in candidates:
        if d and os.path.isdir(d):
            files += [os.path.join(d, f) for f in sorted(os.listdir(d))
                      if f.lower().endswith((".csv", ".txt", ".rlrdata",
                                             ".metdata", ".dat"))]
    monthly, provenance = None, []
    for path in files:
        try:
            df = parse_rlr_monthly(path)
            kind = "rlr_monthly"
            if df is None:
                df = parse_csv_monthly(path)
                kind = "csv_monthly"
        except Exception as e:
            print(f"  skipped {os.path.basename(path)}: {e}")
            continue
        if df is None:
            continue
        monthly = df
        provenance.append({"file": os.path.basename(path), "kind": kind,
                           "n_rows": len(df), "first": int(df.year.min()),
                           "last": int(df.year.max())})
        print(f"  tide-gauge file: {os.path.basename(path)} "
              f"({df.year.min()}-{df.year.max()}, {kind})")
        break            # one gauge per run
    if monthly is None:
        print(__doc__)
        raise SystemExit("No tide-gauge file found; see "
                         "dropzone/DROP_FILES_HERE.md.")

    annual = to_annual(monthly)
    os.makedirs(out_dir, exist_ok=True)
    monthly.to_csv(os.path.join(out_dir, "msl_monthly.csv"), index=False)
    annual.to_csv(os.path.join(out_dir, "msl_annual.csv"), index=False)
    pd.DataFrame(provenance).to_csv(os.path.join(out_dir, "source-library.csv"),
                                    index=False)
    ok = annual[annual.complete]
    print(f"\nComplete years: {len(ok)} ({ok.year.min()}-{ok.year.max()})")
    print(f"Wrote clean CSVs to {out_dir}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or [None]))
