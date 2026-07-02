"""
analysis.py: trend and acceleration in Fremantle mean sea level. Pure
numpy/pandas + the hand-rolled, unit-tested stats_utils, plus a small
quadratic-regression helper (with standard errors from the design matrix)
defined and unit-tested here because stats_utils only carries simple OLS.

Outputs (data/):
  trend_summary.csv     linear rates (mm/yr): full record, pre-1993, 1993-
                        (the satellite-altimetry era), and 30-year windows
  acceleration.csv      quadratic-fit acceleration (mm/yr^2) and its p-value

Usage:  python3 analysis.py [data_dir]
"""
import os
import sys
import math
import numpy as np
import pandas as pd
import stats_utils as su

ALTIMETRY = 1993


def quadratic_fit(x, y):
    """OLS quadratic y = b0 + b1*x + b2*x^2 with classical standard errors.

    Returns dict with b1, b2, se2, t2, p2 where acceleration = 2*b2.
    x is centred internally so the polynomial terms stay well-conditioned.
    """
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    n = x.size
    if n < 10:
        raise ValueError("Need at least 10 points for a quadratic fit")
    xc = x - x.mean()
    X = np.column_stack([np.ones(n), xc, xc * xc])
    XtX = X.T @ X
    beta = np.linalg.solve(XtX, X.T @ y)
    resid = y - X @ beta
    dof = n - 3
    s2 = float(resid @ resid) / dof
    cov = s2 * np.linalg.inv(XtX)
    se2 = math.sqrt(cov[2, 2])
    t2 = beta[2] / se2 if se2 > 0 else float("nan")
    p2 = su.t_pvalue_two_sided(t2, dof)
    return {"b1": float(beta[1]), "b2": float(beta[2]),
            "se2": se2, "t2": float(t2), "p2": float(p2), "n": int(n)}


def rate_row(label, years, vals):
    ols = su.linregress(years, vals)
    sen, _ = su.sens_slope(np.asarray(years, float), np.asarray(vals, float))
    return {"series": label, "n": ols.n,
            "ols_rate_mm_per_yr": ols.slope, "ols_p": ols.pvalue,
            "ols_stderr": ols.stderr, "sen_rate_mm_per_yr": sen}


def rolling_rates(annual, window=30):
    """OLS rate in every complete 30-year window (needs 27+ complete years)."""
    ok = annual[annual.complete]
    rows = []
    for start in range(int(ok.year.min()), int(ok.year.max()) - window + 2):
        w = ok[(ok.year >= start) & (ok.year < start + window)]
        if len(w) >= window - 3:
            r = su.linregress(w.year.values.astype(float), w.anom_mm.values)
            rows.append({"window_start": start, "window_end": start + window - 1,
                         "rate_mm_per_yr": r.slope, "p": r.pvalue})
    return pd.DataFrame(rows)


def main(data_dir="data"):
    path = os.path.join(data_dir, "msl_annual.csv")
    if not os.path.exists(path):
        raise SystemExit("data/msl_annual.csv not found. Run build_dataset.py "
                         "first (see dropzone/DROP_FILES_HERE.md).")
    annual = pd.read_csv(path)
    ok = annual[annual.complete].sort_values("year")

    rows = [rate_row(f"full record ({ok.year.min()}-{ok.year.max()})",
                     ok.year.values.astype(float), ok.anom_mm.values)]
    pre = ok[ok.year < ALTIMETRY]
    post = ok[ok.year >= ALTIMETRY]
    if len(pre) >= 10:
        rows.append(rate_row(f"pre-{ALTIMETRY}", pre.year.values.astype(float),
                             pre.anom_mm.values))
    if len(post) >= 10:
        rows.append(rate_row(f"{ALTIMETRY}- (altimetry era)",
                             post.year.values.astype(float), post.anom_mm.values))
    trends = pd.DataFrame(rows)
    trends.to_csv(os.path.join(data_dir, "trend_summary.csv"), index=False)

    q = quadratic_fit(ok.year.values, ok.anom_mm.values)
    accel = {"acceleration_mm_per_yr2": 2 * q["b2"], "p": q["p2"],
             "n": q["n"], "note": "2*b2 from centred quadratic OLS"}
    pd.DataFrame([accel]).to_csv(os.path.join(data_dir, "acceleration.csv"),
                                 index=False)

    roll = rolling_rates(annual)
    roll.to_csv(os.path.join(data_dir, "rolling_rates.csv"), index=False)

    print("=== Fremantle sea level: findings ===")
    for _, r in trends.iterrows():
        print(f"{r.series}: OLS {r.ols_rate_mm_per_yr:+.2f} mm/yr "
              f"(p = {r.ols_p:.3g}), Sen {r.sen_rate_mm_per_yr:+.2f} mm/yr")
    print(f"Acceleration: {accel['acceleration_mm_per_yr2']:+.4f} mm/yr^2 "
          f"(p = {accel['p']:.3g}, n = {accel['n']})")
    if len(roll):
        hi = roll.loc[roll.rate_mm_per_yr.idxmax()]
        print(f"Fastest 30-year window: {int(hi.window_start)}-"
              f"{int(hi.window_end)} at {hi.rate_mm_per_yr:+.2f} mm/yr")


if __name__ == "__main__":
    main(*(sys.argv[1:2] or ["data"]))
