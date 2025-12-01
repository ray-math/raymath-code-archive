import math
import os
import concurrent.futures

# Check if a number is a perfect square
def is_perfect_square(n):
    return math.isqrt(n) ** 2 == n

def is_equal_cycle(cycle1, cycle2):
    return cycle1[1:] == cycle2[:0:-1]

# Find all Hamiltonian cycles in a graph
def hamiltonian_path_all(graph, vertex, path, result):
    path.append(vertex)

    if len(path) < len(graph):
        neighbors = sorted(graph[vertex], key=lambda v: len(graph[v]))
        for neighbor in neighbors:
            if neighbor not in path:
                hamiltonian_path_all(graph, neighbor, path, result)
    elif path[0] in graph[path[-1]]:
        result.append(list(path))

    path.pop()

# Find a Hamiltonian cycle in a graph
def hamiltonian_path_one(graph, vertex, path):
    path.append(vertex)

    if len(path) == len(graph):
        if path[0] in graph[path[-1]]:
            return True

    neighbors = sorted(graph[vertex], key=lambda v: len(graph[v]))
    for neighbor in neighbors:
        if neighbor not in path and hamiltonian_path_one(graph, neighbor, path):
            return True

    path.pop()
    return False

# Build a graph for a given number
def build_graph(n):
    graph = {i: set() for i in range(1, n+1)}
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            if is_perfect_square(i + j):
                graph[i].add(j)
                graph[j].add(i)
    return graph

# Find all Hamiltonian cycles for a given number
def find_all_hamiltonian_cycles(n):
    graph = build_graph(n)
    result = []
    hamiltonian_path_all(graph, n, [], result)

    unique_cycles = []
    for cycle in result:
        if not any(is_equal_cycle(cycle, unique_cycle) for unique_cycle in unique_cycles):
            unique_cycles.append(cycle)

    return n, unique_cycles

# Find one Hamiltonian cycle for a given number
def find_one_hamiltonian_cycle(n):
    graph = build_graph(n)
    for start in range(1, n+1):
        path = []
        if hamiltonian_path_one(graph, start, path):
            max_index = path.index(max(path))
            path = path[max_index:] + path[:max_index]
            return n, path
    return n, None

# List of numbers for which we need to find all Hamiltonian cycles
numbers_to_find_all = [32, 45, 46 ,47, 48, 49, 50]

# List of numbers for which we need to find one Hamiltonian cycle
numbers_to_find_one = [32, 67, 68, 69, 70,  73, 74, 81, 89, 90, 96, 97, 98, 99, 101, 104, 105, 106, 107, 108, 109, 110]

# Use maximum available CPU cores
worker_threads = os.cpu_count()
print(f"Using {worker_threads} threads.")

# Use ThreadPoolExecutor to run tasks concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=worker_threads) as executor:
    # Finding all Hamiltonian cycles
    futures_all = {executor.submit(find_all_hamiltonian_cycles, n): n for n in numbers_to_find_all}
    # Finding one Hamiltonian cycle
    futures_one = {executor.submit(find_one_hamiltonian_cycle, n): n for n in numbers_to_find_one}
    
    # Consolidating all futures
    all_futures = {**futures_all, **futures_one}

    # Determine the directory of the python script file
    script_dir = os.path.dirname(os.path.realpath(__file__))

    for future in concurrent.futures.as_completed(all_futures):
        n, cycles = future.result()

        # File path for saving the results
        output_file_path = os.path.join(script_dir, f"hamiltonian_cycles_{n}.md") if n in numbers_to_find_all else os.path.join(script_dir, f"one_cycle_{n}.md")

        # Open the output file
        with open(output_file_path, "w") as f:
            if cycles:
                if n in numbers_to_find_all:
                    f.write(f"\nHamiltonian cycles for n={n} found: {len(cycles)}\n")
                    for i, cycle in enumerate(cycles, start=1):
                        f.write(f"Cycle {i}: {cycle}\n")
                else:
                    f.write(f"\nHamiltonian cycle for n={n}\n")
                    f.write(f"{cycles}\n")
            else:
                f.write(f"\nNo Hamiltonian cycles found for n={n}\n")
