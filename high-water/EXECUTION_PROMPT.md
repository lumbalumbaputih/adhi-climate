# Execution Prompt: High Water - Coastal Flood Hours at Fremantle (1984–2026)

> Portfolio project #12 of the `adhi-climate` suite (acute physical climate risk).
> Paste this whole file into a fresh session to start work. Self-contained: no prior context needed.
> Mirrors the structure and proven workflow of the completed projects. Closest siblings:
> `sea-level/` (the same gauge, monthly means, the chronic story this project turns into an
> acute one) and `extreme-heat/` (the threshold-exceedance framing and completeness rules).
> Like `bushfire-weather/`, this project is designed so that **the remote session downloads
> all of its own data**: no files staged in `dropzone/` by hand. Access was verified before
> this plan was written (see below).

---

## Project framing

**Research question.** How often does the sea at Fremantle now reach levels that were
rare in the 1980s, how much of that change is the rising mean sea level versus the
storms and tides riding on top of it, and what does that imply for AASB S2 acute
physical-risk disclosure for ports and coastal assets?

**CV framing.** *"Acute Physical Climate Risk: Coastal Flood Hours at Fremantle
(1984–2026), an Hourly Tide-Gauge Analysis for AASB S2 Physical Risk Assessment."*

**Scope.** One station, one variable, done properly: the hourly sea-level record at
Fremantle (UHSLC station 175), 1984 to the latest complete year. Annual counts of
high-water hours above fixed benchmarks, annual maxima and upper percentiles, their
trends, and a clean decomposition of how much of the change comes from the higher
mean sea level alone.

**Why it matters.** The portfolio's `sea-level/` project established the chronic
story: Fremantle is up about 22 cm since 1897, with the 1993-on era rising at roughly
+5 mm/yr. But AASB S2 preparers do not lose money to a mean; they lose it to the hours
when water is over the wharf, in the substation, or across the access road. Coastal
flooding is the acute physical risk the portfolio does not yet cover, and Fremantle is
the perfect place to cover it: Australia's benchmark tide gauge, sitting in a working
port, in a microtidal sea where a small lift in the baseline translates quickly into
extra hours of high water. The project closes the suite's most natural narrative loop:
`sea-level/` shows the baseline rising, this project shows what that does to flooding.

**Why it starts in 1984.** The gauge has run since 1897, but the digitised **hourly**
record starts in 1984 (the pre-1984 hourly charts have not been digitised into the
research-quality archive). The 1897-on monthly record stays where it belongs, in
`sea-level/`; this project cites it for context and uses it for validation.

**Repo.** Umbrella repo `adhi-climate`, subfolder `high-water/`.

**Front-page motive.** The index grid on the homepage is four columns wide on desktop
(`portfolio.css`, `.pindex` is `repeat(4, 1fr)` at 1100 px and up). Eleven cards leave
an empty cell in the last row; the twelfth card completes a clean 4 × 3 grid.

---

## Data access: verified before this plan was written

**What was verified on 2026-07-13, from the remote session itself:**

- `uhslc.soest.hawaii.edu` is reachable through the environment's network policy
  (HTTP 200), alongside the hosts already unblocked for the earlier projects
  (Open-Meteo, NOAA NCEI, NOAA PSL, CoastWatch ERDDAP, PSMSL, AEMO). The Bureau of
  Meteorology still refuses scripted requests (HTTP 403), which is one more reason to
  source the gauge data from UHSLC.
- The **research-quality** hourly file for Fremantle downloads cleanly:
  `https://uhslc.soest.hawaii.edu/data/csv/rqds/indian/hourly/h175a.csv`
  (5.6 MB, columns `year, month, day, hour, sea_level_mm`, spanning
  **1984-01-01 to 2021-12-31**, missing-value sentinel `-32767`).
- The **fast-delivery** hourly file extends the same station to the present:
  `https://uhslc.soest.hawaii.edu/data/csv/fast/hourly/h175.csv`
  (spanning 1984 through **May 2026** at probe time).
