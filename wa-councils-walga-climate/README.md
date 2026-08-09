# WA Councils' Climate Policy-Making After the WALGA Declaration

**Status: Objective 1 done; design pivoted; the pilot's tooling blocker is
resolved, and doing so broke the pilot's comparison group.** The
systematic literature review is written up below and in `slr/`. Step 4
(rebuilding the signatory sample) found that signing dates are almost
never publicly available, so the design pivoted from a before/after
comparison to a cross-sectional one: confirmed signatories versus
non-confirmed-signatories, current policy content. A second session
(9 Aug 2026) fetched every primary document the first pilot pass could
not reach and found that three of the four "comparison" councils are
themselves confirmed WALGA Declaration signatories: the comparison arm of
this 8-council pilot has effectively collapsed to n = 1 (City of Swan).
See "The design pivot" and "Objectives 2 and 3: a first, small pilot
tranche" below. Project scope, method and constraints live in
[`EXECUTION_PROMPT.md`](EXECUTION_PROMPT.md).

## In one paragraph

WALGA's Western Australian Local Government Declaration on Climate Change
is a commitment councils sign, not a formal climate-emergency declaration
and not the same document as WALGA's 2018 Policy Statement on Climate
Change. This project asks what, if anything, changes in a WA council's
climate policy-making after it signs the Declaration, and whether any
change looks like the outcomes reported in the climate-emergency-
declaration literature or something weaker.

## Objective 1: what the literature review found

A documented search (`slr/search-protocol.md`) covering six identification
queries, screened against explicit inclusion and exclusion criteria
(`slr/prisma-log.csv`, 37 records screened), found no study of WALGA's
Declaration specifically, including a search run for exactly that. That
confirms, for this pass, the gap stated in `EXECUTION_PROMPT.md`. It stays
provisional until re-run against Scopus and Web of Science, which this
environment does not have access to; that limitation is recorded in the
protocol so the re-run has a documented baseline to check against.

Eight studies met the inclusion criteria (`slr/included-studies.csv`). Six
study formal climate-emergency declarations, mostly in Victorian and UK
councils (Ruiz-Campillo, Castan Broto and Westman 2021; Bush and Doyon
2025; Gudde et al. 2021; Hicks, Davidson, Lau et al. 2025; Greenfield,
Moloney and Granberg 2022; Howarth, Lane and Fankhauser 2021). Two study
adjacent, non-emergency instruments closer in kind to WALGA's Declaration:
Krause (2011) on US municipalities joining a voluntary climate-protection
network, and Schulze (2024) on the channels through which local climate
policy diffuses without any single triggering event.

`slr/framework-synthesis.md` works through what each study's framework
assumes about the strength of the instrument it studies, and states plainly
that none of the six emergency-declaration frameworks can be applied to
WALGA's Declaration unmodified: several score against a bar, an asserted
emergency, that the Declaration never sets. `coding-framework.md` is the
resulting adapted scheme, a 12-item checklist built from the transferable
parts of those frameworks plus one item specific to this project, that
catches any source conflating the Declaration with the 2018 Policy
Statement, the same error this project's own framing corrected.

## The design pivot

Objectives 2 and 3 were originally a within-council before/after
comparison plus a same-period comparison group, both keyed to each
council's confirmed signing date. Rebuilding the signatory sample
(`data/signatory-sample.csv`, `data/signatory-search-log.md`) across
roughly 18 WA councils found that signatory status is usually confirmable
from a council's own page, but a signing date almost never is: of six
confirmed signatories found, only one (Shire of Harvey) had even a
medium-confidence date, and no confirmed non-signatory was found at all.
That is too thin a sample for a before/after design.

Ris confirmed a pivot on 5 August 2026: keep the comparison structure, drop
the before/after claim. Objectives 2 and 3 now compare confirmed
signatories' and non-confirmed-signatories' **current** planning documents
against the same 12-item coding framework. This is a real downgrade in
what the design can show, an association between signatory status and
policy content, not that signing caused any difference, and the write-up
says so plainly rather than letting the comparison read as causal. It also
mirrors the closest precedent in the literature review: Hicks, Davidson,
Lau et al. (2025) compare declared against non-declared Victorian
councils' current policy text, not a before/after pair.

## Scope

