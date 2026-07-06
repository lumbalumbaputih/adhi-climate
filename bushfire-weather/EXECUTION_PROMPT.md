# Execution Prompt: Bushfire Weather - Fire Danger Trends in South West WA (FFDI)

> Portfolio project #11 of the `adhi-climate` suite (acute physical climate risk).
> Paste this whole file into a fresh session to start work. Self-contained: no prior context needed.
> Mirrors the structure and proven workflow of the completed projects: `extreme-heat/` (the
> closest sibling: daily weather, from-scratch indices, Mann-Kendall trends) and
> `rainfall-decline/` (the drying story this project extends into fire danger).
> This is the portfolio's first project designed so that **the remote session downloads all
> of its own data**: no files for anyone to stage in `dropzone/` by hand, ever.

---

## Project framing

**Research question.** How has weather conducive to dangerous bushfire changed in the
Perth region and South West WA since the mid-20th century, measured with the McArthur
Forest Fire Danger Index (FFDI), and what does that imply for AASB S2 acute
physical-risk disclosure?

**CV framing.** *"Acute Physical Climate Risk: Fire Weather Trends in South West WA
(1940–2025), a Reanalysis-Based FFDI Analysis for AASB S2 Physical Risk Assessment."*

**Scope.** Four ERA5 grid points chosen to tell one story across the region's exposure
classes: **Perth Airport** (metro fringe, pairs with `extreme-heat/`), **Manjimup**
(southern forests, the highest-fuel landscape), **Merredin** (eastern wheatbelt, pairs
with `wheat-yields/`), and **Margaret River** (high-value coastal viticulture and
tourism). Daily FFDI computed from scratch, 1940 to the latest full fire season.

**Why it matters.** Fire is the acute physical risk the portfolio does not yet cover,
and in WA it is the one insurers, utilities and local governments price first (Wooroloo
2021, Yarloop/Waroona 2016, Parkerville 2014). AASB S2 asks reporters to assess acute
physical risks with quantitative, auditable evidence; a tested, reproducible FFDI series
is exactly that. It also closes the narrative loop with `rainfall-decline/` (the drying)
and `extreme-heat/` (the heat): fire weather is where those two trends compound.

**Repo.** Umbrella repo `adhi-climate`, subfolder `bushfire-weather/`.

---

## Data access: the point of this project

Every prior project stalled on the same step: remote sessions could not reach the data
hosts, so raw files had to be downloaded by hand into `dropzone/`. This project is
designed to remove that step, and the design was tested before this plan was written.

**What was verified on 2026-07-06, from the remote session itself:**

- The environment's network gateway refuses CONNECT to every external data host tried
  (Open-Meteo, NOAA NCEI, NOAA PSL, CoastWatch ERDDAP, PSMSL, AEMO, BoM): HTTP 403
  policy denial at the proxy, for both `curl` and the session's built-in fetch tool.
- GitHub and the package registries (PyPI, npm) are open; a test wheel downloaded from
  PyPI without issues. Code and libraries flow; data does not.

So the blocker is not the data hosts, it is one environment setting, changed once.

**The one-time unblock (owner action, ~2 minutes).** In the Claude Code environment
settings for this repository (claude.ai/code, the environment this session runs in),
change network access so the session can reach the data domains: either allow full
internet access, or add the domains below to the allowlist. Docs:
https://code.claude.com/docs/en/claude-code-on-the-web

| Domain | What it unblocks |
|--------|------------------|
| `archive-api.open-meteo.com` | **This project's primary source** (ERA5 reanalysis, no key) |
| `www.ncei.noaa.gov` | This project's station cross-check (GHCN-Daily); `extreme-heat` `--fetch` re-runs; IBTrACS re-runs; NCEI ERDDAP for `marine-heatwaves` |
| `downloads.psl.noaa.gov` | `cyclone-risk` ERSSTv5 re-runs |
| `coastwatch.pfeg.noaa.gov` | `marine-heatwaves` (alternative ERDDAP server) |
| `psmsl.org` | `sea-level` re-runs |
| `data.wa.aemo.com.au` | `swis-decarbonisation` (currently stalled on data) |
| `www.bom.gov.au` | `water-security` re-runs, cyclone cross-reference (caveat: BoM also refuses some scripted requests server-side, so keep expectations modest) |
| `agriculture.gov.au`, `www.abs.gov.au` | `wheat-yields` (currently stalled on data) |
| `cleanenergyregulator.gov.au`, `data.gov.au` | `transition-risk` (planned) |

