import scene_bootstrap  # noqa: F401

import numpy as np
from manim import (
    Axes,
    Create,
    DOWN,
    FadeIn,
    MathTex,
    NumberPlane,
    RIGHT,
    VGroup,
    Write,
)

from style import Palette
from templates import LayoutTemplateScene


class SquaredIntegral(LayoutTemplateScene):
    """I^2 = double integral over xy-plane. Visual: 2D heatmap of e^(-(x^2+y^2))."""

    def construct(self):
        # Left: 2D heatmap-style visualization of e^(-(x^2+y^2))
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4.2,
            y_length=4.2,
            background_line_style={
                "stroke_color": Palette.GRID,
                "stroke_opacity": 0.3,
            },
            axis_config={"color": Palette.AXIS},
        )

        # Create concentric circles to represent the 2D Gaussian
        circles = VGroup()
        for r in np.arange(0.3, 2.7, 0.3):
            opacity = float(np.exp(-(r**2)) * 0.6)
            circle = plane.plot_parametric_curve(
                lambda t, r=r: np.array([r * np.cos(t), r * np.sin(t), 0]),
                t_range=[0, 2 * np.pi, 0.05],
                color=Palette.OBJECT_A,
                stroke_opacity=opacity,
                stroke_width=3,
            )
            circles.add(circle)

        x_label = MathTex("x", color=Palette.MUTED_TEXT, font_size=28)
        y_label = MathTex("y", color=Palette.MUTED_TEXT, font_size=28)
        x_label.next_to(plane, RIGHT, buff=0.1).shift(DOWN * 0.3)
        y_label.next_to(plane, RIGHT * 0, buff=0.1).shift(
            plane.c2p(0, 3)[1] * (plane.get_height() / 6) * RIGHT * 0
        )
        y_label.move_to(plane.get_top() + RIGHT * 0.3)

        visual = VGroup(plane, circles, x_label, y_label)

        # Right: equations
        eq_define = MathTex(
            r"I", r"=", r"\int_{-\infty}^{\infty}", r"e^{-x^2}", r"\,dx",
            color=Palette.TEXT, font_size=42,
        )
        eq_squared = MathTex(
            r"I^2",
            r"=",
            r"\int_{-\infty}^{\infty}\!\int_{-\infty}^{\infty}",
            r"e^{-(x^2+y^2)}",
            r"\,dx\,dy",
            color=Palette.TEXT,
            font_size=42,
        )
        eq_squared[3].set_color(Palette.OBJECT_A)

        equations = VGroup(eq_define, eq_squared).arrange(DOWN, buff=0.6)

        self.layout_split(visual, equations)

        self.play(Create(plane))
        self.wait_beat(1)
        self.play(Write(eq_define))
        self.wait_beat(2)
        self.play(FadeIn(circles), Write(eq_squared))
        self.wait_beat(2)
