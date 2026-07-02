# DROP DATA FILES HERE

Download the files below from the official sources and drop them into the
matching **subfolder** of `dropzone/` (`dropzone/water-security/`,
`dropzone/sea-level/`, and so on, one per project below). Each project's
`build_dataset.py` looks in its own subfolder first and detects files by
content, so you do not need to rename anything. This staging area exists
because the remote sessions that build the analyses often cannot reach the
data hosts directly; you download, the pipeline does the rest.

(The one exception is `cyclone-risk`, an older, already-complete project
whose files still go straight into `dropzone/` itself, per its own section
below.)

======================================================================
PROJECT: water-security (Perth streamflow)          [DATA NEEDED]
======================================================================

1. BoM Hydrologic Reference Stations - daily streamflow   [REQUIRED]
----------------------------------------------------------------------
Bureau of Meteorology, http://www.bom.gov.au/water/hrs/

On the HRS map, pick 5-8 stations in the south-west WA region (the
Darling Range and SW forest catchments east and south of Perth; choose
the longest records on offer). For each station download the DAILY
streamflow CSV ("Daily flow", ML/day) and drop the files into
    dropzone/water-security/
The parser reads the standard HRS CSV layout (metadata lines, then
Date / Flow columns) and pulls the station number from the metadata.

2. Water Corporation annual inflow to Perth dams          [OPTIONAL]
----------------------------------------------------------------------
https://www.watercorporation.com.au (search "streamflow")

Used only as a cross-check of the gauged story. If the site lets you
export the annual inflow series, save it as a CSV with columns
year,inflow_GL and add a first line recording where it came from:
    # source: <URL you took it from>
Drop it in dropzone/water-security/ alongside the HRS files.

Then run, inside water-security/:
    python3 build_dataset.py && python3 analysis.py && python3 viz.py

======================================================================
PROJECT: swis-decarbonisation (WA main grid)        [DATA NEEDED]
======================================================================

1. AEMO WEM facility generation (SCADA), monthly CSVs     [REQUIRED]
----------------------------------------------------------------------
AEMO WEM data portal, https://data.wa.aemo.com.au

Download the monthly "Facility SCADA" CSV files for the span you want
analysed (the record starts in the mid-2000s; whole calendar years
only, since incomplete years are excluded from trends). Drop them all
into
    dropzone/swis-decarbonisation/
the parser needs a date column, a facility column, and an energy (MWh)
or power (MW) column.

2. WEM facility register (fuel mapping)                   [REQUIRED]
----------------------------------------------------------------------
From the same portal (or AEMO's WEM facilities page). Any CSV with a
facility-code column plus a fuel or technology column works, dropped in
the same dropzone/swis-decarbonisation/ folder. If no register with
fuels is available, hand-build facility_fuel.csv with columns
facility,fuel and a "# source:" first line saying where each
assignment came from.

3. NGA emission factors                                    [OPTIONAL]
----------------------------------------------------------------------
After the first build_dataset.py run, fill in
swis-decarbonisation/data/emission_factors.csv from the current
National Greenhouse Accounts factors workbook (cite it in the source
column). Without it the mix analysis still runs; only the intensity
series is skipped.

Then run, inside swis-decarbonisation/:
    python3 build_dataset.py && python3 analysis.py && python3 viz.py

======================================================================
PROJECT: extreme-heat (Perth + Pilbara)             [DATA NEEDED]
======================================================================

Option A (preferred): on any machine with open network access, run
    cd extreme-heat && python3 build_dataset.py --fetch
which downloads Perth Airport and Port Hedland from the NCEI API and
validates the station names.

Option B: download daily TMAX/TMIN yourself and drop the files into
    dropzone/extreme-heat/
Accepted formats (detected by content, any filename):
  - GHCN daily-summaries CSV (STATION,NAME,DATE,TMAX[,TMIN]), from
    https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=ASN00009021&startDate=1950-01-01&endDate=2025-12-31&dataTypes=TMAX,TMIN&format=csv&includeStationName=true&units=metric
    (repeat with stations=ASN00004032 for Port Hedland; verify the
    returned NAME column says PERTH AIRPORT / PORT HEDLAND)
  - BoM Climate Data Online daily max/min temperature CSVs
    (bom.gov.au/climate/data, one file per element per station)

Then run, inside extreme-heat/:
    python3 build_dataset.py && python3 analysis.py && python3 viz.py

======================================================================
PROJECT: marine-heatwaves (Ningaloo coast)          [DATA NEEDED]
======================================================================

NOAA OISST v2.1 daily SST for the study box, as ERDDAP CSV   [REQUIRED]
----------------------------------------------------------------------
Any ERDDAP server carrying OISST v2.1 works (NOAA CoastWatch's
coastwatch.pfeg.noaa.gov and NCEI's ERDDAP both do; search the server
for "OISST" and use its Data Access Form to build the URL). Subset:

  latitude  -23.5 to -21.5, longitude 112.5 to 114.5
  time      1982-01-01 to the latest available
  variable  sst, format .csv

The parser expects the standard ERDDAP layout (header row, units row,
then time,latitude,longitude,sst). If the server limits request size,
split the download into several date ranges; drop all the files into
    dropzone/marine-heatwaves/
(one study box per run).

Then run, inside marine-heatwaves/:
    python3 build_dataset.py && python3 analysis.py && python3 viz.py

======================================================================
PROJECT: sea-level (Fremantle tide gauge)           [DATA NEEDED]
======================================================================

PSMSL monthly RLR data for Fremantle (station 111)         [REQUIRED]
----------------------------------------------------------------------
https://psmsl.org/data/obtaining/  ->  search "Fremantle" (station id
111)  ->  download the monthly RLR data file. It is a small semicolon-
separated text file (decimal year; height in mm; flags), typically
named 111.rlrdata, with heights around 6500-7500 mm. Drop it as-is into
    dropzone/sea-level/

CAREFUL: the station page also offers a "metric" file (111.metdata,
heights in the hundreds of mm). That variant can contain datum shifts
and the pipeline refuses it; it is the RLR file that is needed.

Then run, inside sea-level/:
    python3 build_dataset.py && python3 analysis.py && python3 viz.py

======================================================================
PROJECT: wheat-yields (WA wheatbelt)                [DATA NEEDED]
======================================================================

WA wheat area and production by season                     [REQUIRED]
----------------------------------------------------------------------
From ABARES (Australian crop report statistical tables, or the
historical agricultural data on agriculture.gov.au/abares) or the ABS
agricultural commodities collection. The spreadsheets change layout
between vintages, so fill this simple CSV from whichever official
table you download (keep the source line), and drop it into
    dropzone/wheat-yields/

    # source: <URL of the table you used>
    year,wheat_area_ha,wheat_production_t
    1975,3200000,4100000
    ...

Label each season by the year the crop was SOWN ("1975-76" -> 1975).
Season-labelled exports ("1975-76" in a year/season column) also parse.

Then run, inside wheat-yields/:
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
