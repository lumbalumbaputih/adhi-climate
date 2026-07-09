"""test_project.py: pipeline-specific tests for transition-risk, run on
synthetic inputs so they need no downloads. CI runs this on every push.

Run:  python3 test_project.py
"""
import os
import tempfile

import numpy as np
import pandas as pd

import build_dataset as bd
import analysis as an

PASS = FAIL = 0


def check(name, cond):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"[PASS] {name}")
    else:
        FAIL += 1
        print(f"[FAIL] {name}")


# ----------------------------------------------------------- CER numbers ----
check("_num parses thousands separators", bd._num("1,234,567") == 1234567)
check("_num treats ' -   ' as missing", np.isnan(bd._num(" -   ")))
check("_num parses parenthesised negatives", bd._num("(123)") == -123)
check("_num passes plain floats", bd._num("0.951") == 0.951)

# ------------------------------------------------------------ column find ----
cols = ["Facility name", " Reported covered emissions ", "Baseline number",
        "MYMP baseline number"]
check("_find matches by keywords", bd._find(cols, "covered", "emissions")
      == " Reported covered emissions ")
check("_find excludes on request",
      bd._find(cols, "baseline", "number", exclude=("mymp",))
      == "Baseline number")

# --------------------------------------------------------- vintage parsing ----
old_csv = (
    "Facility name,State of operation,Responsible emitter,Baseline number,"
    "Type of baseline,Reported covered emissions,"
    "Australian carbon credit units surrendered,Net emissions number,"
    "Multi-year monitoring period start date (if applicable)\n"
    'Alpha Plant,WA,Alpha Pty Ltd,"1,000,000",Reported,"900,000", -   ,'
    '"900,000",-\n'
    'Beta Mine,WA,Beta Pty Ltd,"3,000,000",Calculated,"1,000,000", -   ,'
    '"1,000,000",1/07/2016\n'
    'Gamma Works,NSW,Gamma Pty Ltd,"500,000",Reported,"450,000", -   ,'
    '"450,000",-\n')
new_csv = (
    "Facility name,Responsible emitter,State/Territory of operation,ANZSIC,"
    "ERC,Baseline emissions number,Covered emissions,ACCUs surrendered,"
    "SMCs surrendered,SMCs issued,Net emissions number\n"
    'Alpha Plant,Alpha Pty Ltd,WA,Oil and gas extraction (070),0.951,'
    '"800,000","850,000","50,000", -   , -   ,"800,000"\n')
with tempfile.TemporaryDirectory() as td:
    p_old = os.path.join(td, "2016-17_synthetic.csv")
    p_new = os.path.join(td, "2023-24_synthetic.csv")
    open(p_old, "w").write(old_csv)
    open(p_new, "w").write(new_csv)
    df_old, _ = bd.parse_year_csv(p_old)
    df_new, _ = bd.parse_year_csv(p_new)

check("old vintage parses all rows", len(df_old) == 3)
check("old vintage year label is the start year",
      (df_old.year == 2016).all())
check("old vintage regime is original", (df_old.regime == "original").all())
check("MYMP start date flags the cumulative baseline",
      bool(df_old[df_old.facility == "Beta Mine"]
           .baseline_mymp_cumulative.iloc[0]))
check("plain '-' does not flag MYMP",
      not bool(df_old[df_old.facility == "Alpha Plant"]
               .baseline_mymp_cumulative.iloc[0]))
check("new vintage regime is reformed", (df_new.regime == "reformed").all())
check("new vintage reads SMC surrenders",
      df_new.accus_surrendered.iloc[0] == 50000)
check("new vintage baseline matched",
      df_new.baseline_t.iloc[0] == 800000)

# ------------------------------------------------------------- bucketing ----
check("sector bucket: LNG", bd.bucket_sector("Oil and gas extraction (070)")
      == "LNG / oil and gas")
check("sector bucket: alumina", bd.bucket_sector(
    "Basic non-ferrous metal manufacturing (213)") == "Alumina and metals")
check("parent map: Chevron", an.parent("CHEVRON AUSTRALIA PTY LTD")
      == "Chevron")
check("parent map: Rio via Hamersley", an.parent("Hamersley Iron Pty Ltd")
      == "Rio Tinto")
check("parent map: unknown -> Other", an.parent("Someone Else Pty Ltd")
      == "Other")

# ------------------------------------------------------------- scenarios ----
check("ceiling price grows from the 2025-26 anchor",
      abs(an.ceiling_price(2025) - 82.68) < 1e-9
      and an.ceiling_price(2027) > an.ceiling_price(2025))

# crossover arithmetic: baseline 1.0 declining 4.9%/yr, emissions flat 0.9:
# baseline drops below 0.9 when 1.0*(1-0.049)^n < 0.9 -> n=3 (0.860)
b0, e0 = 1_000_000.0, 900_000.0
cross = None
for y in an.PROJ_YEARS:
    b = b0 * (1 - an.DECLINE) ** (y - 2024)
    if e0 > b and cross is None:
        cross = y
check(f"crossover year arithmetic (got {cross})", cross == 2027)

print(f"\n{PASS} passed, {FAIL} failed")
raise SystemExit(1 if FAIL else 0)
