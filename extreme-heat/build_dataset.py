"""
build_dataset.py: turn raw daily-temperature downloads into the clean CSVs
the analysis uses.

Data provenance
---------------
Daily maximum (and where available minimum) temperature from GHCN-Daily
(NOAA NCEI). The Australian (ASN*) records in GHCN-Daily ARE the Bureau of
Meteorology's station observations redistributed by NOAA in a script-friendly
format, the same source the rainfall-decline project used. BoM Climate Data
Online daily temperature CSVs are also accepted for cross-checking.

Two ways in:
1. Direct download (needs open network access):
       python3 build_dataset.py --fetch
   pulls the configured stations from the NCEI access API and validates the
   station NAME field against the expected name, so a mistyped station id
   cannot slip through.
2. Dropzone ingestion (default): drop GHCN daily-summaries CSVs or BoM CDO
   daily temperature CSVs into ../dropzone/ and run without --fetch. Files
   are detected by content.

Definitions
-----------
Hot day       = TMAX >= 35 C. Very hot day = TMAX >= 40 C. TXx = hottest
                day of the year.
Heatwave      = 3 or more consecutive days with TMAX at or above that
                calendar day's 90th percentile (15-day window around the day,
                baseline 1961-1990 where the station covers at least 20 of
                those years, otherwise the full record, and the output says
                which).
Completeness  = a calendar year is kept only if 18 or fewer TMAX days are
                missing (about 95% complete).
Units         = GHCN-Daily distributes temperatures either in degrees C or
                tenths of degrees C depending on how the file was requested.
                If a station's median TMAX exceeds 80 the file is treated as
                tenths and divided by 10 (nowhere on Earth has a median
                daily maximum of 80 C); the provenance log records when this
                conversion fires.

Usage
-----
    python3 build_dataset.py [source_dir] [out_dir]
    python3 build_dataset.py --fetch [out_dir]
"""
import io
import os
import sys
import urllib.request
import numpy as np
import pandas as pd

# Stations to fetch with --fetch. Ids are validated against the expected
# name substring after download; a mismatch aborts the build.
STATIONS = {
    "ASN00009021": "PERTH AIRPORT",
    "ASN00004032": "PORT HEDLAND",
}
NCEI = ("https://www.ncei.noaa.gov/access/services/data/v1"
        "?dataset=daily-summaries&stations={sid}&startDate=1950-01-01"
        "&endDate=2025-12-31&dataTypes=TMAX,TMIN&format=csv"
        "&includeStationName=true&units=metric")

HOT, VERY_HOT = 35.0, 40.0
BASE_START, BASE_END = 1961, 1990
MIN_BASE_YEARS = 20
MAX_MISSING_DAYS = 18
HW_MIN_RUN = 3
PCTL = 90.0
WINDOW_HALF = 7            # 15-day window = day +/- 7


def _split(line):
    return [c.strip().strip('"') for c in line.split(",")]


def _maybe_tenths(vals, log, label):
    med = np.nanmedian(vals)
    if np.isfinite(med) and med > 80.0:
        log.append(f"{label}: values look like tenths of C (median {med:.0f}); "
                   "divided by 10")
        return vals / 10.0
    return vals


def parse_ghcn(path, log):
    """GHCN daily-summaries CSV: STATION, DATE, TMAX [, TMIN, NAME]."""
    head = open(path, errors="replace").readline()
    cells = [c.upper() for c in _split(head)]
    if not ("STATION" in cells and "DATE" in cells and "TMAX" in cells):
        return None
    df = pd.read_csv(path)
    df.columns = [c.strip().strip('"').upper() for c in df.columns]
    out = pd.DataFrame({
        "station": df.STATION.astype(str),
        "name": (df.NAME.astype(str) if "NAME" in df.columns else df.STATION.astype(str)),
        "date": pd.to_datetime(df.DATE, errors="coerce"),
        "tmax_c": pd.to_numeric(df.TMAX, errors="coerce"),
    })
    if "TMIN" in df.columns:
        out["tmin_c"] = pd.to_numeric(df.TMIN, errors="coerce")
    out = out.dropna(subset=["date"])
    for col in ("tmax_c", "tmin_c"):
        if col in out.columns:
            out[col] = _maybe_tenths(out[col].values, log,
                                     f"{os.path.basename(path)} {col}")
    return out


