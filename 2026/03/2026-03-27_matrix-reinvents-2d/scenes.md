# 행렬이 만드는 2차원의 재발명

## Overview
- **Topic**: 함수공간의 좌표화와 미분/적분의 행렬 표현
- **Hook**: 순서쌍 \((3, 5)\)가 점이 아니라 함수를 가리킨다면?
- **Target Audience**: 고등학교 수학 ~ 대학 기초 선형대수
- **Scene Count**: 4 — 좌표 재해석 → 미분의 행렬화 → 적분의 역행렬화 → 고계 도함수와 확장
- **Key Insight**: 올바른 기저를 고르면 미적분이 선형대수의 언어로 바뀐다

---

## Scene 1: 순서쌍이 함수의 좌표가 된다
**Duration**: ~16s | **Layout**: split | **Template**: LayoutTemplateScene
**File**: `scenes/scene_01_function_coordinates.py`

### Left (Visual)
- 좌표축 위에 함수 곡선 \(ae^x\sin x + be^x\cos x\)
- ValueTracker 두 개로 \((a,b)\)가 \((0,0)\rightarrow(3,5)\)로 이동
- 축 위에 라이브 \((a,b)\) 표시

### Right (Equation)
```latex
(a,\; b) \;\longleftrightarrow\; a e^{x}\sin x + b e^{x}\cos x
```

### Animation Steps
1. 축과 대응식을 동시에 등장
2. tracker가 \((0,0)\)에서 \((3,5)\)로 이동하며 곡선이 실시간 반응
3. 최종 상태를 잠깐 유지

### Notes
- 기준 기저 순서를 명시한다: \((e^x\sin x,\ e^x\cos x)\)
- `always_redraw` + `ValueTracker` 패턴을 사용

---

## Scene 2: 이 좌표계에서는 미분이 행렬 곱셈이다
**Duration**: ~18s | **Layout**: split | **Template**: LayoutTemplateScene
**File**: `scenes/scene_02_derivative_matrix.py`

### Left (Visual)
- 미분 행렬 \(\mathbf{M}_{\text{diff}} = \begin{pmatrix}1 & -1 \\ 1 & 1\end{pmatrix}\)
- 아래에 기저 순서 \((e^x\sin x,\ e^x\cos x)\)를 함께 배치
- 행렬의 두 열이 각각 기저의 미분 결과를 뜻함을 시각적으로 강조

### Right (Equation)
```latex
\begin{pmatrix} a \\ b \end{pmatrix}
\xrightarrow{\text{diff}}
\begin{pmatrix} a-b \\ a+b \end{pmatrix}
\qquad
\begin{pmatrix} 2 \\ -1 \end{pmatrix}
\xrightarrow{\text{diff}}
\begin{pmatrix} 3 \\ 1 \end{pmatrix}
```

### Animation Steps
1. 미분 행렬과 일반 변환식 등장
2. 구체 예시로 전환하며 \((2,-1)\rightarrow(3,1)\)을 강조
3. 행렬 구조와 결과를 함께 고정

### Notes
- 기저 순서를 Scene 1과 동일하게 유지해야 부호가 흔들리지 않는다
- 예시 벡터는 실제 미분 예제와 맞춘다

---

## Scene 3: 적분은 역행렬이 된다
**Duration**: ~18s | **Layout**: split | **Template**: LayoutTemplateScene
**File**: `scenes/scene_03_integral_inverse.py`

### Left (Visual)
- \(\mathbf{M}_{\text{diff}}\)와 \(\mathbf{M}_{\text{int}}\) 두 행렬을 나란히 배치
- \(\mathbf{M}_{\text{int}}=\mathbf{M}_{\text{diff}}^{-1}\) 관계를 먼저 고정
- 아래쪽에 특이 행렬과 \(\det = 0\)으로 닫힘 실패를 대비

### Right (Equation)
```latex
\int(a+bx)\,dx = ax + \tfrac12 bx^2
```

### Animation Steps
1. 좋은 경우의 역행렬 관계를 먼저 보여줌
2. 특이 행렬과 \(\det = 0\)으로 전환
3. \(x^2\) 항이 생기며 원래 공간을 벗어나는 결과를 강조

### Notes
- 이 씬은 “닫혀 있기에 가능한 연산”과 “닫히지 않으면 역연산이 사라진다”를 대비시킨다
- 적분이 함수공간 내부에서만 행렬로 읽힌다는 점을 명확히 한다

---

## Scene 4: 2차원에서 더 큰 함수공간으로
**Duration**: ~18s | **Layout**: split | **Template**: LayoutTemplateScene
**File**: `scenes/scene_04_higher_powers_and_extension.py`

### Left (Visual)
- \( \mathbf{M}_{\text{diff}}^{2} - 2\mathbf{M}_{\text{diff}} + 2\mathbf{I} = \mathbf{O} \)를 먼저 보여주며 반복 구조를 연결
- \( y^{(n)} = \mathbf{M}_{\text{diff}}^{n}y \)로 고계 도함수를 압축
- 마지막에 더 큰 함수공간으로 자연스럽게 확장되는 마무리

### Right (Equation)
```latex
\widehat{f}(\xi)=\int_{-\infty}^{\infty} f(x)e^{-i\xi x}\,dx
```

### Animation Steps
1. 케일리-해밀턴 형태와 \(y^{(n)}\)를 차례로 제시
2. 마지막에 푸리에 계수/변환을 한 줄로 보여 더 큰 좌표계를 암시
3. 최종 구도 유지

### Notes
- 이 장면은 “좌표를 잘 고르면 미적분이 선형대수로 읽힌다”는 메시지를 더 큰 공간으로 확장한다
- 푸리에 한 줄은 확장 방향을 보여 주는 마무리 장치다

---

## Implementation Order
1. **Scene 1** — 기준 좌표계와 함수 대응을 먼저 고정
2. **Scene 2** — 미분 행렬의 열 의미를 바로 연결
3. **Scene 3** — 적분이 역행렬로 돌아오는 조건을 설명
4. **Scene 4** — 고계 도함수와 더 큰 함수공간으로 마무리
