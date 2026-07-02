"""
viz.py: publication-quality charts for the wheat-yields analysis.

Self-contained: reads the CSVs in data/ and writes PNGs to charts/ at 300 dpi.
Uses the Adhi "Hidup" palette so figures match the rest of the suite.
Run:  python3 viz.py [data_dir] [charts_dir]
"""
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import stats_utils as su

INK, MUTED, PAPER = "#1A1614", "#6B6259", "#FBF4E6"
TOMATO, MANGO, FOREST, SEA, MAWAR, INDIGO = (
    "#FF5C39", "#FFC234", "#1F9D55", "#1FA9C7", "#E84BA0", "#2E3192")
CREDIT = ("Data: ABARES/ABS wheat statistics; rainfall from GHCN-Daily "
          "(NOAA NCEI)  ·  Analysis: A. Katili")


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


# --- 1. yield series with technology trend --------------------------------------
def chart_yield(j, trend, charts):
    fig, ax = plt.subplots(figsize=(10, 5.4))
    ax.plot(j.year, j.yield_t_ha, color=FOREST, lw=1.6, marker="o", ms=3.6,
            zorder=3, label="WA wheat yield")
    xs = np.linspace(j.year.min(), j.year.max(), 50)
    ax.plot(xs, trend.intercept + trend.slope_t_ha_per_yr * xs, color=INK,
            lw=1.8, ls="--", zorder=4,
            label=f"Technology trend {10 * trend.slope_t_ha_per_yr:+.2f} t/ha per decade")
    ax.set_title("WA wheat yields keep rising despite the drying")
    ax.set_ylabel("Yield (t/ha)")
    ax.set_xlabel("Season (year of sowing)")
    ax.legend(loc="upper left")
    credit(ax)
    fig.savefig(os.path.join(charts, "01_yield_trend.png"))
    plt.close(fig)


# --- 2. detrended yield vs rainfall scatter ----------------------------------------
def chart_scatter(j, charts):
    fig, ax = plt.subplots(figsize=(7.8, 6.4))
    ax.scatter(j.regional_anom_pct, j.yield_anom_pct, s=36, color=SEA,
               edgecolor=INK, lw=0.5, zorder=3)
    r = su.linregress(j.regional_anom_pct, j.yield_anom_pct)
    xs = np.linspace(j.regional_anom_pct.min(), j.regional_anom_pct.max(), 40)
    ax.plot(xs, r.intercept + r.slope * xs, color=TOMATO, lw=2.2,
            label=f"{10 * r.slope:+.1f}% yield per 10% rain "
                  f"(r = {r.rvalue:+.2f}, p = {r.pvalue:.2g})")
    ax.axhline(0, color=MUTED, lw=1)
    ax.axvline(0, color=MUTED, lw=1)
    ax.set_title("Wet winters mean good harvests")
    ax.set_xlabel("Cool-season rainfall anomaly (%)")
    ax.set_ylabel("Yield anomaly vs technology trend (%)")
    ax.legend(loc="upper left")
    credit(ax)
    fig.savefig(os.path.join(charts, "02_sensitivity.png"))
    plt.close(fig)


# --- 3. paired standardized series ----------------------------------------------------
def chart_paired(j, charts):
    fig, ax = plt.subplots(figsize=(10, 5.2))
    z = lambda s: (s - s.mean()) / s.std()
    ax.plot(j.year, z(j.regional_anom_pct), color=INDIGO, lw=2.0,
            label="Rainfall anomaly (z-score)")
    ax.plot(j.year, z(j.yield_anom_pct), color=FOREST, lw=2.0,
            label="Detrended yield anomaly (z-score)")
    ax.axhline(0, color=MUTED, lw=1)
    ax.set_title("Yield anomalies track the winter rain")
    ax.set_ylabel("Standard deviations from mean")
    ax.set_xlabel("Season")
    ax.legend(loc="lower left")
    credit(ax)
    fig.savefig(os.path.join(charts, "03_paired_series.png"))
    plt.close(fig)


# --- 4. driest decile ---------------------------------------------------------------------
def chart_drought(j, sens, charts):
    cut = sens.driest_decile_cut_pct
    fig, ax = plt.subplots(figsize=(10, 5.2))
    colors = [TOMATO if v <= cut else "#B7AC9B" for v in j.regional_anom_pct]
    ax.bar(j.year, j.yield_anom_pct, color=colors, width=0.85, zorder=2)
    ax.axhline(0, color=MUTED, lw=1)
    ax.set_title("The driest tenth of winters (red) and what they did to yields")
    ax.set_ylabel("Yield anomaly vs technology trend (%)")
    ax.set_xlabel("Season")
    credit(ax)
    fig.savefig(os.path.join(charts, "04_drought_years.png"))
    plt.close(fig)


def main(data_dir="data", charts="charts"):
    jpath = os.path.join(data_dir, "joined_series.csv")
    if not os.path.exists(jpath):
        raise SystemExit("Clean data not found; run build_dataset.py and "
                         "analysis.py first.")
    apply_style()
    os.makedirs(charts, exist_ok=True)
    j = pd.read_csv(jpath)
    trend = pd.read_csv(os.path.join(data_dir, "yield_trend.csv")).iloc[0]
    sens = pd.read_csv(os.path.join(data_dir, "sensitivity_summary.csv")).iloc[0]
    chart_yield(j, trend, charts)
    chart_scatter(j, charts)
    chart_paired(j, charts)
    chart_drought(j, sens, charts)
    print(f"Wrote 4 charts to {charts}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or ["data"]))
