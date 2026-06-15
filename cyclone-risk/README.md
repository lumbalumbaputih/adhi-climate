# Western Australia Tropical Cyclone Climate Risk Analysis (1985 to 2024)

> Status: scaffolding complete, analysis pending data access. The pipeline,
> environment and download script are built and tested. The official data
> hosts are currently blocked by this environment's network policy, so the
> figures and findings below are placeholders until the authoritative data is
> downloaded and the notebook is run. See "How to reproduce".

## Research question

Has tropical cyclone intensity affecting Western Australia changed between 1985
and 2024, and does it correlate with rising sea surface temperatures?

## Why this matters

From 2026, Australia's mandatory climate disclosure standard **AASB S2**
requires companies to quantify their exposure to physical climate risk, both
acute (such as cyclones) and chronic (such as long term rainfall decline).
Western Australia's north and mid west coast, the Pilbara iron ore and LNG
corridor, the Kimberley, the Gascoyne and the Mid West, sit in one of the most
cyclone exposed industrial regions on earth. This project builds the kind of
evidence base that WA companies and their advisers need to make those
disclosures defensible: a transparent, reproducible, primary source analysis of
how cyclone intensity near WA has behaved over the satellite era.

## Data sources (all official primary sources)

| Dataset | Provider | Use | Access |
|---|---|---|---|
| IBTrACS v04r01, Southern Indian Ocean (`SI`) subset | NOAA NCEI | Storm tracks, peak wind, minimum pressure, category | `www.ncei.noaa.gov` |
| ERSSTv5 monthly sea surface temperature | NOAA Physical Sciences Lab | Indian Ocean SST anomaly for correlation | `downloads.psl.noaa.gov` |
| Southern Hemisphere TC database | Australian Bureau of Meteorology | Cross reference for Australian naming and WA proximity | `www.bom.gov.au` |

IBTrACS is the World Meteorological Organization's reference best track archive.
ERSSTv5 is NOAA's standard reconstructed SST product. Both are the recognised
authorities for this kind of work. Exact download URLs are encoded in
`fetch_data.py`.

## Method

The full workflow is in `cyclone_analysis.ipynb`, which runs top to bottom.

1. **Cleaning.** Load the IBTrACS SI subset. Restrict to seasons 1985 to 2024
   (intensity records before the modern satellite era are unreliable and are
   deliberately excluded). Drop observations with missing wind speed. Reduce to
   one record per storm: peak sustained wind, minimum central pressure, date and
   location of peak, and the full track. Flag any storm whose track passes
   within roughly 500 km of the WA coast (Kimberley, Pilbara, Gascoyne, Mid
   West). Outputs: `data/ibtracs_clean.csv` (all SI storms) and
   `data/ibtracs_wa.csv` (WA affecting subset).
2. **Exploratory analysis.** Annual storm counts, peak intensity distribution by
   decade, and the share of storms reaching Category 3 or stronger by decade.
3. **Trend analysis.** Linear regression of peak wind speed against year, and of
   minimum central pressure against year, for WA affecting storms, each with a
   Mann Kendall monotonic trend test and 95% confidence interval.
4. **Rapid intensification.** Count events where sustained wind rose by at least
   30 knots in any 24 hour window, by decade.
5. **SST correlation.** Compute the WA cyclone season (November to April) mean
   Indian Ocean SST anomaly per year from ERSSTv5, and correlate it against the
   annual mean peak intensity of WA affecting storms (Pearson r and p value).

## Key findings

_Pending the data run. This section will report the regression slopes, the
Mann Kendall results, the rapid intensification counts and the SST correlation,
stated honestly whether or not a statistically significant trend is present._

## What this means for WA industry and AASB S2

_Pending the data run. Ris will lead the domain interpretation here, tying the
measured trends (or their absence) to acute physical risk disclosure for WA
asset owners and operators._

## Recent context (to confirm before publishing)

The brief asks to reference the recent WA cyclone season for timeliness. The
specific season, storm names and damage figures should be verified against
primary BOM and insurance sources before they go into the final write up, to
keep every claim defensible. (Note: a "Category 5 Cyclone Narelle" causing about
$500M of damage does not match the historical record, where Narelle was a
January 2013 system that tracked offshore of WA. This needs checking with Ris.)

## Limitations

- Best track intensity estimates carry uncertainty, especially for systems far
  from land or aircraft reconnaissance, which is routine in the Southern Indian
  Ocean.
- Operational practice and instrumentation have changed over 40 years, which can
  introduce non climate trends; the 1985 start date mitigates but does not
  remove this.
- A 40 year record is short for separating a climate change signal from natural
  variability such as ENSO and the Indian Ocean Dipole.
- Correlation between SST and intensity is not by itself causation.

## How to reproduce

```bash
# 1. Create an environment and install dependencies
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Download the authoritative source data (writes to data/raw/)
#    In a restricted egress environment, first allow these hosts:
#      www.ncei.noaa.gov   downloads.psl.noaa.gov   www.bom.gov.au
python fetch_data.py

# 3. Run the analysis end to end
jupyter nbconvert --to notebook --execute cyclone_analysis.ipynb \
  --output cyclone_analysis.ipynb
```

## Repository layout

```
cyclone-risk/
  README.md                 this file
  requirements.txt          pinned dependencies
  fetch_data.py             downloads the authoritative source data
  cyclone_analysis.ipynb    the analysis, runs top to bottom
  data/
    ibtracs_clean.csv       all cleaned SI storms 1985 to 2024 (committed)
    ibtracs_wa.csv          WA affecting subset (committed)
    raw/                    downloaded source data (git ignored)
  charts/                   publication quality 300 dpi PNG outputs
  cv-blurb.txt              three sentence summary for job applications
```

## A note on method and authorship

This is a collaborative analysis built with AI tooling. Adhi (Ris) owns the
research question, the domain interpretation and the conclusions for WA industry
and AASB S2. The data engineering, statistics and charting were produced with an
AI coding assistant. This is a deliberate and increasingly standard way of
working, and every input is a documented, reproducible primary source.
