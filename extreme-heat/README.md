# Acute Physical Climate Risk: Extreme Heat in Perth and the Pilbara

A data analysis written for **AASB S2 physical-risk assessment** (AASB S2 is
Australia's mandatory climate-disclosure standard). Where the cyclone project
covered storms and the rainfall project covered drying, this one measures the
heat: how often Perth and the Pilbara now hit 35 C and 40 C, how hot the
hottest day of the year has become, and whether multi-day heatwaves are
getting more frequent.

> **Status: pipeline complete, awaiting the data drop (or a networked
> --fetch run).** Every number in this README will be computed by
> `analysis.py`. Nothing is pre-filled; see
> [dropzone/DROP_FILES_HERE.md](../dropzone/DROP_FILES_HERE.md), or run
> `python3 build_dataset.py --fetch` on a machine that can reach NOAA.

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

## Validation plan

1. Recent-decade hot-day counts should match the values BoM publishes for
   Perth Airport and Port Hedland in its climate statistics pages.
2. The Perth trend should be consistent in direction with CSIRO / BoM State
   of the Climate statements on increasing extreme heat.
3. Any tenths-conversion events in the provenance log must be checked by
   eye against a few known dates before the results are trusted.

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
#   drop GHCN/BoM daily CSVs into ../dropzone/ and run without --fetch
python3 analysis.py
python3 viz.py
python3 test_stats.py && python3 test_project.py
```
