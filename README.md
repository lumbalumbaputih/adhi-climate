# adhi-climate

A small portfolio of climate-risk analyses for Western Australia. It is built to
support ESG and sustainability roles, and it is framed around **AASB S2**,
Australia's new rules that require big companies to report their climate risks.

Each project is a self-contained, repeatable Python analysis with a plain-English
write-up, honest statistics, and clear charts. Anyone can re-run it from scratch.

| Project | Risk type | Status |
|---------|-----------|--------|
| [**cyclone-risk**](cyclone-risk/): Tropical Cyclone Trends Affecting WA (1985–2024) | Acute physical risk | Complete |
| [**rainfall-decline**](rainfall-decline/): South West WA Rainfall Decline (1950–2024) | Chronic physical risk | Complete |
| [**aasb-s2-review**](aasb-s2-review/): Disclosure Gap Analysis, WA's Biggest Emitters (BHP, Rio Tinto, Woodside) | Disclosure review | Complete |

The portfolio site (`index.html`) ties these together: each project card opens a
case study with the headline findings, the charts, and direct links to the
write-up, notebook, and open data behind every number.

**Author:** Adhi Muhammad Faris Katili · Master of Environment and Climate
Emergency, Curtin University.

The data is all public (from NOAA NCEI and the Bureau of Meteorology). The
statistics are written from scratch and tested against known values; see each
project's `stats_utils.py` and `test_stats.py`.