def parse_bom_cdo(path, log):
    """BoM Climate Data Online daily temperature CSV: Year/Month/Day columns
    plus a 'Maximum temperature' (or Minimum) column."""
    head = open(path, errors="replace").readline()
    cells = [c.lower() for c in _split(head)]
    if not ({"year", "month", "day"} <= set(cells)
            and any("temperature" in c for c in cells)):
        return None
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    low = {c.lower(): c for c in df.columns}
    tcol = next((low[c] for c in low if "maximum temperature" in c), None)
    kind = "tmax_c"
    if tcol is None:
        tcol = next((low[c] for c in low if "minimum temperature" in c), None)
        kind = "tmin_c"
    if tcol is None:
        return None
    sid_col = next((low[c] for c in low if "station number" in c), None)
    sid = str(df[sid_col].iloc[0]) if sid_col else os.path.basename(path)
    out = pd.DataFrame({
        "station": sid, "name": sid,
        "date": pd.to_datetime(dict(year=df[low["year"]], month=df[low["month"]],
                                    day=df[low["day"]]), errors="coerce"),
        kind: pd.to_numeric(df[tcol], errors="coerce"),
    }).dropna(subset=["date"])
    log.append(f"{os.path.basename(path)}: BoM CDO {kind} file for station {sid}")
    return out


def fetch_stations(log):
    frames = []
    for sid, expect in STATIONS.items():
        url = NCEI.format(sid=sid)
        print(f"  fetching {sid} ({expect}) ...")
        with urllib.request.urlopen(url, timeout=120) as r:
            text = r.read().decode("utf-8", "replace")
        df = parse_ghcn_text(text, log, label=sid)
        if df is None or df.empty:
            raise SystemExit(f"Fetch for {sid} returned no parsable data.")
        got = str(df.name.iloc[0]).upper()
        if expect not in got:
            raise SystemExit(
                f"Station {sid} returned name '{got}', expected it to contain "
                f"'{expect}'. Verify the station id before trusting any output.")
        frames.append(df)
        log.append(f"fetched {sid}: {got}, {df.date.min().date()} to "
                   f"{df.date.max().date()}")
    return frames


def parse_ghcn_text(text, log, label):
    tmp = io.StringIO(text)
    first = tmp.readline()
    cells = [c.upper() for c in _split(first)]
    if not ("STATION" in cells and "DATE" in cells and "TMAX" in cells):
        return None
    tmp.seek(0)
    df = pd.read_csv(tmp)
    df.columns = [c.strip().strip('"').upper() for c in df.columns]
    out = pd.DataFrame({
        "station": df.STATION.astype(str),
        "name": (df.NAME.astype(str) if "NAME" in df.columns else df.STATION.astype(str)),
        "date": pd.to_datetime(df.DATE, errors="coerce"),
        "tmax_c": pd.to_numeric(df.TMAX, errors="coerce"),
    })
    if "TMIN" in df.columns:
        out["tmin_c"] = pd.to_numeric(df.TMIN, errors="coerce")
    out = out.dropna(subset=["date"])
    out["tmax_c"] = _maybe_tenths(out.tmax_c.values, log, f"{label} tmax")
    return out


# ---------------------------------------------------------------------------
# Heat metrics
# ---------------------------------------------------------------------------

def doy_percentile_threshold(daily, pctl=PCTL, half=WINDOW_HALF):
    """90th-percentile TMAX per calendar day, from a 15-day window across the
    baseline years. Returns (thresholds indexed 1..366, baseline_label).
    Day-of-year is computed on a leap-stable basis (29 Feb shares day 366)."""
    d = daily.dropna(subset=["tmax_c"]).copy()
    base = d[(d.date.dt.year >= BASE_START) & (d.date.dt.year <= BASE_END)]
    if base.date.dt.year.nunique() >= MIN_BASE_YEARS:
        ref, label = base, f"{BASE_START}-{BASE_END}"
    else:
        ref, label = d, "full record"
    doy = ref.date.dt.dayofyear.values
    vals = ref.tmax_c.values
    thr = np.full(367, np.nan)
    for day in range(1, 367):
        lo, hi = day - half, day + half
        window = ((doy >= lo) & (doy <= hi))
        if lo < 1:
            window |= (doy >= lo + 366)
        if hi > 366:
            window |= (doy <= hi - 366)
        sel = vals[window]
        if sel.size >= 30:
            thr[day] = np.percentile(sel, pctl)
    return thr, label


