import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import solve_ivp

def rossler_system(t, xyz, a, b, c):
    x, y, z = xyz
    return [
        -y - z,
        x + a * y,
        b + z * (x - c)
    ]

def update_plot(num, data, line):
    line.set_data(data[:2, :num])
    line.set_3d_properties(data[2, :num])
    return line,

def animate_rossler_attractor(a, b, c, initial_conditions, t_span, num_points):
    t_eval = np.linspace(t_span[0], t_span[1], num_points)
    solution = solve_ivp(rossler_system, t_span, initial_conditions, args=(a, b, c), t_eval=t_eval)
    data = solution.y

    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('lightgreen')

    # Calculate axis limits and set them
    x_min, x_max = np.min(data[0]), np.max(data[0])
    y_min, y_max = np.min(data[1]), np.max(data[1])
    z_min, z_max = np.min(data[2]), np.max(data[2])
    x_range = 5
    y_range = 5
    z_range = 10
    ax.set_xlim(x_min - x_range, x_max + x_range)
    ax.set_ylim(y_min - y_range, y_max + y_range)
    ax.set_zlim(z_min - z_range, z_max + z_range)

    line, = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1], lw=1, color='navy')

    ax.set_title("Rossler Attractor")

    ani = FuncAnimation(fig, update_plot, num_points, fargs=(data, line), interval=1, blit=True)
    plt.show()

if __name__ == "__main__":
    a = 0.2
    b = 0.2
    c = 5.7
    initial_conditions = [0, 1, 0]
    t_span = (0, 100)
    num_points = 10000

    animate_rossler_attractor(a, b, c, initial_conditions, t_span, num_points)
