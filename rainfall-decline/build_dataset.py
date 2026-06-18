"""
build_dataset.py — turn raw GHCN-Daily + climate-index downloads into the clean
CSVs the analysis uses.

Data provenance
---------------
Station rainfall: GHCN-Daily (NOAA NCEI). The Australian (ASN*) records in
GHCN-Daily ARE the Bureau of Meteorology's station observations, redistributed
by NOAA in a script-friendly fixed-width format. Using them keeps the whole
pipeline reproducible without manual web navigation; results are validated
against BOM/CSIRO published figures in the README.

Six long-record South West Land Division (SWLD) stations spanning the rainfall
gradient (wet SW/coast -> Perth Hills catchment -> dry interior wheatbelt).

Driver indices: NOAA PSL (DMI for the Indian Ocean Dipole; Nino 3.4 anomaly for
ENSO) and the Marshall (2003) station-based Southern Annular Mode index (BAS).

Definitions
-----------
Cool season   = April-October totals (BOM's standard SW WA cool/wet season).
Sub-season    = May-July (where the decline signal is strongest).
Baseline      = 1950-1974 mean (pre-step-change reference).
Anomaly       = each station vs its OWN baseline, in mm and %. The regional
                series is the mean of the per-station anomalies, so wet coastal
                stations don't dominate the dry inland ones.
"""
import calendar
import os
import numpy as np
import pandas as pd

RAW = os.path.join("data", "raw")
OUT = "data"

# Seven SWLD stations chosen for GENUINE full daily coverage 1950-2024 (>=22 of
# 25 baseline years, >=22 recent), spanning the rainfall gradient. Perth
# Darling-scarp catchment stations (Mundaring, Jarrahdale) were excluded because
# their GHCN-Daily *daily* coverage is too gappy; the high-rainfall SW-corner
# stations (Cape Leeuwin, Deeside, Westbourne) carry the same forced signal.
STATIONS = {
    "ASN00009518": "Cape Leeuwin",  # far SW tip, coastal (wettest)
    "ASN00009530": "Deeside",       # SW forest, high-rainfall zone
    "ASN00009616": "Westbourne",    # SW forest (Manjimup region)
    "ASN00009500": "Albany",        # south coast
    "ASN00010614": "Narrogin",      # central wheatbelt
    "ASN00010647": "Wagin",         # southern wheatbelt
    "ASN00010111": "Northam",       # northern Avon valley wheatbelt (driest)
}

COOL_MONTHS = list(range(4, 11))   # Apr..Oct
MJJ_MONTHS = [5, 6, 7]
BASE_START, BASE_END = 1950, 1974
YEAR_MIN, YEAR_MAX = 1950, 2024
MAX_MISSING_DAYS = 3               # per month; more than this -> month invalid
MIN_BASE_YEARS = 15               # need this many valid baseline years per station
MIN_STATIONS_PER_YEAR = 5          # of 7; else regional value for that year is NaN


# ---------------------------------------------------------------------------
# GHCN-Daily .dly parsing
# ---------------------------------------------------------------------------

def parse_dly_prcp(path):
    """Return {(year, month): monthly_total_mm} for months with adequate daily
    coverage (<= MAX_MISSING_DAYS missing/failed days). Daily PRCP is tenths of
    mm; -9999 is missing; a non-blank QFLAG means the value failed QC."""
    monthly = {}
    with open(path) as fh:
        for line in fh:
            if line[17:21] != "PRCP":
                continue
            year = int(line[11:15])
            month = int(line[15:17])
            if not (YEAR_MIN <= year <= YEAR_MAX):
                continue
            ndays = calendar.monthrange(year, month)[1]
            total = 0.0
            valid = 0
            for d in range(ndays):
                base = 21 + d * 8
                raw = line[base:base + 5]
                qflag = line[base + 6]
                try:
                    v = int(raw)
                except ValueError:
                    v = -9999
                if v == -9999 or qflag != " ":
                    continue
                total += v / 10.0
                valid += 1
            if (ndays - valid) <= MAX_MISSING_DAYS:
                monthly[(year, month)] = total
    return monthly


def season_total(monthly, year, months):
    """Sum the listed months for a year; NaN if any month is missing/invalid."""
    vals = [monthly.get((year, m)) for m in months]
    if any(v is None for v in vals):
        return np.nan
    return float(sum(vals))


# ---------------------------------------------------------------------------
# Build station + regional rainfall tables
# ---------------------------------------------------------------------------

