def is_prime(num):
	if num < 2:
		return False
	for i in range(2, int(num ** 0.5) + 1):
		if num % i == 0:
			return False
	return True

def check_goldbach_conjecture():
	n = 4
	while True:
		found = False
		for i in range(2, n):
			if is_prime(i) and is_prime(n - i):
				found = True
				print(f"{n} = {i} + {n - i}")
				break
		if not found:
			print(f"골드바흐의 추측에 반하는 수 발견: {n}")
			return False
		n += 2

check_goldbach_conjecture()