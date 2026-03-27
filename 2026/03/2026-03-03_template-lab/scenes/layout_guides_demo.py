import scene_bootstrap  # noqa: F401

from manim import (
    Circle,
    Create,
    DashedLine,
    DOWN,
    Dot,
    FadeIn,
    LEFT,
    Rectangle,
    Text,
    UP,
    VGroup,
    Write,
    config,
)

from style import Layout, Palette
from templates import LayoutTemplateScene


class LayoutGuidesDemo(LayoutTemplateScene):
    def _label(self, text: str, color: str, size: int = 20) -> Text:
        return Text(text, font=Layout.UI_FONT, color=color, font_size=size)

    def construct(self):
        half_w = config.frame_width / 2
        half_h = config.frame_height / 2

        safe_left, safe_right = self._safe_x_bounds()
        safe_top = half_h - Layout.MARGIN_TOP
        safe_bottom = -half_h + Layout.MARGIN_BOTTOM

        split_left_x, split_right_x = self._split_x_positions()
        raw_center_y = Layout.CENTER_Y
        shifted_center_y = self._with_global_up_shift(Layout.CENTER_Y)
        shifted_split_y = self._with_global_up_shift(Layout.SPLIT_Y)

        frame_rect = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            stroke_color=Palette.MUTED_TEXT,
            stroke_opacity=0.35,
        )
        safe_rect = Rectangle(
            width=safe_right - safe_left,
            height=safe_top - safe_bottom,
            stroke_color=Palette.WARNING,
            stroke_opacity=0.7,
        ).move_to([(safe_left + safe_right) / 2, (safe_top + safe_bottom) / 2, 0])

        raw_center_line = DashedLine(
            [-half_w, raw_center_y, 0],
            [half_w, raw_center_y, 0],
            color=Palette.MUTED_TEXT,
            dash_length=0.12,
        )
        shifted_center_line = DashedLine(
            [-half_w, shifted_center_y, 0],
            [half_w, shifted_center_y, 0],
            color=Palette.OBJECT_C,
            dash_length=0.12,
        )
        split_y_line = DashedLine(
            [-half_w, shifted_split_y, 0],
            [half_w, shifted_split_y, 0],
            color=Palette.HIGHLIGHT,
            dash_length=0.12,
        )
        split_left_line = DashedLine(
            [split_left_x, -half_h, 0],
            [split_left_x, half_h, 0],
            color=Palette.OBJECT_A,
            dash_length=0.12,
        )
        split_right_line = DashedLine(
            [split_right_x, -half_h, 0],
            [split_right_x, half_h, 0],
            color=Palette.OBJECT_B,
            dash_length=0.12,
        )

        center_dot = Dot([0, shifted_center_y, 0], color=Palette.OBJECT_C, radius=0.055)
        split_left_dot = Dot([split_left_x, shifted_split_y, 0], color=Palette.OBJECT_A, radius=0.055)
        split_right_dot = Dot([split_right_x, shifted_split_y, 0], color=Palette.OBJECT_B, radius=0.055)

        config_panel = VGroup(
            self._label(f"GLOBAL_UP_SHIFT = {Layout.GLOBAL_UP_SHIFT:.2f}", Palette.TEXT),
            self._label(f"SPLIT_CENTER_GAP = {Layout.SPLIT_CENTER_GAP:.2f}", Palette.TEXT),
            self._label(f"SPLIT_LEFT_INSET_X = {Layout.SPLIT_LEFT_INSET_X:.2f}", Palette.TEXT),
            self._label(f"STROKE_WIDTH = {Layout.STROKE_WIDTH:.1f}", Palette.TEXT),
            self._label(f"raw center y = {raw_center_y:.2f}", Palette.MUTED_TEXT),
            self._label(f"shifted center y = {shifted_center_y:.2f}", Palette.OBJECT_C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        config_panel.to_edge(UP + LEFT, buff=0.22)

        guide_labels = VGroup(
            self._label("safe area", Palette.WARNING, 18).next_to(safe_rect, UP, buff=0.08),
            self._label("raw center", Palette.MUTED_TEXT, 18).move_to([safe_left + 1.4, raw_center_y + 0.16, 0]),
            self._label("shifted center", Palette.OBJECT_C, 18).move_to(
                [safe_left + 1.7, shifted_center_y + 0.16, 0]
            ),
            self._label("split left", Palette.OBJECT_A, 18).next_to(split_left_dot, UP, buff=0.08),
            self._label("split right", Palette.OBJECT_B, 18).next_to(split_right_dot, UP, buff=0.08),
        )

        center_sample = Circle(
            radius=0.45,
            color=Palette.OBJECT_C,
            stroke_width=Layout.STROKE_WIDTH,
        )
        self.layout_center(center_sample)

        split_left_sample = Circle(
            radius=0.65,
            color=Palette.OBJECT_A,
            stroke_width=Layout.STROKE_WIDTH,
        )
        split_right_sample = self.make_equation(r"\frac{223}{71}<\pi<\frac{22}{7}", font_size=46)
        self._balanced_split(split_left_sample, split_right_sample)

        sample_labels = VGroup(
            self._label("layout_center()", Palette.OBJECT_C, 18).next_to(center_sample, UP, buff=0.12),
            self._label("layout_split() left", Palette.OBJECT_A, 18).next_to(split_left_sample, DOWN, buff=0.12),
            self._label("layout_split() right", Palette.TEXT, 18).next_to(split_right_sample, DOWN, buff=0.12),
        )

        self.play(Create(frame_rect), Create(safe_rect))
        self.play(
            Create(raw_center_line),
            Create(shifted_center_line),
            Create(split_y_line),
            Create(split_left_line),
            Create(split_right_line),
        )
        self.play(FadeIn(center_dot), FadeIn(split_left_dot), FadeIn(split_right_dot))
        self.play(FadeIn(guide_labels), FadeIn(config_panel))

        self.play(Create(center_sample), Write(sample_labels[0]))
        self.play(Create(split_left_sample), Write(split_right_sample), Write(sample_labels[1]), Write(sample_labels[2]))
        self.wait_beat(2.4)
