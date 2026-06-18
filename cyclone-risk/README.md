# Physical Climate Risk: Tropical Cyclone Trends Affecting Western Australia (1985–2024)

A data analysis written to support **AASB S2 physical-risk assessment**. AASB S2 is Australia's mandatory climate-disclosure standard (the rule that requires companies to report their climate risks).

> **The short version.** Between 1985 and 2024 the seas off Western Australia
> warmed by about 0.5 °C. That warming is solid and statistically significant (in
> plain terms, it is a real trend, not just luck of the draw). And yet the
> tropical cyclones that affect WA did **not** get stronger over the same period.
> Their numbers edged down a little. Their average peak strength drifted lower
> (clearly so across the whole South Indian Ocean, and more weakly, without being
> statistically significant, for the WA-only group). And there was **no positive
> link** between how warm the regional sea was and how strong the cyclones got.
> The practical lesson for climate risk is simple: you cannot read WA's future
> cyclone danger straight off the recent local record. Warmer oceans did not show
> up as stronger storms here, so physical-risk assessment has to rely on
> forward-looking climate projections. That is exactly the kind of judgement AASB
> S2 asks companies to make.

This goes against the popular "warmer oceans, stronger storms" headline. That is
the whole point. The value of the analysis is that it tests that assumption
against 40 years of data and reports what the data actually show.

---

## Research question

Have the tropical cyclones that affect Western Australia changed in strength
between 1985 and 2024, and does their strength rise and fall with warming sea
temperatures?

"WA-affecting" means a storm whose track passed within 500 km of the WA coast,
anywhere from the north Kimberley down to the Mid West. The study starts in 1985
because satellite coverage before then was too patchy to estimate storm strength
reliably.

## Data

| Source | What it provides | Used for |
|--------|------------------|----------|
| **IBTrACS v04r01** (NOAA NCEI) | Global best-track cyclone positions, winds and pressures | Cyclone counts, intensity, tracks |
| **BOM Tropical Cyclone Database** (IDCKMSTM0S) | Australia's official Southern-Hemisphere track record | Independent cross-check |
| **NOAA ERSSTv5** | Monthly 2° sea-surface temperature, 1854–present | SST trend and correlation |

A quick gloss on the jargon. Best-track data is the official storm-path record
that weather agencies keep for each cyclone. IBTrACS is the worldwide collection
of those records. ERSSTv5 is NOAA's long-running monthly record of sea-surface
temperature (the temperature of the top layer of the ocean, often shortened to
SST).

The analysis covers **758 South Indian Ocean systems**, of which **194 affected
WA**. Storm strength is reported in two ways: as the **BOM 10-minute sustained
wind** (the standard Australia uses, the wind speed averaged over 10 minutes) and
as **minimum central pressure** (the lowest air pressure at the storm's centre,
where lower means stronger).

A note on how wind is measured, because honesty matters here. Different agencies
average wind speed over different lengths of time. The US agencies report a
1-minute average; the Bureau of Meteorology (Australia's national weather agency,
shortened to BOM) reports a 10-minute average, which works out about 12% lower for
the very same storm. This analysis leads with the BOM 10-minute figure because
the subject is WA, and it cross-checks that against the US winds and against
central pressure (which has no averaging-time ambiguity, so it sidesteps the
problem entirely).

## How the data were validated

Before computing any trend, the cleaned data was checked for trustworthiness.

The BOM 10-minute winds in IBTrACS match the Bureau's own published database to
the knot for the major WA cyclones (Vance 1999 at 120 kt, Orson 1989 at 130 kt,
Marcus 2018 at 135 kt). The US 1-minute winds sit about 12% higher, exactly as
the difference in averaging period predicts. And 97% of the named WA-affecting
storms picked up by the 500 km rule also show up in the Bureau's Australian-region
database, which confirms the geographic filter is sound. Within the WA group, the
BOM wind data is 92% complete (85% in the 1980s, rising to 100% in the most recent
decade). So the headline measure is well-supported for the storms that matter
here, even though it is patchier across the wider basin, where other agencies are
in charge.

---

## Key findings

### 1. Frequency: stable, maybe drifting down a little

WA sees about 5 cyclones come within 500 km of the coast in an average season.
That number is broadly steady, with a slight downward drift, from about 5.1 per
season in 1985–2004 to 4.6 per season in 2005–2024. This fits the wider research
showing a long-term decline in the number of tropical cyclones in the Australian
region.

![Annual cyclone counts](charts/01_annual_count.png)

