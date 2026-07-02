"""
test_project.py: unit tests for the water-security pipeline pieces that carry
analytical weight: water-year labelling, completeness accounting, the tolerant
streamflow parser, and the two elasticity estimators. Synthetic inputs only;
no real data is needed, so this runs in CI.

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


# --- water-year labelling ----------------------------------------------------
dates = pd.to_datetime(["2000-04-30", "2000-05-01", "2001-04-30", "2001-05-01"])
wy = bd.water_year_label(dates)
check("30 Apr 2000 is water year 1999", wy[0], 1999)
check("1 May 2000 is water year 2000", wy[1], 2000)
check("30 Apr 2001 is water year 2000", wy[2], 2000)
check("1 May 2001 is water year 2001", wy[3], 2001)

# expected days: WY 1999 = May 1999-Apr 2000, contains 29 Feb 2000 -> 366
check("WY1999 has 366 days", bd.wy_expected_days(1999), 366)
check("WY2000 has 365 days", bd.wy_expected_days(2000), 365)

# --- aggregation and completeness ----------------------------------------------
full = pd.date_range("2000-05-01", "2001-04-30", freq="D")     # complete WY2000
partial = pd.date_range("2001-05-01", "2002-03-31", freq="D")  # 30 days short
daily = pd.DataFrame({
    "station": "TEST01", "station_name": "Test Brook",
    "date": full.append(partial),
    "flow_ML": 2.0,
})
agg = bd.to_water_years(daily)
row0 = agg[agg.water_year == 2000].iloc[0]
row1 = agg[agg.water_year == 2001].iloc[0]
check("complete year total", row0.total_ML, 2.0 * 365)
check("complete year missing days", row0.days_missing, 0)
check_true("complete year flagged complete", bool(row0.complete))
check("partial year missing days", row1.days_missing, 30)
check_true("partial year flagged incomplete", not bool(row1.complete))

# --- parser: HRS-style daily CSV with metadata and ISO dates ---------------------
hrs_text = "\n".join(
    ["# Hydrologic Reference Stations",
     "# Station Number: 616999",
     "# Station Name: Synthetic Brook at Nowhere",
     "Date,Flow (ML/day),Bureau QCode"]
    + [f"{d.date()},{1.0 + (i % 7) * 0.1:.2f},A"
       for i, d in enumerate(pd.date_range("1980-01-01", "1995-12-31", freq="D"))]
)
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "hrs_station.csv")
    with open(p, "w") as f:
        f.write(hrs_text)
    parsed = bd.parse_daily_flow(p)
check_true("HRS parser returns a frame", parsed is not None)
check_true("HRS parser finds the station id", parsed.station.iloc[0] == "616999")
check("HRS parser row count", len(parsed),
      len(pd.date_range("1980-01-01", "1995-12-31", freq="D")))

# --- parser: day-first dates and negative flows -----------------------------------
dmy_dates = pd.date_range("1980-01-01", "1994-12-31", freq="D")
dmy_text = "Date,Discharge ML\n" + "\n".join(
    f"{d.strftime('%d/%m/%Y')},{-1.0 if i == 0 else 3.0}"
    for i, d in enumerate(dmy_dates))
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "dmy.csv")
    with open(p, "w") as f:
        f.write(dmy_text)
    parsed2 = bd.parse_daily_flow(p)
check_true("day-first parser returns a frame", parsed2 is not None)
check_true("day-first dates form the exact daily range (no month/day swap)",
           parsed2.date.reset_index(drop=True).equals(pd.Series(dmy_dates)))
check_true("negative flow becomes NaN", np.isnan(parsed2.flow_ML.iloc[0]))

# --- parser: annual inflow cross-check file ---------------------------------------
annual_text = ("# source: https://example.invalid/streamflow\n"
               "year,inflow_GL\n1990,300\n1991,250\n")
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "wc.csv")
    with open(p, "w") as f:
        f.write(annual_text)
    parsed3 = bd.parse_daily_flow(p)
check_true("annual file detected", parsed3 is not None
           and parsed3.attrs.get("kind") == "annual_inflow")
check("annual file rows", len(parsed3), 2)

# --- regional series construction ---------------------------------------------------
rng = np.random.default_rng(42)
years = np.arange(1975, 2025)
rows = []
for st, scale in (("A", 100.0), ("B", 10.0)):
    for y in years:
        level = 1.0 if y < 2000 else 0.5      # both stations halve after 2000
        rows.append({"station": st, "station_name": st, "water_year": int(y),
                     "total_ML": scale * level * (1 + 0.05 * rng.standard_normal()),
                     "days_missing": 0, "complete": True})
reg, stations, full_base = bd.build_regional(pd.DataFrame(rows))
pre = reg[reg.water_year < 2000].regional_anom_pct.mean()
post = reg[reg.water_year >= 2000].regional_anom_pct.mean()
check("regional pre-2000 anomaly ~ 0%", pre, 0.0, tol=3.0)
check("regional post-2000 anomaly ~ -50%", post, -50.0, tol=3.0)
check_true("big station does not dominate the % series",
           abs(post - (-50.0)) < 3.0)

# --- elasticity estimators -----------------------------------------------------------
P = np.linspace(400, 900, 40)
e_true = 2.5
Q = 1e-3 * P ** e_true                      # exact power law
ll = an.elasticity_loglog(P, Q)
check("log-log elasticity on exact power law", ll.slope, e_true, tol=1e-9)
enp = an.elasticity_nonparametric(P, Q)
check("non-parametric elasticity on power law", enp, e_true, tol=0.6)
check_true("non-parametric elasticity exceeds 1 for amplifying system", enp > 1.0)

print(f"\n{PASS} passed, {FAIL} failed")
raise SystemExit(1 if FAIL else 0)
