"""
stats_utils.py: self-contained statistics for the adhi-climate analyses.

Why this exists: the analyses deliberately depend only on numpy/pandas/
matplotlib/netCDF4 so they reproduce on any machine without a heavy scientific
stack. The statistics needed (OLS regression with a significance test, Pearson
correlation, the non-parametric Mann-Kendall trend test with an optional
trend-free prewhitening variant for autocorrelated series, Sen's slope, and
the Pettitt change-point test) are implemented here from first principles and
validated against known textbook values in test_stats.py.

This file is intentionally duplicated, byte for byte, in cyclone-risk/ and
rainfall-decline/ so each project stays self-contained. CI checks that the two
copies are identical; edit one, then copy it over the other.

All p-values are two-sided. Results have been checked to agree with
scipy.stats to ~1e-6.
"""
import math
import numpy as np

# ---------------------------------------------------------------------------
# Special functions (Numerical Recipes incomplete beta -> Student-t p-value)
# ---------------------------------------------------------------------------

def _betacf(a, b, x):
    MAXIT, EPS, FPMIN = 300, 3.0e-14, 1.0e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < FPMIN:
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN:
            d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < EPS:
            break
    return h


def _betai(a, b, x):
    """Regularised incomplete beta function I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    bt = math.exp(lbeta + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def t_pvalue_two_sided(t, df):
    """Two-sided p-value for a Student-t statistic with df degrees of freedom."""
    if df <= 0:
        return float("nan")
    t = abs(float(t))
    x = df / (df + t * t)
    return _betai(0.5 * df, 0.5, x)


def normal_pvalue_two_sided(z):
    """Two-sided p-value for a standard-normal z statistic."""
    return math.erfc(abs(float(z)) / math.sqrt(2.0))


def t_critical(df, alpha=0.05):
    """Two-sided critical t* with P(|T| > t*) = alpha. Found by bisection on the
    (monotone) two-sided p-value, so no scipy needed. df=38,alpha=.05 -> 2.024."""
    lo, hi = 0.0, 1000.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if t_pvalue_two_sided(mid, df) > alpha:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# Regression / correlation
# ---------------------------------------------------------------------------

class LinregressResult:
    def __init__(self, slope, intercept, r, pvalue, stderr, n):
        self.slope = slope
        self.intercept = intercept
        self.rvalue = r
        self.r_squared = r * r
        self.pvalue = pvalue
        self.stderr = stderr
        self.n = n

    def __repr__(self):
        return (f"Linregress(slope={self.slope:.5g}, intercept={self.intercept:.5g}, "
                f"r={self.rvalue:.4f}, r2={self.r_squared:.4f}, "
                f"p={self.pvalue:.4g}, stderr={self.stderr:.4g}, n={self.n})")


def linregress(x, y):
    """Ordinary least squares y = slope*x + intercept.

    Returns slope, intercept, Pearson r, two-sided p-value for H0: slope=0
    (Student-t, df=n-2), and the standard error of the slope. Matches
    scipy.stats.linregress.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    n = x.size
    if n < 3:
        raise ValueError("Need at least 3 points for regression")
    xm, ym = x.mean(), y.mean()
    dx, dy = x - xm, y - ym
    ssxx = np.sum(dx * dx)
    ssyy = np.sum(dy * dy)
    ssxy = np.sum(dx * dy)
    slope = ssxy / ssxx
    intercept = ym - slope * xm
    r = ssxy / math.sqrt(ssxx * ssyy) if ssyy > 0 else 0.0
    df = n - 2
    # residual standard error of the slope
    ss_res = ssyy - slope * ssxy
    s2 = ss_res / df if df > 0 else float("nan")
    stderr = math.sqrt(s2 / ssxx) if ssxx > 0 else float("nan")
    if stderr > 0:
        t = slope / stderr
        p = t_pvalue_two_sided(t, df)
    else:
        p = float("nan")
    return LinregressResult(slope, intercept, r, p, stderr, n)


