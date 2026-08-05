# Execution Prompt: WA Councils' Climate Policy-Making After the WALGA Declaration

> Portfolio project (research design, not data science). Paste this whole file
> into a fresh session to start work. Self-contained: no prior context needed.
> Mirrors the framing of the `aasb-s2-review/EXECUTION_PROMPT.md` project, which
> is also a document-based review rather than a statistics pipeline. Where this
> one differs: the unit of analysis is council policy documents, not company
> disclosures, and the review sits inside a Curtin Master of Environment and
> Climate Emergency research project, so it carries thesis-scope and ethics
> constraints that the AASB S2 review does not.

---

## Project framing

**Research question.** After a Western Australian local government signs
WALGA's Western Australian Local Government Declaration on Climate Change,
what changes, if any, occur in that council's climate policy-making, and do
those changes resemble the outcomes reported in the climate-emergency-
declaration literature, or something weaker?

**Thesis relevance.** This sits inside the Master of Environment and Climate
Emergency at Curtin University. It takes an instrument that is specific to
WA local government (WALGA's Declaration) and asks a question the published
literature has not yet asked of it, using methods (systematic review plus
document analysis) that are standard for a coursework-length research
project and realistic inside a four-month window.

**Population in scope.** WA local governments that are signatories to
WALGA's Western Australian Local Government Declaration on Climate Change.
As of this scoping search (5 August 2026), WALGA's own site states 62 local
governments have signed, representing over 87 per cent of WA's population
(WALGA, n.d.). That aggregate figure is a starting point only: it does not
give a per-council signing date, which Objectives 2 and 3 need, so the
signatory list and dates must be rebuilt from primary sources (council
agenda items, minutes and WALGA State Council records), not quoted from the
aggregate count.

**Repo.** Umbrella repo `adhi-climate`, subfolder `wa-councils-walga-climate/`.

---

## Correcting the record: which document this project is about

This project studies WALGA's **Western Australian Local Government
Declaration on Climate Change**, the instrument individual councils sign.
It does **not** study WALGA's **Policy Statement on Climate Change (2018)**,
which is a separate document: WALGA's own sector-wide advocacy position,
endorsed by State Council on 4 July 2018, that sets out WALGA's policy
positions and is not something individual councils sign (WALGA, n.d.). An
earlier framing of this project named the 2018 Policy Statement as the
object of study. That was wrong and is corrected here. Every source used in
Objective 1 must be checked for the same conflation: several WALGA and
council pages discuss the Declaration and the 2018 Policy Statement on the
same page, and a source that blurs the two should be flagged, not quoted as
if it were about the Declaration.

The Declaration itself is also explicitly not a climate emergency
declaration. WALGA's own materials describe it as an acknowledgement of
climate impacts and a commitment to develop "locally appropriate mitigation
and adaptation strategies," and coverage of the Declaration notes it "is not
a declaration of a climate emergency" even though it references urgent
action (WALGA, n.d.; CCWA, n.d.). That distinction is the hinge of the whole
project's problem statement below.

---

## The gap, stated honestly

Two literatures are adjacent to this question and neither answers it
directly.

**Climate-emergency-declaration research (Australian and international)**
studies what happens after a local government formally declares a climate
emergency. Bush and Doyon (2025) examine 39 Victorian councils' emergency
declarations and the action plans that followed, using a "transformative
action" framework built around mitigation and adaptation together,
cross-council and intra-council collaboration, links to biodiversity
emergency responses, acknowledgement of First Peoples' knowledges and
aspirations, and attention to justice and equity. Greenfield, Moloney and
Granberg (2022) study 30 Victorian councils' emergency declarations and
three detailed action plans (Darebin, Moreland, Yarra), asking whether the
declarations are symbolic acts or genuine disruptions to business-as-usual
governance, and find the plans meet most attributes of a "robust" climate
response framework without reaching genuine emergency-mode governance.

**Neither of these, nor the broader emergency-declaration literature they
sit inside, studies WALGA's Declaration.** That is a genuine gap, not a
technicality: an emergency declaration is a stronger, more contested
instrument (it asserts the existence of an emergency and commonly invokes
language about disrupting normal operations), while WALGA's Declaration is
a acknowledgement-and-commitment instrument with no emergency framing at
all. Applying an emergency-declaration framework (for example, "does the
plan disrupt the status quo?") to a WALGA-Declaration signatory risks
grading a weaker instrument against a bar it was never built to clear. The
frameworks are useful as a starting point for what to look for in policy
documents (ambition, resourcing, target-setting, cross-council
collaboration), but they need explicit adaptation before they can be
applied to this weaker instrument, and this project treats that adaptation
as one of its own outputs (Objective 1), not as a solved preliminary step.

This claim, that nothing in the literature studies WALGA's Declaration
specifically, rests on the scoping searches done to write this prompt, not
on a completed systematic search. Objective 1's SLR must re-test it with a
documented search protocol before the rest of the project leans on it.
Adjacent Australian work exists and should be checked at that stage, for
example a 2025 Climatic Change study applying an LLM-based document-analysis
pipeline to Victorian councils' climate-emergency policy, which is close in
method (automated document analysis of council policy) but, like the two
studies above, is scoped to formal emergency declarations rather than
WALGA's instrument.

---

## Division of labour

- **Kai**: runs the SLR search and screening, builds the document corpus and
  coding framework, codes the sampled council documents, drafts the
  synthesis and findings.
- **Ris**: confirms the signatory sample and framing decisions, reviews
  coding for plausibility and local knowledge of WA council politics, owns
  the thesis narrative and any ethics application for Objective 4, and
  decides whether Objective 4 goes ahead given the time remaining.

---

## Read before starting (the credibility tests)

1. **Correlation is not causation.** A council's climate policy can change
   for reasons unconnected to signing the Declaration: a change of council
   after an election, a new corporate business plan cycle, WALGA's own
   Sector Climate Change Adaptation Plan template, state government funding
   rounds, or simple staff turnover. Objective 3's comparison group exists
   specifically to guard against reading a state-wide trend as a
   Declaration effect. Say plainly in the write-up what the design can and
   cannot establish.

2. **A Declaration is not an emergency.** Never import an emergency-
   declaration threshold (for example, "disrupts the status quo") as the
   pass/fail bar for a WALGA signatory without saying explicitly that it has
   been adapted, and how. Document every adaptation decision made when
   carrying a framework from Objective 1 into the coding scheme used in
   Objectives 2 and 3.

3. **Public documents only**, for Objectives 2 and 3: strategic community
   plans, corporate business plans, climate action or environment
   strategies, annual reports, and the council agenda item and minutes that
   record the decision to sign. No internal council data, no unrecorded
   conversations.

4. **Evidence discipline. No fabricated citations, ever.** Every claim about
   a council's policy content needs a document name, date and page or
   section reference. A claim that a topic is absent from a council's
   documents needs a note confirming the corpus was searched, not just
   skimmed.

5. **Track signing dates from primary sources.** WALGA's aggregate
   signatory count (62 councils, 87 per cent of WA's population, as read on
   5 August 2026) will have moved by the time this project runs. Build the
   sample's per-council signing dates from council agenda items, minutes or
   direct confirmation with WALGA, and record the date each figure was
   retrieved.

6. **Objective 4 needs ethics clearance before any interview is booked.**
   Interviews with council staff are human research and require Curtin HREC
   approval (or confirmed exemption) first. Do not contact a council officer
   before that clearance exists.

---

## Objectives

**Objective 1: Systematic literature review.** Map the published research on
local-government climate-emergency and climate-declaration responses,
Australian and international, with a documented search protocol (databases,
search strings, inclusion and exclusion criteria, a PRISMA-style flow of
records found, screened, and included). Catalogue the analytical frameworks
in the included studies, in particular Bush and Doyon's (2025) transformative-
action framework and Greenfield, Moloney and Granberg's (2022) symbolic-act-
versus-disruption framework, plus any others the search turns up (voluntary-
pledge and policy-diffusion literatures are a plausible adjacent body of work
worth checking, since WALGA's Declaration is closer in form to a pledge than
to an emergency declaration). Confirm or correct, with the completed search,
the claim that no existing study addresses WALGA's Declaration specifically.
Output an adapted coding framework for Objectives 2 and 3, with every
adaptation from the source frameworks stated and justified.

**Objective 2: Document analysis, arm 1 (within-council, before and after).**
For a sample of WALGA-Declaration signatory councils, apply the Objective 1
coding framework to each council's planning and policy documents from before
and after its signing date, to test whether measurable change in climate
policy content follows the signing.

**Objective 3: Document analysis, arm 2 (across councils).** Apply the same
coding framework to a comparison group, non-signatory councils, or
early-signing versus late-signing councils, over the matching period, to
check whether any change found in Objective 2 is distinct to signatories or
reflects a wider WA local-government trend.

**Objective 4 (optional, first cut only): Interviews.** Semi-structured
interviews with council officers involved in the decision to sign or in
subsequent implementation, to triangulate what the documents show and probe
why change did, or did not, follow. In scope only if Objectives 1 to 3 are
complete with time and ethics clearance remaining; treated as a first cut to
extend later, not a requirement for this phase.

Objectives 1 to 3 are the realistic four-month scope. Objective 4 is
optional and should not be allowed to compress the document-analysis arms,
which are the project's core evidence base.

---

## Research questions

- RQ1. What analytical frameworks exist in the literature for studying local-
  government policy change after a climate-emergency or climate-declaration
  instrument, and what do they assume about the instrument's strength that
  does not hold for WALGA's Declaration?
- RQ2. Within WA councils that have signed WALGA's Declaration, does their
  climate-related policy content change measurably between the period before
  and after signing?
- RQ3. Where change is found, does it resemble the outcomes reported for
  formal emergency declarations in the literature (Bush and Doyon 2025;
  Greenfield, Moloney and Granberg 2022), or is it smaller or different in
  kind, consistent with a weaker instrument?
- RQ4. Is any change specific to signatory councils, or does it also appear
  in non-signatory or later-signing councils over the same period?

---

## Methodology overview and work steps

| # | Step | Objective | Output |
|---|------|-----------|--------|
| 1 | Register the SLR search protocol: databases, search strings, inclusion and exclusion criteria | 1 | `slr/search-protocol.md` |
| 2 | Run the search, screen records, log the PRISMA-style flow | 1 | `slr/prisma-log.csv`, `slr/included-studies.csv` |
| 3 | Extract and compare frameworks from included studies; adapt a coding scheme for a non-emergency declaration | 1 | `slr/framework-synthesis.md`, `coding-framework.md` |
| 4 | Rebuild the signatory sample: confirm councils, signing dates and sources | 2, 3 | `data/signatory-sample.csv` |
| 5 | Build the document corpus per sampled council (before and after signing, plus comparison group) | 2, 3 | `data/source-library.csv`, `data/raw/` (gitignored) |
| 6 | Code the within-council before/after corpus against the adapted framework | 2 | `data/coding-matrix-within.csv` |
| 7 | Code the comparison-group corpus over the same period | 3 | `data/coding-matrix-comparison.csv` |
| 8 | Synthesise findings against RQ1 to RQ4; write the plain-English report | 1 to 3 | `README.md` |
| 9 | (If scope allows) Draft Objective 4 interview protocol, seek HREC clearance, run a first cut of interviews | 4 | `interviews/protocol.md`, `interviews/notes/` (gitignored, de-identified summaries only) |

---

## Timeline (four-month scope)

| Month | Focus |
|-------|-------|
| 1 | Objective 1: search protocol, screening, framework synthesis, adapted coding scheme. Rebuild the signatory sample and confirm per-council signing dates. |
| 2 | Objective 2: build the document corpus for the within-council sample; begin coding. |
| 3 | Finish Objective 2 coding; Objective 3: build and code the comparison-group corpus. |
| 4 | Synthesis and write-up against RQ1 to RQ4. If time and ethics clearance allow, draft and run a first cut of Objective 4 interviews; otherwise record it as future work. |

---

## Deliverables and formats

| Deliverable | File | Spec |
|-------------|------|------|
| SLR search protocol | `slr/search-protocol.md` | Databases, search strings, inclusion/exclusion criteria, dates run |
| PRISMA-style log | `slr/prisma-log.csv`, `slr/included-studies.csv` | Records found, screened, excluded (with reason), included |
| Framework synthesis | `slr/framework-synthesis.md` | What each included study's framework assumes about the strength of the instrument studied, and what must change to apply it to WALGA's Declaration |
| Adapted coding framework | `coding-framework.md` | The scheme applied in Objectives 2 and 3, with every adaptation from source frameworks stated and justified |
| Signatory sample | `data/signatory-sample.csv` | Council, signing date, source, date retrieved, sample arm (within-council or comparison) |
| Source library | `data/source-library.csv` | Provenance for every document coded: council, document type, title, date, url, date retrieved |
| Coding matrices | `data/coding-matrix-within.csv`, `data/coding-matrix-comparison.csv` | One row per council per document per coding item, with evidence (document, page or section) |
| Written summary | `README.md` | Plain-English: question, method, findings against RQ1 to RQ4, limitations, how to reproduce |
| Interview materials (if Objective 4 proceeds) | `interviews/protocol.md`, de-identified summaries only | HREC-cleared protocol; no raw recordings or identifying notes committed to the repo |

---

## Repo structure (what done looks like)

```
adhi-climate/
└── wa-councils-walga-climate/
    ├── EXECUTION_PROMPT.md        # this file
    ├── README.md                  # written summary and findings
    ├── slr/
    │   ├── search-protocol.md
    │   ├── prisma-log.csv
    │   ├── included-studies.csv
    │   └── framework-synthesis.md
    ├── coding-framework.md
    ├── data/
    │   ├── raw/                   # gitignored: downloaded council documents
    │   ├── signatory-sample.csv
    │   ├── source-library.csv
    │   ├── coding-matrix-within.csv
    │   └── coding-matrix-comparison.csv
    └── interviews/                # only if Objective 4 proceeds
        ├── protocol.md
        └── notes/                 # gitignored: de-identified summaries only
```

---

## Constraints

| Constraint | Rule |
|------------|------|
| Writing style | Chicago 17th author-date for all citations. IELTS 6.5 to 7 reading level: clear, structured, hedged. No em dashes. No double-hyphens. Cohesive paragraphs in the README and synthesis documents; tables and short lists are fine for protocols and matrices |
| Evidence | Every policy-content claim cited to a document, date and page or section; never fabricate quotes, page numbers, or document titles |
| Instrument honesty | Never treat the Declaration as an emergency declaration; state explicitly, every time a source framework is used, how it was adapted |
| Causal honesty | State plainly what the before/after and comparison-group design can and cannot establish about causation |
| Ethics | Objective 4 requires Curtin HREC clearance (or confirmed exemption) before any council officer is contacted; no identifying interview material committed to the repo |
| Scope discipline | Objectives 1 to 3 are the four-month deliverable. Objective 4 is optional and must not compress the document-analysis arms |

---

## Limitations to state upfront

The signatory count and population share quoted from WALGA's site are a
snapshot (5 August 2026) and will move; the sample used in Objectives 2 and
3 must be pinned to confirmed signing dates, not the aggregate figure. The
"no existing study addresses WALGA's Declaration" claim is provisional until
Objective 1's documented search confirms it. A before/after document
comparison, even with a comparison group, cannot fully rule out confounds
specific to individual councils (a change of mayor, an unrelated funding
grant); the write-up should flag where a finding could plausibly have
another cause. Coding council planning documents is an interpretive task;
a second-pass review (Ris) before any finding is locked, in the same spirit
as the two-pass scoring used in the AASB S2 review, keeps that honest.

---

## References

Bush, J., and A. Doyon. 2025. "Climate Emergency Declarations by Local
Governments: What Comes Next?" *npj Climate Action* 4, Article 44.
https://doi.org/10.1038/s44168-025-00253-2.

Conservation Council of Western Australia (CCWA). n.d. "New WA Local
Government Climate Policy Shows the Way Forward." Accessed 5 August 2026.
https://www.ccwa.org.au/walga_climate_policy.

Greenfield, Anthony, Susie Moloney, and Mikael Granberg. 2022. "Climate
Emergencies in Australian Local Governments: From Symbolic Act to
Disrupting the Status Quo?" *Climate* 10 (3): 38.
https://doi.org/10.3390/cli10030038.

WALGA (Western Australian Local Government Association). n.d. "Climate
Change." Accessed 5 August 2026.
https://walga.asn.au/policy-and-advocacy/our-policy-areas/environment/climate-change.

---

## Session start instruction

Start with **Step 1 of Objective 1**. Do not sample or code any council
document yet. First draft the SLR search protocol (databases, search
strings, inclusion and exclusion criteria) and run it, then show the
PRISMA-style flow and the list of included studies, with the "no existing
study on WALGA's Declaration" claim either confirmed or corrected. Pause for
Ris to confirm the included-studies list and the adapted coding framework
before any council document is gathered or coded. Garbage in, garbage out:
the whole comparison in Objectives 2 and 3 rests on a coding framework
that has been honestly adapted, not borrowed wholesale from a literature
built for a stronger instrument.