### 2. Intensity: no rise, a small decline

The average peak strength of WA-affecting cyclones has drifted **down**, not up,
across the four decades. Mean BOM peak wind fell from about 76 kt in 1985–1994 to
63 kt in 2015–2024, and mean central pressure rose (that is, weakened) from 959
hPa to 973 hPa.

| Decade | WA storms | Mean peak wind (BOM, kt) | Mean min pressure (hPa) | Reached Cat 3+ |
|--------|:---------:|:------------------------:|:-----------------------:|:--------------:|
| 1985–94 | 47 | 76 | 959 | 17% |
| 1995–04 | 55 | 78 | 956 | 38% |
| 2005–14 | 50 | 69 | 964 | 28% |
| 2015–24 | 42 | 63 | 973 | 19% |

*(Cat 3+ uses the Saffir–Simpson category, the familiar 1-to-5 hurricane scale,
which is defined on 1-minute winds. So it is computed from the US winds rather
than the 10-minute BOM value.)*

![Intensity by decade](charts/02_intensity_by_decade.png)

Formal trend tests back up this picture, and, just as importantly, show where its
limits are:

| Series | Trend | Significant? |
|--------|-------|--------------|
| WA mean peak wind | −3.6 kt/decade | No (Mann-Kendall p = 0.26) |
| WA mean min pressure | +4.0 hPa/decade (weakening) | Borderline (OLS p = 0.04, Mann-Kendall p = 0.10) |
| Basin-wide mean peak wind | −3.7 kt/decade | **Yes** (Mann-Kendall p = 0.048) |

Two of the test names above are worth a one-line gloss. The Mann-Kendall test is a
standard check for whether a trend is real or just chance. OLS (ordinary least
squares) is the usual way of fitting a straight-line trend through data.

The direction is consistently toward weaker storms. For the WA-only group the
trend is real but not statistically robust, because only about five storms a year
is a small sample with a lot of year-to-year noise. Across the whole South Indian
Ocean, where the sample is much larger, the decline in mean wind is statistically
significant. Two separate measures, wind and pressure, point the same way, which
adds confidence in the direction even where any single test is borderline.

![Wind-speed trend](charts/03_trend_wind_speed.png)
![Pressure trend](charts/04_trend_pressure.png)

### 3. Rapid intensification: appears to be rising, but read it with care

The share of storms that rapidly intensified (a wind jump of at least 30 kt in 24
hours, measured on the US 1-minute winds) rose from about 21% in 1985–1994 to
around 40% in the later decades. This is the one result that points toward a more
dangerous future, and it lines up with the physical expectation that warmer oceans
raise the ceiling on how fast a storm can strengthen.

It comes with a big caveat. Older best-track records are smoother and sampled less
often than modern ones, which automatically makes rapid intensification harder to
spot in the early years. So part of the apparent increase is probably an artefact
of better observations rather than a purely physical change. Treat the trend as
suggestive, not proven.

![Rapid intensification](charts/05_rapid_intensification.png)

### 4. Sea-surface temperature: warming, but unhooked from intensity

The ocean in the WA cyclone development region warmed by **0.16 °C per decade**
(p < 0.0001, in other words a very strong result), about half a degree of warming
from the 1980s to today. Despite that, warmer seasons were **not** linked to
stronger WA cyclones. The correlation between seasonal SST and mean cyclone wind
is slightly negative and not significant (r = −0.22), and the correlation with
pressure points the same way (warmer seasons go with very slightly weaker storms).

![SST correlation](charts/06_sst_correlation.png)

This disconnect is the analytical heart of the project. Sea-surface temperature
sets the energy available to a cyclone, but it is not the only thing that matters.
Vertical wind shear (winds that change with height and can tear a storm apart),
mid-level moisture, and the large-scale circulation (including ENSO, the El
Niño/La Niña cycle, and the Indian Ocean Dipole, a related Indian Ocean
temperature pattern) all decide whether that energy actually gets used. Over the
WA record, those circulation factors appear to have masked or outweighed the
warming signal.

---

## What this means for WA industry and AASB S2

Western Australia's coast carries the Pilbara iron-ore and LNG export
infrastructure, offshore oil and gas, coastal towns and farming, all of it exposed
to cyclones. Under AASB S2, the listed companies and large financial institutions
behind that infrastructure now have to disclose the climate risks that are
material to them. Reporting is being phased in from 1 January 2025, with the
larger second group, which captures many of the big WA operators, starting for
periods from 1 July 2026.

