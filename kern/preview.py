"""Rendert Koerper als PNG - zur Sichtkontrolle vor dem Druck und fuers README.

Gerendert wird IMMER in Wandorientierung (z = 0 ist die Brettoberkante, negativ ist
unten), NICHT in der Drucklage. Die exportierte STL steht kopfueber auf dem Bett -
richtig fuer den Slicer, aber als Bild unverstaendlich. Deshalb wird hier direkt der
Koerper vernetzt statt die STL geladen.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

HALTER = "#e63329"  # Filamentrot
HOLZ = "#d9b382"  # Fichte
STAHL = "#b0b6bb"  # verchromter Stahl

ANSICHTEN = [(18, -62, "Perspektive"), (3, -90, "Von vorn"), (3, -2, "Von der Seite")]


def _dreiecke(teil, toleranz=0.15):
    ecken, dreiecke = teil.tessellate(toleranz)
    pts = np.array([(p.X, p.Y, p.Z) for p in ecken])
    return pts[np.array(dreiecke)]


def render(teile, png_pfad, ansichten=None, titel=None):
    """teile: ein Koerper, oder eine Liste von (Koerper, Farbe)."""
    if not isinstance(teile, (list, tuple)):
        teile = [(teile, HALTER)]

    # ALLE Dreiecke in EINE Collection, mit Farbe pro Dreieck. Getrennte Collections
    # sortiert matplotlib nicht gegeneinander nach Tiefe - es malt sie stur
    # nacheinander, und dann verdeckt das Rohr die Huelse oder umgekehrt.
    netze = [_dreiecke(k) for k, _ in teile]
    dreiecke = np.concatenate(netze)
    farben = np.concatenate([[f] * len(n) for n, (_, f) in zip(netze, teile)])

    alle = dreiecke.reshape(-1, 3)
    mitte = (alle.min(0) + alle.max(0)) / 2
    spanne = (alle.max(0) - alle.min(0)).max() / 2

    ansichten = ansichten or ANSICHTEN
    fig = plt.figure(figsize=(5.5 * len(ansichten), 6.2), facecolor="white")
    for i, (elev, azim, name) in enumerate(ansichten, 1):
        ax = fig.add_subplot(1, len(ansichten), i, projection="3d")
        ax.add_collection3d(
            Poly3DCollection(
                dreiecke, facecolors=farben, edgecolor="#00000010", linewidths=0.08
            )
        )
        for setzen, m in ((ax.set_xlim, mitte[0]), (ax.set_ylim, mitte[1]), (ax.set_zlim, mitte[2])):
            setzen(m - spanne, m + spanne)
        ax.set_box_aspect((1, 1, 1))
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(name, fontsize=12)
        ax.set_axis_off()

    if titel:
        fig.suptitle(titel, fontsize=15, y=0.96)
    fig.tight_layout()
    fig.savefig(png_pfad, dpi=100, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> {png_pfad}")
