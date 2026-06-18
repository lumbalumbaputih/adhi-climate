# Execution Prompt - AASB S2 Readiness: WA's Biggest Emitters

> Portfolio project #3 of the `adhi-climate` suite (disclosure gap analysis, not data science).
> Paste this whole file into a fresh session to start work. Self-contained: no prior context needed.
> Mirrors the structure of the completed cyclone project (`adhi-climate/cyclone-risk/`) and the rainfall execution prompt. Where this one differs: no code, no statistics. The deliverable is a structured, evidence-cited scoring of six companies' public disclosures against the four AASB S2 pillars.

---

## Project framing

**Research question.** How ready are WA's largest ASX-listed emitters to meet AASB S2 mandatory climate disclosure requirements, and where are the common gaps?

**CV framing.** *"AASB S2 Readiness Review: WA's Largest Emitters - A Structured Gap Analysis Across the Four Disclosure Pillars."*

**Companies in scope (6).** BHP, Rio Tinto, Woodside Energy, Fortescue, Mineral Resources (MinRes), South32.

**Why it matters.** This mirrors exactly what graduate ESG analysts at Deloitte, KPMG, GHD and Arup are asked to do in 2026: read client sustainability reports, apply the AASB S2 framework, find the gaps, present the findings. Doing it self-directed signals genuine readiness. All six names are instantly recognisable to any Perth employer. Target: live on GitHub before Deloitte graduate applications open 1 July 2026.

**Repo.** Umbrella repo `adhi-climate`, subfolder `aasb-s2-review/`.

**Source of truth for scope and rubric.** The project wiki page `1-wiki/projects/aasb-s2-readiness.html` holds the canonical brief. This prompt operationalises it and adds the verified AASB S2 sub-requirements and scoring detail the wiki page does not carry. If the two ever disagree, fix the wiki page.

---

## Division of labour

- **Kai** - sources and reads the reports, builds the scoring matrix, scores each sub-requirement with page-cited evidence, drafts the gap analysis, builds the HTML report and the written summary.
- **Ris** - reviews scores for plausibility, supplies domain interpretation (what each gap means in practice and what a consultant would actually recommend), writes the final narrative voice, owns the interview talking points. Ris does not score, but must be able to speak to the findings for about five minutes without notes before this goes on a CV.

---

## Read before starting (the credibility tests)

This is a review of *disclosure*, and the whole project lives or dies on honesty about what that does and does not show. Internalise these five points before scoring anything.

1. **Score disclosed readiness, not actual readiness.** A score reflects what a company has *published*, not what it does internally. A low score may mean a real gap or merely an undisclosed control. Say this explicitly in the write-up. Never imply a company is unprepared when the evidence only shows it is quiet.

2. **Public documents only.** Sustainability reports, climate / transition reports, annual reports, climate action plans, and AASB S2 / IFRS S2 / TCFD content indices. No internal data, no analyst calls, no paywalled databases.

3. **Mind the reporting timeline. These six are all Group 1 reporters.** AASB S2 is phased: Group 1 from periods beginning on or after 1 Jan 2025, Group 2 from 1 Jul 2026, Group 3 from 1 Jul 2027. All six companies are Group 1. That means the FY2024 and most FY2025 reports you will score are *pre-mandatory*, voluntary TCFD-era disclosures. That is the point of a *readiness* review: measuring how close voluntary practice already sits to the mandatory bar that is now biting. Confirm each company's financial year end and flag which report is its first mandatory AASB S2 report. As a starting assumption to verify at source: Rio Tinto and Woodside report on a 31 December year end (first mandatory period = CY2025); BHP, Fortescue, MinRes and South32 report on a 30 June year end (first mandatory period = the year ending 30 June 2026).

4. **Score against AASB S2 specifically, not generic TCFD.** AASB S2 reproduces IFRS S2 content (so the paragraph structure below is faithful) but adds Australian modifications that change what "compliant" means:
   - Scenario analysis must use at least two scenarios, including one consistent with about 1.5°C warming and one high-warming scenario well above 2.5°C.
   - Scope 3 emissions are relieved in the first reporting year and mandatory from the second. Note when a company is leaning on that relief.
   - GHG measurement may use NGER methods, but AASB S2 expects the latest IPCC GWP values (AR6), while NGER still uses AR5. Watch for the mismatch.
   - There is time-limited liability relief for certain forward-looking statements (Scope 3, scenario analysis, transition plans). Do not treat caution in those areas as a pure failure; note it in context.

5. **Evidence discipline. No fabricated citations, ever.** Every non-zero score needs at least one citation: report short-name, page or section, and ideally a short verbatim quote. A score of 0 needs a note confirming the team searched and found nothing material. Do not invent page numbers, quotes, report titles, or figures. If you cannot verify it in the document, it does not exist for scoring purposes. This is the same fabrication rule that made projects #1 and #2 credible.

