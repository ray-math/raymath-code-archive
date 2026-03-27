import scene_bootstrap  # noqa: F401

import math
import random

import numpy as np
from manim import (
    Axes,
    BraceBetweenPoints,
    Create,
    DashedLine,
    DecimalNumber,
    Dot,
    DOWN,
    FadeIn,
    LEFT,
    Line,
    MathTex,
    RIGHT,
    TAU,
    Text,
    UP,
    ValueTracker,
    VGroup,
    Write,
    config,
    linear,
    VMobject,
    always_redraw,
)

from style import Layout, Palette
from templates import LayoutTemplateScene


class GaussianIntegralPi(LayoutTemplateScene):
    """Left-only Gaussian animation with right-side equation."""

    def construct(self):
        axes = Axes(
            x_range=[-4.5, 4.5, 1],
            y_range=[0, 1.15, 0.2],
            x_length=6.6,
            y_length=3.8,
            axis_config={"color": Palette.AXIS, "font_size": 24},
            x_axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False, "include_ticks": False},
            tips=False,
        )
        curve = axes.plot(
            lambda x: np.exp(-(x**2)),
            x_range=[-4.3, 4.3],
            color=Palette.OBJECT_A,
            stroke_width=4,
        )
        area = axes.get_area(curve, x_range=[-4.3, 4.3], color=Palette.OBJECT_A, opacity=0.26)
        baseline = DashedLine(
            axes.c2p(-4.25, 0),
            axes.c2p(4.25, 0),
            color=Palette.GRID,
            dash_length=0.07,
            stroke_opacity=0.5,
            stroke_width=2,
        )

        tail_x = ValueTracker(2.2)
        tail_dot = Dot(
            axes.c2p(tail_x.get_value(), np.exp(-(tail_x.get_value() ** 2))),
            color=Palette.WARNING,
            radius=0.045,
        )
        tail_dot.add_updater(
            lambda mob: mob.move_to(
                axes.c2p(tail_x.get_value(), np.exp(-(tail_x.get_value() ** 2)))
            )
        )
        tail_guide = Line(
            tail_dot.get_center(),
            axes.c2p(tail_x.get_value(), 0),
            color=Palette.WARNING,
            stroke_width=2,
        )
        tail_guide.add_updater(
            lambda mob: mob.put_start_and_end_on(
                tail_dot.get_center(), axes.c2p(tail_x.get_value(), 0)
            )
        )
        zero_marker = Line(
            axes.c2p(4.05, 0),
            axes.c2p(4.28, 0),
            color=Palette.WARNING,
            stroke_width=2,
            stroke_opacity=0.85,
        )
        zero_label = Text("0", color=Palette.WARNING, font_size=24).next_to(
            zero_marker, UP, buff=0.05
        )

        visual = VGroup(axes, baseline, area, curve, tail_guide, tail_dot, zero_marker, zero_label)
        equation = self.make_equation(r"\int_{-\infty}^{\infty} e^{-x^2}\,dx=\sqrt{\pi}", font_size=58)
        self._balanced_split(visual, equation)

        visual.save_state()

        self.play(Create(axes), Create(curve), FadeIn(area), Write(equation), run_time=1.8)
        self.play(FadeIn(tail_dot), Create(tail_guide), FadeIn(zero_marker), FadeIn(zero_label), run_time=0.8)

        # Progressive zoom-in to show the tail approaching zero.
        self.play(
            tail_x.animate.set_value(3.45),
            visual.animate.scale(1.35, about_point=axes.c2p(3.3, 0.04)).shift(LEFT * 0.2),
            run_time=4.0,
            rate_func=linear,
        )
        self.play(
            tail_x.animate.set_value(3.92),
            visual.animate.scale(1.45, about_point=axes.c2p(3.86, 0.007)).shift(LEFT * 0.28),
            run_time=4.0,
            rate_func=linear,
        )
        self.play(
            tail_x.animate.set_value(4.17),
            visual.animate.scale(1.55, about_point=axes.c2p(4.1, 0.0012)).shift(LEFT * 0.25),
            run_time=4.0,
            rate_func=linear,
        )
        self.play(
            tail_x.animate.set_value(4.27),
            visual.animate.scale(1.45, about_point=axes.c2p(4.24, 0.00035)).shift(LEFT * 0.2),
            run_time=3.0,
            rate_func=linear,
        )
        tail_dot.clear_updaters()
        tail_guide.clear_updaters()
        self.wait_beat(2)


