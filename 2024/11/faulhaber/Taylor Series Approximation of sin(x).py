from manim import *
import math

class TaylorSeriesSine(Scene):
    def construct(self):
        # 제목 추가
        title = Text("Taylor Series Approximation of sin(x)", font_size=40)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        # 축 생성 (정의역 확대, 축 레이블 제거)
        axes = Axes(
            x_range=[-3 * PI, 3 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=5,
            tips=False,
        )
        self.play(Create(axes))

        # 테일러 급수 함수 정의
        def taylor_series_sin(x, n):
            """n차 테일러 급수 근사"""
            terms = [((-1)**k * x**(2 * k + 1) / math.factorial(2 * k + 1)) for k in range(n + 1)]
            return sum(terms)

        # 테일러 급수 표현식 생성 함수
        def taylor_series_formula(n):
            """n차 테일러 급수의 수식 표현 생성 (보기 좋은 형태)"""
            terms = [
                f"\\frac{{x^{{{2 * k + 1}}}}}{{{2 * k + 1}!}}" if k % 2 == 0
                else f"- \\frac{{x^{{{2 * k + 1}}}}}{{{2 * k + 1}!}}"
                for k in range(n + 1)
            ]
            return " + ".join(terms).replace("+ -", "- ")  # 양수와 음수 구분

        # 초기 그래프와 텍스트 생성
        taylor_graph = axes.plot(lambda x: taylor_series_sin(x, 0), color=ORANGE, stroke_width=3)
        formula = MathTex(r"\sin(x) \approx", taylor_series_formula(0)).scale(0.6)
        formula.to_edge(DOWN, buff=0.5)

        # 초기 그래프 및 텍스트 애니메이션
        self.play(Create(taylor_graph), Write(formula))
        self.wait(1)

        # 그래프와 수식을 변형하며 12차까지 애니메이션
        colors = [YELLOW, GREEN, BLUE, PURPLE, RED, PINK, TEAL, MAROON]  # 색상 배열
        for n in range(1, 13):
            # 새로운 테일러 그래프와 수식 업데이트 (차수에 따라 색상 변화)
            new_taylor_graph = axes.plot(
                lambda x: taylor_series_sin(x, n),
                color=colors[n % len(colors)],
                stroke_width=4  # 그래프 선 두께 증가
            )
            new_formula = MathTex(r"\sin(x) \approx", taylor_series_formula(n)).scale(0.6)
            new_formula.to_edge(DOWN, buff=0.5)

            # 그래프와 수식 변형
            self.play(
                Transform(taylor_graph, new_taylor_graph),
                Transform(formula, new_formula),
                run_time=2
            )
            self.wait(1)

        # 마지막 그래프와 수식 유지 후 종료
        self.wait(2)