def pearsonr(x, y):
    """Pearson correlation r and two-sided p-value (Student-t, df=n-2)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    n = x.size
    if n < 3:
        raise ValueError("Need at least 3 points for correlation")
    xm, ym = x.mean(), y.mean()
    dx, dy = x - xm, y - ym
    r = np.sum(dx * dy) / math.sqrt(np.sum(dx * dx) * np.sum(dy * dy))
    r = max(-1.0, min(1.0, float(r)))
    df = n - 2
    if abs(r) >= 1.0:
        p = 0.0
    else:
        t = r * math.sqrt(df / (1.0 - r * r))
        p = t_pvalue_two_sided(t, df)
    return r, p, n


# ---------------------------------------------------------------------------
# Non-parametric trend: Mann-Kendall + Sen's slope
# ---------------------------------------------------------------------------

class MannKendallResult:
    def __init__(self, trend, S, z, pvalue, n, tau):
        self.trend = trend
        self.S = S
        self.z = z
        self.pvalue = pvalue
        self.n = n
        self.tau = tau

    def __repr__(self):
        return (f"MannKendall(trend={self.trend!r}, S={self.S}, z={self.z:.4f}, "
                f"p={self.pvalue:.4g}, tau={self.tau:.4f}, n={self.n})")


def mann_kendall(y, alpha=0.05):
    """Mann-Kendall monotonic trend test with tie correction and continuity
    correction. y is ordered by time. Returns trend direction, S, z, two-sided
    p-value (normal approximation), Kendall's tau, and n.
    """
    y = np.asarray(y, dtype=float)
    y = y[np.isfinite(y)]
    n = y.size
    if n < 4:
        raise ValueError("Need at least 4 points for Mann-Kendall")
    # S statistic
    S = 0
    for k in range(n - 1):
        S += np.sum(np.sign(y[k + 1:] - y[k]))
    S = int(S)
    # variance with tie correction
    unique, counts = np.unique(y, return_counts=True)
    tie_term = np.sum(counts * (counts - 1) * (2 * counts + 5))
    var_s = (n * (n - 1) * (2 * n + 5) - tie_term) / 18.0
    # continuity-corrected z
    if S > 0:
        z = (S - 1) / math.sqrt(var_s)
    elif S < 0:
        z = (S + 1) / math.sqrt(var_s)
    else:
        z = 0.0
    p = normal_pvalue_two_sided(z)
    tau = S / (0.5 * n * (n - 1))
    if p < alpha and S > 0:
        trend = "increasing"
    elif p < alpha and S < 0:
        trend = "decreasing"
    else:
        trend = "no trend"
    return MannKendallResult(trend, S, z, p, n, tau)


class TFPWResult:
    def __init__(self, mk, r1, prewhitened, sen):
        self.mk = mk                  # MannKendallResult on the (possibly) prewhitened series
        self.trend = mk.trend
        self.pvalue = mk.pvalue
        self.tau = mk.tau
        self.n = mk.n
        self.r1 = r1                  # lag-1 autocorrelation of the detrended series
        self.prewhitened = prewhitened
        self.sen = sen                # Sen's slope used for detrending (per step)

    def __repr__(self):
        return (f"TFPW(trend={self.trend!r}, p={self.pvalue:.4g}, r1={self.r1:+.3f}, "
                f"prewhitened={self.prewhitened}, n={self.n})")


def mann_kendall_tfpw(y, alpha=0.05):
    """Mann-Kendall with trend-free prewhitening (Yue et al. 2002).

    Serial correlation inflates the variance of the MK statistic and makes
    p-values overconfident. TFPW: (1) remove the Sen's-slope trend, (2) measure
    the lag-1 autocorrelation r1 of the residuals, (3) if r1 is significant at
    the 5% level (|r1| > 1.96/sqrt(n)), filter the AR(1) component out of the
    residuals, add the trend back, and run MK on that series; otherwise run
    plain MK on the original series.

    Assumes (approximately) equally spaced observations; a few missing years
    dropped from an annual series are tolerable, long gaps are not.
    """
    y = np.asarray(y, dtype=float)
    y = y[np.isfinite(y)]
    n = y.size
    if n < 4:
        raise ValueError("Need at least 4 points for Mann-Kendall")
    t = np.arange(n, dtype=float)
    b, _ = sens_slope(t, y)
    resid = y - b * t
    dr = resid - resid.mean()
    denom = np.sum(dr * dr)
    if denom <= 0:
        # strictly linear series: no residual variance, nothing to prewhiten
        mk = mann_kendall(y, alpha=alpha)
        return TFPWResult(mk, 0.0, False, b)
    r1 = float(np.sum(dr[1:] * dr[:-1]) / denom)
    if abs(r1) <= 1.96 / math.sqrt(n):
        mk = mann_kendall(y, alpha=alpha)
        return TFPWResult(mk, r1, False, b)
    filtered = resid[1:] - r1 * resid[:-1]
    blended = filtered + b * t[1:]
    mk = mann_kendall(blended, alpha=alpha)
    return TFPWResult(mk, r1, True, b)


def sens_slope(x, y):
    """Theil-Sen slope: median of pairwise slopes. Robust to outliers.
    Returns (slope, intercept) where intercept = median(y) - slope*median(x).
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    n = x.size
    slopes = []
    for i in range(n - 1):
        dxi = x[i + 1:] - x[i]
        dyi = y[i + 1:] - y[i]
        ok = dxi != 0
        slopes.extend((dyi[ok] / dxi[ok]).tolist())
    slope = float(np.median(slopes))
    intercept = float(np.median(y) - slope * np.median(x))
    return slope, intercept


# ---------------------------------------------------------------------------
# Change-point detection: Pettitt test (non-parametric, single change point)
# ---------------------------------------------------------------------------

class PettittResult:
    def __init__(self, cp_index, K, pvalue, n):
        self.cp_index = cp_index   # 1-indexed split: segments x[:cp] and x[cp:]
        self.K = K
        self.pvalue = pvalue
        self.n = n

    def __repr__(self):
        return (f"Pettitt(cp_index={self.cp_index}, K={self.K:.1f}, "
                f"p={self.pvalue:.4g}, n={self.n})")


def pettitt(x):
    """Pettitt (1979) non-parametric single-change-point test.

    U_t = sum_{i=1..t} sum_{j=t+1..n} sign(x_i - x_j); K = max_t |U_t|.
    Change point is the t maximising |U_t| (split into x[:t] and x[t:]).
    Approx two-sided p-value: p = 2*exp(-6 K^2 / (n^3 + n^2)).

    Returns PettittResult. Ties contribute sign 0, as in the rank form.
    """
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    n = x.size
    if n < 4:
        raise ValueError("Need at least 4 points for Pettitt test")
    S = np.sign(x[:, None] - x[None, :])
    U = np.array([S[:t, t:].sum() for t in range(1, n)])   # t = 1..n-1
    Ua = np.abs(U)
    k = int(np.argmax(Ua))         # 0-based index into U
    cp = k + 1                     # 1-indexed split point
    K = float(Ua[k])
    p = 2.0 * math.exp(-6.0 * K * K / (n ** 3 + n ** 2))
    return PettittResult(cp, K, min(1.0, p), n)
