"""
폰 노이만(Von Neumann) 미니맥스 정리 시각화
가위바위보를 통한 제로섬 게임의 혼합전략 Nash 균형 증명
"""

import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from multiprocessing import Pool, cpu_count
from functools import partial

# matplotlib 기본 설정
plt.rcParams['axes.unicode_minus'] = False

random.seed(42)

class RPSStrategy:
    """가위바위보 전략 클래스"""
    
    @staticmethod
    def random_uniform(history_self, history_opponent):
        """완전 균등 랜덤 전략 (1/3, 1/3, 1/3) - Nash 균형"""
        return random.randint(0, 2)
    
    @staticmethod
    def weak_scissors_bias(history_self, history_opponent):
        """약한 가위 편향 ✌️ (40%, 30%, 30%)"""
        return random.choices([0, 1, 2], weights=[0.4, 0.3, 0.3])[0]
    
    @staticmethod
    def weak_rock_bias(history_self, history_opponent):
        """약한 바위 편향 ✊ (30%, 40%, 30%)"""
        return random.choices([0, 1, 2], weights=[0.3, 0.4, 0.3])[0]
    
    @staticmethod
    def weak_paper_bias(history_self, history_opponent):
        """약한 보 편향 ✋ (30%, 30%, 40%)"""
        return random.choices([0, 1, 2], weights=[0.3, 0.3, 0.4])[0]
    
    @staticmethod
    def strong_scissors_bias(history_self, history_opponent):
        """강한 가위 편향 ✌️ (70%, 15%, 15%)"""
        return random.choices([0, 1, 2], weights=[0.7, 0.15, 0.15])[0]
    
    @staticmethod
    def strong_rock_bias(history_self, history_opponent):
        """강한 바위 편향 ✊ (15%, 70%, 15%)"""
        return random.choices([0, 1, 2], weights=[0.15, 0.7, 0.15])[0]
    
    @staticmethod
    def strong_paper_bias(history_self, history_opponent):
        """강한 보 편향 ✋ (15%, 15%, 70%)"""
        return random.choices([0, 1, 2], weights=[0.15, 0.15, 0.7])[0]
    
    @staticmethod
    def copycat(history_self, history_opponent):
        """카운터 전략: 상대방의 이전 행동을 이기는 것을 냄"""
        if len(history_opponent) == 0:
            return random.randint(0, 2)  # 첫 번째 게임에서는 랜덤
        
        # 상대방의 바로 직전 행동을 이기는 것을 냄
        # 0(가위) -> 1(바위), 1(바위) -> 2(보), 2(보) -> 0(가위)
        return (history_opponent[-1] + 1) % 3
    
    @staticmethod
    def anti_bias_adaptive(history_self, history_opponent):
        """적응형 전략: 상대방 편향을 카운터"""
        if len(history_opponent) < 20:
            return random.randint(0, 2)
        
        # 최근 20게임 분석
        recent = history_opponent[-20:]
        counts = [recent.count(i) for i in range(3)]
        most_frequent = counts.index(max(counts))
        
        # 가장 많이 나온 것을 카운터
        return (most_frequent + 1) % 3

def rps_payoff(move_a, move_b):
    """가위바위보 페이오프 함수 (A의 관점)"""
    if move_a == move_b:
        return 0  # 무승부
    elif (move_a == 0 and move_b == 2) or (move_a == 1 and move_b == 0) or (move_a == 2 and move_b == 1):
        return 1  # A 승리
    else:
        return -1  # A 패배

def simulate_single_match(args):
    """멀티프로세싱을 위한 단일 매치 시뮬레이션"""
    strategy_a, strategy_b, rounds = args
    history_a, history_b = [], []
    total_payoff = 0
    
    for _ in range(rounds):
        move_a = strategy_a(history_a, history_b)
        move_b = strategy_b(history_b, history_a)
        
        payoff = rps_payoff(move_a, move_b)
        total_payoff += payoff
        
        history_a.append(move_a)
        history_b.append(move_b)
    
    return total_payoff / rounds

def simulate_all_combinations(strategies_list, rounds=10000, iterations=10):
    """모든 전략 조합에 대해 한꺼번에 병렬 시뮬레이션"""
    strategy_names = list(strategies_list.keys())
    n = len(strategy_names)
    
    # 모든 전략 조합과 반복에 대한 작업 리스트 생성
    all_tasks = []
    task_mapping = {}  # (i, j) -> task 인덱스 범위 매핑
    
    task_index = 0
    for i, name_a in enumerate(strategy_names):
        for j, name_b in enumerate(strategy_names):
            start_idx = task_index
            for _ in range(iterations):
                all_tasks.append((strategies_list[name_a], strategies_list[name_b], rounds))
                task_index += 1
            end_idx = task_index
            task_mapping[(i, j)] = (start_idx, end_idx)
    
    print(f"총 {len(all_tasks)}개의 시뮬레이션 작업을 병렬로 실행합니다...")
    
    # CPU 코어 수 결정
    num_cores = max(1, int(cpu_count() * 0.8))
    
    # 모든 작업을 한꺼번에 병렬 실행
    with Pool(num_cores) as pool:
        all_results = pool.map(simulate_single_match, all_tasks)
    
    # 결과를 매트릭스 형태로 정리
    mean_matrix = np.zeros((n, n))
    std_matrix = np.zeros((n, n))
    
    for (i, j), (start_idx, end_idx) in task_mapping.items():
        payoffs = all_results[start_idx:end_idx]
        mean_matrix[i, j] = np.mean(payoffs)
        std_matrix[i, j] = np.std(payoffs)
    
    return mean_matrix, std_matrix, strategy_names


