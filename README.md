# adhi-climate

A small portfolio of physical climate-risk analyses for Western Australia, built
to support ESG and sustainability roles and framed around **AASB S2**, Australia's
mandatory climate-disclosure standard.

Each project is a self-contained, reproducible Python analysis with a
plain-English write-up, honest statistics, and publication-quality charts.

| Project | Risk type | Status |
|---------|-----------|--------|
| [**cyclone-risk**](cyclone-risk/) — Tropical Cyclone Trends Affecting WA (1985–2024) | Acute physical risk | Complete |
| sw-wa-rainfall-decline — South West WA Rainfall Step-change (1950–2024) | Chronic physical risk | Planned |
| aasb-s2-readiness — Disclosure Gap Analysis, WA's Biggest Emitters | Disclosure review | Planned |

**Author:** Adhi Muhammad Faris Katili · Master of Environment and Climate
Emergency, Curtin University.

Data sources are public (NOAA NCEI, Bureau of Meteorology). Statistics are
implemented from first principles and unit-tested; see each project's
`stats_utils.py` and `test_stats.py`.
