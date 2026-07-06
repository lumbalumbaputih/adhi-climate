# Chronic Physical Climate Risk: Sea-Level Rise at Fremantle (1897-2022)

A data analysis written for **AASB S2 physical-risk assessment** (AASB S2 is
Australia's mandatory climate-disclosure standard). The Fremantle tide gauge
is one of the longest sea-level records in the Southern Hemisphere, running
since 1897, which makes it the single best place in Australia to ask the two
questions that matter for coastal assets: how fast is the sea rising here,
and is the rise speeding up?

> **In one paragraph.** Fremantle's sea level has risen about **22 cm since
> 1897**, at a long-run rate of **+1.78 mm/yr** (OLS p = 1.8e-24; Sen's
> slope +1.69 mm/yr over 113 complete years). The rise has not been steady:
> the rate was +1.44 mm/yr before 1993 but **+5.11 mm/yr in the
> satellite-altimetry era (1993-2022)**, roughly 3.5 times the earlier pace,
> and the fastest 30-year window in the record is 1985-2014 at +5.62 mm/yr.
> Yet a centred quadratic fit puts the acceleration at **+0.013 mm/yr^2
> with p = 0.11, short of the significance bar**: the record's strong
> ENSO-driven swings (higher sea level in La Nina years via the Leeuwin
> Current) and the mid-century pause (the 1962-1991 window reads
> -0.84 mm/yr) leave room for a slow-then-fast history without a clean
> quadratic shape. The honest AASB S2 reading: the long-run rise is
> unequivocal and the recent era is far faster than the century average,
> but this single gauge cannot yet prove smooth acceleration, and the
> number includes whatever the land under Fremantle is doing (vertical
> land motion is not corrected for).

## Results

Computed by `analysis.py` on annual means of the monthly RLR series,
complete years only (113 of 126; a complete year has 10+ months, so the
1942 wartime disruption and 12 other years are excluded, never
interpolated). Rates are OLS with classical stderr, alongside Sen's slope:

| Series | n | OLS rate (mm/yr) | p | Sen's slope (mm/yr) |
|---|---|---|---|---|
| Full record (1897-2022) | 113 | **+1.78 +/- 0.14** | 1.8e-24 | +1.69 |
| Pre-1993 | 83 | +1.44 +/- 0.18 | 6.8e-12 | +1.41 |
| 1993 on (altimetry era) | 30 | **+5.11 +/- 1.22** | 2.6e-4 | +5.16 |

Acceleration, from the centred quadratic over the full record: **+0.0132
mm/yr^2** (2 x b2), **p = 0.11, not statistically significant**. The
30-year rolling rates (`data/rolling_rates.csv`) run from **-0.84 mm/yr
(1962-1991)** to **+5.62 mm/yr (1985-2014)**, which is exactly why no
single recent window should be quoted as "the" trend.

Charts: `charts/01_msl_series.png` (the full series with trend),
`charts/02_rolling_rate.png` (the 30-year rolling rate),
`charts/03_eras.png` (the era comparison).

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

## Validation

1. **Full-record rate vs the literature: passes.** BoM, CSIRO and the
   tide-gauge literature put Fremantle's long-run rate near the
   global-average order of 1.5-2 mm/yr with a faster recent era; the
   pipeline reads +1.78 mm/yr over 1897-2022 and +5.11 mm/yr since 1993.
2. **Gaps stay gaps: passes.** The 1942 wartime disruption survives as an
   incomplete year (3 months present, year excluded), as do 12 other thin
   years (a 1899-1914 cluster, 1926, 1965, 1967); nothing is interpolated
   or zero-filled.
3. **Rolling-rate shape vs the literature: passes.** The 30-year curve
   shows the well-documented mid-century slow period (bottoming at
   -0.84 mm/yr for 1962-1991) and the faster recent decades (peaking at
   +5.62 mm/yr for 1985-2014), consistent with published work on
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
# drop the PSMSL monthly RLR file into ../dropzone/sea-level/ (see DROP_FILES_HERE.md), then:
python3 build_dataset.py
python3 analysis.py
python3 viz.py
python3 test_stats.py && python3 test_project.py
```

## Update log

How this project evolved, in order. Each entry says what we found and why it
earned an update.

**5 Jul 2026 · First published.** The Fremantle tide gauge, running since 1897,
is one of the longest sea-level records in the Southern Hemisphere. It shows
the sea has risen about 22 cm, and far faster since 1993 than over the century
as a whole. Published the pipeline from the PSMSL research-grade record: the
full series with its trend, the 30-year rolling rate, and the era comparison,
complete years only and nothing interpolated.

**5 Jul 2026 · Choosing honesty over a bigger headline.** The recent rate,
5.1 mm a year, is dramatic and tempting to headline as acceleration. But the
quadratic acceleration term is not statistically significant (p = 0.11): a real
mid-century pause and strong El Nino and La Nina swings leave the curve
unproven on this single gauge. Reported the unequivocal long-run rise and the
far faster recent era as the finding, kept acceleration flagged as not yet
proven, and stated openly that this is relative sea level with land motion not
corrected for.