def create_payoff_matrix():
    """페이오프 매트릭스 생성 (한꺼번에 병렬처리)"""
    strategies = {
        # 무작위 (Nash 균형)
        "Random": RPSStrategy.random_uniform,
        
        # 약한 편향 전략들
        "Scissors-40%": RPSStrategy.weak_scissors_bias,
        "Rock-40%": RPSStrategy.weak_rock_bias,
        "Paper-40%": RPSStrategy.weak_paper_bias,
        
        # 강한 편향 전략들
        "Scissors-70%": RPSStrategy.strong_scissors_bias,
        "Rock-70%": RPSStrategy.strong_rock_bias,
        "Paper-70%": RPSStrategy.strong_paper_bias,
        
        # 카운터 전략
        "Counter": RPSStrategy.copycat,
        
        # 적응형 전략
        "Adaptive": RPSStrategy.anti_bias_adaptive
    }
    
    print("멀티코어 시뮬레이션 진행 중...")
    print(f"사용 중인 CPU 코어: {max(1, int(cpu_count() * 0.8))}개")
    
    # 모든 조합을 한꺼번에 병렬처리
    mean_matrix, std_matrix, strategy_names = simulate_all_combinations(strategies)
    
    mean_df = pd.DataFrame(mean_matrix, index=strategy_names, columns=strategy_names)
    std_df = pd.DataFrame(std_matrix, index=strategy_names, columns=strategy_names)
    
    return mean_df, std_df

def analyze_minimax_theorem(df_mean, df_std):
    """폰 노이만 미니맥스 정리 분석"""
    print("\n" + "="*70)
    print("폰 노이만(Von Neumann) 미니맥스 정리: 혼합전략 분석")
    print("="*70)
    
    # 1. Nash 균형 전략의 성능
    print("\n1. Nash 균형 전략 (1/3, 1/3, 1/3) 분석:")
    if "Random" in df_mean.index:
        nash_row_mean = df_mean.loc["Random"]
        nash_row_std = df_std.loc["Random"]
        print(f"Random vs 모든 전략의 평균: {nash_row_mean.mean():.6f}")
        print(f"Random vs 모든 전략의 표준편차: {nash_row_mean.std():.6f}")
        print(f"Random vs 모든 전략의 최솟값: {nash_row_mean.min():.6f}")
        print(f"Random vs 모든 전략의 최댓값: {nash_row_mean.max():.6f}")
        print("→ Nash 균형의 minimax value ≈ 0.000")
    
    # 2. 약한 편향 전략들의 취약성
    print(f"\n2. 약한 편향 전략들의 minimax 값:")
    weak_strategies = ["Scissors-40%", "Rock-40%", "Paper-40%"]
    for strategy in weak_strategies:
        if strategy in df_mean.index:
            row_mean = df_mean.loc[strategy]
            row_std = df_std.loc[strategy]
            min_value = row_mean.min()
            max_value = row_mean.max()
            std_value = row_mean.std()
            print(f"{strategy}: min = {min_value:.3f}, max = {max_value:.3f}, std = {std_value:.3f}")
    
    # 3. 강한 편향 전략들의 취약성
    print(f"\n3. 강한 편향 전략들의 minimax 값:")
    strong_strategies = ["Scissors-70%", "Rock-70%", "Paper-70%"]
    for strategy in strong_strategies:
        if strategy in df_mean.index:
            row_mean = df_mean.loc[strategy]
            row_std = df_std.loc[strategy]
            min_value = row_mean.min()
            max_value = row_mean.max()
            std_value = row_mean.std()
            print(f"{strategy}: min = {min_value:.3f}, max = {max_value:.3f}, std = {std_value:.3f}")
    # 4. 카운터 전략의 성능
    print(f"\n4. 카운터 전략의 성능:")
    if "Counter" in df_mean.index:
        counter_row_mean = df_mean.loc["Counter"]
        counter_row_std = df_std.loc["Counter"]
        print(f"Counter vs 모든 전략의 평균: {counter_row_mean.mean():.3f}")
        print(f"Counter vs 모든 전략의 표준편차: {counter_row_mean.std():.3f}")
        print(f"Counter vs 모든 전략의 최솟값: {counter_row_mean.min():.3f}")
        print(f"Counter vs 모든 전략의 최댓값: {counter_row_mean.max():.3f}")
        print("→ 상대방의 직전 행동을 카운터하는 전략")
        
    # 5. 적응형 전략의 효과
    print(f"\n5. 적응형 전략의 성능:")
    if "Adaptive" in df_mean.index:
        adaptive_row_mean = df_mean.loc["Adaptive"]
        adaptive_row_std = df_std.loc["Adaptive"]
        print(f"Adaptive vs 모든 전략의 평균: {adaptive_row_mean.mean():.3f}")
        print(f"Adaptive vs 모든 전략의 표준편차: {adaptive_row_mean.std():.3f}")
        
        # 강한 편향 전략들에 대한 성과
        print("\n강한 편향 전략들에 대한 적응형 전략의 성과:")
        for strategy in strong_strategies:
            if strategy in df_mean.columns:
                value_mean = df_mean.loc["Adaptive", strategy]
                value_std = df_std.loc["Adaptive", strategy]
                print(f"Adaptive vs {strategy}: {value_mean:.3f} ± {value_std:.3f}")
    
    return nash_row_mean if "Random" in df_mean.index else None

