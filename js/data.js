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
        "I dig into the real climate risks facing Western Australia, like what is actually happening to its cyclones and its drying south-west, and I check how the state's biggest companies report those risks under Australia's new climate rules (AASB S2). The goal is simple: turn raw climate data into clear answers that business and government can act on.",
      location: "Western Australia · remote-friendly",
      email: "adhiazure@gmail.com",
      linkedin: "https://www.linkedin.com/in/adhi-m/",
      availability: "Available for internships · Perth, WA or remote",
    },
    stats: [
      { label: "Cyclone record", value: "40", unit: "yrs", caption: "1985–2024 tracks" },
      { label: "Rainfall record", value: "74", unit: "yrs", caption: "1950–2024 stations" },
      { label: "Emitters scored", value: "3", caption: "WA ASX majors" },
      { label: "AASB S2 pillars", value: "4", caption: "governance to metrics" },
    ],
    projects: [
      {
        id: "wa-cyclones",
        title: "WA Cyclone Intensity Trends",
        year: "1985–2024",
        status: "Complete",
        category: ["Physical risk", "Climate data", "Data viz"],
        icon: "wind",
        meta: "6 charts · reproducible notebook · 6 open datasets",
        summary:
          "Forty years of cyclone records, checked against one simple question: as the ocean warmed, did the storms hitting WA actually get stronger?",
        result: { value: "40", unit: "yrs", label: "of storm records" },
        headline:
          "The ocean off Western Australia warmed about half a degree in 40 years. The cyclones did not get stronger.",
        body:
          "Most people assume that as the ocean warms, storms get stronger. I put that to the test for Western Australia using 40 years of official cyclone records from international and Australian weather agencies, looking at how strong the storms got and how often they strengthened very fast. The answer was the opposite of what you would expect, and that is exactly why it is worth knowing. It matters because WA's biggest companies now have to report their climate risks under new Australian rules (AASB S2), and those reports need to be built on what the data really shows, not on gut feel.",
        findings: [
          { value: "+0.5", unit: "°C", label: "The ocean is warming", text: "The sea where these cyclones form has warmed by about half a degree since the 1980s. This part is rock solid in the data." },
          { value: "−3.6", unit: "kt/decade", label: "But the storms are not", text: "Despite the warmer ocean, the storms' top wind speeds have edged down, not up, over the 40 years." },
          { value: "−0.22", unit: "link", label: "Warmer seas, stronger storms?", text: "No. Warmer years did not bring stronger storms here. The connection people assume simply is not in WA's record." },
          { value: "~5", unit: "/year", label: "Storms near the coast", text: "About five cyclones come within 500 km of the WA coast in a typical year, a number that has held steady or dipped slightly." },
        ],
        charts: [
          { src: "cyclone-risk/charts/01_annual_count.png", caption: "How many cyclones each year: steady, with a slight dip" },
          { src: "cyclone-risk/charts/02_intensity_by_decade.png", caption: "How strong the storms got, decade by decade: edging down, not up" },
          { src: "cyclone-risk/charts/03_trend_wind_speed.png", caption: "Average top wind speed over time: a gentle downward trend" },
          { src: "cyclone-risk/charts/04_trend_pressure.png", caption: "A second way of measuring strength agrees: storms got slightly weaker" },
          { src: "cyclone-risk/charts/05_rapid_intensification.png", caption: "Storms strengthening very fast: it looks like it is rising, but read with care" },
          { src: "cyclone-risk/charts/06_sst_correlation.png", caption: "Warmer oceans did not mean stronger storms" },
        ],
        meaning:
          "The lesson is simple but important: you cannot judge WA's future cyclone danger just by looking at the recent past. The ocean has warmed, yet the storms here have not gotten stronger, so honest climate-risk reporting has to lean on future projections rather than assume the past will repeat. And a quiet long-term trend does not mean we are safe. Severe Tropical Cyclone Narelle in 2026 caused around $500 million in damage, a reminder that the real danger lives in the rare, extreme storm, not the average one.",
        resources: [
          { label: "Read the full analysis", href: ghBlob("cyclone-risk/README.md"), icon: "file-text" },
          { label: "Open the notebook", href: ghBlob("cyclone-risk/cyclone_analysis.ipynb"), icon: "bar-chart" },
          { label: "Cleaned datasets (6 CSVs)", href: ghTree("cyclone-risk/data"), icon: "layers" },
          { label: "All charts", href: ghTree("cyclone-risk/charts"), icon: "scan" },
          { label: "View on GitHub", href: ghTree("cyclone-risk"), icon: "github" },
        ],
        feature: 5,
        dataset: {
          caption: "WA-affecting cyclones by decade (IBTrACS + BOM)",
          columns: ["Decade", "WA storms", "Mean peak wind (kt)", "Mean min pressure (hPa)", "Reached Cat 3+"],
          rows: [
            ["1985–94", "47", "76", "959", "17%"],
            ["1995–04", "55", "78", "956", "38%"],
            ["2005–14", "50", "69", "964", "28%"],
            ["2015–24", "42", "63", "973", "19%"],
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
        result: { value: "−19", unit: "%", label: "drier than the 1950s" },
        headline:
          "South West WA's winter rain did not slowly tail off. It dropped suddenly around the year 2000 and never came back.",
        body:
          "Using 74 years of rainfall records from Bureau of Meteorology weather stations, I measured how much the cooler-months rain (April to October) in south-west WA has fallen, and what that means for the people who depend on it: water suppliers, farmers, and insurers. I was careful about the cause too, weighing natural climate cycles against human-caused climate change rather than overclaiming either way.",
        findings: [
          { value: "−2.9%", unit: "/decade", label: "Winter rain is falling", text: "The cooler-months rain has dropped about 3% every decade since 1950, roughly 20 mm less rain each decade. This is a real trend, not chance." },
          { value: "~2000", unit: "", label: "When it changed", text: "The fall was not gradual. Rainfall dropped suddenly around the year 2000 and then settled at a new, lower level (from about 571 mm a year to 475 mm)." },
          { value: "−19%", unit: "", label: "Drier than the 1950s", text: "The last 25 years have been about a fifth drier than the 1950s, and early winter (May to July) has dried out even faster." },
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
        scoreboard: {
          headers: ["Company", "Gov", "Strategy", "Risk", "Metrics", "Overall", "Band"],
          rows: [
            ["Rio Tinto", "3.7", "3.7", "3.5", "3.9", "3.69", "Advanced"],
            ["Woodside", "3.8", "3.2", "3.3", "3.1", "3.35", "Advanced"],
            ["BHP", "3.0", "3.0", "3.0", "2.8", "2.94", "Developing"],
          ],
        },
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
      },
    ],
    services: [
      { icon: "wind", title: "Physical climate risk", text: "Finding the real trends in cyclones, rainfall, and heat, and what they mean for the assets and communities exposed to them." },
      { icon: "bar-chart", title: "Climate data analysis", text: "Working with official weather and climate data to pull out the real signal, clearly and honestly, not just the noise." },
      { icon: "file-text", title: "AASB S2 readiness", text: "Reading climate disclosures against Australia's new reporting rules, area by area, and pinpointing the gaps." },
    ],
  };
})();
