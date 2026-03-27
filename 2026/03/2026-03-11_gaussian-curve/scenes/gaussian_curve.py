import scene_bootstrap  # noqa: F401

import numpy as np
from manim import Axes, Create, VGroup, Write

from style import Palette
from templates import LayoutTemplateScene


class GaussianCurve(LayoutTemplateScene):
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
        visual = VGroup(axes, graph)

        equation = self.make_equation(r"f(x) = e^{-x^2}", font_size=60)

        self.layout_split(visual, equation)
        self.play(Create(axes), Create(graph), Write(equation))
        self.wait_beat(2)
