# Chart colours

The palette every chart draws from, and the checks it has to pass. If you change
a chart colour, re-run the validation below and update this note. The rule the
whole portfolio follows: **colour is computed, not eyeballed.**

## The tokens (defined in `tokens/colors.css`, dark overrides in `portfolio.css`)

| Token | Light | Dark | Job |
|-------|-------|------|-----|
| `--chart-1` | `#2A78D6` blue | `#3987E5` | Categorical slot 1 (also the default single-series line) |
| `--chart-2` | `#008300` green | `#008300` | Categorical slot 2 |
| `--chart-3` | `#E87BA4` magenta | `#D55181` | Categorical slot 3 |
| `--chart-4` | `#EDA100` yellow | `#C98500` | Categorical slot 4 |
| `--chart-5` | `#1BAF7A` aqua | `#199E70` | Categorical slot 5 |
| `--chart-6` | `#EB6834` orange | `#D95926` | Categorical slot 6 |
| `--chart-pos` | `#2A78D6` (cool pole) | `#3987E5` | Above baseline / wetter / cooler |
| `--chart-neg` | `#EB6834` (warm pole) | `#D95926` | Below baseline / drier / hotter |
| `--chart-trend` | green (`--leaf`) | green (`--leaf`) | OLS / reference trend annotation |
| `--chart-context` | `--neutral-400` | `--neutral-600` | De-emphasised (grey) context series |
| `--chart-band` | blue @ 14% | blue @ 20% | Confidence-interval fill |
| `--chart-mark` | `--neutral-500` | `--neutral-500` | Event marker line |
| `--chart-dot-ring` | `--surface-card` | `--surface-card` | Ring around the active point |

Categorical slots are assigned in **fixed order, never cycled**. A 7th series is
never a generated hue: fold the tail into "Other", facet into small multiples,
or use composite encoding.

## Source

The six categorical hues are the data-viz skill's reference categorical palette
(slots 1 and 2 are blue and green, which match this site's own accent and leaf
brand hues). The dark column is the same six hues stepped for the dark surface,
not a separate palette.

## Validation (re-run before changing any chart colour)

Run the data-viz validator against **this site's own surfaces** (white card in
light mode, `#181E26` in dark):

```
# light
node validate_palette.js "#2a78d6,#008300,#e87ba4,#eda100,#1baf7a,#eb6834" --mode light --surface "#FFFFFF"
# dark
node validate_palette.js "#3987e5,#008300,#d55181,#c98500,#199e70,#d95926" --mode dark --surface "#181E26"
```

Result recorded (all hard gates pass in both modes):

- Lightness band: pass (6/6 inside the mode band).
- Chroma floor: pass (6/6 >= 0.1).
- Colour-vision separation: worst adjacent pair ΔE 9.1 light / 8.4 dark (target
  >= 8, OKLab x100).
- Normal-vision floor: worst adjacent ΔE 19.6 light / 19.3 dark (floor 15).
- Contrast vs surface: dark passes 3:1 for all six. In **light mode** the
  magenta, yellow and aqua slots sit below 3:1 as small marks on white, so the
  **relief rule** applies: any chart using them keeps visible direct labels or
  its data-table twin. Every chart on the site already carries a sortable table,
  so this is satisfied by construction; keep it that way.

The all-pairs pairlist (scatter, bubble, choropleth) cannot clear the floors at
six slots. Those chart forms cap at the first four slots plus secondary
encoding; past four, fold to "Other" or facet.
