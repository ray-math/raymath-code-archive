import csv
import gmpy2

def generate_primes_gmpy2(n, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Prime'])

        prime = gmpy2.mpz(2)  # mpz는 gmpy2의 고정밀도 정수 타입
        while prime <= n:
            writer.writerow([int(prime)])
            prime = gmpy2.next_prime(prime)

n = 10**5
filename = 'primes_up_to_1_billion.csv'
generate_primes_gmpy2(n, filename)
