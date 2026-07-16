# Visualisation improvement plan

A detailed, phased plan to raise the quality of every chart in this portfolio:
the interactive SVG charts on the site, the matplotlib PNGs in each project's
`charts/`, and the plumbing that keeps the two in sync. It follows the house
rules in `PROCEDURE.md` (no em dashes, every number traces to open data,
honesty over a big headline) and is written so each phase can ship as its own
small PR.

The one-sentence diagnosis: **the analysis is stronger than its presentation.**
The static chart library already contains the portfolio's best visual ideas
(the fuel-mix area, the flood calendar, the seasonal fire heatmap, the event
bubble timeline), but most of them never made it to the project pages, which
often carry only two or three generic line charts. Meanwhile the interactive
chart kit is solid but under-labelled: trends, bands and step lines appear
with no legend, line charts have no x-axis title, and several colours are
hard-coded hexes that ignore dark mode.

## 1. Where things stand (audit)

### The interactive kit (`js/charts.js`, 644 lines, dependency-free)

Nine components: LineChart, BarChart, ScatterChart, HeatTable, MapChart,
RainMapChart, RadarChart, DotCompare, ScoreHeat. Genuine strengths worth
keeping:

- Dependency-free SVG with a `--ck` scale factor so text stays a constant
  on-screen size at any card width.
- Tap-friendly hit targets (invisible fat strokes on map tracks, transparent
  14px strokes on scatter dots, full-height hover bands on lines).
- Honest form choices already made once: the AASB radar was demoted behind a
  toggle in favour of a dot plot, and the cyclone map greys the weak majority
  so severe storms carry the story.
- `prefers-reduced-motion` respected on all draw animations.

Systematic gaps, all fixable in the shared components so every project
benefits at once:

| Gap | Where it bites |
|---|---|
| No legend or direct label for the dashed trend line, the confidence band, the overlay mean, or the pre/post step lines | Every line chart: a reader cannot tell what the green dashed line is without guessing |
| `LineChart` never renders `data.xlabel` (only `ScatterChart` does) | Every time series: "Season", "Year" etc. are silently dropped |
| No annotation layer: no way to mark a year ("step change, 2000", "Ningaloo 2011", "Safeguard reform 2023") or a reference threshold | Every project: the write-up names the moment, the chart does not show it |
| Hard-coded colours that ignore dark mode: `.chart__bar2` pos/neg hexes, `heatColor()` rgba values, tooltip backgrounds, scrolly note colour | Anomaly bars, rainfall heat table, tooltips |
| Hover is mouse/tap only: chart marks are not focusable, no keyboard path to values (ScoreHeat is the one exception and shows the pattern) | All charts except ScoreHeat |
| No shared number formatting: no thousands separators, units repeated inconsistently between axis, tooltip and caption | Bars and tooltips |
| One layout for everything: 6 to 8 equal cards in a horizontal rail, so the hero chart of each story has the same weight as the fourth supporting view | Every project page |

### The static pipeline (`<project>/viz.py`, matplotlib, 300 dpi PNGs)

Consistent "Hidup" palette and a credit line on every figure: good. But each
`viz.py` re-declares the palette and rcParams by copy-paste, so they have
already drifted slightly, and there is no equivalent of the byte-identical
`stats_utils.py` discipline. Chart-level issues found in the audit:

- **Bubble timeline (marine-heatwaves 02):** size encodes duration but there
  is no size legend; the Moderate/Strong colours (mango yellow, tomato) are
  adjacent hues that need a colour-vision check.
- **Fuel-mix area (swis 01):** near-black coal band is a heavy saturated
  block; distillate, bio and other are invisible slivers that still spend
  legend slots; legend order does not match the visual stack order.
- **Full box spines and mid-grey grid on every chart:** more frame than data;
  top/right spines add nothing.
- **Embedded bold titles** duplicate the captions the site and READMEs
  already provide, and lock the wording into the pixels.

### The gap between the two

Charts that exist only as PNGs but belong on the interactive pages, because
they carry each project's actual story:

