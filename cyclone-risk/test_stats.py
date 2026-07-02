"""
test_stats.py: validate stats_utils against known textbook values.
Run: python3 test_stats.py
These checks are what make the from-scratch statistics trustworthy as a
substitute for scipy.stats.
"""
import math
import numpy as np
import stats_utils as su


def approx(a, b, tol=1e-3):
    return abs(a - b) <= tol * max(1.0, abs(b))


def test_t_pvalue():
    # Two-tailed t critical values (standard t-tables):
    # df=4,  t=2.776 -> p=0.05 ;  df=10, t=2.228 -> p=0.05
    # df=20, t=2.086 -> p=0.05 ;  df=9,  t=4.241 -> p=0.00217 (Anscombe I)
    assert approx(su.t_pvalue_two_sided(2.776, 4), 0.05, 1e-2), su.t_pvalue_two_sided(2.776, 4)
    assert approx(su.t_pvalue_two_sided(2.228, 10), 0.05, 1e-2), su.t_pvalue_two_sided(2.228, 10)
    assert approx(su.t_pvalue_two_sided(2.086, 20), 0.05, 1e-2), su.t_pvalue_two_sided(2.086, 20)
    print("PASS t_pvalue: df4@2.776=%.4f df10@2.228=%.4f df20@2.086=%.4f"
          % (su.t_pvalue_two_sided(2.776, 4), su.t_pvalue_two_sided(2.228, 10),
             su.t_pvalue_two_sided(2.086, 20)))


def test_normal_pvalue():
    # P(|Z|>1.96)=0.05 ; P(|Z|>2.576)=0.01 ; P(|Z|>1.645)=0.10
    assert approx(su.normal_pvalue_two_sided(1.95996), 0.05, 1e-3)
    assert approx(su.normal_pvalue_two_sided(2.57583), 0.01, 1e-3)
    assert approx(su.normal_pvalue_two_sided(1.64485), 0.10, 1e-3)
    print("PASS normal_pvalue: 1.96->%.4f 2.576->%.4f" %
          (su.normal_pvalue_two_sided(1.95996), su.normal_pvalue_two_sided(2.57583)))


def test_linregress_anscombe():
    # Anscombe quartet I: known slope=0.5001, intercept=3.0001, r=0.8164,
    # r^2=0.6665, slope p-value=0.00217 (df=9)
    x = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
    y = [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]
    res = su.linregress(x, y)
    assert approx(res.slope, 0.5001, 1e-3), res.slope
    assert approx(res.intercept, 3.0001, 1e-3), res.intercept
    assert approx(res.rvalue, 0.8164, 1e-3), res.rvalue
    assert approx(res.r_squared, 0.6665, 1e-3), res.r_squared
    assert approx(res.pvalue, 0.00217, 5e-2), res.pvalue
    print("PASS linregress (Anscombe I): %s" % res)


def test_pearson():
    # Same data -> r=0.8164, p=0.00217
    x = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
    y = [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]
    r, p, n = su.pearsonr(x, y)
    assert approx(r, 0.8164, 1e-3), r
    assert approx(p, 0.00217, 5e-2), p
    print("PASS pearsonr: r=%.4f p=%.5f n=%d" % (r, p, n))


def test_mann_kendall_monotonic():
    # Strictly increasing n=10: S=45, var=125, z=(45-1)/sqrt(125)=3.9352,
    # two-sided p=8.33e-5
    y = np.arange(10, dtype=float)
    res = su.mann_kendall(y)
    assert res.S == 45, res.S
    assert approx(res.z, 3.9352, 1e-3), res.z
    assert approx(res.pvalue, 8.33e-5, 5e-2), res.pvalue
    assert res.trend == "increasing"
    assert approx(res.tau, 1.0, 1e-9), res.tau
    print("PASS mann_kendall (monotonic up): %s" % res)


def test_mann_kendall_flat():
    # No trend in a symmetric zig-zag
    y = np.array([1.0, 2, 1, 2, 1, 2, 1, 2, 1, 2])
    res = su.mann_kendall(y)
    assert res.trend == "no trend", res
    print("PASS mann_kendall (flat): %s" % res)


def test_sens_slope():
    # Perfect line y=2x+1 -> Sen slope exactly 2
    x = np.arange(20, dtype=float)
    y = 2 * x + 1
    s, b = su.sens_slope(x, y)
    assert approx(s, 2.0, 1e-9), s
    assert approx(b, 1.0, 1e-9), b
    print("PASS sens_slope: slope=%.4f intercept=%.4f" % (s, b))


def test_pettitt():
    # Monotone [1,2,3,4]: cp_index 2, K 4 (hand-computed); and a clear step of
    # 30 zeros then 30 tens: change point at 30, highly significant
    pt = su.pettitt([1, 2, 3, 4])
    assert pt.cp_index == 2 and approx(pt.K, 4.0, 1e-9), pt
    pt2 = su.pettitt([0.0] * 30 + [10.0] * 30)
    assert pt2.cp_index == 30 and pt2.pvalue < 0.001, pt2
    print("PASS pettitt: monotone cp=2 K=4; step cp=30 p=%.2e" % pt2.pvalue)


def test_mann_kendall_tfpw():
    # Strictly linear: zero residual variance, prewhitening skipped
    tf = su.mann_kendall_tfpw(2 * np.arange(20.0) + 1)
    assert not tf.prewhitened and tf.trend == "increasing" and tf.r1 == 0.0, tf
    # White noise (fixed legacy seed): r1 below the 1.96/sqrt(n) gate, result
    # must equal plain Mann-Kendall
    w = np.random.RandomState(3).normal(size=50)
    tw = su.mann_kendall_tfpw(w)
    mw = su.mann_kendall(w)
    assert not tw.prewhitened and abs(tw.pvalue - mw.pvalue) < 1e-12, tw
    # AR(1) rho=0.8 (fixed legacy seed): autocorrelation detected and filtered
    rng = np.random.RandomState(1)
    e = rng.normal(size=200)
    ar = np.zeros(200)
    for i in range(1, 200):
        ar[i] = 0.8 * ar[i - 1] + e[i]
    ta = su.mann_kendall_tfpw(ar[100:])
    assert ta.prewhitened and approx(ta.r1, 0.6082, 1e-3), ta
    print("PASS mann_kendall_tfpw: linear skip, white-noise skip, AR(1) r1=%.3f filtered" % ta.r1)


if __name__ == "__main__":
    test_t_pvalue()
    test_normal_pvalue()
    test_linregress_anscombe()
    test_pearson()
    test_mann_kendall_monotonic()
    test_mann_kendall_flat()
    test_sens_slope()
    test_pettitt()
    test_mann_kendall_tfpw()
    print("\nALL TESTS PASSED")
