/* App entry. Compiled to app.js (edit this .jsx, then recompile). */
(function () {
  const { PNav, PHero, PStatBand, PStories, PAbout, PFooter } = window;

  function App() {
    function scrollToContact() {
      const el = document.getElementById("contact");
      if (el) window.scrollTo({ top: el.offsetTop - 40, behavior: "smooth" });
    }
    return (
      <div className="site">
        <PNav onContact={scrollToContact} />
        <PHero onContact={scrollToContact} />
        <PStatBand />
        <PStories />
        <PAbout />
        <PFooter />
      </div>
    );
  }

  ReactDOM.createRoot(document.getElementById("root")).render(<App />);
})();
