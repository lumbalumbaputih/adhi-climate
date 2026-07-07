# Acute Physical Climate Risk: Marine Heatwaves off the Western Australian Coast

A data analysis written for **AASB S2 physical-risk assessment** (AASB S2 is
Australia's mandatory climate-disclosure standard). Marine heatwaves are the
ocean's version of a heatwave: weeks of abnormally warm sea temperature. Off
WA they are a first-order business risk: the 2011 "Ningaloo Nino" event
devastated the Shark Bay scallop and Abrolhos fisheries, killed seagrass
meadows, and pushed species ranges south. This project measures how often
they happen, how strong they get, and whether they are becoming more common.

> **Status: complete.** Every number below is computed by `analysis.py` from
> OISST v2.1 daily sea-surface temperature for the Ningaloo box (1982 to
> 2026), fetched from NOAA CoastWatch ERDDAP and gap-filled from NOAA NCEI's
> daily archive so the record is unbroken; see
> [dropzone/DROP_FILES_HERE.md](../dropzone/DROP_FILES_HERE.md).

## Research question

How many marine-heatwave days a year does the Ningaloo coast experience,
what were the biggest events on record, and is there a trend? The 2011
event doubles as the pipeline's own validation case: if the analysis does
not find a major event spanning the 2010-11 summer, the inputs are wrong.

## Results

Over 1982 to 2026 the pipeline detects **103 marine-heatwave events** off the
Ningaloo coast.

- **The 2011 Ningaloo Nino is the longest event on record:** 26 September
  2010 to 26 January 2011, **123 consecutive days**, peaking **3.7 C above
  the climatological mean** (category II Strong). It is exactly the event the
  validation plan required the analysis to find, and it falls where the
  literature puts it.
- **The most intense peak** in the record is **3.8 C above climatology**, on
  2 January 2025.
- **Marine-heatwave days per year** are rising at **+4.6 days per decade**,
  just outside significance (Mann-Kendall p = 0.06), so this is reported as a
  suggestive trend, not a settled one.
- **Peak intensity** (+0.24 C per decade, p = 0.01) and **annual-mean SST**
  (+0.12 C per decade, p = 0.04) are both rising significantly. The ocean off
  Ningaloo is measurably warmer, and its hot extremes are getting hotter.

The MHW-day trend is measured against the fixed 1982-2011 baseline in a
warming ocean, so part of it is warming showing through by construction; the
significant mean-SST trend is the cleaner statement of that warming.

## Data

| Source | What it provides | Used for |
|--------|------------------|----------|
| **NOAA OISST v2.1** | Daily quarter-degree sea surface temperature from September 1981, blended from satellite and in-situ observations | The daily SST series for the study box |
| via **ERDDAP** (NOAA CoastWatch / NCEI servers) | Script-friendly CSV subsetting of OISST | The practical way to pull a small coastal box without touching NetCDF |

**Study box.** The default is the Ningaloo coast, roughly 21.5 S to 23.5 S
and 112.5 E to 114.5 E, the epicentre of the 2011 event. The code averages
whatever grid cells arrive, so any single box works; drop one box's files
per run so the spatial mean stays honest.

## Method: the Hobday definition, implemented from scratch

Marine heatwaves are defined following **Hobday et al. (2016)**, the standard
the field uses:

1. A day-of-year climatological mean and 90th-percentile threshold, pooled
   over an 11-day window across the **1982-2011 baseline**, both smoothed
   with a 31-day moving average (the code falls back to a full-record
   baseline, and says so, if the record cannot cover 25 baseline years).
2. An event is **5 or more consecutive days** above the threshold; events
   separated by **2 days or fewer are merged**.
3. Intensity is SST minus the climatological mean; each event's peak, as a
   multiple of (threshold minus climatology), gives the **Hobday et al.
   (2018) category**: I Moderate, II Strong, III Severe, IV Extreme.

Day-of-year matching uses the calendar day with the 11-day window absorbing
the one-day leap offset, the common practical approximation. Missing days
are handled conservatively: they end runs rather than bridging them (except
through the standard 2-day merge rule). Detection is validated in
`test_project.py` by planting a known event, including a mid-event 2-day dip
that must merge and a 3-day spike that must NOT count. Trend statistics are
the suite's shared, tested `stats_utils.py`.

## Validation plan

1. The 2011 event must be detected, span the 2010-11 summer, and rank as
   the (or one of the) most intense on record, consistent with the
   literature on the Ningaloo Nino.
2. Event counts and day counts should be broadly consistent with published
   MHW climatologies for the region.
3. The annual-mean SST trend should be positive and of the order reported
   for the Leeuwin Current region.

## Limitations (write-up must keep these)

- One box is one stretch of coast; MHW behaviour differs between Ningaloo,
  Shark Bay, and the south coast. The pipeline reruns trivially per box.
- OISST is a quarter-degree blended product; nearshore reef-flat
  temperatures can exceed it. Impact statements should stay regional.
- Trends in MHW days partly reflect the fixed 1982-2011 baseline in a
  warming ocean; that is by construction and the write-up must state it
  rather than presenting baseline-relative counts as anomalies of a
  stationary climate.

## Reproduce

```bash
pip install -r requirements.txt
# drop the ERDDAP OISST CSV(s) into ../dropzone/marine-heatwaves/ (see DROP_FILES_HERE.md), then:
python3 build_dataset.py
python3 analysis.py
python3 viz.py
python3 test_stats.py && python3 test_project.py
```

## Update log

**2026-07-06 · First published.** Ran the pipeline on OISST v2.1 daily SST for
the Ningaloo box, 1982 to 2026. The CoastWatch ERDDAP aggregation was missing
scattered days in 2015 and 2016; those days were filled from NOAA NCEI's daily
OISST archive onto the identical grid, so the record is unbroken and
single-source in effect. The 2011 Ningaloo Nino validation case is detected as
the longest event on record (123 days, peak 3.7 C), confirming the inputs and
the Hobday detection are sound.
