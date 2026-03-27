import csv
import bisect

def load_primes(filename):
    with open(filename, 'r') as file:
        next(file)  # 첫 번째 줄 건너뛰기
        primes = [int(row[0]) for row in csv.reader(file) if row]
    return primes

def goldbach(n, primes, primes_set):
    pairs = []
    for p in primes[:bisect.bisect(primes, n // 2)]:
        partner = n - p
        if partner in primes_set:
            pairs.append((p, partner))
    return pairs

def main(primes_filename, start, end, output_filename):
    primes = load_primes(primes_filename)
    primes_set = set(primes)

    with open(output_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for even_number in range(start, end + 1, 2):
            pairs = goldbach(even_number, primes, primes_set)
            writer.writerow([even_number] + pairs)

if __name__ == "__main__":
    primes_filename = 'primes.csv'
    output_filename = 'goldbach_pairs.csv'
    start = 4
    end = 10**4
    main(primes_filename, start, end, output_filename)
