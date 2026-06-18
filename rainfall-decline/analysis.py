"""
analysis.py — step-change, trend, and driver analysis of the SW WA cool-season
rainfall series. Pure numpy/pandas + the hand-rolled, unit-tested stats_utils.

Outputs (data/):
  stepchange_summary.csv   Pettitt change point + pre/post means
  trend_summary.csv        Mann-Kendall + Sen + OLS, full and post-change, plus
                           per-station and May-July rows
  driver_correlation.csv   IOD/SAM/ENSO vs rainfall, raw and detrended

Headline series = regional mean of per-station April-October % anomalies vs each
station's 1950-1974 baseline. The decline is observed; attribution is handled
separately (referenced summary + this illustrative, NOT causal, correlation).
"""
import numpy as np
import pandas as pd
import stats_utils as su

BASE_START, BASE_END = 1950, 1974
COOL_N, MJJ = 7, [5, 6, 7]


def detrend(years, vals):
    r = su.linregress(years, vals)
    return vals - (r.intercept + r.slope * years)


def trend_row(label, years, vals):
    years = np.asarray(years, float)
    vals = np.asarray(vals, float)
    m = np.isfinite(vals)
    years, vals = years[m], vals[m]
    mk = su.mann_kendall(vals)
    sen, _ = su.sens_slope(years, vals)
    ols = su.linregress(years, vals)
    return {
        "series": label, "n": int(years.size),
        "sen_slope_per_decade": 10 * sen,
        "ols_slope_per_decade": 10 * ols.slope,
        "ols_p": ols.pvalue, "mk_tau": mk.tau, "mk_p": mk.pvalue,
        "mk_trend": mk.trend,
    }


def regional_mjj(clean):
    """Build the regional May-July % anomaly series from the clean station table."""
    base = (clean[(clean.year >= BASE_START) & (clean.year <= BASE_END)]
            .groupby("station")["mjj_mm"].mean())
    df = clean.dropna(subset=["mjj_mm"]).copy()
    df["mjj_base"] = df.station.map(base)
    df["mjj_pct"] = 100 * (df.mjj_mm - df.mjj_base) / df.mjj_base
    g = df.groupby("year")
    out = (g["mjj_pct"].mean().to_frame("mjj_anom_pct")
           .assign(n=g["mjj_pct"].count()))
    return out[out.n >= 5].reset_index()


def main():
    reg = pd.read_csv("data/annual_cool_season_anomaly.csv")
    clean = pd.read_csv("data/rainfall_swwa_clean.csv")
    drivers = pd.read_csv("data/drivers.csv")

    years = reg.year.values.astype(float)
    pct = reg.regional_anom_pct.values
    mm = reg.regional_cool_mm.values

    # ---- Pettitt change point on the % anomaly series ----
    pt = su.pettitt(pct)
    cp = pt.cp_index
    cp_year = int(reg.year.iloc[cp])              # first year of the drier regime
    pre, post = reg.iloc[:cp], reg.iloc[cp:]
    pre_mm, post_mm = pre.regional_cool_mm.mean(), post.regional_cool_mm.mean()
    pct_change = 100 * (post_mm - pre_mm) / pre_mm

    # fixed-period comparisons
    def mean_mm(a, b):
        s = reg[(reg.year >= a) & (reg.year <= b)].regional_cool_mm
        return s.mean()
    base_mm = mean_mm(1950, 1974)
    recent_mm = mean_mm(2000, 2024)

    pd.DataFrame([{
        "pettitt_change_year": cp_year, "pettitt_K": pt.K, "pettitt_p": pt.pvalue,
        "pre_period": f"{int(reg.year.min())}-{cp_year-1}",
        "post_period": f"{cp_year}-{int(reg.year.max())}",
        "pre_mean_mm": pre_mm, "post_mean_mm": post_mm,
        "pre_to_post_pct_change": pct_change,
        "mean_1950_1974_mm": base_mm, "mean_2000_2024_mm": recent_mm,
        "pct_change_1950_74_vs_2000_24": 100 * (recent_mm - base_mm) / base_mm,
    }]).to_csv("data/stepchange_summary.csv", index=False)

    # ---- Trends ----
    rows = [
        trend_row("AprOct_pct_full_1950_2024", years, pct),
        trend_row("AprOct_mm_full_1950_2024", years, mm),
        trend_row(f"AprOct_pct_post_{cp_year}", years[years >= cp_year],
                  pct[years >= cp_year]),
    ]
    mjj = regional_mjj(clean)
    rows.append(trend_row("MayJul_pct_full_1950_2024",
                          mjj.year.values.astype(float), mjj.mjj_anom_pct.values))
    # per-station full-period mm trends (robustness)
    for st, g in clean.dropna(subset=["cool_mm"]).groupby("station"):
        rows.append(trend_row(f"station_{st}_mm", g.year.values.astype(float),
                              g.cool_mm.values))
    trend = pd.DataFrame(rows)
    trend.to_csv("data/trend_summary.csv", index=False)

    # ---- Driver correlation (raw + detrended) ----
    merged = reg.merge(drivers, on="year", how="left")
    drv = []
    for col, name in [("dmi_AprOct", "IOD (DMI)"),
                      ("sam_AprOct", "SAM (Marshall)"),
                      ("nino34_AprOct", "ENSO (Nino3.4)")]:
        sub = merged[["year", "regional_anom_pct", col]].dropna()
        yy = sub.year.values.astype(float)
        a, b = sub.regional_anom_pct.values, sub[col].values
        r_raw, p_raw, n = su.pearsonr(a, b)
        r_dt, p_dt, _ = su.pearsonr(detrend(yy, a), detrend(yy, b))
        drv.append({"driver": name, "n_years": n,
                    "period": f"{int(yy.min())}-{int(yy.max())}",
                    "pearson_r_raw": r_raw, "p_raw": p_raw,
                    "pearson_r_detrended": r_dt, "p_detrended": p_dt})
    drv = pd.DataFrame(drv)
    drv.to_csv("data/driver_correlation.csv", index=False)

    # ---- print findings ----
    pd.set_option("display.width", 130)
    print("\n================  STEP CHANGE (Pettitt on Apr-Oct % anomaly)  ================")
    print(f"  Change point ~ {cp_year} (K={pt.K:.0f}, p={pt.pvalue:.4g})")
    print(f"  {int(reg.year.min())}-{cp_year-1} mean = {pre_mm:.0f} mm   ->   "
          f"{cp_year}-{int(reg.year.max())} mean = {post_mm:.0f} mm   "
          f"({pct_change:+.1f}%)")
    print(f"  1950-1974 = {base_mm:.0f} mm  vs  2000-2024 = {recent_mm:.0f} mm "
          f"({100*(recent_mm-base_mm)/base_mm:+.1f}%)")
    print("\n================  TRENDS  ================")
    print(trend.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    print("\n================  DRIVER CORRELATION (illustrative, not causal)  ================")
    print(drv.to_string(index=False, float_format=lambda v: f"{v:.3f}"))


if __name__ == "__main__":
    main()
