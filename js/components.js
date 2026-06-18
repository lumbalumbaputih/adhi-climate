(function () {
  const R = window.React;

  function injectStyle(id, css) {
    if (document.getElementById(id)) return;
    const el = document.createElement("style");
    el.id = id;
    el.textContent = css;
    document.head.appendChild(el);
  }

  /* ------------------------------------------------------------------ Button */
  injectStyle("adhi-btn-css", `
.adhi-btn {
  display: inline-flex; align-items: center; justify-content: center;
  gap: var(--space-2); font-family: var(--font-sans); font-weight: var(--weight-semibold);
  letter-spacing: -0.005em; line-height: 1; border: 1px solid transparent;
  border-radius: var(--radius-md); cursor: pointer; white-space: nowrap;
  transition: background-color var(--duration-fast) var(--ease-standard),
              border-color var(--duration-fast) var(--ease-standard),
              color var(--duration-fast) var(--ease-standard),
              transform var(--duration-fast) var(--ease-standard);
  text-decoration: none;
}
.adhi-btn:active { transform: translateY(1px); }
.adhi-btn:focus-visible { outline: none; box-shadow: var(--shadow-focus); }
.adhi-btn[disabled] { opacity: 0.45; cursor: not-allowed; transform: none; }
.adhi-btn--sm { height: 32px; padding: 0 var(--space-3); font-size: var(--text-sm); }
.adhi-btn--md { height: 40px; padding: 0 var(--space-5); font-size: var(--text-base); }
.adhi-btn--lg { height: 48px; padding: 0 var(--space-6); font-size: var(--text-md); }
.adhi-btn--primary { background: var(--accent); color: var(--text-on-accent); }
.adhi-btn--primary:hover:not([disabled]) { background: var(--accent-hover); }
.adhi-btn--primary:active:not([disabled]) { background: var(--accent-active); }
.adhi-btn--leaf { background: var(--leaf); color: #fff; }
.adhi-btn--leaf:hover:not([disabled]) { background: var(--leaf-hover); }
.adhi-btn--secondary { background: var(--surface-card); color: var(--text-strong); border-color: var(--border-default); }
.adhi-btn--secondary:hover:not([disabled]) { background: var(--bg-subtle); border-color: var(--border-strong); }
.adhi-btn--ghost { background: transparent; color: var(--accent-text); }
.adhi-btn--ghost:hover:not([disabled]) { background: var(--accent-soft); }
.adhi-btn--full { width: 100%; }
  `);

  function Button({ children, variant = "primary", size = "md", fullWidth = false, iconLeft = null, iconRight = null, as = "button", className = "", onClick, type, href, ...rest }) {
    const Tag = as;
    const cls = ["adhi-btn", `adhi-btn--${variant}`, `adhi-btn--${size}`, fullWidth ? "adhi-btn--full" : "", className].filter(Boolean).join(" ");
    return R.createElement(Tag, { className: cls, onClick, type, href, ...rest },
      iconLeft, children != null && R.createElement("span", null, children), iconRight
    );
  }

  /* -------------------------------------------------------------- IconButton */
  injectStyle("adhi-iconbtn-css", `
.adhi-iconbtn {
  display: inline-flex; align-items: center; justify-content: center;
  border-radius: var(--radius-md); border: 1px solid transparent;
  background: transparent; color: var(--text-body); cursor: pointer;
  transition: background-color var(--duration-fast) var(--ease-standard),
              color var(--duration-fast) var(--ease-standard),
              border-color var(--duration-fast) var(--ease-standard);
}
.adhi-iconbtn:hover:not([disabled]) { background: var(--bg-muted); color: var(--text-strong); }
.adhi-iconbtn:active:not([disabled]) { transform: translateY(1px); }
.adhi-iconbtn:focus-visible { outline: none; box-shadow: var(--shadow-focus); }
.adhi-iconbtn[disabled] { opacity: 0.45; cursor: not-allowed; }
.adhi-iconbtn--sm { width: 32px; height: 32px; }
.adhi-iconbtn--md { width: 40px; height: 40px; }
.adhi-iconbtn--lg { width: 48px; height: 48px; }
.adhi-iconbtn--solid { background: var(--accent); color: var(--text-on-accent); }
.adhi-iconbtn--solid:hover:not([disabled]) { background: var(--accent-hover); color: #fff; }
.adhi-iconbtn--outline { border-color: var(--border-default); }
.adhi-iconbtn--outline:hover:not([disabled]) { border-color: var(--border-strong); background: var(--bg-subtle); }
  `);

  function IconButton({ children, variant = "ghost", size = "md", className = "", ...rest }) {
    const cls = ["adhi-iconbtn", `adhi-iconbtn--${variant}`, `adhi-iconbtn--${size}`, className].filter(Boolean).join(" ");
    return R.createElement("button", { type: "button", className: cls, ...rest }, children);
  }

  /* -------------------------------------------------------------------- Stat */
  injectStyle("adhi-stat-css", `
.adhi-stat { display: flex; flex-direction: column; gap: var(--space-2); }
.adhi-stat__label { font-family: var(--font-mono); font-size: var(--text-xs); font-weight: var(--weight-medium); letter-spacing: var(--tracking-eyebrow); text-transform: uppercase; color: var(--text-muted); }
.adhi-stat__value { display: flex; align-items: baseline; gap: var(--space-2); font-family: var(--font-mono); font-weight: var(--weight-semibold); color: var(--text-strong); letter-spacing: -0.01em; line-height: 1; }
.adhi-stat--md .adhi-stat__value { font-size: var(--text-3xl); }
.adhi-stat--lg .adhi-stat__value { font-size: var(--text-5xl); }
.adhi-stat--sm .adhi-stat__value { font-size: var(--text-2xl); }
.adhi-stat__unit { font-size: 0.42em; font-weight: var(--weight-regular); color: var(--text-muted); }
.adhi-stat__delta { font-family: var(--font-mono); font-size: var(--text-sm); font-weight: var(--weight-medium); display: inline-flex; align-items: center; gap: 2px; }
.adhi-stat__delta--down { color: var(--success); }
.adhi-stat__delta--up { color: var(--danger); }
.adhi-stat__delta--neutral { color: var(--text-muted); }
.adhi-stat__caption { font-family: var(--font-sans); font-size: var(--text-sm); color: var(--text-muted); }
  `);

  function Stat({ label, value, unit, delta, trend = "neutral", caption, size = "md", className = "", ...rest }) {
    const arrow = trend === "down" ? "▾" : trend === "up" ? "▴" : "";
    return R.createElement("div", { className: ["adhi-stat", `adhi-stat--${size}`, className].filter(Boolean).join(" "), ...rest },
      label && R.createElement("div", { className: "adhi-stat__label" }, label),
      R.createElement("div", { className: "adhi-stat__value" },
        R.createElement("span", null, value),
        unit && R.createElement("span", { className: "adhi-stat__unit" }, unit),
        delta != null && R.createElement("span", { className: `adhi-stat__delta adhi-stat__delta--${trend}` }, arrow, " ", delta)
      ),
      caption && R.createElement("div", { className: "adhi-stat__caption" }, caption)
    );
  }

  /* ------------------------------------------------------------------- Badge */
  injectStyle("adhi-badge-css", `
.adhi-badge {
  display: inline-flex; align-items: center; gap: var(--space-1);
  font-family: var(--font-mono); font-size: var(--text-xs); font-weight: var(--weight-medium);
  letter-spacing: 0.04em; line-height: 1; padding: 5px 9px;
  border-radius: var(--radius-sm); border: 1px solid transparent; white-space: nowrap;
}
.adhi-badge__dot { width: 6px; height: 6px; border-radius: 999px; background: currentColor; }
.adhi-badge--neutral { background: var(--bg-muted); color: var(--text-body); border-color: var(--border-subtle); }
.adhi-badge--accent  { background: var(--accent-soft); color: var(--accent-text); border-color: var(--accent-soft-border); }
.adhi-badge--leaf    { background: var(--leaf-soft); color: var(--leaf-text); border-color: var(--leaf-soft-border); }
.adhi-badge--success { background: var(--success-soft); color: var(--success); border-color: var(--green-200); }
.adhi-badge--warning { background: var(--warning-soft); color: #B45309; border-color: #FCE3B3; }
.adhi-badge--danger  { background: var(--danger-soft); color: var(--danger); border-color: #F7C9CB; }
.adhi-badge--solid   { background: var(--accent); color: var(--text-on-accent); border-color: transparent; }
  `);

  function Badge({ children, variant = "neutral", dot = false, className = "", ...rest }) {
    return R.createElement("span", { className: ["adhi-badge", `adhi-badge--${variant}`, className].filter(Boolean).join(" "), ...rest },
      dot && R.createElement("span", { className: "adhi-badge__dot" }),
      children
    );
  }

  /* --------------------------------------------------------------------- Tag */
  injectStyle("adhi-tag-css", `
.adhi-tag {
  display: inline-flex; align-items: center; gap: var(--space-2);
  font-family: var(--font-sans); font-size: var(--text-sm); font-weight: var(--weight-medium);
  line-height: 1; padding: 6px 12px; border-radius: var(--radius-full);
  background: var(--surface-card); color: var(--text-body); border: 1px solid var(--border-default);
  transition: border-color var(--duration-fast) var(--ease-standard),
              background-color var(--duration-fast) var(--ease-standard),
              color var(--duration-fast) var(--ease-standard);
}
.adhi-tag--interactive { cursor: pointer; }
.adhi-tag--interactive:hover { border-color: var(--accent); color: var(--accent-text); background: var(--accent-soft); }
.adhi-tag--selected { background: var(--accent); color: var(--text-on-accent); border-color: var(--accent); }
.adhi-tag__remove {
  display: inline-flex; align-items: center; justify-content: center;
  width: 16px; height: 16px; border-radius: 999px; border: 0; padding: 0;
  background: transparent; color: inherit; cursor: pointer; opacity: 0.6;
  font-size: 14px; line-height: 1;
}
.adhi-tag__remove:hover { opacity: 1; }
  `);

  function Tag({ children, selected = false, onRemove, onClick, className = "", ...rest }) {
    const interactive = Boolean(onClick) && !onRemove;
    const cls = ["adhi-tag", interactive ? "adhi-tag--interactive" : "", selected ? "adhi-tag--selected" : "", className].filter(Boolean).join(" ");
    return R.createElement("span", { className: cls, onClick, ...rest },
      children,
      onRemove && R.createElement("button", { type: "button", className: "adhi-tag__remove", "aria-label": "Remove",
        onClick: (e) => { e.stopPropagation(); onRemove(e); } }, "×")
    );
  }

  /* --------------------------------------------------------------- ProgressBar */
  injectStyle("adhi-progress-css", `
.adhi-progress { display: flex; flex-direction: column; gap: var(--space-2); }
.adhi-progress__head { display: flex; justify-content: space-between; align-items: baseline; font-family: var(--font-mono); font-size: var(--text-xs); letter-spacing: 0.04em; color: var(--text-muted); }
.adhi-progress__value { color: var(--text-strong); font-weight: var(--weight-medium); }
.adhi-progress__track { position: relative; width: 100%; height: 8px; background: var(--bg-muted); border-radius: var(--radius-full); overflow: hidden; }
.adhi-progress__fill { position: absolute; inset: 0 auto 0 0; height: 100%; background: var(--accent); border-radius: var(--radius-full); transition: width var(--duration-slow) var(--ease-out); }
.adhi-progress--leaf .adhi-progress__fill { background: var(--leaf); }
.adhi-progress--lg .adhi-progress__track { height: 12px; }
  `);

  function ProgressBar({ value = 0, max = 100, label, showValue = true, variant = "accent", size = "md", className = "", ...rest }) {
    const pct = Math.max(0, Math.min(100, (value / max) * 100));
    return R.createElement("div", { className: ["adhi-progress", `adhi-progress--${variant}`, `adhi-progress--${size}`, className].filter(Boolean).join(" "), ...rest },
      (label || showValue) && R.createElement("div", { className: "adhi-progress__head" },
        R.createElement("span", null, label),
        showValue && R.createElement("span", { className: "adhi-progress__value" }, Math.round(pct) + "%")
      ),
      R.createElement("div", { className: "adhi-progress__track", role: "progressbar", "aria-valuenow": value, "aria-valuemin": 0, "aria-valuemax": max },
        R.createElement("div", { className: "adhi-progress__fill", style: { width: `${pct}%` } })
      )
    );
  }

  /* -------------------------------------------------------------------- Card */
  injectStyle("adhi-card-css", `
.adhi-card {
  display: flex; flex-direction: column;
  background: var(--surface-card); border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); overflow: hidden;
}
.adhi-card--pad-sm { padding: var(--space-4); }
.adhi-card--pad-md { padding: var(--space-6); }
.adhi-card--pad-lg { padding: var(--space-8); }
.adhi-card--pad-none { padding: 0; }
.adhi-card--inset { background: var(--surface-inset); box-shadow: none; }
.adhi-card--flat { box-shadow: none; }
.adhi-card--interactive {
  cursor: pointer;
  transition: box-shadow var(--duration-base) var(--ease-standard),
              border-color var(--duration-base) var(--ease-standard),
              transform var(--duration-base) var(--ease-out);
}
.adhi-card--interactive:hover { box-shadow: var(--shadow-lg); border-color: var(--border-default); transform: translateY(-2px); }
.adhi-card--accent-edge { border-top: 3px solid var(--accent); }
.adhi-card--leaf-edge { border-top: 3px solid var(--leaf); }
  `);

  function Card({ children, padding = "md", interactive = false, variant = "default", edge = "none", className = "", ...rest }) {
    const cls = ["adhi-card", `adhi-card--pad-${padding}`,
      interactive ? "adhi-card--interactive" : "",
      variant === "inset" ? "adhi-card--inset" : "",
      variant === "flat" ? "adhi-card--flat" : "",
      edge === "accent" ? "adhi-card--accent-edge" : "",
      edge === "leaf" ? "adhi-card--leaf-edge" : "",
      className].filter(Boolean).join(" ");
    return R.createElement("div", { className: cls, ...rest }, children);
  }

  /* ------------------------------------------------------------------ Eyebrow */
  injectStyle("adhi-eyebrow-css", `
.adhi-eyebrow {
  display: inline-flex; align-items: center; gap: var(--space-2);
  font-family: var(--font-mono); font-weight: var(--weight-medium);
  font-size: var(--text-xs); letter-spacing: var(--tracking-eyebrow);
  text-transform: uppercase; color: var(--accent-text);
}
.adhi-eyebrow--muted { color: var(--text-muted); }
.adhi-eyebrow--leaf { color: var(--leaf-text); }
.adhi-eyebrow__tick { width: 16px; height: 2px; background: currentColor; border-radius: 2px; }
  `);

  function Eyebrow({ children, tone = "accent", tick = false, className = "", ...rest }) {
    return R.createElement("span", { className: ["adhi-eyebrow", tone !== "accent" ? `adhi-eyebrow--${tone}` : "", className].filter(Boolean).join(" "), ...rest },
      tick && R.createElement("span", { className: "adhi-eyebrow__tick" }),
      children
    );
  }

  /* ------------------------------------------------------------------- Avatar */
  injectStyle("adhi-avatar-css", `
.adhi-avatar {
  display: inline-flex; align-items: center; justify-content: center;
  border-radius: var(--radius-full); background: var(--accent-soft); color: var(--accent-text);
  font-family: var(--font-display); font-weight: var(--weight-semibold);
  overflow: hidden; flex-shrink: 0; border: 1px solid var(--accent-soft-border); user-select: none;
}
.adhi-avatar img { width: 100%; height: 100%; object-fit: cover; }
.adhi-avatar--sm { width: 32px; height: 32px; font-size: var(--text-xs); }
.adhi-avatar--md { width: 44px; height: 44px; font-size: var(--text-sm); }
.adhi-avatar--lg { width: 64px; height: 64px; font-size: var(--text-lg); }
.adhi-avatar--xl { width: 96px; height: 96px; font-size: var(--text-2xl); }
.adhi-avatar--leaf { background: var(--leaf-soft); color: var(--leaf-text); border-color: var(--leaf-soft-border); }
  `);

  function Avatar({ src, alt = "", initials, size = "md", tone = "accent", className = "", ...rest }) {
    return R.createElement("span", { className: ["adhi-avatar", `adhi-avatar--${size}`, tone === "leaf" ? "adhi-avatar--leaf" : "", className].filter(Boolean).join(" "), ...rest },
      src ? R.createElement("img", { src, alt }) : initials
    );
  }

  /* -------------------------------------------------------------------- Input */
  injectStyle("adhi-input-css", `
.adhi-field { display: flex; flex-direction: column; gap: var(--space-2); }
.adhi-field__label { font-family: var(--font-sans); font-size: var(--text-sm); font-weight: var(--weight-medium); color: var(--text-strong); }
.adhi-field__req { color: var(--accent); margin-left: 2px; }
.adhi-input {
  width: 100%; font-family: var(--font-sans); font-size: var(--text-base);
  color: var(--text-strong); background: var(--surface-card);
  border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 10px 12px;
  transition: border-color var(--duration-fast) var(--ease-standard),
              box-shadow var(--duration-fast) var(--ease-standard);
}
.adhi-input::placeholder { color: var(--text-faint); }
.adhi-input:hover { border-color: var(--border-strong); }
.adhi-input:focus { outline: none; border-color: var(--accent); box-shadow: var(--shadow-focus); }
.adhi-input[disabled] { background: var(--bg-subtle); color: var(--text-muted); cursor: not-allowed; }
.adhi-input--textarea { min-height: 112px; resize: vertical; line-height: 1.55; }
.adhi-input--error { border-color: var(--danger); }
.adhi-input--error:focus { box-shadow: 0 0 0 3px rgba(229,72,77,0.35); }
.adhi-field__help { font-family: var(--font-sans); font-size: var(--text-sm); color: var(--text-muted); }
.adhi-field__help--error { color: var(--danger); }
  `);

  let _uid = 0;
  function Input({ label, helper, error, required = false, multiline = false, id, className = "", ...rest }) {
    const autoId = R.useMemo(() => id || `adhi-input-${++_uid}`, [id]);
    const inputCls = ["adhi-input", multiline ? "adhi-input--textarea" : "", error ? "adhi-input--error" : "", className].filter(Boolean).join(" ");
    const Field = multiline ? "textarea" : "input";
    return R.createElement("div", { className: "adhi-field" },
      label && R.createElement("label", { className: "adhi-field__label", htmlFor: autoId },
        label, required && R.createElement("span", { className: "adhi-field__req", "aria-hidden": true }, "*")
      ),
      R.createElement(Field, { id: autoId, className: inputCls, "aria-invalid": !!error, ...rest }),
      (error || helper) && R.createElement("span", { className: `adhi-field__help ${error ? "adhi-field__help--error" : ""}` }, error || helper)
    );
  }

  window.AdhiClimateDesignSystem_bcac21 = {
    Button, IconButton, Stat, Badge, Tag, ProgressBar, Card, Eyebrow, Avatar, Input,
  };
})();
