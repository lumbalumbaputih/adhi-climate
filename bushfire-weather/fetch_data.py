"""fetch_data.py: download the raw inputs for the bushfire-weather project
into ../dropzone/bushfire-weather/ (gitignored), where build_dataset.py reads
them. Run from inside bushfire-weather/. Re-runs skip anything already cached.

Sources (both keyless, both verified reachable from the remote session):
  - Open-Meteo Historical Weather API (ERA5 reanalysis): hourly temperature,
    relative humidity, 10 m wind speed and precipitation for the four study
    sites, 1940 to the present, local time (Australia/Perth).
  - NOAA NCEI GHCN-Daily (station ASN00009021, Perth Airport): daily TMAX and
    PRCP, used only to validate ERA5 against an observed record.

Usage:  python3 fetch_data.py
"""
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DROP = os.path.join(HERE, "..", "dropzone", "bushfire-weather")

SITES = {
    "perth_airport":  ("Perth Airport",  -31.9275, 115.9764),
    "manjimup":       ("Manjimup",       -34.2410, 116.1456),
    "merredin":       ("Merredin",       -31.4820, 118.2790),
    "margaret_river": ("Margaret River", -33.9550, 115.0750),
}
CHUNKS = [(1940, 1949), (1950, 1959), (1960, 1969), (1970, 1979),
          (1980, 1989), (1990, 1999), (2000, 2009), (2010, 2019),
          (2020, 2026)]
ERA5 = ("https://archive-api.open-meteo.com/v1/archive?latitude={lat}"
        "&longitude={lon}&start_date={d0}&end_date={d1}"
        "&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,"
        "precipitation&timezone=Australia%2FPerth")
GHCN = ("https://www.ncei.noaa.gov/access/services/data/v1?dataset="
        "daily-summaries&stations=ASN00009021&startDate=1944-01-01"
        "&endDate=2026-06-30&dataTypes=TMAX,PRCP&format=csv"
        "&includeStationName=true&units=metric")


def get(url, timeout=300):
    req = urllib.request.Request(url, headers={"User-Agent": "adhi-climate/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_era5(site, y0, y1):
    out = os.path.join(DROP, f"era5_{site}_{y0}_{y1}.json")
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        return "cached"
    _, lat, lon = SITES[site]
    d1 = f"{y1}-12-31" if y1 < 2026 else "2026-06-30"
    url = ERA5.format(lat=lat, lon=lon, d0=f"{y0}-01-01", d1=d1)
    for attempt in range(1, 7):
        try:
            raw = get(url)
            j = json.loads(raw)
            n = len(j.get("hourly", {}).get("time", []))
            if n < 24:
                raise ValueError("empty hourly payload")
            tmp = out + ".part"
            with open(tmp, "wb") as f:
                f.write(raw)
            os.replace(tmp, out)
            return f"{n} hours"
        except Exception as e:
            err = str(e)[:100]
            time.sleep(6 * attempt)      # polite backoff, covers 429s
    return f"FAILED: {err}"


def fetch_ghcn():
    out = os.path.join(DROP, "ghcn_perth_airport.csv")
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        return "cached"
    for attempt in range(1, 6):
        try:
            raw = get(GHCN)
            head = raw[:200].decode(errors="replace").upper()
            if "DATE" not in head:
                raise ValueError("unexpected response")
            tmp = out + ".part"
            with open(tmp, "wb") as f:
                f.write(raw)
            os.replace(tmp, out)
            nl = raw.count(b"\n")
            return f"{nl} lines"
        except Exception as e:
            err = str(e)[:100]
            time.sleep(5 * attempt)
    return f"FAILED: {err}"


def main():
    os.makedirs(DROP, exist_ok=True)
    print(f"GHCN Perth Airport: {fetch_ghcn()}", flush=True)
    for site in SITES:
        for y0, y1 in CHUNKS:
            r = fetch_era5(site, y0, y1)
            print(f"{site} {y0}-{y1}: {r}", flush=True)
            if r != "cached":
                time.sleep(1.5)          # stay well inside the free rate limit
    print("FETCH-DONE")


if __name__ == "__main__":
    main()
