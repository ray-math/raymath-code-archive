import scene_bootstrap  # noqa: F401

import numpy as np
from manim import (
    BLUE,
    Create,
    DEGREES,
    DOWN,
    FadeIn,
    GREEN,
    LEFT,
    MathTex,
    PI,
    RIGHT,
    Surface,
    TEAL,
    ThreeDAxes,
    ThreeDScene,
    UP,
    VGroup,
    Write,
    config,
)

from style import Palette


class FinalResult(ThreeDScene):
    """Bell curve rotates to form 3D surface; I^2=pi => I=sqrt(pi)."""

    def construct(self):
        self.camera.background_color = config.background_color

        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 1.2, 0.5],
            x_length=4.0,
            y_length=4.0,
            z_length=2.5,
        )
        axes.shift(LEFT * 3.2 + UP * 0.1)

        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)

        # Start with a partial surface (thin slice) to show the bell curve profile
        # Then expand to full surface to show rotation creates 2pi
        thin_slice = Surface(
            lambda u, v: axes.c2p(
                u * np.cos(v), u * np.sin(v), np.exp(-(u**2))
            ),
            u_range=[0, 3],
            v_range=[-0.05, 0.05],
            resolution=(25, 2),
            fill_opacity=0.8,
        )
        thin_slice.set_color(Palette.OBJECT_A)

        # Build up the surface gradually through rotation angles
        partial_surfaces = []
        for max_theta in [PI / 4, PI / 2, PI, 2 * PI]:
            s = Surface(
                lambda u, v, mt=max_theta: axes.c2p(
                    u * np.cos(v), u * np.sin(v), np.exp(-(u**2))
                ),
                u_range=[0, 3],
                v_range=[0, max_theta],
                resolution=(25, max(4, int(max_theta / PI * 15))),
                fill_opacity=0.7,
            )
            s.set_color_by_gradient(BLUE, TEAL, GREEN)
            partial_surfaces.append(s)

        # --- Right: final equations ---
        eq_result = MathTex(
            r"I^2 = \pi",
            color=Palette.TEXT,
            font_size=52,
        )
        eq_final = MathTex(
            r"\therefore\quad I = \sqrt{\pi}",
            color=Palette.HIGHLIGHT,
            font_size=56,
        )
        eq_meaning = MathTex(
            r"\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}",
            color=Palette.TEXT,
            font_size=44,
        )
        equations = VGroup(eq_result, eq_final, eq_meaning).arrange(DOWN, buff=0.55)
        equations.move_to(RIGHT * 3.5)

        self.add_fixed_in_frame_mobjects(equations)

        # --- Animate: bell curve rotating into full 3D surface ---
        self.play(Create(axes), run_time=1)

        # Show thin slice (the bell curve profile)
        self.play(Create(thin_slice), run_time=1)
        self.wait(0.3)

        # Gradually rotate to show where 2pi comes from
        prev = thin_slice
        for s in partial_surfaces:
            self.play(FadeIn(s), run_time=0.7)
            self.remove(prev)
            prev = s

        self.wait(0.3)
        self.play(Write(eq_result))
        self.wait(0.5)

        # Slow camera rotation to emphasize symmetry
        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(Write(eq_final), run_time=1.5)
        self.wait(1)
        self.play(Write(eq_meaning), run_time=1.5)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)