---

## Source material - acquire in this order

For each of the six companies, gather the most recent available documents in this priority order, then log them before reading.

| # | Document | Why |
|---|----------|-----|
| 1 | Standalone **climate report / climate change report / climate transition action plan** (most recent) | The densest source for Strategy, scenario analysis, Metrics and Targets. Where it exists, it is the spine. |
| 2 | **Sustainability / ESG report** (most recent) | Emissions data, targets, assurance statements, risk narrative. |
| 3 | **Annual report** (most recent) | Governance (board and committee roles), remuneration report (climate-linked pay), financial-effects disclosure, ERM integration. |
| 4 | **AASB S2 / IFRS S2 / TCFD content index** (if published) | A company-supplied map of where each disclosure sits. Use it to navigate, not as evidence in itself. |

Where to get them: each company's investor-relations and sustainability webpages, and the ASX announcements platform. Record the financial year of each document (FY2024 or FY2025) because maturity moves year on year.

Build the source library before scoring:
- Save raw PDFs to `data/raw/` (gitignored, do not commit large binaries).
- Create `data/source-library.csv` with columns: `company, doc_type, title, financial_year, url, page_count, date_retrieved`.
- One row per document. This table is the provenance backbone for every later citation.

---

## The AASB S2 framework - four pillars with verified sub-requirements

Score each company against every sub-requirement below. The IDs (G1, S1, R1, M1 ...) are the row keys in the scoring matrix. Paragraph references are to AASB S2 (which mirror IFRS S2). Verify wording against the standard itself at `https://standards.aasb.gov.au/aasb-s2-sep-2024` before finalising; treat the descriptions here as the working checklist, not the legal text.

### Pillar 1 - Governance (AASB S2 paras 5 to 6)

| ID | Disclosure requirement | Gap watch |
|----|------------------------|-----------|
| G1 | Names the board, committee or individual(s) responsible for oversight of climate risks and opportunities, with the responsibility reflected in terms of reference, mandates or role descriptions | Vague "the Board oversees ESG" with no named committee or charter reference |
| G2 | Explains how the oversight body ensures the right skills and competencies to govern climate (skills matrix, director training) | No skills disclosure; assumes competence |
| G3 | States how and how often the oversight body is informed about climate risks and opportunities | No cadence; no reporting line into the board |
| G4 | Explains how the oversight body factors climate into overseeing strategy, major transactions and risk management, including trade-offs | Climate named but not tied to actual decisions or capex approvals |
| G5 | Explains how the oversight body oversees climate target-setting and monitors progress, including whether performance is linked to remuneration | Targets mentioned but no oversight mechanism; pay link unclear |
| G6 | Describes management's role: the delegated position or committee, how oversight is exercised, and whether dedicated controls and procedures are used and integrated with other functions | Management role absent or purely nominal |

### Pillar 2 - Strategy (AASB S2 paras 8 to 23)

| ID | Disclosure requirement | Gap watch |
|----|------------------------|-----------|
| S1 | Identifies the specific climate risks and opportunities that could reasonably affect prospects, and labels each as physical or transition | Generic risk language; no company-specific risks; opportunities ignored |
| S2 | Defines the short, medium and long-term time horizons used and links them to planning and capital horizons | Horizons undefined or not tied to the business |
| S3 | Describes current and anticipated effects on the business model and value chain, and where they concentrate (assets, geographies, inputs) | No value-chain view; no concentration disclosed |
| S4 | Describes effects on strategy and decision-making, including resource allocation and any transition plan with its key assumptions, dependencies and progress against prior plans | Aspirational net-zero statement with no plan, assumptions or progress |
| S5 | Discloses current and anticipated financial effects on financial position, performance and cash flows over short, medium and long term, quantified where possible, and how climate is reflected in financial planning | Qualitative only; no financial quantification (the most common large gap) |
| S6 | Climate resilience via scenario analysis: discloses the scenarios used (must include about 1.5°C and a high-warming scenario above 2.5°C), the methodology, time horizons and key assumptions | Transition scenarios only, no physical; single scenario; method opaque |

### Pillar 3 - Risk Management (AASB S2 paras 24 to 26)

| ID | Disclosure requirement | Gap watch |
|----|------------------------|-----------|
| R1 | Describes the processes and policies to identify and assess climate risks, including inputs, parameters and use of scenario analysis | Process asserted but not described |
| R2 | Describes how the nature, likelihood and magnitude of risks are assessed (qualitative vs quantitative, thresholds) | No assessment method; no thresholds |
| R3 | Describes how climate risks are prioritised relative to other risk types | No prioritisation methodology disclosed |
| R4 | Describes how climate risks are monitored and whether the process changed from the prior period | Static; no monitoring or change disclosure |
| R5 | Describes processes to identify, assess, prioritise and monitor climate opportunities | Opportunities omitted from the risk process |
| R6 | States the extent to which, and how, these processes are integrated into overall enterprise risk management | Climate risk siloed from ERM (a classic gap) |

