"""
build_dataset.py: turn the raw UHSLC hourly tide-gauge downloads into the
clean CSVs the analysis uses.

Data provenance
---------------
Hourly sea level at Fremantle from the University of Hawaii Sea Level Center
(UHSLC), station 175, in two feeds:

1. Research Quality Data Set (RQDS), quality-controlled, 1984 through 2021:
   https://uhslc.soest.hawaii.edu/data/csv/rqds/indian/hourly/h175a.csv
2. Fast Delivery (FD), near-real-time and not fully quality-controlled,
   1984 to the present. Used ONLY from 2022 onward, to extend the record:
   https://uhslc.soest.hawaii.edu/data/csv/fast/hourly/h175.csv

Both files are headerless CSVs: year, month, day, hour, sea level in
millimetres above the UHSLC station zero (NOT Chart Datum, NOT AHD).
Missing values are -32767. Times are UTC per the UHSLC hourly convention;
day boundaries here are therefore UTC days, which shifts local attribution
by at most eight hours and does not move annual statistics.

Two ways in:
1. Self-fetch (default when the cache is empty): downloads both feeds into
   ../dropzone/high-water/ and proceeds. Needs uhslc.soest.hawaii.edu to be
   reachable; check with tools/check-data-access.sh.
2. Dropzone cache: if CSVs are already present in ../dropzone/high-water/
   they are used as-is (files are detected by content, names do not matter).

Definitions
-----------
Splice        = RQDS rows for years through 2021, FD rows from 2022 onward.
                Each daily/hourly output row records which feed it came from.
Plausibility  = readings outside 0..2500 mm are dropped (the record's real
                range is roughly 200..1900 mm); runs of 24+ hours of exactly
                the same value are dropped as a stuck gauge.
Outputs       = data/hourly_sea_level.csv, one row per UTC day with columns
                h00..h23 (mm, blank = missing) plus the source feed, so the
                full hourly record is committed and every downstream number
                can be recomputed from the repo alone; and
                data/daily_sea_level.csv, a browsable daily summary.

Usage
-----
    python3 build_dataset.py [source_dir] [out_dir]
"""
import datetime
import io
import os
import sys
import urllib.request
import numpy as np
import pandas as pd

STATION = "Fremantle (UHSLC station 175)"
RQDS_URL = "https://uhslc.soest.hawaii.edu/data/csv/rqds/indian/hourly/h175a.csv"
FD_URL = "https://uhslc.soest.hawaii.edu/data/csv/fast/hourly/h175.csv"
SENTINEL = -32767
FD_FROM_YEAR = 2022          # FD rows are used only from this year onward
PLAUSIBLE_MM = (0, 2500)     # hard physical screen for this gauge's datum
FLATLINE_HOURS = 24          # runs of identical values at least this long


def parse_uhslc_hourly(text, label):
    """UHSLC headerless hourly CSV: year, month, day, hour, level_mm.

    Returns a frame with columns t (UTC timestamp) and mm, sentinel rows
    dropped. Returns None if the content does not look like this format.
    """
    try:
        df = pd.read_csv(io.StringIO(text), header=None,
                         names=["year", "month", "day", "hour", "mm"])
    except Exception:
        return None
    if df.shape[1] != 5 or len(df) < 1000:
        return None
    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna()
    if df.empty or not (df.hour.between(0, 23).all()
                        and df.month.between(1, 12).all()):
        return None
    t = pd.to_datetime(dict(year=df.year, month=df.month, day=df.day),
                       errors="coerce") + pd.to_timedelta(df.hour, unit="h")
    out = pd.DataFrame({"t": t, "mm": df.mm.astype(float)}).dropna(subset=["t"])
    out = out[out.mm > SENTINEL].reset_index(drop=True)
    print(f"  {label}: {len(out)} valid hours, "
          f"{out.t.min():%Y-%m-%d} to {out.t.max():%Y-%m-%d}")
    return out


def qc(series, log, label):
    """Plausibility screen: hard range, then stuck-gauge flatlines."""
    lo, hi = PLAUSIBLE_MM
    n0 = len(series)
    series = series[(series.mm >= lo) & (series.mm <= hi)].reset_index(drop=True)
    dropped_range = n0 - len(series)
    # A stuck gauge repeats one value for hours on end. Real water levels at
    # an hourly cadence never hold exactly the same millimetre for a day.
    run_id = (series.mm != series.mm.shift()).cumsum()
    run_len = series.groupby(run_id).mm.transform("size")
    flat = run_len >= FLATLINE_HOURS
    dropped_flat = int(flat.sum())
    series = series[~flat].reset_index(drop=True)
    if dropped_range or dropped_flat:
        log.append(f"{label}: dropped {dropped_range} out-of-range and "
                   f"{dropped_flat} flatlined hours in QC")
    return series


