"""
analysis.py: trends and headline events for WA-coast marine heatwaves.
Pure numpy/pandas + the hand-rolled, unit-tested stats_utils.

Outputs (data/):
  trend_summary.csv    Mann-Kendall + Sen + OLS on annual MHW days, annual
                       max intensity, and annual mean SST (complete years)
  top_events.csv       the ten biggest events by duration and by intensity

Usage:  python3 analysis.py [data_dir]
"""
import os
import sys
import numpy as np
import pandas as pd
import stats_utils as su


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
    apath = os.path.join(data_dir, "annual_mhw_metrics.csv")
    if not os.path.exists(apath):
        raise SystemExit("data/annual_mhw_metrics.csv not found. Run "
                         "build_dataset.py first (see dropzone/DROP_FILES_HERE.md).")
    annual = pd.read_csv(apath)
    events = pd.read_csv(os.path.join(data_dir, "mhw_events.csv"),
                         parse_dates=["start", "end", "peak_date"])
    ok = annual[annual.complete].sort_values("year")
    # first and last year are often partial downloads even when "complete"
    # by the missing-days rule; trend on interior years only if edges short
    rows = [
        trend_row("MHW days per year", ok.year, ok.mhw_days),
        trend_row("annual max intensity (C above climatology)",
                  ok.year, ok.max_intensity_c),
        trend_row("annual mean SST (C)", ok.year, ok.mean_sst_c),
    ]
    trends = pd.DataFrame(rows)
    trends.to_csv(os.path.join(data_dir, "trend_summary.csv"), index=False)

    top = pd.concat([
        events.nlargest(10, "duration_days").assign(rank_by="duration"),
        events.nlargest(10, "max_intensity_c").assign(rank_by="intensity"),
    ])
    top.to_csv(os.path.join(data_dir, "top_events.csv"), index=False)

    print("=== Marine heatwaves: findings ===")
    for _, r in trends.iterrows():
        star = " *" if r.mk_p < 0.05 else ""
        print(f"{r.series}: Sen {r.sen_slope_per_decade:+.2f}/decade, "
              f"MK p = {r.mk_p:.3g} (TFPW p = {r.mk_p_tfpw:.3g}){star}")
    if len(events):
        big = events.loc[events.duration_days.idxmax()]
        hot = events.loc[events.max_intensity_c.idxmax()]
        print(f"Longest event: {big.start.date()} to {big.end.date()} "
              f"({big.duration_days} days, {big.category})")
        print(f"Most intense event: peak {hot.peak_date.date()}, "
              f"{hot.max_intensity_c:.2f} C above climatology ({hot.category})")
        y2011 = events[(events.start.dt.year <= 2011) & (events.end.dt.year >= 2011)]
        if len(y2011):
            e = y2011.loc[y2011.max_intensity_c.idxmax()]
            print(f"2011 Ningaloo Nino check: detected {e.start.date()} to "
                  f"{e.end.date()}, peak {e.max_intensity_c:.2f} C, {e.category}")
        else:
            print("NOTE: no event spans 2011; if the box is Ningaloo this "
                  "is a red flag for the inputs.")


if __name__ == "__main__":
    main(*(sys.argv[1:2] or ["data"]))
