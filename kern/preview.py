"""Rendert eine STL als PNG aus mehreren Blickwinkeln - zur Sichtkontrolle vor dem Druck."""

import struct

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def load_stl(path):
    with open(path, "rb") as f:
        data = f.read()
    n = struct.unpack("<I", data[80:84])[0]
    tris = np.zeros((n, 3, 3), dtype=np.float32)
    for i in range(n):
        off = 84 + i * 50
        vals = struct.unpack("<12f", data[off : off + 48])
        tris[i] = np.array(vals[3:12]).reshape(3, 3)
    return tris


def render(stl_path, png_path, views=None, farbe="#e63329", titel=None):
    views = views or [(20, -60, "Perspektive"), (0, -90, "Vorn"), (0, 0, "Seite")]
    tris = load_stl(stl_path)

    fig = plt.figure(figsize=(6 * len(views), 6.5), facecolor="white")
    for i, (elev, azim, name) in enumerate(views, 1):
        ax = fig.add_subplot(1, len(views), i, projection="3d")
        coll = Poly3DCollection(tris, facecolor=farbe, edgecolor="#00000018", linewidths=0.15)
        ax.add_collection3d(coll)

        pts = tris.reshape(-1, 3)
        lo, hi = pts.min(axis=0), pts.max(axis=0)
        mid, span = (lo + hi) / 2, (hi - lo).max() / 2
        ax.set_xlim(mid[0] - span, mid[0] + span)
        ax.set_ylim(mid[1] - span, mid[1] + span)
        ax.set_zlim(mid[2] - span, mid[2] + span)
        ax.set_box_aspect((1, 1, 1))
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(name, fontsize=13)
        ax.set_axis_off()

    if titel:
        fig.suptitle(titel, fontsize=15, y=0.97)
    fig.tight_layout()
    fig.savefig(png_path, dpi=95, bbox_inches="tight")
    plt.close(fig)
    print(f"  -> {png_path}")
