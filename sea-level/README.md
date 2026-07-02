# Chronic Physical Climate Risk: Sea-Level Rise at Fremantle (1897-present)

A data analysis written for **AASB S2 physical-risk assessment** (AASB S2 is
Australia's mandatory climate-disclosure standard). The Fremantle tide gauge
is one of the longest sea-level records in the Southern Hemisphere, running
since 1897, which makes it the single best place in Australia to ask the two
questions that matter for coastal assets: how fast is the sea rising here,
and is the rise speeding up?

> **Status: pipeline complete, awaiting the data drop.** Every number in
> this README will be computed by `analysis.py` from the file described in
> [dropzone/DROP_FILES_HERE.md](../dropzone/DROP_FILES_HERE.md). Nothing is
> pre-filled.

## Research question

What is the long-run rate of relative sea-level rise at Fremantle, how does
the satellite-altimetry era (1993 onward) compare with the earlier record,
and does a quadratic fit detect statistically significant acceleration?

## Data

| Source | What it provides | Used for |
|--------|------------------|----------|
| **PSMSL monthly RLR, station 111 (Fremantle)** | Monthly mean sea level from 1897 on the Revised Local Reference datum, the international research-grade tide-gauge standard | The entire analysis |

The RLR datum sits roughly 7 m below typical sea level so heights stay
positive; the level is arbitrary, so results are reported as **rates**
(mm/yr) and as anomalies against the station's 1990-2009 mean.

**Definitions.** Annual mean = mean of monthly means, kept only when 10 or
more months are present. Missing values (-99999 in the RLR format) are
dropped, never interpolated.

## Method

1. `build_dataset.py` parses the semicolon-separated RLR file (or an
   equivalent year/month/msl CSV), decodes PSMSL's decimal-year month
   stamps, applies the completeness rule, and writes the monthly and annual
   CSVs plus a provenance log.
2. `analysis.py` computes OLS and Sen's-slope rates for the full record,
   pre-1993, and 1993 onward; fits a centred quadratic for acceleration
   (reported as 2 x the quadratic coefficient, mm/yr^2, with a classical
   t-test on that coefficient); and computes the rate in every 30-year
   rolling window.
3. `viz.py` draws the full series with trend, the rolling 30-year rate, and
   the era comparison.

The quadratic helper is defined in `analysis.py` (the shared `stats_utils`
only carries simple OLS) and unit-tested in `test_project.py` against exact
planted quadratics; the shared statistics are validated in `test_stats.py`.
Both run in CI.

## Validation plan

1. The full-record rate should match published Fremantle estimates (BoM,
   CSIRO and the tide-gauge literature put the long-run rate near the
   global-average order of 1.5-2 mm/yr, with a faster recent era); if it is
   wildly off, suspect the parse before the ocean.
2. The 1943 wartime gap and other missing stretches must appear as
   incomplete years, not as zeros.
3. The rolling-rate curve should show the well-documented mid-century slow
   period and faster recent decades, consistent with the literature on
   Australian tide gauges.

## Limitations (write-up must keep these)

- A tide gauge measures **relative** sea level: land motion at the site is
  in the number. Fremantle sits on the stable Yilgarn margin, but vertical
  land motion (including local groundwater effects reported in the
  literature) is not corrected for here, and the write-up must say so.
- Interannual variability at Fremantle is strongly ENSO-linked (higher sea
  level in La Nina years via the Leeuwin Current), so short-window rates
  swing hard; that is exactly why the rolling window is 30 years.
- The 18.6-year nodal tide cycle aliases into short-period trends; the
  century-scale rate and the quadratic term are the honest headline
  numbers, not any single decade.

## Reproduce

```bash
pip install -r requirements.txt
# drop the PSMSL monthly RLR file into ../dropzone/ (see DROP_FILES_HERE.md), then:
python3 build_dataset.py
python3 analysis.py
python3 viz.py
python3 test_stats.py && python3 test_project.py
```
