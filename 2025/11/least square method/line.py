from manim import *

class RegressionError(Scene):
    def construct(self):
        # 좌표축
        axes = Axes(
            x_range=[-1, 8, 1],
            y_range=[-1, 5, 1],
            x_length=10,
            y_length=5,
            tips=True,
        )
        axes.to_edge(DOWN, buff=1).shift(LEFT * 0.75)

        x_label = MathTex("t").next_to(axes.x_axis.get_end(), RIGHT, buff=0.3)
        y_label = MathTex("y").next_to(axes.y_axis.get_end(), UP, buff=0.3)

        # 1. 축 그리기
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)

        # 직선 y = c t + d
        c = 0.4
        d = 0.8

        def line_func(t):
            return c * t + d

        # 추세선을 점선으로
        line = DashedLine(
            axes.c2p(-0.7, line_func(-0.7)),
            axes.c2p(7.5, line_func(7.5)),
            dash_length=0.15,
            dashed_ratio=0.6,
            stroke_width=4,
            color=BLUE
        )
        line_label = MathTex("y = ct + d").next_to(
            line.get_end(), UP + RIGHT, buff=0.3
        )

        # 샘플 t 값들 (더 넓게 분포)
        ts = [0.5, 1.5, 3.0, 4.5, 5.5, 7.0]
        # 관측값 y_i : 직선에서 조금 위/아래로 벗어나게
        ys = [
            line_func(ts[0]) + 1,
            line_func(ts[1]) - 1,
            line_func(ts[2]) + 2,
            line_func(ts[3]) - 1.4,
            line_func(ts[4]) + 1,
            line_func(ts[5]) - 1.8,
        ]

        dots = VGroup()
        dot_labels = VGroup()
        dashed_lines = VGroup()
        residual_segments = VGroup()

        # 첫 번째 점 라벨
        label_t1 = MathTex("(t_1,\, y_1)").scale(0.7)
        
        # 대표 점 (i) 인덱스
        i_index = 2  # 세 번째 점을 i로 사용

        for idx, (t_val, y_obs) in enumerate(zip(ts, ys)):
            # 관측점 (크기 증가)
            p_obs = axes.c2p(t_val, y_obs)
            dot = Dot(p_obs, radius=0.09, color=YELLOW)
            dots.add(dot)

            # 직선 위의 예측점
            y_pred = line_func(t_val)
            p_pred = axes.c2p(t_val, y_pred)

            # 추세선과 점 사이 점선 (빨간색, 더 두껍게)
            dashed = DashedLine(p_pred, p_obs, dash_length=0.08, dashed_ratio=0.5, 
                               stroke_width=3, color=RED)
            dashed_lines.add(dashed)

            # 세로 오차선
            seg = Line(p_pred, p_obs, stroke_width=2, color=RED)
            residual_segments.add(seg)

            # 라벨 추가
            if idx == 0:  # 첫 번째 점
                label_t1.next_to(p_obs, UP + RIGHT, buff=0.25)
                dot_labels.add(label_t1)
            elif idx == i_index:  # 대표 점 i
                label_ti_yi = MathTex("(t_i,\, y_i)").scale(0.7)
                label_ti_yi.next_to(p_obs, UP + RIGHT, buff=0.25)
                dot_labels.add(label_ti_yi)

        # 2. 데이터 점들과 라벨을 함께 그리기
        for idx in range(len(dots)):
            anims = [GrowFromCenter(dots[idx])]
            if idx < len(dot_labels):
                anims.append(Write(dot_labels[idx]))
            self.play(*anims, run_time=0.4)
        self.wait(0.5)

        # 3. 추세선 그리기
        self.play(Create(line), Write(line_label), run_time=2)
        self.wait(0.5)
        
        # 추세선을 화면에 유지
        self.add(line, line_label)

        # 4. 점선 그리기
        self.play(LaggedStart(*[Create(dashed) for dashed in dashed_lines], lag_ratio=0.15))
        self.wait(0.5)

        # 5. 특정 점의 오차 설명
        ti, yi = ts[i_index], ys[i_index]
        y_pred_i = line_func(ti)
        p_obs_i = axes.c2p(ti, yi)
        p_pred_i = axes.c2p(ti, y_pred_i)

        # 오차선의 중간 지점 (화살표가 가리킬 위치)
        error_mid_point = (p_obs_i + p_pred_i) / 2
        
        # 오차 설명 텍스트 (왼쪽 상단에 배치)
        error_text = MathTex(
            r"\text{error}_i = y_i - (ct_i + d)"
        ).scale(0.8)
        error_text.next_to(axes, UP, buff=0.3).shift(LEFT * 1)
        
        # 텍스트에서 오차선 중간으로 짧은 곡선 화살표
        arrow = CurvedArrow(
            error_text.get_left() + RIGHT * 1.5 + DOWN * 0.3, 
            error_mid_point + LEFT * 0.03,
            color=RED, 
            stroke_width=3,
            angle=TAU/9
        )

        self.play(Create(arrow))
        self.wait(0.2)
        self.play(Write(error_text))
        self.wait(2)
