from manim import *

# 전이 함수 정의 (A에서 A로 계속 전이)
def transition(state, symbol):
    # 상태 A에서 0을 만나면 1을 쓰고 오른쪽으로 이동하며 상태 A 유지
    if state == 'A' and symbol == '0':
        return ('1', 'R', 'A')
    return (symbol, 'S', 'H')  # 기본: 종료 상태로 이동

# 전이 함수를 통해 테이프 동작 계산 (8번 전이 후 종료)
def compute_tape(steps=20, max_moves=8):
    tape = ['0'] * steps  # 초기 테이프 설정 (모두 '0'으로 시작)
    state = 'A'
    head_position = steps // 2  # 초기 헤드 위치는 중간
    actions = []  # 각 스텝의 상태, 테이프 내용, 헤드 위치 기록
    move_count = 0  # 최대 이동 횟수 카운터

    # 튜링 머신 시뮬레이션
    while state != 'H' and move_count < max_moves and 0 <= head_position < len(tape):
        current_symbol = tape[head_position]
        symbol, direction, new_state = transition(state, current_symbol)
        
        # 테이프 업데이트 및 기록 저장
        tape[head_position] = symbol
        actions.append((list(tape), head_position, state, direction, new_state))

        # 헤드 위치 업데이트
        if direction == 'R':
            head_position += 1
        elif direction == 'L':
            head_position -= 1
        
        # 상태 업데이트 및 이동 횟수 증가
        state = new_state
        move_count += 1

    return actions

class A0to1RA(Scene):
    def construct(self):
        move_count = 0

        # 튜링 머신 시뮬레이션 결과 계산 (최대 8번 이동)
        actions = compute_tape(steps=20, max_moves=8)

        # 타이틀 및 전이 함수 텍스트
        title = Tex(r"$\delta(A, 0) \rightarrow (1, R, A)$", font_size=42)
        title.to_edge(UP, buff=0.5)

        # 테이프 셀 초기화 및 초기 설정 유지
        tape_cells = VGroup(*[Square().scale(0.6) for _ in range(20)])
        tape_cells.arrange(RIGHT, buff=0.05)
        tape_cells.shift(DOWN * 1.5)

        # 초기 테이프 값 표시
        tape_labels = VGroup(*[Text("0", font_size=32) for _ in range(20)])
        for cell, label in zip(tape_cells, tape_labels):
            label.move_to(cell)

        # 헤드 초기 설정
        head = Triangle().scale(0.3).set_fill(RED, opacity=0).set_stroke(RED, width=3)
        head.next_to(tape_cells[10], UP, buff=0.1)

        # 상태 및 기타 텍스트 초기 설정
        state_text = Text("State: A", font_size=28, color=WHITE)
        read_text = Text("Read: 0", font_size=28, color=WHITE)
        state_text.next_to(title, DR, buff=1)
        read_text.next_to(state_text, DOWN)
        ones_text = Text("Number of ones: 0", font_size=28, color=WHITE)
        moves_text = Text("Move: 0", font_size=28, color=WHITE)
        ones_text.next_to(title, DL, buff=1)
        moves_text.next_to(ones_text, DOWN)

        # 초기 요소 애니메이션
        self.play(Write(title))
        self.play(Write(state_text), Write(read_text), Write(ones_text), Write(moves_text), Create(tape_cells), Write(tape_labels))
        self.play(FadeIn(head))

        # 나머지 계산된 결과에 따라 애니메이션 적용
        for tape, pos, state, direction, new_state in actions:
            # 테이프 업데이트와 1의 개수 카운트를 동시에 실행
            new_tape_labels = VGroup()
            for i, symbol in enumerate(tape):
                new_label = Text(symbol, font_size=32).move_to(tape_cells[i])
                new_tape_labels.add(new_label)
            ones_count = tape.count('1')
            new_ones_text = Text(f"Number of ones: {ones_count}", font_size=28, color=WHITE).next_to(title, DL, buff=1)
            self.play(ReplacementTransform(tape_labels, new_tape_labels), ReplacementTransform(ones_text, new_ones_text))
            tape_labels, ones_text = new_tape_labels, new_ones_text

            # 헤드 이동 및 이동 횟수 텍스트 업데이트를 동시에 실행
            move_count += 1
            new_moves_text = Text(f"Move: {move_count}", font_size=28, color=WHITE).next_to(ones_text, DOWN)
            next_pos = pos + 1 if direction == 'R' else pos - 1
            head_move_animation = head.animate.next_to(tape_cells[next_pos], UP, buff=0.1) if 0 <= next_pos < len(tape_cells) else FadeOut(head)
            self.play(head_move_animation, ReplacementTransform(moves_text, new_moves_text))
            moves_text = new_moves_text

            # 상태 및 읽은 기호 텍스트 업데이트
            new_state_text = Text(f"State: {new_state}", font_size=28, color=WHITE).next_to(title, DR, buff=1)
            self.play(ReplacementTransform(state_text, new_state_text))
            state_text = new_state_text

            current_symbol = tape[next_pos] if 0 <= next_pos < len(tape) else '0'
            new_read_text = Text(f"Read: {current_symbol}", font_size=28, color=WHITE).next_to(state_text, DOWN)
            self.play(ReplacementTransform(read_text, new_read_text))
            read_text = new_read_text

        # 종료 시 애니메이션
        self.play(head.animate.set_fill(RED, opacity=1))
        self.wait(2)
