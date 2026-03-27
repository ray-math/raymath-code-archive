def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def find_primes():
    num = 2
    while True:
        if is_prime(num):
            print(num)
        num += 1

# 프로그램 실행
find_primes()