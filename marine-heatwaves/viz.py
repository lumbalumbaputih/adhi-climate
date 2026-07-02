"""
viz.py: publication-quality charts for the marine-heatwave analysis.

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
CAT_COLORS = {"I Moderate": MANGO, "II Strong": TOMATO,
              "III Severe": MAWAR, "IV Extreme": INK}
CREDIT = "Data: NOAA OISST v2.1 (via ERDDAP)  ·  Analysis: A. Katili"


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


# --- 1. MHW days per year ------------------------------------------------------
def chart_days(annual, charts):
    ok = annual[annual.complete]
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.bar(ok.year, ok.mhw_days, color=TOMATO, width=0.85, zorder=2)
    run = ok.mhw_days.rolling(5, center=True, min_periods=3).mean()
    ax.plot(ok.year, run, color=INK, lw=2.2, zorder=3, label="5-year mean")
    ax.set_title("Marine heatwave days per year off the WA coast")
    ax.set_ylabel("Days inside a marine heatwave")
    ax.set_xlabel("Year")
    ax.legend(loc="upper left")
    credit(ax)
    fig.savefig(os.path.join(charts, "01_mhw_days.png"))
    plt.close(fig)


# --- 2. event timeline ------------------------------------------------------------
def chart_events(events, charts):
    fig, ax = plt.subplots(figsize=(10, 5.6))
    for cat, color in CAT_COLORS.items():
        e = events[events.category == cat]
        if len(e):
            ax.scatter(e.peak_date, e.max_intensity_c, s=e.duration_days * 3.0,
                       color=color, alpha=0.8, edgecolor=INK, lw=0.5,
                       label=cat, zorder=3)
    ax.set_title("Every detected marine heatwave (size = duration)")
    ax.set_ylabel("Peak intensity (C above climatology)")
    ax.set_xlabel("Event peak date")
    ax.legend(loc="upper left", title="Hobday category")
    credit(ax)
    fig.savefig(os.path.join(charts, "02_event_timeline.png"))
    plt.close(fig)


# --- 3. the biggest event, zoomed ---------------------------------------------------
def chart_zoom(flagged, events, charts):
    if not len(events):
        return
    big = events.loc[events.max_intensity_c.idxmax()]
    pad = pd.Timedelta(days=90)
    w = flagged[(flagged.date >= pd.Timestamp(big.start) - pad)
                & (flagged.date <= pd.Timestamp(big.end) + pad)]
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.plot(w.date, w.clim, color=MUTED, lw=1.6, label="Climatology (1982-2011)")
    ax.plot(w.date, w.thr, color=INK, lw=1.4, ls="--", label="90th percentile")
    ax.plot(w.date, w.sst, color=INDIGO, lw=1.8, label="Observed SST")
    hot = w[w.mhw]
    ax.fill_between(w.date, w.thr, w.sst, where=(w.sst > w.thr),
                    color=TOMATO, alpha=0.5, label="Marine heatwave")
    ax.set_title(f"The most intense event on record "
                 f"(peak {pd.Timestamp(big.peak_date).date()}, {big.category})")
    ax.set_ylabel("SST (C)")
    ax.set_xlabel("Date")
    ax.legend(loc="upper left", fontsize=9)
    credit(ax)
    fig.savefig(os.path.join(charts, "03_biggest_event.png"))
    plt.close(fig)


# --- 4. annual mean SST ---------------------------------------------------------------
def chart_sst(annual, charts):
    ok = annual[annual.complete]
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.plot(ok.year, ok.mean_sst_c, color=SEA, lw=2.2, marker="o", ms=4)
    r = su.linregress(ok.year.values.astype(float), ok.mean_sst_c.values)
    xs = np.linspace(ok.year.min(), ok.year.max(), 40)
    ax.plot(xs, r.intercept + r.slope * xs, color=INK, lw=1.6, ls="--",
            label=f"OLS {10 * r.slope:+.2f} C/decade (p = {r.pvalue:.3g})")
    ax.set_title("Annual mean SST in the study box")
    ax.set_ylabel("SST (C)")
    ax.set_xlabel("Year")
    ax.legend(loc="upper left")
    credit(ax)
    fig.savefig(os.path.join(charts, "04_mean_sst.png"))
    plt.close(fig)


def main(data_dir="data", charts="charts"):
    apath = os.path.join(data_dir, "annual_mhw_metrics.csv")
    if not os.path.exists(apath):
        raise SystemExit("Clean data not found; run build_dataset.py first.")
    apply_style()
    os.makedirs(charts, exist_ok=True)
    annual = pd.read_csv(apath)
    events = pd.read_csv(os.path.join(data_dir, "mhw_events.csv"),
                         parse_dates=["start", "end", "peak_date"])
    flagged = pd.read_csv(os.path.join(data_dir, "sst_flagged.csv"),
                          parse_dates=["date"])
    chart_days(annual, charts)
    chart_events(events, charts)
    chart_zoom(flagged, events, charts)
    chart_sst(annual, charts)
    print(f"Wrote charts to {charts}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or ["data"]))
