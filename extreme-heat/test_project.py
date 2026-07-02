"""
test_project.py: unit tests for the extreme-heat pipeline pieces that carry
analytical weight: the tenths-of-a-degree heuristic, both parsers, the
day-of-year percentile threshold, heatwave run detection, and the annual
metric / completeness accounting. Synthetic inputs only; runs in CI.

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


# --- tenths heuristic -----------------------------------------------------------
log = []
v = bd._maybe_tenths(np.array([250.0, 300.0, 180.0]), log, "t")
check("tenths converted", v[0], 25.0)
check_true("conversion logged", len(log) == 1)
v2 = bd._maybe_tenths(np.array([25.0, 30.0, 18.0]), log, "t")
check("degrees left alone", v2[0], 25.0)

# --- GHCN parser -----------------------------------------------------------------
dates = pd.date_range("1960-01-01", "1999-12-31", freq="D")
ghcn = "STATION,NAME,DATE,TMAX,TMIN\n" + "\n".join(
    f"ASN00009999,TESTVILLE,{d.date()},{30 + 10 * np.sin(2 * np.pi * (d.dayofyear / 365.0)):.1f},15.0"
    for d in dates)
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "ghcn.csv")
    open(p, "w").write(ghcn)
    g = bd.parse_ghcn(p, [])
check_true("GHCN parser returns a frame", g is not None)
check("GHCN row count", len(g), len(dates))
check_true("GHCN tmin captured", "tmin_c" in g.columns)

# --- BoM CDO parser -----------------------------------------------------------------
bom = ("Product code,Bureau of Meteorology station number,Year,Month,Day,"
       "Maximum temperature (Degree C),Days of accumulation,Quality\n"
       + "\n".join(f"IDCJAC0010,9021,{d.year},{d.month},{d.day},30.0,1,Y"
                   for d in pd.date_range("2000-01-01", "2000-03-31", freq="D")))
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "bom.csv")
    open(p, "w").write(bom)
    b = bd.parse_bom_cdo(p, [])
check_true("BoM parser returns a frame", b is not None)
check_true("BoM station id captured", b.station.iloc[0] == "9021")
check("BoM row count", len(b), 91)

# --- heatwave run detection ------------------------------------------------------------
check_true("no runs in all-False", bd.heatwave_runs([False] * 10) == (0, 0))
ev, days = bd.heatwave_runs([False, True, True, True, False, True, True, False])
check("one 3-day event detected", ev, 1)
check("3 days inside events", days, 3)
ev2, days2 = bd.heatwave_runs([True] * 5)
check("run at the end counted", ev2, 1)
check("5-day event length", days2, 5)
# missing days must break runs (conservative)
flags = np.array([True, True, False, True, True, True])
ev3, _ = bd.heatwave_runs(flags)
check("gap breaks the run", ev3, 1)

# --- day-of-year percentile threshold ------------------------------------------------------
const = pd.DataFrame({"date": dates, "tmax_c": 20.0,
                      "station": "X", "name": "X"})
thr, label = bd.doy_percentile_threshold(const)
check("constant series -> threshold equals the constant", np.nanmax(thr), 20.0)
check("constant series -> threshold equals the constant (min)",
      np.nanmin(thr[1:366]), 20.0)
check_true("baseline label says 1961-1990", label == "1961-1990")
short = const[const.date.dt.year >= 1995]
_, label2 = bd.doy_percentile_threshold(short)
check_true("short record falls back to full-record baseline",
           label2 == "full record")

# --- annual metrics and completeness ------------------------------------------------------
d2 = pd.DataFrame({"date": dates, "station": "X", "name": "X",
                   "tmax_c": 30.0})
d2.loc[d2.date.dt.year == 1970, "tmax_c"] = np.where(
    d2[d2.date.dt.year == 1970].date.dt.dayofyear <= 40, 41.0, 30.0)
# knock 30 days out of 1980 to make it incomplete
d2 = d2[~((d2.date.dt.year == 1980) & (d2.date.dt.dayofyear <= 30))]
metrics = bd.annual_metrics(d2)
y1970 = metrics[metrics.year == 1970].iloc[0]
check("1970 has 40 very hot days", y1970.days_ge_40, 40)
check("1970 TXx", y1970.txx_c, 41.0)
y1980 = metrics[metrics.year == 1980].iloc[0]
check_true("1980 flagged incomplete (30 missing days)", not bool(y1980.complete))
y1971 = metrics[metrics.year == 1971].iloc[0]
check_true("1971 complete", bool(y1971.complete))
check("1971 has no 35 C days", y1971.days_ge_35, 0)
# the 1970 hot spell should register as a heatwave (40 consecutive days >= p90)
check_true("1970 hot spell detected as heatwave", y1970.hw_events >= 1)

print(f"\n{PASS} passed, {FAIL} failed")
raise SystemExit(1 if FAIL else 0)
