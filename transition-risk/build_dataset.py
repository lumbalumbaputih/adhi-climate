"""build_dataset.py: turn the Clean Energy Regulator's published Safeguard
Mechanism facility files into the clean WA panel the analysis uses.

Data provenance
---------------
One CSV per compliance year from cer.gov.au (see dropzone/DROP_FILES_HERE.md
for the exact pages): the "safeguard facility data" tables for 2016-17 to
2022-23 (the original Safeguard) and the "baselines and emissions" tables for
2023-24 onward (the reformed Safeguard). Column names shift between vintages;
this parser normalises them by keyword and reports what it matched. Values
use thousands separators and ' - ' for blank; both are cleaned.

The reform seam: from 2023-24 baselines are production-adjusted and decline
each year, and Safeguard Mechanism Credits (SMCs) exist. Baselines before and
after the seam are NOT comparable and the panel carries a `regime` column so
the analysis never mixes them; covered emissions are one continuous series.

Compliance years are labelled by their starting year (2016-17 -> 2016).

Usage:  python3 build_dataset.py [source_dir] [out_dir]
"""
import glob
import os
import re
import sys

import numpy as np
import pandas as pd

REFORM_START = 2023        # first reformed compliance year (2023-24)


def _num(x):
    """CER number cells: '1,234', ' -   ', '', '(123)' -> float or nan."""
    s = str(x).strip().replace(",", "").replace("–", "-")
    if s in ("", "-", "nan", "None"):
        return np.nan
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    try:
        v = float(s)
    except ValueError:
        return np.nan
    return -v if neg else v


def _find(cols, *keywords, exclude=()):
    """First column whose lowercase name contains all keywords."""
    for c in cols:
        low = c.lower()
        if all(k in low for k in keywords) and not any(e in low for e in exclude):
            return c
    return None


def parse_year_csv(path):
    """One CER facility CSV -> tidy rows. Returns (frame, notes) or None."""
    year_m = re.search(r"(20\d\d)-\d\d", os.path.basename(path))
    if not year_m:
        return None
    year = int(year_m.group(1))
    try:
        df = pd.read_csv(path, encoding="utf-8-sig", low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="cp1252", low_memory=False)
    df.columns = [str(c).strip() for c in df.columns]
    cols = list(df.columns)

    fac = _find(cols, "facility", "name")
    state = _find(cols, "state")
    emitter = _find(cols, "responsible", "emitter", exclude=("abn",))
    baseline = _find(cols, "baseline", "emissions", "number") or \
        _find(cols, "baseline", "number", exclude=("multi", "mymp", "cumul"))
    covered = _find(cols, "covered", "emissions")
    net = _find(cols, "net", "emissions", "number", exclude=("multi", "mymp",
                                                             "cumul"))
    if not all((fac, state, baseline, covered)):
        return None
    accus_surr = _find(cols, "accu", "surrendered", exclude=("deemed",)) or \
        _find(cols, "carbon credit units surrendered")
    smcs_surr = _find(cols, "smc", "surrendered")
    smcs_issued = _find(cols, "smc", "issued")
    sector = _find(cols, "anzsic") or _find(cols, "type", "baseline")
    # 2016-17 reports facilities on a multi-year monitoring period with a
    # CUMULATIVE baseline in the 'Baseline number' column; the start-date
    # column identifies them (later vintages carry MYMP figures separately).
    mymp = _find(cols, "multi-year", "start")
    mymp_active = (df[mymp].astype(str).str.strip().str.len().gt(1)
                   if mymp else pd.Series(False, index=df.index))

    out = pd.DataFrame({
        "year": year,
        "facility": df[fac].astype(str).str.strip(),
        "state": df[state].astype(str).str.strip().str.upper(),
        "emitter": (df[emitter].astype(str).str.strip() if emitter else ""),
        "baseline_t": df[baseline].map(_num),
        "covered_t": df[covered].map(_num),
        "net_t": df[net].map(_num) if net else np.nan,
        "accus_surrendered": df[accus_surr].map(_num) if accus_surr else 0.0,
        "smcs_surrendered": df[smcs_surr].map(_num) if smcs_surr else 0.0,
        "smcs_issued": df[smcs_issued].map(_num) if smcs_issued else 0.0,
        "sector_raw": df[sector].astype(str).str.strip() if sector else "",
        "regime": "reformed" if year >= REFORM_START else "original",
        "baseline_mymp_cumulative": mymp_active.values,
    })
    out = out[out.facility.notna() & (out.facility != "") &
              (out.facility.str.lower() != "nan") & out.covered_t.notna()]
    notes = (f"matched: facility={fac!r}, baseline={baseline!r}, "
             f"covered={covered!r}, accus={accus_surr!r}, smcs={smcs_surr!r}")
    return out, notes