- A quick uncorrected pass over the raw feed, done only to confirm the story exists
  before committing to it (all of it to be recomputed by the tested pipeline, none of
  it quotable): the annual-mean level averaged about 715 mm on the gauge datum over
  1984–1993 and about 841 mm over 2015–2024; hours above 1350 mm (the 99.5th
  percentile of the 1984–1993 decade) ran roughly 40/yr in 1984–1993, 65/yr in
  1994–2003, 114/yr in 2004–2013 and 119/yr in 2014–2023. Those later counts are
  floors, not estimates: the fast-delivery feed has gaps (2024 is missing about half
  its hours), which is exactly why the pipeline needs an explicit completeness rule.

**Verification (step 0 of execution).** Run `tools/check-data-access.sh` from the repo
root; this planning PR adds the UHSLC probe to it. Do not start the pipeline until the
UHSLC line shows `ok`.

**Fallback if access breaks.** `build_dataset.py` must read `dropzone/high-water/`
first and only fetch what is missing, the same pattern as `extreme-heat/` and
`bushfire-weather/`. Document the two URLs above in `dropzone/DROP_FILES_HERE.md` when
the pipeline lands. Self-fetch is the default path, not the only path.

---

## Division of labour

- **Kai**: data acquisition (self-fetch), the RQDS/fast-delivery splice, QC and
  completeness rules, annual metrics, trends and the decomposition, charts, README
  draft, and the site integration.
- **Ris**: domain interpretation (what an extra hundred high-water hours a year means
  for a port operator, an insurer, a coastal shire), final narrative, and interview
  talking points. Ris does not write code but must be able to speak to the findings
  for ~5 minutes without notes before this goes on a CV.

---

## ⚠ Read before starting (the credibility tests)

1. **Datum and units, stated once and never fudged.** Levels are millimetres above the
   UHSLC station zero for Fremantle, which is neither Chart Datum nor AHD. Do not
   convert to AHD or to "height above the wharf" without an authoritative offset from
   the station metadata; if none is found, every level in the write-up is stated
   relative to the gauge zero and to the record's own 1984–1993 baseline. The record
   is *relative* sea level: no vertical-land-motion correction is applied, and the
   README says so (same caveat as `sea-level/`).

2. **An exceedance is not a certified flood.** An hourly gauge reading above a
   statistical benchmark is not a mapped inundation of anybody's property. The
   project's words are "high-water hours" and "flood-risk hours", with benchmarks
   defined transparently as percentiles of the 1984–1993 baseline decade. The word
   "flood" attaches to an actual event only if an authoritative local threshold or a
   documented event report backs it.

3. **Two feeds, two quality levels.** Research-quality (RQDS) data is quality-controlled
   and is the record through 2021; fast-delivery data is near-real-time and only
   extends 2022 onward. The splice point is explicit in the code, fast-delivery years
   are flagged in the data and on every chart, and the project is re-run when the RQDS
   file extends. A year enters the annual statistics only if it passes a completeness
   rule set **before** any trend is computed (target: at least 80% of hours present
   and no season-biased gap, since a missing winter biases exceedance counts low;
   2024 currently fails).

4. **The Leeuwin Current and ENSO swing this gauge hard.** Annual-mean sea level at
   Fremantle moves by 10 cm and more with ENSO (the 2011 La Niña year averaged about
   925 mm against a 715 mm baseline-decade mean). No claim rests on endpoints: trends
   are Mann-Kendall plus Sen's slope over all years, and the headline decomposition
   (raw versus mean-adjusted exceedances) is exactly the tool that separates a trend
   from one big La Niña year.

5. **The 18.61-year nodal tide cycle exists.** The record spans about 2.3 nodal
   cycles. Fremantle is microtidal, so the modulation is small, but the README
   acknowledges it and the epoch comparison uses windows a whole number of ~19 years
   apart (1984–1993 versus 2003–2012 versus 2013–2022 style checks) as a sensitivity
   test, not as the headline.

6. **Hourly means understate the true peaks.** Fremantle sees seiches and set-up on
   scales of minutes; the hourly value smooths over them. All claims are about hourly
   water levels, and the README says the true instantaneous maxima ran higher.

