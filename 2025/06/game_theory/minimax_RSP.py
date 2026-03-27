import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

random.seed(42)

def random_strategy(_, __):
    # 완전히 균등한 랜덤 전략 (33.33% 가위, 33.33% 바위, 33.33% 보)
    return random.randint(0, 2)

def scissors_biased_10(_, __):
    # 가위가 10% 더 많이 나오는 전략 (40% 가위, 30% 바위, 30% 보)
    return random.choices([0,1,2], weights=[0.4,0.3,0.3])[0]

def rock_biased_10(_, __):
    # 바위가 10% 더 많이 나오는 전략 (30% 가위, 40% 바위, 30% 보)
    return random.choices([0,1,2], weights=[0.3,0.4,0.3])[0]

def paper_biased_10(_, __):
    # 보가 10% 더 많이 나오는 전략 (30% 가위, 30% 바위, 40% 보)
    return random.choices([0,1,2], weights=[0.3,0.3,0.4])[0]

def scissors_biased_heavy(_, __):
    # 가위가 매우 많이 나오는 전략 (70% 가위, 15% 바위, 15% 보)
    return random.choices([0,1,2], weights=[0.7,0.15,0.15])[0]

def rock_biased_heavy(_, __):
    # 바위가 매우 많이 나오는 전략 (15% 가위, 70% 바위, 15% 보)
    return random.choices([0,1,2], weights=[0.15,0.7,0.15])[0]

def paper_biased_heavy(_, __):
    # 보가 매우 많이 나오는 전략 (15% 가위, 15% 바위, 70% 보)
    return random.choices([0,1,2], weights=[0.15,0.15,0.7])[0]

def cycle_strategy(history_self, _):
    # 순서: Scissors(0) -> Rock(1) -> Paper(2) -> Scissors...
    if not history_self:
        return 0
    else:
        return (history_self[-1] + 1) % 3

def copy_opponent_strategy(history_self, history_opponent):
    # 상대방이 이전에 낸 것을 따라하는 전략 (1라운드는 무작위)
    if not history_opponent:
        return random.randint(0,2)
    else:
        return history_opponent[-1]

def minimax_frequency_analyzer(history_self, history_opponent):
    # 상대방의 빈도를 분석해서 가장 많이 나오는 것을 카운터하는 전략
    if len(history_opponent) < 10:  # 충분한 데이터가 없으면 랜덤
        return random.randint(0, 2)
    
    # 최근 50게임의 빈도 분석
    recent_history = history_opponent[-50:]
    counts = [recent_history.count(i) for i in range(3)]
    
    # 가장 많이 나온 것을 카운터
    most_frequent = counts.index(max(counts))
    counter_move = (most_frequent + 1) % 3  # 가위(0)->바위(1), 바위(1)->보(2), 보(2)->가위(0)
    return counter_move

def minimax_pattern_predictor(history_self, history_opponent):
    # 상대방의 패턴을 예측해서 미리 카운터하는 전략
    if len(history_opponent) < 3:
        return random.randint(0, 2)
    
    # 최근 패턴 분석 (3연속 패턴)
    if len(history_opponent) >= 6:
        # 마지막 3개 패턴
        last_pattern = tuple(history_opponent[-3:])
        
        # 과거에서 같은 패턴 이후에 무엇이 나왔는지 찾기
        pattern_predictions = []
        for i in range(len(history_opponent) - 3):
            if tuple(history_opponent[i:i+3]) == last_pattern:
                if i + 3 < len(history_opponent):
                    pattern_predictions.append(history_opponent[i+3])
        
        if pattern_predictions:
            # 가장 자주 나온 다음 수를 예측
            from collections import Counter
            predicted_move = Counter(pattern_predictions).most_common(1)[0][0]
            return (predicted_move + 1) % 3  # 카운터
    
    # 패턴이 없으면 빈도 기반으로 fallback
    return minimax_frequency_analyzer(history_self, history_opponent)

def anti_cycle_strategy(history_self, history_opponent):
    # 순환 패턴을 감지하고 카운터하는 전략
    if len(history_opponent) < 6:
        return random.randint(0, 2)
    
    # 최근 6게임에서 순환 패턴 확인
    recent = history_opponent[-6:]
    
    # 3-cycle 확인: [a,b,c,a,b,c] 패턴
    if recent[:3] == recent[3:]:
        next_in_cycle = recent[0]  # 다음에 올 것 예측
        return (next_in_cycle + 1) % 3  # 카운터
    
    # 2-cycle 확인: [a,b,a,b,a,b] 패턴
    if len(set(recent[::2])) == 1 and len(set(recent[1::2])) == 1:
        if len(history_opponent) % 2 == 0:
            next_in_cycle = recent[0]
        else:
            next_in_cycle = recent[1]
        return (next_in_cycle + 1) % 3
    
    return minimax_frequency_analyzer(history_self, history_opponent)

