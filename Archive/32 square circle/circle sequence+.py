import math
from collections import defaultdict

def find_all_sequences(n):
    # Calculate possible square pairs
    square_pairs = defaultdict(list)
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            if is_square(i + j):
                square_pairs[i].append(j)
                square_pairs[j].append(i)

    # Sort the pairs in descending order
    for pairs in square_pairs.values():
        pairs.sort(reverse=True)

    # Initialize memoization dictionary
    memo = {}

    def backtrack(node, path):
        if len(path) == n and path[0] in square_pairs[path[-1]]:
            return path
        if (node, len(path)) in memo:
            return memo[(node, len(path))]
        for next_node in sorted(square_pairs[node], reverse=True):
            if next_node not in path:
                result = backtrack(next_node, path + [next_node])
                if result:
                    return result
        return None

    all_sequences = set()

    def process_sequence(sequence):
        index_1 = sequence.index(1)
        if sequence[(index_1-1)%n] > sequence[(index_1+1)%n]:
            sequence = sequence[index_1:] + sequence[:index_1]
        else:
            sequence = sequence[index_1::-1] + sequence[:index_1:-1]
        all_sequences.add(tuple(sequence))

    for i in range(n, 0, -1):
        sequence = backtrack(i, [i])
        if sequence:
            process_sequence(sequence)

    return all_sequences

def is_square(n):
    return math.isqrt(n)**2 == n

# Test the function for a range of numbers
for i in range(46, 52):
    sequences = find_all_sequences(i)
    if sequences:
        for sequence in sequences:
            print(f"For {i}, the sequence is {' '.join(map(str, sequence))}.")
    else:
        print(f"No sequence found for {i}.")