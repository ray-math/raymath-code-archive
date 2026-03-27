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
    RIGHT,
    Surface,
    TEAL,
    ThreeDAxes,
    ThreeDScene,
    UP,
    Write,
    YELLOW,
    config,
)

from style import Palette


class EvaluateIntegral(ThreeDScene):
    """3D Gaussian surface on the left, aligned derivation on the right."""

    def construct(self):
        self.camera.background_color = config.background_color

        # --- Left: 3D surface of e^(-(x^2+y^2)) ---
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 1.2, 0.5],
            x_length=4.0,
            y_length=4.0,
            z_length=2.5,
        )
        surface = Surface(
            lambda u, v: axes.c2p(u, v, np.exp(-(u**2 + v**2))),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30),
            fill_opacity=0.7,
        )
        surface.set_color_by_gradient(BLUE, TEAL, GREEN)

        # Position 3D group to the left
        threed_group = axes
        threed_group.shift(LEFT * 3.2 + UP * 0.1)
        surface.shift(LEFT * 3.2 + UP * 0.1)

        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)

        # --- Right: aligned derivation (all at once) ---
        derivation = MathTex(
            r"I^2",
            r"&= \int_0^{2\pi}\!\int_0^{\infty} e^{-r^2}\,r\,dr\,d\theta \\",
            r"&= \int_0^{2\pi} d\theta \cdot \int_0^{\infty} r\,e^{-r^2}\,dr \\",
            r"&= 2\pi \cdot \left[-\tfrac{1}{2}e^{-r^2}\right]_0^{\infty} \\",
            r"&= 2\pi \cdot \tfrac{1}{2} \\",
            r"&= \pi",
            color=Palette.TEXT,
            font_size=36,
        )
        derivation[5].set_color(Palette.HIGHLIGHT)
        derivation.move_to(RIGHT * 3.5)

        self.add_fixed_in_frame_mobjects(derivation)

        # --- Animate ---
        self.play(Create(axes), run_time=1)
        self.play(Create(surface), run_time=1.5)
        self.wait(0.3)
        self.play(Write(derivation), run_time=2)
        self.wait(0.5)

        # Slow rotation to show the rotational symmetry
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)