The first two rows are enough for this project. The rest turn the whole portfolio
self-service: the three stalled projects and every completed project's re-run stop
needing hand-staged files.

**Verification (step 0 of execution).** Run `tools/check-data-access.sh` from the repo
root. It sends one tiny request per host and prints `ok` / `BLOCKED` / `DENIED` per
line. Do not start the pipeline until the two required hosts show `ok`.

**Fallback if the setting cannot be changed.** The pipeline must still accept staged
files: `build_dataset.py` reads `dropzone/bushfire-weather/` first and only fetches
what is missing, exactly like `extreme-heat/build_dataset.py --fetch`. Document the
fallback URLs in `dropzone/DROP_FILES_HERE.md` when the pipeline lands. Self-fetch is
the default path, not the only path.

---

## Division of labour

- **Kai**: data acquisition (self-fetch), cleaning, the FFDI implementation and its
  tests, analysis, charts, notebook, README draft, and the access-probe tooling.
- **Ris**: domain interpretation (what an FFDI trend means for an insurer, a utility, a
  shire), final narrative, and interview talking points. Ris does not write code but
  must be able to speak to the findings for ~5 minutes without notes before this goes
  on a CV.

---

## ⚠ Read before starting (the credibility tests)

1. **ERA5 is a reanalysis, not a measurement.** It is a physics model constrained by
   observations. Validate it against the GHCN-Daily Perth Airport record (TMAX,
   rainfall) and report the bias and correlation in the README. Where reanalysis and
   station disagree, say so and prefer the station for point claims.

2. **FFDI measures fire *weather*, not fire.** It says nothing about fuel state,
   ignition, or suppression. Claims are about the frequency and severity of dangerous
   fire weather. Known severe fire dates (Wooroloo 2021-02-01, Waroona 2016-01-06/07,
   Parkerville 2014-01-12) are used only as sanity checks that the index spikes when it
   should, never as "the index predicted the fire".

3. **The early record is less trustworthy.** Pre-satellite (before 1979) and especially
   1940s–1950s reanalysis is weakly constrained over WA. Run every trend on both the
   full series and 1975 onward; report both; if they disagree materially, lead with the
   shorter, better-observed one.

4. **Australia replaced FFDI operationally in 2022** (the AFDRS). FFDI remains the
   research standard for climate trend work (it is what BoM/CSIRO State of the Climate
   reports use) and is fully computable from open data. State this choice and the
   reason in the README.

5. **Do not trust remembered constants.** The McArthur Mark 5 FFDI equation, the
   Keetch-Byram Drought Index (KBDI) recursion, and the Griffiths (1999) drought factor
   must be transcribed from primary literature at execution time, cited in the code,
   and unit-tested against published worked examples before any analysis runs.

6. **No fabricated data, ever.** Every request URL is recorded with a retrieval date in
   `data/source-library.csv`. Raw API responses are cached (gitignored) so re-runs are
   reproducible without re-fetching. If a value cannot be traced to a recorded request,
   it does not exist for this analysis.

---

## Data sources: acquire in this order

