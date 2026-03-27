import confpath  # noqa: F401

from manim import (
    AnimationGroup,
    Create,
    DOWN,
    FadeIn,
    Indicate,
    LEFT,
    MathTex,
    RIGHT,
    SurroundingRectangle,
    TransformMatchingTex,
    UP,
    VGroup,
    Write,
    smooth,
)

from style import Layout, Palette
from templates import LayoutTemplateScene


class DifferentiationMatrix(LayoutTemplateScene):
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

        mat_def = MathTex(
            r"D",
            r"=",
            r"\begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix}",
            color=Palette.TEXT,
            font_size=fs,
        )

        generic_map = MathTex(
            r"D\begin{pmatrix} a \\ b \end{pmatrix}",
            r"=",
            r"\begin{pmatrix} a-b \\ a+b \end{pmatrix}",
            color=Palette.TEXT,
            font_size=30,
        )

        concrete_map = MathTex(
            r"D\begin{pmatrix} 3 \\ 5 \end{pmatrix}",
            r"=",
            r"\begin{pmatrix} -2 \\ 8 \end{pmatrix}",
            color=Palette.TEXT,
            font_size=30,
        )
        concrete_map[2].set_color(Palette.HIGHLIGHT)

        step1 = MathTex(
            r"y = ae^{x}\sin x + be^{x}\cos x",
            color=Palette.TEXT,
            font_size=fs,
        )
        step2 = MathTex(
            r"y' = (a-b)e^{x}\sin x + (a+b)e^{x}\cos x",
            color=Palette.TEXT,
            font_size=fs,
        )
        step3 = MathTex(
            r"\begin{pmatrix} a \\ b \end{pmatrix}",
            r"\mapsto",
            r"\begin{pmatrix} a-b \\ a+b \end{pmatrix}",
            color=Palette.TEXT,
            font_size=fs,
        )

        self._balanced_split(VGroup(mat_def), step1)
        generic_map.next_to(mat_def, DOWN, buff=0.55, aligned_edge=LEFT)
        concrete_map.move_to(generic_map)
        step2.move_to(step1)
        step3.move_to(step1)

        self.play(
            AnimationGroup(Write(mat_def), run_time=2, rate_func=smooth),
            AnimationGroup(Write(step1), run_time=2, rate_func=smooth),
        )
        self.wait_beat(1.5)

        self.play(
            AnimationGroup(FadeIn(generic_map, shift=UP * 0.2), run_time=1.8, rate_func=smooth),
            AnimationGroup(TransformMatchingTex(step1, step2), run_time=1.8, rate_func=smooth),
        )
        self.wait_beat(1.5)

        self.play(
            AnimationGroup(TransformMatchingTex(generic_map, concrete_map), run_time=1.8, rate_func=smooth),
            AnimationGroup(TransformMatchingTex(step2, step3), run_time=1.8, rate_func=smooth),
        )

        result_rect = SurroundingRectangle(concrete_map[2], color=Palette.HIGHLIGHT, buff=0.12)
        self.play(Create(result_rect))
        self.play(Indicate(concrete_map[2], color=Palette.HIGHLIGHT))
        self.wait_beat(4)
