import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# 원점
origin = [0, 0, 0]

# 초기화
fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(111, projection='3d', autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2), zlim=(-2, 2))
ax.grid(None)
ax.set_facecolor('yellowgreen')
scale = 2

# 이전까지의 A점의 위치를 저장할 변수
trail_x = []
trail_y = []
trail_z = []

# Create Line3D object for the trail line
trail_line, = ax.plot([], [], [], lw=2, color='#004D81')
arrow_line, = ax.plot([], [], [], lw=2, color='#004D81')
dashed_lines = [ax.plot([], [], [], linestyle='dashed', color='gray')[0] for _ in range(12)]

def init():
    trail_line.set_data([], [])
    trail_line.set_3d_properties([])
    arrow_line.set_data([], [])
    arrow_line.set_3d_properties([])
    for line in dashed_lines:
        line.set_data([], [])
        line.set_3d_properties([])
    return [trail_line, arrow_line] + dashed_lines

# Create Line3D object for the point
point, = ax.plot([], [], [], '>', markersize=10, color='#004D81')

# 애니메이션
def animate(i):
    theta = 3 * np.pi * (i / 1440)  # 0 to 2pi
    phi = np.arccos(1 - 1 * (i / 1440))  # 0 to pi
    x = scale * np.sin(phi) * np.cos(theta)
    y = scale * np.sin(phi) * np.sin(theta)
    z = scale * np.cos(phi)

    # Update point
    point.set_data([x], [y])
    point.set_3d_properties([z])

    # A점의 자취를 그리기 위해 이전까지의 위치 저장
    trail_x.append(x)
    trail_y.append(y)
    trail_z.append(z)

    # 자취 선 그리기
    trail_line.set_data(trail_x, trail_y)
    trail_line.set_3d_properties(trail_z)

    # Arrow line from origin to point A
    arrow_line.set_data([0, x], [0, y])
    arrow_line.set_3d_properties([0, z])
    
    # Update dashed lines
    dashed_lines[0].set_data([x, x], [y, y])
    dashed_lines[0].set_3d_properties([z, 0])

    dashed_lines[1].set_data([x, x], [y, 0])
    dashed_lines[1].set_3d_properties([z, z])

    dashed_lines[2].set_data([x, 0], [y, y])
    dashed_lines[2].set_3d_properties([z, z])

    dashed_lines[3].set_data([x, x], [y, 0])
    dashed_lines[3].set_3d_properties([0, 0])

    dashed_lines[4].set_data([x, 0], [y, y])
    dashed_lines[4].set_3d_properties([0, 0])

    dashed_lines[5].set_data([x, x], [0, 0])
    dashed_lines[5].set_3d_properties([z, 0])

    dashed_lines[6].set_data([x, 0], [0, 0])
    dashed_lines[6].set_3d_properties([z, z])

    dashed_lines[7].set_data([0, 0], [y, y])
    dashed_lines[7].set_3d_properties([z, 0])

    dashed_lines[8].set_data([0, 0], [y, 0])
    dashed_lines[8].set_3d_properties([z, z])

    dashed_lines[9].set_data([x, 0], [0, 0])
    dashed_lines[9].set_3d_properties([0, 0])

    dashed_lines[10].set_data([0, 0], [y, 0])
    dashed_lines[10].set_3d_properties([0, 0])

    dashed_lines[11].set_data([0, 0], [0, 0])
    dashed_lines[11].set_3d_properties([z, 0])

    # 텍스트를 생성합니다
    label_A = ax.text(x, y, z, f"({x:.2f},{y:.2f},{z:.2f})", color='#004D81', fontsize=12, ha='left')
    label_X = ax.text(x, 0, 0, f"{x:.2f}", color='gray', fontsize=12, ha='left')
    label_Y = ax.text(0, y, 0, f"{y:.2f}", color='gray', fontsize=12, ha='left')
    label_Z = ax.text(0, 0, z, f"{z:.2f}", color='gray', fontsize=12, ha='left')

    return [trail_line, arrow_line, label_A, label_X, label_Y, label_Z, point] + dashed_lines

ani = animation.FuncAnimation(fig, animate, frames=5760, interval=20, blit=True, init_func=init)

# Axis off and drawing coordinate lines
ax.axis('off')
ax.plot([-scale*1.5, scale*1.5], [0, 0], [0, 0], color='black')
ax.plot([0, 0], [-scale*2, scale*2], [0, 0], color='black')
ax.plot([0, 0], [0, 0], [-scale*2, scale*2], color='black')

plt.show()