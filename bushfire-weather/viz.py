"""
viz.py: publication-quality charts for the bushfire-weather analysis.

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
SITE_ORDER = ["perth_airport", "merredin", "manjimup", "margaret_river"]
SITE_LABEL = {"perth_airport": "Perth Airport", "merredin": "Merredin",
              "manjimup": "Manjimup", "margaret_river": "Margaret River"}
SITE_COLORS = {"perth_airport": TOMATO, "merredin": MANGO,
               "manjimup": FOREST, "margaret_river": SEA}
CREDIT = ("Data: ERA5 (Copernicus/ECMWF via Open-Meteo), GHCN-Daily (NOAA "
          "NCEI)  ·  Analysis: A. Katili")


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


def chart_vh_days(sm, charts):
    fig, axes = plt.subplots(len(SITE_ORDER), 1,
                             figsize=(10, 3.2 * len(SITE_ORDER)), sharex=True)
    for ax, site in zip(np.atleast_1d(axes), SITE_ORDER):
        g = sm[sm.site == site].sort_values("season")
        ax.bar(g.season, g.days_vh, color=SITE_COLORS[site], width=0.85,
               alpha=0.85, zorder=2)
        run = g.days_vh.rolling(10, center=True, min_periods=5).mean()
        ax.plot(g.season, run, color=INK, lw=2.2, zorder=3,
                label="10-season mean")
        late = g[g.season >= 1975]
        sen, _ = su.sens_slope(late.season.values.astype(float),
                               late.days_vh.values.astype(float))
        ax.set_title(f"{SITE_LABEL[site]}  (Sen {10 * sen:+.1f}/decade since "
                     "1975)", fontsize=12)
        ax.set_ylabel("days")
        ax.axvspan(g.season.min() - 0.5, 1974.5, color=MUTED, alpha=0.08,
                   zorder=1)
        ax.legend(loc="upper right", fontsize=9)
    last = np.atleast_1d(axes)[-1]
    last.set_xlabel("Fire season (labelled by starting year); shaded = "
                    "pre-satellite reanalysis, read with caution")
    fig.suptitle("Very High fire-danger days per season (FFDI >= 25)",
                 fontweight="bold", fontsize=15, y=1.001)
    last.annotate(CREDIT, xy=(1.0, -0.30), xycoords="axes fraction",
                  ha="right", va="top", fontsize=8, color=MUTED)
    fig.tight_layout()
    fig.savefig(os.path.join(charts, "01_very_high_days.png"))
    plt.close(fig)


def chart_decades(sm, charts):
    d = sm.copy()
    d["decade"] = (d.season // 10) * 10
    dec = d.groupby(["site", "decade"], as_index=False).days_vh.mean()
    dec = dec[dec.decade >= 1950]
    fig, ax = plt.subplots(figsize=(10, 5.2))
    width = 0.8 / len(SITE_ORDER)
    for i, site in enumerate(SITE_ORDER):
        g = dec[dec.site == site].sort_values("decade")
        ax.bar(g.decade + i * 10 * width, g.days_vh, width=10 * width * 0.92,
               color=SITE_COLORS[site], label=SITE_LABEL[site], zorder=2)
    ax.set_title("Very High fire-danger days, decade by decade")
    ax.set_ylabel("Mean days per season (FFDI >= 25)")
    ax.set_xlabel("Decade")
    ax.legend(loc="upper left")
    credit(ax)
    fig.savefig(os.path.join(charts, "02_decades.png"))
    plt.close(fig)


def chart_heatmap(data_dir, charts):
    daily = pd.read_csv(os.path.join(data_dir,
                                     "fire_weather_daily_perth_airport.csv"),
                        parse_dates=["date"])
    daily["year"] = daily.date.dt.year
    daily["month"] = daily.date.dt.month
    pv = daily.pivot_table(index="month", columns="year", values="ffdi",
                           aggfunc="mean")
    order = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
    pv = pv.reindex(order)
    fig, ax = plt.subplots(figsize=(12, 5))
    im = ax.pcolormesh(pv.columns, np.arange(len(order)), pv.values,
                       cmap="YlOrRd", shading="nearest")
    ax.set_yticks(np.arange(len(order)))
    ax.set_yticklabels(["Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
                        "Jan", "Feb", "Mar", "Apr", "May", "Jun"])
    ax.set_title("Perth Airport: mean FFDI by month and year")
    ax.set_xlabel("Year")
    ax.grid(False)
    fig.colorbar(im, ax=ax, label="mean FFDI")
    credit(ax)
    fig.savefig(os.path.join(charts, "03_seasonal_heatmap.png"))
    plt.close(fig)


def chart_validation(data_dir, charts):
    era = pd.read_csv(os.path.join(data_dir,
                                   "fire_weather_daily_perth_airport.csv"),
                      parse_dates=["date"])
    obs = pd.read_csv(os.path.join(data_dir, "ghcn_perth_airport_daily.csv"),
                      parse_dates=["date"])
    j = era.merge(obs, on="date").dropna(subset=["tmax", "tmax_obs"])
    r = su.linregress(j.tmax_obs.values, j.tmax.values)
    fig, ax = plt.subplots(figsize=(7.2, 7))
    ax.hexbin(j.tmax_obs, j.tmax, gridsize=60, cmap="YlOrRd", mincnt=1)
    lim = [5, 50]
    ax.plot(lim, lim, color=INK, lw=1.5, ls="--", label="1:1")
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_title("ERA5 vs observed daily maximum, Perth Airport")
    ax.set_xlabel("GHCN-Daily station TMAX (C)")
    ax.set_ylabel("ERA5 grid-cell TMAX (C)")
    bias = (j.tmax - j.tmax_obs).mean()
    ax.annotate(f"r = {r.rvalue:.3f}\nbias = {bias:+.2f} C\nn = {len(j):,}",
                xy=(0.04, 0.96), xycoords="axes fraction", va="top",
                fontsize=11, color=INK)
    ax.legend(loc="lower right")
    credit(ax)
    fig.savefig(os.path.join(charts, "04_validation.png"))
    plt.close(fig)


def chart_season_span(data_dir, charts):
    daily = pd.read_csv(os.path.join(data_dir,
                                     "fire_weather_daily_perth_airport.csv"),
                        parse_dates=["date"])
    d = daily[daily.date.dt.month.isin((10, 11, 12, 1, 2, 3, 4))].copy()
    y = d.date.dt.year.values.copy()
    m = d.date.dt.month.values
    y[m <= 4] -= 1
    d["season"] = y
    start = pd.to_datetime(d.season.astype(str) + "-10-01")
    d["doy"] = (d.date - start.values).dt.days
    rows = []
    for season, g in d.groupby("season"):
        vh = g[g.ffdi >= 25]
        if len(g) < 200 or len(vh) < 2:
            continue
        rows.append({"season": season, "first": vh.doy.min(),
                     "last": vh.doy.max()})
    b = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(10, 5.6))
    ax.fill_between(b.season, b.first, b.last, color=TOMATO, alpha=0.35,
                    label="Very High season (first to last FFDI >= 25 day)")
    ax.plot(b.season, b.first.rolling(10, center=True, min_periods=5).mean(),
            color=INK, lw=2)
    ax.plot(b.season, b.last.rolling(10, center=True, min_periods=5).mean(),
            color=INK, lw=2, label="10-season mean of the edges")
    yt = [0, 31, 61, 92, 123, 151, 182]
    ax.set_yticks(yt)
    ax.set_yticklabels(["1 Oct", "1 Nov", "1 Dec", "1 Jan", "1 Feb",
                        "1 Mar", "1 Apr"])
    ax.set_title("Perth Airport: when the Very High season starts and ends")
    ax.set_xlabel("Fire season (labelled by starting year)")
    ax.legend(loc="upper left", fontsize=9)
    credit(ax)
    fig.savefig(os.path.join(charts, "05_season_span.png"))
    plt.close(fig)


def main(data_dir="data", charts="charts"):
    path = os.path.join(data_dir, "seasonal_metrics.csv")
    if not os.path.exists(path):
        raise SystemExit("Clean data not found; run build_dataset.py and "
                         "analysis.py first.")
    apply_style()
    os.makedirs(charts, exist_ok=True)
    sm = pd.read_csv(path)
    chart_vh_days(sm, charts)
    chart_decades(sm, charts)
    chart_heatmap(data_dir, charts)
    chart_validation(data_dir, charts)
    chart_season_span(data_dir, charts)
    print(f"Wrote 5 charts to {charts}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or ["data"]))
