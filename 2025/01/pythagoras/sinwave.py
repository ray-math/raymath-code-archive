import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

# 그래프 생성
fig = plt.figure(figsize=(20, 20))
ax = fig.add_subplot(111, projection="3d")
ax.set_facecolor("yellowgreen")
ax.axis("off")


# 벡터 필드를 그리는 함수
def update(frame):
    ax.clear()
    ax.axis("off")
    ax.set_xlim3d(-12, 12)
    ax.set_ylim3d(-12, 12)
    ax.set_zlim3d(-12, 12)
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)
    x, y = np.meshgrid(x, y)
    z = np.sin(np.sqrt(x**2 + y**2) - (frame / 10) * 0.1)  # 현수면
    ax.plot_surface(x, y, z, rstride=5, cstride=5, color="k", alpha=0.4)
    magnitude = np.abs(np.sin((frame / 10) * 0.01))  # 벡터의 크기를 조절합니다.
    ax.quiver(
        x[::6, ::6],
        y[::6, ::6],
        z[::6, ::6],
        x[::6, ::6],
        y[::6, ::6],
        z[::6, ::6] * 0,
        length=magnitude / 3,
        color="#004D81",
        linewidths=2,
    )  # 선 굵기를 조정합니다.
    ax.view_init(elev=30.0, azim=frame / 10)  # 카메라 시점을 변경합니다.


plot.show()
