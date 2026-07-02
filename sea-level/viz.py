"""
viz.py: publication-quality charts for the Fremantle sea-level analysis.

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
CREDIT = "Data: PSMSL monthly RLR, Fremantle (station 111)  ·  Analysis: A. Katili"


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


# --- 1. the full record with trend --------------------------------------------
def chart_series(ok, charts):
    fig, ax = plt.subplots(figsize=(10, 5.4))
    ax.plot(ok.year, ok.anom_mm, color=SEA, lw=1.4, marker="o", ms=3,
            zorder=3, label="Annual mean")
    run = ok.anom_mm.rolling(10, center=True, min_periods=5).mean()
    ax.plot(ok.year, run, color=INK, lw=2.2, zorder=4, label="10-year mean")
    r = su.linregress(ok.year.values.astype(float), ok.anom_mm.values)
    xs = np.linspace(ok.year.min(), ok.year.max(), 60)
    ax.plot(xs, r.intercept + r.slope * xs, color=TOMATO, lw=1.8, ls="--",
            zorder=4, label=f"OLS {r.slope:+.2f} mm/yr (p = {r.pvalue:.2g})")
    ax.axhline(0, color=MUTED, lw=1)
    ax.set_title("Fremantle mean sea level since 1897")
    ax.set_ylabel("Annual mean vs 1990-2009 (mm)")
    ax.set_xlabel("Year")
    ax.legend(loc="upper left")
    credit(ax)
    fig.savefig(os.path.join(charts, "01_msl_series.png"))
    plt.close(fig)


# --- 2. rolling 30-year rates ----------------------------------------------------
def chart_rolling(roll, charts):
    if roll.empty:
        return
    mid = (roll.window_start + roll.window_end) / 2.0
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.plot(mid, roll.rate_mm_per_yr, color=INDIGO, lw=2.2, zorder=3)
    ax.fill_between(mid, 0, roll.rate_mm_per_yr, color=INDIGO, alpha=0.15)
    ax.axhline(0, color=MUTED, lw=1)
    ax.set_title("The rate of rise, 30-year window at a time")
    ax.set_ylabel("OLS rate (mm/yr)")
    ax.set_xlabel("Window centre year")
    credit(ax)
    fig.savefig(os.path.join(charts, "02_rolling_rate.png"))
    plt.close(fig)


# --- 3. era comparison ---------------------------------------------------------------
def chart_eras(trends, charts):
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    colors = [MUTED, SEA, TOMATO][:len(trends)]
    bars = ax.bar(trends.series, trends.ols_rate_mm_per_yr, color=colors,
                  width=0.55, zorder=2)
    for b, (_, r) in zip(bars, trends.iterrows()):
        ax.annotate(f"{r.ols_rate_mm_per_yr:+.2f}",
                    xy=(b.get_x() + b.get_width() / 2, b.get_height()),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", fontsize=11, weight="bold")
    ax.set_title("Sea-level rise by era")
    ax.set_ylabel("OLS rate (mm/yr)")
    plt.setp(ax.get_xticklabels(), rotation=12, ha="right")
    credit(ax)
    fig.savefig(os.path.join(charts, "03_eras.png"))
    plt.close(fig)


def main(data_dir="data", charts="charts"):
    path = os.path.join(data_dir, "msl_annual.csv")
    if not os.path.exists(path):
        raise SystemExit("Clean data not found; run build_dataset.py and "
                         "analysis.py first.")
    apply_style()
    os.makedirs(charts, exist_ok=True)
    annual = pd.read_csv(path)
    ok = annual[annual.complete].sort_values("year")
    trends = pd.read_csv(os.path.join(data_dir, "trend_summary.csv"))
    roll = pd.read_csv(os.path.join(data_dir, "rolling_rates.csv"))
    chart_series(ok, charts)
    chart_rolling(roll, charts)
    chart_eras(trends, charts)
    print(f"Wrote 3 charts to {charts}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or ["data"]))