This analysis carries one clear, slightly uncomfortable message for that
disclosure work. The recent observed record does not support a simple "cyclones
are getting stronger because the ocean is warming" story for WA. An honest
physical-risk assessment cannot lean on the historical trend to claim a rising
hazard, because the historical trend does not show one. What it can and should do
is recognise that the absence of an observed trend is not the same as safety. The
ocean has warmed a lot, the energy ceiling for the strongest storms has risen,
rapid intensification may be becoming more common, and forward-looking climate
models still project a shift toward fewer but potentially more intense systems.
Good disclosure therefore rests on scenario-based projections rather than simply
extending the past in a straight line. That is precisely the discipline AASB S2 is
designed to enforce.

The timing is hard to miss. The 2025–26 season produced Severe Tropical Cyclone
Narelle, a Category 5 system that struck the Kimberley and Gascoyne in March 2026
with damage estimated near half a billion dollars. A quiet long-term trend and a
devastating individual season are not a contradiction. They are exactly why risk
has to be judged on the worst cases (the tail of the distribution), not the
average.

---

## Limitations

The honest caveats, stated plainly. The WA-affecting group is small, about five
storms a year, so WA-only trends have limited statistical power, and the
not-significant results should be read as "no clear signal" rather than "no
change." Intensity estimates rest on best-track data whose quality and sampling
improved over the period, which can bias trends, most sharply for rapid
intensification. The SST analysis uses a single regional box and a seasonal
average, so it captures the broad warming signal but not finer-scale ocean
structure. And 40 years is short for detecting climate trends. These results
describe what was observed in the satellite era, not a forecast of the future.

## Reproduce it

Everything except the large raw files is in the repository. The cleaned datasets
are committed, so the notebook runs end to end without the multi-gigabyte
originals; place those in `data/raw/` to rebuild from scratch.

```
pip install -r requirements.txt
python test_stats.py          # validate the statistics against textbook values
jupyter lab cyclone_analysis.ipynb
```

Raw inputs (free): IBTrACS SI v04r01 and NOAA ERSSTv5 from NOAA NCEI, and the BOM
Southern-Hemisphere database from the Bureau of Meteorology. Exact sources are
listed in the notebook.

```
cyclone-risk/
├── cyclone_analysis.ipynb     # the narrated analysis, top to bottom
├── stats_utils.py             # OLS, Pearson, Mann-Kendall, Sen's slope (from scratch)
├── test_stats.py              # validation against known values
├── build_dataset.py           # IBTrACS cleaning + WA-proximity flag
├── viz.py                     # chart styling
├── data/                      # cleaned, committed CSVs (raw/ is git-ignored)
└── charts/                    # six publication-quality figures
```

## A note on the statistics

The trend and correlation tests are written from scratch in `stats_utils.py`
rather than pulled from a library, and `test_stats.py` checks them against known
textbook values. For example, the regression reproduces the Anscombe-quartet slope
and its p-value of 0.0022, and the Mann-Kendall matches a hand-computed series
that only ever moves one direction. (Pearson is the standard measure of how
closely two things move together, and Sen's slope is a robust way to estimate the
size of a trend.) This keeps the project light on dependencies and fully
transparent: every number can be traced to code you can read.

---

### References and context

- **IBTrACS v04r01** (International Best Track Archive for Climate Stewardship), Knapp et al., NOAA NCEI. The global best-track cyclone dataset.
- **NOAA ERSSTv5** (Extended Reconstructed Sea Surface Temperature), Huang et al. (2017). The sea-surface temperature record.
- **AASB S2** *Climate-related Disclosures* (Australian Accounting Standards Board, 2024; phased commencement from 1 January 2025).
- **IPCC AR6 WG1** (2021), Chapter 11, *Weather and Climate Extreme Events in a Changing Climate*. Observed and projected tropical-cyclone trends.
- **Bureau of Meteorology and CSIRO**, *State of the Climate* (2024).
- **Kuleshov et al.**, *Trends in tropical cyclones in the South Indian Ocean and the South Pacific Ocean* (Journal of Geophysical Research, 2010). The observed decline in Australian-region tropical-cyclone frequency.
- **Bhatia et al.**, *Recent increases in tropical cyclone intensification rates* (Nature Communications 10:635, 2019). Rapid-intensification trends.

*Analysis by Adhi Muhammad Faris Katili. Data: IBTrACS (NOAA NCEI), BOM, NOAA
ERSSTv5. Part of the [adhi-climate](../) portfolio.*
