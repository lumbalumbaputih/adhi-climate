"""
analysis.py: how much of WA's wheat yield rides on the winter rain. Pure
numpy/pandas + the hand-rolled, unit-tested stats_utils.

The one methodological point everything hinges on: WA wheat yields have
risen for a century because of breeding and agronomy, while cool-season
rainfall has fallen. Correlating the raw series therefore UNDERSTATES (or
even sign-flips) the climate relationship. The honest comparison is between
the technology-detrended yield anomaly and the rainfall anomaly.

Outputs (data/):
  sensitivity_summary.csv   detrended yield vs rainfall: r, p, slope
                            (% yield per 10% rainfall), raw-series r for
                            contrast, drought-year impact
  yield_trend.csv           the technology trend itself

Usage:  python3 analysis.py [data_dir]
"""
import os
import sys
import numpy as np
import pandas as pd
import stats_utils as su

RAIN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "..", "rainfall-decline", "data")


def detrend_pct(years, vals):
    """OLS-detrend; return residuals as % of the trend value that year."""
    years = np.asarray(years, float)
    vals = np.asarray(vals, float)
    r = su.linregress(years, vals)
    fitted = r.intercept + r.slope * years
    return 100.0 * (vals - fitted) / fitted, r


def main(data_dir="data"):
    wpath = os.path.join(data_dir, "wheat_wa_clean.csv")
    if not os.path.exists(wpath):
        raise SystemExit("data/wheat_wa_clean.csv not found. Run "
                         "build_dataset.py first (see dropzone/DROP_FILES_HERE.md).")
    wheat = pd.read_csv(wpath)
    rain = pd.read_csv(os.path.join(RAIN, "annual_cool_season_anomaly.csv"))
    j = wheat.merge(rain[["year", "regional_anom_pct"]], on="year", how="inner")
    if len(j) < 20:
        raise SystemExit(f"Only {len(j)} overlapping seasons with the rainfall "
                         "series; need at least 20.")

    yld_anom, tr = detrend_pct(j.year.values, j.yield_t_ha.values)
    j = j.assign(yield_anom_pct=yld_anom)

    # rainfall is also trending (down); detrend it too for the pure
    # covariation number, and keep the raw-anomaly version alongside
    rain_dt, _ = detrend_pct(j.year.values,
                             (100.0 + j.regional_anom_pct.values))
    r_raw, p_raw, n = su.pearsonr(j.regional_anom_pct, j.yield_t_ha)
    r_dt, p_dt, _ = su.pearsonr(j.regional_anom_pct, j.yield_anom_pct)
    r_dd, p_dd, _ = su.pearsonr(rain_dt, j.yield_anom_pct)
    sens = su.linregress(j.regional_anom_pct, j.yield_anom_pct)

    dry_cut = j.regional_anom_pct.quantile(0.1)
    dry = j[j.regional_anom_pct <= dry_cut]
    wet = j[j.regional_anom_pct > dry_cut]

    out = {
        "n_seasons": int(len(j)),
        "overlap": f"{j.year.min()}-{j.year.max()}",
        "tech_trend_t_ha_per_decade": 10 * tr.slope,
        "tech_trend_p": tr.pvalue,
        "r_raw_yield_vs_rain": r_raw, "p_raw": p_raw,
        "r_detrended_yield_vs_rain": r_dt, "p_detrended": p_dt,
        "r_both_detrended": r_dd, "p_both_detrended": p_dd,
        "yield_pct_per_10pct_rain": 10 * sens.slope,
        "sens_p": sens.pvalue, "sens_r2": sens.r_squared,
        "driest_decile_cut_pct": float(dry_cut),
        "driest_decile_mean_yield_anom_pct": float(dry.yield_anom_pct.mean()),
        "other_years_mean_yield_anom_pct": float(wet.yield_anom_pct.mean()),
    }
    pd.DataFrame([out]).to_csv(os.path.join(data_dir, "sensitivity_summary.csv"),
                               index=False)
    pd.DataFrame([{
        "slope_t_ha_per_yr": tr.slope, "intercept": tr.intercept,
        "p": tr.pvalue, "r2": tr.r_squared, "n": tr.n,
    }]).to_csv(os.path.join(data_dir, "yield_trend.csv"), index=False)
    j.to_csv(os.path.join(data_dir, "joined_series.csv"), index=False)

    print("=== Wheat yields vs the drying trend: findings ===")
    print(f"Overlap: {out['overlap']} ({out['n_seasons']} seasons)")
    print(f"Technology trend: {out['tech_trend_t_ha_per_decade']:+.3f} t/ha "
          f"per decade (p = {tr.pvalue:.3g})")
    print(f"Raw correlation (misleading, kept for contrast): r = {r_raw:+.2f} "
          f"(p = {p_raw:.3g})")
    print(f"Detrended yield vs rainfall anomaly: r = {r_dt:+.2f} (p = {p_dt:.3g})")
    print(f"Both detrended: r = {r_dd:+.2f} (p = {p_dd:.3g})")
    print(f"Sensitivity: {out['yield_pct_per_10pct_rain']:+.1f}% yield per "
          f"10% rainfall (p = {sens.pvalue:.3g}, r2 = {sens.r_squared:.2f})")
    print(f"Driest-decile seasons (rain anomaly <= {dry_cut:.1f}%): mean yield "
          f"anomaly {out['driest_decile_mean_yield_anom_pct']:+.1f}% vs "
          f"{out['other_years_mean_yield_anom_pct']:+.1f}% in other seasons")


if __name__ == "__main__":
    main(*(sys.argv[1:2] or ["data"]))
