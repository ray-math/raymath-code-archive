from bokeh.plotting import figure, show, output_notebook
from bokeh.models import LinearColorMapper, ColorBar
from bokeh.layouts import column
import numpy as np

# 파라미터 설정
num_iterations = 100  # 총 시뮬레이션 반복 횟수
tape_length = 50  # 테이프 길이
states = ['A', 'B', 'C', 'D', 'E']  # 상태 집합
current_state = 'A'

# 상태별 색상 설정
state_colors = {
    'A': 1,  # 예: A 상태는 1에 해당
    'B': 2,  # B 상태는 2에 해당
    'C': 3,  # C 상태는 3에 해당
    'D': 4,  # D 상태는 4에 해당
    'E': 5   # E 상태는 5에 해당
}
colors = ['#FFFFFF', '#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']  # 흰색 + 상태 색상

# Turing Machine의 규칙 설정
rules = {
    ('A', 0): (1, 'B', 1),
    ('A', 1): (1, 'C', -1),
    ('B', 0): (1, 'C', 1),
    ('B', 1): (1, 'B', -1),
    ('C', 0): (1, 'D', 1),
    ('C', 1): (0, 'E', -1),
    ('D', 0): (1, 'A', -1),
    ('D', 1): (1, 'D', -1),
    ('E', 1): (0, 'A', -1),
}

# 시뮬레이션 데이터를 위한 배열 생성
data = np.zeros((num_iterations, tape_length), dtype=int)
tape = np.zeros(tape_length, dtype=int)  # 테이프 초기 상태
head_position = tape_length // 2  # 초기 헤드 위치

# Turing Machine 시뮬레이션 루프
for i in range(num_iterations):
    # 현재 테이프 상태를 데이터 배열에 저장
    for j in range(tape_length):
        if j == head_position:
            data[i, j] = state_colors[current_state]  # 상태 색상 배정
        else:
            data[i, j] = 0 if tape[j] == 0 else 1  # 0은 검정, 1은 흰색으로 표시
    
    # 규칙에 따라 Turing Machine 동작
    cell_value = tape[head_position]
    if (current_state, cell_value) in rules:
        new_value, new_state, move = rules[(current_state, cell_value)]
        tape[head_position] = new_value
        current_state = new_state
        head_position += move
        head_position = max(0, min(head_position, tape_length - 1))
    else:
        break  # 종료 상태 도달 시 중단

# Bokeh 출력 설정
output_notebook()

# 컬러맵 설정
color_mapper = LinearColorMapper(palette=colors, low=0, high=len(colors) - 1)
color_bar = ColorBar(color_mapper=color_mapper, location=(0, 0), title="States")

# Bokeh figure 생성
p = figure(
    x_range=(0, tape_length),
    y_range=(0, num_iterations),
    title="Turing Machine Space-Time Diagram",
    tools="pan,wheel_zoom,reset",
    match_aspect=True,
    background_fill_color="white"
)

# 데이터 시각화 - 각 셀을 개별적으로 그리며 회색 테두리 추가
for i in range(num_iterations):
    for j in range(tape_length):
        color = colors[data[i, j]]
        p.rect(
            x=j + 0.5, y=num_iterations - i - 0.5, width=1, height=1,
            fill_color=color, line_color="gray", line_width=0.5
        )

# 특정 범위 내에서만 확대/축소
p.x_range.bounds = (0, tape_length)  # x 축 범위 제한
p.y_range.bounds = (0, num_iterations)  # y 축 범위 제한

# 색상 막대 추가
p.add_layout(color_bar, 'right')

# 플롯 출력
show(column(p))