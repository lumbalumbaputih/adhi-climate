# AASB S2 Readiness Review: WA's Biggest Emitters

A structured gap analysis of how three of Western Australia's largest ASX-listed emitters disclose against the four pillars of AASB S2, Australia's mandatory climate-related disclosure standard. This is a self-directed portfolio project framed around the work ESG and sustainability consultants do: read the reports, apply the framework, find the gaps, explain what they mean.

Companies reviewed: BHP, Woodside Energy and Rio Tinto.

## Method

Each company was scored against 31 AASB S2 sub-requirements grouped under the four pillars (Governance, Strategy, Risk Management, Metrics and Targets), on a 0 to 4 scale, from its actual public reports. The reports were read in full from primary text and every non-zero score carries a citation to the report's own section or page. Scoring was deliberately conservative: where the evidence sat between two scores, the lower was taken and the reason recorded. The full evidence sits in `scoring-matrix.csv`, with a per-company write-up in each `*-scorecard.md` and the cross-company patterns in `gap-summary.csv`.

One caveat runs through the whole review. This measures disclosed readiness, not actual readiness. A low score means a company has not published something AASB S2 expects; it does not prove the company lacks the underlying capability. Equally, a high score means the disclosure is complete, not that the company faces low climate risk. Those two things are different, and keeping them apart is the core analytical skill this project demonstrates.

## Reporting status matters

The three companies are not at the same point in the mandatory timeline. All three are Group 1 entities, but Rio Tinto and Woodside have December year-ends, so their CY2025 reports are their first mandatory AASB S2 disclosures. BHP has a June year-end, so its FY2025 report is still a voluntary, TCFD-aligned disclosure, and its first mandatory AASB S2 report will be FY2026. Reading the two cohorts side by side shows what the mandatory regime changes in practice.

## Results

| Company | Governance | Strategy | Risk Mgmt | Metrics & Targets | Overall | Band |
|---------|:---:|:---:|:---:|:---:|:---:|---|
| Rio Tinto | 3.7 | 3.7 | 3.5 | 3.9 | **3.69** | Advanced |
| Woodside | 3.8 | 3.2 | 3.3 | 3.1 | **3.35** | Advanced |
| BHP | 3.0 | 3.0 | 3.0 | 2.8 | **2.94** | Developing |

## Key findings

Rio Tinto sets the disclosure bar. It is the only one of the three that answers the AASB S2 cross-industry metrics in quantified form: the percentage of assets exposed to physical risk with an annualised damage score, the percentage of Scope 1 emissions covered by emissions-limiting regulation, an internal carbon price range, and the percentage of executive remuneration linked to climate. It also discloses both market-based and location-based Scope 2, a full Scope 3 inventory, and the most ambitious operational target of the three (a 50 per cent cut by 2030 against a 2018 baseline).

The mandatory regime lifts completeness, but not evenly. Both first-mandatory reporters (Rio Tinto and Woodside) score in the Advanced band and above BHP's still-voluntary disclosure, which is what you would expect. But mandatory status alone does not guarantee depth: Woodside, though reporting under AASB S2, still leaves the percentage-of-assets-at-risk metrics qualitative, exactly where Rio Tinto quantifies them. The lift comes from a company choosing to do the harder quantification, not simply from the calendar.

The clearest common gaps are the cross-industry asset-exposure metrics and financial quantification. Across the three companies, the weakest sub-requirements are the amount or percentage of assets vulnerable to transition risk, vulnerable to physical risk, and aligned with climate opportunities, together with the quantification of climate-related financial effects on the business. Only Rio Tinto scores well on the first three; all three companies are partial on financial-effect quantification. This mirrors what AASB S2 was designed to force into the open and where the market is least mature.

Scope 3 targets are the substantive weakness even at the top. BHP frames net zero Scope 3 as an uncertain goal rather than a target. Woodside has a Scope 3 investment target and an abatement target but no absolute Scope 3 reduction target. Rio Tinto has the broadest set of Scope 3 targets, but they are largely action or intensity based rather than an absolute cut. For all three, Scope 3 dwarfs operational emissions (Rio Tinto's 575.7 Mt against roughly 31.5 Mt operational), so this is where disclosed ambition is furthest from the scale of the problem.

Strong disclosure is not the same as low risk. Woodside is the clearest example. Its governance and remuneration disclosure is excellent (climate is an explicit 15 per cent of the executive scorecard, and it states an internal carbon price of US$80 per tonne), yet the same report describes an LNG-growth strategy whose transition risk is precisely what AASB S2 exists to surface, and a net Scope 1 and 2 target met partly through carbon credits. Good disclosure and high exposure can sit in the same company, and the review keeps them separate.

## What a consultant would recommend

For BHP, move the cross-industry metrics from narrative to numbers before FY2026, quantify the percentage of assets exposed to physical and transition risk, state the internal carbon price level, and disclose the percentage of incentive tied to climate. For Woodside, set an absolute Scope 3 reduction target and reduce reliance on offsets in the headline Scope 1 and 2 target. For Rio Tinto, convert the action and intensity based Scope 3 targets toward an absolute trajectory. Across all three, deepen the quantification of climate-related financial effects, which is the common weak point and the hardest part of the standard.

## Limitations

Scores reflect public disclosure only and a single reviewer's reading; a few governance and remuneration sub-requirements were cross-referenced rather than read line by line and are flagged in the matrix and scorecards for verification. Page citations are to the reports' own section and page numbers. AASB S2 reproduces IFRS S2 content, so the pillar structure is faithful, but the standard text itself should be checked for any edge case before these scores are presented as definitive.

## Files

`scoring-matrix.csv` (all 93 scored cells with evidence), `gap-summary.csv` (cross-company patterns), `bhp-scorecard.md`, `woodside-scorecard.md`, `rio-tinto-scorecard.md`, `data/source-library.csv`, and `EXECUTION_PROMPT.md` (the method spec). Source reports are in `data/raw/`.
