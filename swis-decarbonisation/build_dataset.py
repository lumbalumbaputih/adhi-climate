"""
build_dataset.py: turn raw AEMO WEM downloads into the clean CSVs the
analysis uses.

Data provenance
---------------
Generation: AEMO's Wholesale Electricity Market (WEM) data portal for the
South West Interconnected System (SWIS), data.wa.aemo.com.au. Download the
monthly "Facility SCADA" (or facility metered generation) CSV files for as
many months as you want analysed (the record starts in the mid-2000s) and
drop them into ../dropzone/ or swis-decarbonisation/data/raw/. Files are
detected by content, so no renaming is needed.

Facility-to-fuel mapping: AEMO's WEM facility register CSV if it carries a
fuel/technology column. If the register you can find does not, create a
simple CSV with columns facility,fuel (one row per facility code, a
"# source:" first line recording where the mapping came from) and drop it in
the same folder. build_dataset.py reports every facility it could not map so
nothing is silently binned as "other".

Optional emissions factors: data/emission_factors.csv ships as a template
with the fuel buckets and an EMPTY factor column. Fill it from the current
National Greenhouse Accounts (NGA) factors workbook (kg CO2-e per kWh sent
out, or t/MWh) and record the source. The analysis only computes emissions
intensity when the factors are filled in; it never invents them.

Units
-----
If the energy column header mentions MWh the values are summed as energy.
If it only mentions MW the values are treated as 30-minute interval
averages and converted (MW * 0.5 = MWh); the provenance log records which
conversion applied to which file.

Usage
-----
    python3 build_dataset.py [source_dir] [out_dir]
"""
import os
import re
import sys
import numpy as np
import pandas as pd

FUEL_BUCKETS = [
    # bio before gas so "Landfill Gas" and "Biogas" land in bio
    ("bio", ("landfill", "biogas", "biomass", "waste", "wte")),
    ("coal", ("coal",)),
    ("gas", ("gas", "cogen", "ccgt", "ocgt")),
    ("distillate", ("distillate", "diesel", "oil", "dual")),
    ("wind", ("wind",)),
    ("solar", ("solar", "pv")),
    ("storage", ("battery", "storage", "bess")),
]


def bucket_fuel(raw):
    low = str(raw).lower()
    for bucket, keys in FUEL_BUCKETS:
        if any(k in low for k in keys):
            return bucket
    return "other"


def _split(line):
    return [c.strip().strip('"') for c in line.split(",")]


def _header_and_cols(path, need, max_scan=50):
    """Find the first line whose lowercase cells satisfy `need` (a callable
    on the list of cells). Returns (line_index, cells) or (None, None)."""
    with open(path, "r", errors="replace") as f:
        for i, ln in enumerate(f):
            if i >= max_scan:
                break
            if ln.lstrip().startswith("#"):
                continue
            cells = [c.lower() for c in _split(ln)]
            if need(cells):
                return i, _split(ln)
    return None, None


def parse_scada(path):
    """Facility generation file: needs a date-ish column, a facility column,
    and an energy (MWh) or power (MW) column. Returns tidy (month, facility,
    energy_MWh) plus a unit note, or None."""
    def need(cells):
        has_fac = any("facility" in c for c in cells)
        has_dt = any("date" in c or "interval" in c or "period" in c for c in cells)
        has_en = any("mwh" in c or "energy" in c or re.search(r"\bmw\b", c) or "quantity" in c
                     for c in cells)
        return has_fac and has_dt and has_en
    hdr, cols = _header_and_cols(path, need)
    if hdr is None:
        return None
    low = [c.lower() for c in cols]
    fac = cols[next(i for i, c in enumerate(low) if "facility" in c)]
    dt = cols[next(i for i, c in enumerate(low) if "date" in c or "period" in c
                   or "interval" in c)]
    encol, unit = None, None
    for c, cl in zip(cols, low):
        if "mwh" in cl or "energy" in cl or "quantity" in cl:
            encol, unit = c, "MWh"
            break
    if encol is None:
        for c, cl in zip(cols, low):
            if re.search(r"\bmw\b", cl) or cl.endswith("(mw)"):
                encol, unit = c, "MW"
                break
    if encol is None:
        return None
    df = pd.read_csv(path, skiprows=hdr, comment="#", low_memory=False)
    df.columns = [c.strip().strip('"') for c in df.columns]
    if not {fac, dt, encol} <= set(df.columns):
        return None
    dates = pd.to_datetime(df[dt].astype(str), format="ISO8601", errors="coerce")
    if dates.isna().mean() > 0.5:
        dates = pd.to_datetime(df[dt].astype(str), dayfirst=True, errors="coerce")
    energy = pd.to_numeric(df[encol], errors="coerce")
    if unit == "MW":
        energy = energy * 0.5          # 30-minute interval average -> MWh
    out = pd.DataFrame({"facility": df[fac].astype(str).str.strip(),
                        "date": dates, "energy_MWh": energy}).dropna()
    if out.empty:
        return None
    out["month"] = out.date.dt.to_period("M").astype(str)
    g = (out.groupby(["month", "facility"], as_index=False).energy_MWh.sum())
    g.attrs["kind"], g.attrs["unit"] = "scada", unit
    return g


