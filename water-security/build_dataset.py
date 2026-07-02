"""
build_dataset.py: turn raw streamflow downloads into the clean CSVs the
analysis uses.

Data provenance
---------------
Gauged streamflow: Bureau of Meteorology Hydrologic Reference Stations (HRS),
bom.gov.au/water/hrs/. HRS stations are the BoM's curated set of long-record,
high-quality gauges in catchments with minimal regulation, which is exactly
what a trend analysis needs. Download the daily streamflow CSV for 5-8
south-west WA stations (Darling Range / SW forest catchments) and drop the
files into ../dropzone/water-security/ (or water-security/data/raw/). This
script detects them by content, not by filename.

Optional cross-check: Water Corporation's published annual inflow to Perth
dams. If you transcribe or export it, save it as a CSV with columns
year,inflow_GL (any filename), note the source URL in a "# source:" comment
line at the top, and drop it in the same folder.

Definitions
-----------
Water year    = 1 May to 30 April, labelled by the calendar year of the May
                start (SW WA streamflow is winter-dominated, so a May-April
                year keeps each wet season in one bucket).
Baseline      = 1975-1999 water years. The rainfall project shows steps down
                around 1975 and 2000, so 1975-1999 is the between-steps
                reference most HRS records can actually cover.
Completeness  = a water year is kept only if 15 or fewer days are missing or
                invalid; a station enters the regional series only with 18 or
                more complete baseline years.
Regional      = mean of per-station % anomalies vs each station's own baseline
                (so big rivers do not drown out small ones), same construction
                as the rainfall-decline regional series.

Usage
-----
    python3 build_dataset.py [source_dir] [out_dir]

Defaults: source_dir = ../dropzone/water-security (falling back to the flat
../dropzone/ and then data/raw), out_dir = data.
Exits non-zero with instructions if no usable streamflow files are found.
"""
import os
import re
import sys
import numpy as np
import pandas as pd

WY_START_MONTH = 5            # water year starts 1 May
BASE_START, BASE_END = 1975, 1999
MAX_MISSING_DAYS = 15
MIN_BASE_YEARS = 18
MIN_STATIONS = 5              # a year enters the regional series only when at
                              # least this many stations report; a "regional"
                              # mean of one or two gauges is not regional


# ---------------------------------------------------------------------------
# Parsing: tolerant readers that detect files by content
# ---------------------------------------------------------------------------

def _split_csv_line(line):
    return [c.strip().strip('"').strip() for c in line.split(",")]


def _find_header(lines):
    """Index of the first line that looks like a CSV header with a date column."""
    for i, ln in enumerate(lines[:300]):
        if ln.lstrip().startswith("#"):
            continue
        cells = [c.lower() for c in _split_csv_line(ln)]
        if len(cells) >= 2 and any(c == "date" or c.startswith("date") for c in cells):
            return i
    return None


def _station_from_metadata(lines, fallback):
    """Pull a station id/name out of '#' metadata lines if present.

    Handles both explicit 'Station Number: 616999' metadata and the BoM HRS
    layout, where the river name and id share one line:
        #,"Murray River - Baden Powell (614006)"
    """
    sid, name = None, None
    for ln in lines[:300]:
        if not ln.lstrip().startswith("#"):
            continue
        low = ln.lower()
        m = re.search(r"station\s*(?:number|id|no\.?)?\s*[:=]?\s*([0-9]{6}[a-z]?)", low)
        if m and sid is None:
            sid = m.group(1).upper()
        m2 = re.search(r"station\s*name\s*[:=]\s*(.+)", ln, flags=re.IGNORECASE)
        if m2 and name is None:
            name = m2.group(1).strip().strip(",")
        m3 = re.search(r'"?([^"#,]+?)\s*\(([0-9]{6}[a-z]?)\)\s*"?\s*$', ln.strip(),
                       flags=re.IGNORECASE)
        if m3:
            if sid is None:
                sid = m3.group(2).upper()
            if name is None:
                name = m3.group(1).strip()
    return sid or fallback, name or (sid or fallback)


def _parse_dates(series):
    """ISO dates first, then Australian day-first formats."""
    d = pd.to_datetime(series, format="ISO8601", errors="coerce")
    if d.isna().mean() > 0.5:
        d = pd.to_datetime(series, dayfirst=True, errors="coerce")
    return d


