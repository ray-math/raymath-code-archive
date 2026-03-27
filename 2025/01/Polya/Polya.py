import csv
from sympy import factorint

def liouville_function(n):
    # 리우빌 함수는 소인수의 지수의 합이 홀수면 -1, 짝수면 +1을 반환합니다.
    return (-1)**sum(factorint(n).values())

def polyas_conjecture(n, filename):
    L_x = 0  # L(x) 초기화

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['L(x)'])

        for i in range(2, n + 1):
            L_x += liouville_function(i)
            writer.writerow([L_x])

n = 10**2
filename = 'polyas_conjecture.csv'
polyas_conjecture(n, filename)
