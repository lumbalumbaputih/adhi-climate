"""fire_indices.py: the fire-weather index chain, implemented from the
primary literature and unit-tested in test_fire_indices.py.

Three pieces, in causal order:

1. Keetch-Byram Drought Index, KBDI (Keetch & Byram 1968, USDA Forest
   Service Research Paper SE-38; SI form as used by Finkele et al. 2006,
   Aust. Met. Mag. 55). A running soil-moisture deficit in mm, 0 (saturated)
   to 203.2 (bone dry). Each day it grows by an evapotranspiration term
   driven by the day's maximum temperature and the site's mean annual
   rainfall, and shrinks by effective rainfall (each rain event's first
   5.08 mm is intercepted and does not count).

2. Drought Factor, DF (Noble, Bary & Gill 1980, Aust. J. Ecol. 5, equation
   for McArthur's Mark 5 meter). Converts the deficit plus the recency and
   size of the last rain into fuel availability on a 0-10 scale:

       DF = 0.191 (I + 104) (N + 1)^1.5 / (3.52 (N + 1)^1.5 + P - 1)

   capped at 10, where I is KBDI (mm), N is days since rain and P the last
   rain amount (mm). Following common practice, "rain" means a day with
   2 mm or more; P is that event's total and N counts days since it ended.

3. Forest Fire Danger Index, FFDI (Noble, Bary & Gill 1980, the standard
   curve fit to McArthur's Mark 5 meter):

       FFDI = 2.0 exp(-0.450 + 0.987 ln DF - 0.0345 H + 0.0338 T + 0.0234 V)

   with H relative humidity (%), T air temperature (C), V wind speed (km/h),
   conventionally the 15:00 local observations. Noble et al. calibrate the
   scale so the Black Friday 1939 conditions (T=40, H=15, V=55 km/h, DF=10)
   give FFDI of about 100; test_fire_indices.py checks we reproduce that.

Operational Australia replaced FFDI with the AFDRS in 2022; FFDI remains the
research standard for climate-trend work and is what this project computes.
"""
import math

import numpy as np

KBDI_MAX = 203.2      # mm, the full soil-moisture store (8 inches)
INTERCEPT = 5.08      # mm intercepted per rain event (0.2 inches)
RAIN_EVENT_MM = 2.0   # a day with >= this much rain counts as rain for DF


def kbdi_series(tmax, rain, mean_annual_rain, q0=KBDI_MAX / 2):
    """Daily KBDI (mm deficit) from arrays of daily max temperature (C) and
    daily rainfall (mm). Starts at q0 (default: half store); the first year
    should be treated as spin-up and discarded by the caller.
    """
    tmax = np.asarray(tmax, float)
    rain = np.asarray(rain, float)
    q = float(q0)
    intercept_left = 0.0      # remaining interception for the current event
    out = np.empty(len(tmax))
    denom = 1.0 + 10.88 * math.exp(-0.001736 * float(mean_annual_rain))
    for i in range(len(tmax)):
        r = rain[i] if np.isfinite(rain[i]) else 0.0
        if r > 0:
            take = min(r, intercept_left if intercept_left > 0 else INTERCEPT)
            if intercept_left <= 0:          # new event starts today
                intercept_left = INTERCEPT
            eff = max(0.0, r - intercept_left)
            intercept_left = max(0.0, intercept_left - r)
            q = max(0.0, q - eff)
        else:
            intercept_left = 0.0             # event over; next rain starts fresh
        t = tmax[i] if np.isfinite(tmax[i]) else 20.0
        et = ((KBDI_MAX - q) * (0.968 * math.exp(0.0875 * t + 1.5552) - 8.30)
              / 1000.0) / denom
        q = min(KBDI_MAX, max(0.0, q + max(0.0, et)))
        out[i] = q
    return out


def drought_factor_series(kbdi, rain):
    """Daily Noble et al. (1980) drought factor (0-10) from the KBDI series
    and daily rainfall. N = days since the end of the last rain event
    (>= RAIN_EVENT_MM), P = that event's total rainfall."""
    kbdi = np.asarray(kbdi, float)
    rain = np.asarray(rain, float)
    out = np.empty(len(kbdi))
    days_since = 30.0        # long-dry start; spin-up discarded by caller
    last_event = 0.0
    in_event = False
    event_total = 0.0
    for i in range(len(kbdi)):
        r = rain[i] if np.isfinite(rain[i]) else 0.0
        if r >= RAIN_EVENT_MM:
            event_total = event_total + r if in_event else r
            in_event = True
            days_since = 0.0
            last_event = event_total
        else:
            in_event = False
            event_total = 0.0
            days_since += 1.0
        n, p = days_since, max(last_event, 1.0)
        df = (0.191 * (kbdi[i] + 104.0) * (n + 1.0) ** 1.5
              / (3.52 * (n + 1.0) ** 1.5 + p - 1.0))
        out[i] = min(10.0, max(0.0, df))
    return out


def ffdi(df, t, rh, wind):
    """McArthur Mark 5 FFDI (Noble et al. 1980). Vectorised; wind in km/h."""
    df = np.asarray(df, float)
    t = np.asarray(t, float)
    rh = np.asarray(rh, float)
    wind = np.asarray(wind, float)
    df_safe = np.clip(df, 1e-6, 10.0)
    return 2.0 * np.exp(-0.450 + 0.987 * np.log(df_safe)
                        - 0.0345 * rh + 0.0338 * t + 0.0234 * wind)
