import math
import os
import concurrent.futures

def is_perfect_square(n):
    return math.isqrt(n) ** 2 == n

def hamiltonian_path(graph, vertex, path, result):
    path.append(vertex)

    if len(path) < len(graph):
        neighbors = sorted(graph[vertex], key=lambda v: len(graph[v]))
        for neighbor in neighbors:
            if neighbor not in path:
                hamiltonian_path(graph, neighbor, path, result)
    elif path[0] in graph[path[-1]]:
        result.append(list(path))

    path.pop()

def build_graph(n):
    graph = {i: set() for i in range(1, n+1)}
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            if is_perfect_square(i + j):
                graph[i].add(j)
                graph[j].add(i)
    return graph

def is_equal_cycle(cycle1, cycle2):
    return cycle1[1:] == cycle2[:0:-1]

def find_hamiltonian_cycle(n):
    graph = build_graph(n)
    result = []
    hamiltonian_path(graph, n, [], result)

    unique_cycles = []
    for cycle in result:
        if not any(is_equal_cycle(cycle, unique_cycle) for unique_cycle in unique_cycles):
            unique_cycles.append(cycle)

    return n, unique_cycles

start_n = 32
end_n = 32

# Use maximum available CPU cores
worker_threads = os.cpu_count()
print(f"Using {worker_threads} threads.")

# Use ThreadPoolExecutor to run tasks concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=worker_threads) as executor:
    futures = {executor.submit(find_hamiltonian_cycle, n): n for n in range(start_n, end_n+1)}
    for future in concurrent.futures.as_completed(futures):
        n, cycles = future.result()

        # File path for saving the results
        script_dir = os.path.dirname(os.path.realpath(__file__))
        output_file_path = os.path.join(script_dir, f"hamiltonian_cycles_{n}.md")

        # Open the output file
        with open(output_file_path, "w") as f:
            if cycles:
                f.write(f"\nHamiltonian cycles for n={n} found: {len(cycles)}\n")
                for i, cycle in enumerate(cycles, start=1):
                    f.write(f"Cycle {i}: {cycle}\n")
            else:
                f.write(f"\nNo Hamiltonian cycles found for n={n}\n")
