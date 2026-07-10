/* App entry. Compiled to app.js (edit this .jsx, then recompile).
   Boots in one of two modes:
   - index (no window.PROJECT_ID): hero, stat band, project index, contact.
   - project page (window.PROJECT_ID set by the generated projects/<id>.html):
     that one project's full story with prev/next navigation. */
(function () {
  const { PNav, PHero, PStatBand, PStories, PProjectPage, PContact, PFooter } = window;
  const P = window.PORTFOLIO;

  // The stories used to live on the front page behind #<id> anchors. Send any
  // old shared links straight to the project's own page.
  if (!window.PROJECT_ID && location.hash) {
    const id = location.hash.slice(1);
    if (P.projects.some((p) => p.id === id)) {
      location.replace("/projects/" + id + ".html");
      return;
    }
  }

  function scrollToContact() {
    const el = document.getElementById("contact");
    if (el) window.scrollTo({ top: el.offsetTop - 40, behavior: "smooth" });
  }

  function IndexApp() {
    return (
      <div className="site">
        <PNav onContact={scrollToContact} />
        <PHero onContact={scrollToContact} />
        <PStatBand />
        <PStories />
        <PContact />
        <PFooter />
      </div>
    );
  }

  function ProjectApp({ p, index }) {
    return (
      <div className="site">
        <PNav onContact={scrollToContact} />
        <PProjectPage p={p} index={index} />
        <PContact />
        <PFooter />
      </div>
    );
  }

  const idx = window.PROJECT_ID ? P.projects.findIndex((p) => p.id === window.PROJECT_ID) : -1;
  ReactDOM.createRoot(document.getElementById("root")).render(
    idx >= 0 ? <ProjectApp p={P.projects[idx]} index={idx} /> : <IndexApp />
  );
})();
