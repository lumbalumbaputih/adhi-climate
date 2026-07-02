"""
analysis.py: the analysis steps as importable functions used by
cyclone_analysis.ipynb. Each makes its chart(s) and returns the numbers.

Runs from raw data (data/raw/) when present, otherwise from the committed
cleaned CSVs, so the pipeline reproduces on a fresh clone. Run as a script to
regenerate every chart and print every headline figure:

    python analysis.py

A core methodological point, visible throughout: the sign of the intensity
trend depends on which agency's wind record you use. BOM 10-min winds drift
down; USA 1-min winds drift up, on the same storms. Both are shown side by
side, and central pressure (no averaging-time ambiguity) is used as the
tie-breaker. Trend p-values are reported plain and with trend-free
prewhitening (TFPW), which corrects for serial correlation.
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
OBS_WA = Path("data/ibtracs_obs_wa.csv")


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
        "mean_USA_wind_kt": wa.loc[wa.decade == d, "peak_usa_wind_kt"].mean(),
        "median_BOM_wind_kt": wa.loc[wa.decade == d, "peak_bom_wind_kt"].median(),
        # BOM pressure: identical to WMO pressure for WA storms (BOM is the
        # WMO agency for the Australian region) but labelled consistently
        "mean_min_pres_hPa": wa.loc[wa.decade == d, "min_bom_pres_hpa"].mean(),
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
def _fit(x, y):
    """OLS + plain MK + TFPW MK + Sen's slope on the finite pairs."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    lr = su.linregress(x[m], y[m])
    mk = su.mann_kendall(y[m])
    tf = su.mann_kendall_tfpw(y[m])
    sen, _ = su.sens_slope(x[m], y[m])
    return lr, mk, tf, sen


def _panel_trend(ax, x, y, lr, mk, tf, sen, ylabel, color, invert=False):
    m = np.isfinite(np.asarray(x, float)) & np.isfinite(np.asarray(y, float))
    xx, yy = np.asarray(x)[m], np.asarray(y)[m]
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
    txt = (f"OLS slope: {lr.slope*10:+.1f}/decade\n"
           f"Sen slope: {sen*10:+.1f}/decade\n"
           f"MK p = {mk.pvalue:.3f}  ({sig})\n"
           f"MK p (prewhitened) = {tf.pvalue:.3f}\n"
           f"r² = {lr.r_squared:.2f}   n = {n} seasons")
    ax.annotate(txt, xy=(0.02, 0.03), xycoords="axes fraction", va="bottom", ha="left",
                fontsize=9, family="monospace",
                bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=viz.MUTED, alpha=0.9))
    ax.set_xlabel("Cyclone season (year season ends)"); ax.set_ylabel(ylabel)
    ax.legend(loc="upper right", ncol=3, fontsize=8.5)


def trends(storms):
    """Trend table across metrics, plus charts 03 (dual wind) and 04 (pressure).

    The wind trend is reported for BOTH agency records because they disagree
    in sign. Coverage matters: BOM winds exist for only ~40% of basin storms
    (BOM is the agency for the Australian region only) and that share rises
    over time, so the basin BOM series mixes a changing subset of storms.
    """
    wa = storms[storms.wa_affecting]
    out = {}
    series = {
        "WA wind (BOM 10-min)": (wa, "peak_bom_wind_kt"),
        "WA wind (USA 1-min)": (wa, "peak_usa_wind_kt"),
        "WA pressure (BOM)": (wa, "min_bom_pres_hpa"),
        "Basin wind (BOM 10-min)": (storms, "peak_bom_wind_kt"),
        "Basin wind (USA 1-min)": (storms, "peak_usa_wind_kt"),
        "Basin pressure (WMO)": (storms, "min_wmo_pres_hpa"),
    }
    for name, (grp, col) in series.items():
        s = _annual(grp, col)
        lr, mk, tf, sen = _fit(SEASONS, s.values)
        out[name] = dict(slope_decade=lr.slope*10, sen_decade=sen*10,
                         ols_p=lr.pvalue, mk_p=mk.pvalue, mk_p_tfpw=tf.pvalue,
                         r1=tf.r1, r2=lr.r_squared, trend=mk.trend,
                         coverage_pct=100.0*grp[col].notna().mean())

    # chart 03: the same WA storms under the two wind records, side by side
    w_bom = _annual(wa, "peak_bom_wind_kt"); w_usa = _annual(wa, "peak_usa_wind_kt")
    fits_bom = _fit(SEASONS, w_bom.values); fits_usa = _fit(SEASONS, w_usa.values)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.4), sharex=True)
    _panel_trend(ax1, SEASONS, w_bom.values, *fits_bom,
                 "Annual mean peak wind (kt, BOM 10-min)", viz.TOMATO)
    ax1.set_title("(a) BOM 10-min wind: drifting down")
    _panel_trend(ax2, SEASONS, w_usa.values, *fits_usa,
                 "Annual mean peak wind (kt, USA 1-min)", viz.INDIGO)
    ax2.set_title("(b) USA 1-min wind: drifting up")
    fig.suptitle("Same WA-affecting storms, two wind records, opposite trends (1985–2024)",
                 fontweight="bold", fontsize=14)
    viz.credit(ax2); fig.savefig("charts/03_trend_wind_speed.png"); plt.close(fig)

    # chart 04: pressure, the record with no averaging-time ambiguity
    p_bom = _annual(wa, "min_bom_pres_hpa")
    lr_p, mk_p, tf_p, sen_p = _fit(SEASONS, p_bom.values)
    fig, ax = plt.subplots(figsize=(9, 5))
    _panel_trend(ax, SEASONS, p_bom.values, lr_p, mk_p, tf_p, sen_p,
                 "Annual mean minimum pressure (hPa)", viz.SEA, invert=True)
    ax.set_title("Trend in WA-affecting cyclone minimum central pressure, 1985–2024")
    viz.credit(ax); fig.savefig("charts/04_trend_pressure.png"); plt.close(fig)
    return pd.DataFrame(out).T


