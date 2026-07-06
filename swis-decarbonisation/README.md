# Transition Analytics: How Fast Is WA's Main Grid Decarbonising?

A data analysis of the South West Interconnected System (SWIS), the grid that
supplies Perth and the south-west, built from AEMO's public Wholesale
Electricity Market (WEM) data. Where the rest of this suite measures climate
risk arriving, this project measures the energy transition actually
happening, which is the flip side of **AASB S2 transition risk**: the pace of
grid decarbonisation drives every WA company's scope 2 trajectory.

> **Status: complete.** Every number below is computed by `analysis.py` from
> AEMO's monthly WEM Facility SCADA files (2006 to 2023), fetched from the
> AEMO data portal, with facilities assigned to fuels from the OpenNEM WEM
> registry; see [dropzone/DROP_FILES_HERE.md](../dropzone/DROP_FILES_HERE.md).

## Results

Trends are measured over the **complete calendar years 2007 to 2022** (2006
and 2023 are partial and excluded). Shares are of utility-scale SCADA
generation, which totals roughly **18 TWh a year**.

- **Renewables are rising fast:** the renewable share went from **4.8% (2007)
  to 22.9% (2022)**, about **+9 percentage points per decade** (Mann-Kendall
  p = 1.3e-05). Almost all of it is **wind**, up from 4.2% to 20.2%
  (+8 pp/decade); utility **solar** is small but growing (0% to 2.2%).
- **Gas is being displaced:** its share fell from **52.0% to 40.9%**, about
  **-9 pp/decade** (p = 9e-05), the mirror image of the renewables rise.
- **Coal has drifted down, not fallen off a cliff:** 43.2% to 36.2%, a real
  decline but not statistically significant over these years (p = 0.75). The
  large Collie and Muja retirements are scheduled for 2023 to 2029, past the
  window of complete data, so the steep part of the coal decline is still
  ahead.

**Scope honesty.** SCADA sees only registered, utility-scale facilities. WA's
large rooftop-solar fleet is behind the meter and appears here only as
suppressed demand, so this renewable share is a **floor**, not the whole
picture. Emissions intensity is not computed: it needs emission factors the
pipeline refuses to invent (see the empty `data/emission_factors.csv`
template), so it is left for a follow-up rather than guessed.

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

## Update log

**2026-07-06 · First published.** Ran the pipeline on AEMO's monthly WEM
Facility SCADA files, 2006 to 2023 (206 monthly files, 94 facilities). Fuels
were assigned from the OpenNEM WEM facility registry, matched to SCADA codes
by station prefix, with a handful of documented manual assignments for large
WA stations OpenNEM does not list separately; every assignment is recorded in
`facility_fuel.csv`. Annual totals land near 18 TWh a year, in line with
published WEM figures. Emissions intensity is deliberately left uncomputed
until the emission-factors template is filled from the National Greenhouse
Accounts workbook.
