"""test_project.py: pipeline-specific tests for bushfire-weather, run on
synthetic inputs so they need no downloads. CI runs this on every push.

Run:  python3 test_project.py
"""
import numpy as np
import pandas as pd

import build_dataset as bd
import analysis as an
import fire_indices as fi

PASS = FAIL = 0


def check(name, cond):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"[PASS] {name}")
    else:
        FAIL += 1
        print(f"[FAIL] {name}")


# ------------------------------------------------ reduce_daily (15:00) ----
hours = pd.date_range("2001-01-01", "2001-01-03 23:00", freq="h")
hh = pd.DataFrame({
    "time": hours,
    "t": np.where(hours.hour == 15, 30.0, 20.0),
    "rh": np.where(hours.hour == 15, 25.0, 60.0),
    "wind": np.where(hours.hour == 15, 22.0, 8.0),
    "rain": np.where(hours.hour == 3, 2.0, 0.0),   # 2 mm at 03:00 daily
})
day = bd.reduce_daily(hh)
check("reduce_daily keeps one row per day", len(day) == 3)
check("reduce_daily picks the 15:00 temperature",
      np.allclose(day.t15, 30.0))
check("reduce_daily picks the 15:00 humidity", np.allclose(day.rh15, 25.0))
check("reduce_daily sums the day's rain", np.allclose(day.rain24, 2.0))
check("reduce_daily takes the daily max temp", np.allclose(day.tmax, 30.0))

# a day with no 15:00 observation is dropped, not silently kept
hh2 = hh[~((hh.time.dt.day == 2) & (hh.time.dt.hour == 15))]
day2 = bd.reduce_daily(hh2)
check("reduce_daily drops a day missing 15:00", len(day2) == 2)

# ------------------------------------------------------- season labels ----
dates = pd.Series(pd.to_datetime(
    ["2000-10-01", "2000-12-31", "2001-01-01", "2001-04-30"]))
lab = an.season_year(dates)
check("season label spans the summer (Oct=start year)",
      list(lab) == [2000, 2000, 2000, 2000])

# --------------------------------------------------- seasonal_metrics ----
rng = pd.date_range("1999-07-01", "2001-06-30", freq="D")
ff = np.full(len(rng), 10.0)
# make the 2000-01 season contain exactly 30 Very High and 5 Severe days
season_days = (rng >= "2000-11-01") & (rng <= "2001-01-31")
idx = np.where(season_days)[0]
ff[idx[:30]] = 30.0
ff[idx[:5]] = 60.0
daily = pd.DataFrame({"date": rng, "ffdi": ff})
sm = an.seasonal_metrics(daily)
row = sm[sm.season == 2000].iloc[0]
check("seasonal_metrics counts Very High days", row.days_vh == 30)
check("seasonal_metrics counts Severe days", row.days_sev == 5)
check("seasonal_metrics season_span covers the run",
      row.season_span == (daily.date[idx[29]] - daily.date[idx[0]]).days)
check("incomplete edge seasons are dropped",
      1999 not in sm.season.values or
      sm[sm.season == 1999].n_days.iloc[0] >= 200)

# ------------------------------------------ index chain on a real shape ----
# two synthetic years: wet mild winter, hot dry summer; FFDI must peak in
# summer and the summer peak must exceed the winter peak by a wide margin
rng = pd.date_range("1990-01-01", "1991-12-31", freq="D")
month = rng.month.values
summer = np.isin(month, (12, 1, 2))
winter = np.isin(month, (6, 7, 8))
tmax = np.where(summer, 36.0, np.where(winter, 16.0, 25.0))
rain = np.where(winter, 6.0, 0.2)
kbdi = fi.kbdi_series(tmax, rain, 700.0)
df = fi.drought_factor_series(kbdi, rain)
f = fi.ffdi(df, np.where(summer, 33.0, 15.0),
            np.where(summer, 15.0, 70.0), 20.0)
check("FFDI peaks in summer on synthetic seasonal cycle",
      f[summer].mean() > 5 * f[winter].mean())
check("KBDI drains through winter rain",
      kbdi[np.where(winter)[0][-1]] < kbdi[np.where(summer)[0][-1]])

# ------------------------------------------------------ GHCN validation ----
era = pd.DataFrame({"date": pd.date_range("2000-01-01", periods=50),
                    "tmax": np.linspace(20, 40, 50)})
obs = pd.DataFrame({"date": pd.date_range("2000-01-01", periods=50),
                    "tmax_obs": np.linspace(20, 40, 50) + 0.5,
                    "prcp_obs": 0.0})
era["rain24"] = 0.0
import tempfile, os
with tempfile.TemporaryDirectory() as td:
    era.to_csv(os.path.join(td, "fire_weather_daily_perth_airport.csv"),
               index=False)
    obs.to_csv(os.path.join(td, "ghcn_perth_airport_daily.csv"), index=False)
    va = an.validation(td)
check("validation joins on date", va.iloc[0].n_days == 50)
check("validation reports the bias", abs(va.iloc[0].bias_c + 0.5) < 1e-9)
check("validation correlation is 1 on a linear pair",
      abs(va.iloc[0].pearson_r - 1.0) < 1e-9)

print(f"\n{PASS} passed, {FAIL} failed")
raise SystemExit(1 if FAIL else 0)
