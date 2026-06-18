# Execution Prompt: SW WA Rainfall Decline (1950–2024)

> Portfolio project #2 of the `adhi-climate` suite (chronic physical climate risk).
> Paste this whole file into a fresh session to start work. Self-contained, no prior context needed.
> Mirrors the structure and proven workflow of the completed cyclone project (`adhi-climate/cyclone-risk/`).

---

## Project framing

**Research question.** Has cool-season (April–October) rainfall in South West WA declined significantly since the 1970s step-change, and what does the full 1950–2024 record show about the magnitude and persistence of the shift?

**CV framing.** *"Chronic Physical Climate Risk: South West WA Rainfall Decline (1950–2024), A Data Analysis for AASB S2 Physical Risk Assessment."*

**Geographic scope.** BOM South West Land Division (SWLD), Perth metro, the SW agricultural / wheatbelt zone, and the high-rainfall zone (Pemberton / Albany).

**Why it matters.** Water utilities (Water Corporation), agriculture and agri-finance, ESG consultancies (Deloitte, GHD, Arup), and state government (DWER) all need this quantified under AASB S2 chronic physical risk. Target: live on GitHub before Deloitte graduate applications open 1 July 2026.

**Repo.** Umbrella repo `adhi-climate`, subfolder `rainfall-decline/`.

---

## Division of labour

- **Kai**, all data acquisition, cleaning, Python code, analysis, charts, notebook structure, and the README draft.
- **Ris**, domain interpretation (what the decline means for WA water, agriculture, fire risk and policy), attribution nuance, final narrative, and interview talking points. Ris does not write code but must be able to speak to the findings for ~5 minutes without notes before this goes on a CV.

---

## ⚠ Attribution: read before starting

The rainfall **decline** is robust and uncontested. The **cause** is not fully settled. Handle drivers two ways:

1. **Referenced summary** drawn from BOM and CSIRO, the backbone. Cover the candidate drivers: Southern Annular Mode (SAM) trend, Indian Ocean Dipole (IOD), ENSO, intensification of the subtropical ridge / rising mean sea-level pressure, and direct anthropogenic forcing.
2. **Quantitative driver correlation** against IOD, SAM and ENSO indices, explicitly labelled **illustrative, not causal**.

Correlation shows association consistent with the literature; it does **not** establish attribution, which requires formal detection-attribution modelling. Do not present it as proof of cause, and **do not invent citations or DOIs**, verify every reference at write-up.

---

## Data sources: acquire in this order

| # | Source | What to download | How to use |
|---|--------|------------------|------------|
| 1 | **BOM Climate Change time series** (primary headline), bom.gov.au/climate/change | "South West of Western Australia" rainfall, **April–October**, annual values 1950–2024 (CSV export from the time-series tool) | BOM's own pre-computed regional cool-season series, the most authoritative, least error-prone source for the headline signal. Use it as the spine. Export raw annual totals; compute anomalies yourself against the 1950–1974 baseline. |
| 2 | **BOM Climate Data Online** (station cross-check), bom.gov.au/climate/data | Monthly rainfall for 6 long-record SWLD stations. Candidates: Perth Airport, Dwellingup, Manjimup, Bridgetown, Pemberton, Katanning, Albany, Wandering. | **Confirm each station number on CDO, do not trust IDs from memory.** Pick the 6 with the most complete continuous 1950–2024 records (target <5% missing months). Verifies the regional signal at individual sites and adds spatial texture (coastal vs inland, high-rainfall zone vs wheatbelt). |
| 3 | **Climate driver indices** (exploratory correlation) | IOD: Dipole Mode Index (DMI). SAM: Marshall / AAO index. ENSO: SOI (BOM) or Niño 3.4 (NOAA). Monthly, 1950–2024. | Aggregate each index to the April–October season; correlate against the regional cool-season rainfall anomaly. Pearson r + p, labelled illustrative. DMI / Niño from NOAA PSL; SOI from BOM; SAM / AAO from BOM or NOAA. |
| 4 | **AGCD gridded rainfall** (OPTIONAL / stretch), bom.gov.au | Gridded monthly rainfall, SWLD extent | Only if time allows and NetCDF handling works in the sandbox. Feeds the decade choropleth (Step 6). Ship the core analysis first. |
| 5 | **CSIRO State of the Climate + IOCI** (attribution sources), csiro.au | Latest State of the Climate report; Indian Ocean Climate Initiative summaries | Source material for the referenced attribution summary only, not data. Cite specific figures; do not paraphrase into invented precision. |

---

## Analysis steps

