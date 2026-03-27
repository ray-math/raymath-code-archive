from manim import *


class DrawMaxGraph(Scene):
    def construct(self):
        self.camera.background_color = "#00FF00"

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

        # \max(|x|, |y|) = 1 그래프 생성
        max_value_graph = ImplicitFunction(
            lambda x, y: max(abs(x), abs(y)) - 2,
            color="#004D81",
            x_range=[-3, 3],
            y_range=[-3, 3],
        )

        # 수식 텍스트 생성 및 위치 조정
        equation_text = MathTex(
            r"\max(\vert x \vert, \vert y \vert) = 1",
            font_size=24,
            color="#004D81",
        ).next_to(max_value_graph, DOWN, buff=1)

        # 모든 요소 추가 및 애니메이션 실행
        self.wait(1)
        self.play(Write(equation_text))
        self.wait(2)
        self.add(origin_point)
        self.add(origin_label)
        self.play(Create(radius_dashed_line))
        self.add(radius_label)
        self.play(Create(max_value_graph))
        self.wait(10)


# 이 코드