| Project | Static-only chart | Interactive today |
|---|---|---|
| swis-decarbonisation | fuel mix stacked area, coal vs renewables crossover | 2 line charts |
| transition-risk | concentration, sector trends, headroom, crossover, cost sensitivity | 1 bar + 1 line |
| bushfire-weather | seasonal heatmap, season span, decade bars | 2 line charts |
| high-water | flood calendar heatmap, distribution shift | 2 lines + 1 grouped bar |
| marine-heatwaves | event bubble timeline, biggest-event zoom (SST vs climatology band) | 2 lines + 1 bar |
| wheat-yields | drought years, paired series | 2 lines + 1 bar |

## 2. Principles (applied to every change below)

1. **Form first, colour last.** Pick the chart by the reader's job: compare
   magnitude, spot a trend, see a polarity, or read one number. If the story
   is one number, the stat blocks (`findings`) already do that job well: do
   not add a chart that repeats them.
2. **One axis, always.** Two measures of different scale get two charts, small
   multiples, or a common index (=100 at the start year). Never dual y-axes.
3. **Emphasis over rainbow.** When one series is the point, it gets the accent
   colour and everything else goes grey (the cyclone map already does this,
   the line charts should too).
4. **Colour is computed, not eyeballed.** Define the chart palette once as
   tokens, then validate it (lightness band, chroma floor, adjacent-pair
   colour-vision separation, contrast) for the light surface and the dark
   surface separately. Fix failures before shipping.
5. **Nothing is colour-alone.** Every multi-series chart keeps a legend, key
   series get direct labels, and every chart keeps its sortable-table twin
   (the `dataset` table each project already has).
6. **Annotate the finding.** If the write-up says "the rivers stepped down in
   2001", the chart shows a marked, labelled 2001. The chart should be able to
   defend the headline on its own.
7. **Uncertainty is part of the picture.** Where `analysis.py` already
   computes a confidence interval or p-value, the chart shows the band or
   states the trend with its significance, not just a clean line.

## 3. Workstream A: foundations (one PR, everything else builds on it)

**A1. Chart colour tokens.** Add a `charts` block to `tokens/colors.css`:
`--chart-1` … `--chart-6` (fixed categorical order, never cycled), `--chart-pos`
/ `--chart-neg` (diverging pair with a neutral midpoint), `--chart-context`
(the de-emphasis grey), `--chart-band` (translucent CI fill), plus dark-mode
overrides selected from the same ramps (not an automatic flip). Replace every
hard-coded hex in `charts.js` and `portfolio.css` (`chart__bar2`, `heatColor`,
tooltip backgrounds, scrolly note) with these tokens.

**A2. Validate both palettes.** Run a colour-vision and contrast validation of
the categorical set, the diverging pair, and the heat ramps against both the
light and dark chart surfaces. Record the passing hexes in a short
`tokens/CHART-COLOURS.md` note so future edits re-run the same check. The
marine-heatwave category colours (mango/tomato/mawar/ink) and the AASB score
scale get the same treatment.

**A3. Legend and annotation support in the shared components.** Extend the
chart data shape (documented in `PROCEDURE.md` step 2) with:

- `series` labels so LineChart renders a small legend row (reusing the
  existing `chart__legend`) whenever a trend, band, overlay or step line is
  present: "annual", "OLS trend", "5-yr mean", "95% band".
- `marks: [{x, label}]` for labelled vertical event markers and
  `refline: {y, label}` for thresholds. Rendered as a hairline with a small
  end label, collision-nudged, hidden from the axis grid.
- `xlabel` rendered by LineChart and BarChart, not just ScatterChart.

**A4. Keyboard access.** Make the invisible hover targets focusable
(`tabIndex`, `onFocus`/`onBlur` mirroring hover, left/right arrow to walk
points), reusing the pattern ScoreHeat already proves. The tooltip becomes the
focus readout; every value remains reachable in the data table.

**A5. Shared number formatting.** One `fmt(value, unit)` helper: thin-space
thousands, one decimal max on hover, unit once. Used by axes, tooltips and
direct labels.

## 4. Workstream B: site-wide layout and new shared components

**B1. Hero chart layout.** Give each story an optional `hero` viz key: the
first chart renders solo at wide width (the existing `story__deep--solo`
treatment) with its annotation marks visible, and the remaining views stay in
the swipe rail. The hero is the chart that carries the headline stat.