| # | Step | Detail | Output |
|---|------|--------|--------|
| 1 | Data acquisition & cleaning | Load the BOM SW WA April–October regional series. Load 6 station monthly records; aggregate each to April–October totals; flag and document missing months, do not silently fill; drop or interpolate explicitly and note which. Tidy CSV: station/region, year, cool-season total (mm). | `data/rainfall_swwa_clean.csv` |
| 2 | Anomaly series | April–October anomaly vs 1950–1974 baseline for the regional series and each station. Add May–July as a secondary series (strongest-signal sub-season). Report % change vs baseline, **compute it; do not assume the "~20%" figure**. | `data/annual_cool_season_anomaly.csv` + time-series chart |
| 3 | Step-change detection | Pettitt test (non-parametric change-point) on the regional cool-season series to locate the change-point year. Compare pre/post means (1950–1974 vs 1975–2024; also isolate 2000–2024). Annotate the ~1975 and ~2000 inflections. | `data/stepchange_summary.csv` + annotated step-change chart |
| 4 | Trend analysis | Mann-Kendall + Sen's slope on the full series and the post-1975 series. OLS for slope and 95% CI. Report direction, magnitude (mm/decade and % decline) and significance. | Trend chart with regression line, CI band, p-value |
| 5 | Driver correlation (exploratory) | Correlate cool-season rainfall anomaly against April–October DMI (IOD), SAM and SOI / Niño 3.4 (ENSO). Pearson r + p each; optional multiple regression (flag multicollinearity). Pair with the referenced BOM / CSIRO attribution summary. **Label illustrative, not causal.** | `data/driver_correlation.csv` + correlation chart + README attribution section |
| 6 | Spatial map (OPTIONAL / stretch) | If AGCD is accessible: decade choropleth of SWLD April–October rainfall anomaly (1950s … 2010s/2020s). Skip without guilt if NetCDF handling is fiddly, the core analysis stands alone. | Decade map (optional) |
| 7 | Write-up | README.md in plain English for a climate-literate non-coder: research question → data → key findings → step-change → trend → drivers (referenced + illustrative correlation) → what it means for WA water/ag/policy and AASB S2 chronic risk → limitations → reproduce. CV blurb: 3 sentences (WA, 1950–2024, AASB S2 chronic physical risk, key finding). INTERVIEW_BRIEF.md: ~5-minute talking points. | `README.md` · `cv-blurb.txt` · `INTERVIEW_BRIEF.md` |

---

## Repo structure (what done looks like)

```
adhi-climate/
└── rainfall-decline/
    ├── README.md
    ├── requirements.txt
    ├── rainfall_analysis.ipynb
    ├── build_dataset.py        # download + clean BOM rainfall and driver indices
    ├── analysis.py             # anomalies, step-change, trend, correlation
    ├── stats_utils.py          # Mann-Kendall, Sen's slope, Pettitt, OLS, Pearson (from scratch)
    ├── test_stats.py           # unit tests for stats_utils
    ├── viz.py                  # chart generation
    ├── cv-blurb.txt
    ├── INTERVIEW_BRIEF.md
    ├── data/
    │   ├── raw/                            # gitignored, raw BOM downloads
    │   ├── rainfall_swwa_clean.csv
    │   ├── annual_cool_season_anomaly.csv
    │   ├── stepchange_summary.csv
    │   └── driver_correlation.csv
    └── charts/
        ├── 01_timeseries_anomaly.png
        ├── 02_stepchange.png
        ├── 03_trend_mannkendall.png
        ├── 04_driver_correlation.png
        └── 05_decade_map.png               # optional / stretch
```

---

## Technical constraints

| Constraint | Reason |
|------------|--------|
| Python only (pandas, numpy, matplotlib). Implement statistics from first principles, Mann-Kendall, Sen's slope, Pettitt, OLS, Pearson, and reuse the cyclone project's `stats_utils.py` as the starting point | scipy would not install in the sandbox on project #1; from-scratch stats kept it reproducible. Don't assume scipy is available. |
| Unit-test every stat function against known / textbook values (`test_stats.py`) | Hand-rolled stats must be proven correct, part of what made project #1 credible. |
| Notebook runs top-to-bottom on a fresh environment; include `requirements.txt` | Reproducibility is part of the portfolio value. |
| Charts: 300dpi PNG, labelled axes with units (mm, mm/decade), clean style. Match the cyclone project's palette for a coherent two-project portfolio | These go on LinkedIn and the CV. |
| Handle missing months explicitly; document the 1950–1974 baseline choice and test sensitivity to it | Gap handling and baseline choice both move the headline number, be transparent. |
| Compute the % decline from the data, do not assume the "~20%" figure | Report what the data show, not the literature's round number. |
| Distinguish observed decline (robust) from cause (contested); driver correlation is illustrative, not causal; never fabricate citations or DOIs | Attribution honesty is the whole credibility test for this project. |

---

## Session start instruction

Start with **Step 1**. Confirm the BOM "South West of Western Australia" April–October series downloaded correctly and show the first 10 and last 10 years before any analysis. Then confirm the 6-station list and each station's record completeness before aggregating.

---

## Interview-readiness bar (for Ris, before this goes on a CV)

Be able to speak, unaided, for ~5 minutes to: (1) what the step-change is and roughly when it occurred; (2) what it means for WA water security, agriculture and fire risk; (3) why the attribution question matters, without overstating the uncertainty. Kai will prepare the INTERVIEW_BRIEF once the analysis is done.
