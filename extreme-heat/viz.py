"""
viz.py: publication-quality charts for the extreme-heat analysis.

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
STATION_COLORS = [TOMATO, INDIGO, FOREST, MAWAR, SEA, MANGO]
CREDIT = ("Data: GHCN-Daily (NOAA NCEI; BoM station observations)  ·  "
          "Analysis: A. Katili")


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


def per_station(m, col, title, ylabel, fname, charts):
    stations = sorted(m.station.unique())
    fig, axes = plt.subplots(len(stations), 1, figsize=(10, 3.4 * len(stations)),
                             sharex=True)
    axes = np.atleast_1d(axes)
    for ax, st, color in zip(axes, stations, STATION_COLORS):
        g = m[m.station == st].sort_values("year")
        ax.bar(g.year, g[col], color=color, width=0.85, alpha=0.85, zorder=2)
        run = g[col].rolling(10, center=True, min_periods=5).mean()
        ax.plot(g.year, run, color=INK, lw=2.2, zorder=3, label="10-year mean")
        sen, _ = su.sens_slope(g.year.values.astype(float), g[col].values.astype(float))
        ax.set_title(f"{g.name.iloc[0]}  (Sen {10 * sen:+.2f}/decade)", fontsize=12)
        ax.set_ylabel(ylabel)
        ax.legend(loc="upper left", fontsize=9)
    axes[-1].set_xlabel("Year")
    fig.suptitle(title, fontweight="bold", fontsize=15, y=1.001)
    credit(axes[-1])
    fig.tight_layout()
    fig.savefig(os.path.join(charts, fname))
    plt.close(fig)


def chart_decades(dec, charts):
    stations = sorted(dec.station.unique())
    fig, ax = plt.subplots(figsize=(10, 5.2))
    width = 0.8 / len(stations)
    for i, (st, color) in enumerate(zip(stations, STATION_COLORS)):
        g = dec[dec.station == st].sort_values("decade")
        g = g[g.decade >= 1950]
        ax.bar(g.decade + i * 10 * width, g.days_ge_35, width=10 * width * 0.92,
               color=color, label=g.name.iloc[0], zorder=2)
    ax.set_title("Hot days per year, decade by decade")
    ax.set_ylabel("Mean days at or above 35 C per year")
    ax.set_xlabel("Decade")
    ax.legend(loc="upper left")
    credit(ax)
    fig.savefig(os.path.join(charts, "04_decades.png"))
    plt.close(fig)


def main(data_dir="data", charts="charts"):
    path = os.path.join(data_dir, "annual_heat_metrics.csv")
    if not os.path.exists(path):
        raise SystemExit("Clean data not found; run build_dataset.py first.")
    apply_style()
    os.makedirs(charts, exist_ok=True)
    m = pd.read_csv(path)
    m = m[m.complete]
    dec = pd.read_csv(os.path.join(data_dir, "decade_summary.csv"))
    per_station(m, "days_ge_35", "Days at or above 35 C each year",
                "days", "01_days_ge_35.png", charts)
    per_station(m, "txx_c", "The hottest day of each year (TXx)",
                "TXx (C)", "02_txx.png", charts)
    per_station(m, "hw_events",
                "Heatwave events (3+ days above the day-of-year 90th percentile)",
                "events", "03_heatwaves.png", charts)
    chart_decades(dec, charts)
    print(f"Wrote 4 charts to {charts}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or ["data"]))
