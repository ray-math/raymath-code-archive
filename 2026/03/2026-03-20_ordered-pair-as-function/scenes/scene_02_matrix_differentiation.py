import scene_bootstrap  # noqa: F401

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
    UP,
    VGroup,
    Write,
    smooth,
)

from style import Layout, Palette
from templates import LayoutTemplateScene


class MatrixDifferentiation(LayoutTemplateScene):
    def construct(self):
        fs = 36  # 좌우 동일 폰트, 큰 값으로 시작

        # ── LEFT: Simple matrix operation ──
        mat_def = MathTex(
            r"D", r"=",
            r"\begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix}",
            color=Palette.TEXT, font_size=fs,
        )

        mat_mult = MathTex(
            r"\begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix}",
            r"\begin{pmatrix} 3 \\ 5 \end{pmatrix}",
            r"=",
            r"\begin{pmatrix} -2 \\ 8 \end{pmatrix}",
            color=Palette.TEXT, font_size=fs,
        )
        mat_mult[3].set_color(Palette.HIGHLIGHT)

        mat_mult.next_to(mat_def, DOWN, buff=0.45, aligned_edge=LEFT)
        visual = VGroup(mat_def, mat_mult)

        # ── RIGHT: Complex traditional derivative (same font) ──
        line1 = MathTex(
            r"\frac{d}{dx}",
            r"\bigl( 3e^{x}\sin x + 5e^{x}\cos x \bigr)",
            color=Palette.TEXT, font_size=fs,
        )
        line2 = MathTex(
            r"= 3", r"(e^{x}\sin x + e^{x}\cos x)",
            color=Palette.TEXT, font_size=fs,
        )
        line3 = MathTex(
            r"+ 5", r"(e^{x}\cos x - e^{x}\sin x)",
            color=Palette.TEXT, font_size=fs,
        )
        line4 = MathTex(
            r"=", r"-2", r"e^{x}\sin x", r"+", r"8", r"e^{x}\cos x",
            color=Palette.TEXT, font_size=fs,
        )
        line4[1].set_color(Palette.HIGHLIGHT)
        line4[4].set_color(Palette.HIGHLIGHT)

        line2.next_to(line1, DOWN, buff=0.15, aligned_edge=LEFT)
        line3.next_to(line2, DOWN, buff=0.08, aligned_edge=LEFT)
        line4.next_to(line3, DOWN, buff=0.2, aligned_edge=LEFT)
        right_eq = VGroup(line1, line2, line3, line4)

        # ── Position: balanced split — equal margins guaranteed ──
        self._balanced_split(visual, right_eq, gap=0.6)

        # ── Phase 1: D definition + derivative question ──
        self.play(
            AnimationGroup(Write(mat_def), run_time=2, rate_func=smooth),
            AnimationGroup(Write(line1), run_time=2, rate_func=smooth),
        )
        self.wait_beat(2)

        # ── Phase 2: Right expands step by step, Left shows result ──
        self.play(
            AnimationGroup(
                FadeIn(mat_mult, shift=DOWN * 0.3),
                run_time=2, rate_func=smooth,
            ),
            AnimationGroup(
                Write(line2), Write(line3),
                run_time=2, rate_func=smooth,
            ),
        )
        self.wait_beat(2)

        # ── Phase 3: Both sides arrive at (-2, 8) ──
        result_rect = SurroundingRectangle(
            mat_mult[3], color=Palette.HIGHLIGHT, buff=0.1,
        )
        self.play(
            AnimationGroup(
                Create(result_rect),
                run_time=1.5, rate_func=smooth,
            ),
            AnimationGroup(
                Write(line4),
                run_time=1.5, rate_func=smooth,
            ),
        )
        self.wait_beat(2)

        # ── Phase 4: Highlight matching coefficients ──
        self.play(
            Indicate(mat_mult[3], color=Palette.HIGHLIGHT),
            Indicate(line4[1], color=Palette.HIGHLIGHT),
            Indicate(line4[4], color=Palette.HIGHLIGHT),
        )

        self.wait_beat(4)
