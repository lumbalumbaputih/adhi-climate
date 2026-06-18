# Chronic Physical Climate Risk: South West WA Rainfall Decline (1950–2024)

A data analysis framed for **AASB S2 physical-risk assessment**, Australia's
mandatory climate-disclosure standard.

> **In one paragraph.** South West Western Australia's cool-season (April–October)
> rainfall has fallen by a statistically significant **~2.9% per decade since
> 1950** (Mann-Kendall p = 0.001). The decline is not a gentle slope but a **step
> down around the year 2000** (Pettitt change-point p = 0.006): the regional total
> drops from about 571 mm (1950–1999) to about 475 mm (2000–2024), leaving the
> last 25 years roughly **19% drier** than the 1950–1974 baseline. The May–July
> early-winter peak is falling faster still (~4.4%/decade), and the signal is
> consistent across **all seven stations** analysed. The decline is well
> established and matches CSIRO/Bureau of Meteorology figures; what carries
> scientific nuance is the *cause*, which is attributed largely to a strengthening
> subtropical pressure ridge and poleward-shifting winter storm tracks under
> greenhouse-gas and ozone forcing. For a water utility, grain lender or insurer
> this is textbook **chronic** physical risk: a permanent shift in the baseline,
> not a run of bad years.

---

## Research question

Has cool-season rainfall in South West WA declined significantly since the
mid-century, how large and how persistent is the shift, and how does it relate to
the major climate drivers?

The **cool season** is April–October, the Bureau of Meteorology's standard wet
season for the southwest. **May–July** is examined separately as the early-winter
sub-season where the decline is known to be sharpest. Anomalies are measured
against a **1950–1974 baseline** (the pre-step-change reference).

## Data

| Source | What it provides | Used for |
|--------|------------------|----------|
| **GHCN-Daily** (NOAA NCEI) | Daily station rainfall; the Australian (`ASN*`) records are the **Bureau of Meteorology's observations** redistributed by NOAA in a script-friendly format | Seven SW WA station series, 1950–2024 |
| **NOAA PSL: DMI** | Dipole Mode Index | Indian Ocean Dipole (IOD) driver |
| **Marshall (2003) SAM index** (BAS) | Station-based Southern Annular Mode index, 1957– | SAM driver |
| **NOAA PSL: Niño 3.4 anomaly** | ERSST-based ENSO index | ENSO driver |

**Why GHCN-Daily rather than the BoM website?** It is the same underlying station
data, but downloadable by script, so the entire pipeline reproduces without manual
web navigation. Results are validated against BoM/CSIRO's published figures (see
*Validation*).

**The seven stations** were chosen for genuine full daily coverage across
1950–2024 (≥22 of 25 baseline years and ≥22 recent years) and to span the
rainfall gradient:

| Station | Setting | 1950–74 Apr–Oct baseline |
|---|---|---|
| Cape Leeuwin | Far SW tip, coastal (wettest) | 897 mm |
| Albany | South coast | 762 mm |
| Deeside | SW forest, high-rainfall zone | 698 mm |
| Westbourne | SW forest (Manjimup region) | 567 mm |
| Narrogin | Central wheatbelt | 409 mm |
| Northam | Northern Avon valley wheatbelt | 381 mm |
| Wagin | Southern wheatbelt | 344 mm |

> **Note on the Perth catchment.** The Perth Darling-scarp dam catchments
> (Mundaring, Jarrahdale), the most-cited part of the SW WA water story, had
> gappy *daily* records in GHCN-Daily and were excluded to avoid biasing the
> series. The high-rainfall SW-corner stations capture the same forced signal.

## Method

1. **Clean** each station's daily rainfall, dropping days that fail NOAA's quality
   flags. A month is used only if it has ≤3 missing/failed days; a cool season is
   used only if all seven months are complete.
2. **Anomalies** are computed per station against its *own* 1950–1974 mean, in mm
   and %. The **regional series** is the mean of the per-station % anomalies
   (requiring ≥5 of 7 stations in a year), so wet coastal sites don't swamp dry
   inland ones.
