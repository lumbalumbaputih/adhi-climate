# Financial Materiality: WA Wheat Yields and the Drying Trend

A data analysis written for **AASB S2 physical-risk assessment** (AASB S2 is
Australia's mandatory climate-disclosure standard). The rainfall-decline
project in this suite measured the climate signal; this project converts it
into the number an agri-lender, insurer or grain handler actually prices:
how many percent of wheat yield does a percent of winter rainfall buy?

> **Status: pipeline complete, awaiting the data drop.** Every number in
> this README will be computed by `analysis.py` from the file described in
> [dropzone/DROP_FILES_HERE.md](../dropzone/DROP_FILES_HERE.md). Nothing is
> pre-filled.

## Research question

After removing the technology trend, how tightly do WA wheat yields track
cool-season rainfall, what is the sensitivity (% yield per 10% rainfall),
and what did the driest tenth of winters do to harvests?

## The methodological point everything hinges on

WA wheat yields have **risen** for decades (breeding, agronomy, no-till,
earlier sowing) while cool-season rainfall has **fallen**. Correlating the
raw series therefore understates, or can even sign-flip, the climate
relationship. The honest comparison is between the **technology-detrended
yield anomaly** and the rainfall anomaly. The analysis reports the raw
correlation too, deliberately, as the cautionary contrast, and
`test_project.py` proves the machinery on synthetic data where the truth is
planted: a rising-tech, drying-rain world in which the raw correlation is
weak but the detrended one is strong.

## Data

| Source | What it provides | Used for |
|--------|------------------|----------|
| **ABARES / ABS wheat statistics** (user-supplied CSV per the documented contract) | WA wheat area (ha) and production (t) by season | Yield = production / area |
| **rainfall-decline project** (this repo) | Regional cool-season rainfall anomaly, 1950-2024, already built and validated | The climate side of the sensitivity |

**Season labelling.** Seasons are labelled by the year the crop was *sown*
("1975-76" is 1975), which lines each harvest up with the April-October
growing-season rainfall of the same calendar year. The parser handles
"1975-76", "1975/76" and plain-year labels.

**Sanity gate.** Yields outside 0.1-6.0 t/ha abort the build; that range is
generous around anything WA has ever produced state-wide, so a units mix-up
(acres, bushels, kilotonnes) cannot slide through silently.

## Method

1. `build_dataset.py` ingests the wheat CSV (documented contract or a
   recognisable ABARES-style export; it reports exactly which columns it
   matched), computes yields, applies the sanity gate, and writes the clean
   CSV plus provenance.
2. `analysis.py` fits the technology trend, forms detrended yield anomalies
   (% of trend), joins the rainfall series, and reports: raw vs detrended
   vs both-detrended correlations, the sensitivity slope (% yield per 10%
   rainfall) with p-value and r-squared, and the driest-decile impact.
3. `viz.py` draws the yield series with trend, the sensitivity scatter, the
   paired standardized series, and the drought-year bars.

Statistics are the suite's shared `stats_utils.py` (byte-identical across
projects, validated in `test_stats.py`); the wheat-specific pieces are
validated in `test_project.py`. Both run in CI.

## Validation plan

1. The yield level and technology trend should match published WA figures
   (state-wide yields roughly 1-2.5 t/ha in recent decades, trending up).
2. Known drought seasons (2000, 2006, 2010 among them) should appear in
   the driest-decile set with clearly negative yield anomalies.
3. The sensitivity should be positive and strongly significant; the
   literature on SW WA dryland wheat leaves no doubt about the sign.

## Limitations (write-up must keep these)

- State-wide aggregates mix the wheatbelt's wet and dry margins; shire or
  port-zone data would sharpen the estimate (the pipeline reruns on any
  region's CSV).
- The rainfall series is the SW WA regional anomaly, not a wheatbelt-only
  index; the two overlap heavily but not perfectly.
- A linear technology trend is a simplification; if the residuals show
  structure, the write-up should test a spline or piecewise trend before
  publishing the sensitivity.
- Sensitivity from observed covariation is not a crop model; frost, heat
  shocks at flowering, and price-driven area decisions all live in the
  residuals.

## Reproduce

```bash
pip install -r requirements.txt
# drop the wheat CSV into ../dropzone/wheat-yields/ (see DROP_FILES_HERE.md), then:
python3 build_dataset.py
python3 analysis.py
python3 viz.py
python3 test_stats.py && python3 test_project.py
```
