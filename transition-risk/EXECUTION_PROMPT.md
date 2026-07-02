# Execution Prompt: Transition Risk - WA's Biggest Emitters Under the Safeguard Mechanism

> Portfolio project #4 of the `adhi-climate` suite (transition climate risk).
> Paste this whole file into a fresh session to start work. Self-contained: no prior context needed.
> Mirrors the structure and proven workflow of the completed projects: `cyclone-risk/` (acute physical),
> `rainfall-decline/` (chronic physical) and `aasb-s2-review/` (disclosure gap analysis).
> This project completes the AASB S2 risk quadrant: it is the **transition risk** analysis the
> portfolio does not yet have, and it reuses the same companies as project #3 so the suite
> reads as one continuous story.

---

## Project framing

**Research question.** How exposed are Western Australia's largest emitting facilities to
Australia's reformed Safeguard Mechanism, and what does the gap between their emissions
trajectories and their declining baselines imply about compliance-cost exposure to 2030?

**CV framing.** *"Transition Climate Risk: WA's Biggest Emitters Under the Safeguard
Mechanism (2016-2024), A Facility-Level Data Analysis for AASB S2 Transition Risk
Assessment."*

**Scope.** All Safeguard Mechanism facilities located in Western Australia (roughly 40-60
facilities; confirm the exact count from the data). Company-level narrative focus on the
names a Perth employer recognises instantly: **BHP, Rio Tinto, Woodside** (the three scored
in `aasb-s2-review/`), plus whichever non-ASX operators the data shows are unavoidable in
WA (expect Chevron's Gorgon and Wheatstone LNG facilities and Alcoa's alumina refineries
to dominate; verify from the data, do not assume the ranking).

**Why it matters.** AASB S2 requires Group 1 reporters to disclose transition risks and
their *anticipated financial effects*. The Safeguard Mechanism is the sharpest, most
quantifiable transition-policy instrument in Australia: since 1 July 2023, baselines
decline every year and facilities that exceed them must surrender carbon units at real
cost. Turning public regulator data into a facility-level exposure picture is exactly the
work ESG and climate-risk teams at Deloitte, KPMG, GHD and Arup do for clients. Projects
#1 and #2 quantified the physical-risk half of AASB S2; project #3 reviewed disclosure;
this one quantifies the transition-risk half and closes the loop.

**Repo.** Umbrella repo `adhi-climate`, subfolder `transition-risk/`.

---

## Division of labour

- **Kai**: all data acquisition, cleaning, Python code, analysis, scenario modelling,
  charts, notebook structure, and the README draft.
- **Ris**: domain interpretation (what baseline decline means for LNG vs iron ore vs
  alumina, how the Safeguard interacts with company net-zero commitments, what a
  consultant would tell each company), final narrative, and interview talking points.
  Ris does not write code but must be able to speak to the findings for ~5 minutes
  without notes before this goes on a CV.

---

## ⚠ Read before starting (the credibility tests)

This project lives or dies on the same honesty rules that made #1-#3 credible.
Internalise these six points before writing any code.

