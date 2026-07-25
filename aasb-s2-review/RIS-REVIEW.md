# Ris Review: AASB S2 Readiness Review audit

This is the Ris review pass (Step 4 of `EXECUTION_PROMPT.md`): a plausibility,
consistency and evidence-discipline audit of every file in `aasb-s2-review/`
before the scores are treated as locked. Kai produced the scoring; this pass
checks it. Per-row verdicts are now recorded in the `ris_review` column of
`scoring-matrix.csv`. This document carries the cross-cutting findings.

Scope of the audit: `scoring-matrix.csv` (93 cells), `gap-summary.csv`,
`README.md`, the three `*-scorecard.md` files, `data/source-library.csv`, and a
repo-wide check for where the review touches other files. The three storm-name
and "PARIS"/"RISK" substring hits elsewhere in the repo are incidental and not
part of this review.

## Verdict summary

| Verdict | Count | Meaning |
|---------|------:|---------|
| Concur, lock | 82 | Score and evidence agree; defensible as written |
| Hold, verify before lock | 8 | Non-zero score rests on an unconfirmed citation or an internal contradiction |
| Query, consider adjustment | 3 | Score is plausible but may be one band high on the evidence shown |

No score is judged a fabrication, and the honesty framing (disclosure, not
actual readiness) is applied consistently across all three companies and the
README. The arithmetic is sound. The issues below are about pinning evidence and
removing small inconsistencies, not about a flawed method.

## Arithmetic check (independently recomputed)

Every pillar mean and overall score in the matrix recomputes correctly, with one
exception in presentation:

| Company | Governance | Strategy | Risk | M&T | Overall (mean of 4 pillars) |
|---------|:---:|:---:|:---:|:---:|:---:|
| BHP | 3.0 | 3.0 | 3.0 | 2.769 | **2.94** |
| Woodside | 3.833 | 3.167 | 3.333 | 3.077 | **3.35** |
| Rio Tinto | 3.667 | 3.667 | 3.5 | 3.923 | **3.69** |

The gap-summary means and the `n_companies_<=2` counts all reconcile.

## Findings, by priority

### 1. BHP overall score is overstated in its scorecard (fix before CV)

`bhp-scorecard.md` reports overall readiness as **3.0, "Developing (top of
band)"**. The matrix and the README both give **2.94**, which rounds to **2.9** at
one decimal, not 3.0. The README is right; the scorecard rounds the wrong way and
nudges BHP from mid-Developing to the top of the band. Make the scorecard read
2.94 (or 2.9) to match the README and the matrix. Small number, but it is the
headline figure for that company and the kind of thing a reviewer checks first.

### 2. Rio Tinto M8, M9 and G5: score 4 and "high" confidence, but figures not extracted

