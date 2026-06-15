/* Portfolio sections — Nav, Hero, StatBand, Work, Services, About, Contact, Footer, ProjectDialog */
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
    const bars = [40, 48, 44, 56, 52, 64, 78];
    return (
      <section className="hero" id="top">
        <div className="wrap hero__grid">
          <div>
            <div className="hero__eyebrow"><Eyebrow tick>Climate &amp; Sustainability · WA</Eyebrow></div>
            <h1 className="hero__title">I turn climate <span className="accent">data</span> into decisions business and government can act on.</h1>
            <p className="hero__lead">{P.profile.intro}</p>
            <div className="hero__actions">
              <Button variant="primary" size="lg" onClick={onContact} iconRight={<Icon name="arrow-right" size={18} />}>Start a project</Button>
              <Button variant="ghost" size="lg" as="a" href="#work" iconRight={<Icon name="arrow-down-right" size={18} />}>See selected work</Button>
            </div>
            <div className="hero__meta">
              <span className="hero__meta-item"><Icon name="map-pin" size={16} />{P.profile.location}</span>
              <span className="hero__meta-item"><Icon name="leaf" size={16} />Physical risk · Climate data · AASB S2</span>
            </div>
          </div>

          <div className="hero__panel" aria-hidden="true">
            <div className="hero__panel-label">WA cyclone peak intensity · 1985–2024</div>
            <div className="hero__chart">
              {bars.map((h, i) => (
                <div key={i} className="hero__bar" style={{ height: h + "%" }} />
              ))}
            </div>
            <div className="hero__panel-stat">
              <span><span className="big">40</span> <span className="unit">yrs analysed</span></span>
              <span className="delta">▴ intensifying</span>
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
          <div className="pcard__foot">
            <span className="pcard__result">
              <span className="v">{p.result.value}</span>
              <span className="u">{p.result.unit}</span>
              <span className="l">{p.result.label}</span>
            </span>
            <span className="pcard__open">Open <Icon name="arrow-up-right" size={15} /></span>
          </div>
        </div>
      </Card>
    );
  }

  function PWork({ onOpen }) {
    const [active, setActive] = React.useState("All");
    const list = active === "All" ? P.projects : P.projects.filter((p) => p.category.includes(active));
    return (
      <section className="section" id="work">
        <div className="wrap">
          <div className="section-head">
            <Eyebrow tick>Selected work</Eyebrow>
            <h2>Projects with measured outcomes.</h2>
            <p>A sample of climate and sustainability engagements — each grounded in a baseline, a method, and a number you can check.</p>
          </div>
          <div className="work__filters">
            {P.filters.map((f) => (
              <Tag key={f} onClick={() => setActive(f)} selected={active === f}>{f}</Tag>
            ))}
          </div>
          <div className="work__grid">
            {list.map((p) => <ProjectCard key={p.id} p={p} onOpen={onOpen} />)}
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
            <Eyebrow tone="leaf" tick>Services</Eyebrow>
            <h2>How I can help.</h2>
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
              Rigorous about data, practical about disclosure.
            </h2>
            <p>{P.profile.intro}</p>
            <p style={{ marginTop: "var(--space-4)" }}>
              The work usually starts with a question no one has quantified for WA yet — then primary data, a
              transparent method, and a result a board or regulator can defend. I care as much about getting the
              attribution right as I do about the headline number, and about whether a finding survives contact with
              an AASB S2 disclosure as I do about the trend behind it.
            </p>
            <div style={{ marginTop: "var(--space-8)" }}>
              <ProgressBar label="AASB S2 readiness — WA ASX majors (median, illustrative)" value={48} variant="accent" />
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
  function PContact({ toast }) {
    function submit(e) {
      e.preventDefault();
      toast("Message sent — I'll be in touch soon.");
      e.target.reset();
    }
    return (
      <section className="section" id="contact">
        <div className="wrap">
          <div className="contact">
            <div className="contact__grid">
              <div>
                <Eyebrow className="contact__eyebrow" tick>Get in touch</Eyebrow>
                <h2>Have a WA climate question worth measuring?</h2>
                <p>Tell me about the decision you're trying to make. I take on a small number of projects in physical climate risk, climate data analysis, and AASB S2 disclosure each quarter.</p>
                <div className="hero__meta" style={{ borderTopColor: "rgba(255,255,255,0.12)" }}>
                  <span className="hero__meta-item" style={{ color: "var(--blue-100)" }}><Icon name="mail" size={16} />{P.profile.email}</span>
                </div>
              </div>
              <form className="contact__form" onSubmit={submit}>
                <Input label="Name" placeholder="Your name" required />
                <Input label="Email" type="email" placeholder="you@org.org" required />
                <Input label="What can I help with?" multiline placeholder="A short note about your project…" />
                <Button variant="leaf" size="lg" type="submit" fullWidth iconRight={<Icon name="arrow-right" size={18} />}>Send message</Button>
              </form>
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
            <IconButton variant="outline" aria-label="LinkedIn"><Icon name="linkedin" size={18} /></IconButton>
            <IconButton variant="outline" aria-label="GitHub"><Icon name="github" size={18} /></IconButton>
            <IconButton variant="outline" aria-label="Email"><Icon name="mail" size={18} /></IconButton>
          </div>
        </div>
      </footer>
    );
  }

  /* ---------------------------------------------------------- ProjectDialog */
  function PProjectDialog({ project, onClose }) {
    React.useEffect(() => {
      function onKey(e) { if (e.key === "Escape") onClose(); }
      document.addEventListener("keydown", onKey);
      return () => document.removeEventListener("keydown", onKey);
    }, [onClose]);
    if (!project) return null;
    const p = project;
    return (
      <div role="dialog" aria-modal="true" onClick={onClose}
        style={{ position: "fixed", inset: 0, zIndex: 70, background: "rgba(14,34,74,0.45)", backdropFilter: "blur(4px)", display: "flex", alignItems: "center", justifyContent: "center", padding: "24px" }}>
        <div onClick={(e) => e.stopPropagation()}
          style={{ width: "min(620px, 100%)", maxHeight: "88vh", overflow: "auto", background: "var(--surface-card)", borderRadius: "var(--radius-xl)", boxShadow: "var(--shadow-xl)", borderTop: "3px solid var(--leaf)" }}>
          <div style={{ padding: "var(--space-8)" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "var(--space-5)" }}>
              <div className="pcard__icon" style={{ width: 52, height: 52 }}><Icon name={p.icon} size={26} /></div>
              <IconButton aria-label="Close" onClick={onClose}><Icon name="x" size={20} /></IconButton>
            </div>
            <div style={{ display: "flex", gap: "8px", marginBottom: "12px", alignItems: "center" }}>
              <Badge variant="leaf" dot>{p.status}</Badge>
              <Badge variant="neutral">{p.year}</Badge>
            </div>
            <h3 style={{ fontSize: "var(--text-3xl)", letterSpacing: "var(--tracking-tight)", marginBottom: "var(--space-4)" }}>{p.title}</h3>
            <p style={{ fontSize: "var(--text-md)", color: "var(--text-body)", lineHeight: "var(--leading-relaxed)", marginBottom: "var(--space-6)" }}>{p.body}</p>
            <Card variant="inset" padding="md" style={{ marginBottom: "var(--space-6)" }}>
              <div style={{ display: "flex", alignItems: "baseline", gap: "8px", fontFamily: "var(--font-mono)" }}>
                <span style={{ fontSize: "var(--text-4xl)", fontWeight: 600, color: "var(--text-strong)" }}>{p.result.value}</span>
                <span style={{ fontSize: "var(--text-md)", color: "var(--text-muted)" }}>{p.result.unit}</span>
                <span style={{ fontSize: "var(--text-sm)", color: "var(--text-faint)", marginLeft: "8px" }}>{p.result.label}</span>
              </div>
            </Card>
            <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
              {p.tags.map((t) => <Tag key={t}>{t}</Tag>)}
            </div>
          </div>
        </div>
      </div>
    );
  }

  Object.assign(window, { PNav, PHero, PStatBand, PWork, PServices, PAbout, PContact, PFooter, PProjectDialog });
})();
