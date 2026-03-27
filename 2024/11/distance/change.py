from manim import *


class CoverScreenWithColor(Scene):
    def construct(self):
        # 초기 카메라 배경색 설정
        self.camera.background_color = "#AAFFAA"

        # 원점 생성 및 "O" LaTeX로 표시
        origin_point = Dot(ORIGIN, color="#004D81")
        origin_label = MathTex("O", font_size=24, color="#004D81").next_to(
            origin_point, DOWN
        )

        # 원점과 라벨을 장면에 추가
        self.play(
            origin_point.animate,
            origin_label.animate,
        )

        # 1초 대기
        self.wait(1)

        # 화면 전체를 덮는 파란색 사각형 생성
        cover_rect = Rectangle(color="#004D81", fill_opacity=1)
        diagonal_length = config.frame_height**2 + config.frame_width**2
        cover_rect.scale(diagonal_length / cover_rect.height)

        # 사각형을 화면에 표시하는 애니메이션
        self.play(FadeIn(cover_rect), run_time=2)

        # 원점과 라벨을 다시 장면에 추가하여 화면 최상단에 위치시킴
        self.add(origin_point, origin_label)

        # 원점과 라벨 색상 변경 애니메이션
        self.play(
            origin_point.animate.set_color(WHITE),
            origin_label.animate.set_color(WHITE),
            run_time=2,
        )

        self.wait(10)