Objectives 1 to 3 (the literature review plus two document-analysis arms,
now both cross-sectional: confirmed signatories, and a comparison group
with no public confirmation of signatory status) are the realistic
four-month scope. Interviews with council officers (Objective 4) are
optional, ethics-gated, and treated as a first cut to extend later, not a
requirement for this phase.

## Objectives 2 and 3: a first, small pilot tranche

A pilot sample was built and coded against the 12-item framework: four
councils originally treated as confirmed WALGA Declaration signatories
(Shire of Harvey, City of Kalamunda, City of Busselton, Shire of Denmark)
and four councils originally treated as having no public confirmation of
signatory status (City of Swan, City of Joondalup, City of Cockburn, City
of Bunbury). This is a small, first-pass pilot, not the full four-month
sample: eight councils, one current document set each, scored against
nine of the twelve coding items (`data/coding-matrix-signatories.csv`,
`data/coding-matrix-comparison.csv`, provenance in
`data/source-library.csv`).

**The first pass's headline number and the tooling blocker behind it
(9 Aug 2026 update).** The first pilot pass found the comparison group
scoring *higher* than the signatory group (0.61 vs 0.39 per item on P1 to
P9), the opposite of what a Declaration effect would predict, and
flagged that as very plausibly an access artifact: roughly half the
pilot's data points came from search-engine summaries standing in for
documents that returned a 403, a JavaScript loading placeholder, or (it
was believed) an unreadable image-based PDF.

A second session installed `poppler-utils` (`pdftotext`) and re-fetched
every one of those documents directly. All of them turned out to be
readable: none was actually image-based, the earlier 403s and size limits
did not reproduce, and `pdftotext` extracted clean, complete text from six
PDFs and two webpages that the first pass could only access as summaries
or fragments. That resolved the access problem the first pass diagnosed,
but reading the primary documents surfaced a different and larger
problem: **three of the four "comparison" councils are themselves
confirmed WALGA Declaration signatories.**

- **City of Joondalup** signed in **September 2013** ("Council endorsed
  the City becoming a signatory to the WALGA Climate Change Declaration"),
  per its own Climate Change Plan 2025-2035 -- directly contradicting the
  City's own initiatives summary webpage, which states the City is "not
  stated as a signatory to any declaration."
- **City of Cockburn** signed in **2012** ("In 2012 the City signed the
  WALGA Climate Change declaration"), stated twice in its Climate Change
  Strategy 2020-2030 -- one of the cleanest confirmed signing dates found
  anywhere in this project.
- **City of Bunbury** signed in **2022** ("the Council in 2022 signing the
  Western Australian Local Government Association (WALGA) Declaration on
  Climate Change"), per its Sustainability and Environmental Strategy
  2023-2028, which also correctly and separately names its support for
  WALGA's 2018 Policy Statement as a different instrument.

None of these three signatory statements appeared on the landing/summary
pages the first pass relied on; all three appear only in the primary
planning document itself. **City of Swan is now the pilot's only
surviving comparison-group council** (its landing page remains a general
sustainability directory with no WALGA reference, and no primary Climate
Change Strategy document for Swan has yet been located). Two other
documents were also upgraded from "unreadable" to fully read: Shire of
Denmark's Carbon Reduction Policy (not image-based after all; confirms a
2018/19 baseline, 50% by 2030, net zero by 2050, and a direct WALGA
reference) and City of Kalamunda's Action Plan (confirms a 2020 baseline,
40% by 2030, net-zero by 2035).

**Corrected numbers, read with a new caveat.** Re-scored against the same
nine items with the fuller documents, the (now 7-council) signatory group
averages **1.43 per item**; the (now 1-council) comparison group, City of
Swan alone, scores **0.22 per item**. That gap now points the direction a
Declaration effect would predict, but it is **not evidence of one**: with
n = 1 in the comparison group, and with "how much of the primary document
could be read" now confounding the comparison (dedicated climate-strategy
PDFs versus a single sustainability directory page), this pilot cannot
support any claim about the direction or size of a Declaration effect.
What it does support is a data-quality finding: **a council's own
summary or landing page is not reliable evidence of its WALGA signatory
status**, in either direction, and coding for this project must go to the
primary planning document before a council's group membership is decided,
not after.

