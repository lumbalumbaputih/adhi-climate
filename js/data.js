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
        "I dig into the real climate risks facing Western Australia, like what is actually happening to its cyclones, its drying south-west, its shrinking rivers and its hotter summers, and I check how the state's biggest companies report those risks under Australia's new climate rules (AASB S2). The goal is simple: turn raw climate data into clear answers that business and government can act on.",
      location: "Western Australia · remote-friendly",
      email: "adhiazure@gmail.com",
      linkedin: "https://www.linkedin.com/in/adhi-m/",
      availability: "Available for internships · Perth, WA or remote",
    },
    stats: [
      { label: "Projects complete", value: "5", caption: "storms to scorecards" },
      { label: "Longest record", value: "81", unit: "yrs", caption: "Perth heat, 1945–2025" },
      { label: "Storms tracked", value: "193", caption: "within 500 km of WA" },
      { label: "Emitters scored", value: "3", caption: "WA ASX majors" },
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