# ----- Step 4: rapid intensification --------------------------------------
def _storm_has_ri(g, thr=30.0):
    """True if the storm gained >= thr kt (USA 1-min wind) over ~24 hours.

    Best-track fixes are nominally 6-hourly but not perfectly regular, so the
    24 h window is taken as 21-27 h. That admits jumps of up to 27 h, which is
    slightly liberal against the strict <= 24 h definition; the bias applies
    equally to every decade, so it does not tilt the decade comparison.
    """
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


def _detrend_on(x, y):
    """Residuals of y regressed on x (finite pairs assumed)."""
    lr = su.linregress(x, y)
    return y - (lr.intercept + lr.slope * x)


def sst_correlation(storms):
    """SST trend and SST-intensity correlation, raw AND detrended.

    Both series carry opposing long-term trends (SST up, BOM wind down), so a
    raw correlation partly measures those trends, not a seasonal link. The
    detrended correlation is the honest year-to-year number.
    """
    wa = storms[storms.wa_affecting]
    if RAW_SST.exists():
        seasonal = _sst_seasonal_from_raw()
        wa_wind = _annual(wa, "peak_bom_wind_kt"); wa_pres = _annual(wa, "min_bom_pres_hpa")
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
    # detrended: remove each series' linear trend in season first
    mm = np.isfinite(seasonal.values) & np.isfinite(wa_wind.values)
    xs = SEASONS[mm].astype(float)
    r_wd, p_wd, _ = su.pearsonr(_detrend_on(xs, seasonal.values[mm]),
                                _detrend_on(xs, wa_wind.values[mm]))
    mp = np.isfinite(seasonal.values) & np.isfinite(wa_pres.values)
    xp = SEASONS[mp].astype(float)
    r_pd, p_pd, _ = su.pearsonr(_detrend_on(xp, seasonal.values[mp]),
                                _detrend_on(xp, wa_pres.values[mp]))
    res = dict(sst_trend_decade=lr_sst.slope*10, sst_p=lr_sst.pvalue,
               r_wind=r_w, p_wind=p_w, r_wind_detrended=r_wd, p_wind_detrended=p_wd,
               r_pres=r_p, p_pres=p_p, r_pres_detrended=r_pd, p_pres_detrended=p_pd,
               n=n_w)

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
    sig = "neither significant" if max(p_w, p_wd) >= 0.05 else "see p-values"
    ax2.annotate(f"raw       r = {r_w:+.2f}  p = {p_w:.2f}\n"
                 f"detrended r = {r_wd:+.2f}  p = {p_wd:.2f}\n"
                 f"(n = {n_w}; {sig}.\n"
                 f"Raw r mostly reflects the two\n"
                 f"opposing long-term trends.)",
                 xy=(0.04, 0.96), xycoords="axes fraction", va="top", fontsize=9.5, family="monospace",
                 bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=viz.MUTED, alpha=0.9))
    viz.credit(ax2); fig.savefig("charts/06_sst_correlation.png"); plt.close(fig)
    return res


