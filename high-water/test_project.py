"""
test_project.py: unit tests for the high-water pipeline pieces that carry
analytical weight: the UHSLC parser, the QC screens, the RQDS/FD splice, the
wide-CSV round trip, the completeness rule, the fixed benchmarks, and the
raw vs mean-adjusted exceedance counting. Synthetic inputs only; runs in CI.

Run:  python3 test_project.py        (exits non-zero on any failure)
"""
import numpy as np
import pandas as pd

import build_dataset as bd
import analysis as an

PASS = 0
FAIL = 0


def check(name, got, want, tol=1e-9):
    global PASS, FAIL
    ok = abs(got - want) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got:.6g}, want {want:.6g}")
    PASS += ok
    FAIL += (not ok)


def check_true(name, cond):
    global PASS, FAIL
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")
    PASS += bool(cond)
    FAIL += (not cond)


def hourly_frame(start, end, mm, feed="rqds"):
    """Constant-level hourly frame over [start, end] inclusive."""
    t = pd.date_range(start, str(pd.Timestamp(end) + pd.Timedelta(hours=23)),
                      freq="h")
    return pd.DataFrame({"t": t, "mm": float(mm), "feed": feed})


# --- parser -----------------------------------------------------------------
text = "\n".join(f"1990,{m},{d},{h},{700 + h}"
                 for m in (1, 2, 3) for d in range(1, 29)
                 for h in range(24))
text += f"\n1990,4,1,0,{bd.SENTINEL}\n1990,4,1,1,800"
p = bd.parse_uhslc_hourly(text, "synthetic")
check_true("parser returns a frame", p is not None)
check_true("sentinel row dropped", (p.mm > bd.SENTINEL).all())
check("parser keeps the valid extra hour", float((p.mm == 800).sum()), 1)
check_true("a stray header line survives numeric coercion",
           bd.parse_uhslc_hourly("year,month,day,hour,mm\n" + text,
                                 "hdr") is not None)

# --- QC ----------------------------------------------------------------------
log = []
s = hourly_frame("2000-01-01", "2000-03-31", 700)
s.loc[5, "mm"] = 9999.0       # out of range high
s.loc[6, "mm"] = -50.0        # out of range low
q = bd.qc(s, log, "t")
# The constant series IS one long flatline, so everything else goes too:
check("flatline screen removes the stuck run", len(q), 0)
varied = hourly_frame("2000-01-01", "2000-03-31", 0)
varied["mm"] = 700 + (np.arange(len(varied)) % 7)   # never 24 identical hours
varied.loc[3, "mm"] = 9999.0
q2 = bd.qc(varied, [], "t")
check("range screen drops exactly one hour", len(q2), len(varied) - 1)

# --- splice -------------------------------------------------------------------
rq = hourly_frame("2020-01-01", "2021-12-31", 700, "x")
fd = hourly_frame("2020-01-01", "2023-12-31", 800, "y")
sp = bd.splice(rq, fd, [])
check_true("pre-2022 hours come from RQDS",
           (sp[sp.t.dt.year < 2022].mm == 700).all())
check_true("2022+ hours come from FD",
           (sp[sp.t.dt.year >= 2022].mm == 800).all())
check_true("feed column recorded", set(sp.feed) == {"rqds", "fd"})

# --- wide round trip ------------------------------------------------------------
w = bd.to_wide(sp)
check("wide has one row per day", len(w), sp.t.dt.date.nunique())
check_true("wide has 24 hour columns + date + feed", w.shape[1] == 26)

# --- completeness rule ----------------------------------------------------------
full = hourly_frame("2010-01-01", "2010-12-31", 700)
full["mm"] = 700 + (np.arange(len(full)) % 7)
cy = an.complete_years(full)
check_true("a full year is complete", cy[2010])
gappy = full[full.t.dt.month != 7].copy()          # July wholly missing
cy2 = an.complete_years(gappy)
check_true("a missing storm month fails the month rule", not cy2[2010])
thin = full.iloc[::2].copy()                        # 50% of hours, evenly
cy3 = an.complete_years(thin)
check_true("50% of hours fails the year rule", not cy3[2010])

# --- benchmarks and exceedance counting -----------------------------------------
# Baseline decade (1984-1993) of a known repeating ramp 0..999 mm, then one
# extra year (1994) shifted up 100 mm. Percentiles and counts are exact.
t = pd.date_range("1984-01-01", "1994-12-31 23:00", freq="h")
idx = np.arange(len(t))
mm = (idx % 1000).astype(float)
is94 = t.year == 1994
mm[is94] += 100.0
ramp = pd.DataFrame({"t": t, "mm": mm, "feed": "rqds"})
marks, base_mean, base_n = an.fixed_benchmarks(ramp)
check("b1 = 99.0th pctl of the ramp", marks["b1"], 989)
check("b2 = 99.5th pctl of the ramp", marks["b2"], 994)
check("b3 = 99.9th pctl of the ramp", marks["b3"], 998)
check("baseline mean is the plain mean of the baseline hours", base_mean,
      float(np.mean(mm[~is94])), tol=1e-9)

completeness = an.complete_years(ramp)
am = an.annual_metrics(ramp, marks, base_mean, completeness)
y0 = am[am.year == 1984].iloc[0]
manual84 = int((mm[t.year == 1984] >= marks["b1"]).sum())
# hand check of the same number: 8784 hours starting at ramp phase 0 give
# 8 full cycles of 11 qualifying phases (989..999) plus phases 0..783, none
# of which qualify: 88 hours.
check("manual 1984 count is the hand-derived 88", manual84, 88)
check("raw exceedance count matches manual count", y0.hours_ge_b1, manual84)

# The shifted 1994 year: raw counting sees the +100 shift, phase-aware.
y94 = am[am.year == 1994].iloc[0]
phase94 = idx[is94][0] % 1000
manual94_raw = int((((phase94 + np.arange(8760)) % 1000) + 100
                    >= marks["b2"]).sum())
check("shifted year raw count (phase-aware)", y94.hours_ge_b2, manual94_raw)
# Adjusted counting removes the year's mean anomaly (about +100 mm here), so
# the count must fall back to within a few ramp steps of an unshifted year.
y92 = am[am.year == 1992].iloc[0]
check("adjusted count undoes the shift", y94.adj_hours_ge_b2,
      y92.hours_ge_b2, tol=15)
check_true("mean-rise contribution dominates the shifted year",
           y94.hours_ge_b2 - y94.adj_hours_ge_b2 > 700)

# --- trend row plumbing -----------------------------------------------------------
tr = an.trend_row("up", np.arange(2000, 2020), np.arange(20) * 2.0)
check("Sen slope on a clean line", tr["sen_slope_per_yr"], 2.0)
check_true("MK calls a clean line increasing", tr["mk_trend"] == "increasing")

print(f"\n{PASS} passed, {FAIL} failed")
raise SystemExit(1 if FAIL else 0)
