import confpath  # noqa: F401

import numpy as np
from manim import (
    Axes,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    MathTex,
    RIGHT,
    UP,
    VGroup,
    Write,
)

from style import Layout, Palette
from templates import LayoutTemplateScene


class PointToFunction(LayoutTemplateScene):
    def _balanced_split(self, left, right, gap=0.8):
        safe_left, safe_right = self._safe_x_bounds()
        target_y = self._with_global_up_shift(Layout.SPLIT_Y)
        max_side_w = (safe_right - safe_left - gap) / 2
        for mob in [left, right]:
            if mob.width > max_side_w:
                mob.scale(max_side_w / mob.width)
        combined = VGroup(left, right).arrange(RIGHT, buff=gap)
        combined.move_to(UP * target_y)
        return combined

    def construct(self):
        fs = 36

        point_axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=5.4,
            y_length=3.8,
            axis_config={"color": Palette.AXIS},
            tips=False,
        )
        dot = Dot(point_axes.c2p(3, 5), color=Palette.HIGHLIGHT, radius=0.08)
        point_label = MathTex(r"(3,\;5)", color=Palette.TEXT, font_size=44)
        point_label.next_to(dot, UP, buff=0.2)
        point_visual = VGroup(point_axes, dot, point_label)
        self.layout_center(point_visual)

        function_axes = Axes(
            x_range=[0, 1.8, 0.5],
            y_range=[-10, 18, 5],
            x_length=4.5,
            y_length=3.4,
            axis_config={"color": Palette.AXIS},
            tips=False,
        )
        curve = function_axes.plot(
            lambda x: 3 * np.exp(x) * np.sin(x) + 5 * np.exp(x) * np.cos(x),
            x_range=[0, 1.7],
            color=Palette.OBJECT_A,
        )
        pair_label = MathTex(r"(3,\;5)", color=Palette.HIGHLIGHT, font_size=44)
        pair_label.next_to(function_axes, UP, buff=0.22)
        function_visual = VGroup(function_axes, curve, pair_label)

        equation = MathTex(
            r"(3,\;5)",
            r"\longleftrightarrow",
            r"3e^{x}\sin x + 5e^{x}\cos x",
            color=Palette.TEXT,
            font_size=fs,
        )
        self._balanced_split(function_visual, equation)

        self.play(Create(point_axes), FadeIn(dot), Write(point_label))
        self.wait_beat(2)

        self.play(
            FadeOut(point_visual, shift=RIGHT * 0.3),
            FadeIn(function_visual, shift=RIGHT * 0.3),
            FadeIn(equation, shift=RIGHT * 0.3),
            run_time=2.2,
        )
        self.wait_beat(4)