These three rows score 4 (Full) at high confidence, yet `rio-tinto-scorecard.md`
states plainly under "Items flagged for your review": "I confirmed that Rio
discloses an internal carbon price range (p.73) and a climate-linked
remuneration percentage (pp.122-139) ... but I did not pull out the exact
figures." A score of 4 means comprehensive, verified disclosure. Claiming that
while recording that the number was never read is the clearest evidence-discipline
tension in the matrix, and it is exactly what an interviewer probes ("you gave
that top marks, so what is the carbon price?"). Resolve one of two ways: pull and
quote the figures (likely keeps the 4), or drop confidence to medium until the
figures are in hand. Do not leave score 4 and confidence high with the figure
unread.

### 3. Citation precision: approximate and blank page references

The project's own rule is "never fabricate page numbers." Approximate pages are
not fabrication, but they fail the "pin every citation" bar and read as soft:

- Tilde / approximate pages: Rio S2 `p.~74`, Rio S5 `p.~58`, Rio M11 `p.~72`, Rio M12 `p.~95`.
- A citation with no page at all: BHP M8 `CTAP2024 p.~ (carbon price protocol)`.

Pin each to an exact page before locking. BHP M8 in particular currently cites a
document and a topic but no location.

### 4. M1 (Scope 1) is cited with a combined Scope 1+2 figure

For both BHP (M1) and Woodside (M1) the row is "Absolute gross Scope 1", scored 4,
but the quoted figure is the combined Scope 1+2 number (BHP 8.7 Mt; Woodside
6,616 kt). The standalone Scope 1 figure is asserted to exist (BHP: "Scope 1 split
in Databook") but not quoted. To hold a 4 on a Scope 1 row, quote the standalone
Scope 1 number; otherwise the cited evidence supports M1+M2 jointly, not M1 alone.

### 5. Non-zero scores still resting on "verify / confirm" notes

These are honestly flagged in the matrix and scorecards, which is good, but a
*locked* score should not depend on an open verification. Resolve before sign-off:

| Row | Score | Open item |
|-----|:---:|-----------|
| BHP G2 | 2 | Climate skills matrix, cross-referenced not read (CGS p.87-100) |
| BHP G5 | 3 | Exact % of incentive tied to climate not confirmed |
| BHP M2 | 3 | Both location- and market-based Scope 2 bases unconfirmed |
| Woodside G2 | 3 | Formal climate skills matrix not confirmed |
| Woodside M2 | 3 | Both Scope 2 bases unconfirmed |
| Woodside M3 | 3 | Scope 3 category breakdown to confirm |
| Woodside M10 | 3 | Explicit SASB mapping to confirm |
| Rio Tinto G2 | 3 | Explicit climate skills matrix not confirmed |
| Rio Tinto M10 | 3 | SASB mapping in Fact Book to confirm |

### 6. The two-scenario rule (S6) is unconfirmed for BHP and Woodside, and it can move the score

AASB S2's Australian modification requires at least two scenarios, including one
around 1.5C and one high-warming above 2.5C. BHP S6 (3) and Woodside S6 (3) both
carry a note that the high-warming physical scenario is "not confirmed." If that
scenario is absent, each S6 should fall to 2, which would pull the Strategy pillar
down for both. Scenario analysis is a headline AASB S2 item, so this is worth
verifying first, not last. Rio S6 (4) is sound: SSP2-4.5 is cited and satisfies
the rule.

### 7. Scope: three companies delivered against a six-company brief

`EXECUTION_PROMPT.md` scopes six companies and 186 cells (BHP, Rio Tinto, Woodside,
Fortescue, Mineral Resources, South32). The delivered work covers three companies
and 93 cells. `data/source-library.csv` already lists documents for all six. The
README is honest in saying "three", but nothing states that three more were
planned. A reader who opens the source library and sees six companies will ask why
only three were scored. Decide and state it: either descope formally to three (and
trim the source library or label the other three "not yet scored"), or finish
Fortescue, MinRes and South32.

### 8. Deliverables named in the brief that are not yet present

`report.html`, `cv-blurb.txt`, `INTERVIEW_BRIEF.md` and the `scoring-matrix.xlsx`
view (with the heatmap and summary sheets) do not exist yet. `data/raw/` is absent,
which is expected since it is gitignored, but it means none of the source PDFs are
in the tree to re-verify a citation against. The README's "Files" section does not
over-claim these, which is correct. Listing them here as outstanding, not as errors.

### 9. Source library hedges what the scorecards assert

`data/source-library.csv` marks Rio Tinto and Woodside as "POSSIBLY first mandatory
- verify", while both scorecards assert first-mandatory status as fact, and the
Woodside scorecard quotes the report confirming it. Once confirmed at source,
update the source library so the provenance record and the findings agree. Also,
every `page_count` is still "TBC".

### 10. gap-summary.csv departs from the brief's spec (acceptable, worth a note)

The brief asks gap-summary for "mean score, count at 0, the common pattern, the
consultant recommendation." The delivered file is a wide per-company matrix with
`mean_score` and `n_companies_<=2` instead. The pattern and recommendation content
lives in the README narrative rather than the CSV. This is a reasonable choice and
internally consistent; flagging only so the deviation from the spec is deliberate
and documented.

### 11. Minor: Woodside net-target arithmetic is off by 1 kt (non-material)

Gross 6,616 kt minus 1,283 kt credits is 5,333 kt, while the stated net target is
5,334 kt. A one-tonne-thousand rounding gap. Not material; note it so the numbers
tie out if quoted in an interview.

## What is solid

The method is honest and applied evenly. The disclosure-versus-readiness
distinction is stated in the README, every scorecard, and the matrix method note,
and the Woodside write-up uses it well (strong disclosure, high LNG transition
exposure, kept apart). Cross-document figures reconcile where they should: Rio's
gross Scope 1+2 of 31.5 Mt equals the cited Scope 1 (24.0) plus market-based Scope
2 (7.5); Woodside's methane price of US$6,720/t equals US$80 times an 84 GWP. The
cautious-scoring rule (take the lower of two, explain why) is visible throughout
and is the right instinct for a portfolio piece that has to survive scrutiny.

## Sign-off status

Not yet locked. The matrix is in good shape and most rows (82 of 93) are cleared
to lock. Clearing the eight Holds and three Queries above, principally Finding 2
(Rio M8/M9/G5) and Finding 6 (S6 two-scenario), and fixing Finding 1 (BHP 2.94),
would let the whole set be locked with confidence. None of these require a redo;
they are verification and tidy-up. The per-row Ris verdicts in
`scoring-matrix.csv` mark which is which.
