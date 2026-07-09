# Acute Physical Climate Risk: Fire Danger Trends in South West WA (FFDI, 1941–2026)

A data analysis written for **AASB S2 physical-risk assessment** (AASB S2 is
Australia's mandatory climate-disclosure standard). Fire weather is the acute
physical risk this portfolio had not yet covered, and in WA it is the one
insurers, utilities and local governments price first (Wooroloo 2021,
Yarloop/Waroona 2016, Parkerville 2014). This project computes the McArthur
Forest Fire Danger Index (FFDI) from scratch, daily since 1941, at four sites
chosen to span the region's exposure classes, and asks whether dangerous fire
weather is becoming more frequent.

> **Status: complete.** Every number below is computed by `analysis.py` from
> ERA5 reanalysis (hourly, via the keyless Open-Meteo archive API) and
> validated against the observed GHCN-Daily Perth Airport record. This is the
> portfolio's first project whose data was downloaded entirely by the remote
> session itself, per the project's
> [EXECUTION_PROMPT.md](EXECUTION_PROMPT.md); no hand-staged files.

## Research question

How has weather conducive to dangerous bushfire changed in the Perth region
and South West WA since the mid-20th century, measured with the McArthur
FFDI, and what does that imply for acute physical-risk disclosure?

## Results

The headline is deliberately unsensational: **the fire-weather record in
south-west WA does not show one simple rising line. Where the signal is
clear, it is rising in the wheatbelt and at the coastal margin, flat but
recently spiking around Perth, and falling in the southern forests.**

- **Validation first:** ERA5 tracks the observed Perth Airport record
  closely: daily maximum temperature correlates at **r = 0.964** with a
  **-0.5 C bias** (ERA5 slightly cool) and 84% rain-day agreement over 82
  years. The known severe fire days spike as they should: Wooroloo
  (2021-02-01) scores FFDI 45 and Waroona (2016-01-07) 44 at the Perth
  point, both in the top 0.1% of all days.
- **The early record is not trustworthy, and we say so.** ERA5's 1940s-50s
  show the highest fire danger of the whole record, yet the region's rainfall
  record (see `rainfall-decline/`) shows those decades were the *wettest*.
  Pre-satellite reanalysis over sparsely observed WA is the likely culprit,
  so every trend is run twice, and the satellite-era window (1975 onward)
  leads the conclusions.
- **Wheatbelt (Merredin): rising.** Very High days (FFDI >= 25) are up
  **+3.0 days per decade since 1975** (Mann-Kendall p = 0.027), reaching a
  2020s mean of 81 days per season, the highest of any decade in the record.
- **Perth: flat trend, sharp recent spike.** No significant 1975+ trend
  (+0.2 days/decade, p = 0.76), but the 2020s average **42 Very High days
  per season versus 25 in the 2000s**, the worst decade since the
  unreliable 1940s. The seasonal 99th-percentile FFDI shows the same shape.
- **Southern forests (Manjimup): falling.** Very High days are down
  -0.8 days per decade since 1975 (p = 0.028), from about 10 per season in
  the mid-century record to about 4 to 6 now. This is a genuine, unexpected
  result worth independent scrutiny before anyone banks on it.
- **Coastal margin (Margaret River): rare but sharpening.** Very High days
  are so rare (about 0.2 per season) that counts carry no trend, but the
  seasonal 99th-percentile FFDI has risen +0.4 per decade since 1975
  (p = 0.047).

**What this means for AASB S2 work.** A reporter with WA exposure cannot
justify a single regional fire-risk assumption: the wheatbelt trend and the
Perth 2020s spike argue for rising acute-risk weighting north and east of
the scarp, while the forest-belt decline shows the region is not one story.
Absolute FFDI values here run lower than station-based operational values
(ERA5 winds are grid-cell averages), so the trends and relative changes, not
the raw day counts, are the disclosure-grade result.

## Data

| Source | What it provides | Used for |
|--------|------------------|----------|
| **ERA5 reanalysis** via the Open-Meteo Historical Weather API (keyless) | Hourly temperature, relative humidity, 10 m wind and precipitation, 1940 to present, local time | The four FFDI input series (15:00 observations plus daily rain and max temperature) |
| **GHCN-Daily** station ASN00009021 (Perth Airport) via the NCEI data service | Observed daily TMAX and PRCP from 1944 | Validating ERA5 against a real station |

**Sites.** Perth Airport (metro fringe, pairs with `extreme-heat/`), Merredin
(eastern wheatbelt, pairs with `wheat-yields/`), Manjimup (southern forests),
Margaret River (coastal viticulture and tourism).

## Method

1. `fetch_data.py` downloads the raw inputs into `../dropzone/bushfire-weather/`
   (gitignored, cached, resumable): nine decade chunks of hourly ERA5 per
   site plus the GHCN file. Re-runs skip anything already present.
2. `build_dataset.py` reduces each site to daily FFDI inputs: the 15:00
   local temperature, humidity and wind (McArthur's observation convention),
   the day's rainfall, and the day's maximum temperature, then runs the
   index chain from `fire_indices.py`: Keetch-Byram Drought Index (KBDI),
   Noble et al. (1980) drought factor, and the Mark 5 FFDI. Each site's mean
   annual rainfall (the KBDI parameter) comes from its own record and is
   logged. The first year is KBDI spin-up and is dropped.
3. `analysis.py` builds October-April seasonal metrics (Very High and Severe
   day counts, 99th percentile, cumulative FFDI, season span) and runs the
   suite's trend battery (Mann-Kendall with prewhitening, Sen's slope, OLS)
   on the full record and on 1975 onward, plus a 1945-1974 vs 1995-2024
   epoch comparison and the ERA5-vs-GHCN validation.
4. `viz.py` draws the five charts in `charts/`.

The index constants are transcribed from the cited primary literature in
`fire_indices.py` and validated in `test_fire_indices.py`, including the
Noble et al. calibration point (Black Friday 1939 conditions must score
FFDI of about 100; we get 104). Pipeline pieces are tested on synthetic
inputs in `test_project.py`; trend statistics are the suite's byte-identical
`stats_utils.py`, validated in `test_stats.py`. All three run in CI.

## Limitations (write-up must keep these)

- **ERA5 is a reanalysis, not a measurement.** It is a physics model
  constrained by observations. It validates well against Perth Airport TMAX,
  but grid-cell winds are smoother than station gusts, so absolute FFDI is
  biased low relative to operational station values. Trends are the result.
- **The pre-1975 record is weakly constrained** over WA and looks too fiery
  against the known wet mid-century. Full-record trends are reported for
  transparency and are led by the 1975+ window everywhere they disagree.
- **FFDI measures fire weather, not fire.** Fuel state, ignition and
  suppression are outside this analysis. The named fire events are used only
  to check the index spikes when it should.
- **Australia replaced FFDI operationally with the AFDRS in 2022.** FFDI
  remains the research standard for climate-trend work (it is what the
  BoM/CSIRO State of the Climate reports use), which is why it is used here.
- **One grid point per site.** ERA5 quarter-degree cells stand in for
  districts; the pipeline reruns trivially for any other coordinates.

## Reproduce

```bash
pip install -r requirements.txt
python3 fetch_data.py        # downloads ~110 MB into ../dropzone/bushfire-weather/
python3 build_dataset.py
python3 analysis.py
python3 viz.py
python3 test_fire_indices.py && python3 test_stats.py && python3 test_project.py
```

## Update log

**2026-07-07 · First published.** Built per the execution prompt: ERA5 hourly
via Open-Meteo (36 decade-chunk requests, four sites, 1940 to mid-2026) plus
the GHCN Perth Airport cross-check, all fetched by the session itself with no
hand-staged files. The index chain reproduces the Noble et al. calibration
point and the known severe fire days. First analysis shows the satellite-era
signal rising in the wheatbelt, flat-with-a-2020s-spike at Perth, and falling
in the southern forests; the suspect pre-satellite decades are shaded in the
charts and excluded from the headline claims.
