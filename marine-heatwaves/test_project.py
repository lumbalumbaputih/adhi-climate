"""
test_project.py: unit tests for the marine-heatwave pipeline pieces that
carry analytical weight: the ERDDAP parser (with its units row), box
averaging, the Hobday climatology, event detection (minimum length, gap
merging, categories), and annual metrics. Synthetic inputs only; runs in CI.

Run:  python3 test_project.py        (exits non-zero on any failure)
"""
import os
import tempfile
import numpy as np
import pandas as pd

import build_dataset as bd

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


# --- ERDDAP parser (units row must be skipped) -------------------------------------
erddap = ("time,latitude,longitude,sst\n"
          "UTC,degrees_north,degrees_east,degree_C\n"
          "2010-01-01T12:00:00Z,-22.125,113.125,26.4\n"
          "2010-01-01T12:00:00Z,-22.375,113.125,26.8\n"
          "2010-01-02T12:00:00Z,-22.125,113.125,27.0\n")
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "erddap.csv")
    open(p, "w").write(erddap)
    e = bd.parse_erddap_sst(p)
check_true("ERDDAP parser returns a frame", e is not None)
check("ERDDAP rows parsed", len(e), 3)
check_true("units row not read as data", np.isfinite(e.sst).all())

bm = bd.box_mean(e)
check("box mean day 1 = mean of 2 cells", bm.sst.iloc[0], 26.6)
check("box mean day 1 counts 2 cells", bm.n_cells.iloc[0], 2)

# --- synthetic 30-year daily SST with a planted event -------------------------------
dates = pd.date_range("1982-01-01", "2014-12-31", freq="D")
rng = np.random.default_rng(5)
seas = 25.0 + 2.0 * np.cos(2 * np.pi * (dates.dayofyear - 40) / 365.25)
sst = seas + 0.3 * rng.standard_normal(len(dates))
sst = pd.Series(sst, index=dates)
# plant a 20-day +4 C spike in Feb-Mar 2011 with a 2-day dip in the middle
spike = pd.date_range("2011-02-10", "2011-03-01", freq="D")
sst.loc[spike] += 4.0
dip = pd.date_range("2011-02-19", "2011-02-20", freq="D")
sst.loc[dip] -= 4.0          # back to normal for 2 days mid-event
daily = pd.DataFrame({"date": dates, "sst": sst.values})

clim_mean, thr, label = bd.climatology(daily)
check_true("baseline label is 1982-2011", label == "1982-2011")
check_true("threshold sits above climatology everywhere",
           np.nanmin((thr - clim_mean)[1:366]) > 0)

events, flagged = bd.detect_events(daily, clim_mean, thr)
check_true("at least one event detected", len(events) >= 1)
big = events.loc[events.max_intensity_c.idxmax()]
check_true("planted 2011 event found",
           pd.Timestamp(big.start).year == 2011)
check_true("2-day dip merged into one event (Hobday gap rule)",
           big.duration_days >= 18)
check_true("peak intensity near +4 C", 3.0 < big.max_intensity_c < 5.5)
check_true("category at least II Strong", big.category != "I Moderate")

# --- minimum-length rule ---------------------------------------------------------------
short = daily.copy()
short_dates = pd.date_range("2005-06-01", "2005-06-03", freq="D")  # 3 days only
short.loc[short.date.isin(short_dates), "sst"] += 6.0
ev2, _ = bd.detect_events(short, clim_mean, thr)
starts_2005_jun = [e for _, e in ev2.iterrows()
                   if pd.Timestamp(e.start).year == 2005
                   and pd.Timestamp(e.start).month == 6]
check_true("3-day spike does NOT become an event (5-day minimum)",
           len(starts_2005_jun) == 0)

# --- annual metrics ------------------------------------------------------------------------
annual = bd.annual_metrics(flagged)
y2011 = annual[annual.year == 2011].iloc[0]
check_true("2011 has the most MHW days",
           y2011.mhw_days == annual.mhw_days.max())
check_true("all synthetic years complete", bool(annual.complete.all()))

print(f"\n{PASS} passed, {FAIL} failed")
raise SystemExit(1 if FAIL else 0)
