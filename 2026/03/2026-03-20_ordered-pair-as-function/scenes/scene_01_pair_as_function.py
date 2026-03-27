import scene_bootstrap  # noqa: F401

import numpy as np
from manim import (
    always_redraw,
    AnimationGroup,
    Axes,
    Create,
    DecimalNumber,
    MathTex,
    RIGHT,
    TransformMatchingTex,
    UP,
    VGroup,
    ValueTracker,
    Write,
    smooth,
)

from style import Layout, Palette
from templates import LayoutTemplateScene


class PairAsFunction(LayoutTemplateScene):
    def construct(self):
        fs = 36  # 큰 값으로 시작, _balanced_split이 자동 조정

        # ── Parameters ──
        tracker_a = ValueTracker(0.0)
        tracker_b = ValueTracker(0.0)

        # ── Left: axes + dynamic curve + live (a, b) label ──
        axes = Axes(
            x_range=[0, 1.8, 0.5],
            y_range=[-10, 18, 5],
            x_length=5.0,
            y_length=3.9,
            axis_config={"color": Palette.AXIS},
            tips=False,
        )

        curve = always_redraw(
            lambda: axes.plot(
                lambda x: (
                    tracker_a.get_value() * np.exp(x) * np.sin(x)
                    + tracker_b.get_value() * np.exp(x) * np.cos(x)
                ),
                x_range=[0, 1.7],
                color=Palette.OBJECT_A,
            )
        )

        pair_label = VGroup(
            MathTex(r"(", color=Palette.TEXT, font_size=44),
            DecimalNumber(0, num_decimal_places=1, color=Palette.HIGHLIGHT, font_size=44),
            MathTex(r",", color=Palette.TEXT, font_size=44),
            DecimalNumber(0, num_decimal_places=1, color=Palette.HIGHLIGHT, font_size=44),
            MathTex(r")", color=Palette.TEXT, font_size=44),
        ).arrange(RIGHT, buff=0.1)
        pair_label[1].add_updater(lambda m: m.set_value(tracker_a.get_value()))
        pair_label[3].add_updater(lambda m: m.set_value(tracker_b.get_value()))
        pair_label.add_updater(lambda m: m.next_to(axes, UP, buff=0.18))

        visual = VGroup(axes, curve, pair_label)

        # ── Right: mapping equation ──
        eq = MathTex(
            r"(a,\; b)",
            r"\;\longleftrightarrow\;",
            r"a e^{x}\sin x + b e^{x}\cos x",
            color=Palette.TEXT, font_size=fs,
        )

        # Concrete version (prepared ahead for simultaneous transform)
        eq_concrete = MathTex(
            r"(3,\; 5)",
            r"\;\longleftrightarrow\;",
            r"3 e^{x}\sin x + 5 e^{x}\cos x",
            color=Palette.TEXT, font_size=fs,
        )

        # ── Position: balanced split — equal margins guaranteed ──
        self._balanced_split(visual, eq, gap=0.6)
        eq_concrete.move_to(eq)

        # ── Phase 1: Draw axes + write equation simultaneously ──
        self.play(
            AnimationGroup(Create(axes), run_time=2, rate_func=smooth),
            AnimationGroup(Write(eq), run_time=2, rate_func=smooth),
        )

        # ── Phase 2: Graph + (a,b) label + right equation ALL change together ──
        self.add(curve, pair_label)
        self.play(
            AnimationGroup(
                tracker_a.animate.set_value(3.0),
                tracker_b.animate.set_value(5.0),
                run_time=3, rate_func=smooth,
            ),
            AnimationGroup(
                TransformMatchingTex(eq, eq_concrete),
                run_time=3, rate_func=smooth,
            ),
        )

        # Clean up updaters
        pair_label[1].clear_updaters()
        pair_label[3].clear_updaters()
        pair_label.clear_updaters()

        self.wait_beat(4)
