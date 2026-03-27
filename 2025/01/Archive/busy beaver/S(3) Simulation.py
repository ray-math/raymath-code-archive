from manim import *

# Updated transition function based on the corrected transition rules
def transition(state, symbol):
    transitions = {
        'A': {'0': ('1', 'R', 'B'), '1': ('1', 'R', 'H')},
        'B': {'0': ('1', 'L', 'B'), '1': ('0', 'R', 'C')},
        'C': {'0': ('1', 'L', 'C'), '1': ('1', 'L', 'A')},
    }
    return transitions.get(state, {}).get(symbol, (symbol, 'S', 'H'))

# Run Turing machine simulation to track tape changes, head position, and states
def compute_tape(steps=20):
    tape = ['0'] * steps  # Initialize tape with '0's
    state = 'A'
    head_position = steps // 2  # Start head at the center of the tape
    actions = []  # Record each step with tape state, head position, and machine state

    while state != 'H' and 0 <= head_position < len(tape):
        current_symbol = tape[head_position]
        symbol, direction, new_state = transition(state, current_symbol)
        
        # Update tape with the new symbol and save the state
        tape[head_position] = symbol
        actions.append((list(tape), head_position, state, direction, new_state))

        # Update head position
        if direction == 'R':
            head_position += 1
        elif direction == 'L':
            head_position -= 1

        # Update state
        state = new_state

    return actions

class S3Simulation(Scene):
    def construct(self):
        move_count = 0

        # Compute Turing machine actions
        actions = compute_tape(steps=20)

        # Title
        title = Text("S(3) Simulation", font_size=42)
        title.to_edge(UP, buff=0.5)

        # Initialize tape cells and labels
        tape_cells = VGroup(*[Square().scale(0.6) for _ in range(20)])
        tape_cells.arrange(RIGHT, buff=0.05)
        tape_cells.shift(DOWN * 1.5)

        tape_labels = VGroup(*[Text("0", font_size=32) for _ in range(20)])
        for cell, label in zip(tape_cells, tape_labels):
            label.move_to(cell)

        # Head indicator
        head = Triangle().scale(0.3).set_fill(RED, opacity=0).set_stroke(RED, width=3)
        head.next_to(tape_cells[10], UP, buff=0.1)

        # State and information text
        state_text = Text("State: A", font_size=28, color=WHITE)
        read_text = Text("Read: 0", font_size=28, color=WHITE)
        state_text.next_to(title, DOWN, buff=1.5)
        read_text.next_to(state_text, DOWN)
        ones_text = Text("Number of ones: 0", font_size=28, color=WHITE)
        moves_text = Text("Move: 0", font_size=28, color=WHITE)
        ones_text.next_to(state_text, LEFT, buff=2)
        moves_text.next_to(ones_text, DOWN)

        # Transition table display
        table_data = [["0", "1RB", "1LB", "1LC"], ["1", "1RH", "0RC", "1LA"]]
        table = Table(table_data, col_labels=[Tex(r"$\delta$"), Text("A"), Text("B"), Text("C")], include_outer_lines=True)
        table.scale(0.5)
        table.next_to(state_text, RIGHT, buff=1)

        # Initial animations
        self.play(Write(title))
        self.play(Write(state_text), Write(read_text), Write(ones_text), Write(moves_text), Create(tape_cells), Write(tape_labels), Create(table))
        self.play(FadeIn(head))

        highlight_box = SurroundingRectangle(table.get_cell((2, 2)), color=RED)
        self.play(FadeIn(highlight_box))

        # Execute actions based on simulation results
        for tape, pos, state, direction, new_state in actions:
            # Update tape display
            new_tape_labels = VGroup()
            for i, symbol in enumerate(tape):
                new_label = Text(symbol, font_size=32).move_to(tape_cells[i])
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

            # Highlight the transition in the table based on state and symbol
            row = 2 if current_symbol == '0' else 3
            col = 2 if new_state == 'A' else (3 if new_state == 'B' else (4 if new_state == 'C' else None))

            # If halt state, fade out highlight box
            if new_state == 'H':
                self.play(FadeOut(highlight_box))
                break
            elif col is not None:
                new_highlight_box = SurroundingRectangle(table.get_cell((row, col)), color=RED)
                self.play(ReplacementTransform(highlight_box, new_highlight_box))
                highlight_box = new_highlight_box

        # Finalize head and update to halt state
        self.play(head.animate.set_fill(RED, opacity=1))
        final_state_text = Text("State: H", font_size=28, color=WHITE).next_to(title, DOWN, buff=1.5)
        self.play(ReplacementTransform(state_text, final_state_text))
        self.wait(3)
