import scene_bootstrap  # noqa: F401

import math

from manim import (
    Circle,
    Create,
    DecimalNumber,
    Dot,
    FadeIn,
    FadeOut,
    DOWN,
    LEFT,
    Line,
    MathTex,
    RIGHT,
    RegularPolygon,
    ReplacementTransform,
    Text,
    UP,
    ValueTracker,
    VGroup,
    Write,
)

from style import Layout, Palette
from templates import LayoutTemplateScene


class ArchimedesBoundsDemo(LayoutTemplateScene):
    def _inscribed_polygon(self, n: int, radius: float) -> RegularPolygon:
        return RegularPolygon(
            n=n,
            radius=radius,
            color=Palette.INSCRIBED,
            stroke_width=Layout.STROKE_WIDTH,
        )

    def _circumscribed_polygon(self, n: int, radius: float) -> RegularPolygon:
        # For a regular n-gon around a circle of radius r, polygon circumradius is r / cos(pi/n).
        outer_radius = radius / math.cos(math.pi / n)
        return RegularPolygon(
            n=n,
            radius=outer_radius,
            color=Palette.OBJECT_B,
            stroke_width=Layout.STROKE_WIDTH * 0.75,
            stroke_opacity=0.95,
        )

    def _format_n_latex(self, n: int) -> str:
        if n < 10_000:
            return str(n)
        exponent = int(math.floor(math.log10(n)))
        mantissa = n / (10**exponent)
        return rf"{mantissa:.2f}\times 10^{{{exponent}}}"

    def _n_label(self, n: int, circle: Circle, radius: float, font_size: int = 32) -> MathTex:
        label = MathTex(
            rf"n={self._format_n_latex(n)}",
            color=Palette.MUTED_TEXT,
            font_size=font_size,
        )
        label.move_to(circle.get_center() + UP * (radius * 0.68))
        return label

    def _bounds_for_n(self, n: float) -> tuple[float, float]:
        n_val = max(6.0, float(n))
        return (
            n_val * math.sin(math.pi / n_val),
            n_val * math.tan(math.pi / n_val),
        )

    def _korean_fraction(
        self,
        numerator: str,
        denominator: str,
        font_size: int = 30,
        color: str = Palette.TEXT,
    ) -> VGroup:
        top = Text(numerator, color=color, font_size=font_size)
        bottom = Text(denominator, color=color, font_size=font_size)
        width = max(top.width, bottom.width) + 0.14
        bar = Line(LEFT * (width / 2), RIGHT * (width / 2), color=color, stroke_width=2.1)
        top.next_to(bar, UP, buff=0.05)
        bottom.next_to(bar, DOWN, buff=0.05)
        return VGroup(top, bar, bottom)

    def _bound_equation(self, n: int | None, font_size: int = 40, denominator: str = "2r") -> MathTex:
        if n is None:
            latex = rf"\frac{{P_n^{{\mathrm{{in}}}}}}{{{denominator}}}<\pi<\frac{{P_n^{{\mathrm{{out}}}}}}{{{denominator}}}"
        else:
            latex = rf"\frac{{P_{{{n}}}^{{\mathrm{{in}}}}}}{{{denominator}}}<\pi<\frac{{P_{{{n}}}^{{\mathrm{{out}}}}}}{{{denominator}}}"
        return self.make_equation(latex, font_size=font_size)

    def _right_lane_max_width(self, padding: float = 0.35) -> float:
        _, safe_right = self._safe_x_bounds()
        _, right_x = self._split_x_positions()
        lane_width = 2 * (safe_right - right_x)
        return max(2.5, lane_width - padding)

    def _fit_to_right_lane(self, mobj: MathTex | VGroup, max_width: float) -> MathTex | VGroup:
        if mobj.width > max_width:
            mobj.scale(max_width / mobj.width)
        return mobj

    def _exact_bound_equation_for_n(self, n: int, font_size: int = 44) -> MathTex:
        # Exact bounds in simplified explicit form (no sin/tan display).
        exact_map = {
            6: r"3<\pi<2\sqrt{3}",
            12: r"3(\sqrt{6}-\sqrt{2})<\pi<12(2-\sqrt{3})",
            24: r"6\sqrt{8-2\sqrt{6}-2\sqrt{2}}<\pi<24(\sqrt{6}+\sqrt{2}-\sqrt{3}-2)",
            48: r"24\sqrt{2-\sqrt{2+\sqrt{2+\sqrt{3}}}}<\pi<48\sqrt{\frac{2-\sqrt{2+\sqrt{2+\sqrt{3}}}}{2+\sqrt{2+\sqrt{2+\sqrt{3}}}}}",
            96: r"48\sqrt{2-\sqrt{2+\sqrt{2+\sqrt{2+\sqrt{3}}}}}<\pi<96\sqrt{\frac{2-\sqrt{2+\sqrt{2+\sqrt{2+\sqrt{3}}}}}{2+\sqrt{2+\sqrt{2+\sqrt{2+\sqrt{3}}}}}}",
        }
        latex = exact_map.get(n)
        if latex is not None:
            size = font_size
            if n >= 24:
                size = min(size, 38)
            if n >= 48:
                size = min(size, 33)
            return self.make_equation(latex, font_size=size)

        # Fallback for any other n.
        latex = rf"{n}\sin\left(\frac{{\pi}}{{{n}}}\right)<\pi<{n}\tan\left(\frac{{\pi}}{{{n}}}\right)"
        return self.make_equation(latex, font_size=font_size)

    def _n_value_equation(self, n: int, font_size: int = 40) -> MathTex:
        return self.make_equation(rf"n={self._format_n_latex(n)}", font_size=font_size)

    def _decimal_bound_equation(self, n: int, digits: int = 12, font_size: int = 34) -> MathTex:
        lower, upper = self._bounds_for_n(n)
        return self.make_equation(
            rf"{lower:.{digits}f}<\pi<{upper:.{digits}f}",
            font_size=font_size,
        )

    def _shares_decimal_prefix(self, n: int, digits: int) -> bool:
        lower, upper = self._bounds_for_n(n)
        scale = 10**digits
        return int(lower * scale) == int(upper * scale)

    def construct(self):
        n_label_font_size = 32
        circle_radius = 2.7
        n_steps = [6, 12, 24, 48, 96]
        growth_end_n = 500_000
        decimal_digits = 10
        right_formula_max_width = self._right_lane_max_width()

        circle = Circle(
            radius=circle_radius,
            color=Palette.CIRCLE,
            stroke_width=Layout.STROKE_WIDTH,
            stroke_opacity=0.95,
        )
        center_dot = Dot(circle.get_center(), radius=0.03, color=Palette.WARNING)
        radius_line = Line(
            circle.get_center(),
            circle.get_center() + RIGHT * circle_radius,
            color=Palette.WARNING,
            stroke_width=3.2,
        )
        r_label_intro = MathTex("r=1", color=Palette.WARNING, font_size=34).next_to(radius_line, UP, buff=0.08)

        current_inscribed = self._inscribed_polygon(6, radius=circle_radius).move_to(circle)
        current_circumscribed = self._circumscribed_polygon(6, radius=circle_radius).move_to(circle)
        triangle_fan = VGroup(
            *[
                Line(
                    circle.get_center(),
                    vertex,
                    color=Palette.GRID,
                    stroke_width=2.1,
                    stroke_opacity=0.75,
                )
                for vertex in current_inscribed.get_vertices()
            ]
        )
        intro_shape_group = VGroup(
            circle,
            current_inscribed,
            triangle_fan,
            radius_line,
            center_dot,
            r_label_intro,
        )

        self.layout_center(VGroup(circle, current_circumscribed, current_inscribed))
        self.play(
            Create(circle),
            Create(current_inscribed),
            Create(current_circumscribed),
            run_time=1.2,
        )
        self.wait(2.0)
        self.play(FadeOut(current_circumscribed), run_time=0.5)
        self.play(
            Create(triangle_fan),
            Create(radius_line),
            FadeIn(center_dot),
            Write(r_label_intro),
            run_time=1.0,
        )

        # Intro equations (no decimal approximation here).
        intro_line_1 = VGroup(
            self.make_equation(r"\pi=", font_size=44),
            self._korean_fraction("원의 둘레", "반지름", font_size=30),
        ).arrange(RIGHT, buff=0.16, aligned_edge=DOWN)
        intro_line_2 = VGroup(
            self.make_equation(r">", font_size=44),
            self._korean_fraction("내접 육각형의 둘레", "반지름", font_size=30),
        ).arrange(RIGHT, buff=0.16, aligned_edge=DOWN)
        intro_line_3 = self.make_equation(r"=\frac{6\cdot 1}{2}", font_size=44)
        intro_line_4 = self.make_equation(r"=3", font_size=44)
        intro_equations = VGroup(intro_line_1, intro_line_2, intro_line_3, intro_line_4).arrange(
            DOWN, buff=0.26, aligned_edge=LEFT
        )

        intro_left_target = VGroup(
            circle.copy(),
            current_inscribed.copy(),
            triangle_fan.copy(),
            radius_line.copy(),
            center_dot.copy(),
            r_label_intro.copy(),
        )
        intro_right_target = intro_equations.copy()
        self.layout_split(intro_left_target, intro_right_target)
        intro_equations.move_to(intro_right_target)

        # Geometry moves first, then equations appear.
        self.play(intro_shape_group.animate.move_to(intro_left_target), run_time=1.0)
        self.play(
            Write(intro_line_1),
            Write(intro_line_2),
            Write(intro_line_3),
            Write(intro_line_4),
            run_time=1.6,
        )
        self.wait(2.0)

        # Transition to general-r phase (remove intro-only visuals).
        r_label = MathTex("r", color=Palette.WARNING, font_size=34).move_to(r_label_intro)
        current_circumscribed = self._circumscribed_polygon(6, radius=circle_radius).move_to(circle)
        current_label = self._n_label(6, circle, circle_radius, font_size=n_label_font_size)
        phase2_group = VGroup(
            circle,
            current_circumscribed,
            current_inscribed,
            radius_line,
            center_dot,
            r_label,
            current_label,
        )
        center_target = phase2_group.copy()
        self.layout_center(center_target)

        self.play(
            FadeOut(intro_equations),
            FadeOut(triangle_fan),
            ReplacementTransform(r_label_intro, r_label),
            Create(current_circumscribed),
            FadeIn(current_label),
            VGroup(
                circle,
                current_circumscribed,
                current_inscribed,
                radius_line,
                center_dot,
                r_label,
                current_label,
            ).animate.move_to(center_target),
            run_time=1.1,
        )
        self.wait_beat(0.8)

        # Split again from n=6.
        n_value_line = self._n_value_equation(6, font_size=42)
        c_bound_line = self._fit_to_right_lane(
            self.make_equation(r"P_n^{\mathrm{in}}<C<P_n^{\mathrm{out}}", font_size=42),
            right_formula_max_width,
        )
        pi_bound_general = self._fit_to_right_lane(
            self._bound_equation(None, font_size=44, denominator="2r"),
            right_formula_max_width,
        )
        pi_bound_indexed = self._fit_to_right_lane(
            self._exact_bound_equation_for_n(6, font_size=44),
            right_formula_max_width,
        )

        left_target = VGroup(
            circle.copy(),
            current_circumscribed.copy(),
            current_inscribed.copy(),
            radius_line.copy(),
            center_dot.copy(),
            r_label.copy(),
            current_label.copy(),
        )
        right_target = VGroup(c_bound_line.copy())
        self.layout_split(left_target, right_target)
        c_bound_line.move_to(right_target)
        equation_anchor = right_target.get_center()

        self.play(
            VGroup(
                circle,
                current_circumscribed,
                current_inscribed,
                radius_line,
                center_dot,
                r_label,
                current_label,
            ).animate.move_to(left_target),
            run_time=1.0,
        )
        self.play(Write(c_bound_line), run_time=0.8)
        self.wait_beat(1.0)

        # Show the second formula first (P_n form), hold 1s, then switch to concrete indexed form.
        pi_bound_general.move_to(c_bound_line)
        self.play(ReplacementTransform(c_bound_line, pi_bound_general), run_time=0.8)
        self.wait(1.0)

        pi_bound_indexed.move_to(pi_bound_general)
        n6_stack = VGroup(n_value_line, pi_bound_indexed).arrange(DOWN, buff=0.28)
        n6_stack.move_to(equation_anchor)
        n_value_line.move_to(n6_stack[0])
        self.play(
            ReplacementTransform(pi_bound_general, pi_bound_indexed),
            FadeIn(n_value_line),
            pi_bound_indexed.animate.move_to(n6_stack[1]),
            run_time=0.9,
        )
        bound_line = pi_bound_indexed

        # Grow from n=6 to n=96 first (no decimal text before 96), then pause.
        for n in n_steps[1:]:
            next_label = self._n_label(n, circle, circle_radius, font_size=n_label_font_size)
            next_n_line = self._n_value_equation(n, font_size=42)
            next_bound_line = self._fit_to_right_lane(
                self._exact_bound_equation_for_n(n, font_size=44),
                right_formula_max_width,
            )
            target_stack = VGroup(next_n_line, next_bound_line).arrange(DOWN, buff=0.28)
            target_stack.move_to(equation_anchor)

            next_inscribed = self._inscribed_polygon(n, radius=circle_radius).move_to(circle)
            next_circumscribed = self._circumscribed_polygon(n, radius=circle_radius).move_to(circle)
            self.play(
                ReplacementTransform(current_inscribed, next_inscribed),
                ReplacementTransform(current_circumscribed, next_circumscribed),
                ReplacementTransform(current_label, next_label),
                ReplacementTransform(n_value_line, target_stack[0]),
                ReplacementTransform(bound_line, target_stack[1]),
                run_time=0.72,
            )
            current_inscribed = next_inscribed
            current_circumscribed = next_circumscribed
            current_label = next_label
            n_value_line = target_stack[0]
            bound_line = target_stack[1]

        # At n=96, switch from exact irrational bound to Archimedes' rational bracket.
        rational_96_line = self._fit_to_right_lane(
            self.make_equation(r"\frac{223}{71}<\pi<\frac{22}{7}", font_size=44),
            right_formula_max_width,
        ).move_to(bound_line)
        self.play(ReplacementTransform(bound_line, rational_96_line), run_time=0.75)
        bound_line = rational_96_line

        decimal_line = self._fit_to_right_lane(
            self._decimal_bound_equation(96, digits=decimal_digits, font_size=33),
            right_formula_max_width,
        )
        stack_with_decimal = VGroup(n_value_line.copy(), bound_line.copy(), decimal_line).arrange(DOWN, buff=0.28)
        stack_with_decimal.move_to(equation_anchor)
        decimal_line.move_to(stack_with_decimal[2])
        self.play(
            n_value_line.animate.move_to(stack_with_decimal[0]),
            bound_line.animate.move_to(stack_with_decimal[1]),
            FadeIn(decimal_line),
            run_time=0.7,
        )

        self.wait(2.0)

        # Then grow continuously up to n = 500,000.
        bound_general = self._fit_to_right_lane(
            self._bound_equation(None, font_size=44, denominator="2r"),
            right_formula_max_width,
        ).move_to(bound_line)
        self.play(ReplacementTransform(bound_line, bound_general), run_time=0.5)
        bound_line = bound_general

        # Convert right-side displays to continuously-updating numeric mobjects.
        right_n_prefix = self.make_equation(r"n=", font_size=42)
        right_n_value = DecimalNumber(96, num_decimal_places=0, group_with_commas=True, font_size=42)
        right_n_line = VGroup(right_n_prefix, right_n_value).arrange(RIGHT, buff=0.08).move_to(n_value_line)

        lower_96, upper_96 = self._bounds_for_n(96)
        lower_decimal = DecimalNumber(lower_96, num_decimal_places=decimal_digits, font_size=33)
        mid_pi = self.make_equation(r"<\pi<", font_size=33)
        upper_decimal = DecimalNumber(upper_96, num_decimal_places=decimal_digits, font_size=33)
        right_decimal_line = VGroup(lower_decimal, mid_pi, upper_decimal).arrange(RIGHT, buff=0.08)
        self._fit_to_right_lane(right_decimal_line, right_formula_max_width)
        right_decimal_line.move_to(decimal_line)

        inner_n_prefix = MathTex(r"n=", color=Palette.MUTED_TEXT, font_size=n_label_font_size)
        inner_n_value = DecimalNumber(
            96,
            num_decimal_places=0,
            group_with_commas=True,
            color=Palette.MUTED_TEXT,
            font_size=n_label_font_size,
        )
        inner_n_line = VGroup(inner_n_prefix, inner_n_value).arrange(RIGHT, buff=0.06).move_to(current_label)

        self.play(
            ReplacementTransform(n_value_line, right_n_line),
            ReplacementTransform(decimal_line, right_decimal_line),
            ReplacementTransform(current_label, inner_n_line),
            run_time=0.6,
        )

        n_anchor = right_n_line.get_center()
        decimal_anchor = right_decimal_line.get_center()
        inner_n_anchor = inner_n_line.get_center()

        growth_progress = ValueTracker(0.0)
        growth_start = 96.0
        growth_ratio = growth_end_n / growth_start

        def tracked_n() -> float:
            return growth_start * (growth_ratio ** growth_progress.get_value())

        def tracked_n_int() -> int:
            return max(6, int(round(tracked_n())))

        right_n_value.add_updater(lambda m: m.set_value(tracked_n_int()))
        inner_n_value.add_updater(lambda m: m.set_value(tracked_n_int()))
        lower_decimal.add_updater(lambda m: m.set_value(self._bounds_for_n(tracked_n())[0]))
        upper_decimal.add_updater(lambda m: m.set_value(self._bounds_for_n(tracked_n())[1]))

        right_n_line.add_updater(lambda m: m.arrange(RIGHT, buff=0.08).move_to(n_anchor))
        right_decimal_line.add_updater(lambda m: m.arrange(RIGHT, buff=0.08).move_to(decimal_anchor))
        inner_n_line.add_updater(lambda m: m.arrange(RIGHT, buff=0.06).move_to(inner_n_anchor))

        self.play(growth_progress.animate.set_value(1.0), run_time=6.0, rate_func=lambda t: t)

        self.wait(2.0)
