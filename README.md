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
| [**transition-risk**](transition-risk/): WA's Biggest Emitters Under the Safeguard Mechanism (2016–2025) | Transition risk | Complete |
| [**water-security**](water-security/): Perth Water Security, Streamflow After the Rainfall Step-Change (1967–2022) | Chronic physical risk | Complete |
| [**swis-decarbonisation**](swis-decarbonisation/): How Fast Is WA's Main Grid Decarbonising? (2006–2023) | Transition analytics | Complete |
| [**extreme-heat**](extreme-heat/): Extreme Heat in Perth and the Pilbara (1945–2025) | Acute physical risk | Complete |
| [**marine-heatwaves**](marine-heatwaves/): Marine Heatwaves off the WA Coast (1982–2026) | Acute physical risk | Complete |
| [**sea-level**](sea-level/): Sea-Level Rise at Fremantle (1897–2022) | Chronic physical risk | Complete |
| [**wheat-yields**](wheat-yields/): WA Wheat Yields and the Drying Trend (1861–2022) | Financial materiality | Complete |
| [**bushfire-weather**](bushfire-weather/): Fire Danger Trends in South West WA (FFDI, 1941–2026) | Acute physical risk | Complete |
| [**high-water**](high-water/): Coastal Flood Hours at Fremantle (1984–2026) | Acute physical risk | Complete |
| [**wa-councils-walga-climate**](wa-councils-walga-climate/): WA Councils' Climate Policy-Making After the WALGA Declaration | Local government policy research | Literature review done, document analysis pending |

The portfolio site (`index.html`) ties these together: each project card opens
that project's own page (`projects/<id>.html`) with the headline findings, the
interactive charts, and direct links to the write-up, notebook, and open data
behind every number, so any single analysis can be shared by URL.

The standard workflow for building and updating all of this, from staging raw
data to adding a project to the front page to re-encrypting the study notes, is
written up in [`PROCEDURE.md`](PROCEDURE.md).

**Author:** Adhi Muhammad Faris Katili · Master of Environment and Climate
Emergency, Curtin University.

The data is all public: NOAA NCEI and the Bureau of Meteorology for the
weather and ocean records, plus NOAA OISST (marine heatwaves), AEMO's WEM data
portal (grid generation), the University of Hawaii Sea Level Center (hourly
tide-gauge data), and the ABS historical agriculture collection (wheat
yields). The statistics are written from scratch and tested against known
values; see each
project's `stats_utils.py` and `test_stats.py`. The two copies of
`stats_utils.py` are kept byte-identical, and CI (GitHub Actions) runs both
test suites and that identity check on every push and pull request.

## Licensing

The code in this repository is released under the [MIT License](LICENSE). The
committed cleaned datasets are derived from public sources: IBTrACS and ERSSTv5
(NOAA NCEI, public domain as US government works), GHCN-Daily (NOAA NCEI,
redistributing Bureau of Meteorology station observations), OISST v2.1 (NOAA
NCEI / CoastWatch), UHSLC research-quality and fast-delivery hourly sea-level
data (Caldwell, Merrifield & Thompson, University of Hawaii Sea Level Center,
NOAA NCEI dataset doi:10.7289/V5T43R7N),
the Marshall (2003) SAM index (British Antarctic Survey),
NOAA PSL climate indices, ERA5 reanalysis (Copernicus/ECMWF, obtained via the
Open-Meteo archive API), WEM Facility SCADA data (AEMO), fuel mappings from
the OpenNEM WEM registry, historical crop statistics (Australian Bureau of
Statistics, 7124.0), and Safeguard Mechanism facility data (Clean Energy
Regulator). The original providers' terms apply to the data; please cite the
sources listed in each project's README when reusing it.
