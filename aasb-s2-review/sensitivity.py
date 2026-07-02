"""
sensitivity.py: how robust are the maturity bands to the uncertain scores?

21 of the 93 scored cells are marked confidence=medium (scored by
cross-reference rather than a full line-by-line read). This check moves every
medium-confidence score down by 1 and up by 1 (clamped to the 0-4 scale),
recomputes each company's overall score both ways, and reports whether any
company changes maturity band.

Overall score = mean of the four pillar means (equal pillar weights), matching
the README. Bands: 0.0-1.0 Nascent, 1.1-2.0 Emerging, 2.1-3.0 Developing,
3.1-4.0 Advanced.

Run:  python3 sensitivity.py
"""
import pandas as pd

BANDS = [(1.0, "Nascent"), (2.0, "Emerging"), (3.0, "Developing"), (4.0, "Advanced")]


def band(score):
    for upper, name in BANDS:
        if score <= upper:
            return name
    return "Advanced"


def overall(df):
    """Mean of pillar means, one company at a time."""
    return df.groupby("pillar").score.mean().mean()


def main():
    m = pd.read_csv("scoring-matrix.csv")
    med = m.confidence == "medium"
    print(f"{med.sum()} of {len(m)} cells scored at medium confidence\n")
    rows = []
    for company, g in m.groupby("company"):
        base = overall(g)
        lo = g.copy()
        lo.loc[lo.confidence == "medium", "score"] = (
            lo.loc[lo.confidence == "medium", "score"] - 1).clip(lower=0)
        hi = g.copy()
        hi.loc[hi.confidence == "medium", "score"] = (
            hi.loc[hi.confidence == "medium", "score"] + 1).clip(upper=4)
        rows.append({
            "company": company,
            "n_medium": int((g.confidence == "medium").sum()),
            "overall": round(base, 2), "band": band(base),
            "overall_minus1": round(overall(lo), 2), "band_minus1": band(overall(lo)),
            "overall_plus1": round(overall(hi), 2), "band_plus1": band(overall(hi)),
        })
    out = pd.DataFrame(rows)
    print(out.to_string(index=False))
    stable = all(r["band"] == r["band_minus1"] == r["band_plus1"] for r in rows)
    print("\nBands stable under +/-1 on all medium-confidence scores:", stable)
    return out


if __name__ == "__main__":
    main()