Shire of Harvey's P12 flag from the first pass is now resolved rather than
open: its climate-change webpage, read in full, does not reference WALGA's
Declaration at all -- it names only a locally-branded "Shire of Harvey
Climate Change Declaration," the same naming pattern as City of Albany.
Harvey's presence in the signatory sample now rests entirely on the
separate Council Action Register evidence in `data/signatory-sample.csv`
(medium confidence), not on this webpage.

## What happens next

The tooling blocker the first pass hit is resolved (`pdftotext` reads
these councils' PDFs cleanly; a JS-placeholder page can usually be worked
around by finding the direct PDF link and fetching that instead of the
wrapping page). What is not resolved is the comparison group: with three
of its four original members reclassified as signatories, Objective 3
needs a **new** comparison sample of similar size, built the same way this
session corrected the old one -- primary Climate Change Strategy or
equivalent document read directly, not a summary page -- before Objectives
2 and 3 can say anything about signatory status and policy content
together. City of Swan's own primary document (if one exists) should be
the first thing the next session looks for, followed by several more
candidate councils from `data/signatory-sample.csv`'s remaining "unknown"
rows.

## Files

`slr/search-protocol.md` (databases and search strings, inclusion and
exclusion criteria, and the stated limitation of using web search in place
of Scopus and Web of Science), `slr/prisma-log.csv` (all 37 records
screened, with a decision and reason for each), `slr/included-studies.csv`
(the 8 included studies, full citations, population, method and framework),
`slr/framework-synthesis.md` (what each framework assumes and how it was
adapted), `coding-framework.md` (the adapted scheme for Objectives 2 and
3), `data/signatory-sample.csv` and `data/signatory-search-log.md` (the
signatory search behind the design pivot), and `EXECUTION_PROMPT.md` (the
full project spec).

## Update log

**5 Aug 2026 · Scoping.** Corrected the object of study from WALGA's 2018
Policy Statement to the Western Australian Local Government Declaration on
Climate Change, confirmed the two are separate documents, and wrote up the
research question, honest literature gap, objectives and four-month scope
in `EXECUTION_PROMPT.md`.

**5 Aug 2026 · Objective 1, first pass.** Ran a documented search (37
records screened), confirmed the stated literature gap for this pass,
included 8 studies, and wrote the framework synthesis and adapted 12-item
coding framework for Objectives 2 and 3. No council document sampling or
coding has started; paused for confirmation as the execution prompt
instructs.

**5 Aug 2026 · Design pivot.** Ran Step 4 (rebuild the signatory sample)
across roughly 18 WA councils and found signing dates are almost never
publicly available, even though signatory status usually is. Pivoted
Objectives 2 and 3 from a before/after comparison to a cross-sectional one:
confirmed signatories versus non-confirmed-signatories, current policy
content, with the causal downgrade stated plainly.

**5 Aug 2026 · First pilot tranche, Objectives 2 and 3.** Coded a small
pilot (4 confirmed signatories, 4 comparison councils) against 9 of the 12
framework items. The headline numbers ran opposite to what a Declaration
effect would predict, comparison group higher than signatories, but heavy
reliance on search-engine summaries in place of several primary documents
that could not be fetched (PDF size limits, 403s, a JavaScript-only page)
makes that very plausibly an access artifact rather than a real finding.
Flagged for the next session: fetch primary documents directly before
scaling the sample.

**9 Aug 2026 · Tooling blocker resolved; comparison group collapsed.**
Installed `poppler-utils` and re-fetched every document the first pilot
pass could not read. All eight were readable directly this time (none was
actually image-based; no 403s or size limits reproduced). Reading the
primary documents instead of summary pages found that City of Joondalup
(signed 2013), City of Cockburn (signed 2012) and City of Bunbury (signed
2022) are confirmed WALGA Declaration signatories, contradicting the
landing pages the first pass relied on for all three. Reclassified them
from the comparison group to the signatory group; City of Swan is now the
pilot's only comparison-group council. Re-scored all nine councils'
documents against the coding framework with the fuller text now available
(`data/coding-matrix-signatories.csv`, `data/coding-matrix-
comparison.csv`, `data/signatory-sample.csv`, `data/source-library.csv`
all updated). The corrected group averages (1.43 vs 0.22 per item) now
point the direction a Declaration effect would predict, but are not
usable as evidence of one: n = 1 in the comparison group. Objective 3
needs a new comparison sample built the same way this session corrected
the old one, before Objectives 2 and 3 can be reported together.
