"""
build_dataset.py: turn the raw WA wheat statistics into the clean CSVs the
analysis uses.

Data provenance
---------------
WA wheat area and production by season. The authoritative sources are
ABARES (Australian crop report / agricultural commodity statistics) and the
ABS agricultural commodities collection; both publish WA wheat area (ha)
and production (t) back several decades, but as spreadsheets whose layout
changes. Rather than pretend to parse every vintage of workbook, this
pipeline takes a documented CSV contract you can fill from whichever
official table you download:

    # source: <URL of the ABARES/ABS table you transcribed or exported>
    year,wheat_area_ha,wheat_production_t
    1975,3200000,4100000
    ...

Season labelling: use the year the crop was SOWN (season "1975-76" is year
1975). That is what lines the season up with the April-October growing-season
rainfall the rainfall-decline project measures.

An ABARES-style CSV export whose header row carries recognisable column
names (year/season, area, production) is also accepted; the parser reports
what it matched so nothing is silently misread.

Usage
-----
    python3 build_dataset.py [source_dir] [out_dir]
"""
import os
import re
import sys
import numpy as np
import pandas as pd


def _season_to_year(val):
    """'1975-76', '1975/76' or '1975' -> 1975 (year of sowing)."""
    s = str(val).strip()
    m = re.match(r"^(\d{4})\s*[-/]\s*\d{2,4}$", s)
    if m:
        return int(m.group(1))
    m = re.match(r"^(\d{4})(\.0)?$", s)
    if m:
        return int(m.group(1))
    return None


def parse_wheat_csv(path):
    """Documented contract or a recognisable ABARES-style export."""
    with open(path, errors="replace") as f:
        lines = f.read().splitlines()
    src = next((l.split(":", 1)[1].strip() for l in lines[:10]
                if l.lower().startswith("# source")), "")
    hdr_i = next((i for i, l in enumerate(lines[:30])
                  if not l.lstrip().startswith("#") and "," in l), None)
    if hdr_i is None:
        return None
    cells = [c.strip().strip('"').lower() for c in lines[hdr_i].split(",")]
    if not any(c in ("year", "season") or c.startswith("year") for c in cells):
        return None
    acol = next((c for c in cells if "area" in c), None)
    pcol = next((c for c in cells if "production" in c or "prod" in c), None)
    if acol is None or pcol is None:
        return None
    df = pd.read_csv(path, skiprows=hdr_i, comment="#")
    df.columns = [c.strip().strip('"').lower() for c in df.columns]
    ycol = next(c for c in df.columns if c in ("year", "season")
                or c.startswith("year"))
    out = pd.DataFrame({
        "year": df[ycol].map(_season_to_year),
        "area_ha": pd.to_numeric(df[acol], errors="coerce"),
        "production_t": pd.to_numeric(df[pcol], errors="coerce"),
    }).dropna()
    if len(out) < 20:
        return None
    out["year"] = out.year.astype(int)
    out = out[(out.area_ha > 0) & (out.production_t >= 0)]
    out["yield_t_ha"] = out.production_t / out.area_ha
    out.attrs["source"] = src
    out.attrs["matched"] = f"year={ycol}, area={acol}, production={pcol}"
    return out.sort_values("year").reset_index(drop=True)


def main(source_dir=None, out_dir="data"):
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [source_dir] if source_dir else [
        os.path.join(here, "..", "dropzone"), os.path.join(here, "data", "raw")]
    files = []
    for d in candidates:
        if d and os.path.isdir(d):
            files += [os.path.join(d, f) for f in sorted(os.listdir(d))
                      if f.lower().endswith((".csv", ".txt"))]
    wheat, provenance = None, []
    for path in files:
        try:
            df = parse_wheat_csv(path)
        except Exception as e:
            print(f"  skipped {os.path.basename(path)}: {e}")
            continue
        if df is None:
            continue
        wheat = df
        provenance.append({"file": os.path.basename(path), "n_rows": len(df),
                           "first": int(df.year.min()), "last": int(df.year.max()),
                           "columns_matched": df.attrs["matched"],
                           "source": df.attrs["source"]})
        print(f"  wheat file: {os.path.basename(path)} "
              f"({df.year.min()}-{df.year.max()}; {df.attrs['matched']})")
        break                    # one series per run
    if wheat is None:
        print(__doc__)
        raise SystemExit("No wheat statistics file found; see "
                         "dropzone/DROP_FILES_HERE.md.")
    if not wheat.attrs["source"]:
        print("  WARNING: no '# source:' line in the wheat file; add one so "
              "every number stays traceable.")

    # sanity: WA wheat yields have historically sat between ~0.3 and ~2.5 t/ha
    bad = wheat[(wheat.yield_t_ha < 0.1) | (wheat.yield_t_ha > 6.0)]
    if len(bad):
        raise SystemExit(f"Implausible yields (t/ha) in years "
                         f"{bad.year.tolist()}; check the units "
                         "(area must be hectares, production tonnes).")

    os.makedirs(out_dir, exist_ok=True)
    wheat.to_csv(os.path.join(out_dir, "wheat_wa_clean.csv"), index=False)
    pd.DataFrame(provenance).to_csv(os.path.join(out_dir, "source-library.csv"),
                                    index=False)
    print(f"\nSeasons: {wheat.year.min()}-{wheat.year.max()} "
          f"({len(wheat)} rows)")
    print(f"Wrote clean CSVs to {out_dir}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or [None]))