class BuffonNeedlePi(LayoutTemplateScene):
    """Needle experiment with aligned geometry and live pi-convergence display."""

    def construct(self):
        spacing = 0.8
        needle_length = 0.62
        x_span = 2.2
        y_min, y_max = -1.6, 1.6

        floor_lines = VGroup(
            *[
                Line(
                    np.array([-x_span, y_val, 0.0]),
                    np.array([x_span, y_val, 0.0]),
                    color=Palette.GRID,
                    stroke_width=2,
                    stroke_opacity=0.62,
                )
                for y_val in np.arange(y_min, y_max + 1e-6, spacing)
            ]
        )
        frame_box = VGroup(
            Line(
                np.array([-x_span, y_min, 0.0]),
                np.array([-x_span, y_max, 0.0]),
                color=Palette.GRID,
                stroke_opacity=0.35,
            ),
            Line(
                np.array([x_span, y_min, 0.0]),
                np.array([x_span, y_max, 0.0]),
                color=Palette.GRID,
                stroke_opacity=0.35,
            ),
        )
        needles = VGroup()

        n_tracker = ValueTracker(0.0)
        p_tracker = ValueTracker(0.0)
        pi_tracker = ValueTracker(0.0)

        n_value = DecimalNumber(
            0.0,
            num_decimal_places=0,
            include_sign=False,
            font_size=32,
            color=Palette.TEXT,
        )
        n_value.add_updater(lambda mob: mob.set_value(n_tracker.get_value()))
        n_display = VGroup(
            MathTex(r"n=", color=Palette.TEXT, font_size=32),
            n_value,
        ).arrange(RIGHT, buff=0.08)

        p_value = DecimalNumber(
            0.0,
            num_decimal_places=3,
            include_sign=False,
            font_size=32,
            color=Palette.TEXT,
        )
        p_value.add_updater(lambda mob: mob.set_value(p_tracker.get_value()))
        p_display = VGroup(
            MathTex(r"P\approx", color=Palette.TEXT, font_size=32),
            p_value,
        ).arrange(RIGHT, buff=0.08)
        stats_display = VGroup(n_display, p_display).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15
        )
        stats_display.next_to(floor_lines, DOWN, buff=0.25)

        visual = VGroup(floor_lines, frame_box, needles, stats_display)

        eq_formula = MathTex(
            r"\pi=\frac{2\ell}{dP}",
            color=Palette.TEXT,
            font_size=60,
        )
        pi_value = DecimalNumber(
            0.0,
            num_decimal_places=3,
            include_sign=False,
            font_size=46,
            color=Palette.HIGHLIGHT,
        )
        pi_value.add_updater(lambda mob: mob.set_value(pi_tracker.get_value()))
        pi_estimate = VGroup(
            MathTex(r"\hat{\pi}\approx", color=Palette.HIGHLIGHT, font_size=46),
            pi_value,
        ).arrange(RIGHT, buff=0.12)
        equations = VGroup(eq_formula, pi_estimate).arrange(
            DOWN, buff=0.55, aligned_edge=LEFT
        )

        self._balanced_split(visual, equations)
        panel_offset = floor_lines.get_center()

        # Left animation and right equations start together.
        self.play(
            Create(floor_lines),
            FadeIn(frame_box),
            FadeIn(stats_display),
            Write(eq_formula),
            FadeIn(pi_estimate),
            run_time=1.0,
        )

        rng = random.Random(21)
        hits = 0
        throws = 0
        total_throws = 200
        needle_fade_time = 1 / config.frame_rate

        for _ in range(total_throws):
            cx = float(rng.uniform(-x_span + needle_length / 2, x_span - needle_length / 2))
            cy = float(rng.uniform(y_min + 0.08, y_max - 0.08))
            theta = float(rng.uniform(0.0, math.pi))

            dx = 0.5 * needle_length * math.cos(theta)
            dy = 0.5 * needle_length * math.sin(theta)

            nearest_line_y = round(cy / spacing) * spacing
            is_hit = abs(cy - nearest_line_y) <= abs(dy)

            p1 = np.array([cx - dx, cy - dy, 0.0]) + panel_offset
            p2 = np.array([cx + dx, cy + dy, 0.0]) + panel_offset
            needle = Line(
                p1,
                p2,
                color=Palette.POSITIVE if is_hit else Palette.NEGATIVE,
                stroke_width=5,
            )

            throws += 1
            if is_hit:
                hits += 1

            p_hat = hits / throws
            pi_hat = 2 * needle_length / (spacing * p_hat) if hits > 0 else 0.0

            self.play(
                FadeIn(needle, shift=DOWN * 0.2),
                n_tracker.animate.set_value(throws),
                p_tracker.animate.set_value(p_hat),
                pi_tracker.animate.set_value(pi_hat),
                run_time=needle_fade_time,
            )
            needles.add(needle)

        self.wait(10)
        n_value.clear_updaters()
        p_value.clear_updaters()
        pi_value.clear_updaters()
        self.wait_beat(2)


