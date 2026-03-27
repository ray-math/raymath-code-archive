import scene_bootstrap  # noqa: F401

import math

from manim import (
    Axes,
    Create,
    DashedLine,
    Dot,
    DOWN,
    FadeIn,
    LEFT,
    LaggedStart,
    MathTex,
    VGroup,
    Write,
)

from style import Palette
from templates import LayoutTemplateScene


class GammaFunctionIntro(LayoutTemplateScene):
    """Gamma function as an extension of factorial to non-integers."""

    def construct(self):
        axes = Axes(
            x_range=[-4.5, 4.5, 1],
            y_range=[-6, 6, 2],
            x_length=5.4,
            y_length=3.6,
            axis_config={"color": Palette.AXIS},
            x_axis_config={
                "include_numbers": True,
                "font_size": 24,
                "decimal_number_config": {"num_decimal_places": 0},
            },
            y_axis_config={"include_numbers": False},
            tips=False,
        )
        eps = 0.08
        segment_ranges = [
            (-4.5, -4 - eps),
            (-4 + eps, -3 - eps),
            (-3 + eps, -2 - eps),
            (-2 + eps, -1 - eps),
            (-1 + eps, -eps),
            (eps, 4.5),
        ]
        gamma_graphs = VGroup(
            *[
                axes.plot(
                    lambda x: math.gamma(x),
                    x_range=[x0, x1],
                    color=Palette.GRAPH_LINE,
                    use_smoothing=False,
                )
                for x0, x1 in segment_ranges
            ]
        )
        pole_lines = VGroup(
            *[
                DashedLine(
                    axes.c2p(x, -6),
                    axes.c2p(x, 6),
                    dash_length=0.08,
                    color=Palette.NEGATIVE,
                    stroke_opacity=0.35,
                    stroke_width=2,
                )
                for x in [-4, -3, -2, -1, 0]
            ]
        )

        integer_dots = VGroup(
            *[
                Dot(axes.c2p(x, math.gamma(x)), radius=0.05, color=Palette.HIGHLIGHT)
                for x in [1, 2, 3, 4]
            ]
        )
        non_integer_dots = VGroup(
            Dot(
                axes.c2p(2.5, math.gamma(2.5)),
                radius=0.05,
                color=Palette.OBJECT_B,
            ),
            Dot(
                axes.c2p(-0.5, math.gamma(-0.5)),
                radius=0.05,
                color=Palette.OBJECT_C,
            ),
        )
        visual = VGroup(axes, pole_lines, gamma_graphs, integer_dots, non_integer_dots)

        eq_definition = MathTex(
            r"\Gamma(x)=\int_0^{\infty} t^{x-1}e^{-t}\,dt",
            color=Palette.TEXT,
            font_size=44,
        )
        eq_factorial = MathTex(
            r"\Gamma(n+1)=n!",
            color=Palette.HIGHLIGHT,
            font_size=58,
        )
        equations = VGroup(eq_definition, eq_factorial).arrange(
            DOWN, buff=0.6, aligned_edge=LEFT
        )

        self.layout_split(visual, equations)

        self.play(Create(axes), run_time=1.1)
        self.play(FadeIn(pole_lines), run_time=0.5)
        self.play(
            LaggedStart(*[Create(graph) for graph in gamma_graphs], lag_ratio=0.1),
            run_time=2.4,
        )
        self.play(FadeIn(integer_dots), FadeIn(non_integer_dots), run_time=0.9)
        self.play(Write(eq_definition))
        self.wait_beat(1)
        self.play(Write(eq_factorial))
        self.wait_beat(3)