| # | Source | What to download | How to use |
|---|--------|------------------|------------|
| 1 | **Open-Meteo Historical Weather API** (primary), `archive-api.open-meteo.com`, ERA5 reanalysis, free for non-commercial use, no API key | Hourly temperature (2 m), relative humidity (2 m), wind speed (10 m), precipitation, for the four sites, 1940-01-01 to the latest complete fire season. Chunk requests by decade; cache raw JSON in `dropzone/bushfire-weather/` (gitignored). Reduce to the daily inputs FFDI needs: 15:00 local temperature, humidity and wind (the standard observation convention), plus 24 h rainfall. | The spine. Everything FFDI needs, one keyless API, all four sites, 85+ years. |
| 2 | **NOAA NCEI GHCN-Daily API** (cross-check), `www.ncei.noaa.gov/access/services/data/v1`, station `ASN00009021` (Perth Airport) | Daily TMAX and PRCP, 1950 to present, CSV. Same endpoint and parser pattern as `extreme-heat/`. | Validation only: ERA5 vs observed at the one site with a long quality record. The validation section of the README comes from this. |
| 3 | **Primary literature for the index formulas** (reference, not data) | Noble, Bary & Gill (1980) for the Mark 5 FFDI equation; Keetch & Byram (1968) for KBDI; Griffiths (1999) for the drought factor; a published worked example or verified reference values for each. | Source of the constants in `fire_indices.py` and the expected values in its tests. Cite in code and README. |

**Why ERA5 via Open-Meteo instead of BoM station data?** Same reason `extreme-heat/`
used GHCN: an authoritative series behind a stable, keyless, script-friendly endpoint
beats a richer source behind a hostile one. BoM blocks scripted access; FFDI needs
humidity and wind, which GHCN's Australian stations do not carry; ERA5 has all four
inputs, hourly, from 1940, for any WA coordinate, and is the dataset national fire-trend
studies already lean on. The GHCN cross-check keeps it honest. Attribution when the
project ships: ERA5 (Copernicus/ECMWF) via Open-Meteo, plus GHCN-Daily (NOAA NCEI);
add both to the root README's licensing paragraph.

Build the provenance log before analysis: `data/source-library.csv` with columns
`source, request_url, sites, span, date_retrieved`, one row per API request.

---

## Analysis steps

| # | Step | Detail | Output |
|---|------|--------|--------|
| 0 | Access check | `tools/check-data-access.sh` shows `ok` for Open-Meteo and NCEI. If not, stop and request the environment change (or fall back to dropzone staging). | go / no-go |
| 1 | Acquisition & cleaning | Chunked, resumable, politely rate-limited fetches; raw JSON cached in the dropzone folder; clean per-site daily CSV committed: `date, t15, rh15, wind15, rain24, tmax`. GHCN Perth Airport pulled the same way. | `data/fire_weather_daily_<site>.csv`, `data/source-library.csv` |
| 2 | Index implementation | `fire_indices.py`: KBDI recursion, Griffiths drought factor, Mark 5 FFDI, each transcribed from the cited paper, each unit-tested against published values in `test_fire_indices.py`. Sanity check: the known severe fire dates spike. | tested `fire_indices.py`, daily FFDI per site |
| 3 | Trend analysis | Per site and fire season (Oct–Apr, labelled by starting year): days at Very High (FFDI ≥ 25) and Severe+ (FFDI ≥ 50), seasonal 99th percentile, cumulative FFDI, season length (first/last Very High day). Mann-Kendall + Sen's slope from the suite's byte-identical `stats_utils.py`, OLS + 95% CI as the parametric cross-check, full period and 1975+. | `data/trend_summary.csv` |
| 4 | Epoch comparison | 1945–1975 vs 1995–2025: distribution shift per site (percentiles, threshold-day counts), presented as levels, not just slopes. | `data/epoch_summary.csv` |
| 5 | Validation | ERA5 vs GHCN at Perth Airport: TMAX correlation and bias, rain-day agreement; one honest paragraph on what reanalysis smooths over. | `data/validation_summary.csv` |
| 6 | Write-up & site | README in the suite voice; story object in `js/data.js`, chart data in `js/chartdata.js`, `npm run build`, update-log entries, per `PROCEDURE.md`. | shipped project |

---

## Statistics and honesty rules