def parse_fuel_map(path):
    """Facility register or hand-made mapping: facility + fuel/technology."""
    def need(cells):
        return (any("facility" in c for c in cells)
                and any("fuel" in c or "technology" in c for c in cells))
    hdr, cols = _header_and_cols(path, need)
    if hdr is None:
        return None
    low = [c.lower() for c in cols]
    fac = cols[next(i for i, c in enumerate(low) if "facility" in c)]
    fuel = cols[next(i for i, c in enumerate(low) if "fuel" in c or "technology" in c)]
    df = pd.read_csv(path, skiprows=hdr, comment="#")
    df.columns = [c.strip().strip('"') for c in df.columns]
    out = pd.DataFrame({"facility": df[fac].astype(str).str.strip(),
                        "fuel_raw": df[fuel].astype(str).str.strip()})
    out["fuel"] = out.fuel_raw.map(bucket_fuel)
    out = out.drop_duplicates(subset="facility")
    out.attrs["kind"] = "fuel_map"
    return out


def load_factors(out_dir):
    """Emission factors (t CO2-e / MWh) if the user filled the template."""
    path = os.path.join(out_dir, "emission_factors.csv")
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path, comment="#")
    df = df.dropna(subset=["factor_t_per_MWh"])
    if df.empty:
        return None
    return dict(zip(df.fuel, df.factor_t_per_MWh))


def write_factor_template(out_dir):
    path = os.path.join(out_dir, "emission_factors.csv")
    if os.path.exists(path):
        return
    with open(path, "w") as f:
        f.write(
            "# Fill factor_t_per_MWh (tonnes CO2-e per MWh sent out) from the\n"
            "# current National Greenhouse Accounts factors workbook, and cite\n"
            "# it in the source column. Leave rows blank to exclude a fuel\n"
            "# (blank factors mean intensity is simply not computed).\n"
            "fuel,factor_t_per_MWh,source\n")
        for bucket, _ in FUEL_BUCKETS:
            f.write(f"{bucket},,\n")
        f.write("other,,\n")


def main(source_dir=None, out_dir="data"):
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [source_dir] if source_dir else [
        os.path.join(here, "..", "dropzone"), os.path.join(here, "data", "raw")]
    files = []
    for d in candidates:
        if d and os.path.isdir(d):
            files += [os.path.join(d, f) for f in sorted(os.listdir(d))
                      if f.lower().endswith((".csv", ".txt"))]
    gen, fmap, provenance = [], None, []
    for path in files:
        try:
            m = parse_fuel_map(path)
            if m is not None:
                fmap = m
                provenance.append({"file": os.path.basename(path), "kind": "fuel_map",
                                   "n_rows": len(m), "note": ""})
                print(f"  fuel map: {os.path.basename(path)} ({len(m)} facilities)")
                continue
            g = parse_scada(path)
            if g is not None:
                gen.append(g)
                provenance.append({"file": os.path.basename(path), "kind": "scada",
                                   "n_rows": len(g),
                                   "note": f"energy unit {g.attrs['unit']}"
                                           + (" (MW*0.5 conversion)" if g.attrs["unit"] == "MW"
                                              else "")})
                print(f"  generation: {os.path.basename(path)} "
                      f"({g.month.min()} to {g.month.max()}, unit {g.attrs['unit']})")
        except Exception as e:
            print(f"  skipped {os.path.basename(path)}: {e}")
    if not gen:
        print(__doc__)
        raise SystemExit("No generation files found; see dropzone/DROP_FILES_HERE.md.")
    if fmap is None:
        raise SystemExit("No facility-to-fuel mapping found; the analysis refuses "
                         "to guess fuels. See dropzone/DROP_FILES_HERE.md.")

    os.makedirs(out_dir, exist_ok=True)
    allg = (pd.concat(gen, ignore_index=True)
            .groupby(["month", "facility"], as_index=False).energy_MWh.sum())
    merged = allg.merge(fmap[["facility", "fuel"]], on="facility", how="left")
    unmapped = sorted(merged[merged.fuel.isna()].facility.unique())
    if unmapped:
        print(f"  WARNING: {len(unmapped)} facilities have no fuel mapping and are "
              f"binned as 'other': {', '.join(unmapped[:12])}"
              + (" ..." if len(unmapped) > 12 else ""))
        merged["fuel"] = merged.fuel.fillna("other")
    monthly = (merged.groupby(["month", "fuel"], as_index=False).energy_MWh.sum())
    monthly["year"] = monthly.month.str.slice(0, 4).astype(int)
    annual = monthly.groupby(["year", "fuel"], as_index=False).energy_MWh.sum()
    tot = annual.groupby("year").energy_MWh.sum().rename("total_MWh")
    annual = annual.merge(tot, on="year")
    annual["share_pct"] = 100.0 * annual.energy_MWh / annual.total_MWh
    monthly.to_csv(os.path.join(out_dir, "generation_by_fuel_month.csv"), index=False)
    annual.to_csv(os.path.join(out_dir, "annual_fuel_mix.csv"), index=False)
    pd.DataFrame(provenance).to_csv(os.path.join(out_dir, "source-library.csv"),
                                    index=False)
    write_factor_template(out_dir)
    print(f"\nYears: {annual.year.min()}-{annual.year.max()}; "
          f"fuels: {', '.join(sorted(annual.fuel.unique()))}")
    print(f"Wrote clean CSVs to {out_dir}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or [None]))
