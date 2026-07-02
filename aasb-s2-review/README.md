# AASB S2 Readiness Review: WA's Biggest Emitters

This is a careful, step-by-step look at how three of Western Australia's largest ASX-listed emitters report on climate. It checks their disclosures against the four pillars of AASB S2 (Australia's new mandatory rules that require big companies to disclose climate-related information). The four pillars are governance, strategy, risk management, and metrics and targets. This is a self-directed portfolio project, built to mirror the work that ESG and sustainability consultants do: read the reports, apply the framework, find the gaps, and explain what they mean. (ESG stands for environmental, social and governance, the lens investors use to judge how responsibly a company is run.)

Companies reviewed: BHP, Woodside Energy and Rio Tinto.

## Method

Each company was scored against 31 AASB S2 sub-requirements (the detailed individual items the standard asks for). These 31 items are grouped under the four pillars (governance, strategy, risk management, and metrics and targets). Each item was scored on a 0 to 4 scale, using the company's own public reports. The reports were read in full from the original text, and every score above zero comes with a citation pointing to the report's own section or page. The scoring was kept deliberately cautious: where the evidence sat between two scores, the lower one was chosen and the reason was written down. All the supporting evidence sits in `scoring-matrix.csv`. There is a separate write-up for each company in the matching `*-scorecard.md` file, and the patterns that show up across all three companies are in `gap-summary.csv`.

**What each score means.** So a reader can judge the judgements, here is the anchor for every level of the 0 to 4 scale:

| Score | Anchor |
|:-----:|--------|
| 0 | Absent: not addressed in any material way in public disclosures |
| 1 | Acknowledged: mentioned but qualitative only; no quantification, no process disclosed |
| 2 | Partial: framework element present but incomplete (for example, scenario analysis started but limited in scope) |
| 3 | Substantially compliant: meets most of the AASB S2 requirement for the item; minor gaps only |
| 4 | Full: comprehensive disclosure; third-party verified or assured where applicable |

**How the numbers roll up.** A pillar score is the plain average of that pillar's sub-requirement scores, and the overall score is the plain average of the **four pillar scores** (equal weight per pillar, not per item). The distinction matters because the pillars are different sizes: Metrics and Targets has 13 of the 31 items, so an average over items would tilt the overall score toward that one pillar. Weighting the pillars equally treats the standard's four questions as equally important. (For transparency: on an item-weighted basis Rio Tinto would score 3.74 rather than 3.69, Woodside 3.29 rather than 3.35, and BHP 2.90 rather than 2.94. No ranking or band changes either way.) Maturity bands: 0.0 to 1.0 Nascent, 1.1 to 2.0 Emerging, 2.1 to 3.0 Developing, 3.1 to 4.0 Advanced.

**How sturdy are the bands?** 21 of the 93 scored cells are marked medium confidence (checked by cross-reference rather than a full line-by-line read; they are flagged in the matrix). `sensitivity.py` moves every one of those scores down one point, then up one point, and recomputes the bands. Rio Tinto and Woodside stay Advanced in both directions. BHP stays Developing in the downward case; only if **all twelve** of its medium-confidence items resolved a full point upward would it cross into Advanced (3.31), which is an extreme assumption rather than a likely one. So the headline bands are robust to the acknowledged uncertainty, with that one caveat stated.

One important point runs through the whole review. This measures how well a company discloses, not how ready it actually is. A low score means the company has not published something AASB S2 expects to see. It does not prove the company lacks the underlying ability. In the same way, a high score means the disclosure is complete, not that the company faces low climate risk. Those two things are different, and keeping them apart is the core skill this project is built to show.

## Reporting status matters

The three companies are not at the same point in the mandatory timeline. All three are Group 1 entities (the largest companies, which have to start reporting first). But Rio Tinto and Woodside both close their books in December, so their CY2025 reports are their first reports that must follow AASB S2. BHP closes its books in June, so its FY2025 report is still voluntary and follows TCFD (the Task Force on Climate-related Financial Disclosures, the older, voluntary framework that AASB S2 grew out of). BHP's first mandatory AASB S2 report will be FY2026. Reading the two groups side by side shows what the mandatory rules actually change in practice.

## Results

| Company | Governance | Strategy | Risk Mgmt | Metrics & Targets | Overall | Band |
|---------|:---:|:---:|:---:|:---:|:---:|---|
| Rio Tinto | 3.7 | 3.7 | 3.5 | 3.9 | **3.69** | Advanced |
| Woodside | 3.8 | 3.2 | 3.3 | 3.1 | **3.35** | Advanced |
| BHP | 3.0 | 3.0 | 3.0 | 2.8 | **2.94** | Developing |

## Key findings

