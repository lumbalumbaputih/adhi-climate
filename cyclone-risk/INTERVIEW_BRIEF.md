# Interview Brief: WA Cyclone Climate Risk Analysis

Everything you need to talk about this project for about five minutes without
notes. Read it a few times, say it out loud once, and you will own it. The whole
project is honest about an unexciting result, and interviewers respect that far
more than a tidy but overstated story.

---

## The 30-second pitch

"I wanted to know whether the cyclones that hit Western Australia have been
getting stronger as the ocean warms, because that is exactly the kind of question
AASB S2 now forces companies to answer about physical climate risk. (AASB S2 is
Australia's mandatory climate-disclosure standard.) I pulled 40 years of cyclone
best-track data, which is the official storm-path records that weather agencies
keep, plus NOAA sea-surface-temperature data. I cleaned it in Python and tested
the trends myself. The seas off WA warmed about half a degree over that time, but
the cyclones did not get stronger. If anything they weakened slightly, and there
was no positive link between ocean temperature and storm strength. The lesson for
risk disclosure is that you cannot just project the past forward; you have to use
forward-looking projections."

## The four findings, in order

1. **Frequency is flat to slightly down.** About five storms come within 500 km
   of WA each year, drifting from roughly 5.1 to 4.6 a season. This matches the
   known long-term decline in the number of cyclones in the Australian region.

2. **Intensity has not risen.** Average peak winds fell from about 76 to 63 knots
   across the four decades, and pressure weakened. The decline is statistically
   significant (a real trend, not chance) across the whole South Indian Ocean, but
   only borderline for the WA-only group because the sample is small.

3. **Rapid intensification looks more common, but be careful.** The share of
   storms that jumped 30 knots in a day rose from about 21% to 40%. I say openly
   that older data is coarser, so part of that rise is probably a measurement
   artefact, not real physics.

4. **Warming oceans are unhooked from intensity.** Sea-surface temperature (SST,
   the temperature of the top layer of the ocean) rose significantly, 0.16 degrees
   per decade, yet did not go with stronger storms. That is the most interesting
   result. It points to wind shear (winds that change with height and can tear a
   storm apart) and large-scale circulation, things like ENSO (the El Niño/La Niña
   cycle) and the Indian Ocean Dipole (a related Indian Ocean temperature
   pattern), as the real controls.

## Why the "boring" answer is the strong answer

If someone asks "so climate change isn't making WA cyclones worse?", do not back
down. The answer is:

"The observed record does not show storms getting stronger yet, and I report that
honestly. But that is not the same as being safe. The ocean has clearly warmed,
the energy ceiling for the worst storms has risen, and the models still project
fewer but more intense systems. The point of the analysis is that you cannot
justify a risk rating by extending a local trend that does not exist, in either
direction. You have to use scenario projections. That is exactly what AASB S2 asks
for, and it is why physical-risk work is a matter of judgement, not just
fitting a line to the past."

## The AASB S2 connection (know this cold)

AASB S2 is Australia's mandatory climate-disclosure standard (the rule that
requires companies to report their climate risks). It started on 1 January 2025
and is phased in by company size; the second group, which includes many large WA
operators, begins reporting for periods from 1 July 2026. It requires companies to
disclose the physical climate risks that are material to them. Cyclone hazard to
Pilbara iron-ore and LNG infrastructure, ports, and coastal towns is a textbook
example. This project is a small worked example of the physical-risk evidence base
a consultant would build.

## Questions you should expect, and answers

**"Which wind measurement did you use and why?"**
The BOM 10-minute sustained wind (the wind speed averaged over 10 minutes), because
the subject is WA and that is the Australian convention. BOM is the Bureau of
Meteorology, Australia's national weather agency. I cross-checked it against US
1-minute winds, which run about 12% higher purely because of the shorter averaging
period, and against central pressure (the air pressure at the storm's centre),
which avoids the averaging issue entirely. All three agree on the direction.

**"How do you know your data cleaning is right?"**
I validated it three ways. My BOM winds match the Bureau's own published database
to the knot for the big storms. The 12% wind gap between the two conventions is
exactly what theory predicts. And 97% of the storms my 500 km rule flagged as
WA-affecting also appear in the Bureau's Australian database.

**"Why not just use a stats library?"**
I wrote the trend tests, Mann-Kendall and Sen's slope and regression, from scratch
and unit-tested them against textbook values. (Mann-Kendall is a standard check
for whether a trend is real or just chance, and Sen's slope is a robust way to
estimate the size of that trend.) It keeps the work transparent and light on
dependencies, and it shows I understand the maths rather than calling a black box.

**"What is the single biggest limitation?"**
Sample size for the WA-only trends. Five storms a year over 40 years is noisy, so
the WA-specific results show a direction but are not definitive. I am explicit
about that, and I lean on the larger basin-wide sample when I need statistical
power.

## Numbers worth memorising

- 758 South Indian Ocean storms, 194 WA-affecting, 1985 to 2024 (40 seasons).
- Ocean warming: +0.16 degrees C per decade, about +0.5 C total, highly
  significant.
- WA intensity: down about 3.6 knots per decade, not significant on its own.
- Basin-wide intensity: down 3.7 knots per decade, significant (p ≈ 0.05).
- SST-to-intensity correlation: r ≈ −0.2, not significant. No positive link.
- Rapid intensification: roughly 21% to 40% of storms, with a data caveat.

## One sentence to close on

"The headline is that warming did not show up as stronger WA cyclones in the
record, and the professional lesson is that good physical-risk disclosure has to
look forward, not just draw a straight line through the past."
