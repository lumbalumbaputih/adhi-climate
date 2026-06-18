/* Portfolio sections: Nav, Hero, StatBand, Work, Services, About, Contact, Footer, ProjectDialog */
(function () {
  const { Button, IconButton, Eyebrow, Stat, Card, Badge, Tag, ProgressBar, Input } = window.AdhiClimateDesignSystem_bcac21;
  const Icon = window.Icon;
  const P = window.PORTFOLIO;

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
            <a className="nav__link" href="#work">Work</a>
            <a className="nav__link" href="#services">Services</a>
            <a className="nav__link" href="#about">About</a>
          </nav>
          <div className="nav__actions">
            <Button variant="secondary" size="sm" as="a" href="https://github.com/lumbalumbaputih/adhi-climate" iconLeft={<Icon name="file-text" size={16} />}>CV</Button>
            <Button variant="primary" size="sm" onClick={onContact} iconRight={<Icon name="arrow-right" size={16} />}>Get in touch</Button>
          </div>
        </div>
      </header>
    );
  }

  /* ------------------------------------------------------------------ Hero */
  function PHero({ onContact }) {
    // Real period-mean sea-surface-temperature anomaly, 1985-2024, from
    // cyclone-risk/data/sst_intensity.csv (lowest period maps to 40%, highest to 82%).
    const bars = [45, 40, 51, 56, 71, 81, 82];
    return (
      <section className="hero" id="top">
        <div className="wrap hero__grid">
          <div>
            <div className="hero__eyebrow"><Eyebrow tick>Climate &amp; Sustainability · WA</Eyebrow></div>
            <h1 className="hero__title">I turn climate <span className="accent">data</span> into decisions business and government can act on.</h1>
            <p className="hero__lead">{P.profile.intro}</p>
            <div className="hero__actions">
              <Button variant="primary" size="lg" onClick={onContact} iconRight={<Icon name="arrow-right" size={18} />}>Get in touch</Button>
              <Button variant="ghost" size="lg" as="a" href="#work" iconRight={<Icon name="arrow-down-right" size={18} />}>See selected work</Button>
            </div>
            <div className="hero__meta">
              <span className="hero__meta-item"><Icon name="map-pin" size={16} />{P.profile.location}</span>
              <span className="hero__meta-item"><Icon name="leaf" size={16} />Physical risk · Climate data · AASB S2</span>
            </div>
          </div>

          <div className="hero__panel" aria-hidden="true">
            <div className="hero__panel-label">WA cyclone-region ocean temperature · <span style={{ whiteSpace: "nowrap" }}>1985–2024</span></div>
            <div className="hero__chart">
              {bars.map((h, i) => (
                <div key={i} className="hero__bar" style={{ height: h + "%" }} />
              ))}
            </div>
            <div className="hero__panel-stat">
              <span><span className="big">40</span> <span className="unit">yrs analysed</span></span>
              <span className="delta">▴ +0.5 °C warming</span>
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
            <div className="statband__cell" key={i}>
              <Stat label={s.label} value={s.value} unit={s.unit} delta={s.delta} trend={s.trend || "neutral"} caption={s.caption} size="md" />
            </div>
          ))}
        </div>
      </section>
    );
  }

  /* ------------------------------------------------------------------ Work */
  function statusVariant(s) {
    if (["Live", "Adopted", "Delivered", "Published"].includes(s)) return "leaf";
    if (["In progress", "Reported"].includes(s)) return "accent";
    return "neutral";
  }

  function ProjectCard({ p, onOpen }) {
    return (
      <Card padding="lg" interactive onClick={() => onOpen(p)}>
        <div className="pcard">
          <div className="pcard__top">
            <div className="pcard__icon"><Icon name={p.icon} size={22} /></div>
            <span className="pcard__year">{p.year}</span>
          </div>
          <div>
            <div style={{ marginBottom: "10px" }}><Badge variant={statusVariant(p.status)} dot>{p.status}</Badge></div>
            <h3 className="pcard__title">{p.title}</h3>
          </div>
          <p className="pcard__summary">{p.summary}</p>
          {p.meta && <div className="pcard__meta">{p.meta}</div>}
          <div className="pcard__foot">
            <span className="pcard__result">
              <span className="v">{p.result.value}</span>
              <span className="u">{p.result.unit}</span>
              <span className="l">{p.result.label}</span>
            </span>
            <span className="pcard__open">Read case study <Icon name="arrow-up-right" size={15} /></span>
          </div>
        </div>
      </Card>
    );
  }

  function PWork({ onOpen }) {
    return (
      <section className="section" id="work">
        <div className="wrap">
          <div className="section-head">
            <Eyebrow tick>Selected work</Eyebrow>
            <h2>Projects with measured outcomes.</h2>
            <p>Three climate and sustainability projects, each grounded in a baseline, a method, and a number you can check.</p>
          </div>
          <div className="work__grid">
            {P.projects.map((p) => <ProjectCard key={p.id} p={p} onOpen={onOpen} />)}
          </div>
        </div>
      </section>
    );
  }

  /* -------------------------------------------------------------- Services */
  function PServices() {
    return (
      <section className="section section--tight" id="services">
        <div className="wrap">
          <div className="section-head">
            <Eyebrow tone="leaf" tick>Skills</Eyebrow>
            <h2>What I can bring to a team.</h2>
          </div>
          <div className="services__grid">
            {P.services.map((s, i) => (
              <Card padding="lg" key={i}>
                <div className="svc">
                  <div className="svc__icon"><Icon name={s.icon} size={24} /></div>
                  <h3>{s.title}</h3>
                  <p>{s.text}</p>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>
    );
  }

  /* ----------------------------------------------------------------- About */
  function PAbout() {
    return (
      <section className="section" id="about">
        <div className="wrap about__grid">
          <div className="about__media">
            <span className="mono">// WA physical risk · disclosure · 1950–2024</span>
          </div>
          <div className="about__body">
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
              This portfolio is where I put that into practice: real Western Australian climate data, honest
              analysis, and findings written so anyone can follow them, framed for the disclosure rules companies
              now have to meet. I care as much about getting the cause right as I do about the headline number.
            </p>
            <div style={{ marginTop: "var(--space-8)" }}>
              <ProgressBar label="AASB S2 disclosure readiness: median of 3 WA majors scored" value={84} variant="accent" />
            </div>
            <div className="about__tags">
              <Tag>Physical climate risk</Tag><Tag>AASB S2</Tag><Tag>IBTrACS / BOM</Tag>
              <Tag>Trend detection</Tag><Tag>Disclosure scoring</Tag>
            </div>
          </div>
        </div>
      </section>
    );
  }

  /* --------------------------------------------------------------- Contact */
  function PContact() {
    return (
      <section className="section" id="contact">
        <div className="wrap">
          <div className="contact">
            <div className="contact__grid">
              <div>
                <Eyebrow className="contact__eyebrow" tick>Get in touch</Eyebrow>
                <h2>Looking for a sustainability intern, or have a WA climate question?</h2>
                <p>I'm a Master's student seeking an internship in sustainability, and I'm always happy to talk about physical climate risk, climate data, or AASB S2 disclosure. The quickest way to reach me is email.</p>
                <div className="hero__meta" style={{ borderTopColor: "rgba(255,255,255,0.12)" }}>
                  <span className="hero__meta-item" style={{ color: "var(--blue-100)" }}><Icon name="mail" size={16} />{P.profile.email}</span>
                </div>
              </div>
              <div className="contact__cta">
                <Button variant="leaf" size="lg" as="a" href={"mailto:" + P.profile.email} iconLeft={<Icon name="mail" size={18} />}>Email me</Button>
              </div>
            </div>
          </div>
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

  /* ---------------------------------------------------------- ProjectDialog */
  function PScoreboard({ data }) {
    return (
      <table className="pscore">
        <thead>
          <tr>{data.headers.map((h) => <th key={h}>{h}</th>)}</tr>
        </thead>
        <tbody>
          {data.rows.map((row) => (
            <tr key={row[0]}>{row.map((cell, i) => <td key={i}>{cell}</td>)}</tr>
          ))}
        </tbody>
      </table>
    );
  }

  function PProjectDialog({ project, onClose }) {
    React.useEffect(() => {
      if (!project) return;
      function onKey(e) { if (e.key === "Escape") onClose(); }
      document.addEventListener("keydown", onKey);
      document.body.style.overflow = "hidden";
      return () => {
        document.removeEventListener("keydown", onKey);
        document.body.style.overflow = "";
      };
    }, [project, onClose]);
    if (!project) return null;
    const p = project;
    return (
      <div className="pdialog__overlay" role="dialog" aria-modal="true" aria-label={p.title} onClick={onClose}>
        <div className="pdialog" onClick={(e) => e.stopPropagation()}>
          <div className="pdialog__bar">
            <div className="pdialog__bar-id">
              <div className="pcard__icon"><Icon name={p.icon} size={20} /></div>
              <div className="pdialog__badges">
                <Badge variant={statusVariant(p.status)} dot>{p.status}</Badge>
                <Badge variant="neutral">{p.year}</Badge>
              </div>
            </div>
            <IconButton aria-label="Close" onClick={onClose}><Icon name="x" size={20} /></IconButton>
          </div>

          <div className="pdialog__body">
            <h3 className="pdialog__title">{p.title}</h3>
            {p.headline && <p className="pdialog__hook">{p.headline}</p>}
            <p className="pdialog__lead">{p.body}</p>

            {p.findings && p.findings.length > 0 && (
              <React.Fragment>
                <div className="pdialog__h">Key findings</div>
                <div className="pdialog__findings">
                  {p.findings.map((f, i) => (
                    <div className="pfind" key={i}>
                      <div className="pfind__v"><span className="v">{f.value}</span>{f.unit && <span className="u">{f.unit}</span>}</div>
                      <div className="pfind__label">{f.label}</div>
                      <div className="pfind__text">{f.text}</div>
                    </div>
                  ))}
                </div>
              </React.Fragment>
            )}

            {p.scoreboard && (
              <React.Fragment>
                <div className="pdialog__h">Disclosure scores (0 to 4)</div>
                <PScoreboard data={p.scoreboard} />
              </React.Fragment>
            )}

            {p.charts && p.charts.length > 0 && (
              <React.Fragment>
                <div className="pdialog__h">The charts</div>
                <div className="pdialog__charts">
                  {p.charts.map((c, i) => (
                    <a className="pchart" key={i} href={c.src} target="_blank" rel="noopener noreferrer">
                      <img src={c.src} alt={c.caption} loading="lazy" />
                      <span className="pchart__cap">{c.caption} <Icon name="arrow-up-right" size={14} /></span>
                    </a>
                  ))}
                </div>
              </React.Fragment>
            )}

            {p.meaning && (
              <React.Fragment>
                <div className="pdialog__h">Why it matters</div>
                <p className="pdialog__lead" style={{ marginBottom: 0 }}>{p.meaning}</p>
              </React.Fragment>
            )}

            {p.resources && p.resources.length > 0 && (
              <React.Fragment>
                <div className="pdialog__h">Explore the work</div>
                <div className="pdialog__links">
                  {p.resources.map((r, i) => (
                    <a className="plink" key={i} href={r.href} target="_blank" rel="noopener noreferrer">
                      <span className="plink__icon"><Icon name={r.icon} size={17} /></span>
                      <span className="plink__label">{r.label}</span>
                      <span className="plink__out"><Icon name="external-link" size={14} /></span>
                    </a>
                  ))}
                </div>
              </React.Fragment>
            )}

            <div style={{ display: "flex", gap: "var(--space-3)", flexWrap: "wrap", marginTop: "var(--space-8)" }}>
              {p.tags.map((t) => <Tag key={t}>{t}</Tag>)}
            </div>
          </div>
        </div>
      </div>
    );
  }

  Object.assign(window, { PNav, PHero, PStatBand, PWork, PServices, PAbout, PContact, PFooter, PProjectDialog });
})();