class BaselSeriesPi(LayoutTemplateScene):
    """Histogram of 1/n^2 + cumulative graph approaching pi^2/6."""

    def construct(self):
        n_max = 12
        target = (math.pi**2) / 6

        axes = Axes(
            x_range=[0, n_max + 0.5, 1],
            y_range=[0, 1.8, 0.2],
            x_length=4.8,
            y_length=3.5,
            axis_config={"color": Palette.AXIS, "font_size": 24},
            y_axis_config={"include_ticks": False},
            tips=False,
        )

        target_line = DashedLine(
            axes.c2p(0, target),
            axes.c2p(n_max + 0.3, target),
            color=Palette.HIGHLIGHT,
            dash_length=0.08,
            stroke_width=2.5,
        )
        target_label = MathTex(
            r"\frac{\pi^2}{6}",
            color=Palette.HIGHLIGHT,
            font_size=32,
        ).next_to(axes.c2p(0, target), LEFT, buff=0.12)

        bars = VGroup()
        term_labels = VGroup()
        cumulative_segments = VGroup()
        sum_dot = Dot(axes.c2p(0, 0), color=Palette.OBJECT_B, radius=0.055)

        sum_tracker = ValueTracker(0.0)
        sum_value = DecimalNumber(
            0.0,
            num_decimal_places=3,
            include_sign=False,
            font_size=32,
            color=Palette.TEXT,
        )
        sum_value.add_updater(lambda mob: mob.set_value(sum_tracker.get_value()))
        sum_display = VGroup(
            MathTex(r"S_n\approx", color=Palette.TEXT, font_size=32),
            sum_value,
        ).arrange(RIGHT, buff=0.1)
        sum_display.next_to(axes, DOWN, buff=0.28)

        visual = VGroup(
            axes,
            target_line,
            target_label,
            bars,
            term_labels,
            cumulative_segments,
            sum_dot,
            sum_display,
        )

        equation = self.make_equation(
            r"\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{6}",
            font_size=54,
        )

        self._balanced_split(visual, equation)

        # Left animation and right equation start together.
        self.play(
            Create(axes),
            FadeIn(target_line),
            Write(target_label),
            Write(equation),
            FadeIn(sum_display),
            run_time=1.0,
        )

        partial = 0.0
        prev_point = axes.c2p(0, 0)
        for n in range(1, n_max + 1):
            term = 1.0 / (n * n)
            bar = Line(
                axes.c2p(n, 0),
                axes.c2p(n, term),
                color=Palette.OBJECT_A,
                stroke_width=27,
            )
            label_latex = r"1" if n == 1 else rf"\frac{{1}}{{{n}^2}}"
            term_label = MathTex(
                label_latex,
                color=Palette.MUTED_TEXT,
                font_size=20,
            ).next_to(axes.c2p(n, term), UP, buff=0.08)

            partial += term
            next_point = axes.c2p(n, partial)
            segment = Line(
                prev_point,
                next_point,
                color=Palette.OBJECT_B,
                stroke_width=4,
            )

            animations = [
                Create(bar),
                Create(segment),
                sum_dot.animate.move_to(next_point),
                sum_tracker.animate.set_value(partial),
                FadeIn(term_label),
            ]
            self.play(*animations, run_time=max(0.08, 0.22 - 0.008 * n))
            bars.add(bar)
            term_labels.add(term_label)
            cumulative_segments.add(segment)
            prev_point = next_point

        self.wait(10)
        sum_value.clear_updaters()
        self.wait_beat(2)


