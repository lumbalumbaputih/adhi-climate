"""
test_project.py: unit tests for the wheat-yields pipeline pieces that carry
analytical weight: season-label parsing, the CSV contract parser, the yield
sanity gate, and the detrended-sensitivity logic (including the raw-vs-
detrended contrast the whole project is about). Synthetic inputs only; runs
in CI.

Run:  python3 test_project.py        (exits non-zero on any failure)
"""
import os
import tempfile
import numpy as np
import pandas as pd

import build_dataset as bd
import analysis as an
import stats_utils as su

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


# --- season labels -----------------------------------------------------------
check("'1975-76' -> 1975", bd._season_to_year("1975-76"), 1975)
check("'1975/76' -> 1975", bd._season_to_year("1975/76"), 1975)
check("'2003-04' -> 2003", bd._season_to_year("2003-04"), 2003)
check("'1975' -> 1975", bd._season_to_year("1975"), 1975)
check_true("garbage -> None", bd._season_to_year("n.a.") is None)

# --- CSV contract parser --------------------------------------------------------
text = ("# source: https://example.invalid/abares\n"
        "year,wheat_area_ha,wheat_production_t\n"
        + "\n".join(f"{y},{3_000_000},{int(3_000_000 * 1.2)}"
                    for y in range(1975, 2025)))
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "wheat.csv")
    open(p, "w").write(text)
    w = bd.parse_wheat_csv(p)
check_true("contract CSV parsed", w is not None)
check("rows", len(w), 50)
check("yield computed", w.yield_t_ha.iloc[0], 1.2)
check_true("source captured", "example.invalid" in w.attrs["source"])

# season-labelled variant with ABARES-ish headers
text2 = ("season,Area planted (ha),Production (t)\n"
         + "\n".join(f"1975-76,100,120" for _ in range(1))
         + "\n" + "\n".join(f"{y}-{str(y + 1)[2:]},100,120"
                            for y in range(1976, 2020)))
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "abares.csv")
    open(p, "w").write(text2)
    w2 = bd.parse_wheat_csv(p)
check_true("season-labelled CSV parsed", w2 is not None)
check("season parsed to sowing year", w2.year.iloc[0], 1975)

# --- detrending ---------------------------------------------------------------------
years = np.arange(1975, 2025, dtype=float)
vals = 1.0 + 0.02 * (years - 1975)          # pure trend, no anomalies
anom, tr = an.detrend_pct(years, vals)
check("pure trend detrends to ~0%", float(np.max(np.abs(anom))), 0.0, tol=1e-8)
check("trend slope recovered", tr.slope, 0.02, tol=1e-12)

# --- the raw-vs-detrended contrast the project exists to show ------------------------
rng = np.random.default_rng(8)
rain_anom = 15 * rng.standard_normal(years.size)          # % anomaly
rain_anom -= 0.4 * (years - 1975)                          # drying trend
tech = 1.0 + 0.02 * (years - 1975)                         # rising technology
yield_t = tech * (1 + 0.008 * rain_anom)                   # 0.8% yield per 1% rain
yld_anom, _ = an.detrend_pct(years, yield_t)
r_raw, _, _ = su.pearsonr(rain_anom, yield_t)
r_dt, _, _ = su.pearsonr(rain_anom, yld_anom)
check_true("raw correlation is weaker or wrong-signed",
           abs(r_raw) < abs(r_dt))
check_true("detrended correlation is strongly positive", r_dt > 0.8)
sens = su.linregress(rain_anom, yld_anom)
check("sensitivity ~ 0.8% per 1% rain", sens.slope, 0.8, tol=0.15)

# --- yield sanity gate ------------------------------------------------------------------
bad_text = ("# source: x\nyear,wheat_area_ha,wheat_production_t\n"
            + "\n".join(f"{y},100,5000" for y in range(1975, 2025)))  # 50 t/ha
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "bad.csv")
    open(p, "w").write(bad_text)
    wb = bd.parse_wheat_csv(p)
check_true("implausible yields parse but would be caught by the gate",
           wb is not None and (wb.yield_t_ha > 6.0).all())

print(f"\n{PASS} passed, {FAIL} failed")
raise SystemExit(1 if FAIL else 0)