def build_rainfall():
    rows = []
    for sid, name in STATIONS.items():
        monthly = parse_dly_prcp(os.path.join(RAW, sid + ".dly"))
        for year in range(YEAR_MIN, YEAR_MAX + 1):
            rows.append({
                "station_id": sid,
                "station": name,
                "year": year,
                "cool_mm": season_total(monthly, year, COOL_MONTHS),
                "mjj_mm": season_total(monthly, year, MJJ_MONTHS),
            })
    df = pd.DataFrame(rows)

    # per-station baseline + anomalies
    base = (df[(df.year >= BASE_START) & (df.year <= BASE_END)]
            .groupby("station")["cool_mm"].agg(["mean", "count"]))
    baselines, dropped = {}, []
    for st, r in base.iterrows():
        if r["count"] >= MIN_BASE_YEARS:
            baselines[st] = r["mean"]
        else:
            dropped.append((st, int(r["count"])))
    if dropped:
        print("  WARNING dropped (too few baseline years):", dropped)

    df = df[df.station.isin(baselines)].copy()
    df["baseline_mm"] = df.station.map(baselines)
    df["cool_anom_mm"] = df.cool_mm - df.baseline_mm
    df["cool_anom_pct"] = 100.0 * df.cool_anom_mm / df.baseline_mm
    df.to_csv(os.path.join(OUT, "rainfall_swwa_clean.csv"), index=False)

    # regional series: mean of per-station anomalies; require >= MIN_STATIONS
    g = df.dropna(subset=["cool_mm"]).groupby("year")
    reg = pd.DataFrame({
        "regional_cool_mm": g["cool_mm"].mean(),
        "regional_anom_pct": g["cool_anom_pct"].mean(),
        "regional_anom_mm": g["cool_anom_mm"].mean(),
        "n_stations": g["cool_mm"].count(),
    }).reset_index()
    reg = reg[reg.n_stations >= MIN_STATIONS_PER_YEAR].reset_index(drop=True)
    reg.to_csv(os.path.join(OUT, "annual_cool_season_anomaly.csv"), index=False)

    print(f"  stations kept: {sorted(baselines)}")
    print("  per-station 1950-1974 cool-season baseline (mm):")
    for st in sorted(baselines):
        print(f"    {st:<11} {baselines[st]:6.1f} mm")
    print(f"  regional series years: {reg.year.min()}-{reg.year.max()} "
          f"({len(reg)} yrs)")
    return df, reg


# ---------------------------------------------------------------------------
# Climate-index parsing (year + 12 monthly columns, text footer ignored)
# ---------------------------------------------------------------------------

def parse_monthly_index(path, missing_at_or_below=-99.0):
    """Parse 'YEAR v1..v12' tables (NOAA PSL / Marshall). Returns DataFrame
    [year, month, value]. Footer/header text lines are skipped; values
    <= missing_at_or_below (e.g. -9999, -99.99) are treated as missing."""
    recs = []
    for line in open(path):
        parts = line.split()
        if len(parts) < 2:
            continue
        try:
            year = int(parts[0])
        except ValueError:
            continue
        if not (1800 <= year <= 2100):
            continue
        for m, tok in enumerate(parts[1:13], start=1):
            try:
                v = float(tok)
            except ValueError:
                continue
            if v <= missing_at_or_below or v >= 9999:
                continue
            recs.append((year, m, v))
    return pd.DataFrame(recs, columns=["year", "month", "value"])


def cool_season_mean(idx):
    sub = idx[idx.month.isin(COOL_MONTHS)]
    g = sub.groupby("year")["value"].agg(["mean", "count"])
    g = g[g["count"] == len(COOL_MONTHS)]      # require all 7 months present
    return g["mean"]


def build_drivers():
    dmi = parse_monthly_index(os.path.join(RAW, "dmi.had.long.data"))
    sam = parse_monthly_index(os.path.join(RAW, "marshall.sam.txt"))
    nino = parse_monthly_index(os.path.join(RAW, "nina34.anom.data"))
    out = pd.DataFrame({"year": range(YEAR_MIN, YEAR_MAX + 1)}).set_index("year")
    out["dmi_AprOct"] = cool_season_mean(dmi)        # Indian Ocean Dipole
    out["sam_AprOct"] = cool_season_mean(sam)        # Southern Annular Mode
    out["nino34_AprOct"] = cool_season_mean(nino)    # ENSO
    out = out.reset_index()
    out.to_csv(os.path.join(OUT, "drivers.csv"), index=False)
    print(f"  drivers: DMI {dmi.year.min()}-{dmi.year.max()}, "
          f"SAM {sam.year.min()}-{sam.year.max()}, "
          f"Nino3.4 {nino.year.min()}-{nino.year.max()}")
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("Building rainfall tables...")
    build_rainfall()
    print("Building driver indices...")
    build_drivers()
    print("Done. Wrote data/rainfall_swwa_clean.csv, "
          "annual_cool_season_anomaly.csv, drivers.csv")
