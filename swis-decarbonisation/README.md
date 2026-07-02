# Transition Analytics: How Fast Is WA's Main Grid Decarbonising?

A data analysis of the South West Interconnected System (SWIS), the grid that
supplies Perth and the south-west, built from AEMO's public Wholesale
Electricity Market (WEM) data. Where the rest of this suite measures climate
risk arriving, this project measures the energy transition actually
happening, which is the flip side of **AASB S2 transition risk**: the pace of
grid decarbonisation drives every WA company's scope 2 trajectory.

> **Status: pipeline complete, awaiting the data drop.** Every number in this
> README will be computed by `analysis.py` from the files described below.
> Nothing is pre-filled; see
> [dropzone/DROP_FILES_HERE.md](../dropzone/DROP_FILES_HERE.md) for the
> download list, then run the three scripts in order.

## Research question

How has the SWIS generation mix shifted, at what rate is the renewables share
rising and the coal share falling, and what has that done to the grid's
emissions intensity?

## Data

| Source | What it provides | Used for |
|--------|------------------|----------|
| **AEMO WEM data portal** (data.wa.aemo.com.au) | Facility-level metered generation (SCADA), monthly CSVs from the mid-2000s | The generation mix, aggregated facility -> fuel -> month -> year |
| **AEMO WEM facility register** | Facility code to fuel/technology mapping | Assigning every facility to a fuel bucket; unmapped facilities are reported, never silently guessed |
| **NGA emission factors** (user-filled template) | t CO2-e per MWh by fuel | Emissions intensity; only computed once `data/emission_factors.csv` is filled from the National Greenhouse Accounts workbook, with the source recorded per row |

**Scope honesty.** SCADA covers utility-scale, registered facilities. WA's
world-leading rooftop solar is behind the meter and does not appear as
generation here; it shows up only as suppressed demand. The write-up must say
so: this analysis measures the utility mix, and therefore *understates* the
total solar contribution to the SWIS.

**Unit honesty.** Files whose energy column is MWh are summed as energy;
files that only report MW are converted as 30-minute interval averages
(MW x 0.5 = MWh) and the provenance log records which conversion applied to
which file.

## Method

1. `build_dataset.py` ingests the monthly generation files and the facility
   register (detected by content), buckets fuels (coal, gas, distillate,
   wind, solar, bio, storage, other), and writes monthly and annual mix CSVs
   plus a provenance log. It also writes the empty emission-factors template.
2. `analysis.py` drops incomplete calendar years, then runs the trend battery
   (Mann-Kendall with prewhitening, Sen's slope, OLS) on each fuel's annual
   share and on the combined renewables share; if the factors template has
   been filled it computes the emissions-intensity series and its trend.
3. `viz.py` draws the stacked mix, the renewables-share trend, the coal vs
   renewables crossover, and (when available) the intensity series.

Statistics are the suite's shared `stats_utils.py` (byte-identical across
projects, validated in `test_stats.py`). Pipeline pieces specific to this
project are tested with synthetic inputs in `test_project.py`. Both run in CI.

## Validation plan

1. Annual totals should be within a few percent of AEMO's published WEM
   statistics for overlapping years.
2. The coal share should fall visibly across the 2010s and 2020s, consistent
   with the announced Collie coal retirements; if it does not, suspect the
   facility mapping first.
3. If intensity is computed, sanity-check the level against published
   estimates of SWIS average emissions intensity for a recent year.

## Limitations (write-up must keep these)

- Rooftop PV is invisible in SCADA; the renewables share here is a floor,
  not the whole story.
- Fuel-type average emission factors ignore plant-level efficiency
  differences; the intensity series is an index built on documented factors,
  not a greenhouse inventory.
- Facility outages, mothballing and new entrants change the mix for
  non-climate reasons; the trend tests describe the outcome, not the cause.

## Reproduce

```bash
pip install -r requirements.txt
# drop the AEMO files into ../dropzone/swis-decarbonisation/ (see DROP_FILES_HERE.md), then:
python3 build_dataset.py
python3 analysis.py
python3 viz.py
python3 test_stats.py && python3 test_project.py
```
