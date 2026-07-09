"""
viz.py: publication-quality charts for the transition-risk analysis.

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

INK, MUTED = "#1A1614", "#6B6259"
TOMATO, MANGO, FOREST, SEA, MAWAR, INDIGO = (
    "#FF5C39", "#FFC234", "#1F9D55", "#1FA9C7", "#E84BA0", "#2E3192")
SECTOR_COLORS = {
    "LNG / oil and gas": TOMATO, "Metal ore mining": MANGO,
    "Alumina and metals": INDIGO, "Other manufacturing": MAWAR,
    "Transport": SEA, "Electricity": FOREST, "Coal mining": "#8B5A2B",
    "Waste": MUTED, "Other": "#999188",
}
DECLINE = 0.049
PROJ_YEARS = [2025, 2026, 2027, 2028, 2029]
CREDIT = ("Data: Clean Energy Regulator, Safeguard facility data  ·  "
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


def credit(ax, y=-0.15):
    ax.annotate(CREDIT, xy=(1.0, y), xycoords="axes fraction", ha="right",
                va="top", fontsize=8, color=MUTED)


def chart_concentration(conc, charts):
    top = conc.head(15).iloc[::-1]
    fig, ax = plt.subplots(figsize=(10, 7.2))
    colors = [SECTOR_COLORS.get(s, "#999188") for s in top.sector]
    ax.barh(np.arange(len(top)), top.covered_t / 1e6, color=colors, zorder=2)
    ax.set_yticks(np.arange(len(top)))
    ax.set_yticklabels([f"{f}  ({p})" for f, p in
                        zip(top.facility, top.parent)], fontsize=9)
    ax.set_xlabel("Covered scope 1 emissions, 2024-25 (Mt CO2-e)")
    ax.set_title("WA's biggest Safeguard facilities")
    handles = [plt.Rectangle((0, 0), 1, 1, color=c)
               for s, c in SECTOR_COLORS.items()
               if s in set(top.sector)]
    labels = [s for s in SECTOR_COLORS if s in set(top.sector)]
    ax.legend(handles, labels, loc="lower right", fontsize=9)
    credit(ax)
    fig.savefig(os.path.join(charts, "01_concentration.png"))
    plt.close(fig)


def chart_sectors(sect, charts):
    keep = (sect.groupby("sector").covered_t.max().sort_values(ascending=False)
            .head(5).index)
    fig, ax = plt.subplots(figsize=(10, 5.6))
    for s in keep:
        g = sect[sect.sector == s].sort_values("year")
        ax.plot(g.year, g.covered_t / 1e6, lw=2.4, marker="o", ms=4,
                color=SECTOR_COLORS.get(s, "#999188"), label=s)
    ax.axvline(2022.5, color=MUTED, lw=1.2, ls="--")
    ax.annotate("Safeguard reformed\n(1 July 2023)", xy=(2022.55, ax.get_ylim()[1]),
                xytext=(2020.6, ax.get_ylim()[1] * 0.97), fontsize=9,
                color=MUTED, va="top")
    ax.set_title("WA covered emissions by sector")
    ax.set_ylabel("Mt CO2-e per compliance year")
    ax.set_xlabel("Compliance year (labelled by starting year)")
    ax.legend(loc="center left", fontsize=9)
    credit(ax)
    fig.savefig(os.path.join(charts, "02_sector_trends.png"))
    plt.close(fig)


def chart_headroom(hr, focus, charts):
    fig, axes = plt.subplots(3, 2, figsize=(12, 11), sharex=True)
    for ax, fac in zip(axes.ravel(), focus):
        g = hr[hr.facility == fac].sort_values("year")
        ax.plot(g.year, g.covered_t / 1e6, color=TOMATO, lw=2.4, marker="o",
                ms=4, label="covered emissions")
        orig = g[g.regime == "original"]
        ref = g[g.regime == "reformed"]
        ax.plot(orig.year, orig.baseline_t / 1e6, color=INK, lw=2,
                ls=":", label="baseline (original rules)")
        ax.plot(ref.year, ref.baseline_t / 1e6, color=INK, lw=2,
                label="baseline (reformed)")
        b0 = ref[ref.year == ref.year.max()].baseline_t.iloc[0]
        proj = [b0 * (1 - DECLINE) ** (y - ref.year.max()) for y in PROJ_YEARS]
        ax.plot(PROJ_YEARS, np.array(proj) / 1e6, color=INK, lw=2, ls="--",
                label="baseline at -4.9%/yr (default path)")
        ax.axvline(2022.5, color=MUTED, lw=1, ls="--")
        ax.set_title(fac[:40], fontsize=11)
        ax.set_ylabel("Mt CO2-e")
    axes[0, 0].legend(fontsize=8, loc="lower left")
    for ax in axes[-1]:
        ax.set_xlabel("Compliance year")
    fig.suptitle("Emissions vs baseline, WA's six biggest Safeguard "
                 "facilities", fontweight="bold", fontsize=15, y=1.0)
    credit(axes[-1, -1], y=-0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(charts, "03_headroom.png"))
    plt.close(fig)


def chart_crossover(hr, charts, fac="Wheatstone Operations"):
    g = hr[hr.facility == fac].sort_values("year")
    ref = g[g.regime == "reformed"]
    y0 = int(ref.year.max())
    e0 = float(ref[ref.year == y0].covered_t.iloc[0])
    b0 = float(ref[ref.year == y0].baseline_t.iloc[0])
    recent = g[g.year >= y0 - 5]
    import stats_utils as su
    sen, _ = su.sens_slope(recent.year.values.astype(float),
                           recent.covered_t.values.astype(float))
    years = [y0] + PROJ_YEARS
    base = [b0 * (1 - DECLINE) ** (y - y0) for y in years]
    flat = [e0 for _ in years]
    trend = [max(0, e0 + sen * (y - y0)) for y in years]
    fig, ax = plt.subplots(figsize=(10, 5.8))
    ax.plot(g.year, g.covered_t / 1e6, color=TOMATO, lw=2.4, marker="o",
            ms=4, label="covered emissions (reported)")
    ax.plot(years, np.array(base) / 1e6, color=INK, lw=2.2, ls="--",
            label="baseline declining 4.9%/yr (default path)")
    ax.plot(years, np.array(flat) / 1e6, color=MANGO, lw=2.2,
            label="scenario: emissions flat at 2024-25")
    ax.plot(years, np.array(trend) / 1e6, color=SEA, lw=2.2,
            label="scenario: recent Sen trend continues")
    ax.fill_between(years, np.array(base) / 1e6, np.array(flat) / 1e6,
                    where=np.array(flat) > np.array(base), color=TOMATO,
                    alpha=0.15, label="shortfall to buy units for")
    ax.set_title(f"{fac}: the closing gap to a declining baseline")
    ax.set_ylabel("Mt CO2-e")
    ax.set_xlabel("Compliance year (labelled by starting year); scenarios "
                  "are what-ifs, not forecasts")
    ax.legend(fontsize=9, loc="lower left")
    credit(ax)
    fig.savefig(os.path.join(charts, "04_crossover.png"))
    plt.close(fig)


def chart_costs(costs, charts):
    flat = costs[costs.scenario == "flat"].sort_values(
        "cost_at_spot_37.50_m", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    y = np.arange(len(flat))
    ax.barh(y - 0.22, flat["cost_at_low_30.00_m"], height=0.2, color=SEA,
            label="ACCUs at $30 (low)")
    ax.barh(y, flat["cost_at_spot_37.50_m"], height=0.2, color=MANGO,
            label="ACCUs at $37.50 (spot, Mar qtr 2026)")
    ax.barh(y + 0.22, flat["cost_at_ceiling_path_m"], height=0.2,
            color=TOMATO, label="cost-containment ceiling path")
    ax.set_yticks(y)
    ax.set_yticklabels(flat.facility, fontsize=9)
    ax.set_xlabel("Cumulative 2025-26 to 2029-30 unit cost, $ million "
                  "(illustrative: flat emissions, default baseline decline)")
    ax.set_title("What staying flat would cost WA's biggest facilities")
    ax.legend(loc="lower right", fontsize=9)
    credit(ax)
    fig.savefig(os.path.join(charts, "05_cost_sensitivity.png"))
    plt.close(fig)


def main(data_dir="data", charts="charts"):
    if not os.path.exists(os.path.join(data_dir, "concentration_summary.csv")):
        raise SystemExit("Run build_dataset.py and analysis.py first.")
    apply_style()
    os.makedirs(charts, exist_ok=True)
    conc = pd.read_csv(os.path.join(data_dir, "concentration_summary.csv"))
    sect = pd.read_csv(os.path.join(data_dir, "sector_annual.csv"))
    hr = pd.read_csv(os.path.join(data_dir, "headroom_summary.csv"))
    costs = pd.read_csv(os.path.join(data_dir, "cost_scenarios.csv"))
    focus = conc.head(6).facility.tolist()
    chart_concentration(conc, charts)
    chart_sectors(sect, charts)
    chart_headroom(hr, focus, charts)
    chart_crossover(hr, charts)
    chart_costs(costs, charts)
    print(f"Wrote 5 charts to {charts}/")


if __name__ == "__main__":
    main(*(sys.argv[1:3] or ["data"]))
