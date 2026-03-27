from manim import *
import sympy as sp
import matplotlib.cm as cm  # Import colormap
from matplotlib.colors import to_hex  # For converting colormap output to hex

class BernoulliPolynomials(Scene):
    def construct(self):
        # Sympy에서 x와 n을 정의합니다.
        x = sp.symbols("x")

        # Title 설정 (맨 위에 위치)
        title = Text("Bernoulli Polynomials", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # 축 설정 (회색으로 설정, 위치를 위로 이동, 화살표 제거)
        axes = Axes(
            x_range=[-0.5, 1.5, 0.25],
            y_range=[-3, 3, 1],
            axis_config={"color": GREY},
            tips=False,  # 화살표 제거
        )
        axes.scale(0.9)

        # 축을 화면에 추가하고, 그리기 애니메이션 적용
        self.play(Create(axes))
        self.wait(0.5)  # 축이 그려진 후 잠깐 대기

        # 초기 그래프 및 라벨 설정
        graph = axes.plot(lambda x: float(sp.bernoulli(1, x)), color=BLUE)
        graph_label = axes.get_graph_label(graph, label="B_{1}(x)").scale(0.7)

        # 그래프 그리기 애니메이션
        self.play(Create(graph), Write(graph_label))
        self.wait(0.5)

        # 함수식 라벨 추가 (크기 조정 및 위치 조정)
        function_label = MathTex(r"B_{1}(x) = " + sp.latex(sp.bernoulli(1, x)))
        function_label.scale(0.5)  # 크기를 더 줄임
        function_label.next_to(axes, DOWN)  # 위치를 좀 더 위로 조정

        # 함수식 라벨 그리기
        self.play(Write(function_label))
        self.wait(0.5)

        # n이 1에서 15까지 변하는 베르누이 다항식 생성
        for n in range(2, 16):
            # Determine the color based on whether n is even or odd
            if n % 2 == 0:
                colormap = cm.get_cmap("Reds")  # Red color map for even n
            else:
                colormap = cm.get_cmap("Blues")  # Blue color map for odd n

            color_intensity = 0.3 + 0.4 * (n / 15)  # This maps n from 0.3 to 0.7
            color = to_hex(colormap(color_intensity))  # Convert to hex color

            new_graph = axes.plot(lambda x, n=n: float(sp.bernoulli(n, x)), color=color)
            new_label = axes.get_graph_label(new_graph, label=f"B_{{{n}}}(x)").scale(
                0.7
            )

            # 새로운 함수식 라벨
            new_function_label = MathTex(
                rf"B_{{{n}}}(x) = " + sp.latex(sp.bernoulli(n, x))
            )
            new_function_label.scale(0.5)
            new_function_label.next_to(axes, DOWN)

            # Transition speed 설정 (B10까지는 빠르게, B11부터는 느리게)
            run_time = 0.6 if n <= 10 else 1.5

            # 그래프와 라벨을 새로운 다항식으로 변환
            self.play(
                Transform(graph, new_graph),
                Transform(graph_label, new_label),
                Transform(function_label, new_function_label),
                run_time=run_time,
            )
            self.wait(0.5)

        # 마지막에 그래프가 좀 더 길게 멈추게 하기
        self.wait(2)
