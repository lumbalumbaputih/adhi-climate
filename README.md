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
| [**transition-risk**](transition-risk/): WA's Biggest Emitters Under the Safeguard Mechanism (2016–2024) | Transition risk | Planned |
| [**water-security**](water-security/): Perth Water Security, Streamflow After the Rainfall Step-Change | Chronic physical risk | Pipeline ready, [awaiting data](dropzone/DROP_FILES_HERE.md) |
| [**swis-decarbonisation**](swis-decarbonisation/): How Fast Is WA's Main Grid Decarbonising? | Transition analytics | Pipeline ready, [awaiting data](dropzone/DROP_FILES_HERE.md) |
| [**extreme-heat**](extreme-heat/): Extreme Heat in Perth and the Pilbara | Acute physical risk | Pipeline ready, [awaiting data](dropzone/DROP_FILES_HERE.md) |
| [**marine-heatwaves**](marine-heatwaves/): Marine Heatwaves off the WA Coast | Acute physical risk | Pipeline ready, [awaiting data](dropzone/DROP_FILES_HERE.md) |

The portfolio site (`index.html`) ties these together: each project card opens a
case study with the headline findings, the charts, and direct links to the
write-up, notebook, and open data behind every number.

**Author:** Adhi Muhammad Faris Katili · Master of Environment and Climate
Emergency, Curtin University.

The data is all public (from NOAA NCEI and the Bureau of Meteorology). The
statistics are written from scratch and tested against known values; see each
project's `stats_utils.py` and `test_stats.py`. The two copies of
`stats_utils.py` are kept byte-identical, and CI (GitHub Actions) runs both
test suites and that identity check on every push and pull request.

## Licensing

The code in this repository is released under the [MIT License](LICENSE). The
committed cleaned datasets are derived from public sources: IBTrACS and ERSSTv5
(NOAA NCEI, public domain as US government works), GHCN-Daily (NOAA NCEI,
redistributing Bureau of Meteorology station observations), the Marshall (2003)
SAM index (British Antarctic Survey), and NOAA PSL climate indices. The
original providers' terms apply to the data; please cite the sources listed in
each project's README when reusing it.
