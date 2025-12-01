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
        for j in range(i+1, n+1):
            if is_square_sum(i, j):
                G.add_edge(i, j)
    return G

# 그래프를 그리는 함수
def draw_graph(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos)
    plt.show()

# 그래프 생성 및 그리기
n = 31  # 노드의 수
G = create_graph(n)
draw_graph(G)
