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

    # Initialize a set to store all sequences
    all_sequences = set()

    def backtrack(node, path):
        if len(path) == n and path[0] in square_pairs[path[-1]]:
            # Process the sequence before adding it to the set
            index_1 = path.index(1)
            if path[(index_1-1)%n] > path[(index_1+1)%n]:
                path = path[index_1:] + path[:index_1]
            else:
                path = path[index_1::-1] + path[:index_1:-1]
            all_sequences.add(tuple(path))
        elif (node, len(path)) not in memo:
            for next_node in sorted(square_pairs[node], reverse=True):
                if next_node not in path:
                    backtrack(next_node, path + [next_node])
            memo[(node, len(path))] = True

    # Start from the largest number
    for i in range(n, 0, -1):
        backtrack(i, [i])

    return all_sequences

def is_square(n):
    return math.isqrt(n)**2 == n

# Test the function for a range of numbers
for i in range(30, 36):
    sequences = find_all_sequences(i)
    if sequences:
        for sequence in sequences:
            print(f"For {i}, the sequence is {' '.join(map(str, sequence))}.")
    else:
        print(f"No sequence found for {i}.")