def heatwave_runs(flags, min_run=HW_MIN_RUN):
    """Count runs of consecutive True of length >= min_run.
    Returns (n_events, n_days_in_those_events). NaN-safe: missing days break
    a run (conservative: never bridges a gap)."""
    n_events = n_days = run = 0
    for f in flags:
        if f:
            run += 1
        else:
            if run >= min_run:
                n_events += 1
                n_days += run
            run = 0
    if run >= min_run:
        n_events += 1
        n_days += run
    return n_events, n_days


def annual_metrics(daily):
    """Per-station, per-year heat metrics with completeness accounting."""
    rows = []
    for (st, name), g in daily.groupby(["station", "name"]):
        g = g.drop_duplicates(subset="date").sort_values("date")
        thr, thr_label = doy_percentile_threshold(g)
        doy = g.date.dt.dayofyear.values
        above = g.tmax_c.values >= thr[doy]
        above &= np.isfinite(g.tmax_c.values)
        g = g.assign(above90=above)
        for y, gy in g.groupby(g.date.dt.year):
            expected = 366 if pd.Timestamp(int(y), 12, 31).is_leap_year else 365
            valid = gy.tmax_c.notna().sum()
            missing = expected - int(valid)
            tmax = gy.tmax_c
            ev, days = heatwave_runs(gy.above90.values)
            rows.append({
                "station": st, "name": name, "year": int(y),
                "days_ge_35": int((tmax >= HOT).sum()),
                "days_ge_40": int((tmax >= VERY_HOT).sum()),
                "txx_c": float(tmax.max()) if valid else float("nan"),
                "hw_events": ev, "hw_days": days,
                "days_missing": missing,
                "complete": missing <= MAX_MISSING_DAYS,
                "hw_baseline": thr_label,
            })
    return pd.DataFrame(rows).sort_values(["station", "year"]).reset_index(drop=True)


def main(argv):
    log = []
    if argv and argv[0] == "--fetch":
        out_dir = argv[1] if len(argv) > 1 else "data"
        frames = fetch_stations(log)
    else:
        source_dir = argv[0] if argv else None
        out_dir = argv[1] if len(argv) > 1 else "data"
        here = os.path.dirname(os.path.abspath(__file__))
        candidates = [source_dir] if source_dir else [
            os.path.join(here, "..", "dropzone"), os.path.join(here, "data", "raw")]
        files = []
        for d in candidates:
            if d and os.path.isdir(d):
                files += [os.path.join(d, f) for f in sorted(os.listdir(d))
                          if f.lower().endswith((".csv", ".txt"))]
        frames = []
        for path in files:
            try:
                df = parse_ghcn(path, log)
                if df is None:
                    df = parse_bom_cdo(path, log)
            except Exception as e:
                print(f"  skipped {os.path.basename(path)}: {e}")
                continue
            if df is not None and not df.empty:
                frames.append(df)
                print(f"  temperature file: {os.path.basename(path)} -> "
                      f"{df.station.iloc[0]} ({df.date.min().date()} to "
                      f"{df.date.max().date()})")
        if not frames:
            print(__doc__)
            raise SystemExit(
                "No temperature files found. Either run with --fetch on a "
                "machine with open network access, or drop GHCN/BoM daily "
                "CSVs into ../dropzone/ (see dropzone/DROP_FILES_HERE.md).")

    daily = pd.concat(frames, ignore_index=True)
    # merge tmax/tmin fragments (e.g. separate BoM CDO files) per station+date
    agg = {"name": "first", "tmax_c": "max"}
    if "tmin_c" in daily.columns:
        agg["tmin_c"] = "min"
    daily = (daily.groupby(["station", "date"], as_index=False).agg(agg))
    metrics = annual_metrics(daily)

    os.makedirs(out_dir, exist_ok=True)
    daily.to_csv(os.path.join(out_dir, "temperature_daily_clean.csv"), index=False)
    metrics.to_csv(os.path.join(out_dir, "annual_heat_metrics.csv"), index=False)
    pd.DataFrame({"note": log}).to_csv(os.path.join(out_dir, "source-library.csv"),
                                       index=False)
    for st, g in metrics.groupby("station"):
        ok = g[g.complete]
        print(f"  {st} ({g.name.iloc[0]}): {len(ok)} complete years "
              f"{ok.year.min()}-{ok.year.max()}, heatwave baseline "
              f"{g.hw_baseline.iloc[0]}")
    print(f"Wrote clean CSVs to {out_dir}/")


if __name__ == "__main__":
    main(sys.argv[1:])