def rps_result(a, b):
    if a == b:
        return 0
    elif (a == 0 and b == 2) or (a == 1 and b == 0) or (a == 2 and b == 1):
        return 1
    else:
        return -1

def match_matrix(strategyA, strategyB, n_rounds):
    histA, histB = [], []
    results = np.zeros(n_rounds, dtype=int)
    for i in range(n_rounds):
        moveA = strategyA(histA, histB)
        moveB = strategyB(histB, histA)
        histA.append(moveA)
        histB.append(moveB)
        results[i] = rps_result(moveA, moveB)
    return np.mean(results)

strategies = {
    "Random": random_strategy,
    "Scissors-10%": scissors_biased_10,
    "Rock-10%": rock_biased_10,
    "Paper-10%": paper_biased_10,
    "Scissors-Heavy": scissors_biased_heavy,
    "Rock-Heavy": rock_biased_heavy,
    "Paper-Heavy": paper_biased_heavy,
    "Cycle": cycle_strategy,
    "Copy-Opponent": copy_opponent_strategy,
    "Minimax-Frequency": minimax_frequency_analyzer,
    "Minimax-Pattern": minimax_pattern_predictor,
    "Anti-Cycle": anti_cycle_strategy
}

N_rounds = 100000
n = len(strategies)
strategy_names = list(strategies.keys())
matrix = np.zeros((n, n))

for i, nameA in enumerate(strategy_names):
    for j, nameB in enumerate(strategy_names):
        matrix[i, j] = match_matrix(strategies[nameA], strategies[nameB], N_rounds)

# DataFrame으로 보기 좋게
results_df = pd.DataFrame(matrix, index=strategy_names, columns=strategy_names)
print("\nPayoff matrix (row strategy vs column strategy, average per game, A's perspective):\n")
print(results_df.round(3))

# 결과 분석 추가
print("\n" + "="*60)
print("폰 노이만(Von Neumann) 미니맥스 정리 시각화")
print("="*60)

# 1. 순수전략들의 페이오프 매트릭스 (이론값)
print("\n1. 순수전략 페이오프 매트릭스 (Player A 관점):")
print("     가위  바위  보")
print("가위   0   -1   +1")
print("바위  +1    0   -1") 
print("보    -1   +1    0")

# 2. 미니맥스 값 계산
print("\n2. 미니맥스 분석:")
print("각 순수전략의 최악의 경우 (minimax):")
print("- 가위만: min(0, -1, +1) = -1")
print("- 바위만: min(+1, 0, -1) = -1")
print("- 보만:   min(-1, +1, 0) = -1")
print("→ 순수전략의 minimax value = -1")

print("\n혼합전략 (1/3, 1/3, 1/3)의 기댓값:")
print("모든 상대 전략에 대해 기댓값 = 0")
print("→ 혼합전략의 minimax value = 0")

print(f"\n폰 노이만 정리: max(minimax) = min(maximin) = 0")
print("Nash 균형: 양 플레이어 모두 (1/3, 1/3, 1/3)")

# 3. 실제 시뮬레이션 결과와 비교
print("\n3. 시뮬레이션 결과 검증:")
random_vs_all = results_df.loc["Random"]
print(f"Random 전략 vs 모든 전략의 평균: {random_vs_all.mean():.6f}")
print(f"Random 전략 vs 모든 전략의 표준편차: {random_vs_all.std():.6f}")
print(f"이론값 0과의 차이: {abs(random_vs_all.mean()):.6f}")

# 4. 편향된 전략들이 Random에게 지는 이유
print("\n4. 편향 전략의 취약성:")
biased_strategies = ["Scissors-Heavy", "Rock-Heavy", "Paper-Heavy"]
for strategy in biased_strategies:
    if strategy in results_df.index:
        value_vs_random = results_df.loc[strategy, "Random"]
        print(f"{strategy} vs Random: {value_vs_random:.3f}")

print("\n편향된 전략은 예측 가능하므로 카운터 당할 수 있습니다.")
print("Random은 어떤 전략도 이용할 수 없으므로 최적입니다.")

# 히트맵으로 시각화
plt.figure(figsize=(14,12))
plt.imshow(results_df, cmap='RdYlGn', interpolation='nearest')
plt.colorbar(label="Average payoff (row vs col)")
plt.xticks(np.arange(n), strategy_names, rotation=45, ha='right')
plt.yticks(np.arange(n), strategy_names)
plt.title("Von Neumann Minimax Theorem: Rock-Paper-Scissors (100,000 games)")
for i in range(n):
    for j in range(n):
        plt.text(j, i, f"{results_df.iloc[i,j]:+.2f}", ha='center', va='center', color='black', fontsize=7)
plt.xlabel("Column: Opponent strategy")
plt.ylabel("Row: Player strategy")
plt.tight_layout()
plt.show()
