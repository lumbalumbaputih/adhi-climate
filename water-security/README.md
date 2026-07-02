# Chronic Physical Climate Risk: Perth Water Security, Streamflow After the Rainfall Step-Change

A data analysis written for **AASB S2 physical-risk assessment** (AASB S2 is
Australia's mandatory climate-disclosure standard, the rulebook that says
companies must report their climate risks). It is the direct sequel to the
[rainfall-decline](../rainfall-decline/) project in this suite: that project
quantified how much drier South West WA has become; this one quantifies what
that dryness did to the water that actually reaches rivers and dams.

> **In one paragraph.** Across 12 Bureau of Meteorology Hydrologic Reference
> Stations in the Darling Range and surrounding SW WA catchments, water-year
> streamflow **stepped down around 2001** (Pettitt change-point test,
> p = 0.007), the same break year the rainfall project found in the winter
> rain. The size of the step is the story: against the 1975-1999 baseline,
> flow since 2000 is down **41%**, and since 2010 down **48%**, while the
> same comparison for rainfall is only about -12%. That is the dry-catchment
> amplifier at work: parched soils and falling groundwater absorb more of
> the rain before any of it runs off, so every 1% of winter rainfall lost
> costs roughly **2.5 to 3.7% of streamflow** (rainfall-runoff elasticity:
> non-parametric estimator 2.55; log-log regression 3.67, r-squared 0.68,
> p < 1e-14). Since 2000 there is no further significant trend (Mann-Kendall
> p = 0.71): the rivers have not kept sliding, they have **settled at the
> new, far lower normal**. Water Corporation's own published series tells
> the same story from the dam side: inflows averaging 418 GL/yr before 1975
> fell to 167 GL/yr after, with 2021-2025 averaging roughly 85 GL/yr. For a
> water utility this is the textbook chronic physical risk: the supply the
> dams were designed around no longer exists, which is exactly why Perth now
> leans on desalination and groundwater replenishment.

## Research question

Did SW WA streamflow step down when the rainfall did, and by how much more?
The physical mechanism being tested is well documented by CSIRO and the
Bureau of Meteorology: when catchments dry out, soils and groundwater soak up
a larger share of the rain before any of it runs off, so streamflow falls
**proportionally much harder than rainfall**. For Perth's water supply this is
the difference between a drier climate and a water-security problem, and it is
why the region now leans on desalination and groundwater replenishment.

The analysis measures three things:

1. **Step change**: a Pettitt change-point test on the regional water-year
   streamflow series, mirroring the rainfall project's method, plus period
   means for 1975-1999, 2000- and 2010-.
2. **Trend**: Mann-Kendall (with trend-free prewhitening) and Sen's slope on
   the regional series.
3. **Amplification**: the rainfall-runoff elasticity (how many % streamflow
   changes per 1% change in rainfall), estimated two ways: the slope of
   ln(flow) on ln(rainfall), and the Sankarasubramanian (2001) non-parametric
   estimator. The rainfall side is the completed rainfall-decline project's
   regional April-October series, so the two projects share one spine.

## Data

| Source | What it provides | Used for |
|--------|------------------|----------|
| **BoM Hydrologic Reference Stations** (bom.gov.au/water/hrs) | Curated long-record daily streamflow for gauges in catchments with minimal regulation | 5-8 SW WA station series, aggregated to May-April water years |
| **rainfall-decline project** (this repo) | Regional cool-season rainfall, 1950-2024, already built and validated | The rainfall side of the elasticity and amplification analysis |
| **Water Corporation** (watercorporation.com.au, optional) | Published annual inflow to Perth dams | Cross-check of the gauged-streamflow story against the water utility's own series |

**Why HRS gauges instead of dam inflows as the spine?** Dam inflow is a
back-calculated quantity of a heavily managed system. HRS stations are the
BoM's reference set chosen specifically for trend detection: long records,
good quality control, minimal extraction or regulation upstream. The Water
Corporation series is kept as the utility-eye validation, not the evidence.

**The stations analysed** (BoM HRS, August 2024 dataset version; 13 files
supplied, 12 in the regional series):

| Station | Gauge | Complete water years |
|---|---|---|
| 614006 | Murray River - Baden Powell | 1964-2022 |
| 614044 | Yarragil Brook - Yarragil Formation | 1953-2022 |
| 614196 | Williams River - Saddleback Rd Bridge | 1967-2022 |
| 614224 | Hotham River - Marradong Rd Bridge | 1967-2022 |
| 616002 | Darkin River - Pine Plantation | 1969-2022 |
| 616006 | Brockman River - Tanamerah | 1981-2022 |
| 616013 | Helena River - Ngangaguringuring | 1972-2016 |
| 616019 | Brockman River - Yalliawirra | 1975-2022 |
| 616041 | Wungong Brook - Vardi Rd | 1981-2022 |
| 616178 | Jane Brook - National Park | 1963-2022 |
| 616216 | Helena River - Poison Lease Gs | 1967-2022 |
| 617003 | Gingin Brook - Bookine Bookine | 1973-2022 |

