from manim import *


class MinkowskiDistance(Scene):
    def construct(self):
        self.camera.background_color = "#AAFFAA"

        # 원점 생성 및 "O" LaTeX로 표시
        origin_point = Dot(ORIGIN, color="#004D81")
        origin_label = MathTex("O", font_size=24, color="#004D81").next_to(
            origin_point, DOWN
        )

        # 반지름을 표시하는 점선 생성
        radius_dashed_line = DashedLine(ORIGIN, RIGHT * 2, color="#004D81")

        # 반지름 길이 "1" LaTeX로 표시
        radius_label = MathTex("1", font_size=24, color="#004D81").next_to(
            radius_dashed_line, DOWN, buff=0.1
        )

        # p 값을 변화시키기 위한 ValueTracker
        p_val = ValueTracker(1)

        # 민코프스키 거리를 나타내는 함수
        def get_minkowski_graph(p):
            if p == 200:
                return Circle(radius=2, color="#004D81")
            return ImplicitFunction(
                lambda x, y: (abs(x) ** p + abs(y) ** p) ** (1 / p) - 2,
                color="#004D81",
                x_range=[-3, 3],
                y_range=[-3, 3],
            )

        # 초기 그래프 (p=1)
        minkowski_graph = always_redraw(lambda: get_minkowski_graph(p_val.get_value()))

        # p 값에 따른 함수 식
        equation_text = always_redraw(
            lambda: MathTex(
                rf"\left( \vert x \vert^{{ {p_val.get_value():.1f} }}"
                rf"+ \vert y \vert^{{ {p_val.get_value():.1f} }}"
                rf"\right)^{{1/{p_val.get_value():.1f}}}"
                r"= 1",
                font_size=24,
                color="#004D81",
            ).next_to(minkowski_graph, DOWN, buff=1)
        )

        # 애니메이션
        self.play(
            AnimationGroup(
                Create(origin_point),
                Create(origin_label),
                Create(radius_dashed_line),
                Create(radius_label),
            )
        )
        self.play(
            AnimationGroup(
                Create(minkowski_graph),
                Write(equation_text),
            )
        )
        self.wait(2)
        self.play(p_val.animate.set_value(2), run_time=2)
        self.wait(2)
        self.play(p_val.animate.set_value(100), run_time=2)
        self.wait(3)
        self.play(p_val.animate.set_value(2), run_time=2)
        self.play(p_val.animate.set_value(0.5), run_time=2)
        self.wait(10)
