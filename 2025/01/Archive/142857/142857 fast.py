import numpy as np


def find_primes(limit):
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[:2] = False
    for n in range(2, int(limit**0.5) + 1):
        if is_prime[n]:
            is_prime[n * n : limit + 1 : n] = False
    return np.nonzero(is_prime)[0]


def to_decimal(numerator, denominator):
    remainders = np.zeros(denominator, dtype=int)
    decimal = ""
    remainder = numerator % denominator
    position = 1

    while remainder and not remainders[remainder]:
        remainders[remainder] = position
        remainder *= 10
        decimal += str(remainder // denominator)
        remainder %= denominator
        position += 1

    if remainders[remainder]:
        start = remainders[remainder]
        decimal = decimal[: start - 1] + "(" + decimal[start - 1 :] + ")"
    return "0." + decimal if decimal else "0"


def find_patterns(prime):
    patterns = {}
    for k in range(1, prime):
        decimal = to_decimal(k, prime)
        part = decimal.split("(")[1][:-1] if "(" in decimal else ""
        if part and part not in patterns.values():
            patterns[k] = part
    return patterns


def to_md(limit, filename):
    primes = find_primes(limit)
    output = ""
    for prime in primes:
        patterns = find_patterns(prime)
        output += f"## Prime: {prime}\n"
        for k in sorted(patterns.keys()):
            output += f"- **{k}**: {patterns[k]}\n"

        classes = {}
        unique = set()
        for k, pattern in patterns.items():
            rotations = {
                "".join(pattern[i:] + pattern[:i]) for i in range(len(pattern))
            }
            key = frozenset(rotations)
            if key not in unique:
                unique.add(key)
                classes[key] = {k}
            else:
                classes[key].add(k)

        for key, ks in classes.items():
            members = sorted(list(ks))
            pattern = patterns[members[0]]
            output += f"\n- **Class ({', '.join(map(str, members))})**: {pattern}\n"
        output += "\n"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(output)


to_md(500, "cyclic_patterns_short.md")
