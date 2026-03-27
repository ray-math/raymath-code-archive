---
artifact: scenes_plan
project: 2026-03-12_pi-four-methods
selected_target_id: VT-01
source_excerpt: "정규분포 적분, 버퐁의 바늘, 바젤 문제, 진자 주기에서 반복해서 나타나는 pi"
on_screen_text_policy: formula_graph_only
---

# PI가 나오는 4가지 과정

## Overview
- **Source Target ID**: VT-01
- **Source Excerpt**: "정규분포 적분, 버퐁의 바늘, 바젤 문제, 진자 주기에서 반복해서 나타나는 pi"
- **Topic**: 서로 다른 현상에서 나타나는 \(\pi\)의 연결
- **Hook**: 원이 보이지 않는 상황에서도 왜 \(\pi\)가 등장하는가
- **Target Audience**: 고등학교 수학 ~ 기초 미적분 수준
- **Scene Count**: 4 — 서로 다른 네 개의 visual system이 같은 상수 \(\pi\)로 이어진다
- **Key Insight**: 기하, 확률, 급수, 진동이 서로 다른 얼굴로 같은 \(\pi\)를 드러낸다
- **On-Screen Text Policy**: 수식/그래프만, 제목/부제 없음

---

## Scene 1: Gaussian Integral
- **Scene ID**: S01
- **Duration**: ~14s
- **Layout**: split
- **Template**: LayoutTemplateScene
- **File**: `pi_four_methods.py`

### Visual Goal
- 종 모양 곡선 아래 면적이 단순한 숫자가 아니라 \(\sqrt{\pi}\)와 연결된다는 놀라움을 만든다.

### Math Claim
- \(\int_{-\infty}^{\infty} e^{-x^2}\,dx=\sqrt{\pi}\).

### Visual
- 좌표축, \(e^{-x^2}\) 그래프, 곡선 아래 면적, 꼬리에서 0으로 가까워지는 guide

### Equation
```latex
\int_{-\infty}^{\infty} e^{-x^2}\,dx=\sqrt{\pi}
```

### Correspondence Checks
- 면적 음영은 적분량과 직접 대응한다.
- 꼬리 guide는 적분 구간이 무한대로 뻗는 감각을 보강한다.

### Scene Success Test
- 시청자가 곡선 아래 면적이라는 시각이 \(\sqrt{\pi}\)와 연결된다는 점을 기억한다.

### Animation Steps
1. 축과 그래프를 동시에 제시한다. (~3s)
2. 면적을 강조하고 꼬리 점/guide를 추가한다. (~5s)
3. 최종 구도를 유지한다. (~4s)

### Notes
- 첫 장면은 “원 없이도 \(\pi\)가 나온다”는 첫 surprise를 만든다.
- 이후 장면들이 모두 이 surprise를 다른 방식으로 반복 강화한다.

---

## Scene 2: Buffon's Needle
- **Scene ID**: S02
- **Duration**: ~16s
- **Layout**: split
- **Template**: LayoutTemplateScene
- **File**: `pi_four_methods.py`

### Visual Goal
- 무작위 실험의 빈도값이 \(\pi\) 추정으로 이어지는 걸 한 화면에서 읽게 한다.

### Math Claim
- 바늘 교차 확률 \(P\)로부터 \(\pi=\frac{2\ell}{dP}\)를 추정할 수 있다.

### Visual
- 평행 바닥선, 랜덤 각도의 바늘 투척, 교차/비교차 색상, \(n\), \(P\), \(\hat{\pi}\) live display

### Equation
```latex
\pi=\frac{2\ell}{dP}
```

### Correspondence Checks
- 교차 횟수 비율이 \(P\) display와 연결된다.
- \(P\) 값이 변할 때 \(\hat{\pi}\) 추정값도 같은 프레임에서 같이 갱신된다.

### Scene Success Test
- 시청자가 무작위 실험의 빈도값이 \(\pi\) 추정으로 바로 이어진다고 느낀다.

### Animation Steps
1. 바닥선과 통계 display, 우측 식을 동시에 연다. (~2s)
2. 바늘을 반복 투척하며 \(n\), \(P\), \(\hat{\pi}\)를 지속 갱신한다. (~10s)
3. 최종 추정값 상태를 유지한다. (~4s)

### Notes
- 이 장면의 핵심은 확률 실험과 수식 추정이 분리되지 않고 동시에 읽히는 것이다.

---

## Scene 3: Basel Series
- **Scene ID**: S03
- **Duration**: ~15s
- **Layout**: split
- **Template**: LayoutTemplateScene
- **File**: `pi_four_methods.py`

### Visual Goal
- \(1/n^2\) 항의 누적합이 \(\pi^2/6\)으로 접근하는 걸 그래프적 수렴으로 느끼게 한다.

### Math Claim
- \(\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{6}\).

### Visual
- 기준선 \(\pi^2/6\), 항별 막대, 누적합 선분, 이동 점, \(S_n\) display

### Equation
```latex
\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{6}
```

### Correspondence Checks
- 항별 막대는 각 \(1/n^2\) 항과 대응한다.
- 누적합 선분과 점의 위치는 \(S_n\) 값 display와 일치해야 한다.

### Scene Success Test
- 시청자가 누적합이 \(\pi^2/6\)으로 접근하는 수렴 그림을 한눈에 읽는다.

### Animation Steps
1. 축, 기준선, 우측 식을 동시에 연다. (~2s)
2. 항을 누적하며 막대와 누적합 곡선을 함께 그린다. (~9s)
3. 목표값 근처 final frame을 유지한다. (~4s)

### Notes
- 이 장면은 “급수도 \(\pi\)를 부른다”는 패턴 인식을 담당한다.

---

## Scene 4: Pendulum Period
- **Scene ID**: S04
- **Duration**: ~15s
- **Layout**: split
- **Template**: LayoutTemplateScene
- **File**: `pi_four_methods.py`

### Visual Goal
- 순수한 물리 진동 장면에서 \(\pi\)가 식에 자연스럽게 등장하는 걸 보여준다.

### Math Claim
- 단진자 주기는 \(T=2\pi\sqrt{\frac{L}{g}}\) 이다.

### Visual
- 지지대, 중심선, 진자 줄/추, \(L\) label, 시간축 위 각도 변화 곡선

### Equation
```latex
T=2\pi\sqrt{\frac{L}{g}}
```

### Correspondence Checks
- 진자의 왕복 속도와 하단 phase curve가 같은 시간 변수에 의해 움직인다.
- \(L\) label은 실제 줄 길이와 함께 움직여 물리적 의미를 유지한다.

### Scene Success Test
- 시청자가 진자의 주기식에 \(\pi\)가 자연스럽게 박혀 있다는 인상을 받는다.

### Animation Steps
1. 진자 구조와 phase curve, 우측 식을 동시에 연다. (~3s)
2. 한 주기 동안 진자와 phase dot을 함께 움직인다. (~8s)
3. 최종 구도를 유지한다. (~4s)

### Notes
- 마지막 장면은 “\(\pi\)는 기하 상수이면서 물리 리듬에도 박혀 있다”는 인상으로 시리즈를 닫는다.

---

## Implementation Order
1. **Scene 1** — Gaussian graph/area relation 먼저 구현
2. **Scene 3** — 누적합/수렴 표현 구현
3. **Scene 2** — 확률 샘플링과 live stats 연결
4. **Scene 4** — updater 기반 진동과 phase correspondence 구현