3. **Step-change**: the **Pettitt** non-parametric change-point test.
4. **Trend**: **Mann-Kendall** significance + **Sen's slope** (robust) + **OLS**
   with a 95% confidence band, on the full record, the May–July sub-season, and
   each station.
5. **Drivers**: Pearson correlation of the cool-season rainfall anomaly against the
   cool-season IOD, SAM and ENSO indices, reported **raw and detrended** (detrended
   isolates year-to-year covariation from the shared long-term trend).

All statistics, OLS, Pearson, Mann-Kendall, Sen's slope and the Pettitt test, are implemented from first principles in [`stats_utils.py`](stats_utils.py) and
validated against known values in [`test_stats.py`](test_stats.py) (22 checks).
**scipy is not required.**

## Key findings

| Result | Number | Significant? |
|---|---|---|
| Apr–Oct trend, 1950–2024 | **−2.9%/decade** (≈ −20 mm/decade) | **Yes** (OLS p=0.0005; MK p=0.001, τ=−0.25) |
| May–July trend, 1950–2024 | **−4.4%/decade** | **Yes** (MK p=0.0001) |
| Step-change (Pettitt) | **~2000** | **Yes** (p=0.006) |
| Pre/post the break | 571 mm (1950–99) → 475 mm (2000–24) = **−17%** | n/a |
| 1950–1974 vs 2000–2024 | 587 mm → 475 mm = **−19%** | n/a |
| Trend *after* 2000 | flat (stepped to a drier normal) | No (MK p=0.66) |
| Stations declining | **7 of 7** (6 significant) | n/a |
| IOD (DMI) correlation | r = −0.41 raw / −0.26 detrended | raw p=0.0003; detrended p=0.027 |
| ENSO (Niño 3.4) correlation | r = −0.41 raw / −0.35 detrended | raw p=0.0003; detrended p=0.002 |
| SAM (Marshall) correlation | r = −0.31 raw / −0.20 detrended | raw p=0.010; detrended p=0.11 (n.s.) |

![Cool-season anomaly](charts/01_timeseries_anomaly.png)
![Step change](charts/02_stepchange.png)
![Trend](charts/03_trend_mannkendall.png)
![Drivers](charts/04_driver_correlation.png)
![Station × decade](charts/05_station_decade.png)

## Validation

The Bureau of Meteorology and CSIRO *State of the Climate* report a **~16%
April–October** and **~20% May–July** decline for SW WA since 1970 (against a
1900–1969 baseline), and state that a decline of this magnitude is "highly
unlikely … due to natural variability alone." This analysis, different stations,
a different baseline period, and an independent code path, lands in the same
place: ~19% drier (1950–74 vs 2000–24), with May–July falling fastest. The
agreement is the credibility check.

## What this means: AASB S2 chronic physical risk

- **Chronic, not acute.** A permanent downward shift in the baseline is precisely
  the slow-onset, persistent hazard AASB S2 asks entities to identify and
  disclose. Because it is a *step-change*, the pre-2000 climate is no longer a
  valid planning baseline, the recent 25 years are the new normal.
- **Exposed parties:** Perth's water supply (dam inflows have fallen far more than
  rainfall, a modest rainfall drop is amplified into a large runoff loss); the
  wheatbelt grain economy and its lenders; and property and crop insurers
  repricing the southwest.
- **The judgement it forces:** assess this risk on the post-step-change baseline
  and forward-looking projections, not a long historical average that no longer
  describes the climate.

## Attribution: what causes the decline (referenced, not invented)

The **decline is robust**; the **cause** is still being refined, and this analysis
does not attempt formal detection-attribution. The published picture:

- The proximate mechanism is a **strengthening subtropical high-pressure ridge**
  and a **poleward shift of the winter westerlies / storm tracks** (a more-positive
  Southern Annular Mode), which deliver **fewer rain-bearing cold fronts** to the
  southwest.
