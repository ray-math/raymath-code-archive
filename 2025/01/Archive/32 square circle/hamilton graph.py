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

# 띄어쓰기로 구분된 숫자 문자열을 입력 받아 이에 해당하는 엣지 목록을 반환하는 함수
def get_hamiltonian_edges(hamiltonian_nodes_str):
    hamiltonian_nodes = list(map(int, hamiltonian_nodes_str.split()))  # 띄어쓰기로 구분된 숫자 문자열을 리스트로 변환
    edges = [(hamiltonian_nodes[i-1], hamiltonian_nodes[i]) for i in range(1, len(hamiltonian_nodes))]
    edges.append((hamiltonian_nodes[-1], hamiltonian_nodes[0]))  # 마지막 노드와 첫번째 노드를 연결
    return edges

# 그래프를 그리는 함수
def draw_graph_with_hamiltonian_path(G, hamiltonian_edges, edge_width):
    pos = {node: (math.sin((node-1) * 2 * math.pi / len(G.nodes())), math.cos((node-1) * 2 * math.pi / len(G.nodes()))) for node in G.nodes()}

    # 모든 엣지를 회색으로 그림
    nx.draw_networkx_edges(G, pos, alpha=0.2, edge_color='gray', width=edge_width)

    # 해밀턴 경로의 엣지를 검은색으로 그림
    nx.draw_networkx_edges(G, pos, edgelist=hamiltonian_edges, edge_color='black', width=edge_width)

    # 노드를 그림
    nx.draw_networkx_nodes(G, pos, node_color='darkblue', node_size=800, alpha=0.8)
    nx.draw_networkx_labels(G, pos, font_color='white', font_size=16)
    
    plt.gcf().set_size_inches(12, 12)  # 이미지 사이즈 설정
    plt.gcf().patch.set_alpha(0)  # 이미지의 배경을 투명하게 설정
    plt.show()

# 숫자 배열 (문자열)
hamiltonian_nodes_str = "1 8 41 40 24 12 37 27 9 16 33 3 6 10 15 34 30 19 17 32 4 21 28 36 13 23 26 38 11 25 39 42 22 14 2 7 18 31 5 20 29 35"

# 숫자 배열에 해당하는 엣지 목록을 얻음
hamiltonian_edges = get_hamiltonian_edges(hamiltonian_nodes_str)

# 숫자 배열에서 가장 큰 숫자를 찾아 노드 수로 사용
n = max(map(int, hamiltonian_nodes_str.split()))

edge_width = 2.0  # 엣지의 두께
G = create_graph(n)
draw_graph_with_hamiltonian_path(G, hamiltonian_edges, edge_width)