### Pillar 4 - Metrics and Targets (AASB S2 paras 27 to 37)

| ID | Disclosure requirement | Gap watch |
|----|------------------------|-----------|
| M1 | Absolute gross Scope 1 GHG emissions (CO2-e), measured per the GHG Protocol or NGER where applicable | Missing, dated, or method unstated |
| M2 | Absolute gross Scope 2 GHG emissions, with location-based and market-based where relevant | Only one Scope 2 basis given |
| M3 | Absolute gross Scope 3 GHG emissions, with the categories included disclosed (mandatory from year 2; note if relief is used) | Scope 3 absent or only partial categories (the single most common gap, and most material for these emitters) |
| M4 | Amount or percentage of assets or business activities vulnerable to transition risks | Not quantified; no stranded-asset view |
| M5 | Amount or percentage of assets or business activities vulnerable to physical risks | Not quantified |
| M6 | Amount or percentage of assets or business activities aligned with climate opportunities | Opportunity exposure not measured |
| M7 | Capital deployment: amount of capex, financing or investment toward climate risks and opportunities | No climate capex figure |
| M8 | Internal carbon price: whether and how it is applied, and the price per tonne CO2-e | No internal price, or price undisclosed |
| M9 | Remuneration: whether and how climate is factored into executive pay, and the percentage linked | Claimed link with no percentage or metric |
| M10 | Industry-based metrics relevant to the sector (SASB-based, for mining and oil and gas) | Cross-industry only; no sector metrics |
| M11 | Targets disclosed with, for each: metric, objective (mitigation or adaptation), coverage, base year or baseline, target period and interim milestones | Headline 2050 target with no baseline or interim steps |
| M12 | For GHG targets: scopes and gases covered, gross vs net, reliance on offsets or credits and the extent, sectoral decarbonisation approach, and alignment with the latest international agreement (Paris 1.5°C) | Net target leaning heavily and silently on offsets |
| M13 | Performance against each target over time, any revisions, and whether emissions or targets are third-party assured or validated (for example SBTi, external assurance) | No progress tracking; no assurance |

That is 6 + 6 + 6 + 13 = 31 sub-requirements per company, 186 scored cells in total.

---

## Scoring methodology

Score every sub-requirement on the 0 to 4 rubric from the project wiki:

| Score | Meaning |
|-------|---------|
| 0 - Absent | Not addressed in any material way in public disclosures |
| 1 - Acknowledged | Mentioned but qualitative only; no quantification, no process disclosed |
| 2 - Partial | Framework element present but incomplete (for example scenario analysis started but limited in scope) |
| 3 - Substantially compliant | Meets most of the AASB S2 requirement for this item; minor gaps only |
| 4 - Full | Comprehensive disclosure; third-party verified or assured where applicable |

Rules:
- **Every score carries evidence.** Non-zero scores need report short-name + page or section + ideally a short verbatim quote. A 0 needs a "searched, not found" note.
- **Roll-up.** Pillar score = mean of that pillar's sub-requirement scores, to one decimal. Company readiness score = mean of the four pillar scores.
- **Maturity bands** for plain-English reporting: 0.0 to 1.0 Nascent, 1.1 to 2.0 Emerging, 2.1 to 3.0 Developing, 3.1 to 4.0 Advanced.
- **Two-pass scoring.** Kai scores first from evidence. Ris reviews for plausibility before any score is locked. Record both in the matrix so disagreements are visible.
- **Consistency over generosity.** Apply the same bar to all six. When unsure between two scores, pick the lower and explain why in the gap note. Under-claiming protects credibility; over-claiming destroys it.

---

## Work steps

| # | Step | Output |
|---|------|--------|
| 1 | Build the source library: download the most recent reports for all six companies, log them in `data/source-library.csv`, confirm each company's year end and first mandatory AASB S2 period | `data/raw/*` + `data/source-library.csv` |
| 2 | Build the empty scoring matrix: one row per company per sub-requirement (186 rows) with the columns defined below | `scoring-matrix.csv` (skeleton) |
| 3 | Score each company across all 31 sub-requirements with page-cited evidence; Kai first pass | `scoring-matrix.csv` (Kai scores) |
| 4 | Ris review pass: plausibility check and domain interpretation; lock scores | `scoring-matrix.csv` (locked) |
| 5 | Identify common gaps: patterns across companies (for example all weak on Scope 3, all partial on physical-risk scenario analysis, financial quantification near-universally absent) | `gap-summary.csv` + heatmap |
| 6 | Write the plain-English findings: what the scores mean, what each gap costs in AASB S2 compliance terms, what a consultant would recommend to close it | `README.md` |
| 7 | Build the HTML report (public, readable without prior ESG knowledge) and the supporting CV blurb and interview brief | `report.html` · `cv-blurb.txt` · `INTERVIEW_BRIEF.md` |

