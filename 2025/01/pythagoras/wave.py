import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib.animation import FuncAnimation

# Create a grid of points
x = np.linspace(-5, 5, 10)
y = np.linspace(-5, 5, 10)
x, y = np.meshgrid(x, y)

# Function to describe the wave
def wave(x, y, t):
    r = np.sqrt(x**2 + y**2)
    return np.sin(r - t)

# Function to describe the vector field
def vector_field(x, y, z, t):
    u = -y * np.sin(t)
    v = x * np.sin(t)
    w = z * np.sin(t)
    return u, v, w

# Create a figure and a 3D axis
fig = plt.figure(figsize=(18, 12))  # Increase the size of the figure
ax = fig.add_subplot(111, projection='3d')

# Remove the axes
ax.axis('off')

# Set the background color
ax.set_facecolor('yellowgreen')

# Create a quiver plot (vector field)
quiver = ax.quiver(x, y, wave(x, y, 0), *vector_field(x, y, wave(x, y, 0), 0), color='#004D81')

# Update function for the animation
def update(t):
    global quiver
    # Remove the old quiver plot
    quiver.remove()
    # Create a new quiver plot for the current time step
    z = wave(x, y, t)
    quiver = ax.quiver(x, y, z, *vector_field(x, y, z, t), color='#004D81')
    # Set the z limit
    ax.set_xlim(-7, 7)
    ax.set_ylim(-7, 7)
    ax.set_zlim(-7, 7)

# Create an animation
ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 100), interval=100)

# Show the plot
plt.show()
