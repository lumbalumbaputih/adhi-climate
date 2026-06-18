# Interview brief: SW WA Rainfall Decline (1950–2024)

The goal: be able to talk about this for about 5 minutes without notes. You own the
interpretation; the numbers below are the backbone.

---

## The 30-second version

Winter rainfall in South West WA (the cool season) has fallen by about **3% a decade
since 1950**, and there is a clear **step down around the year 2000** (a sudden,
lasting drop to a lower level) that leaves the last 25 years roughly **a fifth (19%)
drier** than the 1950–1974 baseline. It shows up at **every one of the seven stations**
I looked at. The decline itself is not controversial: the Bureau of Meteorology and
CSIRO have documented it for years. What carries some nuance is the *cause*, and that
is the part worth understanding.

## The five-minute story (the arc)

1. **What I did.** I took 75 years of daily rainfall from seven long-record SW WA
   stations that cover the full range from wet to dry, from Cape Leeuwin and the
   southern forests through to the wheatbelt. I added the rain up over the
   April–October cool season (the cooler months) and measured each station against
   its own 1950–1974 baseline (its own early-period average). Then I tested for a
   trend, for a step-change, and for links to the big climate drivers.

2. **The headline.** A real, not-just-chance decline: about **−2.9% per decade** over
   the full record (Mann-Kendall p=0.001; Mann-Kendall is a standard test for whether
   a trend is genuine). The **May–July** early-winter peak is falling faster, about
   **−4.4% per decade**.

3. **It is a step, not a slope.** A Pettitt change-point test (a standard check for
   the point where a series shifts to a new level) puts the biggest single break around
   **2000** (p=0.006): the regional total drops from ~571 mm (1950–1999) to ~475 mm
   (2000–2024). Interestingly, *since* 2000 there is no further trend. It stepped down
   to a new, drier normal and stayed there. There was also an earlier, smaller step in
   the mid-1970s that the research talks about; my single-break test simply picks out
   the stronger 2000 shift.

4. **It is everywhere.** All seven stations decline, and six of the seven do so
   significantly. The wettest site, Cape Leeuwin, is dropping about 42 mm/decade. So
   this is not one odd rain gauge, it is a regional signal.

5. **Why (the honest part).** The science puts most of the decline down to a
   **strengthening band of high pressure over the subtropics** and a **shift of the
   winter storm tracks toward the South Pole** (which goes with a more-positive
   Southern Annular Mode), and that means **fewer cold fronts** reach the southwest.
   Those changes in air circulation are largely **human-caused**: greenhouse gases plus
   the ozone hole. I also compared rainfall directly against the Indian Ocean Dipole,
   SAM and ENSO. All three are negatively linked (r around −0.3 to −0.4), but once you
   remove the shared long-term trend, the year-to-year links are modest. That is the
   key point: **the modes explain the wiggles; the forced change in air circulation
   explains the downward staircase.**

## Numbers worth memorising

| Thing | Number |
|---|---|
| Full-record Apr–Oct trend | **−2.9%/decade** (≈ −20 mm/decade), p=0.001 |
| May–July trend | **−4.4%/decade** |
| Step-change year (Pettitt) | **~2000**, p=0.006 |
| 1950–1974 vs 2000–2024 | 587 mm → 475 mm = **−19%** |
| Stations declining | **7 of 7** (6 significant) |
| Driver correlations (raw) | IOD −0.41, ENSO −0.41, SAM −0.31 |

These line up with CSIRO and BoM: they report a ~16% Apr–Oct and ~20% May–Jul decline
since 1970, and they say a decline this big is "highly unlikely … due to natural
variability alone."

## Why it matters (AASB S2 chronic physical risk)

- **It is chronic, not acute.** This is a permanent downward shift in the baseline, not
  a run of dry years, and that is exactly the kind of slow, persistent hazard AASB S2
  (Australia's mandatory climate-disclosure standard) asks companies to report.
- **Who is exposed:** Perth's water supply (dam inflows have fallen much more than
  rainfall, because a small drop in rain turns into a big drop in runoff), the wheatbelt
  grain economy and the lenders behind it, and the property and crop insurers having to
  reprice the region.
- **The risk-assessment lesson:** because it is a step-change, you cannot assume the
  pre-2000 climate is your planning baseline. The recent 25 years are the new normal,
  and projections point further down.

## If they push you

- *"Couldn't this just be natural variability?"* A decline this large and this lasting
  sits at the upper edge of what natural variability produces, and climate models only
  reproduce it when you include human influence. So: largely human-driven, with natural
  variability nudging it up and down.
- *"How confident is the attribution number?"* Be honest: the estimates vary by study
  and method, anywhere from about 40% of the decline being driven by outside forcing in
  one model, to the high-pressure ridge explaining up to two-thirds. The *decline* is
  certain; the exact breakdown is still being worked out.
- *"Why GHCN-Daily and not the BoM website?"* GHCN-Daily *is* the BoM station data,
  redistributed by NOAA in a format you can pull with a script, so the whole thing
  re-runs with one command. I checked the result against BoM and CSIRO's published
  figures and they agree.

## Honest limitations (say these before they ask)

- Seven stations, not the whole gridded region. Solid, but not a substitute for BoM's
  gridded product.
- The Perth Darling-scarp catchment is not directly included (those stations had gappy
  daily records); the high-rainfall SW-corner stations stand in for it.
- The driver correlation shows **association, not formal attribution**. I am careful not
  to oversell it.
