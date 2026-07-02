"""
analysis.py: fuel-mix and emissions-intensity trends for the SWIS (WA's main
grid). Pure numpy/pandas + the hand-rolled, unit-tested stats_utils.

Outputs (data/):
  mix_trends.csv          Mann-Kendall + Sen + OLS on each fuel's annual share
  intensity_summary.csv   emissions-intensity series and trend (only when the
                          user has filled data/emission_factors.csv from the
                          NGA factors workbook; never computed from guesses)

Incomplete calendar years at either end of the record are excluded from trend
fitting (a year of SCADA that starts in July would otherwise read as a fuel
mix shift). Usage:  python3 analysis.py [data_dir]
"""
import os
import sys
import numpy as np
import pandas as pd
import stats_utils as su
from build_dataset import load_factors


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
        "sen_slope_per_decade": 10 * sen,
        "ols_slope_per_decade": 10 * ols.slope,
        "ols_p": ols.pvalue, "mk_tau": mk.tau, "mk_p": mk.pvalue,
        "mk_p_tfpw": tf.pvalue, "mk_r1": tf.r1, "mk_trend": mk.trend,
    }


def complete_years(monthly):
    """Calendar years with all 12 months of data present."""
    m = monthly.copy()
    m["year"] = m.month.str.slice(0, 4).astype(int)
    n_months = m.groupby("year").month.nunique()
    return sorted(n_months[n_months == 12].index)


def main(data_dir="data"):
    annual_path = os.path.join(data_dir, "annual_fuel_mix.csv")
    if not os.path.exists(annual_path):
        raise SystemExit("data/annual_fuel_mix.csv not found. Run build_dataset.py "
                         "first (see dropzone/DROP_FILES_HERE.md for the files).")
    annual = pd.read_csv(annual_path)
    monthly = pd.read_csv(os.path.join(data_dir, "generation_by_fuel_month.csv"))
    keep = complete_years(monthly)
    dropped = sorted(set(annual.year) - set(keep))
    if dropped:
        print(f"Excluding incomplete calendar years from trends: {dropped}")
    annual = annual[annual.year.isin(keep)]
    if annual.year.nunique() < 8:
        raise SystemExit("Fewer than 8 complete years; trend analysis would be "
                         "underpowered. Add more monthly files and re-run.")

    # --- fuel-share trends ----------------------------------------------------
    rows = []
    wide = annual.pivot_table(index="year", columns="fuel", values="share_pct",
                              aggfunc="sum").fillna(0.0)
    for fuel in wide.columns:
        rows.append(trend_row(f"{fuel} share (%)", wide.index, wide[fuel].values))
    renew = wide.reindex(columns=["wind", "solar", "bio"], fill_value=0.0).sum(axis=1)
    rows.append(trend_row("renewables share (%)", wide.index, renew.values))
    trends = pd.DataFrame(rows)
    trends.to_csv(os.path.join(data_dir, "mix_trends.csv"), index=False)

    # --- emissions intensity (only with user-supplied factors) -----------------
    factors = load_factors(data_dir)
    intensity = None
    if factors:
        missing = [f for f in wide.columns
                   if f not in factors and f != "storage"]
        if missing:
            print(f"emission_factors.csv lacks factors for: {missing}; "
                  "intensity NOT computed. Fill the template and re-run.")
        else:
            e = annual.assign(t=annual.fuel.map(factors) * annual.energy_MWh)
            by_year = e.groupby("year").agg(t=("t", "sum"),
                                            MWh=("energy_MWh", "sum"))
            by_year["intensity_t_per_MWh"] = by_year.t / by_year.MWh
            intensity = by_year.reset_index()[["year", "intensity_t_per_MWh"]]
            irow = trend_row("emissions intensity (t/MWh)",
                             intensity.year, intensity.intensity_t_per_MWh)
            intensity.to_csv(os.path.join(data_dir, "intensity_summary.csv"),
                             index=False)
            trends = pd.concat([trends, pd.DataFrame([irow])], ignore_index=True)
            trends.to_csv(os.path.join(data_dir, "mix_trends.csv"), index=False)
    else:
        print("No filled emission_factors.csv: intensity not computed (this is "
              "the no-fabrication rule, not an error).")

    # --- console findings --------------------------------------------------------
    print("=== SWIS decarbonisation: findings ===")
    y0, y1 = int(wide.index.min()), int(wide.index.max())
    print(f"Complete years analysed: {y0}-{y1}")
    for fuel in list(wide.columns) + ["renewables"]:
        series = renew if fuel == "renewables" else wide[fuel]
        r = trends[trends.series.str.startswith(fuel)].iloc[0]
        print(f"{fuel:>11}: {series.iloc[0]:5.1f}% -> {series.iloc[-1]:5.1f}%  "
              f"(Sen {r.sen_slope_per_decade:+.1f} pp/decade, MK p = {r.mk_p:.3g})")
    if intensity is not None:
        print(f"Intensity: {intensity.intensity_t_per_MWh.iloc[0]:.3f} -> "
              f"{intensity.intensity_t_per_MWh.iloc[-1]:.3f} t CO2-e/MWh")


if __name__ == "__main__":
    main(*(sys.argv[1:2] or ["data"]))