- Reuse the suite's **from-scratch, tested** `stats_utils.py` unchanged (CI enforces
  byte-identity). New index code lives in `fire_indices.py` with its own test file,
  same standard: no constant without a citation, no function without a known-value test.
- Trend claims only from Mann-Kendall significance plus a Sen's slope worth reporting;
  where full-period and 1975+ trends disagree, the README says so in the same sentence.
- The words "forecast" and "predict" do not appear. FFDI thresholds are stated with
  their operational meaning at the time (Very High, Severe) and the AFDRS caveat.
- No em dashes anywhere, per house rules.

## Charts (target 5, matplotlib, suite house style)

1. **Severe fire-weather days**: per-season count of FFDI ≥ 25 days, four sites as
   small multiples, Sen's slope overlaid.
2. **The distribution shift**: seasonal FFDI percentile curves (or decade boxes) for
   the two epochs, one site per panel.
3. **Season creep**: first and last Very High day per season at Perth, as a band chart.
4. **Seasonal cycle heatmap**: month × year mean FFDI, Perth (the "it is getting longer
   and worse" single image).
5. **Validation scatter**: ERA5 vs GHCN Perth Airport TMAX, with bias stated on the chart.

---

## Repo layout & deliverables

Mirror the completed projects exactly:

```
bushfire-weather/
├── EXECUTION_PROMPT.md      (this file)
├── README.md                (plain-English write-up, suite voice)
├── build_dataset.py         (self-fetch by default, dropzone fallback, resumable)
├── fire_indices.py          (KBDI, drought factor, FFDI; cited constants)
├── test_fire_indices.py
├── analysis.py              (every number in the README comes from here)
├── stats_utils.py           (byte-identical suite copy)
├── test_stats.py
├── test_project.py
├── viz.py
├── requirements.txt
├── data/                    (clean CSVs committed; raw JSON cache gitignored)
└── charts/
```

**Definition of done**
- [ ] `tools/check-data-access.sh` shows `ok` for both required hosts, and
      `build_dataset.py` runs end to end **with no hand-staged files**.
- [ ] `test_fire_indices.py`, `test_stats.py`, `test_project.py` pass;
      `stats_utils.py` byte-identical across projects; CI green.
- [ ] README has Validation and Limitations sections covering credibility tests 1–5.
- [ ] `data/source-library.csv` traces every committed number to a recorded request.
- [ ] Front page updated per `PROCEDURE.md` (story object, chart data, counts, build,
      headless render check); update log started; root README row flipped to Complete;
      dropzone fallback documented in `DROP_FILES_HERE.md`.
- [ ] Zero em dashes, checked in every form.

---

## Timeline (part-time, ~3 weeks)

| Week | Milestone |
|------|-----------|
| 1 | Network unblock verified, fetches built and cached, clean daily CSVs committed, GHCN cross-check in. |
| 2 | Index code written, cited and tested; trends and epochs computed; validation section drafted. |
| 3 | Charts, README, front-page integration, interview brief, root README updated, PR. |

## Alternatives considered (and when to switch)

- **Frost risk in the wheatbelt** (GHCN TMIN only): the backup if only
  `www.ncei.noaa.gov` can be allowlisted. One keyless source, same parser as
  `extreme-heat/`, complements `wheat-yields/`. Smaller story, but fully self-service.
- **Drought / soil dryness indices** (same Open-Meteo endpoint): viable, but overlaps
  `rainfall-decline/` and `water-security/` without adding a new risk class.
- **Renewable resource trends** (same endpoint): interesting transition-side story, but
  `swis-decarbonisation/` already owns that ground and is only stalled on data, which
  the same network change unblocks.

## Stretch goals (only after the core ships)

- Re-run the three stalled projects (`marine-heatwaves`, `swis-decarbonisation`,
  `wheat-yields`) now that their hosts are reachable, retiring their dropzone-only status.
- Add self-fetch (`--fetch`) paths to the completed projects' `build_dataset.py` so a
  clean machine can rebuild the whole portfolio unattended.
- An interactive FFDI explorer (site picker, season slider) on the front page.
