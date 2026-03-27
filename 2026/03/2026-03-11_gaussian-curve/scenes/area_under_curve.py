import scene_bootstrap  # noqa: F401

import numpy as np
from manim import (
    Axes,
    Create,
    DL,
    DOWN,
    DR,
    FadeIn,
    MathTex,
    TransformMatchingTex,
    UL,
    UR,
    VGroup,
    Write,
)

from style import Palette
from templates import LayoutTemplateScene


class AreaUnderCurve(LayoutTemplateScene):
    """Bell curve with shaded area, then reveal integral = sqrt(pi)."""

    def construct(self):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-0.2, 1.2, 0.5],
            x_length=4.8,
            y_length=3.6,
            axis_config={"color": Palette.AXIS},
            tips=False,
        )
        graph = axes.plot(lambda x: np.exp(-(x**2)), color=Palette.GRAPH_LINE)
        area = axes.get_area(
            graph,
            x_range=[-3, 3],
            color=Palette.OBJECT_A,
            opacity=0.3,
        )
        visual = VGroup(axes, graph, area)

        integral_eq = MathTex(
            r"\int_{-\infty}^{\infty}",
            r"e^{-x^2}",
            r"\,dx",
            r"=",
            r"\sqrt{\pi}",
            color=Palette.TEXT,
            font_size=52,
        )
        integral_eq[4].set_color(Palette.HIGHLIGHT)

        self.layout_split(visual, integral_eq)

        self.play(Create(axes), Create(graph))
        self.wait_beat(1)
        self.play(FadeIn(area))
        self.wait_beat(1)
        self.play(Write(integral_eq))
        self.wait_beat(2)
