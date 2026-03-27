def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def reverse_number(n):
    return int(str(n)[::-1])


def find_emirps(limit):
    emirps = []
    for i in range(13, limit + 1):  # Starting from 13 as it's the first emirp
        if is_prime(i):
            reversed_i = reverse_number(i)
            if i != reversed_i and is_prime(reversed_i):
                emirps.append(i)
    return emirps


# Set a limit to search for emirps up to that number
limit = 10**6
emirps_up_to_limit = find_emirps(limit)
print(emirps_up_to_limit)
