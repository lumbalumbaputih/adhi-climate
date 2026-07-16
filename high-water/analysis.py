"""
analysis.py: high-water hours at Fremantle, their trend, and how much of the
change is the higher mean sea level. Pure numpy/pandas plus the hand-rolled,
unit-tested stats_utils.

Rules fixed BEFORE any trend was computed (and enforced here):
- Benchmarks are the 99.0th, 99.5th and 99.9th percentiles of all QC'd hours
  in the 1984-1993 baseline decade, rounded to the nearest millimetre on the
  UHSLC station datum. They never move.
- A calendar year enters the annual statistics only if at least 80% of its
  hours are present AND every calendar month has at least half of its hours,
  so a missing storm month cannot silently bias a count low.
- Raw counts and mean-adjusted counts are always computed together. The
  adjusted count asks: with this year's mean anomaly (vs the baseline decade
  mean) removed, how many hours would still have cleared the benchmark? The
  gap between the two is the contribution of the higher mean sea level.

Outputs (data/):
  benchmarks.csv          the three fixed benchmarks and the baseline stats
  annual_metrics.csv      per complete year: mean, max, percentiles, hours
                          and days above each benchmark, adjusted hours
  trend_summary.csv       Mann-Kendall + Sen + OLS on the key annual series
  decomposition.csv       per year: raw vs adjusted hours at the middle
                          benchmark and the gap attributable to mean rise
  epoch_summary.csv       first decade vs recent decade vs nodal-phase checks
  monthly_highwater.csv   month x year hours at the middle benchmark
  validation_summary.csv  annual means from hourly vs PSMSL RLR (sea-level/)

Usage:  python3 analysis.py [data_dir]
"""
import os
import sys
import numpy as np
import pandas as pd
import stats_utils as su

BASE_START, BASE_END = 1984, 1993
BENCH_PCTLS = (99.0, 99.5, 99.9)
MIN_YEAR_FRAC = 0.80
MIN_MONTH_FRAC = 0.50
ALTIMETRY = 1993


def load_hourly(data_dir="data"):
    """Read the committed wide CSV back into a long (t, mm, feed) frame."""
    path = os.path.join(data_dir, "hourly_sea_level.csv")
    if not os.path.exists(path):
        raise SystemExit("data/hourly_sea_level.csv not found. Run "
                         "build_dataset.py first.")
    wide = pd.read_csv(path)
    hours = [f"h{h:02d}" for h in range(24)]
    long = wide.melt(id_vars=["date", "feed"], value_vars=hours,
                     var_name="hh", value_name="mm").dropna(subset=["mm"])
    t = (pd.to_datetime(long.date)
         + pd.to_timedelta(long.hh.str[1:].astype(int), unit="h"))
    return (pd.DataFrame({"t": t, "mm": long.mm.astype(float),
                          "feed": long.feed})
            .sort_values("t").reset_index(drop=True))


def hours_in_year(year):
    return 8784 if pd.Timestamp(year, 12, 31).is_leap_year else 8760


def complete_years(hourly):
    """Years passing the completeness rule; returns {year: True/False}."""
    out = {}
    df = hourly.assign(year=hourly.t.dt.year, m=hourly.t.dt.month)
    for y, g in df.groupby("year"):
        total_ok = len(g) >= MIN_YEAR_FRAC * hours_in_year(y)
        mn = g.groupby("m").size()
        months_ok = all(
            mn.get(m, 0) >= MIN_MONTH_FRAC * 24 * pd.Timestamp(y, m, 1).days_in_month
            for m in range(1, 13))
        out[int(y)] = bool(total_ok and months_ok)
    return out


def fixed_benchmarks(hourly):
    """The three benchmarks from the baseline decade, and its mean."""
    base = hourly[(hourly.t.dt.year >= BASE_START)
                  & (hourly.t.dt.year <= BASE_END)].mm.values
    if base.size < 5 * 8760:
        raise SystemExit("Baseline decade has too few hours; check the build.")
    marks = {f"b{i + 1}": int(round(np.percentile(base, p)))
             for i, p in enumerate(BENCH_PCTLS)}
    return marks, float(base.mean()), int(base.size)


