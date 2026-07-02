# Acute Physical Climate Risk: Extreme Heat in Perth and the Pilbara

A data analysis written for **AASB S2 physical-risk assessment** (AASB S2 is
Australia's mandatory climate-disclosure standard). Where the cyclone project
covered storms and the rainfall project covered drying, this one measures the
heat: how often Perth and the Pilbara now hit 35 C and 40 C, how hot the
hottest day of the year has become, and whether multi-day heatwaves are
getting more frequent.

> **In one paragraph.** Both cities are heating, and the Pilbara is heating
> faster. At **Perth Airport** (1945-2025), days at or above 35 C are
> rising by about **2.3 per decade** (Mann-Kendall p = 1.6e-07): from
> roughly 24 such days a year in the 1950s-60s to 36 in the 2010s and 43
> in the 2020s so far. The hottest day of the year has climbed about
> **0.27 C per decade** (from ~41.5 C to ~43.5 C), and multi-day heatwave
> events have gone from about 3 to 8-9 a year. At **Port Hedland**
> (1950-2025), 35 C days are rising **twice as fast, about 4.8 per decade**
> (p = 8e-05): the town has gone from about 133 such days a year
> mid-century to about 163 in the 2020s, more than five months of the year,
> and days spent inside heatwaves have more than doubled (14 to ~37 a
> year). The one metric that does not clear the significance bar is Port
> Hedland's count of 40 C days (Sen +1.0/decade but p = 0.09; it already
> averages ~30-36 such days a year, so the year-to-year noise is large).
> For the iron-ore and LNG workforce this is an occupational heat-stress
> trend; for Perth it is a health and energy-demand trend. The Perth record
> was supplied through two independent portals (BoM Climate Data Online and
> GHCN-Daily), and every Perth trend agrees across the two within a few
> percent, which is the built-in proof the pipeline reads the data
> faithfully.

## Results

Computed by `analysis.py` over complete years only. Perth = BoM CDO record
(1945-2025), with the GHCN copy in brackets as the cross-portal check;
Port Hedland = GHCN record (1950-2025). Sen's slope per decade with
Mann-Kendall p (prewhitened p agreed in every case):

| Metric | Perth Airport | Port Hedland |
|---|---|---|
| Days at or above 35 C | **+2.31** (+2.42), p = 1.6e-07 | **+4.79**, p = 8.2e-05 |
| Days at or above 40 C | **+0.39** (+0.32), p = 0.002 | +1.03, p = 0.09 (not significant) |
| Hottest day of the year, TXx | **+0.27 C** (+0.25 C), p = 0.0005 | **+0.17 C**, p = 0.046 |
| Heatwave events (3+ days above day-of-year p90) | **+0.61** (+0.67), p = 2.6e-06 | **+0.61**, p = 6.8e-05 |
| Days inside heatwaves | **+2.59** (+2.86), p = 4.9e-07 | **+3.33**, p = 2.3e-05 |

Decade means (from `data/decade_summary.csv`):

| | 1950s-60s | 2010s | 2020s so far |
|---|---|---|---|
| Perth: days at or above 35 C | ~24 | 36 | 43 |
| Perth: heatwave events | ~3 | 7.2 | 8.7 |
| Port Hedland: days at or above 35 C | ~133 | 158 | 163 |
| Port Hedland: days inside heatwaves | ~15 | 34 | 37 |

## Research question

Have hot days (35 C+), very hot days (40 C+), the annual maximum temperature
(TXx), and multi-day heatwave frequency increased significantly at Perth
Airport and Port Hedland? The two stations are chosen as the population
centre and the industrial north: the contrast matters because Pilbara heat
is an occupational-safety and productivity issue for the iron-ore and LNG
workforces, while Perth heat is a health and energy-demand issue.

## Data

| Source | What it provides | Used for |
|--------|------------------|----------|
| **GHCN-Daily** (NOAA NCEI) | Daily TMAX/TMIN; the Australian (`ASN*`) records are the Bureau of Meteorology's observations redistributed in a script-friendly format | Station daily series from 1950 |
| **BoM Climate Data Online** (optional) | The same observations from the BoM's own portal | Accepted by the parser as a cross-check or substitute |

The `--fetch` mode validates the station NAME returned by NOAA against the
expected name (Perth Airport, Port Hedland), so a mistyped station id cannot
silently produce the wrong city's climate. Additional stations dropped into
the dropzone are analysed too; the code is not hard-wired to two.

**Definitions.** Hot day = TMAX at or above 35 C; very hot day = 40 C; TXx =
hottest day of the calendar year. Heatwave = 3 or more consecutive days at
or above that calendar day's 90th percentile, computed in a 15-day window
over the 1961-1990 baseline (falling back to the full record, and saying so,
where a station cannot cover 20 baseline years). A year is kept only if 18
or fewer TMAX days are missing; missing days conservatively break heatwave
runs rather than bridging them. GHCN files arriving in tenths of a degree
are detected (median TMAX above 80) and converted, and the provenance log
records every conversion.

## Method

1. `build_dataset.py` fetches or ingests the daily series, merges duplicate
   dates, computes the day-of-year percentile thresholds, and writes the
   per-year metrics with completeness accounting.
2. `analysis.py` runs Mann-Kendall (plain and prewhitened), Sen's slope and
   OLS on each station's metrics over complete years only, plus decadal
   means. Count metrics are skewed, so the non-parametric pair is the
   headline test; OLS is reported for scale.
3. `viz.py` draws per-station panels for hot days, TXx and heatwave events,
   plus a decade-by-decade comparison.

Statistics are the suite's shared `stats_utils.py` (byte-identical across
projects, validated in `test_stats.py`). The heat-specific pieces (tenths
heuristic, both parsers, percentile thresholds, run detection, completeness)
are tested with synthetic inputs in `test_project.py`. Both run in CI.

## Validation

1. **Cross-portal agreement (the strongest check).** The same Perth Airport
   observations arrived via two independent archives (BoM CDO and NOAA
   GHCN-Daily), were parsed by two different code paths, and every trend
   agrees within a few percent. A parsing or units error would show up
   here first.
2. **Consistency with the literature.** Rising extreme-heat frequency in
   both cities matches CSIRO / BoM State of the Climate statements, and
   the levels are plausible against known station climate (Perth ~30-40
   days at or above 35 C in recent years; Port Hedland among Australia's
   hottest sites with its TXx records near 49 C, the maximum in this
   dataset).
3. **No unit conversions fired.** Both GHCN files arrived in degrees C, so
   the tenths-of-a-degree heuristic never triggered (the provenance log
   confirms), removing that class of error entirely.

## Limitations (write-up must keep these)

- Two stations are two points, not a field; the Pilbara especially has
  sharp coastal-inland gradients.
- Station moves and instrument changes can shift extremes; GHCN carries the
  BoM's quality flags but this analysis does not re-homogenise the record.
  Cross-checking against BoM's homogenised ACORN-SAT statements belongs in
  the write-up.
- The heatwave definition is percentile-based and station-relative; it is
  not the BoM's operational EHF severity product, and the write-up should
  not compare event counts across definitions.

## Reproduce

```bash
pip install -r requirements.txt
python3 build_dataset.py --fetch      # on a networked machine, or:
#   drop GHCN/BoM daily CSVs into ../dropzone/extreme-heat/ and run without --fetch
python3 analysis.py
python3 viz.py
python3 test_stats.py && python3 test_project.py
```