class PendulumPeriodPi(LayoutTemplateScene):
    """Angle definition, period meaning, and length label following the rod."""

    def construct(self):
        theta_max = 35 * math.pi / 180
        length = 2.15
        period = 2.6

        time_tracker = ValueTracker(0.0)
        pivot = Dot(UP * 1.25, radius=0.022, color=Palette.AXIS)

        support = Line(
            pivot.get_center() + LEFT * 0.82,
            pivot.get_center() + RIGHT * 0.82,
            color=Palette.AXIS,
            stroke_width=6,
        )
        center_line = DashedLine(
            pivot.get_center(),
            pivot.get_center() + DOWN * length,
            color=Palette.GRID,
            dash_length=0.08,
            stroke_opacity=0.55,
        )

        def theta_value() -> float:
            return theta_max * math.cos(TAU * time_tracker.get_value() / period)

        def bob_point() -> np.ndarray:
            theta = theta_value()
            return pivot.get_center() + np.array(
                [length * math.sin(theta), -length * math.cos(theta), 0.0]
            )

        def perp_offset(vec: np.ndarray, mag: float) -> np.ndarray:
            norm = np.linalg.norm(vec[:2])
            if norm < 1e-8:
                return np.array([0.0, 0.0, 0.0])
            return np.array([-vec[1], vec[0], 0.0]) / norm * mag

        rod = Line(pivot.get_center(), bob_point(), color=Palette.OBJECT_A, stroke_width=5)
        bob = Dot(bob_point(), radius=0.095, color=Palette.HIGHLIGHT)

        l_label = MathTex(r"L", color=Palette.TEXT, font_size=32)

        phase_axes = Axes(
            x_range=[0, period, period / 2],
            y_range=[-theta_max, theta_max, theta_max],
            x_length=3.6,
            y_length=1.25,
            axis_config={"color": Palette.GRID, "stroke_opacity": 0.65, "font_size": 20},
            tips=False,
        )
        phase_curve = phase_axes.plot(
            lambda t: theta_max * math.cos(TAU * t / period),
            x_range=[0, period],
            color=Palette.OBJECT_B,
            stroke_width=3,
        )
        VGroup(phase_axes, phase_curve).move_to(pivot.get_center() + DOWN * 2.95)

        phase_dot = Dot(
            phase_axes.c2p(0, theta_max),
            color=Palette.HIGHLIGHT,
            radius=0.045,
        )
        phase_dot.add_updater(
            lambda mob: mob.move_to(
                phase_axes.c2p(
                    min(time_tracker.get_value(), period),
                    theta_max * math.cos(TAU * min(time_tracker.get_value(), period) / period),
                )
            )
        )

        period_brace = BraceBetweenPoints(
            phase_axes.c2p(0, -theta_max * 1.05),
            phase_axes.c2p(period, -theta_max * 1.05),
            direction=DOWN,
            color=Palette.TEXT,
        )
        time_label = Text("Time", color=Palette.TEXT, font_size=32)
        time_label.next_to(period_brace, DOWN, buff=0.12)
        l_label.move_to(
            0.5 * (pivot.get_center() + bob_point())
            + perp_offset(bob_point() - pivot.get_center(), 0.18)
        )

        rod.add_updater(lambda mob: mob.put_start_and_end_on(pivot.get_center(), bob_point()))
        bob.add_updater(lambda mob: mob.move_to(bob_point()))
        l_label.add_updater(
            lambda mob: mob.move_to(
                0.5 * (pivot.get_center() + bob_point())
                + perp_offset(bob_point() - pivot.get_center(), 0.18)
            )
        )

        visual = VGroup(
            support,
            center_line,
            pivot,
            rod,
            bob,
            l_label,
            phase_axes,
            phase_curve,
            phase_dot,
            period_brace,
            time_label,
        )

        eq_main = self.make_equation(r"T=2\pi\sqrt{\frac{L}{g}}", font_size=58)

        self._balanced_split(visual, eq_main)

        # Left animation and right equation start together.
        self.play(
            Create(support),
            Create(center_line),
            FadeIn(pivot),
            FadeIn(rod),
            FadeIn(bob),
            FadeIn(l_label),
            Create(phase_axes),
            Create(phase_curve),
            FadeIn(phase_dot),
            FadeIn(period_brace),
            FadeIn(time_label),
            Write(eq_main),
            run_time=1.2,
        )

        self.play(time_tracker.animate.set_value(period), run_time=3.6, rate_func=linear)
        self.wait(10)

        rod.clear_updaters()
        bob.clear_updaters()
        l_label.clear_updaters()
        phase_dot.clear_updaters()
        self.wait_beat(2)


