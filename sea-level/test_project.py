"""
test_project.py: unit tests for the sea-level pipeline pieces that carry
analytical weight: the PSMSL RLR parser (semicolon format, -99999 missing,
month decoding), annual completeness, the quadratic acceleration estimator,
and the rolling-rate windows. Synthetic inputs only; runs in CI.

Run:  python3 test_project.py        (exits non-zero on any failure)
"""
import os
import tempfile
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


# --- RLR parser ---------------------------------------------------------------
lines = []
for y in range(1950, 2020):
    for m in range(1, 13):
        t = y + (m - 0.5) / 12.0
        h = -99999 if (y == 1960 and m <= 6) else 7000 + (y - 1950)
        lines.append(f" {t:.4f}; {h}; 0; 000")
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "111.rlrdata")
    open(p, "w").write("\n".join(lines))
    m = bd.parse_rlr_monthly(p)
check_true("RLR parser returns a frame", m is not None)
check("RLR rows", len(m), 70 * 12)
check_true("-99999 becomes NaN", m[(m.year == 1960) & (m.month == 3)]
           .msl_mm.isna().all())
check_true("month decoding: first row is January",
           m.iloc[0].month == 1 and m.iloc[11].month == 12)

# --- metric-file guard: local-datum heights must abort ---------------------------
metric_lines = []
for y in range(1950, 2000):
    for mo in range(1, 13):
        t = y + (mo - 0.5) / 12.0
        metric_lines.append(f" {t:.4f}; {550 + (y - 1950)}; 0; 000")
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "111.metdata")
    open(p, "w").write("\n".join(metric_lines))
    try:
        bd.parse_rlr_monthly(p)
        aborted = False
    except SystemExit as e:
        aborted = "METRIC" in str(e)
check_true("metric-datum file is refused with an explanation", aborted)

# --- annual completeness --------------------------------------------------------
annual = bd.to_annual(m)
y1960 = annual[annual.year == 1960].iloc[0]
check("1960 has 6 valid months", y1960.n_months, 6)
check_true("1960 flagged incomplete", not bool(y1960.complete))
y1970 = annual[annual.year == 1970].iloc[0]
check_true("1970 complete", bool(y1970.complete))
check("linear synthetic: 1970 anomaly vs 1990-2009 mean",
      y1970.anom_mm, (1970 - 1950) - (np.mean(range(1990, 2010)) - 1950))

# --- quadratic acceleration -------------------------------------------------------
years = np.arange(1900, 2020, dtype=float)
# y = 0.5*(t-1960)^2 / 100 -> b2 = 0.005, acceleration = 0.01 mm/yr^2
y = 0.005 * (years - 1960.0) ** 2
q = an.quadratic_fit(years, y)
check("quadratic fit recovers b2", q["b2"], 0.005, tol=1e-12)
check("acceleration = 2*b2", 2 * q["b2"], 0.01, tol=1e-12)
check_true("perfect quadratic: tiny p-value", q["p2"] < 1e-10)
# pure line: acceleration ~ 0, p large
rng = np.random.default_rng(2)
ylin = 1.5 * (years - 1900) + 5.0 * rng.standard_normal(years.size)
q2 = an.quadratic_fit(years, ylin)
check_true("no acceleration in a line (p > 0.05)", q2["p2"] > 0.05)
check("linear term recovered on noisy line", q2["b1"], 1.5, tol=0.15)

# --- rolling rates -----------------------------------------------------------------
ann = pd.DataFrame({"year": years.astype(int),
                    "anom_mm": 2.0 * (years - 1900),
                    "complete": True})
roll = an.rolling_rates(ann, window=30)
check_true("rolling windows produced", len(roll) > 50)
check("every 30-year window of a 2 mm/yr line reads 2 mm/yr",
      float(np.max(np.abs(roll.rate_mm_per_yr - 2.0))), 0.0, tol=1e-9)

print(f"\n{PASS} passed, {FAIL} failed")
raise SystemExit(1 if FAIL else 0)