def parse_daily_flow(path):
    """Read one file. Returns a tidy frame (station, station_name, date,
    flow_ML) for a daily streamflow file, a (year, inflow_GL) frame for an
    annual inflow file, or None if the file is neither.
    """
    with open(path, "r", errors="replace") as f:
        text = f.read()
    lines = text.splitlines()
    hdr = _find_header(lines)

    # annual inflow cross-check file: columns year, inflow_GL
    for i, ln in enumerate(lines[:50]):
        if ln.lstrip().startswith("#"):
            continue
        cells = [c.lower() for c in _split_csv_line(ln)]
        if "year" in cells and any("inflow" in c or c == "gl" for c in cells):
            df = pd.read_csv(path, skiprows=i, comment="#")
            df.columns = [c.strip().lower() for c in df.columns]
            ycol = "year"
            icol = next(c for c in df.columns if "inflow" in c or c == "gl")
            out = pd.DataFrame({
                "year": pd.to_numeric(df[ycol], errors="coerce"),
                "inflow_GL": pd.to_numeric(df[icol], errors="coerce"),
            }).dropna()
            out["year"] = out.year.astype(int)
            src = next((l.split(":", 1)[1].strip() for l in lines[:20]
                        if l.lower().startswith("# source")), "")
            out.attrs["kind"], out.attrs["source"] = "annual_inflow", src
            return out
        break

    if hdr is None:
        return None
    cols = _split_csv_line(lines[hdr])
    low = [c.lower() for c in cols]
    datecol = next(c for c, cl in zip(cols, low) if cl == "date" or cl.startswith("date"))
    flowcol = None
    for c, cl in zip(cols, low):
        if c == datecol:
            continue
        if "flow" in cl or "discharge" in cl or "ml" in cl:
            flowcol = c
            break
    if flowcol is None and len(cols) == 2:
        flowcol = [c for c in cols if c != datecol][0]
    if flowcol is None:
        return None

    df = pd.read_csv(path, skiprows=hdr, comment="#")
    df.columns = [c.strip().strip('"') for c in df.columns]
    if datecol not in df.columns or flowcol not in df.columns:
        return None
    dates = _parse_dates(df[datecol].astype(str))
    flow = pd.to_numeric(df[flowcol], errors="coerce")
    flow = flow.where(flow >= 0)          # negative flows are invalid
    ok = dates.notna()
    if ok.sum() < 3650:                    # need ~10 years of daily data
        return None
    fallback = os.path.splitext(os.path.basename(path))[0]
    sid, name = _station_from_metadata(lines, fallback)
    out = pd.DataFrame({"station": sid, "station_name": name,
                        "date": dates[ok], "flow_ML": flow[ok]})
    out.attrs["kind"] = "daily_flow"
    return out


# ---------------------------------------------------------------------------
# Water-year aggregation
# ---------------------------------------------------------------------------

def water_year_label(dates):
    """Water year = May..April, labelled by the calendar year of the May start."""
    dates = pd.DatetimeIndex(dates)
    return np.where(dates.month >= WY_START_MONTH, dates.year, dates.year - 1)


def wy_expected_days(wy):
    """Days from 1 May wy to 30 April wy+1 inclusive."""
    start = pd.Timestamp(int(wy), WY_START_MONTH, 1)
    end = pd.Timestamp(int(wy) + 1, WY_START_MONTH, 1)
    return int((end - start).days)


def to_water_years(daily):
    """Per-station water-year totals with an explicit completeness flag."""
    d = daily.copy()
    d["water_year"] = water_year_label(d.date)
    rows = []
    for (st, name), g in d.groupby(["station", "station_name"]):
        g = g.dropna(subset=["flow_ML"]).drop_duplicates(subset="date")
        for wy, gg in g.groupby("water_year"):
            expected = wy_expected_days(wy)
            missing = expected - len(gg)
            rows.append({
                "station": st, "station_name": name, "water_year": int(wy),
                "total_ML": float(gg.flow_ML.sum()),
                "days_missing": int(missing),
                "complete": missing <= MAX_MISSING_DAYS,
            })
    return pd.DataFrame(rows).sort_values(["station", "water_year"]).reset_index(drop=True)


