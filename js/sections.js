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
            <Button variant="secondary" size="sm" as="a" href={P.repo} iconLeft={<Icon name="file-text" size={16} />}>CV</Button>
            <Button variant="primary" size="sm" onClick={onContact} iconRight={<Icon name="arrow-right" size={16} />}>Get in touch</Button>
          </div>
        </div>
      </header>
    );
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
      { y: "2019–2024", v: "+0.26", h: 82 },
    ];
    return (
      <section className="hero" id="top">
        <div className="wrap hero__grid">
          <div>
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

          <div className="hero__panel">
            <div className="hero__panel-label">WA cyclone-region ocean temperature · <span style={{ whiteSpace: "nowrap" }}>1985–2024</span></div>
            <div className="hero__chart" role="img" aria-label="WA cyclone-region ocean temperature, 1985 to 2024: five-year averages rise from −0.20 °C to +0.26 °C versus the 1991–2020 average, about 0.5 °C of warming.">
              {bars.map((b, i) => (
                <div key={i} className="hero__bar-wrap">
                  <div className="hero__bar" style={{ height: b.h + "%" }}>
                    <span className="hero__bar-tip" aria-hidden="true">{b.y}<b>{b.v} °C</b><em>vs 1991–2020 avg</em></span>
                  </div>
                </div>
              ))}
            </div>
            <div className="hero__panel-stat">
              <span><span className="big">40</span> <span className="unit">yrs analysed</span></span>
              <span className="delta">▴ +0.5 °C since the 1980s</span>
            </div>
          </div>
        </div>
      </section>
    );
  }

  /* ------------------------------------------------------------- StatBand */
  function PStatBand() {
    return (
      <section className="statband">
        <div className="wrap statband__grid">
          {P.stats.map((s, i) => (
            <Reveal className="statband__cell" key={i} delay={i * 80}>
              <Stat label={s.label} value={s.value} unit={s.unit} delta={s.delta} trend={s.trend || "neutral"} caption={s.caption} size="md" />
            </Reveal>
          ))}
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

  function PScrolly() {
    const D = window.SCROLLYDATA;
    const [stage, setStage] = React.useState(1);
    const steps = React.useRef([]);
    React.useEffect(() => {
      if (typeof IntersectionObserver === "undefined") { setStage(3); return; }
      const io = new IntersectionObserver((entries) => {
        entries.forEach((e) => { if (e.isIntersecting) setStage(Number(e.target.dataset.step)); });
      }, { rootMargin: "-45% 0px -45% 0px", threshold: 0 });
      steps.current.forEach((el) => el && io.observe(el));
      return () => io.disconnect();
    }, []);
    if (!D) return null;
    return (
      <div className="scrolly">
        <div className="scrolly__graphic">
          <div className="story__chart-title">Ocean temperature vs storm strength, 1985–2024</div>
          <ScrollyChart D={D} stage={stage} />
          <div className="scrolly__legend">
            <span><span className="scrolly__sw" style={{ background: "var(--accent)" }} />Ocean temperature</span>
            <span><span className="scrolly__sw" style={{ background: "#FF5C39" }} />Cyclone peak wind</span>
          </div>
        </div>
        <div className="scrolly__steps">
          {SCROLLY_STEPS.map((s, i) => (
            <div className="scrolly__step" key={i} data-step={i} ref={(el) => (steps.current[i] = el)}>
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

  function PStory({ p, index }) {
    const [openData, setOpenData] = React.useState(false);
    const [openCharts, setOpenCharts] = React.useState(false);
    const rev = index % 2 === 1;
    const hasViz = p.viz && p.viz.length > 0 && window.AdhiCharts && window.CHARTDATA;
    return (
      <section className="story" id={p.id}>
        <div className="wrap">
          <div className={"story__grid" + (rev ? " story__grid--rev" : "")}>
            <Reveal className="story__media">
              {p.scoreboard
                ? <div className="story__board"><PDataTable data={p.scoreboard} caption="Disclosure scores, 0 to 4" /></div>
                : hasViz
                  ? <div className="story__feature">
                      <div className="story__chart-title">{p.viz[0].title}</div>
                      <PChart vizKey={p.vizKey} spec={p.viz[0]} />
                    </div>
                  : null}
            </Reveal>

            <Reveal className="story__body" delay={120}>
              <div className="story__tagrow">
                <Eyebrow tick>Project {index + 1} · {p.year}</Eyebrow>
                <Badge variant={statusVariant(p.status)} dot>{p.status}</Badge>
              </div>
              <h2 className="story__title">{p.title}</h2>
              <p className="story__hook">{p.headline}</p>
              <p className="story__lead">{p.body}</p>

              <div className="story__findings">
                {p.findings.map((f, i) => (
                  <div className="pfind" key={i}>
                    <div className="pfind__v"><span className="v">{f.value}</span>{f.unit && <span className="u">{f.unit}</span>}</div>
                    <div className="pfind__label">{f.label}</div>
                    <div className="pfind__text">{f.text}</div>
                  </div>
                ))}
              </div>

              <p className="story__meaning"><span className="story__meaning-tag">Why it matters</span>{p.meaning}</p>

              {((hasViz && p.viz.length > 1) || p.dataset) && (
                <div className="story__toggles">
                  {hasViz && p.viz.length > 1 && (
                    <button type="button" className="story__data-toggle" aria-expanded={openCharts} onClick={() => setOpenCharts((o) => !o)}>
                      <Icon name="bar-chart" size={16} />
                      {openCharts ? "Hide charts" : "See all " + p.viz.length + " charts"}
                      <Icon name="chevron-right" size={15} className={"story__data-chev" + (openCharts ? " story__data-chev--open" : "")} />
                    </button>
                  )}
                  {p.dataset && (
                    <button type="button" className="story__data-toggle" aria-expanded={openData} onClick={() => setOpenData((o) => !o)}>
                      <Icon name="layers" size={16} />
                      {openData ? "Hide the data" : "Explore the raw data"}
                      <Icon name="chevron-right" size={15} className={"story__data-chev" + (openData ? " story__data-chev--open" : "")} />
                    </button>
                  )}
                </div>
              )}

              <div className="story__links">
                {p.resources.map((r, i) => (
                  <a className="story__link" key={i} href={r.href} target="_blank" rel="noopener noreferrer">
                    <Icon name={r.icon} size={15} />{r.label}
                  </a>
                ))}
              </div>
            </Reveal>
          </div>

          {p.hasMap && window.MAPDATA && window.AdhiCharts && window.AdhiCharts.MapChart && (
            <Reveal className="story__map">
              <div className="story__chart-title">Where these storms tracked, season by season</div>
              {React.createElement(window.AdhiCharts.MapChart, { data: window.MAPDATA, label: "Tracks of the 193 cyclones that came within 500 km of WA, 1985 to 2024, coloured by peak wind." })}
              <p className="story__map-note">Every cyclone that came within 500 km of the WA coast, coloured by peak wind. Hover a track to see the storm. Notice how they sweep in from the north-west toward the Pilbara and Kimberley.</p>
            </Reveal>
          )}

          {p.scrolly && window.SCROLLYDATA && (
            <div className="story__scrolly">
              <PScrolly />
            </div>
          )}

          {openCharts && hasViz && (
            <div className="story__charts">
              {p.viz.slice(1).map((spec, i) => (
                <div className="story__chart-card" key={i}>
                  <div className="story__chart-title">{spec.title}</div>
                  <PChart vizKey={p.vizKey} spec={spec} />
                </div>
              ))}
            </div>
          )}
          {openData && p.dataset && (
            <div className="story__data">
              <PDataTable data={p.dataset} caption={p.dataset.caption} />
            </div>
          )}
        </div>
      </section>
    );
  }

  function PStories() {
    return (
      <div id="work">
        <section className="section section--tight">
          <div className="wrap">
            <Reveal className="section-head">
              <Eyebrow tick>Personal projects</Eyebrow>
              <h2>Built out of curiosity.</h2>
              <p>Three projects I took on myself, simply because I love working with data and wanted answers. Each one started with a Western Australian climate question I wanted to work through from the raw data myself, then check my numbers against the published science. No client, no brief, just curiosity and a respect for what the data actually says.</p>
            </Reveal>
          </div>
        </section>
        {P.projects.map((p, i) => <PStory key={p.id} p={p} index={i} />)}
      </div>
    );
  }

  /* ----------------------------------------------------------------- About */
  function PAbout() {
    return (
      <section className="section" id="about">
        <div className="wrap about__grid">
          <Reveal className="about__body">
            <Eyebrow tick>About</Eyebrow>
            <h2 style={{ fontSize: "var(--text-4xl)", letterSpacing: "var(--tracking-tighter)", margin: "12px 0 20px" }}>
              Hi, I'm Adhi.
            </h2>
            <p>
              I'm studying a Master of Environment and Climate Emergency at Curtin University, now in my second
              year with two semesters to go. Right now I'm looking for an internship in sustainability, somewhere
              I can turn this kind of climate-data work into real impact for a team.
            </p>
            <p style={{ marginTop: "var(--space-4)" }}>
              I've arrived here from a few directions. I trained as a naval architect and marine engineer, spent
              two years as a business analyst in regional Western Australia, and worked as a hatchery technician
              while completing a Diploma of Aquaculture. The common thread has always been the same: taking messy,
              real-world data and turning it into something a team can act on.
            </p>
            <p style={{ marginTop: "var(--space-4)" }}>
              This portfolio is where I bring that together: real Western Australian climate data, honest
              analysis, and findings written so anyone can follow them, framed for the disclosure rules companies
              now have to meet. I care as much about getting the cause right as I do about the headline number.
            </p>
            <div className="about__tags">
              <Tag>Physical climate risk</Tag><Tag>AASB S2</Tag><Tag>IBTrACS / BOM</Tag>
              <Tag>Trend detection</Tag><Tag>Disclosure scoring</Tag>
            </div>
          </Reveal>
          <Reveal as="aside" id="contact" className="about__contact" delay={120}>
            <Eyebrow tone="leaf" tick>Get in touch</Eyebrow>
            <h3 className="about__contact-title">Open to sustainability internships.</h3>
            <p>If you're hiring, or you just want to talk about WA climate, I'd love to hear from you.</p>
            <div className="about__contact-actions">
              <Button variant="leaf" size="lg" fullWidth as="a" href={"mailto:" + P.profile.email} iconLeft={<Icon name="mail" size={18} />}>Email me</Button>
              <Button variant="secondary" size="lg" fullWidth as="a" href={P.profile.linkedin} target="_blank" rel="noopener noreferrer" iconLeft={<Icon name="linkedin" size={18} />}>LinkedIn</Button>
            </div>
            <a className="about__contact-email" href={"mailto:" + P.profile.email}><Icon name="mail" size={15} />{P.profile.email}</a>
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

  Object.assign(window, { PNav, PHero, PStatBand, PStories, PAbout, PFooter });
})();
