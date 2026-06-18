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
        "I analyse Western Australia's physical climate risk, from intensifying cyclones to a drying south-west, and assess how the state's biggest emitters disclose that risk under AASB S2. The work pairs primary climate datasets with the disclosure standards now landing on every WA boardroom.",
      location: "Western Australia · remote-friendly",
      email: "hello@adhikatili.earth",
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
          "Forty years of South Indian Ocean track data, tested for trends in peak intensity and rapid intensification off the WA coast.",
        result: { value: "40", unit: "yrs", label: "of track data" },
        headline:
          "The ocean off Western Australia warmed about half a degree in 40 years. The cyclones did not get stronger.",
        body:
          "I combined IBTrACS and BOM best-track records for the South Indian Ocean to test whether tropical cyclones approaching Western Australia are intensifying: peak wind speed, minimum central pressure, and rapid-intensification frequency. The result runs against the intuitive 'warmer oceans, stronger storms' headline, and that is the point. Framed as AASB S2 physical risk against the 2025-26 season and Severe Tropical Cyclone Narelle's roughly $500M damage bill.",
        findings: [
          { value: "+0.5", unit: "°C", label: "Ocean warming, 1980s to today", text: "The cyclone development region warmed 0.16 °C per decade (p < 0.0001). A robust, statistically significant trend." },
          { value: "−3.6", unit: "kt/decade", label: "Peak wind trend", text: "Mean peak wind drifted down, not up. Basin-wide the decline is statistically significant (Mann-Kendall p = 0.048)." },
          { value: "−0.22", unit: "r", label: "SST vs intensity", text: "Warmer seasons were not associated with stronger storms. The thermal signal is decoupled from observed intensity." },
          { value: "~5", unit: "/season", label: "Storms within 500 km", text: "Frequency is stable to slightly declining, from 5.1 per season (1985-2004) to 4.6 (2005-2024)." },
        ],
        charts: [
          { src: "cyclone-risk/charts/01_annual_count.png", caption: "Annual cyclone counts: stable to slightly declining" },
          { src: "cyclone-risk/charts/02_intensity_by_decade.png", caption: "Peak intensity by decade: drifting down, not up" },
          { src: "cyclone-risk/charts/03_trend_wind_speed.png", caption: "Mean peak wind trend with significance test" },
          { src: "cyclone-risk/charts/04_trend_pressure.png", caption: "Minimum central pressure: weakening (rising)" },
          { src: "cyclone-risk/charts/05_rapid_intensification.png", caption: "Rapid intensification: apparently rising, read with caution" },
          { src: "cyclone-risk/charts/06_sst_correlation.png", caption: "Sea-surface temperature vs cyclone intensity: decoupled" },
        ],
        meaning:
          "You cannot read WA's future cyclone hazard straight off the recent local record. Warming oceans did not translate into stronger observed storms here, so an honest AASB S2 physical-risk assessment has to lean on forward-looking projections, not extrapolation of the past. Cyclone Narelle is the reminder that risk lives in the tail of the distribution, not the average.",
        resources: [
          { label: "Read the full analysis", href: ghBlob("cyclone-risk/README.md"), icon: "file-text" },
          { label: "Open the notebook", href: ghBlob("cyclone-risk/cyclone_analysis.ipynb"), icon: "bar-chart" },
          { label: "Cleaned datasets (6 CSVs)", href: ghTree("cyclone-risk/data"), icon: "layers" },
          { label: "All charts", href: ghTree("cyclone-risk/charts"), icon: "scan" },
          { label: "View on GitHub", href: ghTree("cyclone-risk"), icon: "github" },
        ],
        tags: ["IBTrACS + BOM", "Rapid intensification", "AASB S2 physical risk"],
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
          "Mapping one of the world's clearest regional drying signals: the step-change in south-west WA cool-season rainfall.",
        result: { value: "−19", unit: "%", label: "drier since the 1950s" },
        headline:
          "South West WA's cool-season rainfall did not gently slope down. It stepped down around the year 2000 and never came back.",
        body:
          "Using 74 years of BOM station records (redistributed through GHCN-Daily so the whole pipeline reproduces by script), I quantified the south-west WA cool-season rainfall decline and framed it as chronic physical climate risk for water security, agriculture, urban supply, and bushfire. The attribution is handled carefully, weighing ENSO, the Indian Ocean Dipole, and the Southern Annular Mode against anthropogenic forcing, rather than overclaiming.",
        findings: [
          { value: "−2.9%", unit: "/decade", label: "Cool-season trend since 1950", text: "Statistically significant (Mann-Kendall p = 0.001), roughly 20 mm lost every decade." },
          { value: "~2000", unit: "", label: "Step-change (Pettitt)", text: "A break point, not a slope: 571 mm before, 475 mm after (p = 0.006)." },
          { value: "−19%", unit: "", label: "Drier than the 1950-74 baseline", text: "The last 25 years are about a fifth drier. The May-July early-winter peak fell faster still (−4.4%/decade)." },
          { value: "7 / 7", unit: "", label: "Stations declining", text: "Every station analysed shows the signal, and six of seven are individually significant." },
        ],
        charts: [
          { src: "rainfall-decline/charts/01_timeseries_anomaly.png", caption: "Cool-season rainfall anomaly against the 1950-74 baseline" },
          { src: "rainfall-decline/charts/02_stepchange.png", caption: "Pettitt step-change: a drop around 2000, not a gentle slope" },
          { src: "rainfall-decline/charts/03_trend_mannkendall.png", caption: "Mann-Kendall trend with a 95% confidence band" },
          { src: "rainfall-decline/charts/04_driver_correlation.png", caption: "IOD, ENSO and SAM correlations, raw and detrended" },
          { src: "rainfall-decline/charts/05_station_decade.png", caption: "Station by decade: the signal is everywhere" },
        ],
        meaning:
          "This is textbook chronic physical risk: a permanent shift in the baseline, not a run of bad years. Because it is a step-change, the pre-2000 climate is no longer a valid planning baseline for Perth's water supply, the wheatbelt grain economy and its lenders, or insurers repricing the southwest. The decline is certain; the precise split between natural variability and anthropogenic forcing is where the analysis stays careful.",
        resources: [
          { label: "Read the full analysis", href: ghBlob("rainfall-decline/README.md"), icon: "file-text" },
          { label: "Open the notebook", href: ghBlob("rainfall-decline/rainfall_analysis.ipynb"), icon: "bar-chart" },
          { label: "Cleaned datasets (6 CSVs)", href: ghTree("rainfall-decline/data"), icon: "layers" },
          { label: "All charts", href: ghTree("rainfall-decline/charts"), icon: "scan" },
          { label: "View on GitHub", href: ghTree("rainfall-decline"), icon: "github" },
        ],
        tags: ["BOM station data", "Step-change", "Contested attribution"],
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
          "Scoring how three of WA's largest ASX emitters disclose climate risk across the four AASB S2 pillars.",
        result: { value: "3", unit: "firms", label: "scored, 93 cells" },
        headline:
          "Strong climate disclosure is not the same as low climate risk. Reading the actual reports, line by line, is the only way to tell them apart.",
        body:
          "I read the real sustainability and annual reports of three WA-headquartered ASX majors, BHP, Rio Tinto, and Woodside, and scored each across the four AASB S2 pillars (governance, strategy, risk management, and metrics & targets) on 31 sub-requirements. Every non-zero score carries a citation to the report's own section or page, and scoring was deliberately conservative. The output is a clear picture of common disclosure gaps, exactly the work ESG consultants are being paid for right now.",
        findings: [
          { value: "3", unit: "firms", label: "BHP · Rio Tinto · Woodside", text: "Scored across 31 AASB S2 sub-requirements, 93 evidence-backed cells in total." },
          { value: "3.69", unit: "/4", label: "Rio Tinto leads", text: "The only firm answering the cross-industry metrics in quantified form. Woodside scores 3.35, BHP 2.94." },
          { value: "575.7", unit: "Mt", label: "Rio Tinto Scope 3", text: "Against roughly 31.5 Mt operational. Scope 3 targets are the weakest link even at the top." },
          { value: "4", unit: "pillars", label: "Governance to metrics", text: "The clearest common gaps: asset-exposure metrics and quantified climate-related financial effects." },
        ],
        scoreboard: {
          headers: ["Company", "Gov", "Strategy", "Risk", "Metrics", "Overall", "Band"],
          rows: [
            ["Rio Tinto", "3.7", "3.7", "3.5", "3.9", "3.69", "Advanced"],
            ["Woodside", "3.8", "3.2", "3.3", "3.1", "3.35", "Advanced"],
            ["BHP", "3.0", "3.0", "3.0", "2.8", "2.94", "Developing"],
          ],
        },
        meaning:
          "The mandatory regime lifts completeness, but not evenly: depth comes from a company choosing to do the harder quantification, not from the calendar. Woodside is the clearest case that good disclosure and high exposure can sit in the same company, and the review keeps the two apart. That separation, disclosed readiness versus actual readiness, is the core analytical skill the project demonstrates.",
        resources: [
          { label: "Read the full review", href: ghBlob("aasb-s2-review/README.md"), icon: "file-text" },
          { label: "Scoring matrix (93 cells)", href: ghBlob("aasb-s2-review/scoring-matrix.csv"), icon: "layers" },
          { label: "Cross-company gap summary", href: ghBlob("aasb-s2-review/gap-summary.csv"), icon: "bar-chart" },
          { label: "Rio Tinto scorecard", href: ghBlob("aasb-s2-review/rio-tinto-scorecard.md"), icon: "file-text" },
          { label: "Woodside scorecard", href: ghBlob("aasb-s2-review/woodside-scorecard.md"), icon: "file-text" },
          { label: "BHP scorecard", href: ghBlob("aasb-s2-review/bhp-scorecard.md"), icon: "file-text" },
          { label: "View on GitHub", href: ghTree("aasb-s2-review"), icon: "github" },
        ],
        tags: ["BHP · Rio Tinto · Woodside", "31 sub-requirements", "Four S2 pillars"],
      },
    ],
    services: [
      { icon: "wind", title: "Physical climate risk", text: "Cyclone, rainfall, and heat trend analysis framed for AASB S2 physical risk." },
      { icon: "bar-chart", title: "Climate data analysis", text: "IBTrACS, BOM, and reanalysis data, with trend detection and rapid-intensification signals." },
      { icon: "file-text", title: "AASB S2 readiness", text: "Scoring disclosures across governance, strategy, risk management, and metrics & targets." },
    ],
  };
})();
