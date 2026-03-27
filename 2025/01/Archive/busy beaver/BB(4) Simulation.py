from manim import *

# 상태 전환 함수
def transition(state, symbol):
    transitions = {
        'A': {'0': ('1', 'R', 'B'), '1': ('1', 'L', 'B')},
        'B': {'0': ('1', 'L', 'A'), '1': ('0', 'L', 'C')},
        'C': {'0': ('1', 'R', 'H'), '1': ('1', 'L', 'D')},
        'D': {'0': ('1', 'R', 'D'), '1': ('0', 'R', 'A')},
    }
    return transitions.get(state, {}).get(symbol, (symbol, 'S', 'H'))

# 튜링 머신 시뮬레이션
def compute_tape(steps=40):
    tape = ['0'] * steps
    state = 'A'
    head_position = steps // 2
    actions = []

    while state != 'H' and 0 <= head_position < len(tape):
        current_symbol = tape[head_position]
        symbol, direction, new_state = transition(state, current_symbol)
        
        tape[head_position] = symbol
        actions.append((list(tape), head_position, state, direction, new_state))

        if direction == 'R':
            head_position += 1
        elif direction == 'L':
            head_position -= 1

        # Update state
        state = new_state

    return actions


class BB4Simulation(Scene):
    def construct(self):
        move_count = 0
        actions = compute_tape(steps=40)

        # Title
        title = Text("BB(4) Simulation", font_size=42)
        title.to_edge(UP, buff=0.5)

        # 테이프 셀 생성 (40개)
        tape_cells = VGroup(*[Square().scale(0.3) for _ in range(40)])
        tape_cells.arrange(RIGHT, buff=0.05)
        tape_cells.shift(DOWN * 2.5)

        # 테이프 값 초기화
        tape_labels = VGroup(*[Text("0", font_size=24) for _ in range(40)])
        for cell, label in zip(tape_cells, tape_labels):
            label.move_to(cell)

        # Head indicator
        head = Triangle().scale(0.3).set_fill(RED, opacity=0).set_stroke(RED, width=3)
        head.next_to(tape_cells[20], UP, buff=0.1)

        # State and information text
        state_text = Text("State: A", font_size=28, color=WHITE)
        read_text = Text("Read: 0", font_size=28, color=WHITE)
        state_text.next_to(title, DOWN, buff=1.5)
        read_text.next_to(state_text, DOWN)
        ones_text = Text("Number of ones: 0", font_size=28, color=WHITE)
        moves_text = Text("Move: 0", font_size=28, color=WHITE)
        ones_text.next_to(state_text, LEFT, buff=2)
        moves_text.next_to(ones_text, DOWN)

        table_latex = MathTex(
            r"""
            \begin{array}{c|c|c}
            \delta & 0 & 1 \\ \hline
            A & 1RB & 1LB \\ \hline
            B & 1LA & 0LC \\ \hline
            C & 1R\textbf{H} & 1LD \\ \hline
            D & 1RD & 0RA
            \end{array}
            """,
            font_size=36,
        )
        table_latex.next_to(state_text, RIGHT, buff=0)
        table_latex.shift(RIGHT * 2 + DOWN * 1)     

        # Initial animations
        self.play(Write(title))
        self.play(Write(state_text), Write(read_text), Write(ones_text), Write(moves_text), Create(tape_cells), Write(tape_labels), Write(table_latex))
        self.play(FadeIn(head))

        # Execute actions based on simulation results
        for tape, pos, state, direction, new_state in actions:
            # Update tape display
            new_tape_labels = VGroup()
            for i, symbol in enumerate(tape):
                new_label = Text(symbol, font_size=24).move_to(tape_cells[i])
                new_tape_labels.add(new_label)

            # Update number of ones with tape display
            ones_count = tape.count('1')
            new_ones_text = Text(f"Number of ones: {ones_count}", font_size=28, color=WHITE).next_to(state_text, LEFT, buff=2)
            
            # Create animation for writing on the tape
            self.play(
                ReplacementTransform(tape_labels, new_tape_labels),
                ReplacementTransform(ones_text, new_ones_text)
            )
            tape_labels, ones_text = new_tape_labels, new_ones_text

            # Update head position animation and move count simultaneously
            move_count += 1
            next_pos = pos + 1 if direction == 'R' else pos - 1
            new_moves_text = Text(f"Move: {move_count}", font_size=28, color=WHITE).next_to(ones_text, DOWN)
            head_move_animation = head.animate.next_to(tape_cells[next_pos], UP, buff=0.1) if 0 <= next_pos < len(tape_cells) else FadeOut(head)
            self.play(head_move_animation, ReplacementTransform(moves_text, new_moves_text))
            moves_text = new_moves_text

            # Update state display
            new_state_text = Text(f"State: {new_state}", font_size=28, color=WHITE).next_to(title, DOWN, buff=1.5)
            self.play(ReplacementTransform(state_text, new_state_text))
            state_text = new_state_text

            # Update read symbol display
            current_symbol = tape[next_pos] if 0 <= next_pos < len(tape) else '0'
            new_read_text = Text(f"Read: {current_symbol}", font_size=28, color=WHITE).next_to(state_text, DOWN)
            self.play(ReplacementTransform(read_text, new_read_text))
            read_text = new_read_text

        # Finalize head and update to halt state
        self.play(head.animate.set_fill(RED, opacity=1))
        final_state_text = Text("State: H", font_size=28, color=WHITE).next_to(title, DOWN, buff=1.5)
        self.play(ReplacementTransform(state_text, final_state_text))
        self.wait(3)