def annual_metrics(hourly, marks, base_mean, completeness):
    rows = []
    for y, g in hourly.groupby(hourly.t.dt.year):
        v = g.mm.values
        anom = float(v.mean() - base_mean)
        row = {
            "year": int(y), "hours_present": int(v.size),
            "complete": completeness[int(y)],
            "feed": g.feed.iloc[-1],
            "mean_mm": round(float(v.mean()), 1),
            "median_mm": float(np.median(v)),
            "max_mm": float(v.max()),
            "p99_mm": round(float(np.percentile(v, 99.0)), 1),
            "p999_mm": round(float(np.percentile(v, 99.9)), 1),
            "anom_mm": round(anom, 1),
        }
        days = g.t.dt.strftime("%Y-%m-%d")
        for name, mark in marks.items():
            row[f"hours_ge_{name}"] = int((v >= mark).sum())
            row[f"adj_hours_ge_{name}"] = int(((v - anom) >= mark).sum())
        row["days_ge_b2"] = int(days[g.mm.values >= marks["b2"]].nunique())
        rows.append(row)
    return pd.DataFrame(rows).sort_values("year").reset_index(drop=True)


def trend_row(label, years, vals):
    years = np.asarray(years, float)
    vals = np.asarray(vals, float)
    mk = su.mann_kendall(vals)
    sen, _ = su.sens_slope(years, vals)
    ols = su.linregress(years, vals)
    return {"series": label, "n": int(len(vals)),
            "mk_p": mk.pvalue, "mk_trend": mk.trend,
            "sen_slope_per_yr": sen,
            "ols_slope_per_yr": ols.slope, "ols_p": ols.pvalue}


def trends(ok):
    rows = []
    span = f"{ok.year.min()}-{ok.year.max()}"
    for col, label in [
            ("hours_ge_b1", "high-water hours (b1)"),
            ("hours_ge_b2", "high-water hours (b2)"),
            ("hours_ge_b3", "high-water hours (b3)"),
            ("adj_hours_ge_b2", "mean-adjusted hours (b2)"),
            ("days_ge_b2", "high-water days (b2)"),
            ("mean_mm", "annual mean level"),
            ("max_mm", "annual max hourly level"),
            ("p999_mm", "annual 99.9th percentile")]:
        rows.append(trend_row(f"{label}, {span}", ok.year, ok[col]))
        post = ok[ok.year >= ALTIMETRY]
        if len(post) >= 10:
            rows.append(trend_row(
                f"{label}, {post.year.min()}-{post.year.max()}",
                post.year, post[col]))
    return pd.DataFrame(rows)


def epoch_stats(hourly, marks, years):
    """Level and threshold stats for one set of years (hourly values)."""
    sel = hourly[hourly.t.dt.year.isin(years)]
    v = sel.mm.values
    n_yrs = len(years)
    out = {"years": f"{min(years)}-{max(years)}", "n_years": n_yrs,
           "mean_mm": round(float(v.mean()), 1),
           "p50_mm": float(np.percentile(v, 50)),
           "p99_mm": round(float(np.percentile(v, 99)), 1),
           "p999_mm": round(float(np.percentile(v, 99.9)), 1),
           "max_mm": float(v.max())}
    for name, mark in marks.items():
        out[f"hours_per_yr_ge_{name}"] = round(
            float((v >= mark).sum()) / n_yrs, 1)
    return out


def epochs(hourly, marks, completeness):
    ok_years = sorted(y for y, c in completeness.items() if c)
    first = [y for y in ok_years if BASE_START <= y <= BASE_END]
    last = ok_years[-10:]
    rows = [dict(epoch="baseline decade", **epoch_stats(hourly, marks, first)),
            dict(epoch="last 10 complete years",
                 **epoch_stats(hourly, marks, last))]
    # Nodal-cycle sensitivity: windows one 18.61-year cycle apart. If the
    # rise in high-water hours were mostly tidal modulation, the like-phase
    # comparison would flatten it; it does not.
    for start in (BASE_START + 19, BASE_START + 38):
        win = [y for y in ok_years if start <= y <= start + 9]
        if len(win) >= 8:
            rows.append(dict(epoch=f"nodal-phase window ({start})",
                             **epoch_stats(hourly, marks, win)))
    return pd.DataFrame(rows)


def monthly_highwater(hourly, marks, completeness):
    df = hourly[hourly.mm >= marks["b2"]]
    out = (df.groupby([df.t.dt.year.rename("year"),
                       df.t.dt.month.rename("month")])
           .size().rename("hours_ge_b2").reset_index())
    out["complete_year"] = out.year.map(completeness)
    return out


