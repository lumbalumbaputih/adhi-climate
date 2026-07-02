"""
analysis.py: trends in Perth and Pilbara heat extremes. Pure numpy/pandas +
the hand-rolled, unit-tested stats_utils.

Outputs (data/):
  trend_summary.csv    Mann-Kendall (plain and prewhitened) + Sen + OLS per
                       station per metric, complete years only
  decade_summary.csv   decadal means of each metric per station

Count metrics (hot days, heatwave events) are lower-bounded at zero and
skewed, so the headline test is the non-parametric Mann-Kendall / Sen pair;
OLS is reported alongside for scale. Usage:  python3 analysis.py [data_dir]
"""
import os
import sys
import numpy as np
import pandas as pd
import stats_utils as su

METRICS = [
    ("days_ge_35", "days at or above 35 C"),
    ("days_ge_40", "days at or above 40 C"),
    ("txx_c", "hottest day of the year (TXx, C)"),
    ("hw_events", "heatwave events (3+ days above day-of-year p90)"),
    ("hw_days", "days inside heatwaves"),
]


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


def main(data_dir="data"):
    path = os.path.join(data_dir, "annual_heat_metrics.csv")
    if not os.path.exists(path):
        raise SystemExit("data/annual_heat_metrics.csv not found. Run "
                         "build_dataset.py first (see dropzone/DROP_FILES_HERE.md).")
    m = pd.read_csv(path)
    m = m[m.complete].copy()
    if m.empty:
        raise SystemExit("No complete station-years; check the inputs.")

    rows = []
    for st, g in m.groupby("station"):
        g = g.sort_values("year")
        if len(g) < 10:
            print(f"  {st}: only {len(g)} complete years; skipped (need 10)")
            continue
        for col, desc in METRICS:
            rows.append(trend_row(f"{g.name.iloc[0]}: {desc}", g.year, g[col]))
    if not rows:
        raise SystemExit("No station had 10 or more complete years.")
    trends = pd.DataFrame(rows)
    trends.to_csv(os.path.join(data_dir, "trend_summary.csv"), index=False)

    m["decade"] = (m.year // 10) * 10
    dec = (m.groupby(["station", "name", "decade"])
            [["days_ge_35", "days_ge_40", "txx_c", "hw_events", "hw_days"]]
            .mean().round(2).reset_index())
    dec.to_csv(os.path.join(data_dir, "decade_summary.csv"), index=False)

    print("=== Extreme heat: findings ===")
    for _, r in trends.iterrows():
        star = " *" if r.mk_p < 0.05 else ""
        print(f"{r.series}: Sen {r.sen_slope_per_decade:+.2f}/decade, "
              f"MK p = {r.mk_p:.3g} (TFPW p = {r.mk_p_tfpw:.3g}){star}")


if __name__ == "__main__":
    main(*(sys.argv[1:2] or ["data"]))
