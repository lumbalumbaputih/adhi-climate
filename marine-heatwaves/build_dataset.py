"""
build_dataset.py: turn raw sea-surface-temperature downloads into the clean
CSVs the analysis uses, and run the marine-heatwave detection.

Data provenance
---------------
NOAA OISST v2.1 (Optimum Interpolation SST): daily, quarter-degree, global,
from September 1981. The easiest scriptable slice is an ERDDAP CSV subset of
a small box off the WA coast; NOAA CoastWatch and NCEI both run ERDDAP
servers carrying OISST. Drop one or more ERDDAP CSV exports (columns
time, latitude, longitude, sst; ERDDAP puts a units row under the header)
into ../dropzone/marine-heatwaves/ or marine-heatwaves/data/raw/.

The default study box is the Ningaloo coast, the epicentre of the famous
2011 "Ningaloo Nino" event: roughly 21.5 S to 23.5 S, 112.5 E to 114.5 E.
Any box works; the code averages whatever cells arrive. Analyse one box per
run (drop only one box's files at a time) so the spatial mean is honest.

Marine heatwave definition (Hobday et al. 2016)
-----------------------------------------------
Climatology mean and 90th-percentile threshold per calendar day, pooled over
an 11-day window across the 1982-2011 baseline years, then both smoothed
with a 31-day moving average; an event is 5 or more consecutive days above
the threshold, and events separated by 2 days or fewer are merged. Intensity
is SST minus the climatological mean. Categories follow Hobday et al. 2018:
the peak intensity as a multiple of (threshold minus climatology) gives
I Moderate, II Strong, III Severe, IV Extreme.

Day-of-year handling uses the calendar day-of-year with the +/- 5-day window
absorbing the one-day leap offset; this is the common practical
approximation and is stated in the README.

Usage
-----
    python3 build_dataset.py [source_dir] [out_dir]
"""
import os
import sys
import numpy as np
import pandas as pd

BASE_START, BASE_END = 1982, 2011
MIN_BASE_YEARS = 25
WINDOW_HALF = 5          # 11-day window
SMOOTH = 31              # smoothing of climatology and threshold
MIN_EVENT = 5            # days
MAX_GAP = 2              # days
PCTL = 90.0


def _split(line):
    return [c.strip().strip('"') for c in line.split(",")]


def parse_erddap_sst(path):
    """ERDDAP CSV: header row, units row, then data. Needs time and sst
    columns; latitude/longitude optional (single-cell extracts omit them)."""
    with open(path, errors="replace") as f:
        head = f.readline()
    cells = [c.lower() for c in _split(head)]
    if "time" not in cells or not any(c.startswith("sst") for c in cells):
        return None
    df = pd.read_csv(path, skiprows=[1])      # row 1 is the ERDDAP units row
    df.columns = [c.strip().lower() for c in df.columns]
    sstcol = next(c for c in df.columns if c.startswith("sst"))
    out = pd.DataFrame({
        "date": pd.to_datetime(df["time"], errors="coerce", utc=True)
                  .dt.tz_localize(None).dt.normalize(),
        "sst": pd.to_numeric(df[sstcol], errors="coerce"),
    })
    for c in ("latitude", "longitude"):
        if c in df.columns:
            out[c] = pd.to_numeric(df[c], errors="coerce")
    out = out.dropna(subset=["date", "sst"])
    return out if len(out) else None


def box_mean(cells):
    """Average all grid cells to one SST per day, with cell counts kept so a
    day quietly covered by fewer cells is visible in the provenance."""
    g = cells.groupby("date").agg(sst=("sst", "mean"), n_cells=("sst", "size"))
    return g.reset_index().sort_values("date").reset_index(drop=True)


def _smooth_circular(vals, window):
    """Moving average on a 366-length day-of-year array, wrapping the ends."""
    n = len(vals)
    half = window // 2
    padded = np.concatenate([vals[-half:], vals, vals[:half]])
    out = np.full(n, np.nan)
    for i in range(n):
        seg = padded[i:i + window]
        seg = seg[np.isfinite(seg)]
        if seg.size:
            out[i] = seg.mean()
    return out


def climatology(daily):
    """Per-day-of-year climatological mean and p90 threshold (Hobday 2016).
    Returns (clim_mean[367], threshold[367], baseline_label)."""
    d = daily.dropna(subset=["sst"]).copy()
    base = d[(d.date.dt.year >= BASE_START) & (d.date.dt.year <= BASE_END)]
    if base.date.dt.year.nunique() >= MIN_BASE_YEARS:
        ref, label = base, f"{BASE_START}-{BASE_END}"
    else:
        ref, label = d, "full record"
    doy = ref.date.dt.dayofyear.values
    vals = ref.sst.values
    mean_raw = np.full(367, np.nan)
    thr_raw = np.full(367, np.nan)
    for day in range(1, 367):
        lo, hi = day - WINDOW_HALF, day + WINDOW_HALF
        window = (doy >= lo) & (doy <= hi)
        if lo < 1:
            window |= (doy >= lo + 366)
        if hi > 366:
            window |= (doy <= hi - 366)
        sel = vals[window]
        if sel.size >= 50:
            mean_raw[day] = sel.mean()
            thr_raw[day] = np.percentile(sel, PCTL)
    mean = np.full(367, np.nan)
    thr = np.full(367, np.nan)
    mean[1:] = _smooth_circular(mean_raw[1:], SMOOTH)
    thr[1:] = _smooth_circular(thr_raw[1:], SMOOTH)
    return mean, thr, label