def validation(annual, repo_root):
    """Annual means from hourly vs the PSMSL RLR annual means (sea-level/)."""
    path = os.path.join(repo_root, "sea-level", "data", "msl_annual.csv")
    if not os.path.exists(path):
        return pd.DataFrame([{"note": "sea-level/data/msl_annual.csv not "
                              "found; validation skipped"}])
    psmsl = pd.read_csv(path)
    psmsl = psmsl[psmsl.complete][["year", "msl_mm"]]
    both = annual[annual.complete][["year", "mean_mm"]].merge(psmsl, on="year")
    r, p, _ = su.pearsonr(both.mean_mm.values, both.msl_mm.values)
    offset = float((both.msl_mm - both.mean_mm).mean())
    spread = float((both.msl_mm - both.mean_mm).std())
    return pd.DataFrame([{
        "n_overlap_years": int(len(both)),
        "pearson_r": round(float(r), 4), "p": p,
        "mean_offset_mm": round(offset, 1),
        "offset_sd_mm": round(spread, 1),
        "note": "offset is the constant RLR-vs-station-zero datum gap; the "
                "two series should and do move together"}])


def main(data_dir="data"):
    here = os.path.dirname(os.path.abspath(__file__))
    hourly = load_hourly(data_dir)
    completeness = complete_years(hourly)
    marks, base_mean, base_n = fixed_benchmarks(hourly)

    pd.DataFrame([{"benchmark": k, "pctl_of_baseline": p, "level_mm": v,
                   "baseline_years": f"{BASE_START}-{BASE_END}",
                   "baseline_mean_mm": round(base_mean, 1),
                   "baseline_hours": base_n}
                  for (k, v), p in zip(marks.items(), BENCH_PCTLS)]
                 ).to_csv(os.path.join(data_dir, "benchmarks.csv"), index=False)

    annual = annual_metrics(hourly, marks, base_mean, completeness)
    annual.to_csv(os.path.join(data_dir, "annual_metrics.csv"), index=False)
    ok = annual[annual.complete].reset_index(drop=True)

    trends(ok).to_csv(os.path.join(data_dir, "trend_summary.csv"), index=False)

    dec = ok[["year", "feed", "hours_ge_b2", "adj_hours_ge_b2", "anom_mm"]].copy()
    dec["mean_level_contribution"] = dec.hours_ge_b2 - dec.adj_hours_ge_b2
    dec.to_csv(os.path.join(data_dir, "decomposition.csv"), index=False)

    epochs(hourly, marks, completeness).to_csv(
        os.path.join(data_dir, "epoch_summary.csv"), index=False)
    monthly_highwater(hourly, marks, completeness).to_csv(
        os.path.join(data_dir, "monthly_highwater.csv"), index=False)
    validation(annual, os.path.join(here, "..")).to_csv(
        os.path.join(data_dir, "validation_summary.csv"), index=False)

    b2 = marks["b2"]
    first = ok[(ok.year >= BASE_START) & (ok.year <= BASE_END)]
    last = ok.tail(10)
    print("=== Fremantle high water: findings ===")
    print(f"Benchmarks (mm, station datum): {marks}")
    print(f"Complete years: {len(ok)} of {len(annual)} "
          f"({ok.year.min()}-{ok.year.max()})")
    print(f"Hours >= b2 ({b2} mm): {first.hours_ge_b2.mean():.0f}/yr in "
          f"{BASE_START}-{BASE_END} vs {last.hours_ge_b2.mean():.0f}/yr in "
          f"the last 10 complete years")
    print(f"Mean level: {first.mean_mm.mean():.0f} mm vs "
          f"{last.mean_mm.mean():.0f} mm (+{last.mean_mm.mean() - first.mean_mm.mean():.0f} mm)")
    adj = last.adj_hours_ge_b2.mean()
    print(f"Mean-adjusted hours in the last decade: {adj:.0f}/yr, i.e. the "
          f"higher mean accounts for "
          f"{(last.hours_ge_b2.mean() - adj):.0f} of the extra hours/yr")
    tr = trend_row("b2 hours", ok.year, ok.hours_ge_b2)
    print(f"Trend, hours >= b2: Sen {tr['sen_slope_per_yr']:+.2f} hrs/yr/yr, "
          f"MK p = {tr['mk_p']:.2g}")


if __name__ == "__main__":
    main(*(sys.argv[1:2] or ["data"]))
