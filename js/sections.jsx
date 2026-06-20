/* Portfolio sections: Nav, Hero, StatBand, Stories (interactive), About, Footer */
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
      if (reduce || typeof IntersectionObserver === "undefined") { setShown(true); return; }
      const io = new IntersectionObserver((entries) => {
        entries.forEach((e) => { if (e.isIntersecting) { setShown(true); io.disconnect(); } });
      }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
      io.observe(el);
      return () => io.disconnect();
    }, []);
    const Tag = as;
    return (
      <Tag ref={ref}
        className={["reveal", shown ? "reveal--in" : "", className].filter(Boolean).join(" ")}
        style={delay ? { transitionDelay: delay + "ms" } : undefined}
        {...rest}>
        {children}
      </Tag>
    );
  }

  /* ------------------------------------------------------ count-up + theme */
  function CountUp({ end, dur = 1100 }) {
    const [v, setV] = React.useState(0);
    const ref = React.useRef(null);
    React.useEffect(() => {
      const el = ref.current; if (!el) return;
      const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      if (reduce || typeof IntersectionObserver === "undefined" || typeof requestAnimationFrame === "undefined") { setV(end); return; }
      const io = new IntersectionObserver((es) => {
        es.forEach((e) => {
          if (e.isIntersecting) {
            io.disconnect();
            const t0 = performance.now();
            const tick = (t) => { const p = Math.min(1, (t - t0) / dur); setV(Math.round(end * (1 - Math.pow(1 - p, 3)))); if (p < 1) requestAnimationFrame(tick); };
            requestAnimationFrame(tick);
          }
        });
      }, { threshold: 0.4 });
      io.observe(el);
      return () => io.disconnect();
    }, [end]);
    return <span ref={ref}>{v}</span>;
  }

  function PThemeToggle() {
    const isDark = () => document.documentElement.getAttribute("data-theme") === "dark";
    const [dark, setDark] = React.useState(isDark);
    function toggle() {
      const next = !isDark();
      document.documentElement.setAttribute("data-theme", next ? "dark" : "light");
      try { localStorage.setItem("theme", next ? "dark" : "light"); } catch (e) {}
      setDark(next);
    }
    return (
      <IconButton variant="outline" aria-label={dark ? "Switch to light mode" : "Switch to dark mode"} onClick={toggle}>
        <Icon name={dark ? "sun" : "moon"} size={17} />
      </IconButton>
    );
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
        const na = toNum(a[i]), nb = toNum(b[i]);
        if (na !== null && nb !== null) return (na - nb) * sort.dir;
        return String(a[i]).localeCompare(String(b[i])) * sort.dir;
      });
    }, [data, sort]);
    const toggle = (i) => setSort((s) => (s.col === i ? { col: i, dir: -s.dir } : { col: i, dir: 1 }));
    return (
      <figure className="dtable">
        <div className="dtable__scroll">
          <table className="dtable__table">
            <thead>
              <tr>
                {columns.map((c, i) => (
                  <th key={i}
                    className={"dtable__th" + (sort.col === i ? " dtable__th--active" : "")}
                    aria-sort={sort.col === i ? (sort.dir > 0 ? "ascending" : "descending") : "none"}
                    onClick={() => toggle(i)}>
                    {c}<span className="dtable__arrow">{sort.col === i ? (sort.dir > 0 ? "▲" : "▼") : "↕"}</span>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows.map((r, ri) => (
                <tr key={ri}>{r.map((cell, ci) => <td key={ci}>{cell}</td>)}</tr>
              ))}
            </tbody>
          </table>
        </div>
        {caption && <figcaption className="dtable__cap">{caption} · tap a column to sort</figcaption>}
      </figure>
    );
  }

  /* -------------------------------------------------------------------- Nav */
  function PNav({ onContact }) {
    return (
      <header className="nav">
        <div className="wrap nav__inner">
          <a className="nav__brand" href="#top">
            <img src="assets/logo-mark.svg" alt="" />
            <span>
              <span className="nav__name">{P.profile.name}</span>
              <span className="nav__role">{P.profile.role}</span>
            </span>
          </a>
          <nav className="nav__links">
            <a className="nav__link" href="#work">Projects</a>
            <a className="nav__link" href="#about">About</a>
          </nav>
          <div className="nav__actions">
            <PThemeToggle />
            <Button variant="secondary" size="sm" as="a" href={P.repo} iconLeft={<Icon name="file-text" size={16} />}>CV</Button>
            <Button variant="primary" size="sm" onClick={onContact} iconRight={<Icon name="arrow-right" size={16} />}>Get in touch</Button>
          </div>
        </div>
      </header>
    );
  }

  /* ------------------------------------------------------------------ Hero */
  function PHero({ onContact }) {
    return (
      <section className="hero" id="top">
        <div className="wrap">
          <div className="hero__inner">
            <div className="hero__eyebrow"><Eyebrow tick>Climate &amp; Sustainability · WA</Eyebrow></div>
            <h1 className="hero__title">I got curious about Western Australia's <span className="accent">climate</span>, so I started digging.</h1>
            <p className="hero__lead">{P.profile.intro}</p>
            <div className="hero__actions">
              <Button variant="primary" size="lg" onClick={onContact} iconRight={<Icon name="arrow-right" size={18} />}>Get in touch</Button>
              <Button variant="ghost" size="lg" as="a" href="#work" iconRight={<Icon name="arrow-down-right" size={18} />}>See the projects</Button>
            </div>
            <div className="hero__meta">
              <span className="hero__meta-item"><Icon name="map-pin" size={16} />{P.profile.location}</span>
              <span className="hero__meta-item"><Icon name="leaf" size={16} />Physical risk · Climate data · AASB S2</span>
            </div>
          </div>

          <Reveal id="about" className="hero__about" delay={120}>
            <h2 className="hero__about-title">Hi, I'm Adhi.</h2>
            <p className="hero__about-lead">
              I'm studying a Master of Environment and Climate Emergency at Curtin University, now in my second
              year with two semesters to go. Right now I'm looking for an internship in sustainability, somewhere
              I can turn this kind of climate-data work into real impact for a team.
            </p>
            <p>
              I've arrived here from a few directions. I trained as a naval architect and marine engineer, spent
              two years as a business analyst in regional Western Australia, and worked as a hatchery technician
              while completing a Diploma of Aquaculture. The common thread has always been the same: taking messy,
              real-world data and turning it into something a team can act on.
            </p>
            <p>
              This portfolio is where I bring that together: real Western Australian climate data, honest
              analysis, and findings written so anyone can follow them, framed for the disclosure rules companies
              now have to meet. I care as much about getting the cause right as I do about the headline number.
            </p>
            <div className="about__tags">
              <Tag>Physical climate risk</Tag><Tag>AASB S2</Tag><Tag>IBTrACS / BOM</Tag>
              <Tag>Trend detection</Tag><Tag>Disclosure scoring</Tag>
            </div>
          </Reveal>
        </div>
      </section>
    );
  }

  /* ------------------------------------------------------------- StatBand */
  function PStatBand() {
    return (
      <section className="statband">
        <div className="wrap statband__grid">
          {P.stats.map((s, i) => {
            const n = parseInt(s.value, 10);
            const value = String(n) === String(s.value) ? <CountUp end={n} /> : s.value;
            return (
              <Reveal className="statband__cell" key={i} delay={i * 80}>
                <Stat label={s.label} value={value} unit={s.unit} delta={s.delta} trend={s.trend || "neutral"} caption={s.caption} size="md" />
              </Reveal>
            );
          })}
        </div>
      </section>
    );
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
    { eyebrow: "So they came apart", text: "Warmer years were not stronger-storm years (correlation r = −0.22). Ocean heat and storm strength decoupled, which is exactly why WA's future cyclone risk can't be read straight off the recent record." },
  ];

  function ScrollyChart({ D, stage }) {
    const W = 560, H = 340, M = { l: 46, r: 46, t: 16, b: 32 };
    const IW = W - M.l - M.r, IH = H - M.t - M.b;
    const x0 = 1985, x1 = 2024;
    const xs = (y) => M.l + (y - x0) / (x1 - x0) * IW;
    const wv = D.wind.map((p) => p[1]).concat([D.windTrend[1], D.windTrend[3]]);
    const sv = D.sst.map((p) => p[1]).concat([D.sstTrend[1], D.sstTrend[3]]);
    const wlo = Math.min.apply(null, wv) - 4, whi = Math.max.apply(null, wv) + 4;
    const slo = Math.min.apply(null, sv) - 0.08, shi = Math.max.apply(null, sv) + 0.08;
    const ysW = (v) => M.t + IH - (v - wlo) / (whi - wlo) * IH;
    const ysS = (v) => M.t + IH - (v - slo) / (shi - slo) * IH;
    const ln = (arr, f) => arr.map((p, i) => (i ? "L" : "M") + xs(p[0]).toFixed(1) + " " + f(p[1]).toFixed(1)).join(" ");
    return (
      <svg viewBox={`0 0 ${W} ${H}`} className="chart__svg scrolly__svg" role="img" aria-label="Ocean temperature rose between 1985 and 2024 while cyclone peak winds did not.">
        {[0, 1, 2].map((i) => { const v = wlo + (whi - wlo) * i / 2; return (
          <g key={"w" + i}>
            <line x1={M.l} x2={M.l + IW} y1={ysW(v)} y2={ysW(v)} className="chart__grid" />
            <text x={M.l - 8} y={ysW(v) + 3} textAnchor="end" className="chart__tick">{Math.round(v)}</text>
          </g>); })}
        {[0, 1, 2].map((i) => { const v = slo + (shi - slo) * i / 2; return (
          <text key={"s" + i} x={M.l + IW + 8} y={ysS(v) + 3} textAnchor="start" className="chart__tick" style={{ fill: "var(--accent)" }}>{(v > 0 ? "+" : "") + v.toFixed(1)}</text>); })}
        <text x={xs(1985)} y={H - M.b + 18} textAnchor="middle" className="chart__tick">1985</text>
        <text x={xs(2005)} y={H - M.b + 18} textAnchor="middle" className="chart__tick">2005</text>
        <text x={xs(2024)} y={H - M.b + 18} textAnchor="middle" className="chart__tick">2024</text>
        <g className="scrolly__series" style={{ opacity: stage >= 1 ? 1 : 0.12 }}>
          <line className="chart__trend" style={{ stroke: "var(--accent)" }} x1={xs(D.sstTrend[0])} y1={ysS(D.sstTrend[1])} x2={xs(D.sstTrend[2])} y2={ysS(D.sstTrend[3])} />
          <path className="scrolly__line" style={{ stroke: "var(--accent)" }} d={ln(D.sst, ysS)} />
        </g>
        <g className="scrolly__series" style={{ opacity: stage >= 2 ? 1 : 0 }}>
          <line className="chart__trend" style={{ stroke: "#FF5C39" }} x1={xs(D.windTrend[0])} y1={ysW(D.windTrend[1])} x2={xs(D.windTrend[2])} y2={ysW(D.windTrend[3])} />
          <path className="scrolly__line" style={{ stroke: "#FF5C39" }} d={ln(D.wind, ysW)} />
        </g>
        {stage >= 3 && <text x={M.l + IW - 4} y={M.t + 15} textAnchor="end" className="scrolly__note">no link · r = −0.22</text>}
      </svg>
    );
  }

  /* Reusable scrollytelling shell: a sticky graphic on the left whose
     `stage` advances as the reader scrolls the step cards on the right.
     Pass a render-prop `children(stage)` to draw the graphic for each stage. */
  function Scrolly({ title, legend, steps, children }) {
    const [stage, setStage] = React.useState(1);
    const stepRefs = React.useRef([]);
    React.useEffect(() => {
      if (typeof IntersectionObserver === "undefined") { setStage(steps.length - 1); return; }
      const io = new IntersectionObserver((entries) => {
        entries.forEach((e) => { if (e.isIntersecting) setStage(Number(e.target.dataset.step)); });
      }, { rootMargin: "-45% 0px -45% 0px", threshold: 0 });
      stepRefs.current.forEach((el) => el && io.observe(el));
      return () => io.disconnect();
    }, [steps.length]);
    return (
      <div className="scrolly">
        <div className="scrolly__graphic">
          <div className="story__chart-title">{title}</div>
          {children(stage)}
          <div className="scrolly__legend">
            {legend.map((l, i) => (
              <span key={i}><span className="scrolly__sw" style={{ background: l.c }} />{l.t}</span>
            ))}
          </div>
        </div>
        <div className="scrolly__steps">
          {steps.map((s, i) => (
            <div className="scrolly__step" key={i} data-step={i} ref={(el) => (stepRefs.current[i] = el)}>
              <div className={"scrolly__card" + (stage === i ? " is-active" : "")}>
                <div className="scrolly__eyebrow">{s.eyebrow}</div>
                <p>{s.text}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  function PScrolly() {
    const D = window.SCROLLYDATA;
    if (!D) return null;
    return (
      <Scrolly
        title="Ocean temperature vs storm strength, 1985–2024"
        legend={[{ c: "var(--accent)", t: "Ocean temperature" }, { c: "#FF5C39", t: "Cyclone peak wind" }]}
        steps={SCROLLY_STEPS}>
        {(stage) => <ScrollyChart D={D} stage={stage} />}
      </Scrolly>
    );
  }

  /* ----- Rainfall step-change: the sudden ~2000 drop, revealed by scroll --- */
  const RAIN_SCROLLY_STEPS = [
    { eyebrow: "The question", text: "Seventy-four years of cool-season (April–October) rain across south-west WA, measured against the 1950s. Did it drift down slowly, or change all at once?" },
    { eyebrow: "Noisy, year to year", text: "Rain always bounces around — wet years, dry years. For five decades it wobbled near the old normal with no clear direction." },
    { eyebrow: "Then it broke", text: "Around the year 2000 the average dropped to a new, lower level. Not a slow slide but a step down — and the wet years never climbed back over it." },
    { eyebrow: "A drier normal", text: "The last 25 years sit about 19% below the 1950s and have stayed there. For Perth's water, wheatbelt farms and the banks that lend to them, this is the baseline to plan around now." },
  ];

  function RainScrollyChart({ D, stage }) {
    const W = 560, H = 340, M = { l: 48, r: 18, t: 18, b: 32 };
    const IW = W - M.l - M.r, IH = H - M.t - M.b;
    const x0 = 1950, x1 = 2024;
    const xs = (y) => M.l + (y - x0) / (x1 - x0) * IW;
    const yv = D.points.map((p) => p[1]).concat([D.pre.y, D.post.y]);
    const ylo = Math.min.apply(null, yv) - 6, yhi = Math.max.apply(null, yv) + 6;
    const ys = (v) => M.t + IH - (v - ylo) / (yhi - ylo) * IH;
    const ln = (arr) => arr.map((p, i) => (i ? "L" : "M") + xs(p[0]).toFixed(1) + " " + ys(p[1]).toFixed(1)).join(" ");
    const gy = [-30, -15, 0, 15, 30].filter((v) => v > ylo && v < yhi);
    return (
      <svg viewBox={`0 0 ${W} ${H}`} className="chart__svg scrolly__svg" role="img" aria-label="South-west WA cool-season rainfall fell to a new, lower level around the year 2000.">
        {gy.map((v) => (
          <g key={"g" + v}>
            <line x1={M.l} x2={M.l + IW} y1={ys(v)} y2={ys(v)} className={v === 0 ? "chart__axis" : "chart__grid"} />
            <text x={M.l - 8} y={ys(v) + 3} textAnchor="end" className="chart__tick">{(v > 0 ? "+" : "") + v + "%"}</text>
          </g>
        ))}
        {[1950, 1975, 2000, 2024].map((yr) => (
          <text key={"x" + yr} x={xs(yr)} y={H - M.b + 18} textAnchor="middle" className="chart__tick">{yr}</text>
        ))}
        <path className="scrolly__line" style={{ stroke: "var(--accent)", opacity: stage < 1 ? 0.12 : stage >= 2 ? 0.4 : 1 }} d={ln(D.points)} />
        {stage >= 2 && <line className="chart__guide" style={{ stroke: "#FF5C39", strokeDasharray: "4 4" }} x1={xs(2000)} x2={xs(2000)} y1={M.t} y2={M.t + IH} />}
        {stage >= 2 && <line className="chart__trend" style={{ stroke: "#5b6b7d" }} x1={xs(D.pre.x0)} y1={ys(D.pre.y)} x2={xs(D.pre.x1)} y2={ys(D.pre.y)} />}
        {stage >= 2 && <line className="chart__trend" style={{ stroke: "#FF5C39" }} x1={xs(D.post.x0)} y1={ys(D.post.y)} x2={xs(D.post.x1)} y2={ys(D.post.y)} />}
        {stage >= 2 && <text x={xs(1972)} y={ys(D.pre.y) - 9} textAnchor="middle" className="scrolly__note" style={{ fill: "#5b6b7d" }}>old normal</text>}
        {stage >= 3 && <text x={xs(2012)} y={ys(D.post.y) + 19} textAnchor="middle" className="scrolly__note">{"−" + D.drop + "% · new normal"}</text>}
      </svg>
    );
  }

  function PRainScrolly() {
    const D = window.RAINSCROLLYDATA;
    if (!D) return null;
    return (
      <Scrolly
        title="South-west WA cool-season rainfall, 1950–2024"
        legend={[{ c: "var(--accent)", t: "Annual rain vs 1950s" }, { c: "#FF5C39", t: "Average for the era" }]}
        steps={RAIN_SCROLLY_STEPS}>
        {(stage) => <RainScrollyChart D={D} stage={stage} />}
      </Scrolly>
    );
  }

  /* A horizontal, scroll-snapping rail of "deep-dive" cards (charts + data
     tables). This is the "scroll sideways to learn more" surface: the key
     reading (title, findings, why-it-matters) stays vertical and skimmable,
     while the heavier evidence lives in cards you swipe through. */
  function DeepRail({ cards, vizKey }) {
    const trackRef = React.useRef(null);
    const [atStart, setAtStart] = React.useState(true);
    const [atEnd, setAtEnd] = React.useState(false);

    const sync = React.useCallback(() => {
      const el = trackRef.current; if (!el) return;
      setAtStart(el.scrollLeft <= 2);
      setAtEnd(el.scrollLeft + el.clientWidth >= el.scrollWidth - 2);
    }, []);

    React.useEffect(() => {
      sync();
      const el = trackRef.current; if (!el) return;
      el.addEventListener("scroll", sync, { passive: true });
      window.addEventListener("resize", sync);
      return () => { el.removeEventListener("scroll", sync); window.removeEventListener("resize", sync); };
    }, [sync]);

    function nudge(dir) {
      const el = trackRef.current; if (!el) return;
      const item = el.querySelector(".rail__item");
      const gap = 20;
      const step = item ? item.getBoundingClientRect().width + gap : el.clientWidth * 0.85;
      const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      el.scrollBy({ left: dir * step, behavior: reduce ? "auto" : "smooth" });
    }

    return (
      <div className="rail">
        <div className="rail__head">
          <div className="rail__hint"><Icon name="arrow-right" size={14} />Swipe through {cards.length} views</div>
          <div className="rail__nav">
            <IconButton variant="outline" size="sm" aria-label="Previous" disabled={atStart} onClick={() => nudge(-1)}>
              <Icon name="arrow-right" size={16} style={{ transform: "rotate(180deg)" }} />
            </IconButton>
            <IconButton variant="outline" size="sm" aria-label="Next" disabled={atEnd} onClick={() => nudge(1)}>
              <Icon name="arrow-right" size={16} />
            </IconButton>
          </div>
        </div>
        <div className="rail__track" ref={trackRef}>
          {cards.map((c, i) => (
            <div className={"rail__item" + (c.wide ? " rail__item--wide" : "")} key={i}>
              <div className="railcard">
                <div className="story__chart-title">{c.title}</div>
                {c.kind === "chart"
                  ? <PChart vizKey={vizKey} spec={c.spec} />
                  : <PDataTable data={c.data} caption={c.caption} />}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  function PStory({ p, index }) {
    const hasViz = p.viz && p.viz.length > 0 && window.AdhiCharts && window.CHARTDATA;

    // Collect everything heavy into one ordered list of rail cards: charts
    // first, then any scoreboard / raw-data table.
    const cards = [];
    if (hasViz) p.viz.forEach((spec) => cards.push({ kind: "chart", title: spec.title, spec }));
    if (p.scoreboard) cards.push({ kind: "table", title: "Disclosure scores, 0 to 4", data: p.scoreboard, caption: "Disclosure scores, 0 to 4", wide: true });
    if (p.dataset) cards.push({ kind: "table", title: p.dataset.caption, data: p.dataset, caption: p.dataset.caption, wide: true });

    return (
      <section className="story" id={p.id}>
        <div className="wrap">
          <Reveal className="story__head">
            <div className="story__tagrow">
              <Eyebrow tick>Project {index + 1} · {p.year}</Eyebrow>
              <Badge variant={statusVariant(p.status)} dot>{p.status}</Badge>
            </div>
            <h2 className="story__title">{p.title}</h2>
            <p className="story__hook">{p.headline}</p>
            <p className="story__lead">{p.body}</p>
          </Reveal>

          <Reveal className="story__findings" delay={80}>
            {p.findings.map((f, i) => (
              <div className="pfind" key={i}>
                <div className="pfind__v"><span className="v">{f.value}</span>{f.unit && <span className="u">{f.unit}</span>}</div>
                <div className="pfind__label">{f.label}</div>
                <div className="pfind__text">{f.text}</div>
              </div>
            ))}
          </Reveal>

          <Reveal as="p" className="story__meaning" delay={120}>
            <span className="story__meaning-tag">Why it matters</span>{p.meaning}
          </Reveal>

          {p.radar && window.AdhiCharts && window.AdhiCharts.RadarChart && (
            <Reveal className="story__radar" delay={120}>
              <div className="story__chart-title">How the three compare, pillar by pillar</div>
              {React.createElement(window.AdhiCharts.RadarChart, { data: p.radar, label: "Radar chart comparing Rio Tinto, Woodside and BHP across the four AASB S2 pillars — governance, strategy, risk management, and metrics and targets — each scored out of 4." })}
              <p className="story__radar-note">Each company scored out of 4 on the four AASB S2 pillars. Toggle a company in the legend, or hover a point for its score. A bigger, rounder shape means more complete disclosure — but here's the catch this whole project turns on: reporting well (a big shape) is not the same as being low-risk.</p>
            </Reveal>
          )}

          {cards.length > 1 && (
            <Reveal className="story__deep" delay={120}>
              <DeepRail cards={cards} vizKey={p.vizKey} />
            </Reveal>
          )}
          {cards.length === 1 && (
            <Reveal className="story__deep story__deep--solo" delay={120}>
              <div className="rail__item rail__item--wide">
                <div className="railcard">
                  <div className="story__chart-title">{cards[0].title}</div>
                  {cards[0].kind === "chart"
                    ? <PChart vizKey={p.vizKey} spec={cards[0].spec} />
                    : <PDataTable data={cards[0].data} caption={cards[0].caption} />}
                </div>
              </div>
            </Reveal>
          )}

          {p.hasMap && window.MAPDATA && window.AdhiCharts && window.AdhiCharts.MapChart && (
            <Reveal className="story__map">
              <div className="story__chart-title">Where these storms tracked, season by season</div>
              {React.createElement(window.AdhiCharts.MapChart, { data: window.MAPDATA, label: "Tracks of the 193 cyclones that came within 500 km of WA, 1985 to 2024, coloured by peak wind." })}
              <p className="story__map-note">Every cyclone that came within 500 km of the WA coast, coloured by peak wind. Hover a track to see the storm, or use the sliders to filter by season and storm strength. Notice how they sweep in from the north-west toward the Pilbara and Kimberley.</p>
            </Reveal>
          )}

          {p.scrolly && window.SCROLLYDATA && (
            <div className="story__scrolly">
              <PScrolly />
            </div>
          )}

          {p.rainMap && window.RAINMAPDATA && window.AdhiCharts && window.AdhiCharts.RainMapChart && (
            <Reveal className="story__map">
              <div className="story__chart-title">Where the drying hit, decade by decade</div>
              {React.createElement(window.AdhiCharts.RainMapChart, { data: window.RAINMAPDATA, label: "Map of seven south-west WA weather stations, each coloured by how far that decade's cool-season rainfall sat below or above its 1950s baseline." })}
              <p className="story__map-note">Seven long-running weather stations across the south-west, coloured by how far each decade's cool-season rain sat below (red) or above (blue) its 1950s level. Drag the slider and watch the whole region turn red after 2000 — the wheatbelt stations hardest of all.</p>
            </Reveal>
          )}

          {p.rainScrolly && window.RAINSCROLLYDATA && (
            <div className="story__scrolly">
              <PRainScrolly />
            </div>
          )}

          <div className="story__links">
            {p.resources.map((r, i) => (
              <a className="story__link" key={i} href={r.href} target="_blank" rel="noopener noreferrer">
                <Icon name={r.icon} size={15} />{r.label}
              </a>
            ))}
          </div>
        </div>
      </section>
    );
  }

  function PStories() {
    return (
      <div id="work">
        <section className="section section--tight">
          <div className="wrap">
            <Reveal className="section-head section-head--slim">
              <Eyebrow tick>Personal projects</Eyebrow>
              <p>Three projects I took on myself, simply because I love working with data and wanted answers. Each one started with a Western Australian climate question I wanted to work through from the raw data myself, then check my numbers against the published science. No client, no brief, just a respect for what the data actually says.</p>
            </Reveal>
          </div>
        </section>
        {P.projects.map((p, i) => <PStory key={p.id} p={p} index={i} />)}
      </div>
    );
  }

  /* Get-in-touch card — kept at the bottom as the closing call to action. */
  function PContact() {
    return (
      <section className="section contactband">
        <div className="wrap">
          <Reveal as="aside" id="contact" className="about__contact about__contact--center">
            <Eyebrow tone="leaf" tick>Get in touch</Eyebrow>
            <h3 className="about__contact-title">Open to sustainability internships.</h3>
            <p>If you're hiring, or you just want to talk about WA climate, I'd love to hear from you.</p>
            <div className="about__contact-actions">
              <Button variant="leaf" size="lg" fullWidth as="a" href={"mailto:" + P.profile.email} iconLeft={<Icon name="mail" size={18} />}>Email me</Button>
              <Button variant="secondary" size="lg" fullWidth as="a" href={P.profile.linkedin} target="_blank" rel="noopener noreferrer" iconLeft={<Icon name="linkedin" size={18} />}>LinkedIn</Button>
            </div>
            <a className="about__contact-email" href={"mailto:" + P.profile.email}><Icon name="mail" size={15} />{P.profile.email}</a>
            {P.profile.availability && <p className="about__contact-avail"><Icon name="check" size={14} />{P.profile.availability}</p>}
          </Reveal>
        </div>
      </section>
    );
  }

  /* ---------------------------------------------------------------- Footer */
  function PFooter() {
    return (
      <footer className="footer">
        <div className="wrap footer__inner">
          <div className="footer__brand">
            <img src="assets/logo-mark.svg" alt="" />
            <span>{P.profile.name}</span>
          </div>
          <div className="footer__meta">© 2026 · Climate &amp; Sustainability · Built with the Adhi design system</div>
          <div className="footer__social">
            <IconButton as="a" variant="outline" aria-label="LinkedIn" href={P.profile.linkedin} target="_blank" rel="noopener noreferrer"><Icon name="linkedin" size={18} /></IconButton>
            <IconButton as="a" variant="outline" aria-label="GitHub" href={P.repo} target="_blank" rel="noopener noreferrer"><Icon name="github" size={18} /></IconButton>
            <IconButton as="a" variant="outline" aria-label="Email" href={"mailto:" + P.profile.email}><Icon name="mail" size={18} /></IconButton>
          </div>
        </div>
      </footer>
    );
  }

  Object.assign(window, { PNav, PHero, PStatBand, PStories, PContact, PFooter });
})();
