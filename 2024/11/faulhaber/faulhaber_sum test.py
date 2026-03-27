import time
from mpmath import bernoulli, binomial, mp

# mpmath로 정밀도를 높여 연산하기
mp.dps = 100  # 소수점 이하 100자리까지 계산


# 직접 합산 방식
def direct_sum(n, m):
    return sum(k**m for k in range(1, n + 1))


# 파울하버 공식 방식 (mpmath 사용, 결과를 정수형으로 변환)
def faulhaber_sum(n, m):
    result = mp.mpf(0)
    for i in range(m + 1):
        result += (-1) ** i * binomial(m + 1, i) * bernoulli(i) * n ** (m + 1 - i)
    # 최종 결과를 정수형으로 변환
    return int(result / (m + 1))


# 예시
n = 10**6
m = 10

# 직접 합산 방식 시간 측정
start_time = time.time()
direct_result = direct_sum(n, m)
direct_time = time.time() - start_time

# 파울하버 공식 방식 시간 측정
start_time = time.time()
faulhaber_result = faulhaber_sum(n, m)
faulhaber_time = time.time() - start_time

# 결과 출력
print(f"직접합산 공식 결과: {direct_result}, 시간: {direct_time:.6f}초")
print(f"파울하버 공식 결과: {faulhaber_result}, 시간: {faulhaber_time:.6f}초")