def detect_events(daily, clim_mean, thr):
    """Hobday event detection on a daily frame. Missing days end runs (the
    record is nearly gap-free; any gap handling is conservative). Returns
    (events frame, flagged daily frame)."""
    d = daily.sort_values("date").reset_index(drop=True).copy()
    doy = d.date.dt.dayofyear.values
    d["clim"] = clim_mean[doy]
    d["thr"] = thr[doy]
    d["anom"] = d.sst - d.clim
    # missing calendar days split runs: reindex on the full daily calendar
    full = pd.DataFrame({"date": pd.date_range(d.date.min(), d.date.max(),
                                               freq="D")})
    d = full.merge(d, on="date", how="left")
    above = (d.sst.values > d.thr.values) & np.isfinite(d.sst.values)

    # initial runs
    runs = []
    start = None
    for i, f in enumerate(above):
        if f and start is None:
            start = i
        elif not f and start is not None:
            runs.append((start, i - 1))
            start = None
    if start is not None:
        runs.append((start, len(above) - 1))
    runs = [(a, b) for a, b in runs if b - a + 1 >= MIN_EVENT]
    # merge events separated by MAX_GAP days or fewer
    merged = []
    for a, b in runs:
        if merged and a - merged[-1][1] - 1 <= MAX_GAP:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))

    rows = []
    severity = d.anom / (d.thr - d.clim)
    for k, (a, b) in enumerate(merged, start=1):
        seg = d.iloc[a:b + 1]
        peak = seg.anom.idxmax()
        sev = float(severity.iloc[a:b + 1].max())
        cat = ("IV Extreme" if sev >= 4 else "III Severe" if sev >= 3
               else "II Strong" if sev >= 2 else "I Moderate")
        rows.append({
            "event": k,
            "start": seg.date.iloc[0].date(), "end": seg.date.iloc[-1].date(),
            "duration_days": int(b - a + 1),
            "mean_intensity_c": float(seg.anom.mean()),
            "max_intensity_c": float(seg.anom.max()),
            "peak_date": d.date.iloc[peak].date(),
            "severity_ratio": sev, "category": cat,
        })
    d["mhw"] = False
    for a, b in merged:
        d.iloc[a:b + 1, d.columns.get_loc("mhw")] = True
    return pd.DataFrame(rows), d


def annual_metrics(flagged):
    """Per-year MHW days, event starts, and intensity summaries."""
    f = flagged.copy()
    f["year"] = f.date.dt.year
    rows = []
    for y, g in f.groupby("year"):
        valid = g.sst.notna().sum()
        expected = 366 if pd.Timestamp(int(y), 12, 31).is_leap_year else 365
        mhw = g[g.mhw]
        rows.append({
            "year": int(y), "mhw_days": int(g.mhw.sum()),
            "max_intensity_c": (float(mhw.anom.max()) if len(mhw) else 0.0),
            "mean_sst_c": float(g.sst.mean()) if valid else float("nan"),
            "days_missing": int(expected - valid),
            "complete": (expected - valid) <= 18,
        })
    return pd.DataFrame(rows)


def main(source_dir=None, out_dir="data"):
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [source_dir] if source_dir else [
        os.path.join(here, "..", "dropzone", "marine-heatwaves"),
        os.path.join(here, "..", "dropzone"),      # back-compat: flat dropzone
        os.path.join(here, "data", "raw")]
    files = []
    for d in candidates:
        if d and os.path.isdir(d):
            files += [os.path.join(d, f) for f in sorted(os.listdir(d))
                      if f.lower().endswith((".csv", ".txt"))]
    frames, provenance = [], []
    for path in files:
        try:
            df = parse_erddap_sst(path)
        except Exception as e:
            print(f"  skipped {os.path.basename(path)}: {e}")
            continue
        if df is None:
            continue
        frames.append(df)
        note = ""
        if {"latitude", "longitude"} <= set(df.columns):
            note = (f"box {df.latitude.min():.2f}..{df.latitude.max():.2f} N, "
                    f"{df.longitude.min():.2f}..{df.longitude.max():.2f} E")
        provenance.append({"file": os.path.basename(path), "n_rows": len(df),
                           "first": str(df.date.min().date()),
                           "last": str(df.date.max().date()), "note": note})
        print(f"  SST file: {os.path.basename(path)} ({df.date.min().date()} "
              f"to {df.date.max().date()}) {note}")
    if not frames:
        print(__doc__)
        raise SystemExit("No ERDDAP SST files found; see "
                         "dropzone/DROP_FILES_HERE.md.")

    daily = box_mean(pd.concat(frames, ignore_index=True))
    if daily.date.dt.year.nunique() < 15:
        raise SystemExit("Fewer than 15 years of SST; the climatology would "
                         "be meaningless. Extend the download and re-run.")
    clim_mean, thr, label = climatology(daily)
    events, flagged = detect_events(daily, clim_mean, thr)
    annual = annual_metrics(flagged)

    os.makedirs(out_dir, exist_ok=True)
    daily.to_csv(os.path.join(out_dir, "sst_daily.csv"), index=False)
    flagged[["date", "sst", "clim", "thr", "anom", "mhw"]].to_csv(
        os.path.join(out_dir, "sst_flagged.csv"), index=False)
    events.to_csv(os.path.join(out_dir, "mhw_events.csv"), index=False)
    annual.to_csv(os.path.join(out_dir, "annual_mhw_metrics.csv"), index=False)
    pd.DataFrame(provenance).to_csv(os.path.join(out_dir, "source-library.csv"),
                                    index=False)
    print(f"\nClimatology baseline: {label}; events detected: {len(events)}")
    print(f"Wrote clean CSVs to {out_dir}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or [None]))
