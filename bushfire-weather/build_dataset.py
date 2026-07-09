"""build_dataset.py: turn the raw ERA5 (Open-Meteo) and GHCN downloads into
the clean daily fire-weather CSVs the analysis uses.

Inputs (in ../dropzone/bushfire-weather/, fetched by fetch_data.py):
  era5_<site>_<y0>_<y1>.json   Open-Meteo archive API responses: hourly
                               temperature_2m (C), relative_humidity_2m (%),
                               wind_speed_10m (km/h), precipitation (mm),
                               local time (Australia/Perth)
  ghcn_perth_airport.csv       GHCN-Daily TMAX/PRCP for station ASN00009021

Reduction to the daily FFDI inputs (the 15:00 convention):
  t15, rh15, wind15   the 15:00 local values (McArthur's observation time)
  rain24              the calendar day's precipitation total
  tmax                the day's maximum hourly temperature

Then the index chain from fire_indices.py: KBDI (mean annual rainfall taken
from the site's own record and written to the provenance log), Noble et al.
drought factor, and FFDI. The first year of each site is spin-up for the
KBDI recursion and is dropped.

Usage:  python3 build_dataset.py [source_dir] [out_dir]
"""
import json
import os
import sys

import numpy as np
import pandas as pd

import fire_indices as fi

SITES = {
    "perth_airport": "Perth Airport",
    "manjimup": "Manjimup",
    "merredin": "Merredin",
    "margaret_river": "Margaret River",
}


def load_site_hourly(source_dir, site):
    """Concatenate the decade JSON chunks into one hourly frame."""
    frames = []
    for f in sorted(os.listdir(source_dir)):
        if not (f.startswith(f"era5_{site}_") and f.endswith(".json")):
            continue
        j = json.load(open(os.path.join(source_dir, f)))
        h = j.get("hourly", {})
        if not h.get("time"):
            continue
        frames.append(pd.DataFrame({
            "time": pd.to_datetime(h["time"]),
            "t": h["temperature_2m"],
            "rh": h["relative_humidity_2m"],
            "wind": h["wind_speed_10m"],
            "rain": h["precipitation"],
        }))
    if not frames:
        return None
    out = (pd.concat(frames, ignore_index=True)
           .drop_duplicates(subset="time")
           .sort_values("time").reset_index(drop=True))
    return out


def reduce_daily(hourly):
    """Hourly local-time frame -> daily FFDI inputs."""
    h = hourly.copy()
    h["date"] = h.time.dt.normalize()
    h["hour"] = h.time.dt.hour
    at15 = h[h.hour == 15].set_index("date")
    day = h.groupby("date").agg(
        rain24=("rain", "sum"), tmax=("t", "max"), n_hours=("t", "size"))
    day["t15"] = at15["t"]
    day["rh15"] = at15["rh"]
    day["wind15"] = at15["wind"]
    day = day.reset_index()
    # keep only days with a full-enough record and a 15:00 observation
    day = day[(day.n_hours >= 20) & day.t15.notna()
              & day.rh15.notna() & day.wind15.notna()].copy()
    return day


def parse_ghcn(path):
    df = pd.read_csv(path)
    df.columns = [c.strip().upper() for c in df.columns]
    if not {"DATE", "TMAX"} <= set(df.columns):
        return None
    name = str(df.get("NAME", pd.Series(["?"])).iloc[0])
    out = pd.DataFrame({
        "date": pd.to_datetime(df.DATE, errors="coerce"),
        "tmax_obs": pd.to_numeric(df.TMAX, errors="coerce"),
        "prcp_obs": pd.to_numeric(df.get("PRCP"), errors="coerce"),
    }).dropna(subset=["date"])
    out.attrs["station_name"] = name
    return out


def main(source_dir=None, out_dir="data"):
    here = os.path.dirname(os.path.abspath(__file__))
    source_dir = source_dir or os.path.join(here, "..", "dropzone",
                                            "bushfire-weather")
    if not os.path.isdir(source_dir):
        print(__doc__)
        raise SystemExit("No dropzone/bushfire-weather/; run fetch_data.py "
                         "first (see dropzone/DROP_FILES_HERE.md).")
    os.makedirs(out_dir, exist_ok=True)
    provenance = []
    for site, label in SITES.items():
        hourly = load_site_hourly(source_dir, site)
        if hourly is None:
            raise SystemExit(f"No ERA5 chunks for {site}; run fetch_data.py.")
        day = reduce_daily(hourly)
        # KBDI parameter: the site's own mean annual rainfall (complete years)
        yr = day.assign(year=day.date.dt.year).groupby("year").agg(
            rain=("rain24", "sum"), n=("rain24", "size"))
        mar = float(yr[yr.n >= 360].rain.mean())
        day = day.sort_values("date").reset_index(drop=True)
        day["kbdi"] = fi.kbdi_series(day.tmax.values, day.rain24.values, mar)
        day["df"] = fi.drought_factor_series(day.kbdi.values, day.rain24.values)
        day["ffdi"] = fi.ffdi(day.df.values, day.t15.values,
                              day.rh15.values, day.wind15.values)
        first_year = int(day.date.dt.year.min())
        day = day[day.date.dt.year > first_year]        # KBDI spin-up
        cols = ["date", "t15", "rh15", "wind15", "rain24", "tmax",
                "kbdi", "df", "ffdi"]
        num = [c for c in cols if c != "date"]
        day[num] = day[num].round(3)
        day[cols].to_csv(
            os.path.join(out_dir, f"fire_weather_daily_{site}.csv"),
            index=False)
        provenance.append({
            "site": site, "label": label,
            "source": "ERA5 via Open-Meteo archive API (hourly, local time)",
            "first": str(day.date.min().date()),
            "last": str(day.date.max().date()),
            "n_days": len(day), "mean_annual_rain_mm": round(mar, 1),
            "spin_up_year_dropped": first_year,
        })
        print(f"  {label}: {day.date.min().date()} to {day.date.max().date()}"
              f" ({len(day)} days, MAR {mar:.0f} mm)")

    ghcn_path = os.path.join(source_dir, "ghcn_perth_airport.csv")
    if os.path.exists(ghcn_path):
        obs = parse_ghcn(ghcn_path)
        if obs is not None:
            name = obs.attrs["station_name"]
            if "PERTH" not in name.upper():
                raise SystemExit(f"GHCN station name check failed: {name}")
            obs.to_csv(os.path.join(out_dir, "ghcn_perth_airport_daily.csv"),
                       index=False)
            provenance.append({
                "site": "perth_airport", "label": name,
                "source": "GHCN-Daily ASN00009021 via NCEI data service",
                "first": str(obs.date.min().date()),
                "last": str(obs.date.max().date()),
                "n_days": len(obs), "mean_annual_rain_mm": "",
                "spin_up_year_dropped": "",
            })
            print(f"  GHCN cross-check: {name} ({len(obs)} days)")
    pd.DataFrame(provenance).to_csv(
        os.path.join(out_dir, "source-library.csv"), index=False)
    print(f"\nWrote clean CSVs to {out_dir}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or [None]))
