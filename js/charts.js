/* Hand-built, dependency-free interactive SVG charts for the project stories. */
(function () {
  const { useState } = React;
  const W = 540, H = 330, M = { l: 48, r: 16, t: 16, b: 42 };
  const IW = W - M.l - M.r, IH = H - M.t - M.b;
  const round = (n, d = 1) => { const p = Math.pow(10, d); return Math.round(n * p) / p; };

  /* Shared number format: thousands separators above 1000, one decimal below,
     unit appended once. Used by tooltips and direct labels so every value on
     every chart reads the same way. */
  function fmt(v, unit) {
    if (v == null || isNaN(v)) return "";
    const n = Math.abs(v) >= 1000 ? Math.round(v).toLocaleString("en-US") : round(v, 1);
    return n + (unit || "");
  }

  /* One keyboard model for every chart: left/right (or up/down) walk the marks,
     Home/End jump to the ends, Escape clears. Returns an onKeyDown handler that
     drives the same `hi` state the mouse hover uses, so focus and hover show the
     identical tooltip. */
  function arrowKeys(count, hi, setHi) {
    return (e) => {
      if (!count) return;
      const cur = hi == null ? -1 : hi;
      if (e.key === "ArrowRight" || e.key === "ArrowDown") { setHi(Math.min(count - 1, cur + 1)); e.preventDefault(); }
      else if (e.key === "ArrowLeft" || e.key === "ArrowUp") { setHi(Math.max(0, (cur < 0 ? count : cur) - 1)); e.preventDefault(); }
      else if (e.key === "Home") { setHi(0); e.preventDefault(); }
      else if (e.key === "End") { setHi(count - 1); e.preventDefault(); }
      else if (e.key === "Escape") { setHi(null); }
    };
  }

  /* Event markers (labelled vertical lines at a named x) and a reference line
     (a labelled horizontal threshold). Shared by the line and scatter charts so
     the written finding, "the rivers stepped down in 2001", can be drawn on the
     chart that shows it. `nudgeEnd` keeps a right-edge label from overflowing. */
  function Marks({ marks, xs, refline, ys, plotTop, plotBottom }) {
    if (!marks && !refline) return null;
    return React.createElement("g", { style: { pointerEvents: "none" } },
      (marks || []).map((mk, i) => {
        const x = xs(mk.x);
        const nearRight = x > W - 70;
        return React.createElement("g", { key: "mk" + i },
          React.createElement("line", { className: "chart__mark", x1: x, x2: x, y1: plotTop, y2: plotBottom }),
          mk.label && React.createElement("text", {
            x: x + (nearRight ? -4 : 4), y: plotTop + 11, textAnchor: nearRight ? "end" : "start",
            className: "chart__mark-label",
          }, mk.label)
        );
      }),
      refline && React.createElement("g", null,
        React.createElement("line", { className: "chart__refline", x1: M.l, x2: M.l + IW, y1: ys(refline.y), y2: ys(refline.y) }),
        refline.label && React.createElement("text", { x: M.l + IW - 3, y: ys(refline.y) - 4, textAnchor: "end", className: "chart__refline-label" }, refline.label)
      )
    );
  }

  function ticks(min, max, n = 4) {
    if (min === max) { min -= 1; max += 1; }
    const span = max - min, step0 = span / n, mag = Math.pow(10, Math.floor(Math.log10(step0)));
    const norm = step0 / mag, step = mag * (norm >= 5 ? 5 : norm >= 2 ? 2 : norm >= 1 ? 1 : 0.5);
    const out = []; for (let v = Math.ceil(min / step) * step; v <= max + 1e-9; v += step) out.push(round(v, 3));
    return out;
  }
  // pad a [min,max] domain a little
  function domain(vals, padFrac = 0.08, includeZero = false) {
    let lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals);
    if (includeZero) { lo = Math.min(lo, 0); hi = Math.max(hi, 0); }
    const pad = (hi - lo) * padFrac || 1; return [lo - pad, hi + pad];
  }

  /* viewBox units per rendered CSS pixel, so SVG text can be drawn at a
     constant on-screen size whether the chart is squeezed into a phone rail
     card or stretched across a wide solo card. Charts publish it as the
     `--ck` CSS variable; text either uses calc(...) in the stylesheet or an
     inline fontSize multiplied by this factor. */
  function useChartScale(ref, base) {
    const [k, setK] = React.useState(1);
    React.useEffect(() => {
      const el = ref.current;
      if (!el || typeof ResizeObserver === "undefined") return;
      const ro = new ResizeObserver((entries) => {
        const w = entries[0].contentRect.width;
        if (w > 40) setK(Math.round(Math.min(2.2, Math.max(0.7, base / w)) * 100) / 100);
      });
      ro.observe(el);
      return () => ro.disconnect();
    }, [base]);
    return k;
  }

  /* Tooltip drawn inside the SVG; sized in viewBox units scaled by `k` so it
     reads at the same size on screen regardless of the chart's render width. */
  function Tip({ x, y, lines, k = 1 }) {
    if (!lines) return null;
    const w = (Math.max.apply(null, lines.map((l) => l.length)) * 6.4 + 16) * k;
    const h = (lines.length * 15 + 12) * k;
    let tx = x - w / 2; tx = Math.max(4, Math.min(tx, W - 4 - w));
    let ty = y - h - 12 * k; if (ty < 4) ty = y + 14 * k;
    return (
      React.createElement("g", { className: "chart__tip", style: { pointerEvents: "none" } },
        React.createElement("rect", { x: tx, y: ty, width: w, height: h, rx: 7 * k, className: "chart__tip-bg" }),
        lines.map((l, i) => React.createElement("text", {
          key: i, x: tx + w / 2, y: ty + (17 + i * 15) * k, textAnchor: "middle",
          className: i === 0 ? "chart__tip-h" : "chart__tip-t",
          style: { fontSize: 11 * k },
        }, l))
      )
    );
  }

  function Axes({ xTicks, yTicks, xs, ys, xfmt, yfmt, ylabel }) {
    return (
      React.createElement("g", null,
        yTicks.map((t, i) => React.createElement("g", { key: "y" + i },
          React.createElement("line", { x1: M.l, x2: M.l + IW, y1: ys(t), y2: ys(t), className: "chart__grid" }),
          React.createElement("text", { x: M.l - 8, y: ys(t) + 3.5, textAnchor: "end", className: "chart__tick" }, yfmt ? yfmt(t) : t)
        )),
        xTicks.map((t, i) => React.createElement("text", { key: "x" + i, x: xs(t), y: H - M.b + 18, textAnchor: "middle", className: "chart__tick" }, xfmt ? xfmt(t) : t)),
        React.createElement("line", { x1: M.l, x2: M.l + IW, y1: M.t + IH, y2: M.t + IH, className: "chart__axis" }),
        /* Horizontal label above the axis: a rotated label collides with the
           tick numbers once they are scaled up on small charts. */
        ylabel && React.createElement("text", { x: 4, y: 13, textAnchor: "start", className: "chart__axlabel" }, ylabel)
      )
    );
  }

  function Svg({ children, label, refEl, k = 1, after, onKeyDown }) {
    const svgProps = { viewBox: `0 0 ${W} ${H}`, className: "chart__svg", role: "img", "aria-label": label };
    /* When a chart passes a key handler it is operable: make the SVG a focus
       stop and let arrow keys reach every value the mouse can. */
    if (onKeyDown) { svgProps.tabIndex = 0; svgProps.onKeyDown = onKeyDown; }
    return React.createElement("div", { className: "chart", ref: refEl, style: { "--ck": k } },
      React.createElement("svg", svgProps, children),
      after || null
    );
  }

  /* ------------------------------------------------------------- LineChart */
  function LineChart({ data, label }) {
    const [hi, setHi] = useState(null);
    const wrapRef = React.useRef(null);
    const ck = useChartScale(wrapRef, W);
    const pts = data.points;
    const xv = pts.map((p) => p[0]);
    const allY = pts.map((p) => p[1])
      .concat(data.overlay ? data.overlay.map((p) => p[1]) : [])
      .concat(data.band ? data.band.reduce((a, b) => a.concat([b[1], b[2]]), []) : [])
      .concat(data.trend ? [data.trend[1], data.trend[3]] : [])
      .concat(data.bars ? [0] : []);
    const [x0, x1] = domain(xv, 0.02), [y0, y1] = domain(allY, 0.1, data.bars);
    const xs = (v) => M.l + (v - x0) / (x1 - x0) * IW;
    const ys = (v) => M.t + IH - (v - y0) / (y1 - y0) * IH;
    const line = (arr) => arr.map((p, i) => (i ? "L" : "M") + xs(p[0]) + " " + ys(p[1])).join(" ");
    const yfmt = (t) => round(t, t % 1 ? 1 : 0);
    const tip = hi != null && pts[hi]
      ? React.createElement(Tip, { x: xs(pts[hi][0]), y: ys(pts[hi][1]), lines: [String(pts[hi][0]), fmt(pts[hi][1], data.unit)], k: ck }) : null;
    const marks = (data.marks || []).filter((m) => xs(m.x) >= M.l - 1 && xs(m.x) <= M.l + IW + 1);

    /* Legend: shown only when there is more than a single line to name. A lone
       series needs no legend box, the title names it. */
    const leg = [];
    if (data.bars) {
      if (data.posLabel) leg.push({ sw: "var(--chart-pos)", label: data.posLabel });
      if (data.negLabel) leg.push({ sw: "var(--chart-neg)", label: data.negLabel });
    } else {
      leg.push({ ln: "chart__legend-ln", label: data.seriesLabel || "Observed" });
    }
    if (data.overlay) leg.push({ ln: "chart__legend-ln chart__legend-ln--mean", label: data.overlayLabel || "Rolling mean" });
    if (data.trend) leg.push({ ln: "chart__legend-ln chart__legend-ln--trend", label: data.trendLabel || "Trend" });
    if (data.pre || data.post) leg.push({ ln: "chart__legend-ln chart__legend-ln--step", label: data.stepLabel || "Period mean" });
    if (data.band) leg.push({ band: true, label: data.bandLabel || "95% range" });
    const legend = leg.length >= 2 ? React.createElement("div", { className: "chart__legend" },
      leg.map((e, i) => React.createElement("span", { key: i },
        e.band ? React.createElement("span", { className: "chart__legend-band" })
          : e.sw ? React.createElement("span", { className: "chart__legend-sw", style: { background: e.sw } })
          : React.createElement("span", { className: e.ln }),
        e.label))) : null;

    return React.createElement(Svg, { label, refEl: wrapRef, k: ck, after: legend, onKeyDown: arrowKeys(pts.length, hi, setHi) },
      React.createElement(Axes, { xTicks: ticks(x0, x1, 4).filter((t) => t >= Math.min.apply(null, xv) - 1 && t <= Math.max.apply(null, xv) + 1), yTicks: ticks(y0, y1, 4), xs, ys, xfmt: (t) => Math.round(t), yfmt, ylabel: data.ylabel }),
      data.band && React.createElement("path", { className: "chart__band", d: "M" + data.band.map((b) => xs(b[0]) + " " + ys(b[1])).join(" L ") + " L " + data.band.slice().reverse().map((b) => xs(b[0]) + " " + ys(b[2])).join(" L ") + " Z" }),
      data.bars && pts.map((p, i) => React.createElement("rect", {
        key: i, x: xs(p[0]) - Math.max(1.5, IW / pts.length / 2.4), y: Math.min(ys(p[1]), ys(0)), width: Math.max(3, IW / pts.length - 1.5), height: Math.abs(ys(p[1]) - ys(0)),
        className: "chart__bar2 " + (p[1] >= 0 ? "is-pos" : "is-neg") + (hi === i ? " is-hi" : ""),
      })),
      !data.bars && React.createElement("path", { className: "chart__line chart__line--draw", d: line(pts), pathLength: 1 }),
      data.overlay && React.createElement("path", { className: "chart__line chart__line--mean", d: line(data.overlay) }),
      data.trend && React.createElement("line", { className: "chart__trend", x1: xs(data.trend[0]), y1: ys(data.trend[1]), x2: xs(data.trend[2]), y2: ys(data.trend[3]) }),
      data.pre && React.createElement("line", { className: "chart__step", x1: xs(data.pre.x0), y1: ys(data.pre.y), x2: xs(data.pre.x1), y2: ys(data.pre.y) }),
      data.post && React.createElement("line", { className: "chart__step", x1: xs(data.post.x0), y1: ys(data.post.y), x2: xs(data.post.x1), y2: ys(data.post.y) }),
      React.createElement(Marks, { marks, refline: data.refline, xs, ys, plotTop: M.t, plotBottom: M.t + IH }),
      data.xlabel && React.createElement("text", { x: M.l + IW / 2, y: H - 4, textAnchor: "middle", className: "chart__axlabel" }, data.xlabel),
      hi != null && pts[hi] && React.createElement("line", { className: "chart__guide", x1: xs(pts[hi][0]), x2: xs(pts[hi][0]), y1: M.t, y2: M.t + IH }),
      hi != null && pts[hi] && !data.bars && React.createElement("circle", { className: "chart__dot", cx: xs(pts[hi][0]), cy: ys(pts[hi][1]), r: 4 }),
      pts.map((p, i) => React.createElement("rect", {
        key: "h" + i, x: xs(p[0]) - IW / pts.length / 2, y: M.t, width: IW / pts.length, height: IH, fill: "transparent",
        onMouseEnter: () => setHi(i), onMouseLeave: () => setHi(null),
        onClick: () => setHi(i),
      })),
      tip
    );
  }

  /* -------------------------------------------------------------- BarChart */
  function BarChart({ data, label }) {
    const [hi, setHi] = useState(null);
    const wrapRef = React.useRef(null);
    const ck = useChartScale(wrapRef, W);
    const bars = data.bars, grouped = data.keys && data.keys.length > 1;
    const maxV = Math.max.apply(null, bars.reduce((a, b) => grouped ? a.concat(data.keys.map((k) => b[k.k])) : a.concat([b.value]), []));
    const y1 = maxV * 1.12;
    const ys = (v) => M.t + IH - v / y1 * IH;
    const band = IW / bars.length, bw = band * 0.62;
    const yfmt = (t) => round(t, 0);
    function lines(b) {
      if (grouped) return [b.label].concat(data.keys.map((k) => k.label + ": " + fmt(b[k.k], data.unit)));
      const ex = []; if (b.n != null) ex.push("n = " + b.n); if (b.median != null) ex.push("median " + b.median + " kt"); if (b.pres != null) ex.push(b.pres + " hPa"); if (b.cat3 != null) ex.push("Cat 3+: " + b.cat3 + "%");
      return [b.label, fmt(b.value, data.unit)].concat(ex);
    }
    const hb = hi != null ? bars[hi] : null;
    // Legend lives outside the SVG so it can never collide with tall bars.
    const legend = grouped ? React.createElement("div", { className: "chart__legend" },
      data.keys.map((k, i) => React.createElement("span", { key: i },
        React.createElement("span", { className: "chart__legend-sw", style: { background: k.color || "var(--accent)" } }), k.label))) : null;
    return React.createElement(Svg, { label, refEl: wrapRef, k: ck, after: legend, onKeyDown: arrowKeys(bars.length, hi, setHi) },
      React.createElement(Axes, { xTicks: [], yTicks: ticks(0, y1, 4), xs: () => 0, ys, yfmt, ylabel: data.ylabel }),
      data.xlabel && React.createElement("text", { x: M.l + IW / 2, y: H - 3, textAnchor: "middle", className: "chart__axlabel" }, data.xlabel),
      bars.map((b, bi) => {
        const cx = M.l + band * bi + band / 2;
        const segs = grouped ? data.keys : [{ k: "value", color: "var(--accent)" }];
        const sw = bw / segs.length;
        return React.createElement("g", {
          key: bi, onMouseEnter: () => setHi(bi), onMouseLeave: () => setHi(null),
          onClick: () => setHi(bi),
        },
          segs.map((k, ki) => {
            const v = grouped ? b[k.k] : b.value;
            return React.createElement("rect", {
              key: ki, x: cx - bw / 2 + ki * sw, y: ys(v), width: sw - (grouped ? 2 : 0), height: M.t + IH - ys(v),
              className: "chart__bar chart__bar--draw" + (hi === bi ? " is-hi" : ""), style: { fill: k.color || "var(--accent)" },
            });
          }),
          React.createElement("text", { x: cx, y: H - M.b + 18, textAnchor: "middle", className: "chart__tick" }, b.label)
        );
      }),
      hb && React.createElement(Tip, { x: M.l + band * hi + band / 2, y: ys(grouped ? Math.max.apply(null, data.keys.map((k) => hb[k.k])) : hb.value), lines: lines(hb), k: ck })
    );
  }

  /* ------------------------------------------------------------ ScatterChart */
  function ScatterChart({ data, label }) {
    const [hi, setHi] = useState(null);
    const wrapRef = React.useRef(null);
    const ck = useChartScale(wrapRef, W);
    const pts = data.points;
    const [x0, x1] = domain(pts.map((p) => p[0]), 0.08), [y0, y1] = domain(pts.map((p) => p[1]), 0.1);
    const xs = (v) => M.l + (v - x0) / (x1 - x0) * IW;
    const ys = (v) => M.t + IH - (v - y0) / (y1 - y0) * IH;
    const hp = hi != null ? pts[hi] : null;
    return React.createElement(Svg, { label, refEl: wrapRef, k: ck, onKeyDown: arrowKeys(pts.length, hi, setHi) },
      React.createElement(Axes, { xTicks: ticks(x0, x1, 4), yTicks: ticks(y0, y1, 4), xs, ys, xfmt: (t) => round(t, 1), yfmt: (t) => round(t, 0), ylabel: data.ylabel }),
      data.xlabel && React.createElement("text", { x: M.l + IW / 2, y: H - 4, textAnchor: "middle", className: "chart__axlabel" }, data.xlabel),
      React.createElement(Marks, { marks: (data.marks || []).filter((m) => xs(m.x) >= M.l - 1 && xs(m.x) <= M.l + IW + 1), refline: data.refline, xs, ys, plotTop: M.t, plotBottom: M.t + IH }),
      data.trend && React.createElement("line", { className: "chart__trend", x1: xs(data.trend[0]), y1: ys(data.trend[1]), x2: xs(data.trend[2]), y2: ys(data.trend[3]) }),
      data.r != null && React.createElement("text", { x: M.l + IW - 4, y: M.t + 14, textAnchor: "end", className: "chart__rnote" }, "r = " + data.r),
      pts.map((p, i) => React.createElement("circle", {
        key: i, cx: xs(p[0]), cy: ys(p[1]), r: hi === i ? 6 : 3.6, className: "chart__pt chart__pt--draw" + (hi === i ? " is-hi" : ""),
        // transparent stroke widens the hover/tap target without changing the mark
        style: { animationDelay: (i * 12) + "ms", stroke: "transparent", strokeWidth: 14 },
        onMouseEnter: () => setHi(i), onMouseLeave: () => setHi(null),
        onClick: () => setHi(i),
      })),
      hp && React.createElement(Tip, { x: xs(hp[0]), y: ys(hp[1]), lines: [hp[2] != null ? String(hp[2]) : "", fmt(hp[1]) + " · " + round(hp[0], 2)].filter(Boolean), k: ck })
    );
  }

  /* -------------------------------------------------------------- HeatTable */
  function heatColor(v, maxAbs) {
    if (v == null) return "var(--bg-muted)";
    const t = Math.max(-1, Math.min(1, v / maxAbs));
    if (t < 0) { const a = (0.15 + 0.65 * -t).toFixed(2); return `rgba(255,92,57,${a})`; }   // dry = warm
    const a = (0.15 + 0.65 * t).toFixed(2); return `rgba(31,169,199,${a})`;                   // wet = blue
  }
  function HeatTable({ data }) {
    const flat = data.matrix.reduce((a, r) => a.concat(r.filter((v) => v != null)), []);
    const maxAbs = Math.max.apply(null, flat.map(Math.abs));
    return React.createElement("div", { className: "heat" },
      React.createElement("div", { className: "heat__grid", style: { gridTemplateColumns: `minmax(96px,1.2fr) repeat(${data.decades.length}, 1fr)` } },
        React.createElement("div", { className: "heat__corner" }),
        data.decades.map((d) => React.createElement("div", { key: d, className: "heat__colh" }, d)),
        data.stations.map((s, si) => [
          React.createElement("div", { key: "s" + si, className: "heat__rowh" }, s),
          data.matrix[si].map((v, di) => React.createElement("div", {
            key: si + "-" + di, className: "heat__cell", style: { background: heatColor(v, maxAbs) },
            title: `${s} · ${data.decades[di]}: ${v == null ? "no data" : (v > 0 ? "+" : "") + v + "%"}`,
          }, v == null ? "" : (v > 0 ? "+" : "") + Math.round(v))),
        ])
      ),
      React.createElement("div", { className: "heat__legend" }, "Cool-season rainfall vs each station's 1950–74 average · ", React.createElement("span", { className: "heat__sw heat__sw--dry" }), " drier ", React.createElement("span", { className: "heat__sw heat__sw--wet" }), " wetter")
    );
  }

  /* --------------------------------------------------------------- MapChart */
  /* Plasma-like ramp: lightness rises monotonically with wind speed, so
     "brighter = stronger" holds even for colour-blind readers, and the
     strongest storms glow against the dark basemap. */
  const WIND_STOPS = [[20, "#3b4568"], [50, "#7e4e90"], [80, "#b4559b"], [105, "#e0637c"], [125, "#f88f4d"], [150, "#fdc746"]];
  const SEVERE_KT = 64;   // highlight threshold for the default view
  function hx(h) { return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]; }
  function windColor(w) {
    if (!w) return "#9aa7b8";
    for (let i = 0; i < WIND_STOPS.length - 1; i++) {
      const [w0, c0] = WIND_STOPS[i], [w1, c1] = WIND_STOPS[i + 1];
      if (w <= w1 || i === WIND_STOPS.length - 2) {
        const t = Math.max(0, Math.min(1, (w - w0) / (w1 - w0))), a = hx(c0), b = hx(c1);
        return `rgb(${Math.round(a[0] + (b[0] - a[0]) * t)},${Math.round(a[1] + (b[1] - a[1]) * t)},${Math.round(a[2] + (b[2] - a[2]) * t)})`;
      }
    }
    return WIND_STOPS[WIND_STOPS.length - 1][1];
  }
  function MapChart({ data, label }) {
    const [hi, setHi] = useState(null);
    const [year, setYear] = useState(0);   // 0 = all seasons
    const [minW, setMinW] = useState(0);   // minimum peak wind (kt); 0 = any
    const wrapRef = React.useRef(null);
    const win = data.win, VW = 600, VH = 660, m = 16;
    const ck = useChartScale(wrapRef, VW);
    const cosMid = Math.cos((win.lat0 + win.lat1) / 2 * Math.PI / 180);
    const lonMid = (win.lon0 + win.lon1) / 2, latMid = (win.lat0 + win.lat1) / 2;
    const sc = Math.min((VW - 2 * m) / ((win.lon1 - win.lon0) * cosMid), (VH - 2 * m) / (win.lat1 - win.lat0));
    const px = (lo) => VW / 2 + (lo - lonMid) * cosMid * sc;
    const py = (la) => VH / 2 - (la - latMid) * sc;
    const path = (pts) => pts.map((p, i) => (i ? "L" : "M") + px(p[0]).toFixed(1) + " " + py(p[1]).toFixed(1)).join(" ");
    const lonLines = [110, 115, 120, 125, 130], latLines = [-10, -15, -20, -25, -30, -35];

    const ys = data.tracks.map((t) => t.y);
    const minY = Math.min.apply(null, ys), maxY = Math.max.apply(null, ys);
    const total = data.tracks.length;
    const matches = (t) => (year === 0 || t.y === year) && (t.w || 0) >= minW;
    const nVis = data.tracks.reduce((a, t) => a + (matches(t) ? 1 : 0), 0);
    const filtered = year !== 0 || minW !== 0;
    const hv = (hi != null && matches(data.tracks[hi])) ? data.tracks[hi] : null;
    const countTxt = nVis === 0 ? "no storms match these filters"
      : !filtered ? total + " storms within 500 km · " + minY + "–" + maxY
      : nVis + " of " + total + " storms shown";

    const slider = (id, lbl, valTxt, attrs) => React.createElement("div", { className: "map__ctrl" },
      React.createElement("div", { className: "map__ctrl-top" },
        React.createElement("label", { className: "map__ctrl-l", htmlFor: id }, lbl),
        React.createElement("span", { className: "map__ctrl-v" }, valTxt)
      ),
      React.createElement("input", Object.assign({ id, type: "range", className: "map__slider" }, attrs))
    );

    return React.createElement("div", { className: "chart", ref: wrapRef, style: { "--ck": ck } },
      React.createElement("div", { className: "map__controls" },
        slider("map-year", "Season", year === 0 ? "All seasons" : String(year), {
          min: minY - 1, max: maxY, step: 1, value: year === 0 ? minY - 1 : year,
          "aria-label": "Filter storms by season",
          onChange: (e) => { const v = +e.target.value; setYear(v < minY ? 0 : v); },
        }),
        slider("map-wind", "Min peak wind", minW === 0 ? "Any strength" : "≥ " + minW + " kt", {
          min: 0, max: 130, step: 5, value: minW,
          "aria-label": "Filter storms by minimum peak wind",
          onChange: (e) => setMinW(+e.target.value),
        }),
        filtered && React.createElement("button", {
          type: "button", className: "map__reset",
          onClick: () => { setYear(0); setMinW(0); },
        }, "Reset")
      ),
      React.createElement("svg", {
        viewBox: `0 0 ${VW} ${VH}`, className: "chart__svg map__svg", role: "img", "aria-label": label,
        onClick: () => setHi(null),
      },
        lonLines.map((lo) => React.createElement("line", { key: "lo" + lo, x1: px(lo), x2: px(lo), y1: py(win.lat1), y2: py(win.lat0), className: "map__grat" })),
        latLines.map((la) => React.createElement("line", { key: "la" + la, x1: px(win.lon0), x2: px(win.lon1), y1: py(la), y2: py(la), className: "map__grat" })),
        latLines.map((la) => React.createElement("text", { key: "lat" + la, x: px(win.lon0) + 3, y: py(la) - 3, className: "map__grat-label" }, Math.abs(la) + "°S")),
        React.createElement("path", { d: path(data.coast), className: "map__coast" }),
        data.tracks.map((t, i) => {
          const vis = matches(t);
          /* Default view: severe storms in full colour, the weak majority as
             faint grey context. Any slider filter switches to showing every
             match in colour. */
          const context = !filtered && (t.w || 0) < SEVERE_KT && hi !== i;
          const cls = "map__track" + (!vis ? " is-hidden" : hi === i ? " is-hi" : hi != null ? " is-dim" : context ? " is-context" : "");
          return React.createElement("path", {
            key: i, d: path(t.p), fill: "none",
            stroke: context ? "#5b6880" : windColor(t.w),
            strokeWidth: hi === i ? 3 : context ? 1 : 1.7,
            className: cls, style: { pointerEvents: "none" },
          });
        }),
        data.cities.map((c, i) => React.createElement("g", { key: "c" + i },
          React.createElement("circle", { cx: px(c.lo), cy: py(c.la), r: 3, className: "map__city" }),
          React.createElement("text", { x: px(c.lo) + 6, y: py(c.la) + 3.5, className: "map__city-label" }, c.n)
        )),
        /* Invisible fat strokes on top: mouse and touch targets for the thin
           tracks. Click/tap pins a storm; tapping open water clears it. */
        data.tracks.map((t, i) => matches(t) && React.createElement("path", {
          key: "hit" + i, d: path(t.p), fill: "none", stroke: "transparent", strokeWidth: 10,
          style: { pointerEvents: "stroke", cursor: "pointer" },
          onMouseEnter: () => setHi(i), onMouseLeave: () => setHi(null),
          onClick: (e) => { e.stopPropagation(); setHi(i); },
        })),
        hv && React.createElement("g", { style: { pointerEvents: "none" } },
          React.createElement("rect", { x: m, y: m, width: 210 * ck, height: 48 * ck, rx: 8 * ck, className: "map__info-bg" }),
          React.createElement("text", { x: m + 13 * ck, y: m + 21 * ck, className: "map__info-h", style: { fontSize: 14 * ck } }, hv.n + " · " + hv.y),
          React.createElement("text", { x: m + 13 * ck, y: m + 38 * ck, className: "map__info-t", style: { fontSize: 12 * ck } }, "peak " + hv.w + " kt")
        ),
        React.createElement("text", { x: VW - m, y: VH - m, textAnchor: "end", className: "map__count" }, countTxt)
      ),
      React.createElement("div", { className: "map__legend" },
        React.createElement("span", { className: "map__legend-l" }, "Peak wind (kt)"),
        React.createElement("span", { className: "map__scale" },
          React.createElement("span", { className: "map__ramp" }),
          React.createElement("span", { className: "map__scale-ticks" },
            WIND_STOPS.map((s) => React.createElement("span", { key: s[0] }, s[0])))
        ),
        !filtered && React.createElement("span", { className: "map__legend-l" }, "severe (≥ " + SEVERE_KT + " kt) in colour, weaker in grey")
      )
    );
  }

  /* ---------------------------------------------------------- RainMapChart */
  /* A map of south-west WA: each weather station is a dot whose colour and
     size show how far that decade's cool-season rain sat below (red) or
     above (blue) the 1950s baseline. Drag the decade slider to watch the
     drying deepen and spread, the rainfall analogue of the storm-track map. */
  function rainColor(v, maxAbs) {
    if (v == null) return "#9aa7b8";
    const t = Math.max(-1, Math.min(1, v / maxAbs));
    const grey = [150, 167, 184];
    const mix = (a, b, k) => Math.round(a + (b - a) * k);
    const tgt = t < 0 ? [255, 92, 57] : [31, 169, 199];   // drier = warm, wetter = blue
    const k = 0.3 + 0.7 * Math.abs(t);
    return `rgb(${mix(grey[0], tgt[0], k)},${mix(grey[1], tgt[1], k)},${mix(grey[2], tgt[2], k)})`;
  }
  function RainMapChart({ data, label }) {
    const [hi, setHi] = useState(null);
    const [di, setDi] = useState(data.decades.length - 1);   // default = latest decade
    const wrapRef = React.useRef(null);
    const win = data.win, VW = 620, VH = 500, m = 16;
    const ck = useChartScale(wrapRef, VW);
    const cosMid = Math.cos((win.lat0 + win.lat1) / 2 * Math.PI / 180);
    const lonMid = (win.lon0 + win.lon1) / 2, latMid = (win.lat0 + win.lat1) / 2;
    const sc = Math.min((VW - 2 * m) / ((win.lon1 - win.lon0) * cosMid), (VH - 2 * m) / (win.lat1 - win.lat0));
    const px = (lo) => VW / 2 + (lo - lonMid) * cosMid * sc;
    const py = (la) => VH / 2 - (la - latMid) * sc;
    const path = (pts) => pts.map((p, i) => (i ? "L" : "M") + px(p[0]).toFixed(1) + " " + py(p[1]).toFixed(1)).join(" ");
    const lonLines = [114, 116, 118, 120, 122], latLines = [-30, -32, -34];
    const allVals = data.stations.reduce((a, s) => a.concat(s.dec.filter((v) => v != null)), []);
    const maxAbs = Math.max.apply(null, allVals.map(Math.abs));
    const radius = (v) => 6 + Math.abs(v || 0) / maxAbs * 9;
    const decVals = data.stations.map((s) => s.dec[di]).filter((v) => v != null);
    const regionMean = decVals.length ? decVals.reduce((a, b) => a + b, 0) / decVals.length : null;
    const hv = hi != null ? data.stations[hi] : null;

    return React.createElement("div", { className: "chart", ref: wrapRef, style: { "--ck": ck } },
      React.createElement("div", { className: "map__controls" },
        React.createElement("div", { className: "map__ctrl" },
          React.createElement("div", { className: "map__ctrl-top" },
            React.createElement("label", { className: "map__ctrl-l", htmlFor: "rain-decade" }, "Decade"),
            React.createElement("span", { className: "map__ctrl-v" }, data.decades[di])
          ),
          React.createElement("input", {
            id: "rain-decade", type: "range", className: "map__slider",
            min: 0, max: data.decades.length - 1, step: 1, value: di,
            "aria-label": "Choose a decade to map", onChange: (e) => setDi(+e.target.value),
          })
        ),
        di !== data.decades.length - 1 && React.createElement("button", {
          type: "button", className: "map__reset", onClick: () => setDi(data.decades.length - 1),
        }, "Latest")
      ),
      React.createElement("svg", { viewBox: `0 0 ${VW} ${VH}`, className: "chart__svg map__svg", role: "img", "aria-label": label },
        lonLines.map((lo) => React.createElement("line", { key: "lo" + lo, x1: px(lo), x2: px(lo), y1: py(win.lat1), y2: py(win.lat0), className: "map__grat" })),
        latLines.map((la) => React.createElement("line", { key: "la" + la, x1: px(win.lon0), x2: px(win.lon1), y1: py(la), y2: py(la), className: "map__grat" })),
        latLines.map((la) => React.createElement("text", { key: "lat" + la, x: px(win.lon1) - 4, y: py(la) - 3, textAnchor: "end", className: "map__grat-label" }, Math.abs(la) + "°S")),
        React.createElement("path", { d: path(data.coast), className: "map__coast" }),
        data.cities.map((c, i) => React.createElement("g", { key: "c" + i },
          React.createElement("circle", { cx: px(c.lo), cy: py(c.la), r: 2.5, className: "map__city" }),
          React.createElement("text", { x: px(c.lo) + 6, y: py(c.la) + 3.5, className: "map__city-label" }, c.n)
        )),
        data.stations.map((s, i) => {
          const v = s.dec[di];
          const cls = "rainmap__pt" + (hi === i ? " is-hi" : hi != null ? " is-dim" : "");
          return React.createElement("g", { key: "s" + i, style: { cursor: "pointer" },
            onMouseEnter: () => setHi(i), onMouseLeave: () => setHi(null),
            onClick: () => setHi((h) => (h === i ? null : i)) },
            React.createElement("circle", { cx: px(s.lo), cy: py(s.la), r: radius(v), className: cls, style: { fill: rainColor(v, maxAbs) } }),
            React.createElement("text", {
              x: px(s.lo) + (s.dx != null ? s.dx : 9), y: py(s.la) + (s.dy != null ? s.dy : 3.5),
              textAnchor: s.anchor || "start", className: "rainmap__label",
            }, s.n)
          );
        }),
        hv && React.createElement("g", { style: { pointerEvents: "none" } },
          React.createElement("rect", { x: m, y: m, width: 236 * ck, height: 64 * ck, rx: 8 * ck, className: "map__info-bg" }),
          React.createElement("text", { x: m + 13 * ck, y: m + 21 * ck, className: "map__info-h", style: { fontSize: 14 * ck } }, hv.n),
          React.createElement("text", { x: m + 13 * ck, y: m + 39 * ck, className: "map__info-t", style: { fontSize: 12 * ck } }, hv.setting),
          React.createElement("text", { x: m + 13 * ck, y: m + 56 * ck, className: "map__info-t", style: { fontSize: 12 * ck, fill: "#181e26", fontWeight: 600 } },
            data.decades[di] + ": " + (hv.dec[di] > 0 ? "+" : "") + hv.dec[di] + "% vs 1950s")
        ),
        regionMean != null && React.createElement("text", { x: VW - m, y: VH - m, textAnchor: "end", className: "map__count" },
          "Region average " + (regionMean > 0 ? "+" : "") + regionMean.toFixed(1) + "% vs 1950s")
      ),
      React.createElement("div", { className: "map__legend" },
        React.createElement("span", { className: "map__legend-l" }, "Drier"),
        React.createElement("span", { className: "map__ramp map__ramp--rain" }),
        React.createElement("span", { className: "map__legend-l" }, "Wetter vs the 1950s")
      )
    );
  }

  /* ------------------------------------------------------------- RadarChart */
  /* A spider chart comparing each company across the four AASB S2 pillars.
     Toggle a company on/off in the legend; hover a vertex for its score. */
  function rgba(hex, a) { const c = hx(hex); return `rgba(${c[0]},${c[1]},${c[2]},${a})`; }
  function RadarChart({ data, label }) {
    const [hidden, setHidden] = useState({});
    const [hov, setHov] = useState(null);   // { si, ai }  (ai null = whole series)
    const wrapRef = React.useRef(null);
    const axes = data.axes, n = axes.length, max = data.max || 4;
    const VW = 460, VH = 420, cx = VW / 2, cy = VH / 2 + 8, R = 150;
    const ck = useChartScale(wrapRef, VW);
    const ang = (i) => -Math.PI / 2 + i * 2 * Math.PI / n;
    const pt = (i, val) => [cx + R * (val / max) * Math.cos(ang(i)), cy + R * (val / max) * Math.sin(ang(i))];
    const ringPts = (rv) => axes.map((_, i) => { const p = pt(i, rv); return p[0].toFixed(1) + "," + p[1].toFixed(1); }).join(" ");
    const rings = [1, 2, 3, 4].filter((r) => r <= max);
    const visible = data.series.filter((s) => !hidden[s.name]);
    const hovSeries = hov ? data.series[hov.si] : null;

    return React.createElement("div", { className: "radar", ref: wrapRef, style: { "--ck": ck } },
      React.createElement("svg", { viewBox: `0 0 ${VW} ${VH}`, className: "chart__svg radar__svg", role: "img", "aria-label": label },
        rings.map((rv) => React.createElement("polygon", { key: "ring" + rv, className: "radar__ring", points: ringPts(rv) })),
        rings.map((rv) => { const p = pt(0, rv); return React.createElement("text", { key: "rl" + rv, x: p[0] + 5, y: p[1] + 3, className: "radar__ringlabel" }, rv); }),
        axes.map((ax, i) => {
          const p = pt(i, max), lp = pt(i, max + 0.4);
          const anchor = Math.abs(lp[0] - cx) < 8 ? "middle" : lp[0] > cx ? "start" : "end";
          return React.createElement("g", { key: "ax" + i },
            React.createElement("line", { x1: cx, y1: cy, x2: p[0], y2: p[1], className: "radar__spoke" }),
            React.createElement("text", { x: lp[0], y: lp[1] + 3, textAnchor: anchor, className: "radar__axis-label" }, ax)
          );
        }),
        visible.map((s) => {
          const si = data.series.indexOf(s);
          const emph = hov ? (hov.si === si ? 1 : 0.32) : 1;
          const fillA = hov && hov.si === si ? 0.26 : 0.13;
          return React.createElement("polygon", {
            key: "p" + s.name, points: s.values.map((v, i) => { const p = pt(i, v); return p[0].toFixed(1) + "," + p[1].toFixed(1); }).join(" "),
            className: "radar__poly", style: { stroke: s.color, fill: rgba(s.color, fillA), opacity: emph },
          });
        }),
        visible.map((s) => { const si = data.series.indexOf(s); return s.values.map((v, i) => {
          const p = pt(i, v);
          return React.createElement("circle", {
            key: "d" + s.name + i, cx: p[0], cy: p[1], r: hov && hov.si === si && hov.ai === i ? 6 : 3.6,
            className: "radar__dot", style: { fill: s.color },
            onMouseEnter: () => setHov({ si, ai: i }), onMouseLeave: () => setHov(null),
            onClick: () => setHov({ si, ai: i }),
          });
        }); }),
        hovSeries && hov.ai != null && (function () {
          const v = hovSeries.values[hov.ai], p = pt(hov.ai, v);
          const txt = hovSeries.name + " · " + axes[hov.ai] + " " + v.toFixed(1);
          const w = (txt.length * 6.2 + 18) * ck; let tx = p[0] - w / 2; tx = Math.max(6, Math.min(tx, VW - w - 6));
          let ty = p[1] - 30 * ck; if (ty < 4) ty = p[1] + 12 * ck;
          return React.createElement("g", { style: { pointerEvents: "none" } },
            React.createElement("rect", { x: tx, y: ty, width: w, height: 22 * ck, rx: 6 * ck, className: "radar__tip-bg" }),
            React.createElement("text", { x: tx + w / 2, y: ty + 15 * ck, textAnchor: "middle", className: "radar__tip-t", style: { fontSize: 11 * ck } }, txt));
        })()
      ),
      React.createElement("div", { className: "radar__legend" },
        data.series.map((s) => React.createElement("button", {
          key: s.name, type: "button", className: "radar__toggle" + (hidden[s.name] ? " is-off" : ""),
          "aria-pressed": !hidden[s.name],
          onClick: () => setHidden((h) => Object.assign({}, h, { [s.name]: !h[s.name] })),
          onMouseEnter: () => setHov({ si: data.series.indexOf(s), ai: null }), onMouseLeave: () => setHov(null),
        },
          React.createElement("span", { className: "radar__sw", style: { background: s.color } }),
          React.createElement("span", { className: "radar__toggle-name" }, s.name),
          React.createElement("span", { className: "radar__toggle-score" }, s.overall + " · " + s.band)
        ))
      )
    );
  }

  /* ------------------------------------------------------------ DotCompare */
  /* The honest version of the pillar comparison: one row per AASB S2 pillar,
     one dot per company on a 0-4 scale, a grey bar showing the spread. Takes
     the same data object as RadarChart. */
  function DotCompare({ data, label }) {
    const [hidden, setHidden] = useState({});
    const [hov, setHov] = useState(null);   // { si, ai }
    const wrapRef = React.useRef(null);
    const ck = useChartScale(wrapRef, W);
    const axes = data.axes, max = data.max || 4;
    const ML = 118, MR = 20, MT = 14, MB = 34, ROW = 54;
    const DH = MT + axes.length * ROW + MB;
    const x = (v) => ML + v / max * (W - ML - MR);
    const rowY = (i) => MT + i * ROW + ROW / 2;
    const visible = data.series.filter((s) => !hidden[s.name]);
    const hovSeries = hov ? data.series[hov.si] : null;
    return React.createElement("div", { className: "dotc", ref: wrapRef, style: { "--ck": ck } },
      React.createElement("svg", { viewBox: `0 0 ${W} ${DH}`, className: "chart__svg", role: "img", "aria-label": label },
        Array.from({ length: max + 1 }, (_, v) => React.createElement("g", { key: "g" + v },
          React.createElement("line", { x1: x(v), x2: x(v), y1: MT, y2: DH - MB, className: "chart__grid" }),
          React.createElement("text", { x: x(v), y: DH - MB + 18, textAnchor: "middle", className: "chart__tick" }, v)
        )),
        axes.map((ax, ai) => {
          const vals = visible.map((s) => s.values[ai]);
          const lo = Math.min.apply(null, vals), hi2 = Math.max.apply(null, vals);
          return React.createElement("g", { key: "r" + ai },
            React.createElement("text", { x: ML - 12, y: rowY(ai) + 4, textAnchor: "end", className: "dotc__row" }, ax),
            visible.length > 1 && React.createElement("line", {
              x1: x(lo), x2: x(hi2), y1: rowY(ai), y2: rowY(ai), className: "dotc__span",
            }),
            visible.map((s) => {
              const si = data.series.indexOf(s);
              const active = hov && hov.si === si && hov.ai === ai;
              return React.createElement("circle", {
                key: s.name, cx: x(s.values[ai]), cy: rowY(ai), r: active ? 8 : 6,
                className: "dotc__dot", style: { fill: s.color, opacity: hov && hov.si !== si ? 0.35 : 1, stroke: "transparent", strokeWidth: 12 },
                onMouseEnter: () => setHov({ si, ai }), onMouseLeave: () => setHov(null),
                onClick: () => setHov({ si, ai }),
              });
            })
          );
        }),
        hovSeries && hov.ai != null && React.createElement(Tip, {
          x: x(hovSeries.values[hov.ai]), y: rowY(hov.ai) - 6,
          lines: [hovSeries.name, axes[hov.ai] + ": " + hovSeries.values[hov.ai].toFixed(1) + " / " + max], k: ck,
        })
      ),
      React.createElement("div", { className: "radar__legend" },
        data.series.map((s) => React.createElement("button", {
          key: s.name, type: "button", className: "radar__toggle" + (hidden[s.name] ? " is-off" : ""),
          "aria-pressed": !hidden[s.name],
          onClick: () => setHidden((h) => Object.assign({}, h, { [s.name]: !h[s.name] })),
          onMouseEnter: () => setHov({ si: data.series.indexOf(s), ai: null }), onMouseLeave: () => setHov(null),
        },
          React.createElement("span", { className: "radar__sw", style: { background: s.color } }),
          React.createElement("span", { className: "radar__toggle-name" }, s.name),
          React.createElement("span", { className: "radar__toggle-score" }, s.overall + " · " + s.band)
        ))
      )
    );
  }

  /* ------------------------------------------------------------- ScoreHeat */
  /* The 31 AASB S2 sub-requirements as a grouped heatmap: rows are the
     requirements (grouped by pillar), columns are the three companies, each
     cell shaded by its 0-4 score. Hover or tap a cell to load the full
     requirement, score and gap note into the detail panel below. */
  /* Orange-to-teal, not red-to-green: the ends stay distinct for red-green
     colour-blind readers, and lightness still orders the scale. */
  function scoreCell(s) {
    if (s == null) return { bg: "var(--bg-muted)", fg: "var(--text-faint)" };
    if (s >= 3.5) return { bg: "#0E7A66", fg: "#ffffff" };
    if (s >= 2.5) return { bg: "#8FD3C3", fg: "#0f332c" };
    if (s >= 1.5) return { bg: "#F4B740", fg: "#3d2b00" };
    return { bg: "#E8590C", fg: "#ffffff" };
  }
  function ScoreHeat({ data, label }) {
    const [sel, setSel] = useState(null);   // { pi, ri, ci }
    const companies = data.companies;
    const cols = `minmax(150px,1.7fr) repeat(${companies.length}, minmax(54px,1fr))`;
    const selCell = sel ? (() => {
      const row = data.pillars[sel.pi].rows[sel.ri];
      return { pillar: data.pillars[sel.pi].name, row, cell: row.cells[sel.ci], company: companies[sel.ci] };
    })() : null;
    return React.createElement("div", { className: "sheat", role: "group", "aria-label": label },
      React.createElement("div", { className: "sheat__scroll" },
      React.createElement("div", { className: "sheat__grid", style: { gridTemplateColumns: cols } },
        React.createElement("div", { className: "sheat__corner" }, "31 requirements"),
        companies.map((c) => React.createElement("div", { key: "h" + c, className: "sheat__colh" }, c)),
        data.pillars.map((p, pi) => [
          React.createElement("div", { key: "ph" + pi, className: "sheat__pillar", style: { gridColumn: `1 / span ${companies.length + 1}` } }, p.name),
          p.rows.map((row, ri) => [
            React.createElement("div", { key: "rh" + pi + "-" + ri, className: "sheat__rowh", title: row.desc },
              React.createElement("span", { className: "sheat__rid" }, row.id),
              React.createElement("span", { className: "sheat__rdesc" }, row.short)
            ),
            row.cells.map((cell, ci) => {
              const col = scoreCell(cell.s);
              const active = sel && sel.pi === pi && sel.ri === ri && sel.ci === ci;
              return React.createElement("button", {
                key: "c" + pi + "-" + ri + "-" + ci, type: "button",
                className: "sheat__cell" + (active ? " is-active" : ""),
                style: { background: col.bg, color: col.fg },
                onMouseEnter: () => setSel({ pi, ri, ci }), onFocus: () => setSel({ pi, ri, ci }),
                onClick: () => setSel({ pi, ri, ci }),
                "aria-label": `${companies[ci]} ${row.id} ${row.short}: ${cell.s} out of 4`,
              }, cell.s);
            }),
          ]),
        ])
      )),
      React.createElement("div", { className: "sheat__detail" + (selCell ? " is-filled" : "") },
        selCell ? React.createElement(React.Fragment, null,
          React.createElement("div", { className: "sheat__detail-head" },
            React.createElement("span", { className: "sheat__detail-co" }, selCell.company),
            React.createElement("span", { className: "sheat__detail-id" }, selCell.row.id),
            React.createElement("span", { className: "sheat__detail-score", style: { background: scoreCell(selCell.cell.s).bg, color: scoreCell(selCell.cell.s).fg } }, selCell.cell.s + " / 4")
          ),
          React.createElement("div", { className: "sheat__detail-req" }, selCell.row.desc),
          React.createElement("p", { className: "sheat__detail-note" }, selCell.cell.n),
          selCell.cell.e && React.createElement("div", { className: "sheat__detail-ev" }, "Evidence: " + selCell.cell.e)
        ) : React.createElement("p", { className: "sheat__detail-hint" }, "Hover or tap any cell to see the requirement, the score, and the gap note pulled from that company's report.")
      ),
      React.createElement("div", { className: "sheat__legend" },
        React.createElement("span", { className: "sheat__legend-l" }, "Score"),
        [["0-1", "#E8590C"], ["2", "#F4B740"], ["3", "#8FD3C3"], ["4", "#0E7A66"]].map((k) =>
          React.createElement("span", { key: k[0], className: "sheat__legend-k" },
            React.createElement("span", { className: "sheat__legend-sw", style: { background: k[1] } }), k[0])),
        React.createElement("span", { className: "sheat__legend-l" }, "weaker → more complete")
      )
    );
  }

  /* ------------------------------------------------------------- AreaChart */
  /* Stacked area over time. Bands are drawn bottom-to-top in `series` order;
     each band carries a thin surface-coloured stroke so neighbours read as
     separate fills without a border. The widest bands get a direct label; the
     rest lean on the legend (listed top-of-stack first, matching the eye) and
     the per-year hover breakdown. */
  function AreaChart({ data, label }) {
    const [hi, setHi] = useState(null);
    const wrapRef = React.useRef(null);
    const ck = useChartScale(wrapRef, W);
    const rows = data.rows, series = data.series;
    const xvals = rows.map((r) => r.x);
    const xmin = Math.min.apply(null, xvals), xmax = Math.max.apply(null, xvals);
    const xs = (v) => M.l + (v - xmin) / (xmax - xmin) * IW;
    const totals = rows.map((r) => series.reduce((a, s) => a + (r[s.k] || 0), 0));
    // Percent stacks (every year summing to ~100) pin the axis at 100.
    const near100 = totals.every((t) => Math.abs(t - 100) < 1.5);
    const ymax = (data.stack100 || near100) ? 100 : Math.max.apply(null, totals) * 1.02;
    const ys = (v) => M.t + IH - v / ymax * IH;

    // Cumulative bottom/top for each band at each row.
    const cum = rows.map(() => 0);
    const bands = series.map((s) => {
      const seg = rows.map((r, ri) => { const lo = cum[ri]; const top = lo + (r[s.k] || 0); cum[ri] = top; return { x: r.x, lo, hi: top }; });
      return { s, seg };
    });
    const bandPath = (seg) => {
      const top = seg.map((p, i) => (i ? "L" : "M") + xs(p.x).toFixed(1) + " " + ys(p.hi).toFixed(1)).join(" ");
      const bot = seg.slice().reverse().map((p) => "L" + xs(p.x).toFixed(1) + " " + ys(p.lo).toFixed(1)).join(" ");
      return top + " " + bot + " Z";
    };
    const yfmt = (t) => round(t, 0);
    const r = hi != null ? rows[hi] : null;
    const tipLines = r ? [String(r.x)].concat(series.slice().reverse().map((s) => s.label + " " + fmt(r[s.k] || 0, data.unit))) : null;
    // Legend in stack order, top band first.
    const legend = React.createElement("div", { className: "chart__legend" },
      series.slice().reverse().map((s, i) => React.createElement("span", { key: i },
        React.createElement("span", { className: "chart__legend-sw", style: { background: s.color } }), s.label)));

    return React.createElement(Svg, { label, refEl: wrapRef, k: ck, after: legend, onKeyDown: arrowKeys(rows.length, hi, setHi) },
      React.createElement(Axes, { xTicks: ticks(xmin, xmax, 4).filter((t) => t >= xmin && t <= xmax), yTicks: ticks(0, ymax, 4), xs, ys, xfmt: (t) => Math.round(t), yfmt, ylabel: data.ylabel }),
      bands.map((b, bi) => React.createElement("path", {
        key: bi, className: "chart__area-band", d: bandPath(b.seg), style: { fill: b.s.color },
      })),
      // Direct labels inside bands thick enough to hold them at the last year.
      bands.map((b, bi) => {
        const last = b.seg[b.seg.length - 1];
        const th = ys(last.lo) - ys(last.hi);
        if (th < 22) return null;
        return React.createElement("text", {
          key: "l" + bi, x: xs(last.x) - 6, y: (ys(last.lo) + ys(last.hi)) / 2 + 3.5, textAnchor: "end",
          className: "chart__area-label",
        }, b.s.label);
      }),
      data.xlabel && React.createElement("text", { x: M.l + IW / 2, y: H - 3, textAnchor: "middle", className: "chart__axlabel" }, data.xlabel),
      r && React.createElement("line", { className: "chart__guide", x1: xs(r.x), x2: xs(r.x), y1: M.t, y2: M.t + IH }),
      rows.map((row, i) => React.createElement("rect", {
        key: "h" + i, x: xs(row.x) - IW / rows.length / 2, y: M.t, width: IW / rows.length, height: IH, fill: "transparent",
        onMouseEnter: () => setHi(i), onMouseLeave: () => setHi(null), onClick: () => setHi(i),
      })),
      tipLines && React.createElement(Tip, { x: xs(r.x), y: M.t + 4, lines: tipLines, k: ck })
    );
  }

  /* ----------------------------------------------------------- CalendarHeat */
  /* A months x years calendar heatmap on a single-hue sequential ramp (more
     hours = deeper blue). The ramp is opacity over a fixed blue, so it reads
     the same way on the light and the dark card: pale/near-surface at zero,
     saturated at the maximum. A hovered cell loads its month, year and value
     into the readout line below; the colourbar names the two ends. */
  const MONTH_FULL = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  function calHeatColor(v, max) {
    if (v == null) return "var(--bg-muted)";
    const t = Math.pow(Math.max(0, v) / max, 0.72);   // gamma lifts the low end so faint months still read
    return "rgba(42,120,214," + (0.05 + 0.92 * t).toFixed(3) + ")";
  }
  function CalendarHeat({ data, label }) {
    const [hov, setHov] = useState(null);
    const years = data.years, months = data.monthLabels, matrix = data.matrix, max = data.max;
    const cols = "2.1rem repeat(" + years.length + ", minmax(13px, 1fr))";
    const hv = hov ? { m: hov.mi, y: hov.yi, v: matrix[hov.mi][hov.yi] } : null;
    return React.createElement("div", { className: "calheat", role: "group", "aria-label": label },
      React.createElement("div", { className: "calheat__scroll" },
        React.createElement("div", { className: "calheat__grid", style: { gridTemplateColumns: cols } },
          React.createElement("div", { className: "calheat__corner" }),
          years.map((y) => React.createElement("div", { key: "y" + y, className: "calheat__colh" }, y % 5 === 0 ? String(y) : "")),
          months.map((mlab, mi) => [
            React.createElement("div", { key: "m" + mi, className: "calheat__rowh" }, mlab),
            matrix[mi].map((v, yi) => React.createElement("div", {
              key: mi + "-" + yi,
              className: "calheat__cell" + (hov && hov.mi === mi && hov.yi === yi ? " is-hi" : ""),
              style: { background: calHeatColor(v, max) },
              title: MONTH_FULL[mi] + " " + years[yi] + ": " + v + (data.unit || ""),
              onMouseEnter: () => setHov({ mi, yi }), onMouseLeave: () => setHov(null),
            })),
          ])
        )
      ),
      React.createElement("div", { className: "calheat__readout" },
        hv ? React.createElement(React.Fragment, null,
          React.createElement("strong", null, MONTH_FULL[hv.m] + " " + years[hv.y]),
          " · " + fmt(hv.v) + " hours at or above the benchmark")
          : React.createElement("span", { className: "calheat__hint" }, "Hover a cell for its month, year and hours over the benchmark. Deeper blue means more hours of high water.")
      ),
      React.createElement("div", { className: "calheat__legend" },
        React.createElement("span", { className: "calheat__legend-l" }, "0"),
        React.createElement("span", { className: "calheat__ramp" }),
        React.createElement("span", { className: "calheat__legend-l" }, fmt(max) + (data.unit || ""))
      )
    );
  }

  window.AdhiCharts = { LineChart, BarChart, ScatterChart, HeatTable, MapChart, RainMapChart, RadarChart, DotCompare, ScoreHeat, AreaChart, CalendarHeat, useChartScale };
})();
