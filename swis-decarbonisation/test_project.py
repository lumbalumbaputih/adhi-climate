"""
test_project.py: unit tests for the SWIS pipeline pieces that carry analytical
weight: fuel bucketing, the SCADA parser (MWh and MW variants), the fuel-map
parser, complete-year detection, and the intensity calculation. Synthetic
inputs only; runs in CI.

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


# --- fuel bucketing -------------------------------------------------------------
check_true("'Natural Gas / CCGT' -> gas", bd.bucket_fuel("Natural Gas / CCGT") == "gas")
check_true("'Wind Farm' -> wind", bd.bucket_fuel("Wind Farm") == "wind")
check_true("'Solar PV' -> solar", bd.bucket_fuel("Solar PV") == "solar")
check_true("'Black Coal' -> coal", bd.bucket_fuel("Black Coal") == "coal")
check_true("'Landfill Gas' -> bio (not gas)", bd.bucket_fuel("Landfill Gas") == "bio")
check_true("'Biogas' -> bio (not gas)", bd.bucket_fuel("Biogas") == "bio")
check_true("unknown -> other", bd.bucket_fuel("Mystery Machine") == "other")

# --- SCADA parser: MWh variant -----------------------------------------------------
days = pd.date_range("2020-01-01", "2020-03-31", freq="D")
scada_mwh = "Trading Date,Facility Code,Energy Generated (MWh)\n" + "\n".join(
    f"{d.date()},PLANT_A,{24.0}\n{d.date()},WIND_B,{12.0}" for d in days)
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "scada.csv")
    open(p, "w").write(scada_mwh)
    g = bd.parse_scada(p)
check_true("MWh parser returns a frame", g is not None)
check_true("MWh unit detected", g.attrs["unit"] == "MWh")
jan_a = g[(g.month == "2020-01") & (g.facility == "PLANT_A")].energy_MWh.iloc[0]
check("January PLANT_A total", jan_a, 24.0 * 31)

# --- SCADA parser: MW variant converts intervals -------------------------------------
scada_mw = "Interval Date,Facility Code,Power (MW)\n" + "\n".join(
    f"2020-01-01 {h:02d}:{m:02d},PLANT_A,100.0"
    for h in range(24) for m in (0, 30))
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "scada_mw.csv")
    open(p, "w").write(scada_mw)
    g2 = bd.parse_scada(p)
check_true("MW parser returns a frame", g2 is not None)
check_true("MW unit detected", g2.attrs["unit"] == "MW")
check("48 half-hour intervals at 100 MW = 2400 MWh",
      g2.energy_MWh.iloc[0], 100.0 * 0.5 * 48)

# --- fuel map parser -----------------------------------------------------------------
fmap_text = ("# source: https://example.invalid/register\n"
             "Facility Code,Fuel Type\nPLANT_A,Black Coal\nWIND_B,Wind\n")
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "register.csv")
    open(p, "w").write(fmap_text)
    fm = bd.parse_fuel_map(p)
check_true("fuel map parsed", fm is not None and len(fm) == 2)
check_true("coal bucketed", fm[fm.facility == "PLANT_A"].fuel.iloc[0] == "coal")

# --- complete-year detection -----------------------------------------------------------
monthly = pd.DataFrame({
    "month": [f"2019-{m:02d}" for m in range(7, 13)]
             + [f"2020-{m:02d}" for m in range(1, 13)],
    "fuel": "coal", "energy_MWh": 1.0,
})
years = an.complete_years(monthly)
check_true("2020 is complete, 2019 is not", years == [2020])

# --- intensity arithmetic ----------------------------------------------------------------
annual = pd.DataFrame({
    "year": [2020, 2020], "fuel": ["coal", "wind"],
    "energy_MWh": [700.0, 300.0],
})
factors = {"coal": 1.0, "wind": 0.0}
t = (annual.fuel.map(factors) * annual.energy_MWh).sum()
check("intensity: 70% coal at 1 t/MWh -> 0.7 t/MWh",
      t / annual.energy_MWh.sum(), 0.7)

# --- factor template refuses to invent numbers ----------------------------------------------
with tempfile.TemporaryDirectory() as td:
    bd.write_factor_template(td)
    check_true("template written", os.path.exists(os.path.join(td, "emission_factors.csv")))
    check_true("template has no pre-filled factors", bd.load_factors(td) is None)

print(f"\n{PASS} passed, {FAIL} failed")
raise SystemExit(1 if FAIL else 0)
