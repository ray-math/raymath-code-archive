import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 1. 헬퍼 함수 및 환경 정의 (이전과 동일) ---
def calculate_z(x, y):
    dist = np.sqrt(x**2 + y**2) + 1e-6
    return np.sin(dist * 2) * np.exp(-dist * 0.2)

def get_ripple_surface(x, y):
    dist = np.sqrt(x**2 + y**2) + 1e-6
    z = calculate_z(x, y)
    dz_dr = (2 * np.cos(dist * 2) - 0.2 * np.sin(dist * 2)) * np.exp(-dist * 0.2)
    dr_dx = x / dist
    dr_dy = y / dist
    dz_dx = dz_dr * dr_dx
    dz_dy = dz_dr * dr_dy
    normal = np.array([-dz_dx, -dz_dy, 1])
    return np.array([x, y, z]), normal / np.linalg.norm(normal)

def project_to_tangent_plane(v, normal):
    v_projected = v - np.dot(v, normal) * normal
    norm = np.linalg.norm(v_projected)
    return v_projected / (norm + 1e-6)

def vortex_field(p):
    swirl_vector_2d = np.array([-p[1], p[0], 0])
    _, normal = get_ripple_surface(p[0], p[1])
    return project_to_tangent_plane(swirl_vector_2d, normal)

def parallel_transport_step(p_prev, v_prev, p_current):
    _, n_current = get_ripple_surface(p_current[0], p_current[1])
    v_transported = project_to_tangent_plane(v_prev, n_current)
    return v_transported

# --- 2. 3D 그래프 및 애니메이션 설정 ---
fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=25, azim=-75)
ax.axis('off')

x_range = np.linspace(-12, 12, 120)
y_range = np.linspace(-12, 12, 120)
X, Y = np.meshgrid(x_range, y_range)
Z = calculate_z(X, Y)
ax.plot_surface(X, Y, Z, alpha=0.1, cmap='ocean', zorder=0)

points = np.stack([X, Y], axis=-1)[::8, ::8]
for row in points:
    for point_2d in row:
        p, _ = get_ripple_surface(point_2d[0], point_2d[1])
        v = vortex_field(p)
        ax.quiver(*p, *v, length=0.5, color='gray', alpha=0.4, zorder=1)

# --- 3. 세 주인공의 경로 및 객체 정의 ---
n_frames = 500
dt = 0.15 

# 1. 파란색 (코르크 마개)
path_blue = [get_ripple_surface(-3, -8)[0]]
v_initial_blue = vortex_field(path_blue[0])
path_line_blue, = ax.plot([], [], [], 'blue', linewidth=4)
quiver_p_blue = ax.quiver([],[],[],[],[],[], color='blue', linestyle='--', length=1.2)
quiver_f_blue = ax.quiver([],[],[],[],[],[], color='black', length=1.2)
quiver_d_blue = ax.quiver([],[],[],[],[],[], color='blue', length=1.0)


# 2. 주황색 (유조선)
path_orange = np.array([get_ripple_surface(x, 0.08 * x**2 - 5)[0] for x in np.linspace(8, -8, n_frames)])
v_initial_orange = np.array([-0.5, -0.5, 0])
v_initial_orange = project_to_tangent_plane(v_initial_orange, get_ripple_surface(path_orange[0][0], path_orange[0][1])[1])
path_line_orange, = ax.plot([], [], [], 'orange', linewidth=4)
quiver_p_orange = ax.quiver([],[],[],[],[],[], color='orange', linestyle='--', length=1.2)
quiver_f_orange = ax.quiver([],[],[],[],[],[], color='black', length=1.2)
quiver_d_orange = ax.quiver([],[],[],[],[],[], color='orange', length=1.0)

# 3. 검은색 (모터보트)
path_black = np.array([get_ripple_surface(x, -0.8 * x + 1)[0] for x in np.linspace(-10, 10, n_frames)])
v_initial_black = path_black[1] - path_black[0]
v_initial_black = v_initial_black / np.linalg.norm(v_initial_black)
path_line_black, = ax.plot([], [], [], 'black', linewidth=4)
quiver_p_black = ax.quiver([],[],[],[],[],[], color='#666666', linestyle='--', length=1.2)
quiver_f_black = ax.quiver([],[],[],[],[],[], color='black', length=1.2)
quiver_d_black = ax.quiver([],[],[],[],[],[], color='#333333', length=1.0)


# --- 4. 애니메이션 업데이트 함수 ---
v_parallel_blue = v_initial_blue
v_parallel_orange = v_initial_orange
v_parallel_black = v_initial_black