SECTOR_BUCKETS = [
    ("LNG / oil and gas", ("oil and gas", "petroleum")),
    ("Metal ore mining", ("metal ore", "iron ore")),
    ("Coal mining", ("coal mining",)),
    ("Alumina and metals", ("basic non-ferrous", "alumina", "smelt")),
    ("Electricity", ("electricity",)),
    ("Other manufacturing", ("manufactur", "cement", "chemical")),
    ("Transport", ("transport", "air and space", "rail", "water freight")),
    ("Waste", ("waste",)),
]


def bucket_sector(raw):
    low = str(raw).lower()
    for name, keys in SECTOR_BUCKETS:
        if any(k in low for k in keys):
            return name
    return "Other"


def canonical_facility(name):
    """Light normalisation so the same facility matches across vintages."""
    s = str(name).upper().strip()
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def main(source_dir=None, out_dir="data"):
    here = os.path.dirname(os.path.abspath(__file__))
    source_dir = source_dir or os.path.join(here, "..", "dropzone",
                                            "transition-risk")
    files = sorted(glob.glob(os.path.join(source_dir, "*.csv")))
    files = [f for f in files if "surrender-methods" not in f]
    if not files:
        print(__doc__)
        raise SystemExit("No CER facility CSVs found; see "
                         "dropzone/DROP_FILES_HERE.md.")
    frames, provenance = [], []
    for path in files:
        parsed = parse_year_csv(path)
        if parsed is None:
            print(f"  skipped {os.path.basename(path)} (columns not recognised)")
            continue
        df, notes = parsed
        frames.append(df)
        provenance.append({"file": os.path.basename(path),
                           "year": int(df.year.iloc[0]), "n_rows": len(df),
                           "columns_matched": notes})
        print(f"  {df.year.iloc[0]}: {len(df)} facilities ({notes})")
    panel = pd.concat(frames, ignore_index=True)
    panel["facility_id"] = panel.facility.map(canonical_facility)
    panel["sector"] = panel.sector_raw.map(bucket_sector)
    # ANZSIC only exists from 2023-24 (earlier vintages carry no industry
    # column), so backfill each facility's sector from its most recent
    # classified year; facilities never seen post-reform stay "Other".
    known = (panel[panel.sector != "Other"]
             .sort_values("year")
             .groupby("facility_id").sector.last())
    panel["sector"] = panel.facility_id.map(known).fillna("Other")
    # Facilities on a multi-year monitoring period report a CUMULATIVE
    # baseline (e.g. North West Shelf 2016-17: 22.7 Mt vs ~7.7 Mt annual
    # emissions), not comparable to an annual one. The parser flags them from
    # the file's own MYMP column; analysis and charts exclude flagged
    # baselines from headroom while keeping the raw value visible here.

    wa = panel[panel.state.str.contains("WA", na=False)].copy()
    # facility matching table: id -> the name variants seen, per year count
    match = (wa.groupby("facility_id")
             .agg(names=("facility", lambda s: "; ".join(sorted(set(s)))),
                  years=("year", "nunique"),
                  first_year=("year", "min"), last_year=("year", "max"),
                  emitters=("emitter", lambda s: "; ".join(sorted(set(s)))))
             .reset_index())

    os.makedirs(out_dir, exist_ok=True)
    wa.drop(columns=["sector_raw"]).to_csv(
        os.path.join(out_dir, "safeguard_wa_clean.csv"), index=False)
    match.to_csv(os.path.join(out_dir, "facility_matching.csv"), index=False)
    pd.DataFrame(provenance).to_csv(os.path.join(out_dir,
                                                 "source-library.csv"),
                                    index=False)
    latest = wa[wa.year == wa.year.max()]
    print(f"\nWA panel: {wa.facility_id.nunique()} facilities, "
          f"{wa.year.min()}-{wa.year.max()}; latest year covered emissions "
          f"{latest.covered_t.sum()/1e6:.1f} Mt CO2-e")
    print(f"Wrote clean CSVs to {out_dir}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or [None]))
