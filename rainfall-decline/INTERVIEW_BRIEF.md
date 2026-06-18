# Interview brief — SW WA Rainfall Decline (1950–2024)

The goal: be able to talk to this for ~5 minutes without notes. You own the
interpretation; the numbers below are the spine.

---

## The 30-second version

South West WA's cool-season rainfall has fallen by about **3% a decade since
1950**, and there's a clear **step down around the year 2000** that leaves the
last 25 years roughly **a fifth (19%) drier** than the 1950–1974 baseline. It
shows up at **every one of the seven stations** I looked at. The decline itself
is not controversial — the Bureau of Meteorology and CSIRO have documented it for
years. What carries nuance is the *cause*, and that's the part worth
understanding.

## The five-minute story (the arc)

1. **What I did.** Took 75 years of daily rainfall from seven long-record SW WA
   stations spanning the gradient — from Cape Leeuwin and the southern forests
   through to the wheatbelt — added them up over the April–October cool season,
   and measured each one against its own 1950–1974 baseline. Then I tested for a
   trend, for a step-change, and for links to the big climate drivers.

2. **The headline.** A statistically significant decline: about **−2.9% per
   decade** over the full record (Mann-Kendall p=0.001). The **May–July**
   early-winter peak is falling faster, about **−4.4% per decade**.

3. **It's a step, not a slope.** A Pettitt change-point test puts the biggest
   single break around **2000** (p=0.006): the regional total drops from ~571 mm
   (1950–1999) to ~475 mm (2000–2024). Interestingly, *since* 2000 there's no
   further trend — it stepped down to a new, drier normal and stayed there. There
   was also an earlier, smaller step in the mid-1970s that the literature talks
   about; my single-break test just picks the stronger 2000 shift.

4. **It's everywhere.** All seven stations decline; six of seven significantly.
   The wettest site, Cape Leeuwin, is dropping ~42 mm/decade. So this isn't one
   odd gauge — it's a regional signal.

5. **Why (the honest part).** The science attributes most of the decline to a
   **strengthening subtropical high-pressure ridge** and a **poleward shift of
   the winter storm tracks** (a more-positive Southern Annular Mode), which means
   **fewer cold fronts** reach the southwest. Those circulation changes are
   substantially **human-caused** — greenhouse gases plus the ozone hole. I also
   correlated rainfall against the Indian Ocean Dipole, SAM and ENSO directly:
   all three are negatively associated (r around −0.3 to −0.4), but once you
   remove the shared long-term trend the year-to-year correlations are modest.
   That's the key point — **the modes explain the wiggles; the forced
   circulation change explains the downward staircase.**

## Numbers worth memorising

| Thing | Number |
|---|---|
| Full-record Apr–Oct trend | **−2.9%/decade** (≈ −20 mm/decade), p=0.001 |
| May–July trend | **−4.4%/decade** |
| Step-change year (Pettitt) | **~2000**, p=0.006 |
| 1950–1974 vs 2000–2024 | 587 mm → 475 mm = **−19%** |
| Stations declining | **7 of 7** (6 significant) |
| Driver correlations (raw) | IOD −0.41, ENSO −0.41, SAM −0.31 |

These line up with CSIRO/BoM: they report ~16% Apr–Oct and ~20% May–Jul decline
since 1970, and say a decline this big is "highly unlikely … due to natural
variability alone."

## Why it matters (AASB S2 chronic physical risk)

- **It's chronic, not acute.** This is a permanent downward shift in the
  baseline, not a run of dry years — exactly the slow-onset, persistent hazard
  AASB S2 asks companies to disclose.
- **Who's exposed:** Perth's water supply (dam inflows have fallen far more than
  rainfall — a small rainfall drop is amplified into a big runoff drop), the
  wheatbelt grain economy and the lenders behind it, and property/crop insurers
  repricing the region.
- **The risk-assessment lesson:** because it's a step-change, you can't assume the
  pre-2000 climate is your planning baseline. The recent 25 years are the new
  normal — and projections point further down.

## If they push you

- *"Couldn't this just be natural variability?"* — A decline of this size and
  persistence is at the upper edge of what natural variability produces, and
  climate models only reproduce it when you include human forcing. So: largely
  forced, with natural variability modulating it.
- *"How confident is the attribution number?"* — Be honest: estimates vary by
  study and method — anywhere from ~40% of the decline being externally forced in
  one model to the subtropical ridge explaining up to two-thirds. The *decline* is
  certain; the exact apportionment is still being refined.
- *"Why GHCN-Daily and not the BoM website?"* — GHCN-Daily *is* the BoM station
  observations, redistributed by NOAA in a scriptable format, so the whole thing
  reproduces with one script. I validated the result against BoM/CSIRO's published
  figures and they agree.

## Honest limitations (say these before they ask)

- Seven stations, not the whole gridded region — robust, but not a substitute for
  BoM's gridded product.
- The Perth Darling-scarp catchment isn't directly represented (those stations had
  gappy daily records); the high-rainfall SW-corner stations stand in for it.
- The driver correlation is **association, not formal attribution** — I'm careful
  not to oversell it.
