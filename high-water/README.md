# Acute Physical Climate Risk: Coastal Flood Hours at Fremantle (1984-2026)

A data analysis written for **AASB S2 physical-risk assessment** (AASB S2 is
Australia's mandatory climate-disclosure standard). The suite's `sea-level/`
project measured the chronic story at Fremantle: the mean is rising. This
project measures the acute one: how often the water now reaches levels that
were rare in the 1980s, using the hourly record from the same gauge, and how
much of that change is the higher mean sea level itself rather than any
change in the storms and tides riding on it.

> **In one paragraph.** Fremantle's sea spent about **43 hours a year at or
> above 1350 mm** (the 99.5th percentile of the 1984-1993 baseline) in that
> baseline decade. In the last ten complete years (2013-2023) it spent
> **125 hours a year** there, nearly three times as often, and the trend in
> those hours is significant (Sen's slope **+2.2 hours per year each year**,
> Mann-Kendall p = 0.008). The cause is not stormier weather: re-count the
> same hours with each year's mean anomaly removed and the series is flat
> (p = 0.39), at roughly 21-30 hours a year across the whole record. The
> increase is the baseline itself, which lifted about **128 mm** between the
> two decades, part long-run rise and part the La Nina highs of 2011 and
> 2021-2023. That is the textbook mechanism AASB S2 preparers with coastal
> assets need to disclose: the same storms on a higher sea clear the same
> fixed threshold far more often, and every fixed asset is a fixed threshold.

## Results

Computed by `analysis.py` on the spliced hourly record (research-quality
1984-2021, fast-delivery 2022 on), complete years only: 38 of the 43
calendar years the record touches (1991, 2020, 2024 and 2025 fail the
completeness rule; 2026 is in progress). Benchmarks were fixed as
percentiles of the 1984-1993 baseline hours before any trend was computed.

**The benchmarks** (mm above the UHSLC station zero):

| Benchmark | Definition | Level |
|---|---|---|
| b1 | 99.0th percentile of 1984-1993 hours | 1280 mm |
| b2 (headline) | 99.5th percentile of 1984-1993 hours | 1350 mm |
| b3 | 99.9th percentile of 1984-1993 hours | 1480 mm |

**Then vs now** (hours per year at or above each benchmark, decade average):

| Epoch | Complete years | Mean level | >= b1 | >= b2 | >= b3 | Days with any hour >= b2 |
|---|---|---|---|---|---|---|
| 1984-1993 | 9 | 717 mm | 92 | 43 | 11 | 11 |
| 2013-2023 | 10 | 845 mm | 260 | 125 | 33 | 30 |

**Trends across the 38 complete years** (Mann-Kendall + Sen's slope from the
suite's tested `stats_utils.py`, OLS as the parametric cross-check):

| Series | Sen's slope | MK p | Verdict |
|---|---|---|---|
| Hours >= b2 | +2.21 hrs/yr each year | 0.008 | increasing |
| Days >= b2 | +0.53 days/yr each year | 0.004 | increasing |
| **Mean-adjusted hours >= b2** | **-0.21 hrs/yr each year** | **0.39** | **no trend** |
| Annual mean level | +4.53 mm/yr | 8e-6 | increasing |
| Annual max hourly level | +5.00 mm/yr | 0.001 | increasing |
| Annual 99.9th percentile | +3.56 mm/yr | 0.015 | increasing |

The middle row is the finding. Remove each year's mean anomaly and re-count,
and the "storminess" component of high water has no trend at all: the
1984-1993 years re-count to about 30 hours a year and the 2013-2023 years to
about 21. Everything the raw series gained came from the higher mean level.
The annual maximum rose at the same pace as the mean (about 5 mm/yr), which
is exactly what a lifted baseline with unchanged storms looks like.

Charts: `charts/01_highwater_hours.png` (the headline series),
`charts/02_baseline_lift.png` (extremes riding the mean),
`charts/03_same_storms.png` (raw vs adjusted, decade by decade),
`charts/04_distribution_shift.png` (hours per year above every level, then
vs now), `charts/05_flood_calendar.png` (month-by-year timing).

## Research question

How many hours per year does the sea at Fremantle reach levels that were
rare (99.0th, 99.5th, 99.9th percentile) in the first decade of the hourly
record, how has that changed, and how much of the change survives when each
year's mean sea-level anomaly is removed?

## Data

| Source | What it provides | Used for |
|--------|------------------|----------|
| **UHSLC Research Quality Data Set, hourly, station 175a (Fremantle)** | Quality-controlled hourly sea level, 1984-2021, mm above station zero | The record through 2021 |
| **UHSLC Fast Delivery, hourly, station 175 (Fremantle)** | Near-real-time hourly sea level, 1984 to the present | 2022 onward only, flagged as fast-delivery everywhere |
| **PSMSL monthly RLR, station 111 (Fremantle)** | The independent monthly record already used by `sea-level/` | Validation of annual means |

The two UHSLC feeds carry the same gauge: over their 330,893 shared hours
the values are 100.0% byte-identical, so the splice point (1 January 2022)
is a change of quality-control status, not of instrument. Both feeds are
keyless, script-friendly downloads; `build_dataset.py` fetches them itself
(the raw downloads are cached in `../dropzone/high-water/`, gitignored) and
the committed `data/hourly_sea_level.csv` carries the full cleaned hourly
record, so every number here can be recomputed from the repo alone.

**Datum.** Levels are millimetres above the **UHSLC station zero**, which is
neither Chart Datum nor AHD, and no conversion is attempted. Comparisons are
therefore internal to the record: percentiles of it, changes within it. The
gauge measures **relative** sea level; vertical land motion is in the number
and is not corrected for (same caveat as `sea-level/`).

**Definitions.** Times are UTC per the UHSLC convention, so days are UTC
days. Missing values (-32767) are dropped, never interpolated. Readings
outside 0-2500 mm are dropped (24 of 693,529 raw hours); no flatlined runs
were found. A year is **complete** only if at least 80% of its hours are
present and every calendar month has at least half of its hours, so a
missing storm month cannot bias a count low; 1991 (a nearly empty April),
2020 (a thin December), 2024 and 2025 (long outages) are excluded by this
rule. A year's **anomaly** is its mean minus the 1984-1993 baseline mean
(715.3 mm over 86,687 hours); **adjusted** counts re-count the year's hours
with that anomaly subtracted.

## Method

1. `build_dataset.py` fetches both UHSLC feeds (or reads them from the
   dropzone cache), screens them, splices research-quality through 2021
   with fast-delivery from 2022, and writes the committed hourly and daily
   CSVs plus a provenance log with every request URL and retrieval date.
2. `analysis.py` fixes the three benchmarks from the baseline decade,
   applies the completeness rule, computes per-year raw and mean-adjusted
   exceedance hours, runs Mann-Kendall, Sen's slope and OLS on the annual
   series (full record and 1993 on), compares epochs including like-phase
   windows one 18.61-year nodal cycle apart, and validates annual means
   against the PSMSL record.
3. `viz.py` draws the five charts.

The splice, screens, completeness rule, benchmark percentiles and both
counting modes are unit-tested in `test_project.py` against synthetic
records with hand-computable answers; the shared statistics are validated
in `test_stats.py`. Both run in CI.

## Validation

1. **Against the independent PSMSL record: passes.** Annual means computed
   from the hourly series track the PSMSL RLR annual means at r = 0.9989
   over the 37 overlapping complete years, with a constant offset of
   5999.3 mm (the RLR-vs-station-zero datum gap) and a spread of only
   3.7 mm around it.
2. **Against documented storms: passes.** The record's highest hours fall
   on known severe-storm dates: the 15-16 May 2003 front (1947 mm, the
   record), the 10 June 2012 winter storm (1938 mm), and 25 May 2020, when
   the remnants of Tropical Cyclone Mangga merged with a cold front
   (1891 mm).
3. **Against the sibling project: passes.** The annual-mean trend here
   (+4.5 mm/yr over 1984-2023, +5.5 mm/yr from 1993) matches the
   `sea-level/` finding of a fast altimetry era (+5.1 mm/yr from 1993) on
   the same gauge's independent monthly record.
4. **Against the nodal cycle: passes.** The like-phase window one 18.61-year
   cycle after the baseline (2003-2012) already shows 109 hours a year over
   b2, so the increase is not an artefact of tidal modulation.

## Limitations (write-up must keep these)

- **An exceedance is not a certified flood.** These are statistical
  benchmarks on a gauge, not mapped inundation of anybody's property. The
  project counts "high-water hours"; whether 1350 mm on this datum tops a
  given wharf or road needs a local survey this project does not have.
- **The last decade is partly La Nina.** The 2011 and 2021-2023 anomalies
  (+210 to +235 mm) are ENSO/Leeuwin Current highs on top of the long-run
  rise, and 2022 alone logged 355 raw hours over b2. The adjusted counts
  strip the year-mean effect whatever its cause; the raw counts are what
  assets actually experienced. Both are reported, and neither is "the"
  climate trend on its own.
- **Fast-delivery years (2022 on) are not final.** They are flagged in the
  data and charts and will be replaced when the research-quality file
  extends.
- **Hourly values smooth the peaks.** Fremantle sees seiches on scales of
  minutes; instantaneous maxima ran higher than any number here.
- **Relative sea level, station datum.** No vertical-land-motion correction
  and no conversion to AHD or Chart Datum.
- **UTC days.** Day and month attribution can differ from local time by up
  to eight hours; annual statistics are unaffected.

## Reproduce

```bash
pip install -r requirements.txt
# needs uhslc.soest.hawaii.edu reachable (tools/check-data-access.sh), or
# stage the two hourly CSVs in ../dropzone/high-water/ first; then:
python3 build_dataset.py
python3 analysis.py
python3 viz.py
python3 test_stats.py && python3 test_project.py
```

## Update log

**16 Jul 2026 · First published.** Planned as the suite's twelfth project
(acute physical risk) with data access verified from the build environment
before a line of pipeline code was written. The build amended one planning
decision: the full cleaned hourly record is committed (as a compact one row
per day, 24 columns CSV) rather than only a daily reduction, because the
exceedance counts cannot be recomputed from daily summaries and the suite's
rule is that every published number must be reproducible from committed
data. First results: high-water hours at the fixed 1984-1993 benchmarks
nearly tripled by 2013-2023, the trend is significant, and the entire
increase is accounted for by the higher mean level; the storminess
component, isolated by mean-adjusted re-counting, shows no trend at all.