7. **No fabricated data, ever.** Every request URL is recorded with a retrieval date in
   `data/source-library.csv`. Raw downloads are cached in `dropzone/high-water/`
   (gitignored) so re-runs are reproducible without re-fetching. If a value cannot be
   traced to a recorded request, it does not exist for this analysis.

---

## Data sources: acquire in this order

| # | Source | What to download | How to use |
|---|--------|------------------|------------|
| 1 | **UHSLC research-quality hourly data** (primary), station 175a Fremantle, `uhslc.soest.hawaii.edu/data/csv/rqds/indian/hourly/h175a.csv`, free, no key | The full 1984–2021 hourly series, one 5.6 MB CSV. Cache raw in `dropzone/high-water/`. | The quality-controlled spine of the analysis. |
| 2 | **UHSLC fast-delivery hourly data** (extension), station 175, `uhslc.soest.hawaii.edu/data/csv/fast/hourly/h175.csv` | The same series through the present; use only 2022 onward, flagged as fast-delivery. | Brings the record to the latest complete year. |
| 3 | **PSMSL monthly RLR, station 111 (Fremantle)** (validation), already committed under `sea-level/data/` | Nothing new to download. | Annual means computed from the hourly series must track the PSMSL annual means over the overlap up to a constant datum offset; the validation section comes from this. |
| 4 | **UHSLC station metadata** (reference), the station 175 page and metadata files | Datum notes, gauge history, any documented instrument changes. | The datum statement in the README (credibility test 1) and a check for step changes at instrument swaps. |

**Why UHSLC and not the Bureau of Meteorology or the port authority?** The same
reason every project in this suite gives: an authoritative series behind a stable,
keyless, script-friendly endpoint beats a richer source behind a hostile one. BoM
refuses scripted requests (re-verified at probe time), and port-authority data is not
openly downloadable. UHSLC is the international research archive for exactly this
purpose, it is what the sea-level literature uses, and its Fremantle holdings were
verified from this environment before this plan was written. Attribution when the
project ships: UHSLC research-quality and fast-delivery data (Caldwell, Merrifield &
Thompson, NOAA NCEI dataset doi:10.7289/V5T43R7N); add it to the root README's
licensing paragraph.

Build the provenance log before analysis: `data/source-library.csv` with columns
`source, request_url, span, date_retrieved`, one row per download.

---

## Analysis steps

| # | Step | Detail | Output |
|---|------|--------|--------|
| 0 | Access check | `tools/check-data-access.sh` shows `ok` for UHSLC. If not, stop and fix the environment settings, or fall back to dropzone staging. | go / no-go |
| 1 | Acquisition & splice | Download both feeds, cache raw in the dropzone folder. Use RQDS through 2021, fast-delivery from 2022, sentinel `-32767` to missing, plausibility QC (spikes, flatlines, impossible jumps). Commit a **daily** reduction, not the hourly bulk: `date, hours_present, mean_mm, max_mm, source_feed`. The hourly series stays a cached, re-fetchable input. | `data/daily_sea_level.csv`, `data/source-library.csv` |
| 2 | Annual metrics | Per calendar year passing the completeness rule (credibility test 3): mean, median, max, 99th and 99.9th percentile, and high-water hours and days above three fixed benchmarks, the 99th, 99.5th and 99.9th percentiles of the 1984–1993 baseline decade, stated in mm on the gauge datum and fixed **before** any trend test. | `data/annual_metrics.csv` |
| 3 | Trends | Mann-Kendall + Sen's slope from the suite's byte-identical `stats_utils.py` on annual mean, annual max, and high-water hours per benchmark; OLS + 95% CI as the parametric cross-check; full record and 1993-on (the altimetry-era split `sea-level/` already uses). | `data/trend_summary.csv` |
| 4 | The decomposition | The headline. Recompute exceedance hours on a mean-adjusted series: each year's hourly values minus that year's mean anomaly relative to the baseline decade. Raw counts show what happened; adjusted counts show what the same storms and tides would have done on the old baseline; the gap is the price of the higher mean sea level. | `data/decomposition.csv` |
| 5 | Epoch comparison | 1984–1993 versus the last ten complete years: full hourly distribution shift (percentile curves, threshold-hour counts), presented as levels, not just slopes, plus the nodal-phase sensitivity check (credibility test 5). | `data/epoch_summary.csv` |
| 6 | Validation | Annual means from the hourly series versus PSMSL RLR annual means over the overlap: correlation, the constant datum offset, and any years that disagree; plus a check that known event dates (the June–July storm-surge dates the record contains) spike as expected. | `data/validation_summary.csv` |
| 7 | Write-up & site | README in the suite voice; story object in `js/data.js`, chart data in `js/chartdata.js`, counts and copy, `npm run build`, OG card, update log, per `PROCEDURE.md` and the site section below. | shipped project |