Station 614037 (supplied but starting 1983) is excluded because it cannot
cover 18 complete baseline years, and water years 1953-1966 are excluded
because fewer than 5 stations report (a "regional" mean of one or two
gauges is not regional). The published series is **1967-2022**, with 7-12
stations per year and a full-network baseline of 45,063 ML.

**Definitions.** Water year = 1 May to 30 April, labelled by the year of the
May start, so each winter wet season lands in one bucket. Baseline =
1975-1999 water years (between the two known rainfall steps; early enough to
predate the post-2000 drop, late enough that HRS records cover it). A water
year is kept only if 15 or fewer days are missing; a station enters the
regional series only with 18 or more complete baseline years. The regional
series is the mean of per-station % anomalies against each station's own
baseline, the same construction as the rainfall project, so big rivers do not
drown out small ones.

## Method

1. `build_dataset.py` ingests the raw daily CSVs (it detects files by content,
   so no renaming is needed), aggregates to water years with explicit
   missing-day accounting, builds the regional anomaly series, and writes the
   clean CSVs plus a provenance log (`data/source-library.csv`).
2. `analysis.py` runs the Pettitt test, the trend battery, and both
   elasticity estimators, writing `stepchange_summary.csv`,
   `trend_summary.csv` and `elasticity_summary.csv`.
3. `viz.py` draws four charts: the anomaly time series, the step change, the
   rainfall-vs-streamflow amplification comparison, and the log-log
   elasticity fit.

Statistics are the suite's hand-rolled, unit-tested implementations
(`stats_utils.py`, byte-identical across projects, validated in
`test_stats.py`). The pipeline pieces specific to this project (water-year
labelling, completeness rules, the tolerant parser, both elasticity
estimators) are tested with synthetic inputs in `test_project.py`; both test
files run in CI on every push.

## Results

All numbers below are produced by `analysis.py` from the clean CSVs in
`data/`; the charts are in `charts/`.

| Question | Result |
|---|---|
| Step change | Pettitt change point at water year **2001** (p = 0.0075), matching the rainfall project's 2000 break |
| Size of the step | 1975-1999 mean 44,380 ML; 2000-2022 mean 26,044 ML (**-41.3%**); 2010-2022 mean 22,942 ML (**-48.3%**) |
| Long-run trend | Sen's slope **-13.4% per decade** over 1967-2022 (Mann-Kendall p = 0.0034; prewhitened p identical) |
| Trend since 2000 | None (Sen -4.9%/decade, MK p = 0.71): flow has stabilised at the lower level, not kept sliding |
| Elasticity | **2.55** (Sankarasubramanian non-parametric) to **3.67** (log-log OLS, r-squared 0.68, p = 7.7e-15) % of flow per % of rainfall |
| Amplification | Rainfall -12.3% vs streamflow -41.3% against the same 1975-1999 baseline: **3.3x** |

## Validation (all three checks passed)

1. **Consistency with the rainfall project.** The streamflow break lands at
   2001; the rainfall project's Pettitt test found 2000. Same event, seen
   from the river.
2. **Elasticity in the literature range.** SW WA hydrology work (CSIRO,
   Water Corporation, and the research literature) describes streamflow
   declining two to three-plus times faster than rainfall; both estimators
   (2.55 and 3.67) sit in or at the top of that band, and the log-log fit
   explains two-thirds of the year-to-year variance.
3. **Water Corporation cross-check.** The supplied export of Water
   Corporation's streamflow chart (cumulative monthly GL, so the December
   value is the annual total) shows dam inflows averaging **418 GL/yr for
   1911-1974** falling to **166.7 GL/yr post-1975 (-60%)**, with 2021-2025
   averaging about **85 GL/yr (-80% vs pre-1975)**. Their catchments and
   baseline differ from ours (dam catchments vs reference gauges; pre-1975
   vs 1975-1999 base), so the exact percentages should differ exactly the
   way they do: measured from the wetter pre-1975 world, the decline is
   deeper than our -41%.

## Limitations

- Gauged catchments are not the dam catchments; the analysis measures the
  regional streamflow signal, not Perth's supply ledger. The Water
  Corporation cross-check covers the supply side.
- Elasticity from observed covariation is descriptive, not a causal model;
  land-use change and farm dams also reduce runoff and are not separated
  here.
- The 1975-1999 baseline is already a post-first-step period, so the
  reported -41% understates the change since the mid-century climate; Water
  Corporation's own pre-1975 comparison (-60%, and -80% for 2021-2025)
  shows how much deeper the full fall is.
- HRS series are gap-filled by the BoM using a rainfall-runoff model (their
  documentation states this); this analysis uses the HRS values as published
  and does not re-do that infilling.
- Streamflow is far more skewed than rainfall; the elasticity is estimated
  in log space and the step change on the % anomaly series partly for that
  reason.
- The record before 1967 is discarded because fewer than 5 gauges report;
  with the single long gauge (Yarragil Brook) the 1950s-60s would swing the
  "regional" series by hundreds of percent on one small catchment's wet
  years.

## Reproduce

```bash
pip install -r requirements.txt
# drop the HRS daily CSVs into ../dropzone/water-security/ (see DROP_FILES_HERE.md), then:
python3 build_dataset.py
python3 analysis.py
python3 viz.py
python3 test_stats.py && python3 test_project.py   # the proof the stats are right
```