class PiFourMiddleAnimationsOnly(LayoutTemplateScene):
    """20s center-only 2x2 animation collage (compact layout)."""

    def construct(self):
        centers = {
            "gauss": LEFT * 1.95 + UP * 1.08,
            "buffon": RIGHT * 1.95 + UP * 1.08,
            "basel": LEFT * 1.95 + DOWN * 1.08,
            "pendulum": RIGHT * 1.95 + DOWN * 1.08,
        }

        # Gaussian: compact bell curve with moving tail dot.
        gauss_axes = Axes(
            x_range=[-4.4, 4.4, 1],
            y_range=[0, 1.15, 0.3],
            x_length=2.35,
            y_length=1.3,
            axis_config={"color": Palette.AXIS, "include_numbers": False},
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_ticks": False},
            tips=False,
        ).move_to(centers["gauss"])
        gauss_curve = gauss_axes.plot(
            lambda x: np.exp(-(x**2)),
            x_range=[-4.3, 4.3],
            color=Palette.OBJECT_A,
            stroke_width=3,
        )
        gauss_area = gauss_axes.get_area(
            gauss_curve, x_range=[-4.3, 4.3], color=Palette.OBJECT_A, opacity=0.24
        )
        gauss_tail_clock = ValueTracker(0.0)
        gauss_tail_clock.add_updater(lambda mob, dt: mob.increment_value(dt))

        def _gauss_tail_x() -> float:
            phase = (gauss_tail_clock.get_value() % 5.4) / 5.4
            return 2.2 + 2.05 * ((1 - math.exp(-4.2 * phase)) / (1 - math.exp(-4.2)))

        gauss_tail_dot = always_redraw(
            lambda: Dot(
                gauss_axes.c2p(_gauss_tail_x(), np.exp(-(_gauss_tail_x() ** 2))),
                color=Palette.WARNING,
                radius=0.03,
            )
        )
        gauss_tail_guide = always_redraw(
            lambda: DashedLine(
                gauss_tail_dot.get_center(),
                gauss_axes.c2p(_gauss_tail_x(), 0),
                color=Palette.WARNING,
                dash_length=0.03,
                stroke_width=1.6,
            )
        )

        # Buffon: 200 needles in 20s, keep all dropped needles.
        spacing = 0.33
        needle_length = 0.23
        x_span = 1.02
        y_min, y_max = -0.66, 0.66
        buffon_floor = VGroup(
            *[
                Line(
                    np.array([-x_span, y, 0.0]),
                    np.array([x_span, y, 0.0]),
                    color=Palette.GRID,
                    stroke_width=1.6,
                    stroke_opacity=0.62,
                )
                for y in np.arange(y_min, y_max + 1e-6, spacing)
            ]
        ).move_to(centers["buffon"])
        buffon_frame = VGroup(
            Line(
                np.array([-x_span, y_min, 0.0]),
                np.array([-x_span, y_max, 0.0]),
                color=Palette.GRID,
                stroke_opacity=0.4,
                stroke_width=1.6,
            ),
            Line(
                np.array([x_span, y_min, 0.0]),
                np.array([x_span, y_max, 0.0]),
                color=Palette.GRID,
                stroke_opacity=0.4,
                stroke_width=1.6,
            ),
        ).move_to(centers["buffon"])
        needle_group = VGroup()
        buffon_offset = buffon_floor.get_center()

        rng = random.Random(21)
        drop_offset = np.array([0.0, 0.16, 0.0])
        spawn_interval = 20.0 / 200.0
        drop_time = 0.1
        buffon_state = {"spawn_acc": 0.0, "needles": [], "throws": 0}

        def _spawn_needle():
            cx = float(rng.uniform(-x_span + needle_length / 2, x_span - needle_length / 2))
            cy = float(rng.uniform(y_min + 0.03, y_max - 0.03))
            theta = float(rng.uniform(0.0, math.pi))

            dx = 0.5 * needle_length * math.cos(theta)
            dy = 0.5 * needle_length * math.sin(theta)
            nearest_line_y = round(cy / spacing) * spacing
            hit = abs(cy - nearest_line_y) <= abs(dy)

            end1 = np.array([cx - dx, cy - dy, 0.0]) + buffon_offset
            end2 = np.array([cx + dx, cy + dy, 0.0]) + buffon_offset
            start1 = end1 + drop_offset
            start2 = end2 + drop_offset
            needle = Line(
                start1,
                start2,
                color=Palette.POSITIVE if hit else Palette.NEGATIVE,
                stroke_width=2.2,
            )
            needle_group.add(needle)
            buffon_state["needles"].append(
                {"mob": needle, "start1": start1, "start2": start2, "end1": end1, "end2": end2, "age": 0.0}
            )
            buffon_state["throws"] += 1

        def _update_needles(group, dt):
            buffon_state["spawn_acc"] += dt
            while buffon_state["throws"] < 200 and buffon_state["spawn_acc"] >= spawn_interval:
                buffon_state["spawn_acc"] -= spawn_interval
                _spawn_needle()
            for meta in buffon_state["needles"]:
                meta["age"] += dt
                if meta["age"] < drop_time:
                    alpha = meta["age"] / drop_time
                    p1 = meta["start1"] + alpha * (meta["end1"] - meta["start1"])
                    p2 = meta["start2"] + alpha * (meta["end2"] - meta["start2"])
                    meta["mob"].put_start_and_end_on(p1, p2)
                else:
                    meta["mob"].put_start_and_end_on(meta["end1"], meta["end2"])

        needle_group.add_updater(_update_needles)

        # Basel: narrower histogram + fewer bars.
        n_terms = 7
        target = (math.pi**2) / 6
        basel_axes = Axes(
            x_range=[0, n_terms + 0.5, 1],
            y_range=[0, 1.8, 0.3],
            x_length=2.7,
            y_length=1.2,
            axis_config={"color": Palette.AXIS, "include_numbers": False},
            x_axis_config={"include_ticks": False},
            y_axis_config={"include_ticks": False},
            tips=False,
        ).move_to(centers["basel"])
        basel_target_line = DashedLine(
            basel_axes.c2p(0, target),
            basel_axes.c2p(n_terms + 0.2, target),
            color=Palette.HIGHLIGHT,
            dash_length=0.06,
            stroke_width=1.8,
        )
        terms = [1.0 / (n * n) for n in range(1, n_terms + 1)]
        sum_points = [basel_axes.c2p(0, 0)]
        partial = 0.0
        for n, term in enumerate(terms, start=1):
            partial += term
            sum_points.append(basel_axes.c2p(n, partial))

        basel_motion_duration = 8.0
        basel_clock = ValueTracker(0.0)
        basel_clock.add_updater(lambda mob, dt: mob.increment_value(dt))

        def _basel_phase():
            progress = np.clip(basel_clock.get_value() / basel_motion_duration, 0.0, 1.0)
            return progress * n_terms

        def _current_basel_point():
            phase = _basel_phase()
            i = int(phase)
            frac = phase - i
            p0 = sum_points[i]
            p1 = sum_points[min(i + 1, n_terms)]
            return p0 + frac * (p1 - p0)

        def _build_basel_bars():
            phase = _basel_phase()
            full = int(phase)
            frac = phase - full
            bars = VGroup()
            for n in range(1, full + 1):
                bars.add(
                    Line(
                        basel_axes.c2p(n, 0),
                        basel_axes.c2p(n, terms[n - 1]),
                        color=Palette.OBJECT_A,
                        stroke_width=8,
                    )
                )
            if full < n_terms:
                n = full + 1
                bars.add(
                    Line(
                        basel_axes.c2p(n, 0),
                        basel_axes.c2p(n, terms[n - 1] * frac),
                        color=Palette.OBJECT_A,
                        stroke_width=8,
                    )
                )
            return bars

        def _build_sum_curve():
            phase = _basel_phase()
            i = int(phase)
            points = [sum_points[0]]
            if i >= 1:
                points.extend(sum_points[1 : i + 1])
            points.append(_current_basel_point())
            if len(points) < 2:
                points.append(points[0] + RIGHT * 1e-3)
            curve = VMobject(color=Palette.OBJECT_B, stroke_width=3)
            curve.set_points_as_corners(points)
            return curve

        basel_bars = always_redraw(_build_basel_bars)
        basel_curve = always_redraw(_build_sum_curve)
        basel_dot = always_redraw(lambda: Dot(_current_basel_point(), color=Palette.OBJECT_B, radius=0.038))

        # Pendulum only.
        pendulum_time = ValueTracker(0.0)
        pendulum_time.add_updater(lambda mob, dt: mob.increment_value(dt))
        theta_max = 34 * math.pi / 180
        length = 0.95
        period = 2.2
        pivot = Dot(centers["pendulum"] + UP * 0.52, radius=0.025, color=Palette.AXIS)
        support = Line(
            pivot.get_center() + LEFT * 0.48,
            pivot.get_center() + RIGHT * 0.48,
            color=Palette.AXIS,
            stroke_width=3.2,
        )

        def _theta():
            return theta_max * math.cos(TAU * pendulum_time.get_value() / period)

        def _bob_point():
            th = _theta()
            return pivot.get_center() + np.array([length * math.sin(th), -length * math.cos(th), 0.0])

        rod = Line(pivot.get_center(), _bob_point(), color=Palette.OBJECT_A, stroke_width=3.1)
        bob = Dot(_bob_point(), radius=0.058, color=Palette.HIGHLIGHT)
        rod.add_updater(lambda mob: mob.put_start_and_end_on(pivot.get_center(), _bob_point()))
        bob.add_updater(lambda mob: mob.move_to(_bob_point()))

        # Trackers must be in scene to run updaters.
        self.add(gauss_tail_clock, basel_clock, pendulum_time)

        self.add(
            gauss_axes,
            gauss_area,
            gauss_curve,
            gauss_tail_guide,
            gauss_tail_dot,
            buffon_floor,
            buffon_frame,
            needle_group,
            basel_axes,
            basel_target_line,
            basel_bars,
            basel_curve,
            basel_dot,
            support,
            pivot,
            rod,
            bob,
        )

        # Stop Gaussian/Basel motion after they finish their short movement.
        self.wait(basel_motion_duration)
        gauss_tail_clock.clear_updaters()
        basel_clock.clear_updaters()
        basel_clock.set_value(basel_motion_duration)
        self.wait(12.0)

        needle_group.clear_updaters()
        pendulum_time.clear_updaters()
        rod.clear_updaters()
        bob.clear_updaters()
        self.wait_beat(2)
