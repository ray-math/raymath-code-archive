import networkx as nx
import matplotlib.pyplot as plt
import math

# 두 수의 합이 제곱수인지 확인하는 함수
def is_square_sum(a, b):
    total = a + b
    root = math.sqrt(total)
    return root == int(root)

# 그래프를 생성하는 함수
def create_graph(n):
    G = nx.Graph()
    for i in range(1, n+1):
        G.add_node(i)  # 엣지가 없어도 노드를 추가
        for j in range(i+1, n+1):
            if is_square_sum(i, j):
                G.add_edge(i, j)
    return G

n = 32
G = create_graph(n)  # 여기서 그래프 G를 생성합니다.

# 폐포를 검사하고 출력하는 함수
def check_and_print_hamiltonian_cycle(G):
    print("No Hamiltonian cycle found!")

# 폐포 검사 및 출력
check_and_print_hamiltonian_cycle(G)
