# Adapted coding framework for Objectives 2 and 3

Objective 1, Step 3 output. This is the scheme applied to council planning
and policy documents in the within-council before/after arm (Objective 2)
and the cross-council comparison arm (Objective 3). Every item below states
which included study it is drawn from and, where relevant, how it was
changed to fit a non-emergency instrument. See `slr/framework-synthesis.md`
for the reasoning behind each change.

## Design principles carried over from the synthesis

1. **No emergency-mode pass/fail bar.** Following the adaptation of S5
   (Greenfield, Moloney and Granberg 2022), no item scores whether a
   council reaches "emergency-mode governance." Items score whether a
   specific, checkable thing is present in the document.
2. **Presence of implemented items, not wording of intent.** Following S7
   (Krause 2011), coding looks for concrete policy content (a target, a
   named owner, a budget line), not for how strongly a document's language
   expresses concern about climate change.
3. **A standalone plan is one coding item, not a precondition.** Following
   the adaptation of S2 (Bush and Doyon 2025), a council that folds its
   commitments into an existing strategic community plan is coded on the
   same items as a council with a dedicated climate action plan.
4. **Every non-zero code carries a citation.** Document short-name, date,
   and page or section. A zero needs a note that the corpus was searched,
   not skimmed, matching the evidence-discipline rule used in
   `aasb-s2-review`.

## Coding items

| ID | Item | Source | Adaptation from source |
|----|------|--------|-------------------------|
| P1 | Names a climate-related target (mitigation, adaptation, or both) with a baseline and a date | S2, S7 | Scored as present/absent/partial regardless of which document it sits in |
| P2 | Names a person, position or committee responsible for climate action | S3, S7 | Direct carry-over; no emergency framing implied |
| P3 | States a budget line, grant, or resourcing commitment tied to climate action | S3, S7 | Direct carry-over |
| P4 | States a reporting or review cadence (for example, annual progress reporting to council) | S3 | Direct carry-over |
| P5 | Mitigation and adaptation both addressed, not mitigation alone | S2 | Direct carry-over; one of the five transformative-action elements |
| P6 | Evidence of cross-council collaboration (regional group, joint program, shared resourcing) | S2 | Direct carry-over |
| P7 | Acknowledges First Peoples' knowledges, aspirations, or joint planning | S2 | Direct carry-over |
| P8 | Considers justice or equity in who bears climate impacts or costs | S2 | Direct carry-over |
| P9 | Links to a biodiversity or natural-environment response alongside climate action | S2 | Direct carry-over |
| P10 | Document exists as a standalone climate or environment strategy versus folded into a general plan | S2 (adapted) | Recorded as a description of document form, not scored as a precondition |
| P11 | Stated purpose or driver for engaging with climate policy at this point (community pressure, funding round, election commitment, WALGA program, state government requirement) | S6 (adapted) | Used as interpretive context alongside the coding, drawn from the agenda item or minutes that record the decision, not scored as present/absent |
| P12 | Any reference to WALGA's Declaration, the 2018 Policy Statement, or WALGA's Sector Climate Change Adaptation Plan, and which one | New, specific to this project | Needed so that a source conflating the Declaration with the 2018 Policy Statement (the error this project itself corrected) is caught during coding, not assumed away |

Items P1 to P9 are scored 0 (absent), 1 (mentioned, not specified: for
example a target named without a baseline or date), or 2 (specified and
checkable). P10 to P12 are recorded as short descriptive codes, not scored
on the 0 to 2 scale, since they describe document form and context rather
than policy substance.

## Applying the framework across Objectives 2 and 3 (updated after the design pivot)

`EXECUTION_PROMPT.md`'s "Design pivot" section records why this changed:
Step 4 found signing dates almost never publicly available, so the
before/after application below was replaced with a cross-sectional one.
The coding items themselves (P1 to P12) did not need to change, since
none of them depend on having two time points; only how they are applied
did.

**Objective 2 (confirmed signatories, current state).** For each council in
`data/signatory-sample.csv` confirmed as a WALGA Declaration signatory,
code its current planning document set (strategic community plan, climate
or environment strategy, annual report, whichever exist) against P1 to
P12. There is no before state to compare against; the score itself, not a
change in score, is the unit of evidence for RQ2.

**Objective 3 (comparison group, current state).** Code the same document
types for a comparison group of councils with no public confirmation of
signatory status, using the same items. Compare the two groups' scores.
Following credibility point 5 in `EXECUTION_PROMPT.md`, report this
group as "not confirmed as signatory," never as "non-signatory," since
absence of a public statement is not proof of non-signing.

## What this framework cannot settle

Since the pivot, a score difference between the confirmed-signatory group
and the comparison group is an association at one point in time, not a
proven cause, and not even proof of a before/after change, since there is
no before state in the design at all. P11 exists specifically so that,
where a document trail names another plausible driver of a council's
policy content (a funding round, an election, a new corporate plan cycle),
that alternative explanation is recorded next to the finding rather than
left for a reader to guess at. This mirrors the causal-honesty rule in
`EXECUTION_PROMPT.md`.

## References

See `slr/framework-synthesis.md` for full citations of S1 to S8.
