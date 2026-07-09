"""
analysis.py: trends in south-west WA fire weather. Pure numpy/pandas plus the
hand-rolled, unit-tested stats_utils.

Seasons run October to April and are labelled by the starting year (season
1990 is Oct 1990 to Apr 1991). Metrics per site-season:

  days_vh      days with FFDI >= 25 (Very High on the pre-2022 scale)
  days_sev     days with FFDI >= 50 (Severe)
  ffdi_p99     the season's 99th-percentile daily FFDI
  ffdi_sum     cumulative FFDI over the season (a severity integral)
  season_span  days between the season's first and last FFDI >= 25 day

Because ERA5 winds are grid-cell averages, absolute FFDI here runs lower than
station-based values; the trends, not the absolute counts, are the result.
Trends are run twice: on the full record and on 1975 onward, where the
reanalysis is better constrained (satellite era). Both are reported.

Outputs (data/): seasonal_metrics.csv, trend_summary.csv, epoch_summary.csv,
validation_summary.csv.  Usage:  python3 analysis.py [data_dir]
"""
import glob
import os
import sys

import numpy as np
import pandas as pd

import stats_utils as su

SITES = {
    "perth_airport": "Perth Airport",
    "manjimup": "Manjimup",
    "merredin": "Merredin",
    "margaret_river": "Margaret River",
}
VH, SEV = 25.0, 50.0
SEASON_MONTHS = (10, 11, 12, 1, 2, 3, 4)
EPOCH_A = (1945, 1974)
EPOCH_B = (1995, 2024)
METRICS = [
    ("days_vh", "days at Very High (FFDI >= 25)"),
    ("days_sev", "days at Severe (FFDI >= 50)"),
    ("ffdi_p99", "seasonal 99th-percentile FFDI"),
    ("ffdi_sum", "cumulative seasonal FFDI"),
    ("season_span", "days from first to last Very High day"),
]


def season_year(dates):
    """October-April season labelled by starting year."""
    y = dates.dt.year.values.copy()
    m = dates.dt.month.values
    y[m <= 4] -= 1
    return y


def seasonal_metrics(daily):
    d = daily[daily.date.dt.month.isin(SEASON_MONTHS)].copy()
    d["season"] = season_year(d.date)
    rows = []
    for season, g in d.groupby("season"):
        expected = 212 if ((season + 1) % 4 == 0) else 212  # Oct-Apr approx
        if len(g) < 200:            # incomplete season (record edges)
            continue
        vh_days = g[g.ffdi >= VH]
        span = 0
        if len(vh_days) >= 2:
            span = int((vh_days.date.max() - vh_days.date.min()).days)
        elif len(vh_days) == 1:
            span = 1
        rows.append({
            "season": int(season),
            "days_vh": int((g.ffdi >= VH).sum()),
            "days_sev": int((g.ffdi >= SEV).sum()),
            "ffdi_p99": float(np.percentile(g.ffdi, 99)),
            "ffdi_sum": float(g.ffdi.sum()),
            "season_span": span,
            "n_days": len(g),
        })
    return pd.DataFrame(rows)


def trend_row(site, metric, label, years, vals, window):
    years = np.asarray(years, float)
    vals = np.asarray(vals, float)
    m = np.isfinite(vals)
    years, vals = years[m], vals[m]
    mk = su.mann_kendall(vals)
    tf = su.mann_kendall_tfpw(vals)
    sen, _ = su.sens_slope(years, vals)
    ols = su.linregress(years, vals)
    return {
        "site": site, "metric": metric, "label": label, "window": window,
        "n": int(years.size),
        "sen_slope_per_decade": 10 * sen,
        "ols_slope_per_decade": 10 * ols.slope,
        "ols_p": ols.pvalue, "mk_tau": mk.tau, "mk_p": mk.pvalue,
        "mk_p_tfpw": tf.pvalue, "mk_trend": mk.trend,
    }


