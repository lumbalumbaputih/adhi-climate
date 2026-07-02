"""
analysis.py: step-change, trend, and rainfall-runoff amplification analysis of
SW WA gauged streamflow. Pure numpy/pandas + the hand-rolled, unit-tested
stats_utils.

Outputs (data/):
  stepchange_summary.csv   Pettitt change point + period means
  trend_summary.csv        Mann-Kendall + Sen + OLS on the regional series
  elasticity_summary.csv   rainfall-runoff elasticity and amplification

The rainfall side comes from the completed rainfall-decline project in this
repo (its regional April-October series, 1950-2024). The physical story being
tested: dry catchments soak up more of the rain before any of it runs off, so
a given % decline in rainfall produces a much larger % decline in streamflow.
Elasticity is reported two ways: log-log OLS slope and the Sankarasubramanian
(2001) non-parametric estimator. Every projection-free, observed-record number
in the README comes from this script.

Usage:  python3 analysis.py [data_dir]
"""
import os
import sys
import numpy as np
import pandas as pd
import stats_utils as su

BASE_START, BASE_END = 1975, 1999
RAIN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "..", "rainfall-decline", "data")


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


def elasticity_nonparametric(P, Q):
    """Sankarasubramanian et al. (2001): median of ((Q-Qbar)/(P-Pbar))*(Pbar/Qbar).

    Robust, model-free estimate of d(lnQ)/d(lnP). Years where P sits within
    1% of its mean are skipped (the ratio degenerates there).
    """
    P = np.asarray(P, float)
    Q = np.asarray(Q, float)
    Pbar, Qbar = P.mean(), Q.mean()
    dP = P - Pbar
    ok = np.abs(dP) > 0.01 * Pbar
    if ok.sum() < 5:
        return float("nan")
    return float(np.median((Q[ok] - Qbar) / dP[ok] * (Pbar / Qbar)))


def elasticity_loglog(P, Q):
    """OLS slope of ln(Q) on ln(P): the parametric elasticity estimate."""
    P = np.asarray(P, float)
    Q = np.asarray(Q, float)
    ok = (P > 0) & (Q > 0)
    return su.linregress(np.log(P[ok]), np.log(Q[ok]))


def rainfall_mm_adjusted():
    """Composition-adjusted regional cool-season rainfall in mm (the same
    construction rainfall-decline/viz.py uses: rescale the full-network
    baseline by the % anomaly series)."""
    reg = pd.read_csv(os.path.join(RAIN, "annual_cool_season_anomaly.csv"))
    clean = pd.read_csv(os.path.join(RAIN, "rainfall_swwa_clean.csv"))
    full_base = clean.groupby("station").baseline_mm.first().mean()
    reg["rain_mm_adj"] = full_base * (1.0 + reg.regional_anom_pct / 100.0)
    return reg[["year", "rain_mm_adj"]]


def period_mean(df, a, b, col):
    sel = df[(df.water_year >= a) & (df.water_year <= b)][col]
    return float(sel.mean()) if len(sel) else float("nan")


def main(data_dir="data"):
    path = os.path.join(data_dir, "annual_streamflow_anomaly.csv")
    if not os.path.exists(path):
        raise SystemExit(
            "data/annual_streamflow_anomaly.csv not found. Run build_dataset.py "
            "first (it needs the HRS files described in dropzone/DROP_FILES_HERE.md).")
    reg = pd.read_csv(path).sort_values("water_year").reset_index(drop=True)

    # --- step change -------------------------------------------------------
    pt = su.pettitt(reg.regional_anom_pct.values)
    cp_year = int(reg.water_year.iloc[pt.cp_index])
    base_ml = period_mean(reg, BASE_START, BASE_END, "regional_ML_adj")
    post00 = period_mean(reg, 2000, 2100, "regional_ML_adj")
    post10 = period_mean(reg, 2010, 2100, "regional_ML_adj")
    step = {
        "pettitt_change_year": cp_year, "pettitt_p": pt.pvalue,
        "baseline_1975_1999_ML": base_ml,
        "post2000_ML": post00, "post2010_ML": post10,
        "post2000_vs_baseline_pct": 100.0 * (post00 / base_ml - 1.0),
        "post2010_vs_baseline_pct": 100.0 * (post10 / base_ml - 1.0),
    }
    pd.DataFrame([step]).to_csv(os.path.join(data_dir, "stepchange_summary.csv"),
                                index=False)

    # --- trends -------------------------------------------------------------
    rows = [trend_row("regional % anomaly, full record",
                      reg.water_year, reg.regional_anom_pct)]
    post = reg[reg.water_year >= 2000]
    if len(post) >= 8:
        rows.append(trend_row("regional % anomaly, 2000-",
                              post.water_year, post.regional_anom_pct))
    trend = pd.DataFrame(rows)
    trend.to_csv(os.path.join(data_dir, "trend_summary.csv"), index=False)

    # --- rainfall-runoff amplification --------------------------------------
    rain = rainfall_mm_adjusted()
    j = reg.merge(rain, left_on="water_year", right_on="year", how="inner")
    ll = elasticity_loglog(j.rain_mm_adj, j.regional_ML_adj)
    enp = elasticity_nonparametric(j.rain_mm_adj, j.regional_ML_adj)
    rbase = rain[(rain.year >= BASE_START) & (rain.year <= BASE_END)].rain_mm_adj.mean()
    rpost = rain[rain.year >= 2000].rain_mm_adj.mean()
    rain_pct = 100.0 * (rpost / rbase - 1.0)
    elast = {
        "n_overlap_years": int(len(j)),
        "elasticity_loglog": ll.slope, "elasticity_loglog_p": ll.pvalue,
        "elasticity_loglog_r2": ll.r_squared,
        "elasticity_nonparametric": enp,
        "rain_post2000_vs_1975_1999_pct": rain_pct,
        "flow_post2000_vs_1975_1999_pct": step["post2000_vs_baseline_pct"],
        "amplification_ratio": (step["post2000_vs_baseline_pct"] / rain_pct
                                if rain_pct != 0 else float("nan")),
    }
    pd.DataFrame([elast]).to_csv(os.path.join(data_dir, "elasticity_summary.csv"),
                                 index=False)

    # --- console findings ----------------------------------------------------
    print("=== Perth water security: findings ===")
    print(f"Pettitt change point: water year {cp_year} (p = {pt.pvalue:.4g})")
    print(f"Mean flow 1975-1999: {base_ml:,.0f} ML | 2000-: {post00:,.0f} ML "
          f"({step['post2000_vs_baseline_pct']:+.1f}%) | 2010-: {post10:,.0f} ML "
          f"({step['post2010_vs_baseline_pct']:+.1f}%)")
    for r in rows:
        print(f"Trend [{r['series']}]: Sen {r['sen_slope_per_decade']:+.1f} %/decade, "
              f"MK p = {r['mk_p']:.4g} (TFPW p = {r['mk_p_tfpw']:.4g})")
    print(f"Elasticity: log-log {ll.slope:.2f} (p = {ll.pvalue:.3g}, "
          f"r2 = {ll.r_squared:.2f}); non-parametric {enp:.2f}")
    print(f"Amplification: rainfall {rain_pct:+.1f}% vs streamflow "
          f"{step['post2000_vs_baseline_pct']:+.1f}% (ratio "
          f"{elast['amplification_ratio']:.1f}x)")


if __name__ == "__main__":
    main(*(sys.argv[1:2] or ["data"]))
