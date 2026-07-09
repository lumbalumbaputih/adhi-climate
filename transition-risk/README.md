# Transition Climate Risk: WA's Biggest Emitters Under the Safeguard Mechanism (2016–2025)

A data analysis written for **AASB S2 transition-risk assessment** (AASB S2 is
Australia's mandatory climate-disclosure standard). The Safeguard Mechanism is
Australia's sharpest transition-policy instrument: since 1 July 2023 every
large facility's emissions baseline declines each year, and a facility that
ends the year above its baseline must surrender carbon units at real cost.
This project turns the Clean Energy Regulator's published facility data into
a WA exposure picture: who emits, who is above their baseline already, and
what staying still would cost.

> **Status: complete.** Every number below is computed by `analysis.py` from
> the CER's published Safeguard facility files for all nine compliance years
> (2016-17 to 2024-25), downloaded by the session itself from cer.gov.au; see
> [dropzone/DROP_FILES_HERE.md](../dropzone/DROP_FILES_HERE.md). The framing
> rules in [EXECUTION_PROMPT.md](EXECUTION_PROMPT.md) apply throughout:
> scenarios are what-ifs, not forecasts, and **exceeding a baseline and
> surrendering units is compliance**, never wrongdoing.

## Research question

How exposed are Western Australia's largest emitting facilities to the
reformed Safeguard Mechanism, and what does the gap between their emissions
and their declining baselines imply about compliance-cost exposure to
2029-30?

## Results

- **WA's industrial emissions are concentrated and LNG-heavy.** In 2024-25,
  81 WA facilities reported 47.2 Mt CO2-e of covered emissions; the top ten
  hold 66%. LNG and oil/gas contribute 24.1 Mt (over half), then metal ore
  mining (10.0 Mt) and alumina (6.1 Mt). Chevron alone (Gorgon + Wheatstone)
  covers 13.0 Mt; Woodside's five facilities 8.2 Mt.
- **Emissions are not falling yet.** WA covered emissions drifted up about
  +0.4 Mt a year over 2016-2024 (not significant, Mann-Kendall p = 0.25).
  The significant rises are metal ore mining (+0.61 Mt/yr, p = 0.001) and
  transport (+0.10 Mt/yr, p = 0.005); LNG is up but noisy. Nothing in the WA
  panel is significantly declining.
- **The reform already bites: 56 of 81 WA facilities were above their
  baselines in 2024-25**, including four of the six biggest (Gorgon, North
  West Shelf, Worsley, Pluto). They comply by surrendering ACCUs and SMCs:
  WA facilities surrendered about 3.9 million units for 2024-25, while WA's
  under-baseline facilities earned 2.3 million SMCs (Prelude FLNG alone
  1.4 million).
- **The crossover question is mostly answered, and the answer is "already".**
  Under the default baseline decline of 4.9% a year, a facility that merely
  holds its 2024-25 emissions flat stays (or goes) above baseline: Gorgon,
  North West Shelf, Worsley and Pluto are already above; Wheatstone crosses
  in 2025-26 in the flat scenario. Prelude FLNG, running well below its
  baseline, is the exception and does not cross by 2029-30.
- **Cost exposure is material but manageable at spot, and triples at the
  ceiling.** Cumulative 2025-26 to 2029-30, flat-emissions scenario, ACCUs
  at the March-2026 spot of $37.50: about **$310 m for Gorgon, $297 m for
  North West Shelf, $103 m for Wheatstone, $104 m for Worsley, $72 m for
  Pluto**, roughly $0.9 bn across the six focus facilities. At the
  legislated cost-containment ceiling path the same shortfalls cost about
  $2.2 bn. Every figure is illustrative and carries its assumption in the
  output row.

**What this means for AASB S2 work.** For WA reporters the Safeguard is no
longer a future risk: most large facilities are already in structural
shortfall against declining baselines, so the disclosure question shifts
from "when could this bind" to "what does the unit bill do to operating cost,
and what abatement changes the trajectory". The concentration picture also
matters for banks and insurers: two companies carry almost half of WA's
covered emissions.

## Data

| Source | What it provides | Used for |
|--------|------------------|----------|
| **CER Safeguard facility files**, one per compliance year 2016-17 to 2024-25 (cer.gov.au) | Facility name, responsible emitter, state, baseline, covered emissions, ACCUs/SMCs surrendered, SMCs issued | The whole panel |
| **DCCEEW Safeguard reform settings** | Default baseline decline of 4.9% a year to 2029-30 | The scenario baseline path (verified at execution, 2026-07-07) |
| **CER Quarterly Carbon Market Report** (March quarter 2026) and the legislated cost-containment measure | Generic ACCU spot about $37.50; ceiling $82.68 in 2025-26, indexed CPI+2% | The price band in the cost scenarios |

## Method

1. `build_dataset.py` normalises the nine CER vintages (column names shift
   between years; the parser matches by keyword and logs what it matched),
   filters to WA, buckets sectors from ANZSIC (backfilled to pre-reform
   years from each facility's most recent classification), builds the
   facility-matching table, and **flags multi-year-monitoring-period
   baselines** (cumulative, not annual; e.g. North West Shelf 2016-17 shows
   22.7 Mt) so they are excluded from headroom rather than silently mixed in.
2. `analysis.py` computes concentration, sector trends (the suite's
   Mann-Kendall + Sen + OLS battery), per-facility headroom by regime,
   flat-vs-trend crossover scenarios against the default declining baseline,
   and the cost-sensitivity table across the price band. Baselines are never
   compared across the 1 July 2023 reform seam.
3. `viz.py` draws the five charts in `charts/`.

Statistics are the suite's byte-identical `stats_utils.py` (validated in
`test_stats.py`); parser and scenario arithmetic are tested on synthetic
inputs in `test_project.py`. Both run in CI.

## Limitations (write-up must keep these)

- **Scenarios are not forecasts.** Companies have production plans,
  abatement projects and TEBA decline-rate variations this analysis cannot
  see. Where a company's own disclosure differs, prefer theirs for
  forward-looking statements.
- **The default 4.9% decline is not universal**: trade-exposed
  baseline-adjusted facilities can have lower decline rates, and borrowing /
  MYMP flexibilities shift timing. The crossover table is the default-path
  view.
- **Unit prices are volatile and partly administered.** The band ($30 /
  $37.50 spot / ceiling path) is a snapshot with sources and retrieval date;
  it will drift.
- **Facility boundaries move.** Renames, splits and responsible-emitter
  changes are handled by a matching table with the name variants recorded;
  ambiguous histories are excluded from facility trend claims rather than
  fuzzy-joined.
- **Covered emissions are scope 1 only** as defined by the Safeguard; scope
  2 and downstream (scope 3) exposure of the same companies is out of scope
  here.

## Reproduce

```bash
pip install -r requirements.txt
# download the nine CER facility files into ../dropzone/transition-risk/
# (see dropzone/DROP_FILES_HERE.md for the exact pages), then:
python3 build_dataset.py
python3 analysis.py
python3 viz.py
python3 test_stats.py && python3 test_project.py
```

## Update log

**2026-07-07 · First published.** Built from all nine CER compliance years,
downloaded directly from cer.gov.au by the session. The multi-year-monitoring
trap surfaced immediately (North West Shelf's 2016-17 "baseline" is a 22.7 Mt
cumulative figure) and is handled by flagging from the CER files' own MYMP
column rather than a heuristic. Scenario parameters (4.9% decline, $37.50
spot, $82.68 ceiling) were verified against DCCEEW and CER pages on the day
of analysis and are recorded with the outputs.
