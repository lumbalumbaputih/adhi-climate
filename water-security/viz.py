"""
viz.py: publication-quality charts for the Perth water-security analysis.

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

# Hidup palette
INK, MUTED, PAPER = "#1A1614", "#6B6259", "#FBF4E6"
TOMATO, MANGO, FOREST, SEA, MAWAR, INDIGO = (
    "#FF5C39", "#FFC234", "#1F9D55", "#1FA9C7", "#E84BA0", "#2E3192")

BASE_START, BASE_END = 1975, 1999
CREDIT = ("Data: BoM Hydrologic Reference Stations; rainfall from GHCN-Daily "
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


def rainfall_mm_adjusted():
    rain_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "rainfall-decline", "data")
    reg = pd.read_csv(os.path.join(rain_dir, "annual_cool_season_anomaly.csv"))
    clean = pd.read_csv(os.path.join(rain_dir, "rainfall_swwa_clean.csv"))
    full_base = clean.groupby("station").baseline_mm.first().mean()
    reg["rain_mm_adj"] = full_base * (1.0 + reg.regional_anom_pct / 100.0)
    return reg[["year", "rain_mm_adj"]]


# --- 1. regional streamflow anomaly time series -------------------------------
def chart_timeseries(reg, charts):
    fig, ax = plt.subplots(figsize=(10, 5.2))
    y = reg.regional_anom_pct.values
    colors = [SEA if v >= 0 else TOMATO for v in y]
    ax.bar(reg.water_year, y, color=colors, width=0.85, zorder=2)
    run = pd.Series(y).rolling(5, center=True, min_periods=3).mean()
    ax.plot(reg.water_year, run, color=INK, lw=2.2, zorder=3, label="5-year mean")
    ax.axhline(0, color=MUTED, lw=1)
    ax.set_title("SW WA gauged streamflow anomaly by water year")
    ax.set_ylabel(f"May-April total vs {BASE_START}-{BASE_END} (%)")
    ax.set_xlabel("Water year (year of the May start)")
    ax.legend(loc="lower left")
    credit(ax)
    fig.savefig(os.path.join(charts, "01_streamflow_anomaly.png"))
    plt.close(fig)


# --- 2. step change ------------------------------------------------------------
def chart_stepchange(reg, step, charts):
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.plot(reg.water_year, reg.regional_ML_adj / 1000.0, color=INK, lw=1.4,
            marker="o", ms=3.5, zorder=3)
    cp = int(step.pettitt_change_year)
    pre = reg[reg.water_year < cp]
    post = reg[reg.water_year >= cp]
    for seg, col, lab in ((pre, SEA, "pre"), (post, TOMATO, "post")):
        if len(seg):
            m = seg.regional_ML_adj.mean() / 1000.0
            ax.hlines(m, seg.water_year.min(), seg.water_year.max(),
                      color=col, lw=2.6, zorder=4,
                      label=f"{lab}-{cp} mean: {m:,.0f} GL")
    ax.axvline(cp - 0.5, color=MUTED, lw=1.2, ls="--")
    ax.annotate(f"Pettitt change point: {cp}\np = {step.pettitt_p:.3g}",
                xy=(0.02, 0.05), xycoords="axes fraction", ha="left",
                va="bottom", fontsize=10, color=INK)
    ax.set_title("The step down in SW WA streamflow")
    ax.set_ylabel("Regional water-year flow (GL, composition-adjusted)")
    ax.set_xlabel("Water year")
    ax.legend(loc="upper right")
    credit(ax)
    fig.savefig(os.path.join(charts, "02_stepchange.png"))
    plt.close(fig)


# --- 3. rainfall vs streamflow amplification -----------------------------------
def chart_amplification(reg, charts):
    rain = rainfall_mm_adjusted()
    j = reg.merge(rain, left_on="water_year", right_on="year", how="inner")
    rbase = j[(j.water_year >= BASE_START) & (j.water_year <= BASE_END)]
    fig, ax = plt.subplots(figsize=(10, 5.2))
    rp = 100.0 * (j.rain_mm_adj / rbase.rain_mm_adj.mean() - 1.0)
    qp = 100.0 * (j.regional_ML_adj / rbase.regional_ML_adj.mean() - 1.0)
    ax.plot(j.water_year, rp.rolling(5, center=True, min_periods=3).mean(),
            color=INDIGO, lw=2.2, label="Rainfall (5-yr mean)")
    ax.plot(j.water_year, qp.rolling(5, center=True, min_periods=3).mean(),
            color=TOMATO, lw=2.2, label="Streamflow (5-yr mean)")
    ax.axhline(0, color=MUTED, lw=1)
    ax.set_title("Streamflow falls much faster than rainfall")
    ax.set_ylabel(f"Change vs {BASE_START}-{BASE_END} mean (%)")
    ax.set_xlabel("Water year")
    ax.legend(loc="lower left")
    credit(ax)
    fig.savefig(os.path.join(charts, "03_amplification.png"))
    plt.close(fig)


# --- 4. elasticity scatter ------------------------------------------------------
def chart_elasticity(reg, elast, charts):
    rain = rainfall_mm_adjusted()
    j = reg.merge(rain, left_on="water_year", right_on="year", how="inner")
    fig, ax = plt.subplots(figsize=(7.6, 6.4))
    x, y = np.log(j.rain_mm_adj), np.log(j.regional_ML_adj)
    ax.scatter(x, y, s=34, color=SEA, edgecolor=INK, lw=0.5, zorder=3)
    r = su.linregress(x, y)
    xs = np.linspace(x.min(), x.max(), 50)
    ax.plot(xs, r.intercept + r.slope * xs, color=TOMATO, lw=2.2,
            label=f"slope (elasticity) = {r.slope:.2f}, r$^2$ = {r.r_squared:.2f}")
    ax.set_title("Rainfall-runoff elasticity, log-log")
    ax.set_xlabel("ln(cool-season rainfall, mm)")
    ax.set_ylabel("ln(water-year streamflow, ML)")
    ax.legend(loc="upper left")
    credit(ax)
    fig.savefig(os.path.join(charts, "04_elasticity.png"))
    plt.close(fig)


def main(data_dir="data", charts="charts"):
    path = os.path.join(data_dir, "annual_streamflow_anomaly.csv")
    if not os.path.exists(path):
        raise SystemExit("Clean data not found; run build_dataset.py and "
                         "analysis.py first.")
    apply_style()
    os.makedirs(charts, exist_ok=True)
    reg = pd.read_csv(path)
    step = pd.read_csv(os.path.join(data_dir, "stepchange_summary.csv")).iloc[0]
    elast = pd.read_csv(os.path.join(data_dir, "elasticity_summary.csv")).iloc[0]
    chart_timeseries(reg, charts)
    chart_stepchange(reg, step, charts)
    chart_amplification(reg, charts)
    chart_elasticity(reg, elast, charts)
    print(f"Wrote 4 charts to {charts}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or ["data"]))
