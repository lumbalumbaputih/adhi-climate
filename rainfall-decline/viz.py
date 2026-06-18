"""
viz.py: publication-quality charts for the SW WA rainfall-decline analysis.

Self-contained: reads the CSVs in data/ and writes PNGs to charts/ at 300 dpi.
Uses the Adhi "Hidup" palette so figures match the cyclone-risk project.
Run:  python3 viz.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import stats_utils as su

# Hidup palette
INK, MUTED, PAPER = "#1A1614", "#6B6259", "#FBF4E6"
TOMATO, MANGO, FOREST, SEA, MAWAR, INDIGO = (
    "#FF5C39", "#FFC234", "#1F9D55", "#1FA9C7", "#E84BA0", "#2E3192")

BASE_START, BASE_END = 1950, 1974
CREDIT = ("Data: GHCN-Daily (NOAA NCEI; BoM station observations) & NOAA PSL "
          "indices  ·  Analysis: A. Katili")


def apply_style():
    plt.rcParams.update({
        "figure.dpi": 120, "savefig.dpi": 300, "savefig.bbox": "tight",
        "font.family": "DejaVu Sans", "font.size": 11,
        "axes.edgecolor": INK, "axes.labelcolor": INK, "axes.titlecolor": INK,
        "axes.titleweight": "bold", "axes.titlesize": 14, "axes.labelsize": 12,
        "axes.linewidth": 1.0, "axes.grid": True, "axes.axisbelow": True,
        "grid.color": "#D8D0C0", "grid.linewidth": 0.7,
        "xtick.color": INK, "ytick.color": INK, "text.color": INK,
        "legend.frameon": False, "figure.facecolor": "white",
        "axes.facecolor": "white",
    })


def credit(ax):
    ax.annotate(CREDIT, xy=(1.0, -0.15), xycoords="axes fraction", ha="right",
                va="top", fontsize=8, color=MUTED)


def load():
    reg = pd.read_csv("data/annual_cool_season_anomaly.csv")
    clean = pd.read_csv("data/rainfall_swwa_clean.csv")
    drivers = pd.read_csv("data/drivers.csv")
    step = pd.read_csv("data/stepchange_summary.csv").iloc[0]
    return reg, clean, drivers, step


# --- 1. time series of % anomaly ---------------------------------------------
def chart_timeseries(reg):
    fig, ax = plt.subplots(figsize=(10, 5.2))
    y = reg.regional_anom_pct.values
    colors = [SEA if v >= 0 else TOMATO for v in y]
    ax.bar(reg.year, y, color=colors, width=0.85, zorder=2)
    run = pd.Series(y).rolling(5, center=True, min_periods=3).mean()
    ax.plot(reg.year, run, color=INK, lw=2.2, zorder=3, label="5-year mean")
    ax.axhline(0, color=MUTED, lw=1)
    ax.set_title("South West WA cool-season rainfall anomaly, 1950–2024")
    ax.set_ylabel("April–October anomaly vs 1950–1974 (%)")
    ax.set_xlabel("Year")
    ax.set_xlim(1949, 2025)
    ax.legend(loc="lower left")
    ax.annotate("Wetter", xy=(1951, max(y) * 0.8), color=SEA, fontsize=10, weight="bold")
    ax.annotate("Drier", xy=(1951, min(y) * 0.85), color=TOMATO, fontsize=10, weight="bold")
    credit(ax)
    fig.savefig("charts/01_timeseries_anomaly.png")
    plt.close(fig)


# --- 2. step change -----------------------------------------------------------
def chart_stepchange(reg, step):
    fig, ax = plt.subplots(figsize=(10, 5.2))
    cp = int(step.pettitt_change_year)
    ax.plot(reg.year, reg.regional_cool_mm, color=MUTED, lw=1.3,
            marker="o", ms=3, label="Annual Apr–Oct total")
    pre = reg[reg.year < cp]
    post = reg[reg.year >= cp]
    ax.hlines(pre.regional_cool_mm.mean(), reg.year.min(), cp - 1,
              color=INDIGO, lw=3, zorder=4,
              label=f"{int(reg.year.min())}–{cp-1} mean = {pre.regional_cool_mm.mean():.0f} mm")
    ax.hlines(post.regional_cool_mm.mean(), cp, reg.year.max(),
              color=TOMATO, lw=3, zorder=4,
              label=f"{cp}–{int(reg.year.max())} mean = {post.regional_cool_mm.mean():.0f} mm")
    ax.axvline(cp - 0.5, color=INK, ls="--", lw=1.2)
    ax.axvspan(1972, 1977, color=MANGO, alpha=0.18, zorder=0)
    ax.annotate("1970s step", xy=(1974.5, ax.get_ylim()[1]), xytext=(0, -14),
                textcoords="offset points", ha="center", color=MUTED, fontsize=9)
    ax.annotate(f"Pettitt change point ≈ {cp}\n(p = {step.pettitt_p:.3f})",
                xy=(cp, post.regional_cool_mm.mean()), xytext=(cp + 2, post.regional_cool_mm.mean() + 60),
                color=INK, fontsize=10,
                arrowprops=dict(arrowstyle="->", color=INK))
    pct = step.pre_to_post_pct_change
    ax.set_title(f"A step down, not a gentle slope: {pct:+.0f}% across the break")
    ax.set_ylabel("Regional April–October rainfall (mm)")
    ax.set_xlabel("Year")
    ax.set_xlim(1949, 2025)
    ax.legend(loc="upper right")
    credit(ax)
    fig.savefig("charts/02_stepchange.png")
    plt.close(fig)


# --- 3. trend with OLS + CI + Sen ---------------------------------------------
def chart_trend(reg):
    fig, ax = plt.subplots(figsize=(10, 5.2))
    x = reg.year.values.astype(float)
    y = reg.regional_anom_pct.values
    r = su.linregress(x, y)
    mk = su.mann_kendall(y)
    sen, sen_b = su.sens_slope(x, y)
    xbar = x.mean()
    Sxx = np.sum((x - xbar) ** 2)
    s = r.stderr * np.sqrt(Sxx)                       # residual std dev
    tcrit = su.t_critical(r.n - 2, 0.05)
    xs = np.linspace(x.min(), x.max(), 200)
    fit = r.intercept + r.slope * xs
    se_fit = s * np.sqrt(1.0 / r.n + (xs - xbar) ** 2 / Sxx)
    ax.scatter(x, y, color=SEA, s=26, zorder=3, alpha=0.85)
    ax.fill_between(xs, fit - tcrit * se_fit, fit + tcrit * se_fit,
                    color=TOMATO, alpha=0.15, zorder=1, label="95% CI (OLS)")
    ax.plot(xs, fit, color=TOMATO, lw=2.4, zorder=4,
            label=f"OLS {r.slope*10:+.1f}%/decade (p={r.pvalue:.3f})")
    ax.plot(xs, sen_b + sen * xs, color=INK, lw=1.6, ls="--", zorder=4,
            label=f"Sen's slope {sen*10:+.1f}%/decade")
    ax.axhline(0, color=MUTED, lw=1)
    ax.set_title("Long-term decline in cool-season rainfall, 1950–2024")
    ax.set_ylabel("April–October anomaly vs 1950–1974 (%)")
    ax.set_xlabel("Year")
    ax.set_xlim(1949, 2025)
    ax.annotate(f"Mann–Kendall: {mk.trend} (τ={mk.tau:.2f}, p={mk.pvalue:.3f})",
                xy=(0.02, 0.04), xycoords="axes fraction", fontsize=10, color=MUTED)
    ax.legend(loc="upper right")
    credit(ax)
    fig.savefig("charts/03_trend_mannkendall.png")
    plt.close(fig)


# --- 4. driver correlation ----------------------------------------------------
def chart_drivers(reg, drivers):
    m = reg.merge(drivers, on="year", how="left")
    specs = [("dmi_AprOct", "IOD, Dipole Mode Index", SEA),
             ("sam_AprOct", "SAM, Marshall index", FOREST),
             ("nino34_AprOct", "ENSO, Niño 3.4 anomaly (°C)", MAWAR)]
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6))
    for ax, (col, title, c) in zip(axes, specs):
        sub = m[["regional_anom_pct", col]].dropna()
        xx, yy = sub[col].values, sub.regional_anom_pct.values
        rr, pp, n = su.pearsonr(xx, yy)
        ax.scatter(xx, yy, color=c, s=22, alpha=0.8, zorder=3)
        lr = su.linregress(xx, yy)
        xs = np.linspace(xx.min(), xx.max(), 50)
        ax.plot(xs, lr.intercept + lr.slope * xs, color=INK, lw=2, zorder=4)
        ax.axhline(0, color=MUTED, lw=0.8)
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("Cool-season index")
        ax.annotate(f"r = {rr:.2f}\np = {pp:.3f}\nn = {n}", xy=(0.04, 0.04),
                    xycoords="axes fraction", fontsize=9.5, color=INK,
                    va="bottom")
    axes[0].set_ylabel("Apr–Oct rainfall anomaly (%)")
    fig.suptitle("Rainfall vs climate drivers (illustrative association, not causal attribution)",
                 fontsize=13, weight="bold")
    axes[2].annotate(CREDIT, xy=(1.0, -0.22), xycoords="axes fraction",
                     ha="right", va="top", fontsize=8, color=MUTED)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig("charts/04_driver_correlation.png")
    plt.close(fig)


# --- 5. station x decade heatmap (spatial texture) ---------------------------
def chart_station_decade(clean):
    df = clean.dropna(subset=["cool_anom_pct"]).copy()
    df["decade"] = (df.year // 10 * 10)
    lab = {1950: "1950s", 1960: "1960s", 1970: "1970s", 1980: "1980s",
           1990: "1990s", 2000: "2000s", 2010: "2010s", 2020: "2020–24"}
    piv = df.pivot_table(index="station", columns="decade",
                         values="cool_anom_pct", aggfunc="mean")
    order = (clean.groupby("station").baseline_mm.first()
             .sort_values(ascending=False).index)
    piv = piv.reindex(order)
    cmap = LinearSegmentedColormap.from_list("dry_wet", [TOMATO, PAPER, SEA])
    vmax = np.nanmax(np.abs(piv.values))
    fig, ax = plt.subplots(figsize=(10, 4.8))
    im = ax.imshow(piv.values, cmap=cmap, vmin=-vmax, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(piv.columns)))
    ax.set_xticklabels([lab.get(c, str(c)) for c in piv.columns])
    ax.set_yticks(range(len(piv.index)))
    ax.set_yticklabels([f"{s} ({clean[clean.station==s].baseline_mm.iloc[0]:.0f} mm)"
                        for s in piv.index])
    ax.grid(False)
    for i in range(piv.shape[0]):
        for j in range(piv.shape[1]):
            v = piv.values[i, j]
            if np.isfinite(v):
                ax.text(j, i, f"{v:+.0f}", ha="center", va="center",
                        fontsize=8.5, color=INK)
    cb = fig.colorbar(im, ax=ax, shrink=0.85)
    cb.set_label("Decadal mean Apr–Oct anomaly vs 1950–1974 (%)")
    ax.set_title("Region-wide decline: every station drier by the 2000s")
    credit(ax)
    fig.savefig("charts/05_station_decade.png")
    plt.close(fig)


def main():
    apply_style()
    reg, clean, drivers, step = load()
    chart_timeseries(reg)
    chart_stepchange(reg, step)
    chart_trend(reg)
    chart_drivers(reg, drivers)
    chart_station_decade(clean)
    print("Wrote 5 charts to charts/")


if __name__ == "__main__":
    main()
