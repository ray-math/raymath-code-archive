import scene_bootstrap  # noqa: F401

import numpy as np
from manim import (
    BLUE,
    Create,
    DEGREES,
    DOWN,
    GREEN,
    LEFT,
    MathTex,
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


class GaussianProof3D(ThreeDScene):
    """Combined scene: 3D Gaussian surface rotates on the left, equations on the right.
    Phase 1 (15s): derivation.
    Phase 2 (15s): final result.
    Uses frame_center to shift view so ORIGIN (3D) appears left of screen.
    """

    def construct(self):
        self.camera.background_color = config.background_color

        # --- 3D content at ORIGIN ---
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 1.2, 0.5],
            x_length=4.5,
            y_length=4.5,
            z_length=2.5,
            axis_config={"tip_length": 0.12, "tip_width": 0.08},
        )
        surface = Surface(
            lambda u, v: axes.c2p(u, v, np.exp(-(u**2 + v**2))),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30),
            fill_opacity=0.7,
        )
        surface.set_color_by_gradient(BLUE, TEAL, GREEN)

        # Keep the camera fixed at the previous scene's end look (~34s),
        # then rotate the function in place.
        total_spin_time = 15 + 1.5 + 15
        end_theta = (-50 + np.degrees(0.15 * total_spin_time)) * DEGREES

        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=end_theta,
            frame_center=RIGHT * 1.3,
        )

        # --- Phase 1: Derivation (fixed in frame, right side) ---
        eq_anchor = RIGHT * 4.2 + UP * 0.1

        derivation = MathTex(
            r"I^2",
            r"&= \int_0^{2\pi}\!\int_0^{\infty} e^{-r^2}\,r\,dr\,d\theta \\",
            r"&= \int_0^{2\pi} d\theta \cdot \int_0^{\infty} r\,e^{-r^2}\,dr \\",
            r"&= 2\pi \cdot \left[-\tfrac{1}{2}e^{-r^2}\right]_0^{\infty} \\",
            r"&= 2\pi \cdot \tfrac{1}{2} \\",
            r"&= \pi",
            color=Palette.TEXT,
            font_size=32,
        )
        derivation[5].set_color(Palette.HIGHLIGHT)
        derivation.move_to(eq_anchor)

        self.add_fixed_in_frame_mobjects(derivation)

        # Everything appears together
        self.play(
            Create(axes),
            Create(surface),
            Write(derivation),
            run_time=2.5,
        )

        # Rotate only the function+axes around world z-axis in place.
        spin_center = axes.c2p(0, 0, 0)
        z_axis = np.array([0.0, 0.0, 1.0])

        def spin_in_place(mob, dt):
            mob.rotate(-0.15 * dt, axis=z_axis, about_point=spin_center)

        axes.add_updater(spin_in_place)
        surface.add_updater(spin_in_place)
        self.wait(15)

        # --- Phase 2: Transform equations ---
        eq_result = MathTex(r"I^2", r"=", r"\pi", color=Palette.TEXT, font_size=52)
        eq_final = MathTex(
            r"\therefore\quad I",
            r"=",
            r"\sqrt{\pi}",
            color=Palette.HIGHLIGHT,
            font_size=56,
        )
        eq_meaning = MathTex(
            r"\int_{-\infty}^{\infty} e^{-x^2}\,dx",
            r"=",
            r"\sqrt{\pi}",
            color=Palette.TEXT,
            font_size=44,
        )
        final_eqs = VGroup(eq_result, eq_final, eq_meaning).arrange(
            DOWN, buff=0.55, aligned_edge=LEFT
        )
        equals_x = eq_result[1].get_x()
        for eq in (eq_final, eq_meaning):
            eq.shift((equals_x - eq[1].get_x()) * RIGHT)
        final_eqs.move_to(eq_anchor)

        # fixed_in_frame + crossfade (ReplacementTransform breaks fixed_in_frame)
        self.add_fixed_in_frame_mobjects(final_eqs)
        final_eqs.set_opacity(0)
        self.play(
            derivation.animate.set_opacity(0),
            final_eqs.animate.set_opacity(1),
            run_time=1.5,
        )
        self.remove(derivation)

        # Continue in-place spin for 15 seconds
        self.wait(15)
        axes.remove_updater(spin_in_place)
        surface.remove_updater(spin_in_place)
        self.wait(0.5)
