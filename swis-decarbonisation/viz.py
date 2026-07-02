"""
viz.py: publication-quality charts for the SWIS decarbonisation analysis.

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
from analysis import complete_years

INK, MUTED, PAPER = "#1A1614", "#6B6259", "#FBF4E6"
TOMATO, MANGO, FOREST, SEA, MAWAR, INDIGO = (
    "#FF5C39", "#FFC234", "#1F9D55", "#1FA9C7", "#E84BA0", "#2E3192")

FUEL_COLORS = {
    "coal": INK, "gas": MUTED, "distillate": MAWAR,
    "wind": SEA, "solar": MANGO, "bio": FOREST,
    "storage": INDIGO, "other": "#B7AC9B",
}
CREDIT = "Data: AEMO WEM data portal (SWIS)  ·  Analysis: A. Katili"


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


def fuel_order(wide):
    return [f for f in FUEL_COLORS if f in wide.columns]


# --- 1. stacked fuel mix ------------------------------------------------------
def chart_mix(wide, charts):
    order = fuel_order(wide)
    fig, ax = plt.subplots(figsize=(10, 5.6))
    ax.stackplot(wide.index, [wide[f].values for f in order],
                 labels=order, colors=[FUEL_COLORS[f] for f in order],
                 alpha=0.92)
    ax.set_title("What powers WA's main grid, year by year")
    ax.set_ylabel("Share of SWIS generation (%)")
    ax.set_xlabel("Year")
    ax.set_ylim(0, 100)
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5))
    credit(ax)
    fig.savefig(os.path.join(charts, "01_fuel_mix.png"))
    plt.close(fig)


# --- 2. renewables share with trend --------------------------------------------
def chart_renewables(wide, charts):
    renew = wide.reindex(columns=["wind", "solar", "bio"], fill_value=0.0).sum(axis=1)
    years = wide.index.values.astype(float)
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.plot(years, renew.values, color=FOREST, lw=2.4, marker="o", ms=4.5,
            zorder=3, label="Wind + solar + bio share")
    sen, _ = su.sens_slope(years, renew.values)
    r = su.linregress(years, renew.values)
    xs = np.linspace(years.min(), years.max(), 50)
    ax.plot(xs, r.intercept + r.slope * xs, color=INK, lw=1.6, ls="--",
            label=f"OLS {10 * r.slope:+.1f} pp/decade (Sen {10 * sen:+.1f})")
    ax.set_title("Renewables' share of SWIS generation")
    ax.set_ylabel("Share (%)")
    ax.set_xlabel("Year")
    ax.legend(loc="upper left")
    credit(ax)
    fig.savefig(os.path.join(charts, "02_renewables_share.png"))
    plt.close(fig)


# --- 3. coal vs renewables crossover ---------------------------------------------
def chart_coal(wide, charts):
    fig, ax = plt.subplots(figsize=(10, 5.2))
    if "coal" in wide.columns:
        ax.plot(wide.index, wide["coal"], color=INK, lw=2.4, marker="o", ms=4.5,
                label="Coal")
    renew = wide.reindex(columns=["wind", "solar", "bio"], fill_value=0.0).sum(axis=1)
    ax.plot(wide.index, renew, color=FOREST, lw=2.4, marker="s", ms=4.5,
            label="Wind + solar + bio")
    ax.set_title("Coal down, renewables up")
    ax.set_ylabel("Share of SWIS generation (%)")
    ax.set_xlabel("Year")
    ax.legend(loc="center left")
    credit(ax)
    fig.savefig(os.path.join(charts, "03_coal_vs_renewables.png"))
    plt.close(fig)


# --- 4. emissions intensity (only if computed) --------------------------------------
def chart_intensity(data_dir, charts):
    path = os.path.join(data_dir, "intensity_summary.csv")
    if not os.path.exists(path):
        print("intensity_summary.csv absent; skipping the intensity chart "
              "(fill data/emission_factors.csv to enable it)")
        return
    it = pd.read_csv(path)
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.plot(it.year, it.intensity_t_per_MWh, color=TOMATO, lw=2.4, marker="o",
            ms=4.5)
    ax.set_title("Emissions intensity of SWIS generation")
    ax.set_ylabel("t CO2-e per MWh (NGA fuel factors)")
    ax.set_xlabel("Year")
    credit(ax)
    fig.savefig(os.path.join(charts, "04_intensity.png"))
    plt.close(fig)


def main(data_dir="data", charts="charts"):
    annual_path = os.path.join(data_dir, "annual_fuel_mix.csv")
    if not os.path.exists(annual_path):
        raise SystemExit("Clean data not found; run build_dataset.py first.")
    apply_style()
    os.makedirs(charts, exist_ok=True)
    annual = pd.read_csv(annual_path)
    monthly = pd.read_csv(os.path.join(data_dir, "generation_by_fuel_month.csv"))
    annual = annual[annual.year.isin(complete_years(monthly))]
    wide = annual.pivot_table(index="year", columns="fuel", values="share_pct",
                              aggfunc="sum").fillna(0.0)
    chart_mix(wide, charts)
    chart_renewables(wide, charts)
    chart_coal(wide, charts)
    chart_intensity(data_dir, charts)
    print(f"Wrote charts to {charts}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or ["data"]))
