# DROP DATA FILES HERE

Download the files below from the official sources and drop them into this
`dropzone/` folder. Each project's `build_dataset.py` detects its files by
content, so you do not need to rename anything. This staging area exists
because the remote sessions that build the analyses often cannot reach the
data hosts directly; you download, the pipeline does the rest.

======================================================================
PROJECT: water-security (Perth streamflow)          [DATA NEEDED]
======================================================================

1. BoM Hydrologic Reference Stations - daily streamflow   [REQUIRED]
----------------------------------------------------------------------
Bureau of Meteorology, http://www.bom.gov.au/water/hrs/

On the HRS map, pick 5-8 stations in the south-west WA region (the
Darling Range and SW forest catchments east and south of Perth; choose
the longest records on offer). For each station download the DAILY
streamflow CSV ("Daily flow", ML/day) and drop the files here.
The parser reads the standard HRS CSV layout (metadata lines, then
Date / Flow columns) and pulls the station number from the metadata.

2. Water Corporation annual inflow to Perth dams          [OPTIONAL]
----------------------------------------------------------------------
https://www.watercorporation.com.au (search "streamflow")

Used only as a cross-check of the gauged story. If the site lets you
export the annual inflow series, save it as a CSV with columns
year,inflow_GL and add a first line recording where it came from:
    # source: <URL you took it from>

Then run, inside water-security/:
    python3 build_dataset.py && python3 analysis.py && python3 viz.py

======================================================================
PROJECT: cyclone-risk (complete; files only needed to re-run
the pipeline from scratch)
======================================================================

1. IBTrACS v04r01 - Southern Indian Ocean subset   [REQUIRED]
----------------------------------------------------------------------
NOAA NCEI - International Best Track Archive for Climate Stewardship.
Expected file: ibtracs.SI.list.v04r01.csv  (tens of MB)

Direct link:
https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/ibtracs.SI.list.v04r01.csv

----------------------------------------------------------------------
2. ERSSTv5 - monthly sea surface temperature       [REQUIRED]
----------------------------------------------------------------------
NOAA Physical Sciences Lab - Extended Reconstructed SST, version 5.
Single NetCDF file covering all months 1854 to present.
Expected file: sst.mnmean.nc  (tens of MB)

Direct link:
https://downloads.psl.noaa.gov/Datasets/noaa.ersst.v5/sst.mnmean.nc

----------------------------------------------------------------------
3. BOM Southern Hemisphere tropical cyclone database   [OPTIONAL]
----------------------------------------------------------------------
Australian Bureau of Meteorology. Used only as a naming / WA-proximity
cross reference. The analysis runs fine without it.

Landing page (download the CSV from here):
http://www.bom.gov.au/cyclone/tropical-cyclone-knowledge-centre/databases/

Best-known direct CSV (may change; grab from the page above if it 404s):
http://www.bom.gov.au/clim_data/IDCKMSTM0S.csv

----------------------------------------------------------------------
When the two REQUIRED files are in this folder, tell me "files are in" and
I will take it from there.