1. **Scenarios, not forecasts.** Projecting emissions against declining baselines to 2030
   is a *what-if* exercise. Label every projection with its assumption ("if emissions stay
   flat at the FY2024 level", "if the FY2019-FY2024 trend continues"). Never present a
   crossover year or a dollar figure as a prediction.

2. **Surrendering units IS compliance.** A facility that exceeds its baseline and
   surrenders ACCUs or SMCs has met its obligation. Frame exceedance as *cost exposure*,
   never as "non-compliance" or wrongdoing. This is the difference between analysis and
   defamation.

3. **The time series has a seam at 1 July 2023.** The reformed Safeguard changed how
   baselines are set (production-adjusted, declining ~4.9%/yr by default) and introduced
   Safeguard Mechanism Credits (SMCs). Pre-reform and post-reform baselines are not
   comparable; emissions data is. Analyse emissions as one series and baselines as two
   regimes, and say so in the write-up. Verify the exact decline rate and the
   trade-exposed / landfill variations from the Clean Energy Regulator (CER) or DCCEEW at
   execution time; do not trust the 4.9% figure from memory.

4. **Facility boundaries move.** Facilities get renamed, split, merged, and change
   responsible emitter. Build a facility-matching table with explicit notes rather than
   fuzzy-joining names across years and hoping. Where a facility's history cannot be
   stitched cleanly, exclude it from trend analysis and log the exclusion.

5. **Carbon prices are volatile and partly administered.** Cost scenarios must use a
   *range* of ACCU prices (verify the current spot range and the cost-containment ceiling
   at execution time; the ceiling was legislated at $75 indexed, but confirm the current
   value). Present cost exposure as a sensitivity table, not a single number.

6. **No fabricated data, ever.** Every number must trace to a CER/NGER published file or
   a company report with a recorded URL and retrieval date. If a facility's figure cannot
   be verified, it does not exist for this analysis. Do not invent facility names,
   baselines, or prices.

---

## Data sources: acquire in this order

| # | Source | What to download | How to use |
|---|--------|------------------|------------|
| 1 | **CER: Safeguard Mechanism facility data** (primary), cleanenergyregulator.gov.au | Published annual Safeguard facility-level data: facility name, responsible emitter, state, covered (scope 1) emissions, baseline, and units surrendered (ACCUs / SMCs), for every available compliance year (2016-17 onward; the first reformed year is 2023-24). CSV/Excel. | The spine of the project. Filter to WA. Baseline vs emissions per facility per year is the whole exposure story. |
| 2 | **CER: NGER designated large facilities / facility-level emissions data** | Facility-level scope 1, scope 2 and energy data for all published years. | Cross-checks Safeguard covered emissions, adds scope 2 context and non-Safeguard large facilities for the concentration picture. |
| 3 | **CER: SMC issuance data + ACCU market data** | SMCs issued by facility (2023-24 onward); ACCU spot/auction price history (CER quarterly carbon market reports, or Jarden/CORE markets summaries if CER is insufficient). | SMC issuance shows who is *under* baseline (earning credits). Price history anchors the cost-scenario range. |
| 4 | **DCCEEW: Safeguard Mechanism rules** (reference, not data) | The reform explainer and legislated decline rates, trade-exposed provisions, cost-containment settings. | Source for the projection assumptions. Cite the actual instrument; verify every rate. |
| 5 | **Company reports** (secondary, already gathered for project #3) | BHP / Rio Tinto / Woodside climate reports: their own stated Safeguard exposure, net-zero targets, ACCU strategies. | Compare "what the regulator's data shows" against "what the company says". This is the bridge back to `aasb-s2-review/`. |

**Why CER data instead of company disclosures?** Same reason projects #1 and #2 used
GHCN-Daily: it is the authoritative, uniform, script-downloadable source, and every
company is measured with the same ruler (NGER methods). Company reports become the
cross-check, not the spine.

Build the provenance log before analysis: `data/source-library.csv` with columns
`source, file, compliance_year, url, date_retrieved` - one row per downloaded file.

---

## Analysis steps

| # | Step | Detail | Output |
|---|------|--------|--------|
| 1 | Data acquisition & cleaning | Download all Safeguard and NGER facility files. Normalise column names across years (they change). Filter to WA. Build the facility-matching table across years with explicit notes for renames/splits. Tidy panel: facility, responsible emitter, parent company, sector, year, scope 1, baseline, units surrendered, SMCs issued. | `data/safeguard_wa_clean.csv`, `data/facility_matching.csv` |
| 2 | Concentration picture | How concentrated are WA's industrial emissions? Top-10 facilities' share of WA Safeguard emissions, sector mix (LNG, iron ore, alumina, nickel, other), company-level totals. | `data/concentration_summary.csv` + chart 01 |
| 3 | Emissions trends | Facility- and sector-level trends 2016-17 to latest, using the suite's standard tools: Mann-Kendall + Sen's slope (reuse the `stats_utils.py` pattern from projects #1-#2), with OLS slope + 95% CI as the parametric cross-check. Report which facilities/sectors are genuinely declining vs flat vs growing. | `data/trend_summary.csv` + chart 02 |
| 4 | Baseline headroom | For each focus facility: emissions vs baseline for every year, headroom (baseline − emissions) in kt and %, and the post-reform trajectory of that headroom as baselines decline to 2029-30. | `data/headroom_summary.csv` + chart 03 |
| 5 | Crossover scenarios | Under (a) flat emissions at latest year, (b) continuation of each facility's fitted Sen's slope: which year does each focus facility cross its declining baseline? Report as a scenario table with assumptions stated in the table itself. | `data/crossover_scenarios.csv` + chart 04 |
| 6 | Cost-exposure sensitivity | Cumulative shortfall to 2030 under each scenario × ACCU price band (low / mid / ceiling; values verified at execution time). Company-level roll-up for BHP, Rio Tinto, Woodside. Explicitly labelled illustrative. | `data/cost_scenarios.csv` + chart 05 |
| 7 | Disclosure bridge | One-page comparison per focus company: what this analysis shows vs what their climate report discloses about Safeguard exposure (pull from project #3's source library). Where the company's own numbers differ, say so and prefer theirs for forward statements - they know their production plans; we do not. | section in README + chart 06 |

---

## Statistics and honesty rules

- Reuse the **from-scratch, tested** statistics pattern: `stats_utils.py` implementing
  Mann-Kendall, Sen's slope and OLS with CI, plus `test_stats.py` validating against
  known values (copy the test approach, not the code blindly - emissions panels are
  shorter and lumpier than 75-year rainfall series, so also test small-n behaviour).
- Trend claims only where n ≥ 8 annual observations; otherwise report levels, not trends.
- Every projection carries its assumption in the same sentence. Every dollar figure is a
  range. The words "forecast" and "predict" do not appear in the write-up.

## Charts (target 5-6, matplotlib, suite house style)

1. **Concentration**: ranked bar of WA Safeguard facilities' scope 1 emissions, coloured
   by sector, focus companies annotated.
2. **Sector trends**: small-multiple time series 2016-17 to latest with Sen's slope.
3. **Headroom**: per focus facility, emissions line vs baseline line with the reform seam
   marked and the post-2023 baseline decline shown to 2029-30.
4. **Crossover fan**: scenario trajectories vs declining baseline for the headline facility.
5. **Cost sensitivity**: heatmap or grouped bar - scenario × price band → cumulative $ exposure.
6. *(Optional)* Surrender mix: ACCUs vs SMCs surrendered/issued in WA, 2023-24 onward.

---

## Repo layout & deliverables

Mirror the completed projects exactly:

```
transition-risk/
├── EXECUTION_PROMPT.md      (this file)
├── README.md                (plain-English write-up, same voice as #1-#2)
├── build_dataset.py         (download + clean, re-runnable from scratch)
├── analysis.py              (all numbers in the README come from here)
├── stats_utils.py           (from-scratch stats, tested)
├── test_stats.py
├── viz.py                   (all charts)
├── transition_analysis.ipynb
├── requirements.txt
├── data/                    (clean CSVs committed; raw downloads gitignored)
├── charts/
├── INTERVIEW_BRIEF.md
└── cv-blurb.txt
```

**Definition of done**
- [ ] `build_dataset.py` re-runs from scratch on a clean machine (raw files re-downloadable or cached with recorded URLs).
- [ ] `test_stats.py` passes; every statistic in the README is produced by `analysis.py`.
- [ ] README follows the suite voice: one-paragraph summary up top, plain-English explanations of every technical term, a Validation section cross-checking totals against CER's own published aggregates and company-reported figures, and a Limitations section covering points 1-5 above.
- [ ] INTERVIEW_BRIEF.md and cv-blurb.txt written; Ris can talk to the findings for 5 minutes unaided.
- [ ] Root `README.md` table row flipped from Planned to Complete.

---

## Timeline (part-time, ~4 weeks)

| Week | Milestone |
|------|-----------|
| 1 | Data acquisition, facility matching table, clean panel built and validated against CER published totals. |
| 2 | Steps 2-5: concentration, trends, headroom, crossover scenarios. Stats tested. |
| 3 | Step 6-7: cost sensitivity, disclosure bridge. All charts. README drafted. |
| 4 | Validation pass, limitations honed, interview brief, CV blurb, root README updated. |

## Stretch goals (only after the core ships)

- Integrate into the portfolio site (`index.html` + `js/`) as the fourth case-study card,
  following the existing data-file pattern (`js/aasbdata.js` is the closest precedent).
- Extend the concentration picture Australia-wide for context (WA's share of national
  Safeguard emissions).
- An interactive headroom explorer (facility picker → trajectory chart) on the site.