def visualize_results(df_mean, df_std):
    """결과 시각화 - 색상 민감도와 텍스트 크기 개선"""
    plt.figure(figsize=(16, 14))
    
    # 더 민감한 색상 범위 설정 (±0.4로 줄여서 작은 차이도 잘 보이게)
    vmin, vmax = -0.4, 0.4
    im = plt.imshow(df_mean.values, cmap='RdYlGn', vmin=vmin, vmax=vmax, interpolation='nearest')
    
    # 축 설정 - 더 큰 폰트 사이즈
    plt.xticks(range(len(df_mean.columns)), df_mean.columns, rotation=45, ha='right', fontsize=14, fontweight='bold')
    plt.yticks(range(len(df_mean.index)), df_mean.index, fontsize=14, fontweight='bold')
    
    # 값 표시 (평균값과 표준편차) - 더 큰 폰트
    for i in range(len(df_mean.index)):
        for j in range(len(df_mean.columns)):
            mean_val = df_mean.iloc[i,j]
            std_val = df_std.iloc[i,j]
            
            # 배경 색상에 따른 텍스트 색상 결정 (더 정교하게)
            normalized_val = (mean_val - vmin) / (vmax - vmin)
            text_color = 'white' if normalized_val < 0.3 or normalized_val > 0.7 else 'black'
            
            # 평균값 (위쪽) - 더 큰 폰트
            plt.text(j, i-0.15, f'{mean_val:+.3f}', 
                    ha='center', va='center', 
                    color=text_color,
                    fontsize=12, fontweight='bold')
            
            # 표준편차 (아래쪽, 회색) - 더 큰 폰트
            plt.text(j, i+0.2, f'±{std_val:.3f}', 
                    ha='center', va='center', 
                    color='darkgray',
                    fontsize=10, fontweight='bold')
    
    # 전략명 맵핑 (텍스트만 사용)
    strategy_map = {
        'Random': 'Random',
        'Scissors-40%': 'Scissors-40%',
        'Rock-40%': 'Rock-40%', 
        'Paper-40%': 'Paper-40%',
        'Scissors-70%': 'Scissors-70%',
        'Rock-70%': 'Rock-70%',
        'Paper-70%': 'Paper-70%',
        'Counter': 'Counter',
        'Adaptive': 'Adaptive'
    }
    
    # x축 라벨 업데이트
    x_labels = [strategy_map.get(name, name) for name in df_mean.columns]
    y_labels = [strategy_map.get(name, name) for name in df_mean.index]
    
    plt.xticks(range(len(df_mean.columns)), x_labels, rotation=45, ha='right', fontsize=10)
    plt.yticks(range(len(df_mean.index)), y_labels, fontsize=10)
    
    # 제목과 라벨 - 더 큰 폰트
    plt.title('Von Neumann Minimax Theorem\nMixed Strategy Competition in Rock-Paper-Scissors', 
              fontsize=18, fontweight='bold', pad=25)
    plt.xlabel('Opponent Strategy (Column Player)', fontsize=14, fontweight='bold')
    plt.ylabel('Player Strategy (Row Player)', fontsize=14, fontweight='bold')
    
    # 컬러바 - 더 큰 폰트
    cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
    cbar.set_label('Average Payoff', rotation=270, labelpad=25, fontsize=14, fontweight='bold')
    cbar.ax.tick_params(labelsize=12)
    
    # 격자 제거
    plt.grid(False)
    
    plt.tight_layout()
    plt.show()


def main():
    """메인 실행 함수"""
    print("폰 노이만 미니맥스 정리 시뮬레이션 시작")
    print("="*50)
    
    # 페이오프 매트릭스 생성
    payoff_mean_df, payoff_std_df = create_payoff_matrix()
    
    # 결과 출력
    print(f"\n페이오프 매트릭스 (행 플레이어 관점):")
    print("평균 페이오프:")
    print(payoff_mean_df.round(3))
    print("\n표준편차:")
    print(payoff_std_df.round(3))
    
    # 미니맥스 정리 분석
    analyze_minimax_theorem(payoff_mean_df, payoff_std_df)
    
    # 시각화
    visualize_results(payoff_mean_df, payoff_std_df)
    
    return payoff_mean_df, payoff_std_df

if __name__ == "__main__":
    results = main()
