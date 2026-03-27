from manim import *
import cmath
import numpy as np

class ZetaPolarVisualization(Scene):
    def construct(self):
        # 제목
        title = Text("Riemann Zeta Function in Polar Coordinates", font_size=36, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        
        # 복소 평면 설정
        complex_plane = ComplexPlane(
            x_range=[-10, 10],
            y_range=[-10, 10],
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1}
        ).add_coordinates()
        self.play(Create(complex_plane))

        # 리만 제타 함수 정의
        def zeta(s, terms=100):
            result = 0
            for n in range(1, terms):
                result += 1 / (n ** s)
            return result
        
        # 극좌표 형태의 격자 그리기
        radial_lines = VGroup()
        for angle in np.linspace(0, TAU, 16):
            radial_line = Line(start=complex_plane.c2p(0, 0), end=complex_plane.c2p(6 * np.cos(angle), 6 * np.sin(angle)), color=YELLOW, stroke_width=1)
            radial_lines.add(radial_line)
        
        circles = VGroup()
        for radius in np.linspace(0.5, 6, 12):
            circle = Circle(radius=radius).set_color(YELLOW).move_to(complex_plane.c2p(0, 0))
            circles.add(circle)

        self.play(Create(radial_lines), Create(circles))

        # 리만 제타 함수의 값을 따라가는 점 추가
        zeta_points = VGroup()
        resolution = 100
        for r in np.linspace(0.1, 6, resolution):
            for theta in np.linspace(0, TAU, resolution):
                s = r * cmath.exp(1j * theta)
                zeta_value = zeta(s)
                
                # 절대값에 따른 색상 설정
                color = interpolate_color(PINK, RED, abs(zeta_value) % 1)
                
                # 점 추가
                point = Dot(point=complex_plane.c2p(r * np.cos(theta), r * np.sin(theta)), color=color, radius=0.03)
                zeta_points.add(point)
        
        # 모든 점을 동시에 나타내기
        self.play(FadeIn(zeta_points), run_time=5)
        self.wait(3)