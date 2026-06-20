/* Hand-built, dependency-free interactive SVG charts for the project stories. */
(function () {
  const { useState } = React;
  const W = 540, H = 330, M = { l: 48, r: 16, t: 16, b: 42 };
  const IW = W - M.l - M.r, IH = H - M.t - M.b;
  const round = (n, d = 1) => { const p = Math.pow(10, d); return Math.round(n * p) / p; };

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

  /* Tooltip drawn inside the SVG so it scales with the chart. */
  function Tip({ x, y, lines }) {
    if (!lines) return null;
    const w = Math.max.apply(null, lines.map((l) => l.length)) * 6.4 + 16;
    const h = lines.length * 15 + 12;
    let tx = x - w / 2; tx = Math.max(M.l, Math.min(tx, W - M.r - w));
    let ty = y - h - 12; if (ty < M.t) ty = y + 14;
    return (
      React.createElement("g", { className: "chart__tip", style: { pointerEvents: "none" } },
        React.createElement("rect", { x: tx, y: ty, width: w, height: h, rx: 7, className: "chart__tip-bg" }),
        lines.map((l, i) => React.createElement("text", {
          key: i, x: tx + w / 2, y: ty + 17 + i * 15, textAnchor: "middle",
          className: i === 0 ? "chart__tip-h" : "chart__tip-t",
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
        ylabel && React.createElement("text", { x: -(M.t + IH / 2), y: 13, transform: "rotate(-90)", textAnchor: "middle", className: "chart__axlabel" }, ylabel)
      )
    );
  }

  function Svg({ children, label }) {
    return React.createElement("div", { className: "chart" },
      React.createElement("svg", { viewBox: `0 0 ${W} ${H}`, className: "chart__svg", role: "img", "aria-label": label }, children)
    );
  }

  /* ------------------------------------------------------------- LineChart */
  function LineChart({ data, label }) {
    const [hi, setHi] = useState(null);
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
      ? React.createElement(Tip, { x: xs(pts[hi][0]), y: ys(pts[hi][1]), lines: [String(pts[hi][0]), round(pts[hi][1], 1) + (data.unit || "")] }) : null;
    return React.createElement(Svg, { label },
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
      hi != null && pts[hi] && React.createElement("line", { className: "chart__guide", x1: xs(pts[hi][0]), x2: xs(pts[hi][0]), y1: M.t, y2: M.t + IH }),
      hi != null && pts[hi] && !data.bars && React.createElement("circle", { className: "chart__dot", cx: xs(pts[hi][0]), cy: ys(pts[hi][1]), r: 4 }),
      pts.map((p, i) => React.createElement("rect", {
        key: "h" + i, x: xs(p[0]) - IW / pts.length / 2, y: M.t, width: IW / pts.length, height: IH, fill: "transparent",
        onMouseEnter: () => setHi(i), onMouseLeave: () => setHi(null),
      })),
      tip
    );
  }

  /* -------------------------------------------------------------- BarChart */
  function BarChart({ data, label }) {
    const [hi, setHi] = useState(null);
    const bars = data.bars, grouped = data.keys && data.keys.length > 1;
    const maxV = Math.max.apply(null, bars.reduce((a, b) => grouped ? a.concat(data.keys.map((k) => b[k.k])) : a.concat([b.value]), []));
    const y1 = maxV * 1.12;
    const ys = (v) => M.t + IH - v / y1 * IH;
    const band = IW / bars.length, bw = band * 0.62;
    const yfmt = (t) => round(t, 0);
    function lines(b) {
      if (grouped) return [b.label].concat(data.keys.map((k) => k.label + ": " + round(b[k.k], 1) + (data.unit || "")));
      const ex = []; if (b.n != null) ex.push("n = " + b.n); if (b.median != null) ex.push("median " + b.median + " kt"); if (b.pres != null) ex.push(b.pres + " hPa"); if (b.cat3 != null) ex.push("Cat 3+: " + b.cat3 + "%");
      return [b.label, round(b.value, 1) + (data.unit || "")].concat(ex);
    }
    const hb = hi != null ? bars[hi] : null;
    return React.createElement(Svg, { label },
      React.createElement(Axes, { xTicks: [], yTicks: ticks(0, y1, 4), xs: () => 0, ys, yfmt, ylabel: data.ylabel }),
      bars.map((b, bi) => {
        const cx = M.l + band * bi + band / 2;
        const segs = grouped ? data.keys : [{ k: "value", color: "var(--accent)" }];
        const sw = bw / segs.length;
        return React.createElement("g", { key: bi, onMouseEnter: () => setHi(bi), onMouseLeave: () => setHi(null) },
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
      hb && React.createElement(Tip, { x: M.l + band * hi + band / 2, y: ys(grouped ? Math.max.apply(null, data.keys.map((k) => hb[k.k])) : hb.value), lines: lines(hb) }),
      grouped && React.createElement("g", null, data.keys.map((k, i) => React.createElement("g", { key: i, transform: `translate(${M.l + i * 96}, ${M.t})` },
        React.createElement("rect", { width: 11, height: 11, rx: 2, style: { fill: k.color } }),
        React.createElement("text", { x: 16, y: 9.5, className: "chart__tick" }, k.label))))
    );
  }

  /* ------------------------------------------------------------ ScatterChart */
  function ScatterChart({ data, label }) {
    const [hi, setHi] = useState(null);
    const pts = data.points;
    const [x0, x1] = domain(pts.map((p) => p[0]), 0.08), [y0, y1] = domain(pts.map((p) => p[1]), 0.1);
    const xs = (v) => M.l + (v - x0) / (x1 - x0) * IW;
    const ys = (v) => M.t + IH - (v - y0) / (y1 - y0) * IH;
    const hp = hi != null ? pts[hi] : null;
    return React.createElement(Svg, { label },
      React.createElement(Axes, { xTicks: ticks(x0, x1, 4), yTicks: ticks(y0, y1, 4), xs, ys, xfmt: (t) => round(t, 1), yfmt: (t) => round(t, 0), ylabel: data.ylabel }),
      data.xlabel && React.createElement("text", { x: M.l + IW / 2, y: H - 4, textAnchor: "middle", className: "chart__axlabel" }, data.xlabel),
      data.trend && React.createElement("line", { className: "chart__trend", x1: xs(data.trend[0]), y1: ys(data.trend[1]), x2: xs(data.trend[2]), y2: ys(data.trend[3]) }),
      data.r != null && React.createElement("text", { x: M.l + IW - 4, y: M.t + 14, textAnchor: "end", className: "chart__rnote" }, "r = " + data.r),
      pts.map((p, i) => React.createElement("circle", {
        key: i, cx: xs(p[0]), cy: ys(p[1]), r: hi === i ? 6 : 3.6, className: "chart__pt chart__pt--draw" + (hi === i ? " is-hi" : ""),
        style: { animationDelay: (i * 12) + "ms" }, onMouseEnter: () => setHi(i), onMouseLeave: () => setHi(null),
      })),
      hp && React.createElement(Tip, { x: xs(hp[0]), y: ys(hp[1]), lines: [hp[2] != null ? String(hp[2]) : "", round(hp[1], 1) + " · " + round(hp[0], 2)].filter(Boolean) })
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
  const WIND_STOPS = [[20, "#6b7a8f"], [50, "#1fa9c7"], [80, "#1f9d55"], [105, "#ffc234"], [125, "#ff5c39"], [150, "#b5179e"]];
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
    const win = data.win, VW = 600, VH = 660, m = 16;
    const cosMid = Math.cos((win.lat0 + win.lat1) / 2 * Math.PI / 180);
    const lonMid = (win.lon0 + win.lon1) / 2, latMid = (win.lat0 + win.lat1) / 2;
    const sc = Math.min((VW - 2 * m) / ((win.lon1 - win.lon0) * cosMid), (VH - 2 * m) / (win.lat1 - win.lat0));
    const px = (lo) => VW / 2 + (lo - lonMid) * cosMid * sc;
    const py = (la) => VH / 2 - (la - latMid) * sc;
    const path = (pts) => pts.map((p, i) => (i ? "L" : "M") + px(p[0]).toFixed(1) + " " + py(p[1]).toFixed(1)).join(" ");
    const lonLines = [110, 115, 120, 125, 130], latLines = [-10, -15, -20, -25, -30, -35];
    const hv = hi != null ? data.tracks[hi] : null;
    return React.createElement("div", { className: "chart" },
      React.createElement("svg", { viewBox: `0 0 ${VW} ${VH}`, className: "chart__svg map__svg", role: "img", "aria-label": label },
        lonLines.map((lo) => React.createElement("line", { key: "lo" + lo, x1: px(lo), x2: px(lo), y1: py(win.lat1), y2: py(win.lat0), className: "map__grat" })),
        latLines.map((la) => React.createElement("line", { key: "la" + la, x1: px(win.lon0), x2: px(win.lon1), y1: py(la), y2: py(la), className: "map__grat" })),
        latLines.map((la) => React.createElement("text", { key: "lat" + la, x: px(win.lon0) + 3, y: py(la) - 3, className: "map__grat-label" }, Math.abs(la) + "°S")),
        React.createElement("path", { d: path(data.coast), className: "map__coast" }),
        data.tracks.map((t, i) => React.createElement("path", {
          key: i, d: path(t.p), fill: "none", stroke: windColor(t.w), strokeWidth: hi === i ? 3 : 1.4,
          className: "map__track" + (hi === i ? " is-hi" : (hi != null ? " is-dim" : "")),
          onMouseEnter: () => setHi(i), onMouseLeave: () => setHi(null),
        })),
        data.cities.map((c, i) => React.createElement("g", { key: "c" + i },
          React.createElement("circle", { cx: px(c.lo), cy: py(c.la), r: 3, className: "map__city" }),
          React.createElement("text", { x: px(c.lo) + 6, y: py(c.la) + 3.5, className: "map__city-label" }, c.n)
        )),
        hv && React.createElement("g", { style: { pointerEvents: "none" } },
          React.createElement("rect", { x: m, y: m, width: 210, height: 48, rx: 8, className: "map__info-bg" }),
          React.createElement("text", { x: m + 13, y: m + 21, className: "map__info-h" }, hv.n + " · " + hv.y),
          React.createElement("text", { x: m + 13, y: m + 38, className: "map__info-t" }, "peak " + hv.w + " kt")
        ),
        React.createElement("text", { x: VW - m, y: VH - m, textAnchor: "end", className: "map__count" }, data.tracks.length + " storms within 500 km · 1985–2024")
      ),
      React.createElement("div", { className: "map__legend" },
        React.createElement("span", { className: "map__legend-l" }, "Peak wind"),
        React.createElement("span", { className: "map__ramp" }),
        React.createElement("span", { className: "map__legend-l" }, "weaker → stronger (Cat 5)")
      )
    );
  }

  window.AdhiCharts = { LineChart, BarChart, ScatterChart, HeatTable, MapChart };
})();
