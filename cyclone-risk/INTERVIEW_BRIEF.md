# Interview Brief — WA Cyclone Climate Risk Analysis

Everything you need to speak to this project for about five minutes without
notes. Read it a few times, say it out loud once, and you will own it. The whole
project is honest about an unglamorous result, and interviewers respect that far
more than a tidy but overstated story.

---

## The 30-second pitch

"I wanted to know whether the cyclones that hit Western Australia have been
getting stronger as the ocean warms, because that is exactly the kind of question
AASB S2 now forces companies to answer about physical climate risk. I pulled 40
years of cyclone best-track data and NOAA sea-surface-temperature data, cleaned
it in Python, and tested the trends myself. The seas off WA warmed about half a
degree over that time, but the cyclones did not get stronger. If anything they
weakened slightly, and there was no positive link between ocean temperature and
storm intensity. The lesson for risk disclosure is that you cannot just
extrapolate the past; you have to use forward-looking projections."

## The four findings, in order

1. **Frequency is flat to slightly down.** About five storms come within 500 km
   of WA each year, drifting from roughly 5.1 to 4.6 a season. This matches the
   known long-term decline in Australian-region cyclone numbers.

2. **Intensity has not risen.** Average peak winds fell from about 76 to 63 knots
   across the four decades, and pressure weakened. The decline is statistically
   significant across the whole South Indian Ocean, but only marginal for the
   WA-only subset because the sample is small.

3. **Rapid intensification looks more common, but be careful.** The share of
   storms that jumped 30 knots in a day rose from about 21% to 40%. I flag openly
   that older data is coarser, so part of that rise is probably an observing
   artefact, not pure physics.

4. **Warming oceans are decoupled from intensity.** SST rose significantly
   (0.16 degrees per decade) yet did not correlate with stronger storms. That is
   the most interesting result, and it points to wind shear and large-scale
   circulation, things like ENSO and the Indian Ocean Dipole, as the real
   controls.

## Why the "boring" answer is the strong answer

If you get asked "so climate change isn't making WA cyclones worse?", do not
retreat. The answer is:

"The observed record does not show intensification yet, and I report that
honestly. But that is not the same as safety. The ocean has clearly warmed, the
energy ceiling for the worst storms has risen, and the models still project fewer
but more intense systems. The point of the analysis is that you cannot justify a
risk rating by extrapolating a local trend that does not exist, in either
direction. You have to use scenario projections. That is precisely what AASB S2
asks for, and it is why physical-risk work is judgement, not just trend-fitting."

## The AASB S2 connection (know this cold)

AASB S2 is Australia's mandatory climate-disclosure standard. It started on
1 January 2025 and is phased by company size; the second group, which includes
many large WA operators, begins reporting for periods from 1 July 2026. It
requires companies to disclose material physical climate risks. Cyclone hazard to
Pilbara iron-ore and LNG infrastructure, ports, and coastal towns is a textbook
example. This project is a small worked example of the physical-risk evidence base
a consultant would build.

## Questions you should expect, and answers

**"Which wind measurement did you use and why?"**
BOM 10-minute sustained wind, because the subject is WA and that is the Australian
convention. I cross-checked it against US 1-minute winds, which run about 12%
higher purely because of the shorter averaging period, and against central
pressure, which avoids the convention issue entirely. All three agree on the
direction.

**"How do you know your data cleaning is right?"**
I validated it three ways. My BOM winds match the Bureau's own published database
to the knot for the big storms. The 12% wind gap between conventions is exactly
what theory predicts. And 97% of the storms my 500 km rule flagged as WA-affecting
also appear in the Bureau's Australian database.

**"Why not just use a stats library?"**
I implemented the trend tests, Mann-Kendall and Sen's slope and regression, from
first principles and unit-tested them against textbook values. It keeps the work
transparent and dependency-light, and it shows I understand the maths rather than
calling a black box.

**"What is the single biggest limitation?"**
Sample size for the WA-only trends. Five storms a year over 40 years is noisy, so
the WA-specific results are directional, not definitive. I am explicit about that,
and I lean on the larger basin-wide sample where I need statistical power.

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
be forward-looking, not a straight line drawn through the past."