# ----- Step 6: proximity sensitivity ---------------------------------------
def proximity_sensitivity(storms):
    """Two robustness checks on the 'WA-affecting' definition.

    (1) Lifetime peak vs near-coast peak. The headline intensity metric is a
        storm's lifetime peak, which can occur thousands of km from WA. Here
        the peak is recomputed using only fixes within 500 km of the WA coast,
        which is what actually matters for WA assets.
    (2) The 500 km radius itself: counts and intensity trends are recomputed
        with 300 and 700 km radii.

    Uses the committed per-observation track file, so it runs on a fresh clone.
    Writes data/wa_proximity_sensitivity.csv and charts/07_proximity_sensitivity.png.
    """
    wa = storms[storms.wa_affecting]
    obs = pd.read_csv(OBS_WA, parse_dates=["ISO_TIME"])
    near = obs[obs.dist_wa_km <= 500.0]
    near_peak = near.groupby("SID").agg(near_bom_kt=("BOM_WIND", "max"),
                                        near_usa_kt=("USA_WIND", "max"),
                                        season=("SEASON", "first")).reset_index()

    life = _annual(wa, "peak_bom_wind_kt")
    near_annual = (near_peak.dropna(subset=["near_bom_kt"])
                   .groupby("season")["near_bom_kt"].mean().reindex(SEASONS))

    rows = []
    for label, s in [("lifetime_peak_bom", life), ("near_wa_peak_bom", near_annual)]:
        lr, mk, tf, sen = _fit(SEASONS, s.values)
        rows.append({"series": label, "radius_km": 500,
                     "slope_kt_decade": lr.slope*10, "ols_p": lr.pvalue,
                     "mk_p": mk.pvalue, "mk_p_tfpw": tf.pvalue})

    # radius sensitivity: counts + intensity trend at 300/500/700 km
    for radius in (300.0, 500.0, 700.0):
        sub = storms[storms.min_dist_wa_km <= radius]
        counts = sub.groupby("season").size().reindex(SEASONS, fill_value=0)
        lr_c, mk_c, tf_c, _ = _fit(SEASONS, counts.values.astype(float))
        winds = _annual(sub, "peak_bom_wind_kt")
        lr_w, mk_w, tf_w, _ = _fit(SEASONS, winds.values)
        rows.append({"series": "radius_check", "radius_km": int(radius),
                     "n_storms": int(len(sub)),
                     "mean_count_per_season": float(counts.mean()),
                     "count_slope_decade": lr_c.slope*10, "count_mk_p": mk_c.pvalue,
                     "slope_kt_decade": lr_w.slope*10, "ols_p": lr_w.pvalue,
                     "mk_p": mk_w.pvalue, "mk_p_tfpw": tf_w.pvalue})
    tab = pd.DataFrame(rows)
    tab.to_csv("data/wa_proximity_sensitivity.csv", index=False)

    # chart 07
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.4))
    ax1.plot(SEASONS, life.values, color=viz.TOMATO, lw=1.6, marker="o", ms=4,
             alpha=0.9, label="lifetime peak (anywhere in basin)")
    ax1.plot(SEASONS, near_annual.values, color=viz.FOREST, lw=1.6, marker="s", ms=4,
             alpha=0.9, label="peak within 500 km of WA coast")
    for s, c in [(life, viz.TOMATO), (near_annual, viz.FOREST)]:
        lr, *_ = _fit(SEASONS, s.values)
        xs = np.array([SEASONS.min(), SEASONS.max()])
        ax1.plot(xs, lr.intercept + lr.slope*xs, color=c, lw=2.0, ls="--")
    ax1.set_xlabel("Cyclone season (year season ends)")
    ax1.set_ylabel("Annual mean peak wind (kt, BOM 10-min)")
    ax1.set_title("(a) Lifetime peak vs peak near the WA coast")
    ax1.legend(loc="upper right", fontsize=9)

    rc = tab[tab.series == "radius_check"]
    x = np.arange(len(rc))
    ax2.bar(x, rc.mean_count_per_season, width=0.55, color=viz.SEA, alpha=0.7)
    for i, (_, r) in enumerate(rc.iterrows()):
        ax2.annotate(f"{r.mean_count_per_season:.1f}/season\n"
                     f"wind {r.slope_kt_decade:+.1f} kt/dec\nMK p={r.mk_p:.2f}",
                     (i, r.mean_count_per_season), ha="center", va="bottom", fontsize=9)
    ax2.set_xticks(x); ax2.set_xticklabels([f"{int(r)} km" for r in rc.radius_km])
    ax2.set_xlabel("Proximity radius defining 'WA-affecting'")
    ax2.set_ylabel("Mean storms per season")
    ax2.set_ylim(0, ax2.get_ylim()[1]*1.35)
    ax2.set_title("(b) Sensitivity to the proximity radius")
    fig.suptitle("How robust is the 'WA-affecting' definition?", fontweight="bold", fontsize=14)
    viz.credit(ax2); fig.savefig("charts/07_proximity_sensitivity.png"); plt.close(fig)
    return tab


if __name__ == "__main__":
    storms = load_storms()
    print(f"{len(storms)} SI storms, {storms.wa_affecting.sum()} WA-affecting")
    summary, *_ = explore(storms)
    print("\nDecadal summary:\n", summary.to_string(index=False))
    print("\nTrends (note coverage_pct before trusting a series):\n",
          trends(storms).to_string())
    print("\nRapid intensification:\n", rapid_intensification(storms).to_string(index=False))
    print("\nSST correlation (raw and detrended):\n", sst_correlation(storms))
    print("\nProximity sensitivity:\n", proximity_sensitivity(storms).to_string(index=False))
    print("\nAll 7 charts regenerated.")
