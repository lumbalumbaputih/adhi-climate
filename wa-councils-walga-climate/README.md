# WA Councils' Climate Policy-Making After the WALGA Declaration

**Status: Objective 1 done; design pivoted; Objectives 2 and 3 have a
small first pilot tranche (n = 4 signatories, n = 4 comparison), not yet
the full sample.** The systematic literature review is written up below
and in `slr/`. Step 4 (rebuilding the signatory sample) found that signing
dates are almost never publicly available, so the design pivoted from a
before/after comparison to a cross-sectional one: confirmed signatories
versus non-confirmed-signatories, current policy content. See "The design
pivot" and "Objectives 2 and 3: a first, small pilot tranche" below.
Project scope, method and constraints live in
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
confirmed WALGA Declaration signatories (Shire of Harvey, City of
Kalamunda, City of Busselton, Shire of Denmark) and four councils with no
public confirmation of signatory status (City of Swan, City of Joondalup,
City of Cockburn, City of Bunbury). This is a small, first-pass pilot, not
the full four-month sample: eight councils, one current document set each,
scored against nine of the twelve coding items (`data/coding-matrix-
signatories.csv`, `data/coding-matrix-comparison.csv`, provenance in
`data/source-library.csv`).

**The headline number has to be read with its own caveat attached.** On
the nine scored items (P1 to P9, each 0 to 2), the confirmed-signatory
group averaged 0.39 per item and the comparison group averaged 0.61, the
comparison group scoring *higher*. Taken at face value that is the
opposite of what a Declaration effect would predict. It should not be
taken at face value. Roughly half of this pilot's data points came from
search-engine summaries or webpages that were truncated, returned a 403,
or served only a JavaScript loading placeholder rather than the actual
policy document (`data/source-library.csv` records exactly which; City of
Kalamunda's Action Plan PDF and City of Cockburn's Sustainability Policy
PDF, for two examples, were never directly read). A "0" in these matrices
usually means "not found in what could be accessed," not "confirmed absent
from the council's full corpus." The comparison group happened to have two
councils (Cockburn, Bunbury) whose strategies were well summarised by
search results even though the primary documents themselves were
unreachable, while two signatory-group councils (Kalamunda, Busselton)
were hit by access failures on the primary or near-primary source. That
is very plausibly an access artifact, not a real difference between the
groups, and this pilot is too small and too access-limited to tell the two
apart. Two real, useful findings survive that caveat regardless: Shire of
Harvey's page names a "Shire of Harvey Climate Change Declaration" in
wording that does not clearly distinguish whether it means WALGA's
Declaration or a locally branded version of it, the same ambiguity found
at City of Albany, so it is flagged for disambiguation rather than scored
as confirmed; and City of Joondalup, in the comparison group, is a
documented early mover (a Climate Change Strategy adopted in 2014,
independent of WALGA's Declaration), which is itself evidence that strong
climate policy content can and does exist for reasons that have nothing to
do with signing.

## What happens next

Scaling this pilot to a defensible sample needs primary documents read
directly, not search-engine summaries standing in for them, which this
session's tools could not reliably fetch (PDF size limits, 403s,
JavaScript-rendered pages). That is a tooling gap more than a scope one:
the documents exist and are public. The next session should prioritise
direct downloads of each council's Climate Change Strategy or Action Plan
PDF (or a plain-text extraction of it) before adding more councils to the
sample, and only then expand the sample size.

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
