"""
viz.py: publication-quality charts for the Fremantle high-water analysis.

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
CREDIT = ("Data: UHSLC hourly, Fremantle (station 175)  ·  "
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


# --- 1. high-water hours per year (the headline) ---------------------------
def chart_hours(ok, b2, charts):
    fig, ax = plt.subplots(figsize=(10, 5.4))
    colors = [SEA if f == "rqds" else MANGO for f in ok.feed]
    ax.bar(ok.year, ok.hours_ge_b2, color=colors, width=0.8, zorder=3)
    sen, inter = su.sens_slope(ok.year.values.astype(float),
                               ok.hours_ge_b2.values.astype(float))
    xs = np.array([ok.year.min(), ok.year.max()], float)
    ax.plot(xs, inter + sen * xs, color=TOMATO, lw=2.0, ls="--", zorder=4,
            label=f"Sen's slope {sen:+.1f} hours/yr each year")
    from matplotlib.patches import Patch
    handles, labels = ax.get_legend_handles_labels()
    handles += [Patch(color=SEA), Patch(color=MANGO)]
    labels += ["Research-quality years", "Fast-delivery years (2022 on)"]
    ax.set_title(f"Hours at or above {b2} mm each year at Fremantle")
    ax.set_ylabel(f"Hours >= {b2} mm (99.5th pct of 1984-1993)")
    ax.set_xlabel("Year")
    ax.legend(handles, labels, loc="upper left")
    credit(ax)
    fig.savefig(os.path.join(charts, "01_highwater_hours.png"))
    plt.close(fig)


# --- 2. the baseline lift ---------------------------------------------------
def chart_lift(ok, b2, charts):
    fig, ax = plt.subplots(figsize=(10, 5.4))
    ax.plot(ok.year, ok.max_mm, color=TOMATO, lw=1.6, marker="o", ms=3,
            zorder=3, label="Highest hour of the year")
    ax.plot(ok.year, ok.mean_mm, color=SEA, lw=1.8, zorder=3,
            label="Annual mean level")
    ax.axhline(b2, color=INK, lw=1.2, ls=":",
               label=f"High-water benchmark ({b2} mm)")
    ax.set_title("The extremes ride on the rising mean")
    ax.set_ylabel("Hourly sea level (mm, station datum)")
    ax.set_xlabel("Year")
    ax.legend(loc="center left")
    credit(ax)
    fig.savefig(os.path.join(charts, "02_baseline_lift.png"))
    plt.close(fig)


# --- 3. same storms, higher sea ---------------------------------------------
def chart_decomposition(dec, b2, charts):
    dec = dec.copy()
    dec["decade"] = (dec.year // 10) * 10
    g = dec.groupby("decade").agg(
        raw=("hours_ge_b2", "mean"), adj=("adj_hours_ge_b2", "mean"),
        n=("year", "size"))
    x = np.arange(len(g))
    fig, ax = plt.subplots(figsize=(9, 5.4))
    ax.bar(x - 0.2, g.raw, width=0.38, color=SEA, zorder=3,
           label="What happened")
    ax.bar(x + 0.2, g.adj, width=0.38, color=MUTED, zorder=3,
           label="Same hours with each year's mean anomaly removed")
    ax.set_xticks(x, [f"{int(d)}s\n({n} complete yrs)"
                      for d, n in zip(g.index, g.n)])
    ax.set_title("Same storms, higher sea")
    ax.set_ylabel(f"Hours >= {b2} mm per year (decade average)")
    ax.legend(loc="upper left")
    credit(ax)
    fig.savefig(os.path.join(charts, "03_same_storms.png"))
    plt.close(fig)


# --- 4. the distribution shift ----------------------------------------------
def chart_distribution(hourly_first, hourly_last, labels, charts):
    fig, ax = plt.subplots(figsize=(10, 5.4))
    top = max(hourly_first.max(), hourly_last.max())
    levels = np.arange(np.percentile(hourly_last, 90) // 10 * 10, top, 10)
    for vals, n_yrs, label, color in (
            (hourly_first, labels[0], labels[1], MUTED),
            (hourly_last, labels[2], labels[3], TOMATO)):
        hrs = [(vals >= L).sum() / n_yrs for L in levels]
        ax.plot(levels, hrs, color=color, lw=2.2, label=label)
    ax.set_yscale("log")
    ax.set_title("Hours per year above each level: then vs now")
    ax.set_ylabel("Hours per year at or above level (log scale)")
    ax.set_xlabel("Hourly sea level (mm, station datum)")
    ax.legend()
    credit(ax)
    fig.savefig(os.path.join(charts, "04_distribution_shift.png"))
    plt.close(fig)


# --- 5. the flood calendar ---------------------------------------------------
def chart_calendar(monthly, b2, charts):
    piv = (monthly.pivot_table(index="month", columns="year",
                               values="hours_ge_b2", aggfunc="sum")
           .reindex(index=range(1, 13)).fillna(0))
    fig, ax = plt.subplots(figsize=(11, 4.6))
    im = ax.imshow(piv.values, aspect="auto", cmap="YlGnBu",
                   extent=[piv.columns.min() - 0.5, piv.columns.max() + 0.5,
                           12.5, 0.5])
    ax.set_yticks(range(1, 13),
                  ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"])
    ax.set_title("When the high water comes: hours over the benchmark")
    ax.set_xlabel("Year")
    ax.set_ylabel("Month")
    ax.grid(False)
    cb = fig.colorbar(im, ax=ax, pad=0.01)
    cb.set_label(f"Hours >= {b2} mm")
    credit(ax)
    fig.savefig(os.path.join(charts, "05_flood_calendar.png"))
    plt.close(fig)


def main(data_dir="data", charts="charts"):
    path = os.path.join(data_dir, "annual_metrics.csv")
    if not os.path.exists(path):
        raise SystemExit("Clean data not found; run build_dataset.py and "
                         "analysis.py first.")
    apply_style()
    os.makedirs(charts, exist_ok=True)
    marks = pd.read_csv(os.path.join(data_dir, "benchmarks.csv"))
    b2 = int(marks[marks.benchmark == "b2"].level_mm.iloc[0])
    annual = pd.read_csv(path)
    ok = annual[annual.complete].sort_values("year")
    dec = pd.read_csv(os.path.join(data_dir, "decomposition.csv"))
    monthly = pd.read_csv(os.path.join(data_dir, "monthly_highwater.csv"))

    chart_hours(ok, b2, charts)
    chart_lift(ok, b2, charts)
    chart_decomposition(dec, b2, charts)

    import analysis
    hourly = analysis.load_hourly(data_dir)
    completeness = analysis.complete_years(hourly)
    ok_years = sorted(y for y, c in completeness.items() if c)
    first_years = [y for y in ok_years
                   if analysis.BASE_START <= y <= analysis.BASE_END]
    last_years = ok_years[-10:]
    hf = hourly[hourly.t.dt.year.isin(first_years)].mm.values
    hl = hourly[hourly.t.dt.year.isin(last_years)].mm.values
    chart_distribution(
        hf, hl,
        (len(first_years), f"{min(first_years)}-{max(first_years)}",
         len(last_years), f"{min(last_years)}-{max(last_years)}"), charts)
    chart_calendar(monthly[monthly.complete_year], b2, charts)
    print(f"Wrote 5 charts to {charts}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or ["data"]))