def update(frame):
    global v_parallel_blue, v_parallel_orange, v_parallel_black, path_blue
    
    # 각 객체에 대한 quiver 핸들러
    global quiver_p_blue, quiver_f_blue, quiver_d_blue
    global quiver_p_orange, quiver_f_orange, quiver_d_orange
    global quiver_p_black, quiver_f_black, quiver_d_black
    
    # 이전 프레임의 화살표들 모두 삭제
    quivers = [quiver_p_blue, quiver_f_blue, quiver_d_blue, 
               quiver_p_orange, quiver_f_orange, quiver_d_orange,
               quiver_p_black, quiver_f_black, quiver_d_black]
    for q in quivers: q.remove()

    # 1. 파란색 (코르크 마개) 업데이트
    p_curr_b = path_blue[-1]
    v_field_b = vortex_field(p_curr_b)
    p_next_b, _ = get_ripple_surface(*(p_curr_b[:2] + v_field_b[:2] * dt))
    path_blue.append(p_next_b)
    path_blue_np = np.array(path_blue)
    path_line_blue.set_data(path_blue_np[:, 0], path_blue_np[:, 1])
    path_line_blue.set_3d_properties(path_blue_np[:, 2])
    v_parallel_blue = parallel_transport_step(p_curr_b, v_parallel_blue, p_next_b)
    v_deriv_b = v_field_b - v_parallel_blue
    
    quiver_p_blue = ax.quiver(*p_next_b, *v_parallel_blue, color='blue', linestyle='--', length=1.2)
    quiver_f_blue = ax.quiver(*p_next_b, *v_field_b, color='black', length=1.2)
    quiver_d_blue = ax.quiver(*p_next_b, *v_deriv_b, color='blue', length=1.0)

    # 2. 주황색 (유조선) 업데이트
    p_curr_o, p_prev_o = path_orange[frame], path_orange[max(0, frame-1)]
    path_line_orange.set_data(path_orange[:frame, 0], path_orange[:frame, 1])
    path_line_orange.set_3d_properties(path_orange[:frame, 2])
    v_parallel_orange = parallel_transport_step(p_prev_o, v_parallel_orange, p_curr_o)
    v_field_o = vortex_field(p_curr_o)
    v_deriv_o = v_field_o - v_parallel_orange
    
    quiver_p_orange = ax.quiver(*p_curr_o, *v_parallel_orange, color='orange', linestyle='--', length=1.2)
    quiver_f_orange = ax.quiver(*p_curr_o, *v_field_o, color='black', length=1.2)
    quiver_d_orange = ax.quiver(*p_curr_o, *v_deriv_o, color='orange', length=1.0)

    # 3. 검은색 (모터보트) 업데이트
    p_curr_k, p_prev_k = path_black[frame], path_black[max(0, frame-1)]
    path_line_black.set_data(path_black[:frame, 0], path_black[:frame, 1])
    path_line_black.set_3d_properties(path_black[:frame, 2])
    v_parallel_black = parallel_transport_step(p_prev_k, v_parallel_black, p_curr_k)
    v_field_k = vortex_field(p_curr_k)
    v_deriv_k = v_field_k - v_parallel_black
    
    quiver_p_black = ax.quiver(*p_curr_k, *v_parallel_black, color='#666666', linestyle='--', length=1.2)
    quiver_f_black = ax.quiver(*p_curr_k, *v_field_k, color='black', length=1.2)
    quiver_d_black = ax.quiver(*p_curr_k, *v_deriv_k, color='#333333', length=1.0)
        
    return path_line_blue, path_line_orange, path_line_black

# --- 5. 애니메이션 실행 ---
ani = FuncAnimation(fig, update, frames=n_frames, interval=30, blit=False, repeat=False)
ax.set_title("Three Travelers: A Comparative Visualization")
ax.set_zlim(-2, 3)
ax.set_box_aspect([1, 1, 0.4])

legend_text = (
    "--- Vector Legend ---\n"
    "[Dashed  --]: Parallel Transport (Inertial Heading)\n"
    "[Black   --]: Actual Field (Wind at Location)\n"
    "[Solid Color]: Covariant Derivative (Required Force / Path Curvature)\n\n"
    "--- Traveler Legend ---\n"
    "[Blue Path]: The Cork (Drifts with the wind)\n"
    "[Orange Path]: The Supertanker (Follows pre-defined path)\n"
    "[Black Path]: The Motorboat (Follows pre-defined path)"
)
ax.text2D(0.02, 0.98, legend_text, transform=ax.transAxes, fontsize=12,
          verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', fc='lightyellow', alpha=0.8))

plt.show()