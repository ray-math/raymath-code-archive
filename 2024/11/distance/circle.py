from manim import *


class Draw(Scene):
    def construct(self):
        self.camera.background_color = "#00FF00"

        # 원점 생성 및 "O" LaTeX로 표시
        origin_point = Dot(ORIGIN, color="#004D81")
        origin_label = MathTex("O", font_size=24, color="#004D81").next_to(
            origin_point, DOWN
        )

        # 크기가 2배인 단위원 생성
        circle = Circle(radius=2, color="#004D81")  # 반지름을 2로 설정

        # 반지름을 표시하는 점선 생성
        radius_dashed_line = DashedLine(ORIGIN, RIGHT * 2, color="#004D81")  # 길이를 2로 설정

        # 반지름 길이 "1" LaTeX로 표시
        radius_label = MathTex("1", font_size=24, color="#004D81").next_to(
            radius_dashed_line, DOWN, buff=0.1
        )

        # 원점에서 시작하는 점 (2,0) 생성
        moving_dot = Dot(radius=0.04, color="#004D81").move_to(circle.get_start())

        # 원을 그리는 애니메이션 생성
        circle_animation = Create(circle, run_time=2, rate_func=linear)

        # 수식 텍스트 생성 및 위치 조정
        equation_text = MathTex(
            r"\sqrt{(x-0)^2 + (y-0)^2} = 1",
            r"\quad \Rightarrow \quad",
            r"x^2 + y^2 = 1",
            font_size=24,
            color="#004D81",
        ).next_to(circle, DOWN, buff=1)

        # 모든 요소 추가 및 애니메이션 실행
        self.add(origin_point)
        self.wait(1)
        self.play(Create(origin_label))
        self.play(Create(radius_dashed_line))
        self.play(Create(radius_label))
        self.wait(1)
        self.play(Create(circle))
        self.wait(1)
        self.play(Write(equation_text))
        self.wait(1)