def validation(data_dir):
    """ERA5 vs GHCN observed at Perth Airport: TMAX agreement, rain days."""
    era = pd.read_csv(os.path.join(data_dir,
                                   "fire_weather_daily_perth_airport.csv"),
                      parse_dates=["date"])
    obs = pd.read_csv(os.path.join(data_dir, "ghcn_perth_airport_daily.csv"),
                      parse_dates=["date"])
    j = era.merge(obs, on="date", how="inner").dropna(subset=["tmax",
                                                              "tmax_obs"])
    r = su.linregress(j.tmax_obs.values, j.tmax.values)
    bias = float((j.tmax - j.tmax_obs).mean())
    rmse = float(np.sqrt(((j.tmax - j.tmax_obs) ** 2).mean()))
    rain = j.dropna(subset=["prcp_obs"])
    both = ((rain.rain24 >= 1.0) == (rain.prcp_obs >= 1.0)).mean()
    return pd.DataFrame([{
        "comparison": "ERA5 tmax vs GHCN tmax (Perth Airport)",
        "n_days": len(j), "pearson_r": r.rvalue, "bias_c": bias,
        "rmse_c": rmse, "rain_day_agreement": float(both),
        "first": str(j.date.min().date()), "last": str(j.date.max().date()),
    }])


def main(data_dir="data"):
    files = sorted(glob.glob(os.path.join(data_dir, "fire_weather_daily_*.csv")))
    if not files:
        raise SystemExit("No clean daily files. Run build_dataset.py first.")
    all_seasonal, trends, epochs = [], [], []
    for site, label in SITES.items():
        path = os.path.join(data_dir, f"fire_weather_daily_{site}.csv")
        daily = pd.read_csv(path, parse_dates=["date"])
        sm = seasonal_metrics(daily)
        sm.insert(0, "site", site)
        all_seasonal.append(sm)
        for metric, mlabel in METRICS:
            trends.append(trend_row(site, metric, mlabel,
                                    sm.season, sm[metric], "full"))
            late = sm[sm.season >= 1975]
            trends.append(trend_row(site, metric, mlabel,
                                    late.season, late[metric], "1975+"))
        a = sm[(sm.season >= EPOCH_A[0]) & (sm.season <= EPOCH_A[1])]
        b = sm[(sm.season >= EPOCH_B[0]) & (sm.season <= EPOCH_B[1])]
        for metric, mlabel in METRICS:
            epochs.append({
                "site": site, "metric": metric,
                "epoch_1945_1974": float(a[metric].mean()),
                "epoch_1995_2024": float(b[metric].mean()),
                "change": float(b[metric].mean() - a[metric].mean()),
                "pct_change": (100.0 * (b[metric].mean() - a[metric].mean())
                               / a[metric].mean()) if a[metric].mean() else np.nan,
            })

    seasonal = pd.concat(all_seasonal, ignore_index=True)
    seasonal.to_csv(os.path.join(data_dir, "seasonal_metrics.csv"), index=False)
    tr = pd.DataFrame(trends)
    tr.to_csv(os.path.join(data_dir, "trend_summary.csv"), index=False)
    ep = pd.DataFrame(epochs)
    ep.to_csv(os.path.join(data_dir, "epoch_summary.csv"), index=False)
    va = validation(data_dir)
    va.to_csv(os.path.join(data_dir, "validation_summary.csv"), index=False)

    print("=== Fire weather in SW WA: findings ===")
    v = va.iloc[0]
    print(f"Validation (Perth Airport): ERA5 vs GHCN TMAX r = {v.pearson_r:.3f}, "
          f"bias {v.bias_c:+.2f} C, rain-day agreement {100*v.rain_day_agreement:.0f}%")
    for site, label in SITES.items():
        g = tr[(tr.site == site) & (tr.metric == "days_vh")]
        full = g[g.window == "full"].iloc[0]
        late = g[g.window == "1975+"].iloc[0]
        e = ep[(ep.site == site) & (ep.metric == "days_vh")].iloc[0]
        print(f"{label}: Very High days {e.epoch_1945_1974:.1f} -> "
              f"{e.epoch_1995_2024:.1f} per season between epochs; "
              f"Sen {full.sen_slope_per_decade:+.2f}/decade full "
              f"(MK p={full.mk_p:.3g}), {late.sen_slope_per_decade:+.2f}/decade "
              f"1975+ (p={late.mk_p:.3g})")


if __name__ == "__main__":
    main(*(sys.argv[1:2] or ["data"]))