def splice(rqds, fd, log):
    """RQDS through FD_FROM_YEAR-1, FD from FD_FROM_YEAR onward."""
    a = rqds[rqds.t.dt.year < FD_FROM_YEAR].assign(feed="rqds")
    b = fd[fd.t.dt.year >= FD_FROM_YEAR].assign(feed="fd")
    both = (pd.concat([a, b], ignore_index=True)
            .drop_duplicates(subset="t").sort_values("t").reset_index(drop=True))
    # Honesty check on the overlap years: the two feeds carry the same gauge,
    # so they should agree almost everywhere RQDS has data.
    ov = rqds.merge(fd, on="t", suffixes=("_r", "_f"))
    if len(ov):
        agree = float((ov.mm_r == ov.mm_f).mean()) * 100
        log.append(f"feed overlap: {len(ov)} shared hours, "
                   f"{agree:.1f}% byte-identical values")
    log.append(f"splice: {len(a)} RQDS hours (through {FD_FROM_YEAR - 1}), "
               f"{len(b)} FD hours ({FD_FROM_YEAR} on)")
    return both


def to_wide(hourly):
    """One row per UTC day: date, feed, h00..h23 (mm, blank = missing)."""
    df = hourly.copy()
    df["date"] = df.t.dt.strftime("%Y-%m-%d")
    df["hh"] = "h" + df.t.dt.hour.astype(str).str.zfill(2)
    wide = df.pivot_table(index="date", columns="hh", values="mm",
                          aggfunc="first")
    wide = wide.reindex(columns=[f"h{h:02d}" for h in range(24)])
    feed = df.groupby("date").feed.first()
    wide.insert(0, "feed", feed)
    return wide.reset_index()


def to_daily(hourly):
    g = hourly.groupby(hourly.t.dt.strftime("%Y-%m-%d"))
    daily = pd.DataFrame({
        "hours_present": g.mm.size(),
        "mean_mm": g.mm.mean().round(1),
        "max_mm": g.mm.max(),
        "feed": g.feed.first(),
    })
    daily.index.name = "date"
    return daily.reset_index()


def load_or_fetch(cache_dir, log):
    """Read both feeds from the dropzone cache, fetching what is missing."""
    os.makedirs(cache_dir, exist_ok=True)
    frames = {}
    cached = [os.path.join(cache_dir, f) for f in sorted(os.listdir(cache_dir))
              if f.lower().endswith((".csv", ".dat", ".txt"))]
    for path in cached:
        text = open(path, errors="replace").read()
        df = parse_uhslc_hourly(text, os.path.basename(path))
        if df is None:
            continue
        # RQDS ends in 2021 by definition; a feed reaching the current or
        # previous year must be the FD file.
        kind = "fd" if df.t.dt.year.max() >= FD_FROM_YEAR else "rqds"
        if kind not in frames:
            frames[kind] = df
            log.append(f"cache: {os.path.basename(path)} used as {kind} feed, "
                       f"{df.t.min():%Y-%m-%d} to {df.t.max():%Y-%m-%d}")
    for kind, url in (("rqds", RQDS_URL), ("fd", FD_URL)):
        if kind in frames:
            continue
        name = os.path.basename(url)
        print(f"  fetching {kind} feed: {url}")
        with urllib.request.urlopen(url, timeout=300) as r:
            text = r.read().decode("utf-8", "replace")
        open(os.path.join(cache_dir, name), "w").write(text)
        df = parse_uhslc_hourly(text, name)
        if df is None or df.empty:
            raise SystemExit(f"Fetched {url} but could not parse it; aborting.")
        frames[kind] = df
        log.append(f"fetched {kind}: {url} "
                   f"({df.t.min():%Y-%m-%d} to {df.t.max():%Y-%m-%d})")
    return frames["rqds"], frames["fd"]


def main(source_dir=None, out_dir="data"):
    here = os.path.dirname(os.path.abspath(__file__))
    cache_dir = source_dir or os.path.join(here, "..", "dropzone", "high-water")
    log = []
    rqds, fd = load_or_fetch(cache_dir, log)
    rqds = qc(rqds, log, "rqds")
    fd = qc(fd, log, "fd")
    hourly = splice(rqds, fd, log)

    os.makedirs(out_dir, exist_ok=True)
    to_wide(hourly).to_csv(os.path.join(out_dir, "hourly_sea_level.csv"),
                           index=False)
    to_daily(hourly).to_csv(os.path.join(out_dir, "daily_sea_level.csv"),
                            index=False)
    today = datetime.date.today().isoformat()
    prov = [
        {"source": f"UHSLC RQDS hourly, {STATION}", "request_url": RQDS_URL,
         "span": f"{rqds.t.min():%Y-%m-%d} to {rqds.t.max():%Y-%m-%d}",
         "date_retrieved": today, "note": "; ".join(log)},
        {"source": f"UHSLC Fast Delivery hourly, {STATION}",
         "request_url": FD_URL,
         "span": f"{fd.t.min():%Y-%m-%d} to {fd.t.max():%Y-%m-%d}",
         "date_retrieved": today,
         "note": f"used from {FD_FROM_YEAR} onward only"},
    ]
    pd.DataFrame(prov).to_csv(os.path.join(out_dir, "source-library.csv"),
                              index=False)
    years = hourly.t.dt.year
    print(f"\nSpliced record: {len(hourly)} hours, "
          f"{years.min()}-{years.max()}")
    print(f"Wrote clean CSVs to {out_dir}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or [None]))
