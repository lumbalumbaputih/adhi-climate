"""
analysis.py: WA facilities under the Safeguard Mechanism. Pure numpy/pandas
plus the hand-rolled, unit-tested stats_utils.

Everything here follows the credibility rules in EXECUTION_PROMPT.md:
scenarios are what-ifs with their assumption in the same row, exceeding a
baseline and surrendering units IS compliance (cost exposure, not
wrongdoing), and the 1 July 2023 reform seam means baselines form two
regimes while covered emissions are one continuous series.

Scenario parameters (verified 2026-07-07, sources in the README):
  decline rate   4.9% a year to 2029-30 (default; TEBA facilities differ)
  price band     ACCU generic spot about $37.50 (CER QCMR, March qtr 2026);
                 $30 as the low case; the legislated cost-containment ceiling
                 $82.68 in 2025-26, grown at an assumed CPI+2% = 4.5% a year

Outputs (data/): concentration_summary.csv, sector_trends.csv,
headroom_summary.csv, crossover_scenarios.csv, cost_scenarios.csv,
company_rollup.csv.  Usage:  python3 analysis.py [data_dir]
"""
import os
import sys

import numpy as np
import pandas as pd

import stats_utils as su

DECLINE = 0.049                 # default annual baseline decline to 2029-30
SPOT, SPOT_LOW = 37.5, 30.0     # $/t, CER QCMR March qtr 2026 (generic ACCU)
CEIL_2025, CEIL_GROWTH = 82.68, 0.045   # $/t in 2025-26; assumed CPI+2%
PROJ_YEARS = [2025, 2026, 2027, 2028, 2029]   # compliance years by start year
FOCUS_N = 6

PARENTS = [
    ("Chevron", ("chevron",)),
    ("Woodside", ("woodside",)),
    ("Shell", ("shell",)),
    ("Alcoa", ("alcoa",)),
    ("South32", ("south32",)),
    ("BHP", ("bhp", "nickel west")),
    ("Rio Tinto", ("rio tinto", "hamersley", "pilbara iron", "robe river",
                   "dampier salt")),
    ("Fortescue", ("fmg", "fortescue", "chichester", "pilbara ports")),
    ("CITIC", ("citic",)),
    ("Yara", ("yara",)),
]


def parent(emitter):
    low = str(emitter).lower()
    for name, keys in PARENTS:
        if any(k in low for k in keys):
            return name
    return "Other"


def trend_row(label, years, vals):
    years = np.asarray(years, float)
    vals = np.asarray(vals, float)
    m = np.isfinite(vals)
    years, vals = years[m], vals[m]
    mk = su.mann_kendall(vals)
    tf = su.mann_kendall_tfpw(vals)
    sen, _ = su.sens_slope(years, vals)
    ols = su.linregress(years, vals)
    return {
        "series": label, "n": int(years.size),
        "sen_slope_per_year": sen, "ols_slope_per_year": ols.slope,
        "ols_p": ols.pvalue, "mk_tau": mk.tau, "mk_p": mk.pvalue,
        "mk_p_tfpw": tf.pvalue, "mk_trend": mk.trend,
    }


def ceiling_price(year):
    return CEIL_2025 * (1 + CEIL_GROWTH) ** (year - 2025)


