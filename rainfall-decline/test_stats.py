"""
test_stats.py — unit tests for stats_utils, validated against known values.

Run:  python3 test_stats.py        (exits non-zero on any failure)

Hand-rolled statistics are only credible if proven correct, so every function
is checked against an analytically known or textbook value.
"""
import math
import numpy as np
import stats_utils as s

PASS = 0
FAIL = 0


def check(name, got, want, tol=1e-4):
    global PASS, FAIL
    ok = abs(got - want) <= tol
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got:.6g}, want {want:.6g}")
    PASS += ok
    FAIL += (not ok)


# --- OLS regression (classic example: slope 0.6, intercept 2.2, r 0.774597) ---
res = s.linregress([1, 2, 3, 4, 5], [2, 4, 5, 4, 5])
check("linregress slope", res.slope, 0.6)
check("linregress intercept", res.intercept, 2.2)
check("linregress r", res.rvalue, 0.7745967)
check("linregress r^2", res.r_squared, 0.6)

# perfect line y = 2x + 1
res2 = s.linregress([0, 1, 2, 3, 4], [1, 3, 5, 7, 9])
check("perfect line slope", res2.slope, 2.0)
check("perfect line intercept", res2.intercept, 1.0)
check("perfect line r", res2.rvalue, 1.0)

# --- Pearson correlation ---
r, p, n = s.pearsonr([1, 2, 3, 4, 5], [2, 4, 5, 4, 5])
check("pearson r", r, 0.7745967)
r2, _, _ = s.pearsonr([1, 2, 3, 4], [4, 3, 2, 1])
check("pearson r (anti)", r2, -1.0)

# --- Student-t two-sided p-value: t*=2.024, df=38 -> p ~ 0.05 ---
check("t_pvalue(2.024,38)", s.t_pvalue_two_sided(2.024, 38), 0.05, tol=2e-3)
check("t_critical(38)", s.t_critical(38, 0.05), 2.024, tol=2e-3)
# normal two-sided p at z=1.96 -> 0.05
check("normal_pvalue(1.96)", s.normal_pvalue_two_sided(1.96), 0.05, tol=2e-3)

# --- Mann-Kendall: strictly increasing 1..10 -> S = n(n-1)/2 = 45, tau = 1 ---
mk = s.mann_kendall(list(range(1, 11)))
check("MK S (monotone up)", mk.S, 45)
check("MK tau (monotone up)", mk.tau, 1.0)
assert mk.trend == "increasing", "MK should report increasing"
print("[PASS] MK trend label = increasing")
PASS += 1
mk2 = s.mann_kendall(list(range(10, 0, -1)))
check("MK S (monotone down)", mk2.S, -45)

# --- Sen's slope: y = 3x + 7 -> slope 3 ---
sl, ic = s.sens_slope([0, 1, 2, 3, 4, 5], [7, 10, 13, 16, 19, 22])
check("Sen slope", sl, 3.0)
check("Sen intercept", ic, 7.0)

# --- Pettitt: monotone [1,2,3,4] -> cp_index 2, K 4 (hand-computed) ---
pt = s.pettitt([1, 2, 3, 4])
check("Pettitt cp (monotone)", pt.cp_index, 2)
check("Pettitt K (monotone)", pt.K, 4.0)

# clear step: 30 values at 0 then 30 at 10 -> change point at 30, tiny p
step = [0.0] * 30 + [10.0] * 30
pt2 = s.pettitt(step)
check("Pettitt cp (step at 30)", pt2.cp_index, 30)
assert pt2.pvalue < 0.001, f"step change should be highly significant, got p={pt2.pvalue}"
print(f"[PASS] Pettitt step p < 0.001 (p={pt2.pvalue:.2e})")
PASS += 1

print(f"\n{PASS} passed, {FAIL} failed")
raise SystemExit(1 if FAIL else 0)
