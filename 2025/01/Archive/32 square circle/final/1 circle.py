import math
import concurrent.futures
import os

def is_perfect_square(n):
    return math.isqrt(n) ** 2 == n

def hamiltonian_path(graph, vertex, path):
    path.append(vertex)

    if len(path) == len(graph):
        if path[0] in graph[path[-1]]:
            return True

    neighbors = sorted(graph[vertex], key=lambda v: len(graph[v]))
    for neighbor in neighbors:
        if neighbor not in path and hamiltonian_path(graph, neighbor, path):
            return True

    path.pop()
    return False

def build_graph(n):
    graph = {i: set() for i in range(1, n+1)}
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            if is_perfect_square(i + j):
                graph[i].add(j)
                graph[j].add(i)
    return graph

def find_hamiltonian_cycle(n):
    graph = build_graph(n)
    for start in range(1, n+1):
        path = []
        if hamiltonian_path(graph, start, path):
            max_index = path.index(max(path))
            path = path[max_index:] + path[:max_index]
            return path
    return None

# List of numbers for which we need to find Hamiltonian cycles
numbers_to_check = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

# Use maximum available CPU cores
worker_threads = os.cpu_count()

print(f"Using {worker_threads} threads.")

with concurrent.futures.ThreadPoolExecutor(max_workers=worker_threads) as executor:
    futures = {executor.submit(find_hamiltonian_cycle, n): n for n in numbers_to_check}
    for future in concurrent.futures.as_completed(futures):
        n = futures[future]
        cycle = future.result()
        if cycle:
            print(f"<details><summary>Hamiltonian cycle for n={n}</summary>")
            print(f"{cycle}")
            print("</details>")
        else:
            print(f"No Hamiltonian cycles found for n={n}")
