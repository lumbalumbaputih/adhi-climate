/* COMPILED from js/sections.jsx. Do not edit directly; edit the .jsx and recompile. */
/* Portfolio sections: Nav, Hero, StatBand, Stories (interactive), About, Footer */
(function () {
  const {
    Button,
    IconButton,
    Eyebrow,
    Stat,
    Badge,
    Tag
  } = window.AdhiClimateDesignSystem_bcac21;
  const Icon = window.Icon;
  const P = window.PORTFOLIO;

  /* ----------------------------------------------------- scroll-reveal wrap */
  function Reveal({
    children,
    as = "div",
    className = "",
    delay = 0,
    ...rest
  }) {
    const ref = React.useRef(null);
    const [shown, setShown] = React.useState(false);
    React.useEffect(() => {
      const el = ref.current;
      if (!el) return;
      const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (reduce || typeof IntersectionObserver === "undefined") {
        setShown(true);
        return;
      }
      const io = new IntersectionObserver(entries => {
        entries.forEach(e => {
          if (e.isIntersecting) {
            setShown(true);
            io.disconnect();
          }
        });
      }, {
        threshold: 0.12,
        rootMargin: "0px 0px -8% 0px"
      });
      io.observe(el);
      return () => io.disconnect();
    }, []);
    const Tag = as;
    return /*#__PURE__*/React.createElement(Tag, {
      ref: ref,
      className: ["reveal", shown ? "reveal--in" : "", className].filter(Boolean).join(" "),
      style: delay ? {
        transitionDelay: delay + "ms"
      } : undefined,
      ...rest
    }, children);
  }

  /* ------------------------------------------------------ count-up + theme */
  function CountUp({
    end,
    dur = 1100
  }) {
    const [v, setV] = React.useState(0);
    const ref = React.useRef(null);
    React.useEffect(() => {
      const el = ref.current;
      if (!el) return;
      const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (reduce || typeof IntersectionObserver === "undefined" || typeof requestAnimationFrame === "undefined") {
        setV(end);
        return;
      }
      const io = new IntersectionObserver(es => {
        es.forEach(e => {
          if (e.isIntersecting) {
            io.disconnect();
            const t0 = performance.now();
            const tick = t => {
              const p = Math.min(1, (t - t0) / dur);
              setV(Math.round(end * (1 - Math.pow(1 - p, 3))));
              if (p < 1) requestAnimationFrame(tick);
            };
            requestAnimationFrame(tick);
          }
        });
      }, {
        threshold: 0.4
      });
      io.observe(el);
      return () => io.disconnect();
    }, [end]);
    return /*#__PURE__*/React.createElement("span", {
      ref: ref
    }, v);
  }
  function PThemeToggle() {
    const isDark = () => document.documentElement.getAttribute("data-theme") === "dark";
    const [dark, setDark] = React.useState(isDark);
    function toggle() {
      const next = !isDark();
      document.documentElement.setAttribute("data-theme", next ? "dark" : "light");
      try {
        localStorage.setItem("theme", next ? "dark" : "light");
      } catch (e) {}
      setDark(next);
    }
    return /*#__PURE__*/React.createElement(IconButton, {
      variant: "outline",
      "aria-label": dark ? "Switch to light mode" : "Switch to dark mode",
      onClick: toggle
    }, /*#__PURE__*/React.createElement(Icon, {
      name: dark ? "sun" : "moon",
      size: 17
    }));
  }

  /* ------------------------------------------------- interactive data table */
  function PDataTable({
    data,
    caption
  }) {
    const columns = data.columns || data.headers || [];
    const [sort, setSort] = React.useState({
      col: null,
      dir: 1
    });
    const toNum = s => {
      const n = parseFloat(String(s).replace(/[−–]/g, "-").replace(/[^0-9.\-]/g, ""));
      return isNaN(n) ? null : n;
    };
    const rows = React.useMemo(() => {
      if (sort.col === null) return data.rows;
      const i = sort.col;
      return data.rows.slice().sort((a, b) => {
        const na = toNum(a[i]),
          nb = toNum(b[i]);
        if (na !== null && nb !== null) return (na - nb) * sort.dir;
        return String(a[i]).localeCompare(String(b[i])) * sort.dir;
      });
    }, [data, sort]);
    const toggle = i => setSort(s => s.col === i ? {
      col: i,
      dir: -s.dir
    } : {
      col: i,
      dir: 1
    });
    return /*#__PURE__*/React.createElement("figure", {
      className: "dtable"
    }, /*#__PURE__*/React.createElement("div", {
      className: "dtable__scroll"
    }, /*#__PURE__*/React.createElement("table", {
      className: "dtable__table"
    }, /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, columns.map((c, i) => /*#__PURE__*/React.createElement("th", {
      key: i,
      className: "dtable__th" + (sort.col === i ? " dtable__th--active" : ""),
      "aria-sort": sort.col === i ? sort.dir > 0 ? "ascending" : "descending" : "none",
      onClick: () => toggle(i)
    }, c, /*#__PURE__*/React.createElement("span", {
      className: "dtable__arrow"
    }, sort.col === i ? sort.dir > 0 ? "▲" : "▼" : "↕"))))), /*#__PURE__*/React.createElement("tbody", null, rows.map((r, ri) => /*#__PURE__*/React.createElement("tr", {
      key: ri
    }, r.map((cell, ci) => /*#__PURE__*/React.createElement("td", {
      key: ci
    }, cell))))))), caption && /*#__PURE__*/React.createElement("figcaption", {
      className: "dtable__cap"
    }, caption, " · tap a column to sort"));
  }

  /* -------------------------------------------------------------------- Nav */
  function PNav({
    onContact
  }) {
    return /*#__PURE__*/React.createElement("header", {
      className: "nav"
    }, /*#__PURE__*/React.createElement("div", {
      className: "wrap nav__inner"
    }, /*#__PURE__*/React.createElement("a", {
      className: "nav__brand",
      href: "#top"
    }, /*#__PURE__*/React.createElement("img", {
      src: "assets/logo-mark.svg",
      alt: ""
    }), /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("span", {
      className: "nav__name"
    }, P.profile.name), /*#__PURE__*/React.createElement("span", {
      className: "nav__role"
    }, P.profile.role))), /*#__PURE__*/React.createElement("nav", {
      className: "nav__links"
    }, /*#__PURE__*/React.createElement("a", {
      className: "nav__link",
      href: "#work"
    }, "Projects"), /*#__PURE__*/React.createElement("a", {
      className: "nav__link",
      href: "#about"
    }, "About")), /*#__PURE__*/React.createElement("div", {
      className: "nav__actions"
    }, /*#__PURE__*/React.createElement(PThemeToggle, null), /*#__PURE__*/React.createElement(Button, {
      variant: "secondary",
      size: "sm",
      as: "a",
      href: P.repo,
      iconLeft: /*#__PURE__*/React.createElement(Icon, {
        name: "file-text",
        size: 16
      })
    }, "CV"), /*#__PURE__*/React.createElement(Button, {
      variant: "primary",
      size: "sm",
      onClick: onContact,
      iconRight: /*#__PURE__*/React.createElement(Icon, {
        name: "arrow-right",
        size: 16
      })
    }, "Get in touch"))));
  }

  /* ------------------------------------------------------------------ Hero */
  function PHero({
    onContact
  }) {
    return /*#__PURE__*/React.createElement("section", {
      className: "hero hero--center",
      id: "top"
    }, /*#__PURE__*/React.createElement("div", {
      className: "wrap hero__inner"
    }, /*#__PURE__*/React.createElement("div", {
      className: "hero__eyebrow"
    }, /*#__PURE__*/React.createElement(Eyebrow, {
      tick: true
    }, "Climate & Sustainability · WA")), /*#__PURE__*/React.createElement("h1", {
      className: "hero__title"
    }, "I got curious about Western Australia's ", /*#__PURE__*/React.createElement("span", {
      className: "accent"
    }, "climate"), ", so I started digging."), /*#__PURE__*/React.createElement("p", {
      className: "hero__lead"
    }, P.profile.intro), /*#__PURE__*/React.createElement("div", {
      className: "hero__actions"
    }, /*#__PURE__*/React.createElement(Button, {
      variant: "primary",
      size: "lg",
      onClick: onContact,
      iconRight: /*#__PURE__*/React.createElement(Icon, {
        name: "arrow-right",
        size: 18
      })
    }, "Get in touch"), /*#__PURE__*/React.createElement(Button, {
      variant: "ghost",
      size: "lg",
      as: "a",
      href: "#work",
      iconRight: /*#__PURE__*/React.createElement(Icon, {
        name: "arrow-down-right",
        size: 18
      })
    }, "See the projects")), /*#__PURE__*/React.createElement("div", {
      className: "hero__meta"
    }, /*#__PURE__*/React.createElement("span", {
      className: "hero__meta-item"
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "map-pin",
      size: 16
    }), P.profile.location), /*#__PURE__*/React.createElement("span", {
      className: "hero__meta-item"
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "leaf",
      size: 16
    }), "Physical risk · Climate data · AASB S2"))));
  }

  /* ------------------------------------------------------------- StatBand */
  function PStatBand() {
    return /*#__PURE__*/React.createElement("section", {
      className: "statband"
    }, /*#__PURE__*/React.createElement("div", {
      className: "wrap statband__grid"
    }, P.stats.map((s, i) => {
      const n = parseInt(s.value, 10);
      const value = String(n) === String(s.value) ? /*#__PURE__*/React.createElement(CountUp, {
        end: n
      }) : s.value;
      return /*#__PURE__*/React.createElement(Reveal, {
        className: "statband__cell",
        key: i,
        delay: i * 80
      }, /*#__PURE__*/React.createElement(Stat, {
        label: s.label,
        value: value,
        unit: s.unit,
        delta: s.delta,
        trend: s.trend || "neutral",
        caption: s.caption,
        size: "md"
      }));
    })));
  }

  /* ---------------------------------------------------------------- Stories */
  function statusVariant(s) {
    if (["Live", "Adopted", "Delivered", "Published", "Complete"].includes(s)) return "leaf";
    if (["In progress", "Reported"].includes(s)) return "accent";
    return "neutral";
  }
  function PChart({
    vizKey,
    spec
  }) {
    const AC = window.AdhiCharts || {};
    const CD = (window.CHARTDATA || {})[vizKey] || {};
    let data = CD[spec.key];
    if (!data) return null;
    if (spec.sub) data = Object.assign({}, data[spec.sub], {
      ylabel: data.ylabel
    });
    if (spec.keys) data = Object.assign({}, data, {
      keys: spec.keys
    });
    const Comp = {
      line: AC.LineChart,
      bar: AC.BarChart,
      scatter: AC.ScatterChart,
      heat: AC.HeatTable
    }[spec.type];
    return Comp ? React.createElement(Comp, {
      data,
      label: spec.title
    }) : null;
  }
  const SCROLLY_STEPS = [{
    eyebrow: "The setup",
    text: "Forty years of cyclones near Western Australia. As the climate warms, two things are worth watching together: how warm the ocean was, and how strong the storms got."
  }, {
    eyebrow: "The ocean warmed",
    text: "The sea where these cyclones form rose by about 0.5 °C since the 1980s. The trend is unmistakable, and statistically rock solid."
  }, {
    eyebrow: "The storms did not",
    text: "If warmer water meant stronger storms, peak winds should climb too. They didn't. Mean peak wind actually edged downward over the same years."
  }, {
    eyebrow: "So they came apart",
    text: "Warmer years were not stronger-storm years (correlation r = −0.22). Ocean heat and storm strength decoupled, which is exactly why WA's future cyclone risk can't be read straight off the recent record."
  }];
  function ScrollyChart({
    D,
    stage
  }) {
    const W = 560,
      H = 340,
      M = {
        l: 46,
        r: 46,
        t: 16,
        b: 32
      };
    const IW = W - M.l - M.r,
      IH = H - M.t - M.b;
    const x0 = 1985,
      x1 = 2024;
    const xs = y => M.l + (y - x0) / (x1 - x0) * IW;
    const wv = D.wind.map(p => p[1]).concat([D.windTrend[1], D.windTrend[3]]);
    const sv = D.sst.map(p => p[1]).concat([D.sstTrend[1], D.sstTrend[3]]);
    const wlo = Math.min.apply(null, wv) - 4,
      whi = Math.max.apply(null, wv) + 4;
    const slo = Math.min.apply(null, sv) - 0.08,
      shi = Math.max.apply(null, sv) + 0.08;
    const ysW = v => M.t + IH - (v - wlo) / (whi - wlo) * IH;
    const ysS = v => M.t + IH - (v - slo) / (shi - slo) * IH;
    const ln = (arr, f) => arr.map((p, i) => (i ? "L" : "M") + xs(p[0]).toFixed(1) + " " + f(p[1]).toFixed(1)).join(" ");
    return /*#__PURE__*/React.createElement("svg", {
      viewBox: `0 0 ${W} ${H}`,
      className: "chart__svg scrolly__svg",
      role: "img",
      "aria-label": "Ocean temperature rose between 1985 and 2024 while cyclone peak winds did not."
    }, [0, 1, 2].map(i => {
      const v = wlo + (whi - wlo) * i / 2;
      return /*#__PURE__*/React.createElement("g", {
        key: "w" + i
      }, /*#__PURE__*/React.createElement("line", {
        x1: M.l,
        x2: M.l + IW,
        y1: ysW(v),
        y2: ysW(v),
        className: "chart__grid"
      }), /*#__PURE__*/React.createElement("text", {
        x: M.l - 8,
        y: ysW(v) + 3,
        textAnchor: "end",
        className: "chart__tick"
      }, Math.round(v)));
    }), [0, 1, 2].map(i => {
      const v = slo + (shi - slo) * i / 2;
      return /*#__PURE__*/React.createElement("text", {
        key: "s" + i,
        x: M.l + IW + 8,
        y: ysS(v) + 3,
        textAnchor: "start",
        className: "chart__tick",
        style: {
          fill: "var(--accent)"
        }
      }, (v > 0 ? "+" : "") + v.toFixed(1));
    }), /*#__PURE__*/React.createElement("text", {
      x: xs(1985),
      y: H - M.b + 18,
      textAnchor: "middle",
      className: "chart__tick"
    }, "1985"), /*#__PURE__*/React.createElement("text", {
      x: xs(2005),
      y: H - M.b + 18,
      textAnchor: "middle",
      className: "chart__tick"
    }, "2005"), /*#__PURE__*/React.createElement("text", {
      x: xs(2024),
      y: H - M.b + 18,
      textAnchor: "middle",
      className: "chart__tick"
    }, "2024"), /*#__PURE__*/React.createElement("g", {
      className: "scrolly__series",
      style: {
        opacity: stage >= 1 ? 1 : 0.12
      }
    }, /*#__PURE__*/React.createElement("line", {
      className: "chart__trend",
      style: {
        stroke: "var(--accent)"
      },
      x1: xs(D.sstTrend[0]),
      y1: ysS(D.sstTrend[1]),
      x2: xs(D.sstTrend[2]),
      y2: ysS(D.sstTrend[3])
    }), /*#__PURE__*/React.createElement("path", {
      className: "scrolly__line",
      style: {
        stroke: "var(--accent)"
      },
      d: ln(D.sst, ysS)
    })), /*#__PURE__*/React.createElement("g", {
      className: "scrolly__series",
      style: {
        opacity: stage >= 2 ? 1 : 0
      }
    }, /*#__PURE__*/React.createElement("line", {
      className: "chart__trend",
      style: {
        stroke: "#FF5C39"
      },
      x1: xs(D.windTrend[0]),
      y1: ysW(D.windTrend[1]),
      x2: xs(D.windTrend[2]),
      y2: ysW(D.windTrend[3])
    }), /*#__PURE__*/React.createElement("path", {
      className: "scrolly__line",
      style: {
        stroke: "#FF5C39"
      },
      d: ln(D.wind, ysW)
    })), stage >= 3 && /*#__PURE__*/React.createElement("text", {
      x: M.l + IW - 4,
      y: M.t + 15,
      textAnchor: "end",
      className: "scrolly__note"
    }, "no link · r = −0.22"));
  }
  function PScrolly() {
    const D = window.SCROLLYDATA;
    const [stage, setStage] = React.useState(1);
    const steps = React.useRef([]);
    React.useEffect(() => {
      if (typeof IntersectionObserver === "undefined") {
        setStage(3);
        return;
      }
      const io = new IntersectionObserver(entries => {
        entries.forEach(e => {
          if (e.isIntersecting) setStage(Number(e.target.dataset.step));
        });
      }, {
        rootMargin: "-45% 0px -45% 0px",
        threshold: 0
      });
      steps.current.forEach(el => el && io.observe(el));
      return () => io.disconnect();
    }, []);
    if (!D) return null;
    return /*#__PURE__*/React.createElement("div", {
      className: "scrolly"
    }, /*#__PURE__*/React.createElement("div", {
      className: "scrolly__graphic"
    }, /*#__PURE__*/React.createElement("div", {
      className: "story__chart-title"
    }, "Ocean temperature vs storm strength, 1985–2024"), /*#__PURE__*/React.createElement(ScrollyChart, {
      D: D,
      stage: stage
    }), /*#__PURE__*/React.createElement("div", {
      className: "scrolly__legend"
    }, /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("span", {
      className: "scrolly__sw",
      style: {
        background: "var(--accent)"
      }
    }), "Ocean temperature"), /*#__PURE__*/React.createElement("span", null, /*#__PURE__*/React.createElement("span", {
      className: "scrolly__sw",
      style: {
        background: "#FF5C39"
      }
    }), "Cyclone peak wind"))), /*#__PURE__*/React.createElement("div", {
      className: "scrolly__steps"
    }, SCROLLY_STEPS.map((s, i) => /*#__PURE__*/React.createElement("div", {
      className: "scrolly__step",
      key: i,
      "data-step": i,
      ref: el => steps.current[i] = el
    }, /*#__PURE__*/React.createElement("div", {
      className: "scrolly__card" + (stage === i ? " is-active" : "")
    }, /*#__PURE__*/React.createElement("div", {
      className: "scrolly__eyebrow"
    }, s.eyebrow), /*#__PURE__*/React.createElement("p", null, s.text))))));
  }

  /* A horizontal, scroll-snapping rail of "deep-dive" cards (charts + data
     tables). This is the "scroll sideways to learn more" surface: the key
     reading (title, findings, why-it-matters) stays vertical and skimmable,
     while the heavier evidence lives in cards you swipe through. */
  function DeepRail({
    cards,
    vizKey
  }) {
    const trackRef = React.useRef(null);
    const [atStart, setAtStart] = React.useState(true);
    const [atEnd, setAtEnd] = React.useState(false);
    const sync = React.useCallback(() => {
      const el = trackRef.current;
      if (!el) return;
      setAtStart(el.scrollLeft <= 2);
      setAtEnd(el.scrollLeft + el.clientWidth >= el.scrollWidth - 2);
    }, []);
    React.useEffect(() => {
      sync();
      const el = trackRef.current;
      if (!el) return;
      el.addEventListener("scroll", sync, {
        passive: true
      });
      window.addEventListener("resize", sync);
      return () => {
        el.removeEventListener("scroll", sync);
        window.removeEventListener("resize", sync);
      };
    }, [sync]);
    function nudge(dir) {
      const el = trackRef.current;
      if (!el) return;
      const item = el.querySelector(".rail__item");
      const gap = 20;
      const step = item ? item.getBoundingClientRect().width + gap : el.clientWidth * 0.85;
      const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      el.scrollBy({
        left: dir * step,
        behavior: reduce ? "auto" : "smooth"
      });
    }
    return /*#__PURE__*/React.createElement("div", {
      className: "rail"
    }, /*#__PURE__*/React.createElement("div", {
      className: "rail__head"
    }, /*#__PURE__*/React.createElement("div", {
      className: "rail__hint"
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "arrow-right",
      size: 14
    }), "Swipe through ", cards.length, " views"), /*#__PURE__*/React.createElement("div", {
      className: "rail__nav"
    }, /*#__PURE__*/React.createElement(IconButton, {
      variant: "outline",
      size: "sm",
      "aria-label": "Previous",
      disabled: atStart,
      onClick: () => nudge(-1)
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "arrow-right",
      size: 16,
      style: {
        transform: "rotate(180deg)"
      }
    })), /*#__PURE__*/React.createElement(IconButton, {
      variant: "outline",
      size: "sm",
      "aria-label": "Next",
      disabled: atEnd,
      onClick: () => nudge(1)
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "arrow-right",
      size: 16
    })))), /*#__PURE__*/React.createElement("div", {
      className: "rail__track",
      ref: trackRef
    }, cards.map((c, i) => /*#__PURE__*/React.createElement("div", {
      className: "rail__item" + (c.wide ? " rail__item--wide" : ""),
      key: i
    }, /*#__PURE__*/React.createElement("div", {
      className: "railcard"
    }, /*#__PURE__*/React.createElement("div", {
      className: "story__chart-title"
    }, c.title), c.kind === "chart" ? /*#__PURE__*/React.createElement(PChart, {
      vizKey: vizKey,
      spec: c.spec
    }) : /*#__PURE__*/React.createElement(PDataTable, {
      data: c.data,
      caption: c.caption
    }))))));
  }
  function PStory({
    p,
    index
  }) {
    const hasViz = p.viz && p.viz.length > 0 && window.AdhiCharts && window.CHARTDATA;

    // Collect everything heavy into one ordered list of rail cards: charts
    // first, then any scoreboard / raw-data table.
    const cards = [];
    if (hasViz) p.viz.forEach(spec => cards.push({
      kind: "chart",
      title: spec.title,
      spec
    }));
    if (p.scoreboard) cards.push({
      kind: "table",
      title: "Disclosure scores, 0 to 4",
      data: p.scoreboard,
      caption: "Disclosure scores, 0 to 4",
      wide: true
    });
    if (p.dataset) cards.push({
      kind: "table",
      title: p.dataset.caption,
      data: p.dataset,
      caption: p.dataset.caption,
      wide: true
    });
    return /*#__PURE__*/React.createElement("section", {
      className: "story",
      id: p.id
    }, /*#__PURE__*/React.createElement("div", {
      className: "wrap"
    }, /*#__PURE__*/React.createElement(Reveal, {
      className: "story__head"
    }, /*#__PURE__*/React.createElement("div", {
      className: "story__tagrow"
    }, /*#__PURE__*/React.createElement(Eyebrow, {
      tick: true
    }, "Project ", index + 1, " · ", p.year), /*#__PURE__*/React.createElement(Badge, {
      variant: statusVariant(p.status),
      dot: true
    }, p.status)), /*#__PURE__*/React.createElement("h2", {
      className: "story__title"
    }, p.title), /*#__PURE__*/React.createElement("p", {
      className: "story__hook"
    }, p.headline), /*#__PURE__*/React.createElement("p", {
      className: "story__lead"
    }, p.body)), /*#__PURE__*/React.createElement(Reveal, {
      className: "story__findings",
      delay: 80
    }, p.findings.map((f, i) => /*#__PURE__*/React.createElement("div", {
      className: "pfind",
      key: i
    }, /*#__PURE__*/React.createElement("div", {
      className: "pfind__v"
    }, /*#__PURE__*/React.createElement("span", {
      className: "v"
    }, f.value), f.unit && /*#__PURE__*/React.createElement("span", {
      className: "u"
    }, f.unit)), /*#__PURE__*/React.createElement("div", {
      className: "pfind__label"
    }, f.label), /*#__PURE__*/React.createElement("div", {
      className: "pfind__text"
    }, f.text)))), /*#__PURE__*/React.createElement(Reveal, {
      as: "p",
      className: "story__meaning",
      delay: 120
    }, /*#__PURE__*/React.createElement("span", {
      className: "story__meaning-tag"
    }, "Why it matters"), p.meaning), cards.length > 1 && /*#__PURE__*/React.createElement(Reveal, {
      className: "story__deep",
      delay: 120
    }, /*#__PURE__*/React.createElement(DeepRail, {
      cards: cards,
      vizKey: p.vizKey
    })), cards.length === 1 && /*#__PURE__*/React.createElement(Reveal, {
      className: "story__deep story__deep--solo",
      delay: 120
    }, /*#__PURE__*/React.createElement("div", {
      className: "rail__item rail__item--wide"
    }, /*#__PURE__*/React.createElement("div", {
      className: "railcard"
    }, /*#__PURE__*/React.createElement("div", {
      className: "story__chart-title"
    }, cards[0].title), cards[0].kind === "chart" ? /*#__PURE__*/React.createElement(PChart, {
      vizKey: p.vizKey,
      spec: cards[0].spec
    }) : /*#__PURE__*/React.createElement(PDataTable, {
      data: cards[0].data,
      caption: cards[0].caption
    })))), p.hasMap && window.MAPDATA && window.AdhiCharts && window.AdhiCharts.MapChart && /*#__PURE__*/React.createElement(Reveal, {
      className: "story__map"
    }, /*#__PURE__*/React.createElement("div", {
      className: "story__chart-title"
    }, "Where these storms tracked, season by season"), React.createElement(window.AdhiCharts.MapChart, {
      data: window.MAPDATA,
      label: "Tracks of the 193 cyclones that came within 500 km of WA, 1985 to 2024, coloured by peak wind."
    }), /*#__PURE__*/React.createElement("p", {
      className: "story__map-note"
    }, "Every cyclone that came within 500 km of the WA coast, coloured by peak wind. Hover a track to see the storm. Notice how they sweep in from the north-west toward the Pilbara and Kimberley.")), p.scrolly && window.SCROLLYDATA && /*#__PURE__*/React.createElement("div", {
      className: "story__scrolly"
    }, /*#__PURE__*/React.createElement(PScrolly, null)), /*#__PURE__*/React.createElement("div", {
      className: "story__links"
    }, p.resources.map((r, i) => /*#__PURE__*/React.createElement("a", {
      className: "story__link",
      key: i,
      href: r.href,
      target: "_blank",
      rel: "noopener noreferrer"
    }, /*#__PURE__*/React.createElement(Icon, {
      name: r.icon,
      size: 15
    }), r.label)))));
  }
  function PStories() {
    return /*#__PURE__*/React.createElement("div", {
      id: "work"
    }, /*#__PURE__*/React.createElement("section", {
      className: "section section--tight"
    }, /*#__PURE__*/React.createElement("div", {
      className: "wrap"
    }, /*#__PURE__*/React.createElement(Reveal, {
      className: "section-head"
    }, /*#__PURE__*/React.createElement(Eyebrow, {
      tick: true
    }, "Personal projects"), /*#__PURE__*/React.createElement("h2", null, "Built out of curiosity."), /*#__PURE__*/React.createElement("p", null, "Three projects I took on myself, simply because I love working with data and wanted answers. Each one started with a Western Australian climate question I wanted to work through from the raw data myself, then check my numbers against the published science. No client, no brief, just curiosity and a respect for what the data actually says.")))), P.projects.map((p, i) => /*#__PURE__*/React.createElement(PStory, {
      key: p.id,
      p: p,
      index: i
    })));
  }

  /* ----------------------------------------------------------------- About */
  /* Personal intro — moved up top, right under the hero, as the "who I am". */
  function PIntro() {
    return /*#__PURE__*/React.createElement("section", {
      className: "section section--tight intro",
      id: "about"
    }, /*#__PURE__*/React.createElement("div", {
      className: "wrap"
    }, /*#__PURE__*/React.createElement(Reveal, {
      className: "intro__body"
    }, /*#__PURE__*/React.createElement(Eyebrow, {
      tick: true
    }, "About"), /*#__PURE__*/React.createElement("h2", {
      className: "intro__title"
    }, "Hi, I'm Adhi."), /*#__PURE__*/React.createElement("p", {
      className: "intro__lead"
    }, "I'm studying a Master of Environment and Climate Emergency at Curtin University, now in my second year with two semesters to go. Right now I'm looking for an internship in sustainability, somewhere I can turn this kind of climate-data work into real impact for a team."), /*#__PURE__*/React.createElement("p", null, "I've arrived here from a few directions. I trained as a naval architect and marine engineer, spent two years as a business analyst in regional Western Australia, and worked as a hatchery technician while completing a Diploma of Aquaculture. The common thread has always been the same: taking messy, real-world data and turning it into something a team can act on."), /*#__PURE__*/React.createElement("p", null, "This portfolio is where I bring that together: real Western Australian climate data, honest analysis, and findings written so anyone can follow them, framed for the disclosure rules companies now have to meet. I care as much about getting the cause right as I do about the headline number."), /*#__PURE__*/React.createElement("div", {
      className: "about__tags"
    }, /*#__PURE__*/React.createElement(Tag, null, "Physical climate risk"), /*#__PURE__*/React.createElement(Tag, null, "AASB S2"), /*#__PURE__*/React.createElement(Tag, null, "IBTrACS / BOM"), /*#__PURE__*/React.createElement(Tag, null, "Trend detection"), /*#__PURE__*/React.createElement(Tag, null, "Disclosure scoring")))));
  }

  /* Get-in-touch card — kept at the bottom as the closing call to action. */
  function PContact() {
    return /*#__PURE__*/React.createElement("section", {
      className: "section contactband"
    }, /*#__PURE__*/React.createElement("div", {
      className: "wrap"
    }, /*#__PURE__*/React.createElement(Reveal, {
      as: "aside",
      id: "contact",
      className: "about__contact about__contact--center"
    }, /*#__PURE__*/React.createElement(Eyebrow, {
      tone: "leaf",
      tick: true
    }, "Get in touch"), /*#__PURE__*/React.createElement("h3", {
      className: "about__contact-title"
    }, "Open to sustainability internships."), /*#__PURE__*/React.createElement("p", null, "If you're hiring, or you just want to talk about WA climate, I'd love to hear from you."), /*#__PURE__*/React.createElement("div", {
      className: "about__contact-actions"
    }, /*#__PURE__*/React.createElement(Button, {
      variant: "leaf",
      size: "lg",
      fullWidth: true,
      as: "a",
      href: "mailto:" + P.profile.email,
      iconLeft: /*#__PURE__*/React.createElement(Icon, {
        name: "mail",
        size: 18
      })
    }, "Email me"), /*#__PURE__*/React.createElement(Button, {
      variant: "secondary",
      size: "lg",
      fullWidth: true,
      as: "a",
      href: P.profile.linkedin,
      target: "_blank",
      rel: "noopener noreferrer",
      iconLeft: /*#__PURE__*/React.createElement(Icon, {
        name: "linkedin",
        size: 18
      })
    }, "LinkedIn")), /*#__PURE__*/React.createElement("a", {
      className: "about__contact-email",
      href: "mailto:" + P.profile.email
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "mail",
      size: 15
    }), P.profile.email), P.profile.availability && /*#__PURE__*/React.createElement("p", {
      className: "about__contact-avail"
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "check",
      size: 14
    }), P.profile.availability))));
  }

  /* ---------------------------------------------------------------- Footer */
  function PFooter() {
    return /*#__PURE__*/React.createElement("footer", {
      className: "footer"
    }, /*#__PURE__*/React.createElement("div", {
      className: "wrap footer__inner"
    }, /*#__PURE__*/React.createElement("div", {
      className: "footer__brand"
    }, /*#__PURE__*/React.createElement("img", {
      src: "assets/logo-mark.svg",
      alt: ""
    }), /*#__PURE__*/React.createElement("span", null, P.profile.name)), /*#__PURE__*/React.createElement("div", {
      className: "footer__meta"
    }, "© 2026 · Climate & Sustainability · Built with the Adhi design system"), /*#__PURE__*/React.createElement("div", {
      className: "footer__social"
    }, /*#__PURE__*/React.createElement(IconButton, {
      as: "a",
      variant: "outline",
      "aria-label": "LinkedIn",
      href: P.profile.linkedin,
      target: "_blank",
      rel: "noopener noreferrer"
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "linkedin",
      size: 18
    })), /*#__PURE__*/React.createElement(IconButton, {
      as: "a",
      variant: "outline",
      "aria-label": "GitHub",
      href: P.repo,
      target: "_blank",
      rel: "noopener noreferrer"
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "github",
      size: 18
    })), /*#__PURE__*/React.createElement(IconButton, {
      as: "a",
      variant: "outline",
      "aria-label": "Email",
      href: "mailto:" + P.profile.email
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "mail",
      size: 18
    })))));
  }
  Object.assign(window, {
    PNav,
    PHero,
    PIntro,
    PStatBand,
    PStories,
    PContact,
    PFooter
  });
})();
