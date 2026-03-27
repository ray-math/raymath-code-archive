---
artifact: scenes_plan
project: 2026-03-20_ordered-pair-as-function
selected_target_id: VT-01
source_excerpt: "순서쌍 (3,5)가 점이 아니라 함수의 좌표라면 미분은 행렬 곱셈이 된다."
on_screen_text_policy: formula_graph_only
---

# 순서쌍이 함수를 가리킨다면 — 미분은 행렬이 된다

## Overview
- **Source Target ID**: VT-01
- **Source Excerpt**: "순서쌍 (3,5)가 점이 아니라 함수의 좌표라면 미분은 행렬 곱셈이 된다."
- **Topic**: 함수공간의 좌표 표현과 미분의 행렬화
- **Hook**: 순서쌍 (3, 5)가 점이 아니라 함수를 가리킨다면?
- **Target Audience**: 고등학교 수학 ~ 대학 기초 선형대수
- **Scene Count**: 2 — 좌표 재해석(beat 1) + 행렬 곱셈=미분(beat 2)
- **Key Insight**: 함수에 좌표를 부여하면 미분이 행렬 곱셈으로 바뀐다
- **On-Screen Text Policy**: 수식/그래프만, 제목/부제 없음

---

## Scene 1: 순서쌍이 함수를 가리킨다면
- **Scene ID**: S01
- **Duration**: ~18s
- **Layout**: split
- **Template**: LayoutTemplateScene
- **File**: `scene_01_pair_as_function.py`

### Visual Goal
- `(3,5)`가 점 좌표가 아니라 함수 계수라는 재해석을 시청자가 그림만 보고 이해한다.

### Math Claim
- `(a,b)`는 `ae^x sin x + be^x cos x`의 좌표로 읽을 수 있고, `(3,5)`는 구체적인 함수 하나를 가리킨다.

### Visual
- 좌표축 (Axes, Palette.AXIS)
- 함수 그래프: `ae^x sin x + be^x cos x` (always_redraw, Palette.OBJECT_A)
- ValueTracker로 `(a,b)`가 `(0,0)→(3,5)`로 변하면서 곡선이 실시간 반응
- 축 위에 `(a, b)` 라이브 표시 (DecimalNumber, Palette.HIGHLIGHT)

### Equation
```latex
(a,\; b) \;\longleftrightarrow\; a e^{x}\sin x + b e^{x}\cos x
```

### Correspondence Checks
- 좌측 `(a,b)` 값이 변할 때 우측 식의 계수도 같은 값으로 바뀐다.
- 최종 그래프 모양과 우측 concrete equation이 같은 함수를 가리켜야 한다.

### Scene Success Test
- 시청자가 `(3,5)`를 점 좌표가 아니라 함수 계수로 읽게 된다.

### Animation Steps
1. 양쪽 동시 시작 (~4s): 왼쪽에서 축 등장, 오른쪽에서 대응 수식 Write.
2. `(a,b)`가 `(0,0)→(3,5)`로 이동하면서 곡선과 concrete equation이 함께 변환 (~6s).
3. 최종 구도 유지 (~4s).

### Notes
- ValueTracker 2개 (tracker_a, tracker_b), always_redraw로 곡선 갱신
- x_range=[0, 1.7], y_range=[-10, 18] (e^x 급증 방지)
- `_balanced_split()` 기준으로 좌우 여백을 맞춘다
- 이 장면은 "순서쌍을 함수 좌표로 다시 해석한다"는 개념 전환을 담당한다

---

## Scene 2: 미분은 행렬 곱셈이 된다
- **Scene ID**: S02
- **Duration**: ~20s
- **Layout**: split
- **Template**: LayoutTemplateScene
- **File**: `scene_02_matrix_differentiation.py`

### Visual Goal
- 미분이 복잡한 연산이 아니라 2×2 행렬이 좌표를 새 좌표로 보내는 작용처럼 보이게 만든다.

### Math Claim
- 기저 `{e^x sin x, e^x cos x}`에서 미분 연산은 `D = [[1, -1], [1, 1]]`로 표현되고, `D·(3,5)^T = (-2,8)^T`이다.

### Visual
- 2×2 행렬 `D = [[1, -1], [1, 1]]` (Matrix, Palette.TEXT)
- 첫째 열은 Palette.OBJECT_A, 둘째 열은 Palette.OBJECT_B로 강조
- 결과 벡터 `(-2, 8)`이 나오는 과정을 시각적으로 강조

### Equation
```latex
\begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix}
\begin{pmatrix} 3 \\ 5 \end{pmatrix}
=
\begin{pmatrix} -2 \\ 8 \end{pmatrix}
```

### Correspondence Checks
- 행렬의 첫째/둘째 열 강조가 각각 기저 함수의 미분 결과 계수와 대응한다.
- 우측 결과 벡터 `(-2,8)`은 Scene 1의 함수를 미분한 뒤의 새 계수와 정확히 일치해야 한다.

### Scene Success Test
- 시청자가 미분 연산을 좌표 공간에서의 행렬 작용으로 받아들인다.

### Animation Steps
1. 양쪽 동시 시작 (~3s): 왼쪽에서 행렬 등장, 오른쪽에서 행렬·벡터 곱 수식 Write.
2. 열 강조 + 수식 변환 (~4s): 왼쪽 열 강조와 함께 우측 결과 벡터로 TransformMatchingTex.
3. 결과 강조 (~2s): `(-2, 8)`을 Indicate로 강조.
4. 최종 구도 유지 (~4s).

### Notes
- Matrix mobject: `Matrix([[1, -1], [1, 1]])`
- `_balanced_split()` 기준으로 좌우 여백을 맞춘다
- 수학 검증:
  - `d/dx[e^x sin x] = e^x sin x + e^x cos x`
  - `d/dx[e^x cos x] = -e^x sin x + e^x cos x`
  - 따라서 `D = [[1, -1], [1, 1]]`, `D·(3,5)^T = (-2,8)^T`
- 이 장면은 "미분 = 행렬 곱셈"이라는 핵심 주장을 책임진다

---

## Implementation Order
1. **Scene 1** — ValueTracker와 equation correspondence 먼저 구현
2. **Scene 2** — Matrix + TransformMatchingTex 패턴 적용