---

## Statistics and honesty rules

- Reuse the suite's **from-scratch, tested** `stats_utils.py` unchanged (CI enforces
  byte-identity; the workflow discovers `high-water/` automatically, nothing to edit).
- Project-specific logic (the splice, completeness rule, benchmark counting, the
  mean-adjustment) lives in `build_dataset.py` / `analysis.py` and is tested in
  `test_project.py` against tiny synthetic hourly fixtures where every count is
  hand-checkable.
- Benchmarks and the completeness rule are fixed before trend tests and never tuned to
  the result. Raw and mean-adjusted counts are always reported together.
- Trend claims only from Mann-Kendall significance plus a Sen's slope worth reporting;
  where the full record and 1993-on disagree, the README says so in the same sentence.
- The words "forecast" and "predict" do not appear. Nothing is called a flood unless
  an authoritative threshold or event report backs it (credibility test 2).
- No em dashes anywhere, per house rules.

## Charts (target 5, matplotlib, suite house style)

1. **High-water hours per year** (the headline): annual hours above the middle
   benchmark, Sen's slope overlaid, fast-delivery years visually flagged.
2. **The baseline lift**: annual mean and annual max as two series on the gauge datum,
   showing the extremes riding on the rising mean.
3. **Same storms, higher sea**: raw versus mean-adjusted exceedance hours, the
   decomposition as one paired chart.
4. **The distribution shift**: hourly sea-level distribution, first decade versus the
   last ten complete years, with the upper tail emphasised.
5. **The flood calendar**: month × year heatmap of high-water hours (the winter storm
   season, visibly widening and darkening).

---

## Repo layout & deliverables

Mirror the completed projects exactly:

```
high-water/
├── EXECUTION_PROMPT.md      (this file)
├── README.md                (plain-English write-up, suite voice)
├── build_dataset.py         (self-fetch by default, dropzone fallback, resumable)
├── analysis.py              (every number in the README comes from here)
├── stats_utils.py           (byte-identical suite copy)
├── test_stats.py
├── test_project.py
├── viz.py
├── requirements.txt
├── data/                    (clean daily/annual CSVs committed; raw hourly cached, gitignored)
└── charts/
```

## Site integration (the twelfth card)

Follow `PROCEDURE.md` "Adding a completed project to the site" to the letter; the
project-specific decisions are made here so execution does not re-decide them:

- **Story object** in `js/data.js`: id `fremantle-high-water`, title
  "High Water at Fremantle", year `1984–2026`, category
  `["Physical risk", "Climate data", "Data viz"]`, `vizKey: "highwater"`. Place it
  **immediately after `fremantle-sea-level`** in the `projects` array: the two are
  siblings (chronic mean, acute extremes) and the prev/next page links will pair them
  automatically.
- **Icon**: add a `waves` icon to `js/icons.js` in the house style (24 px viewBox,
  stroked paths, no fill), since the current set has nothing water-line shaped;
  fall back to `layers` only if the new icon does not land cleanly.
- **Card stat** (`result`): the headline multiplication of high-water hours, first
  decade to last decade, in the form the final numbers support (the uncorrected
  pre-check suggests roughly a tripling, but the shipped number comes from
  `analysis.py`, nowhere else).
- **Chart data**: add the `highwater` key to `js/chartdata.js` with a small script
  reading the committed CSVs, per `PROCEDURE.md` step 2. Never edit that file by hand.
