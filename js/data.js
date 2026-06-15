(function () {
  window.PORTFOLIO = {
    profile: {
      name: "Adhi Katili",
      role: "Climate & Sustainability",
      tagline: "I turn Western Australia's climate data into decisions business and government can act on.",
      intro:
        "I analyse Western Australia's physical climate risk — intensifying cyclones, a drying south-west — and assess how the state's biggest emitters disclose that risk under AASB S2. The work pairs primary climate datasets with the disclosure standards now landing on every WA boardroom.",
      location: "Western Australia · remote-friendly",
      email: "hello@adhikatili.earth",
    },
    stats: [
      { label: "Cyclone record", value: "40", unit: "yrs", caption: "1985–2024 tracks" },
      { label: "Rainfall record", value: "74", unit: "yrs", caption: "1950–2024 stations" },
      { label: "Emitters scored", value: "6", caption: "WA ASX majors" },
      { label: "AASB S2 pillars", value: "4", caption: "governance → metrics" },
    ],
    filters: ["All", "Physical risk", "Climate data", "Disclosure & AASB S2", "Data viz"],
    projects: [
      {
        id: "wa-cyclones",
        title: "WA Cyclone Intensity Trends",
        year: "1985–2024",
        status: "Published",
        category: ["Physical risk", "Climate data", "Data viz"],
        icon: "wind",
        summary:
          "Forty years of South Indian Ocean track data, tested for trends in peak intensity and rapid intensification off the WA coast.",
        result: { value: "40", unit: "yrs", label: "of track data" },
        body:
          "Combined IBTrACS and BOM best-track records for the South Indian Ocean to test whether tropical cyclones approaching Western Australia are intensifying — peak wind speed, minimum central pressure, and rapid-intensification frequency. Framed as AASB S2 physical risk against the 2025–26 season and Cyclone Narelle's ~$500M damage bill. Documented in the wiki.",
        tags: ["IBTrACS + BOM", "Rapid intensification", "AASB S2 physical risk"],
      },
      {
        id: "sw-wa-rainfall",
        title: "SW WA Rainfall Decline",
        year: "1950–2024",
        status: "In progress",
        category: ["Physical risk", "Climate data"],
        icon: "droplet",
        summary:
          "Mapping one of the world's clearest regional drying signals — the step-change in south-west WA cool-season rainfall.",
        result: { value: "74", unit: "yrs", label: "of station data" },
        body:
          "Using BOM station records to quantify the south-west WA cool-season rainfall step-change and frame it as chronic physical climate risk for water security, agriculture, urban supply, and bushfire. The attribution is handled carefully — ENSO and the Indian Ocean Dipole versus anthropogenic forcing — rather than overclaiming. Relevant to the WA government, water utilities, and the agriculture sector.",
        tags: ["BOM station data", "Step-change", "Contested attribution"],
      },
      {
        id: "aasb-s2-readiness",
        title: "AASB S2 Readiness: WA's Biggest Emitters",
        year: "2025",
        status: "In progress",
        category: ["Disclosure & AASB S2", "Policy"],
        icon: "file-text",
        summary:
          "Scoring how WA's largest ASX emitters disclose climate risk across the four AASB S2 pillars.",
        result: { value: "6", unit: "firms", label: "scored" },
        body:
          "Reading the actual sustainability and annual reports of WA-headquartered ASX majors — BHP, Rio Tinto, Woodside, Fortescue, Mineral Resources, and South32 — and scoring each across the four AASB S2 pillars: governance, strategy, risk management, and metrics & targets. The output is a clear picture of common disclosure gaps — exactly the work ESG consultants are being paid for right now.",
        tags: ["BHP · Rio · Woodside", "Fortescue · MinRes · South32", "Four S2 pillars"],
      },
    ],
    services: [
      { icon: "wind", title: "Physical climate risk", text: "Cyclone, rainfall, and heat trend analysis framed for AASB S2 physical risk." },
      { icon: "bar-chart", title: "Climate data analysis", text: "IBTrACS, BOM, and reanalysis data — trend detection and rapid-intensification signals." },
      { icon: "file-text", title: "AASB S2 readiness", text: "Scoring disclosures across governance, strategy, risk management, and metrics & targets." },
    ],
  };
})();
