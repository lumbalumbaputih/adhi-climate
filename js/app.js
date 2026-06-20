/* COMPILED from js/app.jsx. Do not edit directly; edit the .jsx and recompile. */
/* App entry. Compiled to app.js (edit this .jsx, then recompile). */
(function () {
  const {
    PNav,
    PHero,
    PStatBand,
    PStories,
    PContact,
    PFooter
  } = window;
  function App() {
    function scrollToContact() {
      const el = document.getElementById("contact");
      if (el) window.scrollTo({
        top: el.offsetTop - 40,
        behavior: "smooth"
      });
    }
    return /*#__PURE__*/React.createElement("div", {
      className: "site"
    }, /*#__PURE__*/React.createElement(PNav, {
      onContact: scrollToContact
    }), /*#__PURE__*/React.createElement(PHero, {
      onContact: scrollToContact
    }), /*#__PURE__*/React.createElement(PStatBand, null), /*#__PURE__*/React.createElement(PStories, null), /*#__PURE__*/React.createElement(PContact, null), /*#__PURE__*/React.createElement(PFooter, null));
  }
  ReactDOM.createRoot(document.getElementById("root")).render(/*#__PURE__*/React.createElement(App, null));
})();