- These circulation changes are substantially **anthropogenic**, greenhouse gases
  plus stratospheric ozone depletion. High-resolution models reproduce the decline
  only with that forcing included.
- **Apportionment varies by study and method**: one modelling estimate finds ~43%
  of the multi-decadal decline is externally forced; other work attributes up to
  two-thirds of the post-1975 decline to the intensifying ridge; climate change is
  commonly implicated in a 20–30% rainfall reduction. The decline is certain; the
  precise split is not.
- The **Indian Ocean Dipole** (more frequent positive events) and **ENSO** add
  year-to-year variability.

**This project's own correlation is illustrative, not causal.** IOD, ENSO and SAM
are all negatively associated with cool-season rainfall (r ≈ −0.3 to −0.4), but
once the shared long-term trend is removed the year-to-year correlations are
modest. In plain terms: the climate modes explain the year-to-year *wiggles*,
while the forced circulation change explains the downward *staircase*. Correlation
here is consistent with the literature but does not establish causation.

## Limitations

- Seven stations, not a gridded regional product, robust and spatially coherent,
  but not a substitute for BoM's gridded analysis.
- The Perth Darling-scarp catchment is not directly represented (gappy daily data).
- The Pettitt test reports a single dominant change point (~2000); the smaller
  mid-1970s step documented in the literature is visible in the series but not
  separately tested here.
- Driver correlation is association, not formal attribution.

## Reproduce

```bash
pip install -r requirements.txt

# 1. statistics are correct
python3 test_stats.py

# 2. rebuild the clean CSVs from raw downloads (see data/raw/ note below)
python3 build_dataset.py

# 3. run the analysis (prints the findings, writes summary CSVs)
python3 analysis.py

# 4. regenerate the charts
python3 viz.py
```

Raw downloads live in `data/raw/` and are **git-ignored** (re-downloadable from the
sources above): the GHCN-Daily station files `ASN000095xx/0101xx.dly`, the GHCN
metadata `ghcnd-stations.txt` and `ghcnd-inventory.txt`, and the three index files
`dmi.had.long.data`, `marshall.sam.txt`, `nina34.anom.data`. The cleaned CSVs in
`data/` are committed, so the analysis and charts reproduce without re-downloading.

## Repo structure

```
rainfall-decline/
├── README.md                 ├── analysis.py        (step-change, trend, drivers)
├── requirements.txt          ├── viz.py             (5 charts)
├── rainfall_analysis.ipynb   ├── stats_utils.py     (MK, Sen, OLS, Pearson, Pettitt)
├── cv-blurb.txt              ├── test_stats.py      (22 unit tests)
├── INTERVIEW_BRIEF.md        ├── build_dataset.py   (parse + clean)
├── data/   (committed CSVs; raw/ git-ignored)
└── charts/ (5 × 300 dpi PNG)
```

## Sources

- CSIRO & Bureau of Meteorology, *State of the Climate 2024*: https://www.csiro.au/en/research/environmental-impacts/climate-change/state-of-the-climate/report-at-a-glance
- BoM, *Recent rainfall, drought and southern Australia's long-term rainfall decline*: https://www.bom.gov.au/climate/updates/articles/a010-southern-rainfall-decline.shtml
- Delworth & Zeng (2014), *Regional rainfall decline in Australia attributed to anthropogenic greenhouse gases and ozone levels*, Nature Geoscience: https://www.nature.com/articles/ngeo2201
- Hawke et al. (2025), *A Review of Drivers of Cool Season Rainfall in Southwest Western Australia*, WIREs Climate Change: https://wires.onlinelibrary.wiley.com/doi/10.1002/wcc.70028
- Data: GHCN-Daily (NOAA NCEI); NOAA PSL climate indices; Marshall (2003) SAM index (BAS).

---

*Author: Adhi Muhammad Faris Katili · Master of Environment and Climate Emergency,
Curtin University. Statistics implemented from first principles and unit-tested;
findings independently validated against CSIRO/BoM published figures.*
