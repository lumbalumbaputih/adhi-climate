"""test_fire_indices.py: validate the fire-weather index chain against the
published equations and their documented behaviour.

The FFDI checks are the strong ones: Noble et al. (1980) state their curve
fit reproduces McArthur's meter, whose scale was set so the Black Friday
1939 conditions score about 100. The KBDI/DF checks pin the documented
invariants (bounds, monotonic drying, rain resets, interception) that the
recursions must satisfy.

Run:  python3 test_fire_indices.py
"""
import numpy as np

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


# ---------------------------------------------------------------- FFDI ----
# Black Friday 1939 calibration point (Noble et al. 1980): T=40 C, RH=15%,
# wind 55 km/h, DF=10 -> FFDI approx 100.
v = float(fi.ffdi(10, 40, 15, 55))
check(f"FFDI Black Friday calibration ~100 (got {v:.1f})", 95 <= v <= 110)

# Hand-computed from the published equation (independent arithmetic):
# DF=10, T=35, H=10, V=35: exponent = -0.450 + 0.987*ln(10) - 0.345
#   + 1.183 + 0.819 = 3.4797; FFDI = 2*exp(3.4797) = 64.9
v = float(fi.ffdi(10, 35, 10, 35))
check(f"FFDI hand-computed case 64.9 (got {v:.1f})", abs(v - 64.9) < 0.5)

# A mild winter day should be a low FFDI: DF=3, T=15, H=70, V=10
v = float(fi.ffdi(3, 15, 70, 10))
check(f"FFDI mild-day case is low (got {v:.2f})", 0 < v < 3)

# Monotonicity: hotter, drier, windier, drier fuel -> higher FFDI
base = float(fi.ffdi(5, 30, 30, 20))
check("FFDI rises with temperature", float(fi.ffdi(5, 35, 30, 20)) > base)
check("FFDI falls with humidity", float(fi.ffdi(5, 30, 50, 20)) < base)
check("FFDI rises with wind", float(fi.ffdi(5, 30, 30, 40)) > base)
check("FFDI rises with drought factor", float(fi.ffdi(8, 30, 30, 20)) > base)

# ---------------------------------------------------------------- KBDI ----
# 100 bone-dry hot days from half store: deficit must rise monotonically
# and stay inside [0, 203.2].
q = fi.kbdi_series(np.full(100, 35.0), np.zeros(100), 800.0)
check("KBDI monotonic through a dry spell", np.all(np.diff(q) >= 0))
check("KBDI bounded above", q.max() <= fi.KBDI_MAX + 1e-9)

# A huge storm empties the deficit (bar the 5.08 mm interception).
q = fi.kbdi_series([30, 30, 30], [0, 0, 150], 800.0, q0=100.0)
check(f"KBDI collapses after 150 mm storm (got {q[-1]:.1f})", q[-1] < 5)

# Interception: 4 mm of rain (< 5.08) must not reduce the deficit.
q_dry = fi.kbdi_series([30, 30], [0, 0], 800.0, q0=100.0)
q_wet = fi.kbdi_series([30, 30], [0, 4.0], 800.0, q0=100.0)
check("KBDI ignores sub-interception rain", abs(q_dry[-1] - q_wet[-1]) < 1e-6)

# Hotter days dry the soil faster.
q_cool = fi.kbdi_series(np.full(30, 20.0), np.zeros(30), 800.0, q0=50.0)
q_hot = fi.kbdi_series(np.full(30, 40.0), np.zeros(30), 800.0, q0=50.0)
check("KBDI grows faster when hotter", q_hot[-1] > q_cool[-1])

# Higher mean annual rainfall means denser vegetation and therefore MORE
# evapotranspiration in Keetch-Byram's model, so the deficit grows FASTER
# in a wetter climate (Keetch & Byram 1968, the 1 + 10.88 exp(-0.001736 R)
# annual-rainfall damping term sits in the denominator).
q_arid = fi.kbdi_series(np.full(30, 30.0), np.zeros(30), 300.0, q0=50.0)
q_wetc = fi.kbdi_series(np.full(30, 30.0), np.zeros(30), 1200.0, q0=50.0)
check("KBDI dries faster in a wetter climate (KB68 vegetation term)",
      q_wetc[-1] > q_arid[-1])

# ------------------------------------------------------- drought factor ----
# Long dry + high KBDI must pin DF at the cap of 10.
df = fi.drought_factor_series(np.full(60, 180.0), np.zeros(60))
check(f"DF reaches cap 10 in long dry (got {df[-1]:.2f})", abs(df[-1] - 10) < 1e-9)

# Fresh heavy rain knocks DF down, then it recovers as days pass.
rain = np.zeros(30)
rain[10] = 40.0
df = fi.drought_factor_series(np.full(30, 100.0), rain)
check("DF drops on the rain day", df[10] < df[9])
check("DF recovers after the rain", df[29] > df[10])

# DF never leaves [0, 10].
rng = np.random.default_rng(42)
df = fi.drought_factor_series(rng.uniform(0, 203, 500), rng.exponential(2, 500))
check("DF bounded in [0, 10]", df.min() >= 0 and df.max() <= 10)

# Noble et al. equation spot value, independent arithmetic: I=100, N=20,
# P=10 (last rain 10 mm, 20 days ago): (N+1)^1.5 = 96.234;
# DF = 0.191*204*96.234 / (3.52*96.234 + 9) = 3749.8 / 347.7 = 10.78 -> cap 10.
rain = np.zeros(22)
rain[0] = 10.0
kb = np.full(22, 100.0)
df = fi.drought_factor_series(kb, rain)
check(f"DF spot value capped at 10 (got {df[20]:.2f})", abs(df[20] - 10.0) < 1e-9)

# Same but wetter event P=50, N=5: (N+1)^1.5=14.697;
# DF = 0.191*204*14.697/(3.52*14.697+49) = 572.7/100.7 = 5.687
rain = np.zeros(7)
rain[0] = 50.0
kb = np.full(7, 100.0)
df = fi.drought_factor_series(kb, rain)
check(f"DF spot value 5.69 (got {df[5]:.2f})", abs(df[5] - 5.687) < 0.05)

print(f"\n{PASS} passed, {FAIL} failed")
raise SystemExit(1 if FAIL else 0)