- **Counts and copy** (this is the "make the homepage look right" step):
  - `js/data.js` stat band: "Projects complete" 11 → **12**.
  - `js/sections.jsx` stories intro: "Eleven finished projects" → "Twelve finished
    projects", and add the flooding story to the physical-risk list in the same
    sentence.
  - `index.html`: the `description` and `og:description` both start "Eleven Western
    Australian climate-risk analyses"; change the count and add coastal flooding to
    both lists.
  - Root `README.md`: flip this project's row from Planned to Complete, and add the
    UHSLC attribution to the licensing paragraph.
- **Build and pages**: `npm run build` (edits go in the `.jsx`, never the `.js`);
  commit the regenerated `projects/fremantle-high-water.html` and `sitemap.xml`.
- **Share card**: `node tools/build-og.js`, commit `assets/og/fremantle-high-water.png`
  (remote sessions have Chromium at `/opt/pw-browsers/chromium`; set `OG_CHROME` if
  the script does not find it).
- **Update log**: a single "First published" entry in `js/data.js` and an
  `## Update log` section in the project README, per `PROCEDURE.md`.
- **Verify** per `PROCEDURE.md`: headless render with no console errors, index cards
  4 × 3 with no empty cell at desktop width, the new page's charts, table and timeline
  present, prev/next pointing at `fremantle-sea-level` and `bushfire-weather`, and the
  em-dash greps clean.

**Definition of done**

- [ ] `tools/check-data-access.sh` shows `ok` for UHSLC, and `build_dataset.py` runs
      end to end **with no hand-staged files**.
- [ ] `test_stats.py` and `test_project.py` pass; `stats_utils.py` byte-identical
      across projects; CI green.
- [ ] README has Datum, Validation and Limitations sections covering credibility
      tests 1–6.
- [ ] `data/source-library.csv` traces every committed number to a recorded request.
- [ ] Raw and mean-adjusted exceedance counts both published; benchmarks and the
      completeness rule documented as fixed in advance.
- [ ] Front page updated per the site-integration section: story object, chart data,
      stat band at 12, intro copy, `index.html` meta, generated page, sitemap, share
      card, update log; root README row flipped to Complete; dropzone fallback
      documented in `DROP_FILES_HERE.md`.
- [ ] Zero em dashes, checked in every form.
- [ ] Draft pull request opened.

---

## Timeline (part-time, ~2 weeks)

One station, one variable, and no new index mathematics, so shorter than
`bushfire-weather/`:

| Week | Milestone |
|------|-----------|
| 1 | Access probe green, both feeds fetched and cached, splice + QC + completeness rule implemented and tested, daily and annual CSVs committed, PSMSL validation done. |
| 2 | Trends, decomposition and epochs computed; charts; README; site integration and counts; share card; interview brief; PR. |

## Alternatives considered (and when to switch)

- **Heat and the grid** (SWIS operational demand versus Perth temperature, AEMO WEM
  portal + Open-Meteo, both verified reachable): the strongest candidate for
  project #13. Passed over here because `swis-decarbonisation/` already owns the grid
  ground on the homepage, and the portfolio's bigger gap is the acute coastal story.
- **North-west extreme rainfall** (GHCN-Daily PRCP at Port Hedland and Broome, same
  parser as `extreme-heat/`): viable and fully self-service, but `wa-cyclones` already
  tells the north-west storm story, and it would be a fifth heat/rain station study.
- **Wheatbelt frost risk** (GHCN TMIN): the standing fallback if UHSLC access breaks;
  smallest scope, complements `wheat-yields/`.

## Stretch goals (only after the core ships)

- A from-scratch harmonic tide fit (least squares on the major constituents, tested
  against a published worked example) to split tide from surge and put trends on skew
  surge itself: the most impressive possible extension, kept out of the core scope on
  purpose.
- A simple Gumbel fit on annual maxima (from scratch, tested against known values) for
  return-level framing of the record's biggest events.
- An interactive benchmark slider on the project page: drag the level, the chart
  re-counts high-water hours per year client-side from data already in `CHARTDATA`.
- Re-run when the UHSLC research-quality file extends past 2021, retiring the
  fast-delivery years one by one.