**B2. Small-multiples card.** A `multiples` chart type: 2 to 4 mini line
charts with a shared y-scale and one legend, for the station-vs-station and
driver-vs-driver comparisons that are currently 3 to 6 separate rail cards.

**B3. Stacked-area component.** One new `AreaChart` (stacked, 100% mode
optional) for the SWIS fuel mix: at most 5 bands plus "Other" (fold
distillate, bio, other together), direct labels inside the wide bands, legend
in stack order, 2px surface gaps between bands, hover gives the full-year
breakdown.

**B4. Calendar heatmap component.** A `CalendarHeat` (months x years grid,
single-hue ramp, colourbar legend with labelled ends) for high-water's flood
calendar and bushfire's seasonal heatmap. Cells get the same hover/focus
detail treatment as ScoreHeat.

**B5. Event-timeline component.** A `BubbleTimeline` (x time, y intensity,
size duration with a 3-step size legend, colour by ordered category) for the
marine-heatwave event record. Category colours from the validated ordinal
ramp, not four unrelated hues.

**B6. "View the data" link on every rail card,** jumping to the project's
sortable table, so the table twin is discoverable from the chart it backs.

## 5. Workstream C: per-project upgrades

Ordered by impact. Each item is a small, self-contained change to
`js/data.js` + `js/chartdata.js` (via the generator in Workstream E) once the
components from A and B exist.

**C1. swis-decarbonisation (biggest gap).** Hero: interactive fuel-mix
stacked area (B3), annotated with the coal-exit announcements. Add a coal vs
renewables crossover line chart (two series, direct-labelled endpoints, the
projected crossover year marked). Keep renewable share and intensity lines,
with the intensity trend labelled.

**C2. transition-risk.** Turn top facilities into a horizontal bar chart
(long facility names read flat, sorted by emissions, the top three
direct-labelled). Add sector trends as small multiples (B2) and the headroom
chart (diverging bars around zero using `--chart-pos`/`--chart-neg`). Annotate
the WA total line with the 2023 Safeguard reform mark.

**C3. bushfire-weather.** Hero: seasonal heatmap (B4). Add the season-span
chart (first/last Very High day per season as a range band: the season is
lengthening). Keep the two station lines as small multiples with a shared
y-scale and the FFDI >= 25 threshold as a labelled refline.

**C4. marine-heatwaves.** Hero: event bubble timeline (B5) with size legend.
Add the biggest-event zoom: observed SST line over the climatology line and
90th-percentile threshold, exceedance filled, "Ningaloo, Feb 2011" (or the
actual peak event) annotated. Keep MHW days/year with its 5-yr mean legend.

**C5. fremantle-high-water.** Hero: flood calendar (B4), the strongest single
image in the portfolio. Annotate the hours/year line with the 2021–22
cluster. The raw vs mean-adjusted grouped bar keeps its legend but gains the
takeaway as a direct label ("same storms, higher sea").

**C6. extreme-heat.** Replace six near-identical rail cards with two
small-multiples cards (B2): days >= 35C (Perth vs Hedland, shared scale) and
heatwave days (same). Keep TXX as one line with its record year annotated.
Grouped decade bars stay, colours moved to tokens.

