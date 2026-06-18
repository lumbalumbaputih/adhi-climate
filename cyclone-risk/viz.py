"""
viz.py: shared chart styling for the cyclone-risk analysis.
Uses the Adhi "Hidup" palette so the figures are consistent across the
portfolio. Publication settings: 300 dpi, labelled axes, light grid.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Hidup palette
INK = "#1A1614"
MUTED = "#6B6259"
PAPER = "#FBF4E6"
TOMATO = "#FF5C39"
MANGO = "#FFC234"
FOREST = "#1F9D55"
SEA = "#1FA9C7"
MAWAR = "#E84BA0"
INDIGO = "#2E3192"

# decade colours (ordered, cool -> warm to read as "time")
DECADE_COLORS = {
    "1985-94": INDIGO,
    "1995-04": SEA,
    "2005-14": MANGO,
    "2015-24": TOMATO,
}


def apply_style():
    plt.rcParams.update({
        "figure.dpi": 120,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "axes.titlecolor": INK,
        "axes.titleweight": "bold",
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "axes.linewidth": 1.0,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": "#D8D0C0",
        "grid.linewidth": 0.7,
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
        "legend.frameon": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    })


def credit(ax, text="Data: IBTrACS v04r01 (NOAA NCEI) & NOAA ERSSTv5  ·  Analysis: A. Katili"):
    ax.annotate(text, xy=(1.0, -0.14), xycoords="axes fraction", ha="right",
                va="top", fontsize=8, color=MUTED)
