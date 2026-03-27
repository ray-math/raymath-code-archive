import confpath  # noqa: F401

from manim import (
    AnimationGroup,
    DOWN,
    FadeTransform,
    Indicate,
    LEFT,
    MathTex,
    RIGHT,
    TransformMatchingTex,
    UP,
    VGroup,
    Write,
    smooth,
)

from style import Layout, Palette
from templates import LayoutTemplateScene


class PowerAndExtension(LayoutTemplateScene):
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
        fs = 34

        d_def = MathTex(
            r"D = \begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix}",
            color=Palette.TEXT,
            font_size=fs,
        )
        d_four = MathTex(
            r"D^{4} = -4I",
            color=Palette.HIGHLIGHT,
            font_size=32,
        )
        left_block = VGroup(d_def, d_four).arrange(DOWN, buff=0.45, aligned_edge=LEFT)

        five_matrix = MathTex(
            r"[D]_{\mathcal B} =",
            r"\begin{pmatrix} 0 & -1 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 & -1 \\ 0 & 0 & 0 & 1 & 1 \end{pmatrix}",
            color=Palette.TEXT,
            font_size=26,
        )

        step1 = MathTex(r"y^{(n)} = D^{n} y", color=Palette.TEXT, font_size=fs)
        step2 = MathTex(r"D^{4} = -4I", color=Palette.TEXT, font_size=fs)
        step3 = MathTex(
            r"\begin{pmatrix} a \\ b \\ c \\ d \\ f \end{pmatrix}",
            r"\mapsto",
            r"\begin{pmatrix} -b \\ a \\ c \\ d-f \\ d+f \end{pmatrix}",
            color=Palette.TEXT,
            font_size=fs,
        )

        self._balanced_split(left_block, step1)
        five_matrix.move_to(left_block)
        step2.move_to(step1)
        step3.move_to(step1)

        self.play(
            AnimationGroup(Write(d_def), Write(d_four), run_time=2, rate_func=smooth),
            AnimationGroup(Write(step1), run_time=2, rate_func=smooth),
        )
        self.wait_beat(1.5)

        self.play(TransformMatchingTex(step1, step2))
        self.play(Indicate(d_four, color=Palette.HIGHLIGHT))
        self.wait_beat(1.5)

        self.play(
            AnimationGroup(FadeTransform(left_block, five_matrix), run_time=2, rate_func=smooth),
            AnimationGroup(TransformMatchingTex(step2, step3), run_time=2, rate_func=smooth),
        )
        self.wait_beat(4)
