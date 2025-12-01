import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Define Lorenz system parameters
sigma = 10
rho = 28
beta = 8/3

# Define Lorenz system
def lorenz(t, y):
    y1, y2, y3 = y
    return [sigma*(y2-y1), y1*(rho-y3)-y2, y1*y2-beta*y3]

# Define initial conditions
y0 = [2, 1, 2]

# Define time span and time step
t_span = [0, 100]
t_step = 0.003

# Solve Lorenz system using solve_ivp
sol = solve_ivp(lorenz, t_span, y0, t_eval=np.arange(t_span[0], t_span[1], t_step))

# Create figure and axis for animation
fig = plt.figure(figsize=(12,9))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-25, 25)
ax.set_ylim(-25, 25)
ax.set_zlim(0, 50)
ax.set_facecolor((0.1, 0.9, 0.2))  # set background color to green

# Define function to update animation
def update(i):
    ax.clear()
    ax.set_xlim(-25, 25)
    ax.set_ylim(-25, 25)
    ax.set_zlim(0, 50)
    ax.set_title("Lorenz system simulation")
    ax.set_facecolor((0.1, 0.9, 0.2))  # set background color to green
    ax.plot(sol.y[0, :i*20], sol.y[1, :i*20], sol.y[2, :i*20], color="navy")
    return ax

# Create animation
animation = FuncAnimation(fig, update, frames=1000, interval=10, blit=False)

# Show animation
plt.show()
