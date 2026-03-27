import scene_bootstrap  # noqa: F401

import numpy as np
from manim import (
    Angle,
    Arrow,
    Circle,
    Create,
    DashedLine,
    Dot,
    DOWN,
    FadeIn,
    LEFT,
    Line,
    MathTex,
    NumberPlane,
    RIGHT,
    UP,
    VGroup,
    Write,
)

from style import Palette
from templates import LayoutTemplateScene


class PolarTransform(LayoutTemplateScene):
    """Polar coordinate transformation: x,y -> r,theta diagram."""

    def construct(self):
        # Left: xy-plane with point, r line, theta angle
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4.2,
            y_length=4.2,
            background_line_style={
                "stroke_color": Palette.GRID,
                "stroke_opacity": 0.2,
            },
            axis_config={"color": Palette.AXIS, "stroke_opacity": 0.6},
        )

        # Point at (2, 1.5) in plane coords
        px, py = 1.8, 1.3
        point_pos = plane.c2p(px, py)
        origin = plane.c2p(0, 0)
        x_axis_pt = plane.c2p(px, 0)

        dot = Dot(point_pos, color=Palette.HIGHLIGHT, radius=0.07)
        point_label = MathTex("(x, y)", color=Palette.HIGHLIGHT, font_size=28)
        point_label.next_to(dot, UP + RIGHT, buff=0.12)

        # r line from origin to point
        r_line = Line(origin, point_pos, color=Palette.OBJECT_B, stroke_width=3)
        r_label = MathTex("r", color=Palette.OBJECT_B, font_size=32)
        r_label.move_to(r_line.get_center() + LEFT * 0.25 + UP * 0.15)

        # Dashed lines for x and y projections
        x_proj = DashedLine(origin, x_axis_pt, color=Palette.MUTED_TEXT, stroke_width=2)
        y_proj = DashedLine(x_axis_pt, point_pos, color=Palette.MUTED_TEXT, stroke_width=2)

        # Theta angle arc
        theta_arc = Angle(
            Line(origin, plane.c2p(3, 0)),
            r_line,
            radius=0.5,
            color=Palette.OBJECT_C,
        )
        theta_label = MathTex(r"\theta", color=Palette.OBJECT_C, font_size=28)
        theta_label.next_to(theta_arc, RIGHT, buff=0.1).shift(UP * 0.05)

        # Dashed circle showing r = const
        r_val = np.sqrt(px**2 + py**2)
        r_circle = Circle(
            radius=plane.c2p(r_val, 0)[0] - origin[0],
            color=Palette.OBJECT_B,
            stroke_width=1.5,
            stroke_opacity=0.4,
        ).move_to(origin)

        x_ax_label = MathTex("x", color=Palette.MUTED_TEXT, font_size=26)
        y_ax_label = MathTex("y", color=Palette.MUTED_TEXT, font_size=26)
        x_ax_label.next_to(plane.c2p(3, 0), DOWN, buff=0.15)
        y_ax_label.next_to(plane.c2p(0, 3), LEFT, buff=0.15)

        visual = VGroup(
            plane, x_proj, y_proj, r_line, r_circle,
            theta_arc, theta_label, r_label, dot, point_label,
            x_ax_label, y_ax_label,
        )

        # Right: polar coordinate equations
        eq1 = MathTex(
            r"x = r\cos\theta", color=Palette.TEXT, font_size=40,
        )
        eq2 = MathTex(
            r"y = r\sin\theta", color=Palette.TEXT, font_size=40,
        )
        eq3 = MathTex(
            r"x^2 + y^2 = r^2", color=Palette.OBJECT_B, font_size=44,
        )
        eq4 = MathTex(
            r"dx\,dy = r\,dr\,d\theta", color=Palette.OBJECT_C, font_size=44,
        )

        equations = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, buff=0.45)

        self.layout_split(visual, equations)

        self.play(Create(plane), Write(x_ax_label), Write(y_ax_label))
        self.wait_beat(1)
        self.play(Create(dot), Write(point_label))
        self.play(Create(x_proj), Create(y_proj))
        self.play(Create(r_line), Write(r_label), Write(eq1), Write(eq2))
        self.wait_beat(1)
        self.play(Create(theta_arc), Write(theta_label))
        self.wait_beat(1)
        self.play(FadeIn(r_circle), Write(eq3))
        self.wait_beat(1)
        self.play(Write(eq4))
        self.wait_beat(2)