def build_regional(clean):
    """Regional mean-of-% -anomaly series from complete station years."""
    c = clean[clean.complete].copy()
    base = (c[(c.water_year >= BASE_START) & (c.water_year <= BASE_END)]
            .groupby("station").total_ML.agg(baseline_ML="mean", n_base="count"))
    keep = base[base.n_base >= MIN_BASE_YEARS]
    dropped = sorted(set(c.station) - set(keep.index))
    if dropped:
        print(f"  excluded (fewer than {MIN_BASE_YEARS} complete baseline years): "
              + ", ".join(dropped))
    if keep.empty:
        raise SystemExit("No station has enough complete 1975-1999 baseline years; "
                         "check the input records.")
    c = c[c.station.isin(keep.index)].merge(keep.baseline_ML.reset_index(), on="station")
    c["anom_pct"] = (c.total_ML / c.baseline_ML - 1.0) * 100.0
    reg = (c.groupby("water_year")
            .agg(regional_anom_pct=("anom_pct", "mean"),
                 n_stations=("station", "size"))
            .reset_index())
    thin = reg[reg.n_stations < MIN_STATIONS]
    if len(thin):
        print(f"  dropped {len(thin)} water years with fewer than "
              f"{MIN_STATIONS} reporting stations: "
              f"{int(thin.water_year.min())}-{int(thin.water_year.max())}")
        reg = reg[reg.n_stations >= MIN_STATIONS].reset_index(drop=True)
    full_base = float(keep.baseline_ML.mean())
    reg["regional_ML_adj"] = full_base * (1.0 + reg.regional_anom_pct / 100.0)
    return reg, c, full_base


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(source_dir=None, out_dir="data"):
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [source_dir] if source_dir else [
        os.path.join(here, "..", "dropzone", "water-security"),
        os.path.join(here, "..", "dropzone"),      # back-compat: flat dropzone
        os.path.join(here, "data", "raw")]
    files = []
    for d in candidates:
        if d and os.path.isdir(d):
            files += [os.path.join(d, f) for f in sorted(os.listdir(d))
                      if f.lower().endswith((".csv", ".txt"))]
    daily, annual, provenance = [], None, []
    for path in files:
        try:
            parsed = parse_daily_flow(path)
        except Exception as e:
            print(f"  skipped {os.path.basename(path)}: {e}")
            continue
        if parsed is None:
            continue
        if parsed.attrs.get("kind") == "annual_inflow":
            annual = parsed
            provenance.append({"file": os.path.basename(path), "kind": "annual_inflow",
                               "station": "", "n_rows": len(parsed),
                               "first": int(parsed.year.min()), "last": int(parsed.year.max()),
                               "note": parsed.attrs.get("source", "")})
            print(f"  annual inflow cross-check: {os.path.basename(path)} "
                  f"({parsed.year.min()}-{parsed.year.max()})")
        else:
            daily.append(parsed)
            provenance.append({"file": os.path.basename(path), "kind": "daily_flow",
                               "station": parsed.station.iloc[0], "n_rows": len(parsed),
                               "first": str(parsed.date.min().date()),
                               "last": str(parsed.date.max().date()), "note": ""})
            print(f"  daily flow: {os.path.basename(path)} -> station "
                  f"{parsed.station.iloc[0]} ({parsed.date.min().date()} to "
                  f"{parsed.date.max().date()})")
    if not daily:
        print(__doc__)
        raise SystemExit(
            "No daily streamflow files found. Download HRS daily CSVs "
            "(see dropzone/DROP_FILES_HERE.md) and re-run.")

    os.makedirs(out_dir, exist_ok=True)
    clean = to_water_years(pd.concat(daily, ignore_index=True))
    reg, stations, full_base = build_regional(clean)
    clean.to_csv(os.path.join(out_dir, "streamflow_clean.csv"), index=False)
    stations[["station", "station_name", "water_year", "total_ML",
              "baseline_ML", "anom_pct"]].to_csv(
        os.path.join(out_dir, "station_anomalies.csv"), index=False)
    reg.to_csv(os.path.join(out_dir, "annual_streamflow_anomaly.csv"), index=False)
    if annual is not None:
        annual.to_csv(os.path.join(out_dir, "wc_inflow.csv"), index=False)
    pd.DataFrame(provenance).to_csv(os.path.join(out_dir, "source-library.csv"),
                                    index=False)
    print(f"\nStations in the regional series: {stations.station.nunique()} "
          f"(full-network baseline {full_base:,.0f} ML)")
    print(f"Water years: {reg.water_year.min()}-{reg.water_year.max()}")
    print(f"Wrote clean CSVs to {out_dir}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or [None]))
