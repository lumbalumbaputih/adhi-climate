# SLR search protocol

Objective 1, Step 1. Written and run in the same session, 5 August 2026.

## What "database" means in this pass

This project has no institutional access to Scopus, Web of Science or
ProQuest inside this environment. This first pass substitutes a general web
search tool (the session's search and page-fetch tools) for those databases,
plus direct verification of each candidate's bibliographic details on the
publisher's own page where that page was reachable. That is a real
limitation, not a formality: a general web search does not guarantee the
same recall as a citation database, and several candidate records below
could not be fully verified because their publisher pages sat behind a
paywall or a login redirect. Before this SLR is treated as complete for
thesis purposes, it should be re-run against Scopus and Web of Science (both
available through the Curtin library) using the same search strings and
criteria below, and the included-studies list reconciled against that
re-run. This protocol and its limitation are recorded here so that
reconciliation is a check against a documented baseline, not a restart.

## Search strings run

**Identification searches** (the six queries that surfaced new candidate
records):

1. `"climate emergency declaration" "local government" outcomes systematic review`
2. `"climate emergency" declaration council "what happens after" OR "does it matter" policy change`
3. `WALGA "declaration on climate change" academic study OR thesis OR research`
4. `voluntary climate pledge local government policy diffusion symbolic commitment`
5. `climate emergency declaration United Kingdom local authority outcomes evaluation research`
6. `"climate emergency declaration" Australia council case study before after policy content analysis`

**Earlier scoping searches** (run while drafting `EXECUTION_PROMPT.md`, before
Objective 1 formally started; folded into the same record list below because
they surfaced two of the included studies):

7. `WALGA "Western Australian Local Government Declaration on Climate Change"`
8. `Bush Doyon 2025 local government climate emergency declaration`
9. `Greenfield Moloney Granberg 2022 climate emergency declaration local government`
10. `WALGA Declaration Climate Change year adopted State Council signatories list councils`
11. `"Bush" "Doyon" "npj Climate Action" 2025 "what comes next" volume DOI`

**Verification searches** (run to confirm full bibliographic details for
candidates found above; these did not themselves surface new candidates):

12. `Gudde "role of UK local government in delivering on net zero" Energy Policy 2021 volume authors full citation`
13. `"Implications of declaration of climate emergency on Australian local government policy" Victoria LLM retriever-reader authors Climatic Change 2025 volume`
14. `Schulze 2024 "soft channels of policy diffusion" local climate adaptation authors`
15. `Wang 2012 OR Krause "Symbolic or Substantive Policy" local commitment climate protection authors journal`

## Inclusion criteria

A record is included in the synthesis if it meets all of:

- Peer-reviewed journal article (or, where noted, a book chapter or working
  paper from an identifiable academic source), in English.
- Empirically studies, or builds a measurement or analytical framework for,
  local-government responses to a climate-emergency declaration, a
  voluntary climate commitment or pledge, or policy diffusion in local
  government climate policy.
- The unit of analysis is a local government (a council, municipality or
  equivalent), not a firm, a national government, or an individual.

Given the emergency-declaration literature only exists from December 2016
onward (the first declaration, by the City of Darebin), no lower date bound
was applied to that strand. The adjacent voluntary-commitment and
policy-diffusion strand was searched without a date bound, since its
relevance here is theoretical grounding rather than currency.

## Exclusion criteria

- Studies corporate, national, or individual voluntary commitments rather
  than local-government ones (for example, a firm-level voluntary
  environmental agreement).
- Measures public opinion or support for a symbolic policy rather than the
  local government's own policy-making or planning content.
- Advocacy-organisation web pages, campaign sites, news articles, or
  general encyclopedia entries (including Wikipedia and AI-summary sites)
  with no identifiable peer-reviewed method. These were used only to
  orient the search, never cited as evidence.
- A different kind of declaration entirely (for example, a faith-based
  international climate declaration, or a university's own climate-
  emergency declaration): kept out of the core synthesis because the
  population does not match, but noted in the framework synthesis where a
  parallel is instructive.
- Duplicate records: a preprint superseded by its own published version, or
  the same article indexed twice under a different repository mirror.

## Screening process and result

Every record returned by the six identification searches (37 after removing
exact duplicate mirrors of the same publication) was screened against the
criteria above by title and, where available, abstract. The full screening
log, with a decision and reason for every record, is in `prisma-log.csv`.
The count:

| Stage | Records |
|-------|--------:|
| Identified (six identification searches, plus the earlier scoping searches that surfaced two of the included studies) | 37 |
| Excluded (wrong population, not peer-reviewed, off-topic) | 20 |
| Duplicate or superseded (repository mirror or preprint of an included study) | 3 |
| Search outcome, not a document (the WALGA-specific search returning nothing) | 1 |
| Screened out pending full-text access (paywalled or unverifiable in this session; flagged for the Scopus/Web of Science re-run) | 5 |
| Included in synthesis | 8 |

`included-studies.csv` carries the 8 included records with full
bibliographic details, population, method and framework. `framework-
synthesis.md` compares what each assumes about the strength of the
instrument being studied, and states what needs to change before that
framework can be applied to WALGA's Declaration.

## What this confirms about the stated gap

None of the 37 records found across these searches, including the three
searches run specifically for "WALGA declaration on climate change" plus
academic, study or thesis (queries 3 and 7), returned a study of WALGA's
Declaration itself. That supports, but on a general web search rather than
a full database sweep, the claim in `EXECUTION_PROMPT.md` that nothing in
the literature studies WALGA's Declaration specifically. Treat that claim
as confirmed for this pass and re-confirm it in the Scopus and Web of
Science re-run before it is relied on in the thesis write-up.