Rio Tinto sets the bar for disclosure. It is the only one of the three that answers the AASB S2 cross-industry metrics with actual numbers. (Cross-industry metrics are the standard, comparable figures every company has to report, no matter what sector it is in.) Rio Tinto reports the percentage of assets exposed to physical risk along with an annualised damage score, the percentage of Scope 1 emissions covered by emissions-limiting regulation, an internal carbon price range, and the percentage of executive pay linked to climate. (Scope 1 emissions are the emissions a company makes directly from its own operations. An internal carbon price is a made-up cost per tonne of emissions that a company applies to its own decisions to factor in climate risk.) Rio Tinto also discloses both market-based and location-based Scope 2 (Scope 2 is the emissions from the electricity the company buys; the two methods are just two accepted ways of measuring it), a full Scope 3 inventory (Scope 3 is the emissions from everyone else in the company's value chain, including customers using its products, rather than from the company's own operations), and the most ambitious operational target of the three (a 50 per cent cut by 2030 against a 2018 baseline).

The mandatory rules lift completeness, but not evenly. Both companies reporting under the rules for the first time (Rio Tinto and Woodside) land in the Advanced band and score above BHP's still-voluntary disclosure, which is what you would expect. But being mandatory on its own does not guarantee depth. Woodside, even though it reports under AASB S2, still leaves the percentage-of-assets-at-risk metrics as words rather than numbers, exactly where Rio Tinto puts in figures. The lift comes from a company choosing to do the harder work of quantifying, not simply from the calendar moving on.

The clearest shared gaps are the cross-industry asset-exposure metrics and putting a dollar figure on climate effects. Across the three companies, the weakest items are the amount or percentage of assets at risk from the shift to a low-carbon economy (transition risk), the amount or percentage at risk from the physical effects of climate change such as floods and heat (physical risk), the amount or percentage lined up with climate opportunities, and putting numbers on the financial effects of climate on the business. Only Rio Tinto scores well on the first three. All three companies are only partial on putting numbers to financial effects. This is exactly what AASB S2 was built to force into the open, and it is where the market is least mature.

Scope 3 targets are the real weakness, even at the top. BHP describes net zero Scope 3 as an uncertain goal rather than a firm target. Woodside has a Scope 3 investment target and an abatement target, but no absolute target to cut Scope 3 emissions. Rio Tinto has the widest set of Scope 3 targets, but they are mostly about specific actions or about intensity (emissions per unit of output) rather than an absolute cut in the total. For all three, Scope 3 is far larger than operational emissions (Rio Tinto's 575.7 Mt against roughly 31.5 Mt operational). So this is where the ambition they disclose is furthest from the real size of the problem.

Strong disclosure is not the same as low risk. Woodside is the clearest example. Its disclosure on governance and pay is excellent: climate is an explicit 15 per cent of the executive scorecard, and it states an internal carbon price of US$80 per tonne. Yet the same report describes a strategy built on growing its LNG business (LNG is liquefied natural gas, a fossil fuel), and the transition risk in that strategy is exactly what AASB S2 exists to bring to light. The same report also shows a net Scope 1 and 2 target that is met partly through carbon credits (paying for emissions cuts elsewhere to offset its own). Good disclosure and high exposure can sit inside the same company, and this review keeps the two apart.

## What a consultant would recommend

For BHP: turn the cross-industry metrics from words into numbers before FY2026, put a figure on the percentage of assets exposed to physical and transition risk, state the level of its internal carbon price, and disclose the percentage of incentive pay tied to climate. For Woodside: set an absolute target to cut Scope 3 emissions, and lean less on offsets in its headline Scope 1 and 2 target. For Rio Tinto: shift its action-based and intensity-based Scope 3 targets toward an absolute path of cuts. For all three: go deeper on putting numbers to the financial effects of climate, which is the common weak point and the hardest part of the standard.

## Limitations

These scores reflect public disclosure only, and one reviewer's reading. A few of the governance and pay sub-requirements were checked by cross-reference rather than read line by line, and these are flagged in the matrix and scorecards so they can be verified; the Method section quantifies how much those flagged scores could move the result (run `python3 sensitivity.py` to reproduce it). Page citations point to the reports' own section and page numbers. AASB S2 reproduces the content of IFRS S2 (the matching international standard), so the pillar structure here is faithful. Even so, the standard's own text should be checked for any edge case before these scores are treated as final.

## Files

`scoring-matrix.csv` (all 93 scored cells with evidence), `gap-summary.csv` (patterns across the companies), `bhp-scorecard.md`, `woodside-scorecard.md`, `rio-tinto-scorecard.md`, `sensitivity.py` (the band-robustness check described under Method), `data/source-library.csv`, and `EXECUTION_PROMPT.md` (the method spec). The source reports are in `data/raw/`.