---

## Deliverables and formats

| Deliverable | File | Spec |
|-------------|------|------|
| Source library | `data/source-library.csv` | Provenance for every citation |
| Scoring matrix | `scoring-matrix.csv` (and an `.xlsx` view with summary sheets) | Columns: `company, pillar, subreq_id, subreq_desc, score, evidence_report, evidence_page, evidence_quote, gap_note, kai_score, ris_score, status`. XLSX adds two summary sheets: per-company pillar scores, and a cross-company heatmap (companies as rows, sub-requirements or pillars as columns, colour by score) |
| Gap summary | `gap-summary.csv` | One row per sub-requirement: mean score across the six, count at 0, the common pattern, the consultant recommendation |
| Written summary | `README.md` | Plain-English: question, method, the headline scores, the common gaps, what they mean, limitations, how to reproduce. Reads cleanly for a climate-literate non-coder |
| HTML report | `report.html` | Self-contained single file. Uses the Adhi design system (read `memory/design/tokens.md` first; do not invent brand values). Includes the heatmap, a one-paragraph profile per company, and the common-gaps narrative. Readable by an employer without downloading anything |
| CV blurb | `cv-blurb.txt` | Three sentences: scope (six WA emitters, AASB S2, four pillars), method (evidence-cited scoring of public disclosures), and the single most striking finding |
| Interview brief | `INTERVIEW_BRIEF.md` | About five minutes of talking points, matching the cyclone project's brief in tone: the pitch, the common gaps, and what a consultant does about them |

---

## Repo structure (what done looks like)

```
adhi-climate/
└── aasb-s2-review/
    ├── EXECUTION_PROMPT.md        # this file
    ├── README.md                  # written summary and findings
    ├── scoring-matrix.csv
    ├── scoring-matrix.xlsx        # with heatmap + summary sheets
    ├── gap-summary.csv
    ├── report.html                # public report, Adhi design system
    ├── cv-blurb.txt
    ├── INTERVIEW_BRIEF.md
    └── data/
        ├── raw/                   # gitignored: downloaded PDFs
        └── source-library.csv
```

All deliverables live inside `aasb-s2-review/`, matching how `cyclone-risk/` and `rainfall-decline/` keep everything in their own subfolder. This is a self-contained git repo project, so the HTML report stays here with its siblings rather than going to `2-claout/`.

---

## Constraints

| Constraint | Rule |
|------------|------|
| Writing style | Chicago 17th author-date if any external sources are cited. IELTS 6.5 to 7 reading level: clear, structured, hedged. No em dashes. No double-hyphens. In the README prose and HTML report, no bullet-point lectures; write in cohesive paragraphs (tables and short lists are fine for the matrix and findings) |
| Evidence | Every non-zero score cited to a page or section; verify quotes; never fabricate page numbers, quotes, titles or figures |
| Design | HTML report uses the Adhi design system. Read `memory/design/tokens.md` before building it |
| Honesty framing | Score discloses readiness, not actual readiness; state limitations plainly; do not imply unpreparedness from silence |
| Workspace | Final files in `3-projects/adhi-climate/aasb-s2-review/`. Raw PDFs in `data/raw/` (gitignored). Append a `1-wiki/logs/file-log.html` entry when files are created or moved. Update the project page status log |
| Scope discipline | Six companies, four pillars, the 31 sub-requirements above. Resist adding companies or inventing new criteria mid-stream |

---

## Session start instruction

Start with **Step 1**. Do not score anything yet. First confirm the source library: for each of the six companies, list the exact report titles and financial years you found, their URLs, and each company's financial year end and first mandatory AASB S2 period. Show that table and pause for Ris to confirm the document set is the right one before any scoring begins. Garbage in, garbage out: the whole review rests on scoring the correct, most recent documents.

---

## Interview-readiness bar (for Ris, before this goes on a CV)

Be able to speak, unaided, for about five minutes to: (1) what the four AASB S2 pillars require, in plain words; (2) which gaps were most common across the six companies and why (expect Scope 3, physical-risk scenario analysis, and financial quantification to dominate); and (3) what an ESG consultant would actually do to close those gaps. That is the minimum bar. Kai prepares `INTERVIEW_BRIEF.md` once the scoring is locked.
