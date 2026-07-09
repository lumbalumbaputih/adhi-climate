(function () {
  // Everything on the page links back to the work that produced it.
  const REPO = "https://github.com/lumbalumbaputih/adhi-climate";
  const ghBlob = (path) => `${REPO}/blob/main/${path}`;
  const ghTree = (path) => `${REPO}/tree/main/${path}`;

  window.PORTFOLIO = {
    repo: REPO,
    profile: {
      name: "Adhi Katili",
      role: "Climate & Sustainability",
      tagline: "I turn Western Australia's climate data into decisions business and government can act on.",
      intro:
        "I dig into the real climate risks facing Western Australia, like what is actually happening to its cyclones, its drying south-west, its shrinking rivers, its hotter summers and its rising seas, and I check how the state's biggest companies report those risks under Australia's new climate rules (AASB S2). The goal is simple: turn raw climate data into clear answers that business and government can act on.",
      location: "Western Australia · remote-friendly",
      email: "adhiazure@gmail.com",
      linkedin: "https://www.linkedin.com/in/adhi-m/",
      availability: "Available for internships · Perth, WA or remote",
    },
    stats: [
      { label: "Projects complete", value: "11", caption: "storms to safeguards" },
      { label: "Longest record", value: "161", unit: "yrs", caption: "WA wheat yields, 1861–2022" },
      { label: "Facilities analysed", value: "175", caption: "WA power + Safeguard emitters" },
      { label: "Risk types covered", value: "4", caption: "AASB S2, all four quadrants" },
    ],
    projects: [
      {
        id: "wa-cyclones",
        title: "WA Cyclone Intensity Trends",
        year: "1985–2024",
        status: "Complete",
        category: ["Physical risk", "Climate data", "Data viz"],
        icon: "wind",
        meta: "7 charts · reproducible notebook · 7 open datasets",
        summary:
          "Forty years of cyclone records, checked against one simple question: as the ocean warmed, did the storms hitting WA actually get stronger?",
        result: { value: "40", unit: "yrs", label: "of storm records" },
        headline:
          "The ocean off Western Australia warmed about half a degree in 40 years. Whether the cyclones weakened or strengthened depends on which wind record you trust, and that ambiguity is the finding.",
        body:
          "Most people assume that as the ocean warms, storms get stronger. I put that to the test for Western Australia using 40 years of official cyclone records from international and Australian weather agencies, looking at how strong the storms got and how often they strengthened very fast. The answer turned out to hinge on the measurement itself: Australia's wind record drifts down while the US record for the very same storms drifts up, and neither trend is statistically solid. That ambiguity is exactly why it is worth knowing. It matters because WA's biggest companies now have to report their climate risks under new Australian rules (AASB S2), and those reports need to be built on what the data really shows, not on gut feel.",
        findings: [
          { value: "+0.5", unit: "°C", label: "The ocean is warming", text: "The sea where these cyclones form has warmed by about half a degree since the 1980s. This part is rock solid in the data." },
          { value: "−3.6 / +3.9", unit: "kt/decade", label: "Two records, two directions", text: "Australia's 10-minute wind record drifts down while the US 1-minute record drifts up, for the same storms. Neither trend is significant. The record cannot settle the direction." },
          { value: "−0.08", unit: "link", label: "Warmer seas, stronger storms?", text: "No. Once the shared long-term trends are removed, warm years and strong-storm years are unrelated (r = −0.08). The connection people assume simply is not in WA's record." },
          { value: "~5", unit: "/year", label: "Storms near the coast", text: "About five cyclones come within 500 km of the WA coast in a typical year, a number that has held steady or dipped slightly." },
        ],
        charts: [
          { src: "cyclone-risk/charts/01_annual_count.png", caption: "How many cyclones each year: steady, with a slight dip" },
          { src: "cyclone-risk/charts/02_intensity_by_decade.png", caption: "How strong the storms got, decade by decade: edging down, not up" },
          { src: "cyclone-risk/charts/03_trend_wind_speed.png", caption: "Same storms, two wind records, opposite trends" },
          { src: "cyclone-risk/charts/04_trend_pressure.png", caption: "Pressure, the cleanest measure: leaning weaker, but borderline" },
          { src: "cyclone-risk/charts/05_rapid_intensification.png", caption: "Storms strengthening very fast: it looks like it is rising, but read with care" },
          { src: "cyclone-risk/charts/06_sst_correlation.png", caption: "Warmer oceans did not mean stronger storms, raw or detrended" },
          { src: "cyclone-risk/charts/07_proximity_sensitivity.png", caption: "Robustness: peak strength near the coast, and 300/500/700 km definitions" },
        ],
        meaning:
          "The lesson is simple but important: you cannot judge WA's future cyclone danger just by looking at the recent past. The ocean has warmed, yet the record cannot even settle whether the storms strengthened or weakened, so honest climate-risk reporting has to lean on future projections rather than extend the past in either direction. And a quiet long-term trend does not mean we are safe. Severe Tropical Cyclone Narelle in 2026 caused around $500 million in damage, a reminder that the real danger lives in the rare, extreme storm, not the average one.",
        resources: [
          { label: "Read the full analysis", href: ghBlob("cyclone-risk/README.md"), icon: "file-text" },
          { label: "Open the notebook", href: ghBlob("cyclone-risk/cyclone_analysis.ipynb"), icon: "bar-chart" },
          { label: "Cleaned datasets (7 CSVs)", href: ghTree("cyclone-risk/data"), icon: "layers" },
          { label: "All charts", href: ghTree("cyclone-risk/charts"), icon: "scan" },
          { label: "View on GitHub", href: ghTree("cyclone-risk"), icon: "github" },
        ],
        feature: 5,
        dataset: {
          caption: "WA-affecting cyclones by decade (IBTrACS + BOM)",
          columns: ["Decade", "WA storms", "Peak wind, BOM (kt)", "Peak wind, USA (kt)", "Mean min pressure (hPa)", "Reached Cat 3+"],
          rows: [
            ["1985–94", "47", "76", "65", "959", "17%"],
            ["1995–04", "55", "78", "80", "955", "38%"],
            ["2005–14", "50", "69", "77", "964", "28%"],
            ["2015–24", "42", "63", "75", "973", "19%"],
          ],
        },
        vizKey: "cyclone",
        hasMap: true,
        scrolly: true,
        viz: [
          { type: "scatter", key: "sst_scatter", title: "Warmer seas vs storm strength" },
          { type: "bar", key: "intensity_decade", title: "Peak intensity by decade" },
          { type: "line", key: "trend_wind", title: "Mean peak wind, season by season" },
          { type: "line", key: "trend_pressure", title: "Mean central pressure, season by season" },
          { type: "bar", key: "ri_decade", title: "Rapid intensification by decade", keys: [{ k: "wa", label: "Near WA", color: "var(--accent)" }, { k: "si", label: "Whole basin", color: "var(--leaf)" }] },
          { type: "line", key: "annual_count", title: "Cyclones within 500 km each year" },
        ],
        tags: ["Official cyclone records", "Warmer seas, not stronger storms", "Climate-risk reporting (AASB S2)"],
        updates: [
          {
            date: "15 Jun 2026",
            title: "First published",
            found: "Forty years of official cyclone records, put against one question: as the ocean off WA warmed, did the storms get stronger? The first pass suggested they had drifted slightly weaker.",
            change: "Published the full pipeline: annual counts, intensity by decade, long-term trends, rapid intensification and the ocean-temperature link, with every chart backed by an open dataset.",
          },
          {
            date: "18 Jun 2026",
            title: "Plain-language rewrite",
            found: "The write-up assumed the reader knew what a Mann-Kendall test was. A portfolio only works if anyone can follow the findings without a statistics degree.",
            change: "Rewrote every reader-facing sentence in plain English and moved the technical detail into the methods notes, without softening a single number.",
          },
          {
            date: "2 Jul 2026",
            title: "The audit that changed the headline",
            found: "A full self-audit caught a real problem: the 'storms drifted weaker' headline leaned on Australia's 10-minute wind record, which covers only about 41% of these storms, and its coverage grows over time. The US 1-minute record for the very same storms trends the other way.",
            change: "Rebuilt the analysis to show both wind records side by side, kept pressure as the tie-breaker, added detrended ocean-heat correlations and a coastal-proximity check, and rewrote the headline to what the data actually supports: the record cannot settle the direction, and that ambiguity is the finding.",
          },
        ],
      },
      {
        id: "sw-wa-rainfall",
        title: "SW WA Rainfall Decline",
        year: "1950–2024",
        status: "Complete",
        category: ["Physical risk", "Climate data", "Data viz"],
        icon: "droplet",
        meta: "5 charts · reproducible pipeline · 6 open datasets",
        summary:
          "One of the clearest examples anywhere of a region drying out: the south-west corner of WA, where winter rain dropped sharply and never recovered.",
        result: { value: "−17", unit: "%", label: "drier than the 1950s" },
        headline:
          "South West WA's winter rain did not slowly tail off. It dropped suddenly around the year 2000 and never came back.",
        body:
          "Using 74 years of rainfall records from Bureau of Meteorology weather stations, I measured how much the cooler-months rain (April to October) in south-west WA has fallen, and what that means for the people who depend on it: water suppliers, farmers, and insurers. I was careful about the cause too, weighing natural climate cycles against human-caused climate change rather than overclaiming either way.",
        findings: [
          { value: "−2.9%", unit: "/decade", label: "Winter rain is falling", text: "The cooler-months rain has dropped about 3% every decade since 1950, roughly 20 mm less rain each decade. This is a real trend, not chance." },
          { value: "~2000", unit: "", label: "When it changed", text: "The fall was not gradual. Rainfall dropped suddenly around the year 2000 and then settled at a new, lower level (from about 567 mm a year to 483 mm, with the figures adjusted so years missing a wet station do not read spuriously dry)." },
          { value: "−17%", unit: "", label: "Drier than the 1950s", text: "The last 25 years have been about 17% drier than the 1950s, and early winter (May to July) has dried out even faster." },
          { value: "7 / 7", unit: "", label: "Every station agrees", text: "All seven weather stations show the same drying, so this is a genuine regional change, not a quirk of one location." },
        ],
        charts: [
          { src: "rainfall-decline/charts/01_timeseries_anomaly.png", caption: "Winter rainfall each year compared with the 1950s: mostly drier" },
          { src: "rainfall-decline/charts/02_stepchange.png", caption: "Rainfall dropped suddenly around 2000, then stayed low" },
          { src: "rainfall-decline/charts/03_trend_mannkendall.png", caption: "The long-term downward trend, with its margin of certainty" },
          { src: "rainfall-decline/charts/04_driver_correlation.png", caption: "How natural climate cycles relate to the rain: part of the story, not all of it" },
          { src: "rainfall-decline/charts/05_station_decade.png", caption: "Every weather station, decade by decade: drying across the board" },
        ],
        meaning:
          "This is not just a run of dry years, it is a permanent shift to a drier normal that began around 2000 and has not reversed. That changes the game for anyone who plans around water: Perth's drinking-water supply, wheatbelt farmers and the banks that lend to them, and insurers pricing risk in the south-west. They can no longer plan using the old, wetter climate. As for the cause, human-caused climate change is a big part of it, alongside natural ups and downs, and the analysis is careful not to overstate exactly how much is each.",
        resources: [
          { label: "Read the full analysis", href: ghBlob("rainfall-decline/README.md"), icon: "file-text" },
          { label: "Open the notebook", href: ghBlob("rainfall-decline/rainfall_analysis.ipynb"), icon: "bar-chart" },
          { label: "Cleaned datasets (6 CSVs)", href: ghTree("rainfall-decline/data"), icon: "layers" },
          { label: "All charts", href: ghTree("rainfall-decline/charts"), icon: "scan" },
          { label: "View on GitHub", href: ghTree("rainfall-decline"), icon: "github" },
        ],
        feature: 1,
        dataset: {
          caption: "Cool-season rainfall by station, 1950–74 baseline (BOM via GHCN-Daily)",
          columns: ["Station", "Setting", "Apr–Oct baseline (mm)"],
          rows: [
            ["Cape Leeuwin", "Far SW tip, coastal", "897"],
            ["Albany", "South coast", "762"],
            ["Deeside", "SW forest", "698"],
            ["Westbourne", "SW forest (Manjimup)", "567"],
            ["Narrogin", "Central wheatbelt", "409"],
            ["Northam", "Avon valley wheatbelt", "381"],
            ["Wagin", "Southern wheatbelt", "344"],
          ],
        },
        vizKey: "rainfall",
        rainMap: true,
        rainScrolly: true,
        viz: [
          { type: "line", key: "stepchange", title: "The step-change around 2000" },
          { type: "line", key: "anomaly", title: "Cool-season rainfall, year by year" },
          { type: "line", key: "trend", title: "The long-term trend, with its 95% band" },
          { type: "scatter", key: "drivers", sub: "IOD", title: "Rainfall vs the Indian Ocean Dipole" },
          { type: "scatter", key: "drivers", sub: "SAM", title: "Rainfall vs the Southern Annular Mode" },
          { type: "scatter", key: "drivers", sub: "ENSO", title: "Rainfall vs ENSO (Niño 3.4)" },
          { type: "heat", key: "station_decade", title: "Every station, decade by decade" },
        ],
        tags: ["BOM weather stations", "A sudden drop around 2000", "Cause handled carefully"],
        updates: [
          {
            date: "18 Jun 2026",
            title: "First published",
            found: "Seventy-four years of Bureau of Meteorology rainfall showed the south-west's winter rain did not fade slowly. It dropped suddenly around 2000 and settled at a new, lower level.",
            change: "Published the full pipeline: the step-change test, the long-term trend, the climate-driver checks and all seven stations, decade by decade.",
          },
          {
            date: "2 Jul 2026",
            title: "Fixing a quiet bias in the headline number",
            found: "The audit found the raw regional average had a composition problem: in years where a wet station was missing from the record, the region looked spuriously dry. That overstated the decline by about 2 percentage points.",
            change: "Switched the headline figures to composition-adjusted values (567 mm down to 483 mm across the break, 17% drier than the 1950s), added a pre-break flat-trend check, and stated the caveats plainly: the stations are not re-homogenised, and step tests can be fooled by autocorrelation.",
          },
          {
            date: "2 Jul 2026",
            title: "The question it left behind",
            found: "Drier is one thing, but Perth does not drink rain, it drinks streamflow. The obvious follow-up: what did this drying do to the rivers that fill the dams?",
            change: "Started the Perth water security project as a direct sequel. The answer turned out to be dramatic: the rivers fell three times harder than the rain. Read it below.",
          },
        ],
      },
      {
        id: "perth-water-security",
        title: "Perth Water Security: The Rivers After the Rain",
        year: "1967–2022",
        status: "Complete",
        category: ["Physical risk", "Climate data", "Data viz"],
        icon: "trending-down",
        meta: "4 charts · 12 river gauges · reproducible pipeline",
        summary:
          "The sequel to the rainfall story. The rain fell about 12%, but the rivers that feed Perth's dams lost 41%. This project measures that multiplier.",
        result: { value: "−41", unit: "%", label: "streamflow since 2000" },
        headline:
          "South-west WA lost about 12% of its winter rain. The rivers lost 41%. Dry catchments drink the rain before it can run off, and that multiplier is the whole story of Perth's water problem.",
        body:
          "This project picks up exactly where the rainfall story ends. Using 56 years of daily records from 12 Bureau of Meteorology reference river gauges in the hills around Perth, I asked what the drying actually did to the water that reaches rivers and dams. The answer is a textbook case of how climate risk compounds: the rivers stepped down in 2001, the same break year as the rain, but they fell more than three times harder. Parched soils and falling groundwater soak up the rain first, so every 1% of winter rainfall lost costs roughly 2.5 to 3.7% of streamflow. Water Corporation's own dam-inflow figures tell the same story from the supply side. This is why Perth now leans on desalination plants and groundwater replenishment instead of its dams.",
        findings: [
          { value: "2001", unit: "", label: "Same break, seen from the river", text: "The rivers stepped down at water year 2001 (a change-point test puts p at 0.007), matching the rainfall project's break at 2000. Same event, two datasets." },
          { value: "−41%", unit: "", label: "Three times harder than the rain", text: "Against the 1975–1999 baseline, flow since 2000 is down 41% and since 2010 down 48%, while rainfall on the same comparison is only down about 12%. That gap is the dry-catchment amplifier." },
          { value: "2.5–3.7", unit: "%", label: "The cost of 1% less rain", text: "Two independent estimates of rainfall-runoff elasticity agree: every 1% of winter rain lost costs roughly 2.5 to 3.7% of streamflow. The relationship explains two-thirds of the year-to-year variance." },
          { value: "p = 0.71", unit: "", label: "Not still sliding, settled", text: "Since 2000 there is no further significant trend. The rivers have not kept falling, they have settled at the new, far lower normal. That is what a step change means." },
        ],
        meaning:
          "For a water utility this is the textbook chronic physical risk: the supply the dams were designed around no longer exists. The dams did not fail, the climate they were built for went away, which is exactly why Perth now gets most of its water from desalination and groundwater replenishment. For anyone reporting under AASB S2, this project is also a lesson in how physical risk compounds: a modest change in the climate input (12% less rain) became a severe change in the thing that matters (41% less water). Reading the rainfall number alone would have understated the real exposure by a factor of three.",
        resources: [
          { label: "Read the full analysis", href: ghBlob("water-security/README.md"), icon: "file-text" },
          { label: "Cleaned datasets (7 CSVs)", href: ghTree("water-security/data"), icon: "layers" },
          { label: "All charts", href: ghTree("water-security/charts"), icon: "scan" },
          { label: "View on GitHub", href: ghTree("water-security"), icon: "github" },
        ],
        dataset: {
          caption: "The 12 reference river gauges behind the regional series (BoM Hydrologic Reference Stations)",
          columns: ["Gauge", "River and site", "Complete water years"],
          rows: [
            ["614006", "Murray River at Baden Powell", "1964–2022"],
            ["614044", "Yarragil Brook at Yarragil Formation", "1953–2022"],
            ["614196", "Williams River at Saddleback Rd Bridge", "1967–2022"],
            ["614224", "Hotham River at Marradong Rd Bridge", "1967–2022"],
            ["616002", "Darkin River at Pine Plantation", "1969–2022"],
            ["616006", "Brockman River at Tanamerah", "1981–2022"],
            ["616013", "Helena River at Ngangaguringuring", "1972–2016"],
            ["616019", "Brockman River at Yalliawirra", "1975–2022"],
            ["616041", "Wungong Brook at Vardi Rd", "1981–2022"],
            ["616178", "Jane Brook at National Park", "1963–2022"],
            ["616216", "Helena River at Poison Lease Gs", "1967–2022"],
            ["617003", "Gingin Brook at Bookine Bookine", "1973–2022"],
          ],
        },
        vizKey: "water",
        viz: [
          { type: "line", key: "stepchange", title: "The rivers stepped down around 2001" },
          { type: "bar", key: "amplification", title: "The amplifier: rain fell 12%, rivers fell 41%" },
          { type: "scatter", key: "elasticity", title: "Wet years, dry years: rain vs river, 1967–2022" },
          { type: "line", key: "anomaly", title: "Streamflow year by year, with the long trend" },
        ],
        tags: ["BoM reference river gauges", "Sequel to the rainfall story", "The dry-catchment amplifier"],
        updates: [
          {
            date: "2 Jul 2026",
            title: "First published",
            found: "The rainfall project ended on a question: Perth does not drink rain, it drinks streamflow, so what did the drying do to the rivers that fill the dams? Twelve BoM reference gauges and 56 years of daily flow had the answer.",
            change: "Published the full pipeline: the 2001 step-down, the rain-versus-river comparison, the elasticity estimate and the annual series, with Water Corporation's own dam-inflow figures kept as a cross-check.",
          },
          {
            date: "2 Jul 2026",
            title: "The multiplier that became the headline",
            found: "The rivers did not just fall, they fell more than three times harder than the rain: winter rainfall down about 12%, streamflow down 41% against the same baseline. That amplifier, not the rainfall figure, is the real exposure.",
            change: "Framed the whole story around the dry-catchment amplifier, added both elasticity estimates (2.5 to 3.7% of flow per 1% of rain), and stated plainly that reading the rainfall number alone understates the risk by a factor of three.",
          },
        ],
      },
      {
        id: "extreme-heat",
        title: "Extreme Heat in Perth and the Pilbara",
        year: "1945–2025",
        status: "Complete",
        category: ["Physical risk", "Climate data", "Data viz"],
        icon: "sun",
        meta: "4 charts · 2 stations · 2 independent archives, cross-checked",
        summary:
          "Eighty years of daily temperatures. Perth's hot days are climbing steadily, and Port Hedland, already one of Australia's hottest towns, is heating twice as fast.",
        result: { value: "2×", unit: "", label: "Pilbara heats twice as fast" },
        headline:
          "Perth now sees about 43 days a year at 35 °C or hotter, up from about 24 mid-century. Port Hedland is adding hot days twice as fast as Perth, and already spends more than five months of the year at 35 °C or above.",
        body:
          "Where the cyclone project covered storms and the rainfall project covered drying, this one measures the heat. I took 80 years of daily temperature records for Perth Airport and Port Hedland, the population centre and the industrial north, and counted the things that matter to people and businesses: days at or above 35 °C and 40 °C, the hottest day of each year, and multi-day heatwaves. Every Perth number was computed twice, from two independent archives of the same observations (the Bureau of Meteorology's portal and NOAA's global archive), and every trend agreed within a few percent, which is the built-in proof the pipeline reads the data faithfully. The one trend that did not clear the significance bar is reported that way, not rounded up to a finding.",
        findings: [
          { value: "+2.3", unit: "days/decade", label: "Perth keeps adding hot days", text: "Days at or above 35 °C are rising by about 2.3 per decade, from roughly 24 a year mid-century to 43 in the 2020s so far. The trend is about as statistically solid as climate data gets." },
          { value: "+4.8", unit: "days/decade", label: "Port Hedland heats twice as fast", text: "The Pilbara town has gone from about 133 days a year at 35 °C or above to about 163, more than five months of the year. For its iron-ore and LNG workforce that is an occupational heat-stress trend." },
          { value: "+2", unit: "°C", label: "The hottest day got hotter", text: "Perth's hottest day of the year has climbed from about 41.5 °C to about 43.5 °C over the record. The extremes are moving, not just the averages." },
          { value: "3 → 9", unit: "/yr", label: "Heatwaves tripled", text: "Perth's multi-day heatwave events went from about 3 a year mid-century to 8 to 9 now, and days spent inside heatwaves more than doubled at both stations." },
        ],
        meaning:
          "The two stations tell two different risk stories, which is exactly why both are here. For Perth, more hot days and triple the heatwaves mean health risk and air-conditioning demand, a chronic strain on people and the grid. For Port Hedland, the stakes are occupational: the town already spends five months a year at 35 °C or above, it is heating twice as fast as Perth, and it happens to load most of Australia's iron ore. There is also an honesty lesson in here: Port Hedland's count of 40 °C days is rising but does not clear the significance bar (p = 0.09), so this analysis says so instead of quietly promoting it to a finding.",
        resources: [
          { label: "Read the full analysis", href: ghBlob("extreme-heat/README.md"), icon: "file-text" },
          { label: "Cleaned datasets (5 CSVs)", href: ghTree("extreme-heat/data"), icon: "layers" },
          { label: "All charts", href: ghTree("extreme-heat/charts"), icon: "scan" },
          { label: "View on GitHub", href: ghTree("extreme-heat"), icon: "github" },
        ],
        dataset: {
          caption: "Hot days and heatwaves by decade (BoM observations via CDO and GHCN-Daily)",
          columns: ["Decade", "Perth: 35 °C+ days", "Perth: heatwave events", "Hedland: 35 °C+ days", "Hedland: heatwave days"],
          rows: [
            ["1950s", "24", "3.3", "130", "14"],
            ["1960s", "24", "3.0", "139", "17"],
            ["1970s", "30", "4.2", "130", "12"],
            ["1980s", "25", "3.9", "134", "16"],
            ["1990s", "29", "3.6", "145", "18"],
            ["2000s", "29", "4.8", "150", "26"],
            ["2010s", "36", "7.2", "158", "34"],
            ["2020s so far", "43", "8.7", "163", "37"],
          ],
        },
        vizKey: "heat",
        viz: [
          { type: "line", key: "perth_35", title: "Perth: days at 35 °C or above, 1945–2025" },
          { type: "line", key: "hedland_35", title: "Port Hedland: days at 35 °C or above" },
          { type: "bar", key: "decade_35", title: "Hot days per year, decade by decade", keys: [{ k: "perth", label: "Perth Airport", color: "var(--accent)" }, { k: "hedland", label: "Port Hedland", color: "#FF5C39" }] },
          { type: "line", key: "perth_txx", title: "Perth: the hottest day of each year" },
          { type: "line", key: "perth_hw", title: "Perth: days inside heatwaves each year" },
          { type: "line", key: "hedland_hw", title: "Port Hedland: days inside heatwaves each year" },
        ],
        tags: ["BoM + NOAA, cross-checked", "Two stations, two speeds", "Occupational heat stress"],
        updates: [
          {
            date: "2 Jul 2026",
            title: "First published",
            found: "Eighty years of daily temperatures for Perth Airport showed hot days climbing steadily: about 2.3 more days a year above 35 °C every decade. Every Perth number was computed twice, from two independent archives, and agreed within a few percent.",
            change: "Published the pipeline: the 35 °C and 40 °C day counts, the hottest day of each year and multi-day heatwaves, each figure cross-checked between the Bureau of Meteorology and NOAA archives.",
          },
          {
            date: "2 Jul 2026",
            title: "Adding the Pilbara",
            found: "Perth alone told only half the story. The industrial north, where the heat-stress stakes are highest, was missing, and it turned out to be heating twice as fast, already spending more than five months a year at 35 °C or above.",
            change: "Added Port Hedland as the second station, kept the two risk stories side by side, and reported the one trend that did not clear the significance bar (Hedland's 40 °C days, p = 0.09) as exactly that, rather than rounding it up to a finding.",
          },
        ],
      },
      {
        id: "fremantle-sea-level",
        title: "Sea-Level Rise at Fremantle",
        year: "1897–2022",
        status: "Complete",
        category: ["Physical risk", "Climate data", "Data viz"],
        icon: "trending-up",
        meta: "3 charts · 126-year tide gauge · reproducible pipeline",
        summary:
          "One of the Southern Hemisphere's longest sea-level records, asked the two questions coastal owners care about: how fast is the sea rising here, and is the rise speeding up?",
        result: { value: "+22", unit: "cm", label: "risen since 1897" },
        headline:
          "Fremantle's sea has risen about 22 cm since 1897. The recent pace, 5.1 mm a year since 1993, is roughly three and a half times the century-long average, yet this one gauge still cannot prove the rise is smoothly accelerating.",
        body:
          "The Fremantle tide gauge has been reading sea level since 1897, which makes it one of the best places in Australia to measure long-run coastal risk. Using the research-grade PSMSL monthly record, I measured the long-run rate of rise, compared the satellite-altimetry era (1993 onward) with everything before it, and tested for acceleration. The honest finding has two halves: the long-run rise is unequivocal and the recent decades are far faster than the century average, but the record's strong El Niño and La Niña swings, plus a real mid-century pause, mean a single gauge cannot yet prove clean, smooth acceleration. It also measures relative sea level, so whatever the land itself is doing is baked into the number.",
        findings: [
          { value: "+1.78", unit: "mm/yr", label: "The long-run rise is rock solid", text: "Over the full 1897 to 2022 record the sea rose 1.78 mm a year (p around 1e-24), about 22 cm in total. Sen's slope agrees at 1.69 mm/yr. This part is not in doubt." },
          { value: "5.1", unit: "mm/yr", label: "The recent era is much faster", text: "Since 1993, the satellite-altimetry era, the rate is 5.11 mm/yr, roughly 3.5 times the 1.44 mm/yr measured before 1993. The fastest 30-year window in the record is 1985 to 2014 at 5.62 mm/yr." },
          { value: "p = 0.11", unit: "", label: "But acceleration is not proven", text: "A centred quadratic fit puts the acceleration at 0.013 mm per year squared, short of the significance bar. A slow-then-fast history is there, but this single gauge cannot pin it to a clean curve." },
          { value: "−0.84", unit: "mm/yr", label: "The record is not a straight line", text: "The 30-year rate swings from a mid-century pause (1962 to 1991 reads slightly negative) to the fast recent decades. That is exactly why no single window should be quoted as 'the' trend." },
        ],
        meaning:
          "For anyone with coastal assets, ports, jetties, low-lying land or infrastructure, this is textbook chronic physical risk: the water is rising, it has already risen 22 cm, and the recent pace is several times the long-run average. But the project is also a lesson in honest uncertainty. The headline a risk reporter should carry is the unequivocal long-run rise and the far faster recent era, not a precise acceleration figure this record cannot yet support. And because a tide gauge measures relative sea level, land motion at the site is in the number and is not corrected for here, which any AASB S2 disclosure built on it has to say out loud.",
        resources: [
          { label: "Read the full analysis", href: ghBlob("sea-level/README.md"), icon: "file-text" },
          { label: "Cleaned datasets (6 CSVs)", href: ghTree("sea-level/data"), icon: "layers" },
          { label: "All charts", href: ghTree("sea-level/charts"), icon: "scan" },
          { label: "View on GitHub", href: ghTree("sea-level"), icon: "github" },
        ],
        dataset: {
          caption: "Rate of rise by era at Fremantle (PSMSL monthly RLR, station 111)",
          columns: ["Series", "Years", "Complete years", "OLS rate (mm/yr)", "Sen's slope (mm/yr)"],
          rows: [
            ["Full record", "1897–2022", "113", "+1.78", "+1.69"],
            ["Pre-1993", "1897–1992", "83", "+1.44", "+1.41"],
            ["Altimetry era", "1993–2022", "30", "+5.11", "+5.16"],
          ],
        },
        vizKey: "sealevel",
        viz: [
          { type: "line", key: "msl_series", title: "Sea level at Fremantle, 1897 to 2022" },
          { type: "line", key: "rolling_rate", title: "The 30-year rate, window by window" },
          { type: "bar", key: "eras", title: "Rate of rise: full record vs the recent era" },
        ],
        tags: ["PSMSL research-grade tide gauge", "Fast recent era, unproven acceleration", "Relative sea level, land motion included"],
        updates: [
          {
            date: "5 Jul 2026",
            title: "First published",
            found: "The Fremantle tide gauge, running since 1897, is one of the longest sea-level records in the Southern Hemisphere. It shows the sea has risen about 22 cm, and far faster since 1993 than over the century as a whole.",
            change: "Published the pipeline from the PSMSL research-grade record: the full series with its trend, the 30-year rolling rate, and the era comparison, complete years only and nothing interpolated.",
          },
          {
            date: "5 Jul 2026",
            title: "Choosing honesty over a bigger headline",
            found: "The recent rate, 5.1 mm a year, is dramatic and tempting to headline as acceleration. But the quadratic acceleration term is not statistically significant (p = 0.11): a real mid-century pause and strong El Niño and La Niña swings leave the curve unproven on this single gauge.",
            change: "Reported the unequivocal long-run rise and the far faster recent era as the finding, kept acceleration flagged as not yet proven, and stated openly that this is relative sea level with land motion not corrected for.",
          },
        ],
      },
      {
        id: "bushfire-weather",
        title: "Fire Danger Trends in South West WA",
        year: "1941–2026",
        status: "Complete",
        category: ["Physical risk", "Climate data", "Data viz"],
        icon: "sun",
        meta: "5 charts · 4 sites · FFDI built from scratch, validated vs station data",
        summary:
          "Eighty-five years of daily fire weather at four WA sites, built from ERA5 reanalysis. The trend is not one line: rising in the wheatbelt, spiking around Perth in the 2020s, and falling in the southern forests.",
        result: { value: "42", unit: "days", label: "Perth's Very High days, 2020s vs 25 in the 2000s" },
        headline:
          "I computed the McArthur Forest Fire Danger Index (FFDI) from scratch, daily since 1941, for Perth, Merredin, Manjimup and Margaret River. The honest headline is that south-west WA has no single fire-weather trend: it depends where you stand.",
        body:
          "Fire is the acute physical risk this portfolio had not yet covered, and in WA it is the one insurers and shires price first. There is no long daily record of humidity and wind at these towns, so I used ERA5 reanalysis (a physics model pinned to observations, pulled hourly from the keyless Open-Meteo archive) and built the full index chain by hand: the Keetch-Byram drought index, the Noble et al. drought factor, and the Mark 5 FFDI, each transcribed from the original papers and unit-tested against their published calibration points. Then I checked the whole thing against the real Perth Airport station record: ERA5's daily maximum temperature matches the observations at r = 0.96, and the known disaster days (Wooroloo 2021, Waroona 2016) land in the top 0.1% of all days, which is the proof the pipeline reads the weather faithfully.",
        findings: [
          {
            value: "+3.0",
            unit: "days/decade",
            label: "The wheatbelt is getting more dangerous",
            text: "Merredin's Very High fire-danger days (FFDI ≥ 25) are rising about 3 per decade since 1975 (p = 0.03), reaching 81 a season in the 2020s, the highest of any decade on record.",
          },
          {
            value: "42 vs 25",
            unit: "days",
            label: "Perth's 2020s spike",
            text: "Perth shows no significant long-run trend, but the 2020s so far average 42 Very High days a season against 25 in the 2000s, the worst decade since the unreliable 1940s.",
          },
          {
            value: "−0.8",
            unit: "days/decade",
            label: "The forests are going the other way",
            text: "Manjimup, in the southern forests, is falling about 0.8 Very High days per decade since 1975 (p = 0.03), from roughly 10 a season mid-century to 4 to 6 now. An unexpected result, reported as it stands.",
          },
          {
            value: "r = 0.96",
            unit: "",
            label: "The reanalysis checks out",
            text: "ERA5 grid-cell maximum temperature tracks the observed Perth Airport record at r = 0.96 with a small −0.5 °C bias, so the fire-weather trends rest on data that agrees with the real station.",
          },
        ],
        meaning:
          "For an AASB S2 reporter with WA exposure, the lesson is that a single regional fire-risk assumption cannot be justified: the wheatbelt trend and the Perth 2020s spike argue for more weight north and east of the scarp, while the forest-belt decline shows the region is not one story. Two honesty notes ride along: absolute FFDI here runs low because ERA5 winds are grid-cell averages, so the trends and relative changes are the result, not the raw counts; and the pre-1975 reanalysis looks too fiery against the known wet mid-century, so those decades are shaded on the charts and kept out of the headline.",
        resources: [
          { label: "Read the full analysis", href: "https://github.com/lumbalumbaputih/adhi-climate/blob/main/bushfire-weather/README.md", icon: "file-text" },
          { label: "Cleaned datasets", href: "https://github.com/lumbalumbaputih/adhi-climate/tree/main/bushfire-weather/data", icon: "layers" },
          { label: "All charts", href: "https://github.com/lumbalumbaputih/adhi-climate/tree/main/bushfire-weather/charts", icon: "scan" },
          { label: "View on GitHub", href: "https://github.com/lumbalumbaputih/adhi-climate/tree/main/bushfire-weather", icon: "github" },
        ],
        dataset: {
          caption: "Very High fire-danger days per season (FFDI ≥ 25), by decade and site (ERA5 reanalysis)",
          columns: ["Decade", "Perth", "Merredin", "Manjimup"],
          rows: [
            ["1960s", "29", "64", "8"],
            ["1970s", "36", "66", "8"],
            ["1980s", "30", "64", "8"],
            ["1990s", "30", "70", "4"],
            ["2000s", "25", "70", "3"],
            ["2010s", "29", "68", "4"],
            ["2020s", "42", "81", "6"],
          ],
        },
        vizKey: "bushfire",
        viz: [
          { type: "line", key: "perth_vh", title: "Perth: Very High fire-danger days per season (FFDI ≥ 25)" },
          { type: "line", key: "merredin_vh", title: "Merredin (wheatbelt): Very High days per season" },
          {
            type: "bar", key: "decades_vh", title: "Very High days per season, decade by decade",
            keys: [
              { k: "perth", label: "Perth", color: "var(--accent)" },
              { k: "merredin", label: "Merredin", color: "#FFC234" },
              { k: "manjimup", label: "Manjimup", color: "#1F9D55" },
            ],
          },
        ],
        tags: ["ERA5, self-downloaded", "FFDI from scratch", "Three sites, three trends"],
        updates: [
          {
            date: "7 Jul 2026",
            title: "First published",
            found: "Eighty-five years of daily fire weather at four WA sites, built from ERA5 reanalysis downloaded by the pipeline itself, showed no single regional trend: rising in the wheatbelt, spiking at Perth in the 2020s, falling in the southern forests. The index chain reproduces its published calibration points and ERA5 matches the Perth Airport station at r = 0.96.",
            change: "Published the FFDI pipeline for Perth, Merredin, Manjimup and Margaret River, with the suspect pre-satellite decades shaded and excluded from the headline, and the reanalysis validated against the real station record.",
          },
        ],
      },
      {
        id: "marine-heatwaves",
        title: "Marine Heatwaves off the WA Coast",
        year: "1982–2026",
        status: "Complete",
        category: ["Physical risk", "Climate data", "Data viz"],
        icon: "globe",
        meta: "4 charts · 44 years of daily SST · Hobday detection from scratch",
        summary:
          "Forty-four years of daily sea temperature off Ningaloo. The pipeline finds 103 marine heatwaves, correctly flags the 2011 Ningaloo Niño as the longest on record, and shows the ocean measurably warming.",
        result: { value: "123", unit: "days", label: "the 2011 Ningaloo Niño, longest on record" },
        headline:
          "Marine heatwaves are the ocean's version of a heatwave, and off WA they wreck fisheries and seagrass. I built the standard Hobday detection from scratch on 44 years of daily satellite SST, and the 2011 Ningaloo Niño falls out of it exactly where the science says it should.",
        body:
          "The study box sits over the Ningaloo coast, the epicentre of the 2011 event that devastated the Shark Bay scallop and Abrolhos fisheries. The data is NOAA's OISST v2.1 daily sea-surface temperature. Getting it clean was its own small battle: the fast ERDDAP feed had genuine gaps across 2015 and 2016, so the pipeline patches those days from NOAA's authoritative daily archive onto the identical grid, giving an unbroken record with no seam. On top of it sits the Hobday et al. definition, coded by hand: a day-of-year climatology and 90th-percentile threshold over the 1982–2011 baseline, then events of five or more consecutive days above it. The 2011 event is the built-in check: if it did not appear as a major multi-month event, the inputs would be wrong.",
        findings: [
          {
            value: "123",
            unit: "days",
            label: "The 2011 Ningaloo Niño",
            text: "Detected running 26 Sep 2010 to 26 Jan 2011, the longest single event in the record, peaking 3.7 °C above the climatological mean. It lands exactly where the literature puts it, validating the pipeline.",
          },
          {
            value: "103",
            unit: "events",
            label: "Marine heatwaves since 1982",
            text: "The Hobday detection finds 103 distinct events over 44 years off Ningaloo, with the most intense peak, 3.8 °C above climatology, occurring as recently as January 2025.",
          },
          {
            value: "+0.12",
            unit: "°C/decade",
            label: "The ocean is warming",
            text: "Annual mean SST is rising about 0.12 °C per decade (p = 0.04), a significant warming trend that is the clean statement behind the noisier count of heatwave days.",
          },
          {
            value: "71 vs 11",
            unit: "days",
            label: "Heatwave days are climbing",
            text: "Marine-heatwave days averaged 71 a year in the 2020s against just 11 in the 2000s. Some of that is warming showing through a fixed baseline, which the write-up states plainly.",
          },
        ],
        meaning:
          "For the fishing, aquaculture and tourism operators along this coast, marine heatwaves are the acute ocean risk, and both their frequency and their peak intensity are trending up on a significantly warming baseline. The honest caveat is built into the method: heatwave-day counts are measured against a fixed 1982–2011 climatology, so in a warming ocean part of the rising count is simply that warming, which is why the significant mean-SST trend is reported as the cleaner underlying signal.",
        resources: [
          { label: "Read the full analysis", href: "https://github.com/lumbalumbaputih/adhi-climate/blob/main/marine-heatwaves/README.md", icon: "file-text" },
          { label: "Cleaned datasets", href: "https://github.com/lumbalumbaputih/adhi-climate/tree/main/marine-heatwaves/data", icon: "layers" },
          { label: "All charts", href: "https://github.com/lumbalumbaputih/adhi-climate/tree/main/marine-heatwaves/charts", icon: "scan" },
          { label: "View on GitHub", href: "https://github.com/lumbalumbaputih/adhi-climate/tree/main/marine-heatwaves", icon: "github" },
        ],
        dataset: {
          caption: "Marine-heatwave days and mean sea-surface temperature by decade (NOAA OISST v2.1, Ningaloo box)",
          columns: ["Decade", "MHW days/yr", "Mean SST (°C)"],
          rows: [
            ["1980s", "39", "25.3"],
            ["1990s", "24", "25.1"],
            ["2000s", "11", "25.1"],
            ["2010s", "44", "25.4"],
            ["2020s", "71", "25.7"],
          ],
        },
        vizKey: "mhw",
        viz: [
          { type: "line", key: "mhw_days", title: "Marine-heatwave days per year off Ningaloo" },
          { type: "line", key: "mean_sst", title: "Annual mean sea-surface temperature" },
          { type: "bar", key: "top_events", title: "The eight longest marine heatwaves on record (duration, days)" },
        ],
        tags: ["NOAA OISST, gap-filled", "Hobday from scratch", "2011 event validated"],
        updates: [
          {
            date: "7 Jul 2026",
            title: "First published",
            found: "Forty-four years of daily SST off Ningaloo yielded 103 marine-heatwave events under the Hobday definition, with the 2011 Ningaloo Niño coming out as the longest on record (123 days, peak 3.7 °C) and annual mean SST warming significantly. The CoastWatch feed was missing scattered days in 2015 and 2016.",
            change: "Filled the missing days from NOAA's daily OISST archive onto the identical grid for an unbroken record, then published the detection with the 2011 event as the built-in validation case and the fixed-baseline caveat stated openly.",
          },
        ],
      },
      {
        id: "wheat-yields",
        title: "WA Wheat Yields and the Drying Trend",
        year: "1861–2022",
        status: "Complete",
        category: ["Physical risk", "Climate data", "Data viz"],
        icon: "sprout",
        meta: "4 charts · 150 seasons · yield trend detrended against rainfall",
        summary:
          "A century and a half of WA wheat. Yields have quadrupled on farming technology, and once you remove that trend the link to the rainfall decline is real but surprisingly weak, which is the finding.",
        result: { value: "+0.17", unit: "t/ha/decade", label: "the technology yield trend" },
        headline:
          "WA wheat yields have climbed from well under one tonne a hectare to about two, driven by farming technology, not weather. The interesting question is what the south-west's rainfall decline did on top of that, and the honest answer is: less than you would guess.",
        body:
          "This project pairs the state's wheat record with the growing-season rainfall from the rainfall-decline project. The wheat data is the full ABS historical series, 1861 to 2022, 150 seasons. The trap here is that yields rise steeply on technology (better varieties, fertiliser, machinery, agronomy), so a naive correlation with rainfall is dominated by that shared upward-and-downward drift and badly overstates the climate link. The pipeline detrends first: it fits and removes the technology trend, then asks whether the leftover year-to-year yield wobble tracks the rainfall wobble. That is the statistically honest way to isolate the weather signal from the progress signal.",
        findings: [
          {
            value: "+0.17",
            unit: "t/ha/decade",
            label: "Technology, not weather, drove the yield",
            text: "The long-run yield trend is about 0.17 tonnes per hectare per decade and overwhelmingly significant (p ≈ 3 × 10⁻¹⁶). Mean yield roughly doubled from the 1970s to the 2020s.",
          },
          {
            value: "weak",
            unit: "",
            label: "The rainfall link is real but modest",
            text: "Once yields and rainfall are both detrended, the correlation between them is weak and not statistically significant. The drying matters, but it is not the dominant driver of year-to-year yield.",
          },
          {
            value: "150",
            unit: "seasons",
            label: "One of the longest records here",
            text: "The ABS series runs from 1861, giving 150 seasons of area and production, one of the longest continuous records in the whole portfolio.",
          },
          {
            value: "2.05",
            unit: "t/ha",
            label: "The 2020s are the most productive decade",
            text: "Despite the drying, the 2020s so far average about 2.05 t/ha, the highest of any decade, because technology gains have outrun the rainfall headwind, so far.",
          },
        ],
        meaning:
          "For a grower, an agribusiness lender or an AASB S2 financial-materiality assessment, the message is nuanced: the drying south-west is a genuine chronic risk, but across the whole state and the whole record it has so far been masked by faster technology gains, not translated one-for-one into lost yield. That is a more defensible, and more useful, statement than a scary raw correlation, and it is exactly the kind of signal-versus-progress separation that honest climate-risk work turns on.",
        resources: [
          { label: "Read the full analysis", href: "https://github.com/lumbalumbaputih/adhi-climate/blob/main/wheat-yields/README.md", icon: "file-text" },
          { label: "Cleaned datasets", href: "https://github.com/lumbalumbaputih/adhi-climate/tree/main/wheat-yields/data", icon: "layers" },
          { label: "All charts", href: "https://github.com/lumbalumbaputih/adhi-climate/tree/main/wheat-yields/charts", icon: "scan" },
          { label: "View on GitHub", href: "https://github.com/lumbalumbaputih/adhi-climate/tree/main/wheat-yields", icon: "github" },
        ],
        dataset: {
          caption: "WA wheat mean yield by decade (ABS historical agriculture series, 7124.0)",
          columns: ["Decade", "Mean yield (t/ha)"],
          rows: [
            ["1970s", "1.07"],
            ["1980s", "1.11"],
            ["1990s", "1.63"],
            ["2000s", "1.63"],
            ["2010s", "1.80"],
            ["2020s", "2.05"],
          ],
        },
        vizKey: "wheat",
        viz: [
          { type: "line", key: "yield", title: "WA wheat yield, 1861–2022 (with technology trend)" },
          { type: "line", key: "area", title: "Area sown to wheat (million hectares)" },
          { type: "bar", key: "decade_yield", title: "Mean yield by decade (t/ha)" },
        ],
        tags: ["ABS 1861–2022", "Detrended, not naive", "Signal vs progress"],
        updates: [
          {
            date: "7 Jul 2026",
            title: "First published",
            found: "A century and a half of WA wheat showed yields quadrupling on farming technology (about +0.17 t/ha per decade), and once that trend is removed the link between year-to-year yield and growing-season rainfall is real but weak and not significant.",
            change: "Published the paired analysis, detrending yields before testing the rainfall link so the technology signal is not mistaken for a climate one, using the full ABS series downloaded by the pipeline.",
          },
        ],
      },
      {
        id: "swis-decarbonisation",
        title: "How Fast Is WA's Main Grid Decarbonising?",
        year: "2006–2023",
        status: "Complete",
        category: ["Transition analytics", "Climate data", "Data viz"],
        icon: "leaf",
        meta: "4 charts · 206 monthly files · 94 facilities mapped to fuels",
        summary:
          "Seventeen years of WA's main grid from AEMO metering. The renewable share more than quadrupled to 23%, emissions intensity fell from 0.71 to 0.58 t/MWh, and coal has barely started to move.",
        result: { value: "23%", unit: "", label: "renewable share, 2022, from under 5%" },
        headline:
          "Where the rest of this portfolio measures climate risk arriving, this one measures the energy transition actually happening: the South West Interconnected System's generation mix, facility by facility, from AEMO's own metering.",
        body:
          "The SWIS is the grid that powers Perth and the south-west, and its decarbonisation pace drives every WA company's scope 2 trajectory. I pulled all 206 monthly AEMO facility-metering files from 2006 to 2023, then mapped each of the 94 generators to a fuel using the OpenNEM registry, every assignment recorded, none guessed. From there the pipeline builds the annual fuel mix, tests the trends with the same statistics as the rest of the suite, and, using per-fuel emission factors taken from the regulator's own published facility data, computes an emissions-intensity index for the grid.",
        findings: [
          {
            value: "4.8 → 22.9%",
            unit: "",
            label: "Renewables more than quadrupled",
            text: "The renewable share of utility generation rose from 4.8% in 2007 to 22.9% in 2022, about +9 percentage points per decade (p = 1 × 10⁻⁵). Wind did almost all of the work.",
          },
          {
            value: "0.71 → 0.58",
            unit: "t/MWh",
            label: "The grid got cleaner per unit",
            text: "Emissions intensity fell from 0.71 to 0.58 tonnes CO₂-e per MWh, a significant decline (p = 5 × 10⁻⁴), driven by wind and solar displacing gas.",
          },
          {
            value: "−9",
            unit: "pp/decade",
            label: "Gas is being displaced",
            text: "Gas fell from 52% to 41% of the mix, the mirror image of the renewables rise. It, not coal, is what new renewables have pushed aside so far.",
          },
          {
            value: "43 → 36%",
            unit: "",
            label: "Coal has barely started",
            text: "Coal drifted from 43% to 36% but the change is not statistically significant. The big Collie and Muja retirements are scheduled for 2023 to 2029, past the window of complete data, so the steep decline is still ahead.",
          },
        ],
        meaning:
          "For a WA business setting a scope 2 emissions target, the grid is genuinely getting cleaner but is nowhere near clean: still four-tenths gas and a third coal in the latest complete year. The honest scope note matters here: this measures only registered, utility-scale generation, so WA's world-leading rooftop solar, which sits behind the meter, does not appear as supply, which means the renewable share shown is a floor, not the whole picture. The intensity series is an index on documented fuel factors, not a full greenhouse inventory.",
        resources: [
          { label: "Read the full analysis", href: "https://github.com/lumbalumbaputih/adhi-climate/blob/main/swis-decarbonisation/README.md", icon: "file-text" },
          { label: "Cleaned datasets", href: "https://github.com/lumbalumbaputih/adhi-climate/tree/main/swis-decarbonisation/data", icon: "layers" },
          { label: "All charts", href: "https://github.com/lumbalumbaputih/adhi-climate/tree/main/swis-decarbonisation/charts", icon: "scan" },
          { label: "View on GitHub", href: "https://github.com/lumbalumbaputih/adhi-climate/tree/main/swis-decarbonisation", icon: "github" },
        ],
        dataset: {
          caption: "SWIS generation mix and emissions intensity, four-yearly (AEMO WEM metering; CER emission factors)",
          columns: ["Year", "Coal %", "Gas %", "Renewables %", "Intensity (t/MWh)"],
          rows: [
            ["2007", "43.2", "52.0", "4.8", "0.71"],
            ["2012", "47.5", "44.6", "7.9", "0.70"],
            ["2017", "49.2", "41.6", "9.2", "0.70"],
            ["2022", "36.2", "40.9", "22.9", "0.58"],
          ],
        },
        vizKey: "swis",
        viz: [
          { type: "line", key: "renewables", title: "Renewable share of SWIS utility generation" },
          { type: "line", key: "intensity", title: "Grid emissions intensity (t CO₂-e/MWh)" },
          {
            type: "bar", key: "mix", title: "Coal, gas and renewables share by year",
            keys: [
              { k: "coal", label: "Coal", color: "#6B6259" },
              { k: "gas", label: "Gas", color: "#FFC234" },
              { k: "renewables", label: "Renewables", color: "#1F9D55" },
            ],
          },
        ],
        tags: ["AEMO metering, self-downloaded", "94 facilities mapped", "Rooftop solar is invisible"],
        updates: [
          {
            date: "7 Jul 2026",
            title: "First published",
            found: "Seventeen years of AEMO metering showed the SWIS renewable share more than quadrupling to 23% (wind the main driver) while gas fell and coal barely moved, and a first-cut analysis left emissions intensity uncomputed rather than invent emission factors.",
            change: "Published the fuel-mix pipeline built from all 206 monthly files, with facilities mapped to fuels from the OpenNEM registry, then added the intensity series using per-fuel factors from the regulator's own published SWIS facility data.",
          },
        ],
      },
      {
        id: "transition-risk",
        title: "WA's Biggest Emitters Under the Safeguard Mechanism",
        year: "2016–2025",
        status: "Complete",
        category: ["Transition risk", "Climate data", "Data viz"],
        icon: "bar-chart",
        meta: "5 charts · 9 compliance years · scenarios, not forecasts",
        summary:
          "The Clean Energy Regulator's facility data, filtered to WA. It shows a concentrated, LNG-heavy emissions base where most big facilities are already above their declining baselines, and buying units to comply.",
        result: { value: "56", unit: "of 81", label: "WA facilities above baseline in 2024-25" },
        headline:
          "The Safeguard Mechanism is Australia's sharpest transition-policy lever: every large facility's emissions baseline now declines each year, and exceeding it costs real money in carbon units. Turned on WA's data, it shows the squeeze has already started.",
        body:
          "This is the transition-risk half of AASB S2, and it reuses the same regulator data every company is measured against. I downloaded all nine published compliance years (2016-17 to 2024-25) from the Clean Energy Regulator, normalised their shifting column formats, and filtered to WA. One trap needed care: some early years report a multi-year cumulative baseline that dwarfs annual emissions, so the parser flags those from the files' own markers and excludes them from the headroom maths rather than mixing them in. Everything downstream, the concentration picture, the emissions-vs-baseline gap, the crossover scenarios and the cost sensitivity, follows the project's own rule: exceeding a baseline and surrendering units is compliance, framed as cost exposure, never wrongdoing.",
        findings: [
          {
            value: "56 of 81",
            unit: "",
            label: "Most big facilities are already over",
            text: "In 2024-25, 56 of 81 WA facilities reported covered emissions above their baseline, including four of the six biggest (Gorgon, North West Shelf, Worsley, Pluto). They comply by surrendering carbon units.",
          },
          {
            value: "66%",
            unit: "",
            label: "The emissions base is concentrated",
            text: "The top ten facilities hold 66% of WA's 47 Mt of covered emissions. LNG and oil-and-gas alone are over half; Chevron's two facilities cover 13 Mt, Woodside's five another 8 Mt.",
          },
          {
            value: "~$0.9bn",
            unit: "",
            label: "The illustrative cost of standing still",
            text: "If the six biggest facilities held emissions flat while baselines decline at the default 4.9% a year, the 2025–2029 unit bill at spot ACCU prices is about $0.9 bn, roughly $2.2 bn at the legislated ceiling. Illustrative, with every assumption stated.",
          },
          {
            value: "+0.6",
            unit: "Mt/yr",
            label: "Mining emissions are still rising",
            text: "Nothing in the WA panel is significantly declining. Metal ore mining is rising about 0.6 Mt a year (p = 0.001) and transport is up too; the total drifts upward against baselines heading down.",
          },
        ],
        meaning:
          "For WA reporters the Safeguard is no longer a future risk but a present cost: most large facilities are in structural shortfall against baselines that keep falling, so the disclosure question shifts from when this binds to what the unit bill does to operating cost and what abatement changes the path. The scenarios here are deliberately what-ifs, never forecasts, every projection carries its assumption in the same breath and every dollar figure is a range, because the companies, not this analysis, know their real production and abatement plans.",
        resources: [
          { label: "Read the full analysis", href: "https://github.com/lumbalumbaputih/adhi-climate/blob/main/transition-risk/README.md", icon: "file-text" },
          { label: "Cleaned datasets", href: "https://github.com/lumbalumbaputih/adhi-climate/tree/main/transition-risk/data", icon: "layers" },
          { label: "All charts", href: "https://github.com/lumbalumbaputih/adhi-climate/tree/main/transition-risk/charts", icon: "scan" },
          { label: "View on GitHub", href: "https://github.com/lumbalumbaputih/adhi-climate/tree/main/transition-risk", icon: "github" },
        ],
        dataset: {
          caption: "WA's six biggest Safeguard facilities, 2024-25 (Clean Energy Regulator)",
          columns: ["Facility", "Covered (Mt)", "Baseline (Mt)", "Headroom (Mt)"],
          rows: [
            ["Gorgon", "9.02", "8.54", "−0.48"],
            ["North West Shelf", "5.75", "4.83", "−0.92"],
            ["Wheatstone", "4.02", "4.03", "+0.00"],
            ["Worsley", "3.22", "3.09", "−0.13"],
            ["Prelude FLNG", "2.25", "3.68", "+1.42"],
            ["Pluto", "1.89", "1.74", "−0.14"],
          ],
        },
        vizKey: "transition",
        viz: [
          { type: "bar", key: "top_facilities", title: "WA's ten biggest Safeguard facilities (covered emissions, Mt, 2024-25)" },
          { type: "line", key: "wa_total", title: "WA total covered emissions, 2016–2024 (Mt)" },
          {
            type: "bar", key: "sectors", title: "Covered emissions by sector, by year (Mt)",
            keys: [
              { k: "lng", label: "LNG / oil & gas", color: "var(--accent)" },
              { k: "mining", label: "Metal ore mining", color: "#FFC234" },
              { k: "alumina", label: "Alumina & metals", color: "#2E3192" },
            ],
          },
        ],
        tags: ["CER data, all 9 years", "Scenarios, not forecasts", "Compliance = cost, not blame"],
        updates: [
          {
            date: "7 Jul 2026",
            title: "First published",
            found: "All nine Safeguard compliance years for WA showed a concentrated, LNG-heavy emissions base where 56 of 81 facilities were already above their declining baselines in 2024-25, complying by surrendering units, while total emissions still drift upward. Some early years hide a multi-year cumulative baseline that would distort the headroom maths.",
            change: "Published the WA exposure analysis, flagging and excluding the cumulative baselines from the files' own markers, and reporting crossovers and costs strictly as assumption-labelled scenarios, with exceedance framed as cost exposure rather than wrongdoing.",
          },
        ],
      },
      {
        id: "aasb-s2-readiness",
        title: "AASB S2 Readiness: WA's Biggest Emitters",
        year: "2025",
        status: "Complete",
        category: ["Disclosure & AASB S2", "Policy"],
        icon: "file-text",
        meta: "3 scorecards · 93 evidence-backed cells · scoring matrix",
        summary:
          "Grading three of WA's biggest companies on how clearly and completely they report their climate risks under Australia's new disclosure rules.",
        result: { value: "3", unit: "firms", label: "graded, 93 checks" },
        headline:
          "Reporting climate risk well is not the same as having low climate risk. The only way to tell them apart is to read the actual reports, line by line.",
        body:
          "Australia has brought in new rules (called AASB S2) that make big companies report their climate risks in a consistent way. I read the actual reports of three of WA's largest listed companies, BHP, Rio Tinto, and Woodside, and graded each one against what the rules ask for, across four areas: how the board oversees climate, company strategy, how risks are managed, and the numbers and targets they publish. Every score is backed by a specific page in the company's own report. This is exactly the kind of work ESG and sustainability consultants are hired to do.",
        findings: [
          { value: "3", unit: "firms", label: "BHP · Rio Tinto · Woodside", text: "Three companies, graded on 31 specific requirements, with 93 pieces of evidence pulled straight from their reports." },
          { value: "3.69", unit: "/4", label: "Rio Tinto scored highest", text: "It was the only one to back its climate claims with hard numbers. Woodside scored 3.35 and BHP 2.94 out of 4." },
          { value: "575.7", unit: "Mt", label: "The emissions almost no one targets", text: "Most of these firms' emissions come from customers using their products (Rio Tinto's are 575.7 Mt, versus about 31.5 from its own operations), yet that is where their targets are weakest." },
          { value: "4", unit: "areas", label: "The same gaps everywhere", text: "Across all three, the biggest gaps were the same: which assets are actually at risk, and putting a dollar figure on the financial impact." },
        ],
        matrix: true,
        radar: {
          axes: ["Governance", "Strategy", "Risk", "Metrics"],
          max: 4,
          series: [
            { name: "Rio Tinto", color: "#2563EB", values: [3.7, 3.7, 3.5, 3.9], overall: "3.69", band: "Advanced" },
            { name: "Woodside", color: "#10B981", values: [3.8, 3.2, 3.3, 3.1], overall: "3.35", band: "Advanced" },
            { name: "BHP", color: "#FF5C39", values: [3.0, 3.0, 3.0, 2.8], overall: "2.94", band: "Developing" },
          ],
        },
        meaning:
          "The big takeaway: clear reporting and low risk are not the same thing. Woodside is the perfect example. Its reporting is strong, yet its growth plans carry exactly the kind of climate risk these rules are meant to bring into the open. Being able to hold those two ideas apart, how well a company reports versus how exposed it actually is, is the core skill this project shows. The new rules raise the bar, but the real depth comes from companies choosing to do the harder work of putting numbers on it.",
        resources: [
          { label: "Read the full review", href: ghBlob("aasb-s2-review/README.md"), icon: "file-text" },
          { label: "Scoring matrix (93 cells)", href: ghBlob("aasb-s2-review/scoring-matrix.csv"), icon: "layers" },
          { label: "Cross-company gap summary", href: ghBlob("aasb-s2-review/gap-summary.csv"), icon: "bar-chart" },
          { label: "Rio Tinto scorecard", href: ghBlob("aasb-s2-review/rio-tinto-scorecard.md"), icon: "file-text" },
          { label: "Woodside scorecard", href: ghBlob("aasb-s2-review/woodside-scorecard.md"), icon: "file-text" },
          { label: "BHP scorecard", href: ghBlob("aasb-s2-review/bhp-scorecard.md"), icon: "file-text" },
          { label: "View on GitHub", href: ghTree("aasb-s2-review"), icon: "github" },
        ],
        tags: ["BHP · Rio Tinto · Woodside", "31 requirements graded", "Four reporting areas"],
        updates: [
          {
            date: "18 Jun 2026",
            title: "First published",
            found: "Australia's new climate-disclosure rules (AASB S2) give every big company the same test. Reading BHP, Rio Tinto and Woodside against it, line by line, showed three very different levels of readiness.",
            change: "Published the three scorecards, 93 evidence-backed cells, and the cross-company gap summary, with every score tied to a page in the company's own report.",
          },
          {
            date: "20 Jun 2026",
            title: "A better picture than a table",
            found: "The flat scores table mostly repeated what the radar chart already said, and it buried the most interesting pattern: the row-level gaps that all three companies share.",
            change: "Replaced the table with a 31-requirement heatmap, so the shared weak band (asset-level metrics and dollar figures on the impact) jumps out at a glance.",
          },
          {
            date: "2 Jul 2026",
            title: "Showing the working",
            found: "The audit asked a fair question: the scores looked defensible, but a reader could not see the rubric behind them, or test whether the rankings would survive a different judgement call.",
            change: "Published the 0–4 rubric anchors, stated the equal-pillar weighting openly, and added a sensitivity script proving the maturity bands survive a one-point swing on all 21 medium-confidence scores.",
          },
        ],
      },
    ],
    services: [
      { icon: "wind", title: "Physical climate risk", text: "Finding the real trends in cyclones, rainfall, and heat, and what they mean for the assets and communities exposed to them." },
      { icon: "bar-chart", title: "Climate data analysis", text: "Working with official weather and climate data to pull out the real signal, clearly and honestly, not just the noise." },
      { icon: "file-text", title: "AASB S2 readiness", text: "Reading climate disclosures against Australia's new reporting rules, area by area, and pinpointing the gaps." },
    ],
  };
})();
