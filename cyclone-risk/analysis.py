"""
analysis.py: the four analysis steps as importable functions used by
cyclone_analysis.ipynb. Each makes its chart(s) and returns the numbers.

Runs from raw data (data/raw/) when present, otherwise from the committed
cleaned CSVs, so the pipeline reproduces on a fresh clone. Run as a script to
regenerate every chart and print every headline figure:

    python analysis.py
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import stats_utils as su
import viz
import build_dataset as bd

viz.apply_style()
DECADES = ["1985-94", "1995-04", "2005-14", "2015-24"]
SEASONS = np.arange(1985, 2025)
RAW_IB = Path("data/raw/ibtracs.SI.list.v04r01.csv")
RAW_SST = Path("data/raw/sst.mnmean.nc")


# --------------------------------------------------------------------------
def load_storms():
    """Per-storm table: rebuild from raw if available, else load committed CSV."""
    if RAW_IB.exists():
        storms, _, _ = bd.build()
    else:
        storms = pd.read_csv("data/ibtracs_clean.csv")
    storms["decade"] = pd.Categorical(storms["decade"], categories=DECADES, ordered=True)
    return storms


def _annual(df, col, how="mean"):
    g = df.dropna(subset=[col]).groupby("season")[col]
    s = g.mean() if how == "mean" else (g.min() if how == "min" else g.max())
    return s.reindex(SEASONS)


# ----- Step 2: exploratory -------------------------------------------------
def explore(storms):
    wa = storms[storms.wa_affecting].copy()
    all_count = storms.groupby("season").size().reindex(SEASONS, fill_value=0)
    wa_count = wa.groupby("season").size().reindex(SEASONS, fill_value=0)

    def cat3(g):
        s = g.peak_usa_sshs.dropna()
        return 100.0 * (s >= 3).mean() if len(s) else np.nan

    summary = pd.DataFrame([{
        "decade": d, "n_WA": int((wa.decade == d).sum()),
        "mean_BOM_wind_kt": wa.loc[wa.decade == d, "peak_bom_wind_kt"].mean(),
        "median_BOM_wind_kt": wa.loc[wa.decade == d, "peak_bom_wind_kt"].median(),
        "mean_min_pres_hPa": wa.loc[wa.decade == d, "min_wmo_pres_hpa"].mean(),
        "pct_Cat3plus": cat3(wa[wa.decade == d]),
    } for d in DECADES])
    summary.to_csv("data/decadal_summary.csv", index=False)

    # chart 01
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(SEASONS, all_count.values, color=viz.INDIGO, alpha=0.30,
           label="All South Indian Ocean storms")
    ax.plot(SEASONS, wa_count.values, color=viz.TOMATO, lw=2.2, marker="o", ms=4,
            label="WA-affecting (within 500 km of WA coast)")
    for i in range(4):
        yrs = SEASONS[(SEASONS >= 1985 + i*10) & (SEASONS <= 1994 + i*10)]
        m = wa_count.loc[yrs[0]:yrs[-1]].mean()
        ax.plot([yrs[0]-0.5, yrs[-1]+0.5], [m, m], color=viz.INK, lw=1.4, ls="--", alpha=0.7, zorder=5)
    ax.set_xlabel("Cyclone season (year season ends)"); ax.set_ylabel("Number of storms")
    ax.set_title("Annual tropical cyclone counts, South Indian Ocean (1985–2024)")
    ax.set_xlim(1984, 2025); ax.legend(loc="upper right")
    ax.annotate("dashed = decadal mean of WA-affecting count", xy=(0.012, 0.96),
                xycoords="axes fraction", va="top", fontsize=8.5, color=viz.MUTED)
    viz.credit(ax); fig.savefig("charts/01_annual_count.png"); plt.close(fig)

    # chart 02
    fig, ax = plt.subplots(figsize=(9, 5))
    data = [wa.loc[wa.decade == d, "peak_bom_wind_kt"].dropna().values for d in DECADES]
    bp = ax.boxplot(data, tick_labels=DECADES, patch_artist=True, widths=0.6,
                    medianprops=dict(color=viz.INK, lw=2),
                    whiskerprops=dict(color=viz.MUTED), capprops=dict(color=viz.MUTED),
                    flierprops=dict(marker="o", ms=4, mfc=viz.MUTED, mec="none", alpha=0.5))
    for patch, d in zip(bp["boxes"], DECADES):
        patch.set_facecolor(viz.DECADE_COLORS[d]); patch.set_alpha(0.55); patch.set_edgecolor(viz.INK)
    means = [np.nanmean(x) for x in data]
    ax.plot(range(1, 5), means, color=viz.INK, marker="D", ms=7, lw=0, zorder=6, label="decade mean")
    for i, m in enumerate(means):
        ax.annotate(f"{m:.0f} kt", (i+1, m), xytext=(10, 0), textcoords="offset points",
                    va="center", fontsize=9, color=viz.INK, fontweight="bold")
    for i, d in enumerate(DECADES):
        ax.annotate(f"Cat 3+: {summary.pct_Cat3plus.iloc[i]:.0f}%", (i+1, 8),
                    ha="center", fontsize=8.5, color=viz.MUTED)
    ax.set_ylabel("Peak intensity, BOM 10-min sustained wind (knots)")
    ax.set_xlabel("Decade")
    ax.set_title("WA-affecting cyclone peak intensity by decade (1985–2024)")
    ax.legend(loc="upper right"); ax.set_ylim(0, ax.get_ylim()[1])
    viz.credit(ax); fig.savefig("charts/02_intensity_by_decade.png"); plt.close(fig)
    return summary, all_count, wa_count


# ----- Step 3: trends ------------------------------------------------------
def _trend_chart(x, y, lr, mk, sen, title, ylabel, fname, invert=False, color=viz.TOMATO):
    m = np.isfinite(x) & np.isfinite(y)
    xx, yy = np.asarray(x)[m], np.asarray(y)[m]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(xx, yy, color=color, lw=1.4, marker="o", ms=4, alpha=0.85, label="annual mean")
    xs = np.linspace(xx.min(), xx.max(), 100)
    yhat = lr.intercept + lr.slope*xs
    n = lr.n; xbar = xx.mean(); ssxx = np.sum((xx-xbar)**2)
    resid = yy - (lr.intercept + lr.slope*xx)
    s = np.sqrt(np.sum(resid**2)/(n-2)); tcrit = su.t_critical(n-2, 0.05)
    se = s*np.sqrt(1.0/n + (xs-xbar)**2/ssxx)
    ax.plot(xs, yhat, color=viz.INK, lw=2.2, label="OLS trend")
    ax.fill_between(xs, yhat-tcrit*se, yhat+tcrit*se, color=viz.INK, alpha=0.12, label="95% CI")
    if invert:
        ax.invert_yaxis()
    sig = "significant" if mk.pvalue < 0.05 else "not significant"
    txt = (f"OLS slope: {lr.slope:+.2f}/yr  ({lr.slope*10:+.1f}/decade)\n"
           f"Sen slope: {sen:+.2f}/yr\nMann-Kendall p = {mk.pvalue:.3f}  ({sig})\n"
           f"r² = {lr.r_squared:.2f}   n = {n} seasons")
    ax.annotate(txt, xy=(0.02, 0.03), xycoords="axes fraction", va="bottom", ha="left",
                fontsize=9.5, family="monospace",
                bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=viz.MUTED, alpha=0.9))
    ax.set_xlabel("Cyclone season (year season ends)"); ax.set_ylabel(ylabel); ax.set_title(title)
    ax.legend(loc="upper right", ncol=3, fontsize=9)
    viz.credit(ax); fig.savefig(fname); plt.close(fig)


def trends(storms):
    wa = storms[storms.wa_affecting]
    out = {}
    series = {
        "WA wind": (_annual(wa, "peak_bom_wind_kt"), "kt"),
        "WA pressure": (_annual(wa, "min_wmo_pres_hpa"), "hPa"),
        "Basin wind": (_annual(storms, "peak_bom_wind_kt"), "kt"),
        "Basin pressure": (_annual(storms, "min_wmo_pres_hpa"), "hPa"),
    }
    for name, (s, unit) in series.items():
        yv = s.values; mask = np.isfinite(yv)
        lr = su.linregress(SEASONS[mask], yv[mask])
        mk = su.mann_kendall(yv[mask]); sen, _ = su.sens_slope(SEASONS[mask], yv[mask])
        out[name] = dict(slope=lr.slope, slope_decade=lr.slope*10, ols_p=lr.pvalue,
                         mk_p=mk.pvalue, r2=lr.r_squared, sen=sen, trend=mk.trend)
    w = series["WA wind"][0]; p = series["WA pressure"][0]
    lr_w = su.linregress(SEASONS, w.values); mk_w = su.mann_kendall(w.dropna().values); sen_w, _ = su.sens_slope(SEASONS, w.values)
    lr_p = su.linregress(SEASONS, p.values); mk_p = su.mann_kendall(p.dropna().values); sen_p, _ = su.sens_slope(SEASONS, p.values)
    _trend_chart(SEASONS, w.values, lr_w, mk_w, sen_w,
                 "Trend in WA-affecting cyclone intensity (BOM 10-min wind), 1985–2024",
                 "Annual mean peak wind (knots)", "charts/03_trend_wind_speed.png", color=viz.TOMATO)
    _trend_chart(SEASONS, p.values, lr_p, mk_p, sen_p,
                 "Trend in WA-affecting cyclone minimum central pressure, 1985–2024",
                 "Annual mean minimum pressure (hPa)", "charts/04_trend_pressure.png", invert=True, color=viz.SEA)
    return pd.DataFrame(out).T


# ----- Step 4: rapid intensification --------------------------------------
def _storm_has_ri(g, thr=30.0):
    g = g.dropna(subset=["USA_WIND", "ISO_TIME"]).sort_values("ISO_TIME")
    if len(g) < 2:
        return False
    t = g.ISO_TIME.values.astype("datetime64[s]").astype("int64")/3600.0
    w = g.USA_WIND.values; best = 0.0
    for i in range(len(t)):
        dt = t - t[i]; j = np.where((dt >= 21) & (dt <= 27))[0]
        if j.size:
            best = max(best, float(np.max(w[j]-w[i])))
    return best >= thr


def rapid_intensification(storms):
    if RAW_IB.exists():
        obs = bd.load_obs()
        wa_sids = set(storms[storms.wa_affecting].sid)
        rec = [{"season": int(g.SEASON.iloc[0]), "ri": _storm_has_ri(g), "wa": sid in wa_sids}
               for sid, g in obs.groupby("SID")]
        ri = pd.DataFrame(rec)
        ri["decade"] = pd.cut(ri.season, [1984, 1994, 2004, 2014, 2024], labels=DECADES)
        wa = ri[ri.wa]
        tab = pd.DataFrame([{
            "decade": d,
            "WA_RI": int(wa[wa.decade == d].ri.sum()), "WA_n": int((wa.decade == d).sum()),
            "WA_RI_pct": 100*wa[wa.decade == d].ri.mean(),
            "SI_RI": int(ri[ri.decade == d].ri.sum()), "SI_n": int((ri.decade == d).sum()),
            "SI_RI_pct": 100*ri[ri.decade == d].ri.mean()} for d in DECADES])
        tab.to_csv("data/ri_by_decade.csv", index=False)
    else:
        tab = pd.read_csv("data/ri_by_decade.csv")

    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(4)
    ax.bar(x-0.2, tab.WA_RI, width=0.38, color=viz.TOMATO, alpha=0.85, label="WA-affecting")
    ax.bar(x+0.2, tab.SI_RI, width=0.38, color=viz.INDIGO, alpha=0.45, label="All South Indian Ocean")
    for i in range(4):
        ax.annotate(f"{int(tab.WA_RI.iloc[i])}\n({tab.WA_RI_pct.iloc[i]:.0f}%)", (x[i]-0.2, tab.WA_RI.iloc[i]),
                    ha="center", va="bottom", fontsize=8.5, color=viz.INK)
        ax.annotate(f"{int(tab.SI_RI.iloc[i])}\n({tab.SI_RI_pct.iloc[i]:.0f}%)", (x[i]+0.2, tab.SI_RI.iloc[i]),
                    ha="center", va="bottom", fontsize=8.5, color=viz.MUTED)
    ax.set_xticks(x); ax.set_xticklabels(DECADES)
    ax.set_xlabel("Decade"); ax.set_ylabel("Storms undergoing rapid intensification")
    ax.set_title("Rapid intensification (≥30 kt in 24 h) by decade, 1985–2024")
    ax.legend(loc="upper right"); ax.set_ylim(0, max(tab.SI_RI.max(), tab.WA_RI.max())*1.25)
    ax.annotate("Counts = storms with ≥1 RI episode. RI defined on USA 1-min winds.",
                xy=(0.012, 0.97), xycoords="axes fraction", va="top", fontsize=8.5, color=viz.MUTED)
    viz.credit(ax); fig.savefig("charts/05_rapid_intensification.png"); plt.close(fig)
    return tab


# ----- Step 5: SST correlation --------------------------------------------
def _sst_seasonal_from_raw():
    import xarray as xr
    ds = xr.open_dataset("data/raw/sst.mnmean.nc")
    sst = ds.sst; lat, lon = sst.lat, sst.lon
    box = sst.sel(lat=lat[(lat >= -30) & (lat <= -10)], lon=lon[(lon >= 70) & (lon <= 130)])
    ts = box.weighted(np.cos(np.deg2rad(box.lat))).mean(dim=["lat", "lon"]).to_series()
    df = ts.to_frame("sst"); df["year"] = df.index.year; df["month"] = df.index.month
    clim = df[(df.year >= 1991) & (df.year <= 2020)].groupby("month")["sst"].mean()
    df["anom"] = df["sst"] - df["month"].map(clim)
    df["season"] = np.where(df.month >= 11, df.year+1, df.year)
    return (df[df.month.isin([11, 12, 1, 2, 3, 4])].groupby("season")["anom"].mean().reindex(SEASONS))


def sst_correlation(storms):
    wa = storms[storms.wa_affecting]
    if RAW_SST.exists():
        seasonal = _sst_seasonal_from_raw()
        wa_wind = _annual(wa, "peak_bom_wind_kt"); wa_pres = _annual(wa, "min_wmo_pres_hpa")
        pd.DataFrame({"season": SEASONS, "sst_anom_NovApr": seasonal.values,
                      "wa_mean_wind_kt": wa_wind.values, "wa_mean_pres_hPa": wa_pres.values}
                     ).to_csv("data/sst_intensity.csv", index=False)
    else:
        d = pd.read_csv("data/sst_intensity.csv")
        seasonal = pd.Series(d.sst_anom_NovApr.values, index=d.season.values)
        wa_wind = pd.Series(d.wa_mean_wind_kt.values, index=d.season.values)
        wa_pres = pd.Series(d.wa_mean_pres_hPa.values, index=d.season.values)

    lr_sst = su.linregress(SEASONS, seasonal.values)
    r_w, p_w, n_w = su.pearsonr(seasonal.values, wa_wind.values)
    r_p, p_p, _ = su.pearsonr(seasonal.values, wa_pres.values)
    res = dict(sst_trend_decade=lr_sst.slope*10, sst_p=lr_sst.pvalue,
               r_wind=r_w, p_wind=p_w, r_pres=r_p, p_pres=p_p, n=n_w)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))
    ax1.bar(SEASONS, seasonal.values, color=viz.SEA, alpha=0.55)
    ax1.axhline(0, color=viz.MUTED, lw=0.8)
    ax1.set_ylabel("Nov–Apr SST anomaly (°C, vs 1991–2020)", color=viz.SEA)
    ax1.tick_params(axis="y", labelcolor=viz.SEA); ax1.set_xlabel("Cyclone season")
    axb = ax1.twinx()
    axb.plot(SEASONS, wa_wind.values, color=viz.TOMATO, lw=2, marker="o", ms=3.5)
    axb.set_ylabel("WA mean peak wind (kt, BOM 10-min)", color=viz.TOMATO)
    axb.tick_params(axis="y", labelcolor=viz.TOMATO); axb.grid(False)
    ax1.set_title("(a) Indian Ocean SST anomaly vs WA cyclone intensity")
    m = np.isfinite(seasonal.values) & np.isfinite(wa_wind.values)
    xx, yy = seasonal.values[m], wa_wind.values[m]
    lr = su.linregress(xx, yy)
    ax2.scatter(xx, yy, color=viz.INDIGO, s=36, alpha=0.8, edgecolor="white", zorder=3)
    xs = np.linspace(xx.min(), xx.max(), 50)
    ax2.plot(xs, lr.intercept+lr.slope*xs, color=viz.INK, lw=2)
    ax2.set_xlabel("Nov–Apr SST anomaly (°C)"); ax2.set_ylabel("WA mean peak wind (kt)")
    ax2.set_title("(b) Correlation")
    ax2.annotate(f"Pearson r = {r_w:+.2f}\np = {p_w:.2f}  (n = {n_w})\n"
                 f"{'not ' if p_w >= 0.05 else ''}significant",
                 xy=(0.04, 0.96), xycoords="axes fraction", va="top", fontsize=10, family="monospace",
                 bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=viz.MUTED, alpha=0.9))
    viz.credit(ax2); fig.savefig("charts/06_sst_correlation.png"); plt.close(fig)
    return res


if __name__ == "__main__":
    storms = load_storms()
    print(f"{len(storms)} SI storms, {storms.wa_affecting.sum()} WA-affecting")
    summary, *_ = explore(storms)
    print("\nDecadal summary:\n", summary.to_string(index=False))
    print("\nTrends:\n", trends(storms).to_string())
    print("\nRapid intensification:\n", rapid_intensification(storms).to_string(index=False))
    print("\nSST correlation:\n", sst_correlation(storms))
    print("\nAll 6 charts regenerated.")
