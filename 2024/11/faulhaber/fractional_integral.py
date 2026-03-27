import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 변수 및 함수 정의
x = sp.symbols("x")
f = sp.sin(x)


# Caputo 분수 차수 미분 함수 정의
def caputo_derivative(f, x, alpha):
    n = sp.ceiling(alpha)  # alpha보다 큰 가장 작은 정수
    t = sp.symbols("t")
    integrand = (sp.diff(f, (x, n)) / sp.gamma(n - alpha)) * (x - t) ** (n - alpha - 1)
    return sp.integrate(integrand, (t, 0, x))


# 초기 alpha 값
alpha_init = 0.5

# Caputo 분수 차수 미분 계산
caputo_diff = caputo_derivative(f, x, alpha_init)
caputo_diff_func = sp.lambdify(x, caputo_diff, "numpy")

# x값 범위 설정
x_vals = np.linspace(-2 * np.pi, 4 * np.pi, 400)
f_vals = np.sin(x_vals)

# `sqrt` 함수에서 발생하는 오류를 피하기 위해 양의 값으로만 제한
x_vals_pos = np.where(x_vals >= 0, x_vals, np.nan)
caputo_diff_vals = caputo_diff_func(x_vals_pos)

# 그래프 설정
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
(l_sin,) = plt.plot(x_vals, f_vals, label="sin(x)", color="blue")
(l_caputo,) = plt.plot(
    x_vals,
    caputo_diff_vals,
    label=f"Caputo fractional derivative of order {alpha_init}",
    color="red",
    linestyle="--",
)

# x축과 y축 더 진하게
plt.axhline(0, color="black", linewidth=1.3)
plt.axvline(0, color="black", linewidth=1.3)

# 그리드 설정
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.minorticks_on()
plt.grid(which="minor", color="gray", linestyle=":", linewidth=0.5)

# x축 그리드 간격을 pi/2로 설정
plt.xticks(
    np.arange(-2 * np.pi, 4 * np.pi + np.pi / 2, np.pi / 2),
    [f"${int(i/2)}\\pi$" if i % 2 == 0 else "" for i in range(-4, 9)],
)

plt.title(r"$\sin(x)$ and its Caputo fractional derivative")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()

# 슬라이더 설정
ax_alpha = plt.axes([0.25, 0.1, 0.65, 0.03])
slider_alpha = Slider(ax_alpha, "Alpha", 0.1, 2.0, valinit=alpha_init, valstep=0.1)


# 슬라이더 이벤트 처리
def update(val):
    alpha = slider_alpha.val
    caputo_diff = caputo_derivative(f, x, alpha)
    caputo_diff_func = sp.lambdify(x, caputo_diff, "numpy")
    caputo_diff_vals = caputo_diff_func(x_vals_pos)

    l_caputo.set_ydata(caputo_diff_vals)
    l_caputo.set_label(f"Caputo fractional derivative of order {alpha}")
    ax.legend()
    fig.canvas.draw_idle()


slider_alpha.on_changed(update)

plt.show()
