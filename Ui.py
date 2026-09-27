"""Textbook-style Group-IV alloy band diagram UI.

E vs k band diagram: valence band centered at Gamma, direct conduction valley
at Gamma, and indirect conduction valley at L. Whichever valley is lower is
highlighted as the true band gap, sliding live as composition sliders are dragged.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from CalculateBandGapType import CalculateBandGapType


class BandDiagramApp:

    K_L = 1.0            # zone-edge L position, reduced k-units
    K_MAX = 1.45
    VB_CURVATURE = 1.35
    CB_CURVATURE = 1.6

    def __init__(self):
        self.xSi = 0.00
        self.ySn = 0.10

        self.fig, self.ax = plt.subplots(figsize=(9, 6.5))
        self.fig.patch.set_facecolor("#1e1e1e")
        self.fig.subplots_adjust(bottom=0.28, top=0.86)

        self._init_sliders()
        self.update_diagram()

    # ------------------------------------------------------------------ #
    def _style_axes(self):
        self.ax.set_facecolor("#1e1e1e")
        self.ax.set_xlabel("Crystal momentum, k", color="white")
        self.ax.set_ylabel("Energy (eV)", color="white")
        self.ax.tick_params(colors="white")
        for spine in self.ax.spines.values():
            spine.set_color("white")
        self.ax.axhline(0, color="#666666", lw=0.8, ls=":")

    def _init_sliders(self):
        ax_si = self.fig.add_axes((0.15, 0.14, 0.7, 0.03))
        ax_sn = self.fig.add_axes((0.15, 0.08, 0.7, 0.03))
        for a in (ax_si, ax_sn):
            a.set_facecolor("#333333")

        self.slider_si = Slider(
            ax_si, "Si fraction (x)", 0.0, 1.0, valinit=self.xSi,
            color="#3399ff",
        )
        self.slider_sn = Slider(
            ax_sn, "Sn fraction (y)", 0.0, 1.0, valinit=self.ySn,
            color="#f59e0b",
        )
        for s in (self.slider_si, self.slider_sn):
            s.label.set_color("white")
            s.valtext.set_color("white")

        self.slider_si.on_changed(self._on_si_change)
        self.slider_sn.on_changed(self._on_sn_change)

    # ------------------------------------------------------------------ #
    def _on_si_change(self, val):
        self.xSi = val
        if self.xSi + self.ySn > 1.0:
            self.ySn = max(0.0, 1.0 - self.xSi)
            self.slider_sn.eventson = False
            self.slider_sn.set_val(self.ySn)
            self.slider_sn.eventson = True
        self.update_diagram()

    def _on_sn_change(self, val):
        self.ySn = val
        if self.xSi + self.ySn > 1.0:
            self.xSi = max(0.0, 1.0 - self.ySn)
            self.slider_si.eventson = False
            self.slider_si.set_val(self.xSi)
            self.slider_si.eventson = True
        self.update_diagram()

    # ------------------------------------------------------------------ #
    def update_diagram(self):
        xSi, ySn = self.xSi, self.ySn
        zGe = 1 - xSi - ySn

        # Authoritative energy calculation (unstrained bulk mode)
        result = CalculateBandGapType(xSi, ySn)
        gap_type, eg_value = result[0], result[1]
        e_gamma, e_L = result.e_gamma, result.e_l

        self.ax.clear()
        self._style_axes()

        k = np.linspace(-self.K_MAX, self.K_MAX, 400)

        # Valence band: parabolic approximation centered at Gamma, referenced to 0 eV
        vb = -self.VB_CURVATURE * k ** 2
        self.ax.plot(k, vb, color="#dddddd", lw=2.5, label="Valence band")

        # Gamma (direct) and L (indirect) conduction valleys
        cb_gamma = e_gamma + self.CB_CURVATURE * k ** 2
        cb_L_pos = e_L + self.CB_CURVATURE * (k - self.K_L) ** 2
        cb_L_neg = e_L + self.CB_CURVATURE * (k + self.K_L) ** 2

        is_direct = gap_type == "Direct"

        self.ax.plot(
            k, cb_gamma,
            color="#3399ff" if is_direct else "#777777",
            lw=3 if is_direct else 1.5,
            ls="-" if is_direct else "--",
            label="Γ valley (direct)",
        )
        self.ax.plot(
            k, cb_L_pos,
            color="#f59e0b" if not is_direct else "#777777",
            lw=3 if not is_direct else 1.5,
            ls="-" if not is_direct else "--",
            label="L valley (indirect)",
        )
        self.ax.plot(
            k, cb_L_neg,
            color="#f59e0b" if not is_direct else "#777777",
            lw=3 if not is_direct else 1.5,
            ls="-" if not is_direct else "--",
        )

        # Draw band-gap annotation arrow from valence band maximum (0, 0)
        semimetallic = eg_value <= 0
        arrow_color = "#f87171" if semimetallic else "#4ade80"
        self.ax.annotate(
            "", xy=(0, eg_value), xytext=(0, 0),
            arrowprops=dict(arrowstyle="<->", color=arrow_color, lw=2),
        )
        label = (
            f"ΔE = {eg_value:.3f} eV\n(semimetallic overlap)"
            if semimetallic else
            f"E$_g$ = {eg_value:.3f} eV\n({gap_type})"
        )
        self.ax.text(
            0.08, eg_value / 2 if abs(eg_value) > 1e-6 else 0.15,
            label, color=arrow_color, fontsize=11, va="center",
        )

        self.ax.legend(
            facecolor="#1e1e1e", edgecolor="white", labelcolor="white",
            loc="upper right", fontsize=9,
        )

        y_lo = vb.min() - 0.3
        y_hi = max(e_gamma, e_L) + 2.5
        self.ax.set_ylim(y_lo, y_hi)
        self.ax.set_xlim(-self.K_MAX, self.K_MAX)
        self.ax.set_xticks([-self.K_L, 0, self.K_L])
        self.ax.set_xticklabels(["L", "Γ", "L"], color="white", fontsize=12)

        self.fig.suptitle(
            "Group-IV Alloy Band Diagram (Si$_x$Ge$_z$Sn$_y$)\n"
            f"Si: {xSi:.2f}   Sn: {ySn:.2f}   Ge: {zGe:.2f}   |   "
            f"{gap_type} gap, E$_g$ = {eg_value:.3f} eV",
            color="white", fontsize=12, y=0.98,
        )

        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()


def start_ui():
    app = BandDiagramApp()
    app.show()


if __name__ == "__main__":
    start_ui()