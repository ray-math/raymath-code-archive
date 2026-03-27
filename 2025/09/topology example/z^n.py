# Further shorten arrow length, and ensure only one B-point marker (blue) remains (no overlapping orange).
# Keep A preimage points orange, B point blue.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# ---------- configuration ----------
LW_ARC = 3.0
LW_CIRCLE = 1.2
OFFSET = 1.8
ARROW_GAP = 1.2   # even shorter arrow (larger margin from circles)
PT_SIZE = 40

def unit_circle(num=1024):
    t = np.linspace(0, 2*np.pi, num, endpoint=True)
    return np.cos(t), np.sin(t)

def arc_thetas(center_angle, half_len, num=512):
    num = max(8, int(num))
    return np.linspace(center_angle - half_len, center_angle + half_len, num, endpoint=True)

def xy_from_theta(t):
    return np.cos(t), np.sin(t)

def translate(x, y, dx):
    return np.array(x) + dx, np.array(y)

# ---------- plotting setup ----------
fig = plt.figure(figsize=(11.5, 7.2))
ax = fig.add_axes([0.06, 0.30, 0.88, 0.66])
ax.set_aspect('equal', 'box')
ax.set_xlim([-OFFSET-1.3, OFFSET+1.3])
ax.set_ylim([-1.4, 1.3])
ax.set_xticks([])
ax.set_yticks([])

# base circles
xC, yC = unit_circle()
(axA_circle,) = ax.plot(*(translate(xC, yC, -OFFSET)), linewidth=LW_CIRCLE)
(axB_circle,) = ax.plot(*(translate(xC, yC,  OFFSET)), linewidth=LW_CIRCLE)

# labels
ax.text(-OFFSET, -1.25, r"$A: S^{1}$", ha='center', va='center', fontsize=14)
ax.text( OFFSET, -1.25, r"$B: S^{1}$", ha='center', va='center', fontsize=14)

# central arrow
arrow = ax.annotate("",
            xy=(OFFSET-ARROW_GAP, 0.0), xycoords='data',
            xytext=(-OFFSET+ARROW_GAP, 0.0), textcoords='data',
            arrowprops=dict(arrowstyle="->", linewidth=1.5))
func_text = ax.text(0.0, 0.18, r"$f(z)=z^{3}$", ha='center', va='bottom', fontsize=16)

# Title
title_main = ax.set_title(r"$A$: preimage   |   $B$: open arc of length $\varepsilon$")

# Sliders
ax_n = fig.add_axes([0.12, 0.20, 0.76, 0.035])
ax_eps = fig.add_axes([0.12, 0.13, 0.76, 0.035])
ax_reset = fig.add_axes([0.12, 0.06, 0.16, 0.045])

s_n = Slider(ax=ax_n, label='n', valmin=-5, valmax=15, valinit=3, valstep=1)
s_eps = Slider(ax=ax_eps, label='epsilon (arc length in B)', valmin=0.01, valmax=float(2*np.pi-0.01),
               valinit=float(np.pi/6), valstep=0.001)
btn = Button(ax_reset, 'reset')

# Dynamic artists
(B_arc_line,) = ax.plot([], [], linewidth=LW_ARC, color=axB_circle.get_color())
B_point_scatter, = ax.plot([1.0+OFFSET],[0.0], marker='o', linestyle='', markersize=6, color=axB_circle.get_color())
A_arc_lines = []
A_point_scatters = []

def render():
    global A_arc_lines, A_point_scatters
    for ln in A_arc_lines:
        ln.remove()
    for sc in A_point_scatters:
        sc.remove()
    A_arc_lines = []
    A_point_scatters = []

    n = int(s_n.val)
    eps = float(s_eps.val)

    func_text.set_text(rf"$f(z)=z^{{{n}}}$")

    # B arc
    tB = arc_thetas(0.0, eps/2.0, num=512)
    xB, yB = xy_from_theta(tB)
    xB, yB = translate(xB, yB, OFFSET)
    B_arc_line.set_data(xB, yB)

    # A arcs + points
    A_color = axA_circle.get_color()
    if n == 0:
        xA_all, yA_all = translate(xC, yC, -OFFSET)
        (ln,) = ax.plot(xA_all, yA_all, linewidth=LW_ARC, color=A_color)
        A_arc_lines.append(ln)
        (sc,) = ax.plot([1.0 - OFFSET],[0.0], marker='o', linestyle='', markersize=6, color=A_color)
        A_point_scatters.append(sc)
    else:
        m = abs(n)
        half_len = eps / (2*m)
        per_arc = max(16, int(512 / max(1, m)))
        for k in range(m):
            center = 2*np.pi*k/m if n > 0 else -2*np.pi*k/m
            tA = arc_thetas(center, half_len, num=per_arc)
            xA, yA = xy_from_theta(tA)
            xA, yA = translate(xA, yA, -OFFSET)
            (ln,) = ax.plot(xA, yA, linewidth=LW_ARC, color=A_color)
            A_arc_lines.append(ln)
            cx, cy = np.cos(center)-OFFSET, np.sin(center)
            (sc,) = ax.plot([cx],[cy], marker='o', linestyle='', markersize=6, color=A_color)
            A_point_scatters.append(sc)

    title_main.set_text(rf"$A$: preimage,  $B$: arc length $\varepsilon={eps:.4f}$,  $n={n}$")
    fig.canvas.draw_idle()

def on_reset(event):
    s_n.reset(); s_eps.reset()

s_n.on_changed(lambda _: render())
s_eps.on_changed(lambda _: render())
btn.on_clicked(on_reset)

render()
plt.show()