def main(data_dir="data"):
    path = os.path.join(data_dir, "safeguard_wa_clean.csv")
    if not os.path.exists(path):
        raise SystemExit("Run build_dataset.py first.")
    wa = pd.read_csv(path)
    wa["parent"] = wa.emitter.map(parent)
    latest_year = int(wa.year.max())
    latest = wa[wa.year == latest_year].copy()

    # 1. concentration ------------------------------------------------------
    conc = latest.sort_values("covered_t", ascending=False)[
        ["facility", "emitter", "parent", "sector", "covered_t",
         "baseline_t", "smcs_issued", "accus_surrendered",
         "smcs_surrendered"]].reset_index(drop=True)
    conc["share_pct"] = 100 * conc.covered_t / conc.covered_t.sum()
    conc["cum_share_pct"] = conc.share_pct.cumsum()
    conc.to_csv(os.path.join(data_dir, "concentration_summary.csv"),
                index=False)

    # 2. sector + total trends (covered emissions are one series) -----------
    sect = (wa.groupby(["year", "sector"], as_index=False).covered_t.sum())
    total = wa.groupby("year", as_index=False).covered_t.sum()
    rows = [trend_row("WA total covered emissions (t)", total.year,
                      total.covered_t)]
    for s, g in sect.groupby("sector"):
        if g.year.nunique() >= 8:
            rows.append(trend_row(f"sector: {s}", g.year, g.covered_t))
    pd.DataFrame(rows).to_csv(os.path.join(data_dir, "sector_trends.csv"),
                              index=False)
    sect.to_csv(os.path.join(data_dir, "sector_annual.csv"), index=False)

    # 3. headroom (per regime; reformed years are the decision-relevant ones)
    # MYMP-cumulative baselines are not annual quantities: exclude them from
    # headroom (they stay visible, flagged, in safeguard_wa_clean.csv)
    wa.loc[wa.baseline_mymp_cumulative, "baseline_t"] = np.nan
    wa["headroom_t"] = wa.baseline_t - wa.covered_t
    hr = wa[["year", "regime", "facility", "parent", "sector", "covered_t",
             "baseline_t", "headroom_t", "accus_surrendered",
             "smcs_surrendered", "smcs_issued"]].copy()
    hr["above_baseline"] = hr.headroom_t < 0
    hr.to_csv(os.path.join(data_dir, "headroom_summary.csv"), index=False)

    # 4. crossover scenarios for the focus facilities ------------------------
    focus = conc.head(FOCUS_N).facility.tolist()
    scen_rows = []
    for fac in focus:
        g = wa[wa.facility == fac].sort_values("year")
        e0 = float(g[g.year == latest_year].covered_t.iloc[0])
        b0 = float(g[g.year == latest_year].baseline_t.iloc[0])
        recent = g[g.year >= latest_year - 5]
        sen, _ = su.sens_slope(recent.year.values.astype(float),
                               recent.covered_t.values.astype(float))
        for scen, slope in (("flat at latest year", 0.0),
                            ("recent Sen trend continues", sen)):
            cross = None
            for y in PROJ_YEARS:
                b = b0 * (1 - DECLINE) ** (y - latest_year)
                e = max(0.0, e0 + slope * (y - latest_year))
                if e > b and cross is None:
                    cross = y
            scen_rows.append({
                "facility": fac, "scenario": scen,
                "assumption": (f"emissions {'flat at' if slope==0 else 'moving'} "
                               f"{slope:+.0f} t/yr from the {latest_year}-"
                               f"{str(latest_year+1)[2:]} level; baseline "
                               f"declines {DECLINE*100:.1f}%/yr from its "
                               f"{latest_year}-{str(latest_year+1)[2:]} value"),
                "latest_covered_t": e0, "latest_baseline_t": b0,
                "already_above": e0 > b0,
                "first_year_above_baseline": (f"{cross}-{str(cross+1)[2:]}"
                                              if cross else "not by 2029-30"),
            })
    scen = pd.DataFrame(scen_rows)
    scen.to_csv(os.path.join(data_dir, "crossover_scenarios.csv"), index=False)

    # 5. cost-exposure sensitivity (illustrative, labelled) ------------------
    cost_rows = []
    for fac in focus:
        g = wa[wa.facility == fac]
        e0 = float(g[g.year == latest_year].covered_t.iloc[0])
        b0 = float(g[g.year == latest_year].baseline_t.iloc[0])
        recent = g[g.year >= latest_year - 5].sort_values("year")
        sen, _ = su.sens_slope(recent.year.values.astype(float),
                               recent.covered_t.values.astype(float))
        for scen_name, slope in (("flat", 0.0), ("trend", sen)):
            shortfall = 0.0
            cost_spot = cost_low = cost_ceil = 0.0
            for y in PROJ_YEARS:
                b = b0 * (1 - DECLINE) ** (y - latest_year)
                e = max(0.0, e0 + slope * (y - latest_year))
                s = max(0.0, e - b)
                shortfall += s
                cost_spot += s * SPOT
                cost_low += s * SPOT_LOW
                cost_ceil += s * ceiling_price(y)
            cost_rows.append({
                "facility": fac, "scenario": scen_name,
                "cumulative_shortfall_t_2025_2029": shortfall,
                "cost_at_spot_37.50_m": cost_spot / 1e6,
                "cost_at_low_30.00_m": cost_low / 1e6,
                "cost_at_ceiling_path_m": cost_ceil / 1e6,
                "note": "illustrative; assumes full shortfall met with "
                        "purchased units at the stated price",
            })
    pd.DataFrame(cost_rows).to_csv(os.path.join(data_dir,
                                                "cost_scenarios.csv"),
                                   index=False)

    # 6. company roll-up ------------------------------------------------------
    roll = (latest.groupby("parent", as_index=False)
            .agg(facilities=("facility", "nunique"),
                 covered_t=("covered_t", "sum"),
                 baseline_t=("baseline_t", "sum"),
                 smcs_issued=("smcs_issued", "sum"),
                 units_surrendered=("accus_surrendered", "sum"))
            .sort_values("covered_t", ascending=False))
    roll["headroom_t"] = roll.baseline_t - roll.covered_t
    roll.to_csv(os.path.join(data_dir, "company_rollup.csv"), index=False)

    # findings ----------------------------------------------------------------
    yl = f"{latest_year}-{str(latest_year + 1)[2:]}"
    print(f"=== WA under the Safeguard Mechanism: findings ({yl}) ===")
    print(f"WA facilities: {latest.facility.nunique()}; covered emissions "
          f"{latest.covered_t.sum()/1e6:.1f} Mt CO2-e; top 10 hold "
          f"{conc.head(10).share_pct.sum():.0f}%")
    t = pd.DataFrame(rows)
    tot = t[t.series.str.startswith("WA total")].iloc[0]
    print(f"WA total covered emissions trend 2016-{latest_year}: Sen "
          f"{tot.sen_slope_per_year/1e6:+.2f} Mt/yr (MK p = {tot.mk_p:.3g})")
    above = latest[latest.baseline_t < latest.covered_t]
    print(f"Facilities above baseline in {yl}: {len(above)} of "
          f"{len(latest)} (they comply by surrendering units)")
    for _, r in scen[scen.scenario == "flat at latest year"].iterrows():
        tag = "already above" if r.already_above else r.first_year_above_baseline
        print(f"  {r.facility[:34]:34} flat-emissions crossover: {tag}")


if __name__ == "__main__":
    main(*(sys.argv[1:2] or ["data"]))
