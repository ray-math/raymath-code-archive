from manim import *

class ColumnSpaceProjection(ThreeDScene):
    def construct(self):
        # 카메라 설정
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        
        # 벡터 시작점 (원점보다 왼쪽)
        start_point = np.array([-2, -1, 0])
        
        # 보조 함수: 화살표를 시작점에서 끝점으로 자연스럽게 성장시킴
        def animate_arrow(start, end, color, extra_anims=None, run_time=1.5):
            tracker = ValueTracker(0)
            direction = end - start
            unit_dir = direction / np.linalg.norm(direction)

            body = always_redraw(
                lambda: Line3D(
                    start=start,
                    end=start + tracker.get_value() * direction,
                    color=color,
                    thickness=0.02,
                )
            )
            tip = always_redraw(
                lambda: Cone(
                    base_radius=0.08,
                    height=0.15,
                    direction=unit_dir,
                    resolution=(12, 8),
                )
                .move_to(start + tracker.get_value() * direction - 0.075 * unit_dir)
                .set_color(color)
            )

            self.add(body, tip)
            animations = [tracker.animate.set_value(1)]
            if extra_anims:
                animations.extend(extra_anims)
            self.play(*animations, run_time=run_time, rate_func=linear)

            body.clear_updaters()
            tip.clear_updaters()
            self.remove(body, tip)

            arrow = Arrow3D(
                start=start,
                end=end,
                color=color,
                thickness=0.02,
                height=0.3,
                base_radius=0.08,
            )
            self.add(arrow)
            return arrow

        # W 평면 생성 (회색 격자)
        plane = Surface(
            lambda u, v: np.array([u, v, 0]),
            u_range=[-4, 4],
            v_range=[-3, 3],
            resolution=(2, 2),
        )
        plane.set_fill(color=GRAY_D, opacity=0.5)
        plane.set_style(stroke_width=0)

        grid_lines = VGroup()
        for x in np.linspace(-4, 4, 9):
            grid_lines.add(
                Line3D(
                    start=np.array([x, -3, 0]),
                    end=np.array([x, 3, 0]),
                    color=GREY_B,
                    thickness=0.008,
                )
            )
        for y in np.linspace(-3, 3, 7):
            grid_lines.add(
                Line3D(
                    start=np.array([-4, y, 0]),
                    end=np.array([4, y, 0]),
                    color=GREY_B,
                    thickness=0.008,
                )
            )
        plane_group = VGroup(plane, grid_lines)
        
        # W 레이블 (평면 오른쪽 위에, 카메라를 향하게)
        w_label = Tex(r"$W$", font_size=48, color=WHITE)
        w_label.move_to([3, 2, 0])
        
        # 1단계: W 평면 디졸브로 나타내기
        self.play(FadeIn(plane_group), run_time=2)
        self.add_fixed_orientation_mobjects(w_label)
        self.play(Write(w_label), run_time=1)
        self.wait(1)
        
        # 2단계: y 벡터 (시작점에서 y로)
        y_point = np.array([1.5, 2, 2.5])
        y_dot = Dot3D(point=y_point, color=YELLOW, radius=0.08)
        # 라벨을 카메라를 향하게 고정
        y_label = Tex(r"$\mathbf{y}$", font_size=36, color=YELLOW)
        y_label.move_to(y_point + np.array([0.3, 0.3, 0.3]))
        self.add_fixed_orientation_mobjects(y_label)
        
        animate_arrow(
            start=start_point,
            end=y_point,
            color=YELLOW,
            extra_anims=[FadeIn(y_dot), Write(y_label)],
        )
        self.wait(1)
        
        # 3단계: 수선의 발 먼저 표시
        ax0_point = np.array([1.5, 2, 0])
        
        # 수선 (y에서 평면으로) - 빨간 점선 화살표
        perp_vector = ax0_point - y_point
        num_perp_segments = 20
        perp_segments = VGroup()
        for i in range(num_perp_segments):
            t_start = i / num_perp_segments
            t_end = (i + 0.5) / num_perp_segments
            if i % 2 == 0:
                segment = Line3D(
                    start=y_point + t_start * perp_vector,
                    end=y_point + t_end * perp_vector,
                    color=RED,
                    thickness=0.02
                )
                perp_segments.add(segment)
        cone_direction = perp_vector / np.linalg.norm(perp_vector)
        perp_arrow_tip = Cone(
            base_radius=0.08,
            height=0.15,
            direction=cone_direction,
            resolution=(8, 8),
            fill_color=RED,
            stroke_color=RED
        )
        perp_arrow_tip.move_to(ax0_point - 0.075 * cone_direction)

        perp_v1 = y_point - ax0_point
        perp_v2_dir = np.array([1, 0, 0])
        perp_v1_norm = perp_v1 / np.linalg.norm(perp_v1)
        perp_size = 0.25
        perp_corner1 = ax0_point + perp_size * perp_v1_norm
        perp_corner2 = ax0_point + perp_size * (perp_v1_norm + perp_v2_dir)
        perp_corner3 = ax0_point + perp_size * perp_v2_dir

        perpendicular_marks = VGroup(
            Line3D(perp_corner1, perp_corner2, color=RED, thickness=0.02),
            Line3D(perp_corner2, perp_corner3, color=RED, thickness=0.02)
        )
        
        self.play(
            *[Create(seg) for seg in perp_segments],
            FadeIn(perp_arrow_tip),
            Create(perpendicular_marks),
            run_time=1.5,
            rate_func=linear
        )
        self.wait(1)
        
        # 4단계: Ax_0 벡터 (시작점에서 평면 위의 점까지) - 파란색
        # 라벨을 카메라를 향하게 고정
        ax0_label = Tex(r"$A\mathbf{x}_0$", font_size=36, color=BLUE)
        ax0_label.move_to(ax0_point + np.array([0, -0.75, 0.05]))
        self.add_fixed_orientation_mobjects(ax0_label)
        
        animate_arrow(
            start=start_point,
            end=ax0_point,
            color=BLUE,
            extra_anims=[Write(ax0_label)],
        )
        self.wait(1)

        # 잔차 벡터 레이블을 빨간 점선 옆에 표시
        residual_label = Tex(r"$\mathbf{r}_0 = \mathbf{y} - A\mathbf{x}_0$", font_size=32, color=RED)
        residual_mid = 0.5 * (y_point + ax0_point)
        residual_label.move_to(residual_mid + np.array([1.3, 0.2, 0.15]))
        self.add_fixed_orientation_mobjects(residual_label)
        self.play(Write(residual_label), run_time=1)
        
        self.wait(2)
