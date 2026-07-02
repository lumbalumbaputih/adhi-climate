# Chronic Physical Climate Risk: Perth Water Security, Streamflow After the Rainfall Step-Change

A data analysis written for **AASB S2 physical-risk assessment** (AASB S2 is
Australia's mandatory climate-disclosure standard, the rulebook that says
companies must report their climate risks). It is the direct sequel to the
[rainfall-decline](../rainfall-decline/) project in this suite: that project
quantified how much drier South West WA has become; this one quantifies what
that dryness did to the water that actually reaches rivers and dams.

> **Status: pipeline complete, awaiting the data drop.** Every number in this
> README will be computed by `analysis.py` from the files described below.
> Nothing here is pre-filled, because the suite rule is that no figure is
> published before the code has produced it from source data. To finish the
> project, drop the streamflow files described in
> [dropzone/DROP_FILES_HERE.md](../dropzone/DROP_FILES_HERE.md) and run the
> three scripts in order.

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

## Validation plan

Before the results are published in this README they must pass three checks:

1. The regional streamflow step-change year should be consistent with the
   rainfall project's change point (around 2000) rather than contradicting it.
2. Elasticity should land in the range hydrology literature reports for SW WA
   (well above 1; CSIRO and Water Corporation both describe streamflow
   declining several times faster than rainfall). If it does not, the first
   suspect is the station set, not the climate.
3. The gauged story should be directionally consistent with Water
   Corporation's published inflow series if that file is supplied.

## Limitations (write-up must keep these)

- Gauged catchments are not the dam catchments; the analysis measures the
  regional streamflow signal, not Perth's supply ledger.
- Elasticity from observed covariation is descriptive, not a causal model;
  land-use change and farm dams also reduce runoff and are not separated here.
- The 1975-1999 baseline is already a post-first-step period, so the reported
  post-2000 decline understates the change since the mid-century climate.
- Streamflow is far more skewed than rainfall; the elasticity is estimated in
  log space and the step change on the % anomaly series partly for that
  reason.

## Reproduce

```bash
pip install -r requirements.txt
# drop the HRS daily CSVs into ../dropzone/ (see DROP_FILES_HERE.md), then:
python3 build_dataset.py
python3 analysis.py
python3 viz.py
python3 test_stats.py && python3 test_project.py   # the proof the stats are right
```
