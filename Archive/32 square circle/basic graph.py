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

# 그래프를 그리는 함수
def draw_graph(G, edge_width):
    # 노드의 색상을 결정하는 함수
    def get_node_color(node):
        if G.degree(node) == 0:
            return 'red'
        elif G.degree(node) == 1:
            return 'orange'
        else:
            return 'darkblue'

    node_colors = [get_node_color(node) for node in G.nodes()]
    pos = {node: (math.sin((node-1) * 2 * math.pi / len(G.nodes())), math.cos((node-1) * 2 * math.pi / len(G.nodes()))) for node in G.nodes()}
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1000, font_color='white', font_size=16, alpha=0.8, edge_color='gray', width=edge_width)
    plt.gcf().set_size_inches(10, 10)  # 이미지 사이즈 설정
    plt.gcf().patch.set_alpha(0)  # 이미지의 배경을 투명하게 설정
    plt.show()

# 그래프 생성 및 그리기
n = 31  # 노드의 수
edge_width = 2.0  # 엣지의 두께
G = create_graph(n)
draw_graph(G, edge_width)
