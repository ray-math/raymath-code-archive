import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# 테서렉트의 16개의 정점을 정의합니다.
vertices = np.array([[-1, -1, -1, -1], [-1, -1, 1, -1], [-1, 1, 1, -1], [-1, 1, -1, -1],
                     [1, -1, -1, -1], [1, -1, 1, -1], [1, 1, 1, -1], [1, 1, -1, -1],
                     [-1, -1, -1, 1], [-1, -1, 1, 1], [-1, 1, 1, 1], [-1, 1, -1, 1],
                     [1, -1, -1, 1], [1, -1, 1, 1], [1, 1, 1, 1], [1, 1, -1, 1]])

# 테서렉트의 엣지를 정의합니다.
edges = [[0, 1], [0, 3], [0, 4], [2, 1], [2, 3], [2, 6], [5, 1], [5, 4], [5, 6], [7, 3], [7, 4], [7, 6],
         [8, 9], [8, 11], [8, 12], [10, 9], [10, 11], [10, 14], [13, 9], [13, 12], [13, 14], [15, 11], [15, 12], [15, 14],
         [0, 8], [1, 9], [2, 10], [3, 11], [4, 12], [5, 13], [6, 14], [7, 15]]

fig = plt.figure(figsize=(20, 20))  # 그림 크기를 조정합니다.
ax = fig.add_subplot(111, projection='3d', autoscale_on=False)
ax.set_facecolor('yellowgreen')

# 애니메이션을 위한 업데이트 함수를 정의합니다.
def update(frame):
    ax.clear()
    ax.set_xlim3d(-1/2, 1/2)
    ax.set_ylim3d(-1/2, 1/2)
    ax.set_zlim3d(-1/2, 1/2)
    ax.axis('off')
    for edge in edges:
        # 4차원 회전 행렬을 사용하여 테서렉트를 회전시킵니다.
        rotation_matrix = np.array([[np.cos(frame), np.sin(frame), 0, 0],
                                    [-np.sin(frame), np.cos(frame), 0, 0],
                                    [0, 0, np.cos(frame), np.sin(frame)],
                                    [0, 0, -np.sin(frame), np.cos(frame)]])
        rotated_vertices = np.dot(vertices, rotation_matrix)
        # 4차원에서 3차원으로 투영합니다.
        projected_vertices = rotated_vertices[:, :3] / (4 - rotated_vertices[:, 3:4])
        ax.plot3D(*zip(projected_vertices[edge[0]], projected_vertices[edge[1]]), color='#004D81', linewidth=4)  # 선 굵기를 조정합니다.
    return fig,

# 애니메이션을 생성합니다.
ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 2 * np.pi, 1800), interval=16.67)

# FFMpegWriter를 사용하여 애니메이션을 mp4 파일로 저장합니다.
Writer = animation.writers['ffmpeg']
writer = Writer(fps=60, metadata=dict(artist='Me'), bitrate=1800)

# 애니메이션을 저장합니다.
ani.save('tesseract.mp4', writer=animation.FFMpegWriter(fps=60))