**C7. sw-wa-rainfall.** Fold the three driver scatters (IOD, SAM, ENSO) into
one small-multiples card with r values shown consistently. Annotate the
step-change chart at 2000 and label the pre/post means directly ("1950–1999
mean", "2000–2024 mean"). HeatTable colours move to the validated diverging
tokens.

**C8. perth-water-security.** Annotate the 2001 step. Rebuild "rain fell 12%,
rivers fell 41%" as a paired-drop (dumbbell) view: two rows, before/after
dots, connecting line, the amplification stated once as a direct label. Add
quadrant shading to the elasticity scatter (dry-year quadrant tinted).

**C9. fremantle-sea-level.** Add the 95% band to the long series (the data
shape already supports `band`), annotate the era boundary used by the eras
bar, and add a zero refline to the 30-year rolling-rate chart so
acceleration reads instantly.

**C10. wheat-yields.** Annotate the drought years flagged by the analysis on
the yield chart (the static 04 chart already identifies them). If yield and
rainfall are ever shown together, index both to a common base on one axis,
never two scales.

**C11. wa-cyclones.** Already the flagship: add legend chips for the trend
line, and show the two wind records honestly on one chart (agency vs US
series as two labelled lines), since the update log says the ambiguity IS the
finding. Annotate Seroja (2021) on the annual-count chart. Consider a
"play through decades" step on the map as a later nicety.

**C12. aasb-s2-readiness.** Smallest changes: it already has the best
interaction model. Add a per-pillar mean row to ScoreHeat, and a three-tile
KPI row above it (one overall score per company) so the headline is readable
before the matrix.

## 6. Workstream D: static chart pipeline

**D1. Shared style module.** Extract `viz_style.py` (palette, rcParams,
credit, `save(fig, name)` writing 300 dpi PNG, direct-label helpers) and keep
it byte-identical across projects exactly like `stats_utils.py`, with the
same CI diff check added to `.github/workflows/tests.yml`.

**D2. House style refresh, applied by D1 everywhere at once:** drop top/right
spines, lighten the grid one step, sentence-case titles or no embedded title
at all (captions live in the README and the site), legend only when two or
more series, direct labels for single-series takeaways.

**D3. Chart-level fixes:**
- marine-heatwaves 02: add a size legend (three reference bubbles: 10, 30,
  60 days); re-step the category colours to the validated ordinal ramp.
- swis 01: lighten coal to a dark-but-not-black step, fold
  distillate/bio/other into "Other", order the legend to match the stack.
- cyclone 01: thin the basin bars to context grey so the WA-affecting line
  carries the story (emphasis, not two competing series).
- Everywhere: check labels do not collide after the restyle, re-render all
  PNGs, and re-run `tools/build-og.js` for any project whose hero changed.

## 7. Workstream E: plumbing that keeps charts honest

**E1. `tools/build-chartdata.py`.** One committed script that regenerates
`js/chartdata.js` from each project's committed CSVs (per-project extractor
functions, minified single-line output). `PROCEDURE.md` already demands
"edit it with a script": this makes the script real, versioned and reusable.

**E2. CI drift check.** A workflow step that runs E1 and fails if the
regenerated `chartdata.js` differs from the committed one, extending the
"every number traces back to tested code" guarantee to the site's charts.

**E3. Document the new chart shapes** (legend/marks/refline fields, area,
calendar, multiples, bubble types) in `PROCEDURE.md` step 2 so the next
project uses them without re-deciding anything.

## 8. Phasing and sequencing

| Phase | Contents | Ships as |
|---|---|---|
| 0 | A1–A5 (tokens, validation, legends, annotations, keyboard, formatting) | 1 PR, no visual regressions beyond colour corrections |
| 1 | B1–B6 (hero layout, small multiples, area, calendar heat, bubble timeline, data links) | 1–2 PRs, components land with the first project that uses them |
| 2a | C1–C4 (swis, transition, bushfire, marine heatwaves: the biggest story-to-page gaps) | 1 PR per project |
| 2b | C5–C8 (high-water, extreme heat, rainfall, water security) | 1 PR per project |
| 2c | C9–C12 (sea level, wheat, cyclones, AASB polish) | 1 PR per project |
| 3 | D1–D3 (shared matplotlib style + PNG refresh) and E1–E3 (chartdata generator + CI) | 2 PRs |

Phase 3 can run in parallel with phase 2; nothing in it blocks the site work.
Every phase ends with `npm run build`, a render check of the affected pages
in both themes at 360px and 1280px, and the no-em-dash check.

## 9. Acceptance checklist (the definition of "better")

A chart is done when:

- [ ] Its form matches the reader's job (magnitude, trend, polarity, or a
      stat tile if the story is one number).
- [ ] Every mark on it is identified: legend for 2+ series, direct labels on
      the series that carry the finding, axis titles on both axes.
- [ ] The written finding is visible on the chart itself (annotation, refline
      or direct label), not only in the caption.
- [ ] Colours come from the validated tokens, in both light and dark mode,
      and no meaning is carried by colour alone.
- [ ] Values are reachable by keyboard and by the data table, not only by
      mouse hover.
- [ ] Uncertainty computed by the analysis (bands, p-values, n per group) is
      shown or stated on the chart.
- [ ] The numbers behind it regenerate from committed CSVs via
      `tools/build-chartdata.py` and CI proves it.
