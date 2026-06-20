/* COMPILED from js/sections.jsx. Do not edit directly; edit the .jsx and recompile. */
function _extends() {return _extends = Object.assign ? Object.assign.bind() : function (n) {for (var e = 1; e < arguments.length; e++) {var t = arguments[e];for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]);}return n;}, _extends.apply(null, arguments);} /* Portfolio sections: Nav, Hero, StatBand, Stories (interactive), About, Footer */
(function () {
  const { Button, IconButton, Eyebrow, Stat, Badge, Tag } = window.AdhiClimateDesignSystem_bcac21;
  const Icon = window.Icon;
  const P = window.PORTFOLIO;

  /* ----------------------------------------------------- scroll-reveal wrap */
  function Reveal({ children, as = "div", className = "", delay = 0, ...rest }) {
    const ref = React.useRef(null);
    const [shown, setShown] = React.useState(false);
    React.useEffect(() => {
      const el = ref.current;
      if (!el) return;
      const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (reduce || typeof IntersectionObserver === "undefined") {setShown(true);return;}
      const io = new IntersectionObserver((entries) => {
        entries.forEach((e) => {if (e.isIntersecting) {setShown(true);io.disconnect();}});
      }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
      io.observe(el);
      return () => io.disconnect();
    }, []);
    const Tag = as;
    return (/*#__PURE__*/
      React.createElement(Tag, _extends({ ref: ref,
        className: ["reveal", shown ? "reveal--in" : "", className].filter(Boolean).join(" "),
        style: delay ? { transitionDelay: delay + "ms" } : undefined },
      rest),
      children
      ));

  }

  /* ------------------------------------------------------ count-up + theme */
  function CountUp({ end, dur = 1100 }) {
    const [v, setV] = React.useState(0);
    const ref = React.useRef(null);
    React.useEffect(() => {
      const el = ref.current;if (!el) return;
      const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (reduce || typeof IntersectionObserver === "undefined" || typeof requestAnimationFrame === "undefined") {setV(end);return;}
      const io = new IntersectionObserver((es) => {
        es.forEach((e) => {
          if (e.isIntersecting) {
            io.disconnect();
            const t0 = performance.now();
            const tick = (t) => {const p = Math.min(1, (t - t0) / dur);setV(Math.round(end * (1 - Math.pow(1 - p, 3))));if (p < 1) requestAnimationFrame(tick);};
            requestAnimationFrame(tick);
          }
        });
      }, { threshold: 0.4 });
      io.observe(el);
      return () => io.disconnect();
    }, [end]);
    return /*#__PURE__*/React.createElement("span", { ref: ref }, v);
  }

  function PThemeToggle() {
    const isDark = () => document.documentElement.getAttribute("data-theme") === "dark";
    const [dark, setDark] = React.useState(isDark);
    function toggle() {
      const next = !isDark();
      document.documentElement.setAttribute("data-theme", next ? "dark" : "light");
      try {localStorage.setItem("theme", next ? "dark" : "light");} catch (e) {}
      setDark(next);
    }
    return (/*#__PURE__*/
      React.createElement(IconButton, { variant: "outline", "aria-label": dark ? "Switch to light mode" : "Switch to dark mode", onClick: toggle }, /*#__PURE__*/
      React.createElement(Icon, { name: dark ? "sun" : "moon", size: 17 })
      ));

  }

  /* ------------------------------------------------- interactive data table */
  function PDataTable({ data, caption }) {
    const columns = data.columns || data.headers || [];
    const [sort, setSort] = React.useState({ col: null, dir: 1 });
    const toNum = (s) => {
      const n = parseFloat(String(s).replace(/[−–]/g, "-").replace(/[^0-9.\-]/g, ""));
      return isNaN(n) ? null : n;
    };
    const rows = React.useMemo(() => {
      if (sort.col === null) return data.rows;
      const i = sort.col;
      return data.rows.slice().sort((a, b) => {
        const na = toNum(a[i]),nb = toNum(b[i]);
        if (na !== null && nb !== null) return (na - nb) * sort.dir;
        return String(a[i]).localeCompare(String(b[i])) * sort.dir;
      });
    }, [data, sort]);
    const toggle = (i) => setSort((s) => s.col === i ? { col: i, dir: -s.dir } : { col: i, dir: 1 });
    return (/*#__PURE__*/
      React.createElement("figure", { className: "dtable" }, /*#__PURE__*/
      React.createElement("div", { className: "dtable__scroll" }, /*#__PURE__*/
      React.createElement("table", { className: "dtable__table" }, /*#__PURE__*/
      React.createElement("thead", null, /*#__PURE__*/
      React.createElement("tr", null,
      columns.map((c, i) => /*#__PURE__*/
      React.createElement("th", { key: i,
        className: "dtable__th" + (sort.col === i ? " dtable__th--active" : ""),
        "aria-sort": sort.col === i ? sort.dir > 0 ? "ascending" : "descending" : "none",
        onClick: () => toggle(i) },
      c, /*#__PURE__*/React.createElement("span", { className: "dtable__arrow" }, sort.col === i ? sort.dir > 0 ? "▲" : "▼" : "↕")
      )
      )
      )
      ), /*#__PURE__*/
      React.createElement("tbody", null,
      rows.map((r, ri) => /*#__PURE__*/
      React.createElement("tr", { key: ri }, r.map((cell, ci) => /*#__PURE__*/React.createElement("td", { key: ci }, cell)))
      )
      )
      )
      ),
      caption && /*#__PURE__*/React.createElement("figcaption", { className: "dtable__cap" }, caption, " \xB7 tap a column to sort")
      ));

  }

  /* -------------------------------------------------------------------- Nav */
  function PNav({ onContact }) {
    return (/*#__PURE__*/
      React.createElement("header", { className: "nav" }, /*#__PURE__*/
      React.createElement("div", { className: "wrap nav__inner" }, /*#__PURE__*/
      React.createElement("a", { className: "nav__brand", href: "#top" }, /*#__PURE__*/
      React.createElement("img", { src: "assets/logo-mark.svg", alt: "" }), /*#__PURE__*/
      React.createElement("span", null, /*#__PURE__*/
      React.createElement("span", { className: "nav__name" }, P.profile.name), /*#__PURE__*/
      React.createElement("span", { className: "nav__role" }, P.profile.role)
      )
      ), /*#__PURE__*/
      React.createElement("nav", { className: "nav__links" }, /*#__PURE__*/
      React.createElement("a", { className: "nav__link", href: "#work" }, "Projects"), /*#__PURE__*/
      React.createElement("a", { className: "nav__link", href: "#about" }, "About")
      ), /*#__PURE__*/
      React.createElement("div", { className: "nav__actions" }, /*#__PURE__*/
      React.createElement(PThemeToggle, null), /*#__PURE__*/
      React.createElement(Button, { variant: "secondary", size: "sm", as: "a", href: P.repo, iconLeft: /*#__PURE__*/React.createElement(Icon, { name: "file-text", size: 16 }) }, "CV"), /*#__PURE__*/
      React.createElement(Button, { variant: "primary", size: "sm", onClick: onContact, iconRight: /*#__PURE__*/React.createElement(Icon, { name: "arrow-right", size: 16 }) }, "Get in touch")
      )
      )
      ));

  }

  /* ------------------------------------------------------------------ Hero */
  function PHero({ onContact }) {
    // Real period-mean Nov-Apr sea-surface-temperature anomaly (vs the 1991-2020
    // average), 1985-2024, from cyclone-risk/data/sst_intensity.csv. Height maps
    // the lowest period to 40% and the highest to 82%.
    const bars = [
    { y: "1985–1990", v: "−0.20", h: 45 },
    { y: "1991–1995", v: "−0.26", h: 40 },
    { y: "1996–2001", v: "−0.13", h: 51 },
    { y: "2002–2007", v: "−0.07", h: 56 },
    { y: "2008–2013", v: "+0.12", h: 71 },
    { y: "2014–2018", v: "+0.25", h: 81 },
    { y: "2019–2024", v: "+0.26", h: 82 }];

    return (/*#__PURE__*/
      React.createElement("section", { className: "hero", id: "top" }, /*#__PURE__*/
      React.createElement("div", { className: "wrap hero__grid" }, /*#__PURE__*/
      React.createElement("div", null, /*#__PURE__*/
      React.createElement("div", { className: "hero__eyebrow" }, /*#__PURE__*/React.createElement(Eyebrow, { tick: true }, "Climate & Sustainability \xB7 WA")), /*#__PURE__*/
      React.createElement("h1", { className: "hero__title" }, "I got curious about Western Australia's ", /*#__PURE__*/React.createElement("span", { className: "accent" }, "climate"), ", so I started digging."), /*#__PURE__*/
      React.createElement("p", { className: "hero__lead" }, P.profile.intro), /*#__PURE__*/
      React.createElement("div", { className: "hero__actions" }, /*#__PURE__*/
      React.createElement(Button, { variant: "primary", size: "lg", onClick: onContact, iconRight: /*#__PURE__*/React.createElement(Icon, { name: "arrow-right", size: 18 }) }, "Get in touch"), /*#__PURE__*/
      React.createElement(Button, { variant: "ghost", size: "lg", as: "a", href: "#work", iconRight: /*#__PURE__*/React.createElement(Icon, { name: "arrow-down-right", size: 18 }) }, "See the projects")
      ), /*#__PURE__*/
      React.createElement("div", { className: "hero__meta" }, /*#__PURE__*/
      React.createElement("span", { className: "hero__meta-item" }, /*#__PURE__*/React.createElement(Icon, { name: "map-pin", size: 16 }), P.profile.location), /*#__PURE__*/
      React.createElement("span", { className: "hero__meta-item" }, /*#__PURE__*/React.createElement(Icon, { name: "leaf", size: 16 }), "Physical risk \xB7 Climate data \xB7 AASB S2")
      )
      ), /*#__PURE__*/

      React.createElement("div", { className: "hero__panel" }, /*#__PURE__*/
      React.createElement("div", { className: "hero__panel-label" }, "WA cyclone-region ocean temperature \xB7 ", /*#__PURE__*/React.createElement("span", { style: { whiteSpace: "nowrap" } }, "1985\u20132024")), /*#__PURE__*/
      React.createElement("div", { className: "hero__chart", role: "img", "aria-label": "WA cyclone-region ocean temperature, 1985 to 2024: five-year averages rise from \u22120.20 \xB0C to +0.26 \xB0C versus the 1991\u20132020 average, about 0.5 \xB0C of warming." },
      bars.map((b, i) => /*#__PURE__*/
      React.createElement("div", { key: i, className: "hero__bar-wrap" }, /*#__PURE__*/
      React.createElement("div", { className: "hero__bar", style: { height: b.h + "%", animationDelay: i * 70 + "ms" } }, /*#__PURE__*/
      React.createElement("span", { className: "hero__bar-tip", "aria-hidden": "true" }, b.y, /*#__PURE__*/React.createElement("b", null, b.v, " \xB0C"), /*#__PURE__*/React.createElement("em", null, "vs 1991\u20132020 avg"))
      )
      )
      )
      ), /*#__PURE__*/
      React.createElement("div", { className: "hero__panel-stat" }, /*#__PURE__*/
      React.createElement("span", null, /*#__PURE__*/React.createElement("span", { className: "big" }, "40"), " ", /*#__PURE__*/React.createElement("span", { className: "unit" }, "yrs analysed")), /*#__PURE__*/
      React.createElement("span", { className: "delta" }, "\u25B4 +0.5 \xB0C since the 1980s")
      )
      )
      )
      ));

  }

  /* ------------------------------------------------------------- StatBand */
  function PStatBand() {
    return (/*#__PURE__*/
      React.createElement("section", { className: "statband" }, /*#__PURE__*/
      React.createElement("div", { className: "wrap statband__grid" },
      P.stats.map((s, i) => {
        const n = parseInt(s.value, 10);
        const value = String(n) === String(s.value) ? /*#__PURE__*/React.createElement(CountUp, { end: n }) : s.value;
        return (/*#__PURE__*/
          React.createElement(Reveal, { className: "statband__cell", key: i, delay: i * 80 }, /*#__PURE__*/
          React.createElement(Stat, { label: s.label, value: value, unit: s.unit, delta: s.delta, trend: s.trend || "neutral", caption: s.caption, size: "md" })
          ));

      })
      )
      ));

  }

  /* ---------------------------------------------------------------- Stories */
  function statusVariant(s) {
    if (["Live", "Adopted", "Delivered", "Published", "Complete"].includes(s)) return "leaf";
    if (["In progress", "Reported"].includes(s)) return "accent";
    return "neutral";
  }

  function PChart({ vizKey, spec }) {
    const AC = window.AdhiCharts || {};
    const CD = (window.CHARTDATA || {})[vizKey] || {};
    let data = CD[spec.key];
    if (!data) return null;
    if (spec.sub) data = Object.assign({}, data[spec.sub], { ylabel: data.ylabel });
    if (spec.keys) data = Object.assign({}, data, { keys: spec.keys });
    const Comp = { line: AC.LineChart, bar: AC.BarChart, scatter: AC.ScatterChart, heat: AC.HeatTable }[spec.type];
    return Comp ? React.createElement(Comp, { data, label: spec.title }) : null;
  }

  const SCROLLY_STEPS = [
  { eyebrow: "The setup", text: "Forty years of cyclones near Western Australia. As the climate warms, two things are worth watching together: how warm the ocean was, and how strong the storms got." },
  { eyebrow: "The ocean warmed", text: "The sea where these cyclones form rose by about 0.5 °C since the 1980s. The trend is unmistakable, and statistically rock solid." },
  { eyebrow: "The storms did not", text: "If warmer water meant stronger storms, peak winds should climb too. They didn't. Mean peak wind actually edged downward over the same years." },
  { eyebrow: "So they came apart", text: "Warmer years were not stronger-storm years (correlation r = −0.22). Ocean heat and storm strength decoupled, which is exactly why WA's future cyclone risk can't be read straight off the recent record." }];


  function ScrollyChart({ D, stage }) {
    const W = 560,H = 340,M = { l: 46, r: 46, t: 16, b: 32 };
    const IW = W - M.l - M.r,IH = H - M.t - M.b;
    const x0 = 1985,x1 = 2024;
    const xs = (y) => M.l + (y - x0) / (x1 - x0) * IW;
    const wv = D.wind.map((p) => p[1]).concat([D.windTrend[1], D.windTrend[3]]);
    const sv = D.sst.map((p) => p[1]).concat([D.sstTrend[1], D.sstTrend[3]]);
    const wlo = Math.min.apply(null, wv) - 4,whi = Math.max.apply(null, wv) + 4;
    const slo = Math.min.apply(null, sv) - 0.08,shi = Math.max.apply(null, sv) + 0.08;
    const ysW = (v) => M.t + IH - (v - wlo) / (whi - wlo) * IH;
    const ysS = (v) => M.t + IH - (v - slo) / (shi - slo) * IH;
    const ln = (arr, f) => arr.map((p, i) => (i ? "L" : "M") + xs(p[0]).toFixed(1) + " " + f(p[1]).toFixed(1)).join(" ");
    return (/*#__PURE__*/
      React.createElement("svg", { viewBox: `0 0 ${W} ${H}`, className: "chart__svg scrolly__svg", role: "img", "aria-label": "Ocean temperature rose between 1985 and 2024 while cyclone peak winds did not." },
      [0, 1, 2].map((i) => {const v = wlo + (whi - wlo) * i / 2;return (/*#__PURE__*/
          React.createElement("g", { key: "w" + i }, /*#__PURE__*/
          React.createElement("line", { x1: M.l, x2: M.l + IW, y1: ysW(v), y2: ysW(v), className: "chart__grid" }), /*#__PURE__*/
          React.createElement("text", { x: M.l - 8, y: ysW(v) + 3, textAnchor: "end", className: "chart__tick" }, Math.round(v))
          ));}),
      [0, 1, 2].map((i) => {const v = slo + (shi - slo) * i / 2;return (/*#__PURE__*/
          React.createElement("text", { key: "s" + i, x: M.l + IW + 8, y: ysS(v) + 3, textAnchor: "start", className: "chart__tick", style: { fill: "var(--accent)" } }, (v > 0 ? "+" : "") + v.toFixed(1)));}), /*#__PURE__*/
      React.createElement("text", { x: xs(1985), y: H - M.b + 18, textAnchor: "middle", className: "chart__tick" }, "1985"), /*#__PURE__*/
      React.createElement("text", { x: xs(2005), y: H - M.b + 18, textAnchor: "middle", className: "chart__tick" }, "2005"), /*#__PURE__*/
      React.createElement("text", { x: xs(2024), y: H - M.b + 18, textAnchor: "middle", className: "chart__tick" }, "2024"), /*#__PURE__*/
      React.createElement("g", { className: "scrolly__series", style: { opacity: stage >= 1 ? 1 : 0.12 } }, /*#__PURE__*/
      React.createElement("line", { className: "chart__trend", style: { stroke: "var(--accent)" }, x1: xs(D.sstTrend[0]), y1: ysS(D.sstTrend[1]), x2: xs(D.sstTrend[2]), y2: ysS(D.sstTrend[3]) }), /*#__PURE__*/
      React.createElement("path", { className: "scrolly__line", style: { stroke: "var(--accent)" }, d: ln(D.sst, ysS) })
      ), /*#__PURE__*/
      React.createElement("g", { className: "scrolly__series", style: { opacity: stage >= 2 ? 1 : 0 } }, /*#__PURE__*/
      React.createElement("line", { className: "chart__trend", style: { stroke: "#FF5C39" }, x1: xs(D.windTrend[0]), y1: ysW(D.windTrend[1]), x2: xs(D.windTrend[2]), y2: ysW(D.windTrend[3]) }), /*#__PURE__*/
      React.createElement("path", { className: "scrolly__line", style: { stroke: "#FF5C39" }, d: ln(D.wind, ysW) })
      ),
      stage >= 3 && /*#__PURE__*/React.createElement("text", { x: M.l + IW - 4, y: M.t + 15, textAnchor: "end", className: "scrolly__note" }, "no link \xB7 r = \u22120.22")
      ));

  }

  function PScrolly() {
    const D = window.SCROLLYDATA;
    const [stage, setStage] = React.useState(1);
    const steps = React.useRef([]);
    React.useEffect(() => {
      if (typeof IntersectionObserver === "undefined") {setStage(3);return;}
      const io = new IntersectionObserver((entries) => {
        entries.forEach((e) => {if (e.isIntersecting) setStage(Number(e.target.dataset.step));});
      }, { rootMargin: "-45% 0px -45% 0px", threshold: 0 });
      steps.current.forEach((el) => el && io.observe(el));
      return () => io.disconnect();
    }, []);
    if (!D) return null;
    return (/*#__PURE__*/
      React.createElement("div", { className: "scrolly" }, /*#__PURE__*/
      React.createElement("div", { className: "scrolly__graphic" }, /*#__PURE__*/
      React.createElement("div", { className: "story__chart-title" }, "Ocean temperature vs storm strength, 1985\u20132024"), /*#__PURE__*/
      React.createElement(ScrollyChart, { D: D, stage: stage }), /*#__PURE__*/
      React.createElement("div", { className: "scrolly__legend" }, /*#__PURE__*/
      React.createElement("span", null, /*#__PURE__*/React.createElement("span", { className: "scrolly__sw", style: { background: "var(--accent)" } }), "Ocean temperature"), /*#__PURE__*/
      React.createElement("span", null, /*#__PURE__*/React.createElement("span", { className: "scrolly__sw", style: { background: "#FF5C39" } }), "Cyclone peak wind")
      )
      ), /*#__PURE__*/
      React.createElement("div", { className: "scrolly__steps" },
      SCROLLY_STEPS.map((s, i) => /*#__PURE__*/
      React.createElement("div", { className: "scrolly__step", key: i, "data-step": i, ref: (el) => steps.current[i] = el }, /*#__PURE__*/
      React.createElement("div", { className: "scrolly__card" + (stage === i ? " is-active" : "") }, /*#__PURE__*/
      React.createElement("div", { className: "scrolly__eyebrow" }, s.eyebrow), /*#__PURE__*/
      React.createElement("p", null, s.text)
      )
      )
      )
      )
      ));

  }

  function PStory({ p, index }) {
    const [openData, setOpenData] = React.useState(false);
    const [openCharts, setOpenCharts] = React.useState(false);
    const rev = index % 2 === 1;
    const hasViz = p.viz && p.viz.length > 0 && window.AdhiCharts && window.CHARTDATA;
    return (/*#__PURE__*/
      React.createElement("section", { className: "story", id: p.id }, /*#__PURE__*/
      React.createElement("div", { className: "wrap" }, /*#__PURE__*/
      React.createElement("div", { className: "story__grid" + (rev ? " story__grid--rev" : "") }, /*#__PURE__*/
      React.createElement(Reveal, { className: "story__media" },
      p.scoreboard ? /*#__PURE__*/
      React.createElement("div", { className: "story__board" }, /*#__PURE__*/React.createElement(PDataTable, { data: p.scoreboard, caption: "Disclosure scores, 0 to 4" })) :
      hasViz ? /*#__PURE__*/
      React.createElement("div", { className: "story__feature" }, /*#__PURE__*/
      React.createElement("div", { className: "story__chart-title" }, p.viz[0].title), /*#__PURE__*/
      React.createElement(PChart, { vizKey: p.vizKey, spec: p.viz[0] })
      ) :
      null
      ), /*#__PURE__*/

      React.createElement(Reveal, { className: "story__body", delay: 120 }, /*#__PURE__*/
      React.createElement("div", { className: "story__tagrow" }, /*#__PURE__*/
      React.createElement(Eyebrow, { tick: true }, "Project ", index + 1, " \xB7 ", p.year), /*#__PURE__*/
      React.createElement(Badge, { variant: statusVariant(p.status), dot: true }, p.status)
      ), /*#__PURE__*/
      React.createElement("h2", { className: "story__title" }, p.title), /*#__PURE__*/
      React.createElement("p", { className: "story__hook" }, p.headline), /*#__PURE__*/
      React.createElement("p", { className: "story__lead" }, p.body), /*#__PURE__*/

      React.createElement("div", { className: "story__findings" },
      p.findings.map((f, i) => /*#__PURE__*/
      React.createElement("div", { className: "pfind", key: i }, /*#__PURE__*/
      React.createElement("div", { className: "pfind__v" }, /*#__PURE__*/React.createElement("span", { className: "v" }, f.value), f.unit && /*#__PURE__*/React.createElement("span", { className: "u" }, f.unit)), /*#__PURE__*/
      React.createElement("div", { className: "pfind__label" }, f.label), /*#__PURE__*/
      React.createElement("div", { className: "pfind__text" }, f.text)
      )
      )
      ), /*#__PURE__*/

      React.createElement("p", { className: "story__meaning" }, /*#__PURE__*/React.createElement("span", { className: "story__meaning-tag" }, "Why it matters"), p.meaning),

      (hasViz && p.viz.length > 1 || p.dataset) && /*#__PURE__*/
      React.createElement("div", { className: "story__toggles" },
      hasViz && p.viz.length > 1 && /*#__PURE__*/
      React.createElement("button", { type: "button", className: "story__data-toggle", "aria-expanded": openCharts, onClick: () => setOpenCharts((o) => !o) }, /*#__PURE__*/
      React.createElement(Icon, { name: "bar-chart", size: 16 }),
      openCharts ? "Hide charts" : "See all " + p.viz.length + " charts", /*#__PURE__*/
      React.createElement(Icon, { name: "chevron-right", size: 15, className: "story__data-chev" + (openCharts ? " story__data-chev--open" : "") })
      ),

      p.dataset && /*#__PURE__*/
      React.createElement("button", { type: "button", className: "story__data-toggle", "aria-expanded": openData, onClick: () => setOpenData((o) => !o) }, /*#__PURE__*/
      React.createElement(Icon, { name: "layers", size: 16 }),
      openData ? "Hide the data" : "Explore the raw data", /*#__PURE__*/
      React.createElement(Icon, { name: "chevron-right", size: 15, className: "story__data-chev" + (openData ? " story__data-chev--open" : "") })
      )

      ), /*#__PURE__*/


      React.createElement("div", { className: "story__links" },
      p.resources.map((r, i) => /*#__PURE__*/
      React.createElement("a", { className: "story__link", key: i, href: r.href, target: "_blank", rel: "noopener noreferrer" }, /*#__PURE__*/
      React.createElement(Icon, { name: r.icon, size: 15 }), r.label
      )
      )
      )
      )
      ),

      p.hasMap && window.MAPDATA && window.AdhiCharts && window.AdhiCharts.MapChart && /*#__PURE__*/
      React.createElement(Reveal, { className: "story__map" }, /*#__PURE__*/
      React.createElement("div", { className: "story__chart-title" }, "Where these storms tracked, season by season"),
      React.createElement(window.AdhiCharts.MapChart, { data: window.MAPDATA, label: "Tracks of the 193 cyclones that came within 500 km of WA, 1985 to 2024, coloured by peak wind." }), /*#__PURE__*/
      React.createElement("p", { className: "story__map-note" }, "Every cyclone that came within 500 km of the WA coast, coloured by peak wind. Hover a track to see the storm. Notice how they sweep in from the north-west toward the Pilbara and Kimberley.")
      ),


      p.scrolly && window.SCROLLYDATA && /*#__PURE__*/
      React.createElement("div", { className: "story__scrolly" }, /*#__PURE__*/
      React.createElement(PScrolly, null)
      ),


      openCharts && hasViz && /*#__PURE__*/
      React.createElement("div", { className: "story__charts" },
      p.viz.slice(1).map((spec, i) => /*#__PURE__*/
      React.createElement("div", { className: "story__chart-card", key: i }, /*#__PURE__*/
      React.createElement("div", { className: "story__chart-title" }, spec.title), /*#__PURE__*/
      React.createElement(PChart, { vizKey: p.vizKey, spec: spec })
      )
      )
      ),

      openData && p.dataset && /*#__PURE__*/
      React.createElement("div", { className: "story__data" }, /*#__PURE__*/
      React.createElement(PDataTable, { data: p.dataset, caption: p.dataset.caption })
      )

      )
      ));

  }

  function PStories() {
    return (/*#__PURE__*/
      React.createElement("div", { id: "work" }, /*#__PURE__*/
      React.createElement("section", { className: "section section--tight" }, /*#__PURE__*/
      React.createElement("div", { className: "wrap" }, /*#__PURE__*/
      React.createElement(Reveal, { className: "section-head" }, /*#__PURE__*/
      React.createElement(Eyebrow, { tick: true }, "Personal projects"), /*#__PURE__*/
      React.createElement("h2", null, "Built out of curiosity."), /*#__PURE__*/
      React.createElement("p", null, "Three projects I took on myself, simply because I love working with data and wanted answers. Each one started with a Western Australian climate question I wanted to work through from the raw data myself, then check my numbers against the published science. No client, no brief, just curiosity and a respect for what the data actually says.")
      )
      )
      ),
      P.projects.map((p, i) => /*#__PURE__*/React.createElement(PStory, { key: p.id, p: p, index: i }))
      ));

  }

  /* ----------------------------------------------------------------- About */
  function PAbout() {
    return (/*#__PURE__*/
      React.createElement("section", { className: "section", id: "about" }, /*#__PURE__*/
      React.createElement("div", { className: "wrap about__grid" }, /*#__PURE__*/
      React.createElement(Reveal, { className: "about__body" }, /*#__PURE__*/
      React.createElement(Eyebrow, { tick: true }, "About"), /*#__PURE__*/
      React.createElement("h2", { style: { fontSize: "var(--text-4xl)", letterSpacing: "var(--tracking-tighter)", margin: "12px 0 20px" } }, "Hi, I'm Adhi."

      ), /*#__PURE__*/
      React.createElement("p", null, "I'm studying a Master of Environment and Climate Emergency at Curtin University, now in my second year with two semesters to go. Right now I'm looking for an internship in sustainability, somewhere I can turn this kind of climate-data work into real impact for a team."



      ), /*#__PURE__*/
      React.createElement("p", { style: { marginTop: "var(--space-4)" } }, "I've arrived here from a few directions. I trained as a naval architect and marine engineer, spent two years as a business analyst in regional Western Australia, and worked as a hatchery technician while completing a Diploma of Aquaculture. The common thread has always been the same: taking messy, real-world data and turning it into something a team can act on."




      ), /*#__PURE__*/
      React.createElement("p", { style: { marginTop: "var(--space-4)" } }, "This portfolio is where I bring that together: real Western Australian climate data, honest analysis, and findings written so anyone can follow them, framed for the disclosure rules companies now have to meet. I care as much about getting the cause right as I do about the headline number."



      ), /*#__PURE__*/
      React.createElement("div", { className: "about__tags" }, /*#__PURE__*/
      React.createElement(Tag, null, "Physical climate risk"), /*#__PURE__*/React.createElement(Tag, null, "AASB S2"), /*#__PURE__*/React.createElement(Tag, null, "IBTrACS / BOM"), /*#__PURE__*/
      React.createElement(Tag, null, "Trend detection"), /*#__PURE__*/React.createElement(Tag, null, "Disclosure scoring")
      )
      ), /*#__PURE__*/
      React.createElement(Reveal, { as: "aside", id: "contact", className: "about__contact", delay: 120 }, /*#__PURE__*/
      React.createElement(Eyebrow, { tone: "leaf", tick: true }, "Get in touch"), /*#__PURE__*/
      React.createElement("h3", { className: "about__contact-title" }, "Open to sustainability internships."), /*#__PURE__*/
      React.createElement("p", null, "If you're hiring, or you just want to talk about WA climate, I'd love to hear from you."), /*#__PURE__*/
      React.createElement("div", { className: "about__contact-actions" }, /*#__PURE__*/
      React.createElement(Button, { variant: "leaf", size: "lg", fullWidth: true, as: "a", href: "mailto:" + P.profile.email, iconLeft: /*#__PURE__*/React.createElement(Icon, { name: "mail", size: 18 }) }, "Email me"), /*#__PURE__*/
      React.createElement(Button, { variant: "secondary", size: "lg", fullWidth: true, as: "a", href: P.profile.linkedin, target: "_blank", rel: "noopener noreferrer", iconLeft: /*#__PURE__*/React.createElement(Icon, { name: "linkedin", size: 18 }) }, "LinkedIn")
      ), /*#__PURE__*/
      React.createElement("a", { className: "about__contact-email", href: "mailto:" + P.profile.email }, /*#__PURE__*/React.createElement(Icon, { name: "mail", size: 15 }), P.profile.email),
      P.profile.availability && /*#__PURE__*/React.createElement("p", { className: "about__contact-avail" }, /*#__PURE__*/React.createElement(Icon, { name: "check", size: 14 }), P.profile.availability)
      )
      )
      ));

  }

  /* ---------------------------------------------------------------- Footer */
  function PFooter() {
    return (/*#__PURE__*/
      React.createElement("footer", { className: "footer" }, /*#__PURE__*/
      React.createElement("div", { className: "wrap footer__inner" }, /*#__PURE__*/
      React.createElement("div", { className: "footer__brand" }, /*#__PURE__*/
      React.createElement("img", { src: "assets/logo-mark.svg", alt: "" }), /*#__PURE__*/
      React.createElement("span", null, P.profile.name)
      ), /*#__PURE__*/
      React.createElement("div", { className: "footer__meta" }, "\xA9 2026 \xB7 Climate & Sustainability \xB7 Built with the Adhi design system"), /*#__PURE__*/
      React.createElement("div", { className: "footer__social" }, /*#__PURE__*/
      React.createElement(IconButton, { as: "a", variant: "outline", "aria-label": "LinkedIn", href: P.profile.linkedin, target: "_blank", rel: "noopener noreferrer" }, /*#__PURE__*/React.createElement(Icon, { name: "linkedin", size: 18 })), /*#__PURE__*/
      React.createElement(IconButton, { as: "a", variant: "outline", "aria-label": "GitHub", href: P.repo, target: "_blank", rel: "noopener noreferrer" }, /*#__PURE__*/React.createElement(Icon, { name: "github", size: 18 })), /*#__PURE__*/
      React.createElement(IconButton, { as: "a", variant: "outline", "aria-label": "Email", href: "mailto:" + P.profile.email }, /*#__PURE__*/React.createElement(Icon, { name: "mail", size: 18 }))
      )
      )
      ));

  }

  Object.assign(window, { PNav, PHero, PStatBand, PStories, PAbout, PFooter });
})();