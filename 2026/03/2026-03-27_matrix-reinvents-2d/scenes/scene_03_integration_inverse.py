import confpath  # noqa: F401

from manim import (
    AnimationGroup,
    DOWN,
    FadeIn,
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


class IntegrationInverse(LayoutTemplateScene):
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
        fs = 32

        inv_def = MathTex(
            r"D^{-1}",
            r"=",
            r"\tfrac12\begin{pmatrix} 1 & 1 \\ -1 & 1 \end{pmatrix}",
            color=Palette.TEXT,
            font_size=fs,
        )
        identity = MathTex(
            r"D^{-1}D",
            r"=",
            r"I",
            color=Palette.TEXT,
            font_size=30,
        )
        bad_matrix = MathTex(
            r"\begin{pmatrix} 0 & 1 \\ 0 & 0 \end{pmatrix}",
            r",\ \det = 0",
            color=Palette.TEXT,
            font_size=30,
        )
        bad_matrix[1].set_color(Palette.OBJECT_C)

        step1 = MathTex(
            r"\int y\,dx = \tfrac12(a+b)e^{x}\sin x + \tfrac12(-a+b)e^{x}\cos x",
            color=Palette.TEXT,
            font_size=fs,
        )
        step2 = MathTex(
            r"\begin{pmatrix} a \\ b \end{pmatrix}",
            r"\mapsto",
            r"\tfrac12\begin{pmatrix} a+b \\ -a+b \end{pmatrix}",
            color=Palette.TEXT,
            font_size=fs,
        )
        step3 = MathTex(
            r"\int (a+bx)\,dx",
            r"=",
            r"ax",
            r"+",
            r"\tfrac12 b x^{2}",
            color=Palette.TEXT,
            font_size=fs,
        )
        step3[4].set_color(Palette.OBJECT_C)

        self._balanced_split(VGroup(inv_def), step1)
        identity.next_to(inv_def, DOWN, buff=0.55, aligned_edge=LEFT)
        bad_matrix.move_to(identity)
        step2.move_to(step1)
        step3.move_to(step1)

        self.play(
            AnimationGroup(Write(inv_def), run_time=2, rate_func=smooth),
            AnimationGroup(Write(step1), run_time=2, rate_func=smooth),
        )
        self.wait_beat(1.5)

        self.play(
            AnimationGroup(FadeIn(identity, shift=UP * 0.2), run_time=1.8, rate_func=smooth),
            AnimationGroup(TransformMatchingTex(step1, step2), run_time=1.8, rate_func=smooth),
        )
        self.play(Indicate(identity[2], color=Palette.HIGHLIGHT))
        self.wait_beat(1.5)

        self.play(
            AnimationGroup(TransformMatchingTex(identity, bad_matrix), run_time=1.8, rate_func=smooth),
            AnimationGroup(TransformMatchingTex(step2, step3), run_time=1.8, rate_func=smooth),
        )
        self.play(Indicate(step3[4], color=Palette.OBJECT_C))
        self.wait_beat(4)
