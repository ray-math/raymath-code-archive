def fraction_to_recurring_decimal(numerator, denominator):
    remainder = numerator % denominator
    seen_remainders = {}
    recurring_decimal = ""
    while remainder != 0 and remainder not in seen_remainders:
        seen_remainders[remainder] = len(recurring_decimal)
        remainder *= 10
        quotient = remainder // denominator
        recurring_decimal += str(quotient)
        remainder %= denominator
    if remainder in seen_remainders:
        start = seen_remainders[remainder]
        recurring_decimal = (
            recurring_decimal[:start] + "(" + recurring_decimal[start:] + ")"
        )
    return "0." + recurring_decimal if recurring_decimal else "0"


def find_cyclic_patterns_for_prime(prime):
    patterns = {}
    for k in range(1, prime):
        decimal_representation = fraction_to_recurring_decimal(k, prime)
        recurring_part = (
            decimal_representation.split("(")[1].split(")")[0]
            if "(" in decimal_representation
            else ""
        )
        if recurring_part not in patterns.values():
            patterns[k] = recurring_part
    return patterns


def find_and_print_unique_cyclic_patterns(primes):
    for prime in primes:
        patterns = find_cyclic_patterns_for_prime(prime)

        print(f"Prime: {prime}")
        for k in sorted(patterns.keys()):
            print(f"{k}: {patterns[k]}")

        classes = {}
        unique_patterns = set()
        for k, pattern in patterns.items():
            rotations = {
                "".join(pattern[i:] + pattern[:i]) for i in range(len(pattern))
            }
            key = frozenset(rotations)
            if key not in unique_patterns:
                unique_patterns.add(key)
                classes[key] = {k}
            else:
                classes[key].add(k)

        for key, ks in classes.items():
            class_members = sorted(list(ks))
            representative_pattern = patterns[class_members[0]]
            print(f"\n({', '.join(map(str, class_members))}): {representative_pattern}")
        print("\n")


find_and_print_unique_cyclic_patterns(
    [
        7,
        11,
        13,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        43,
        47,
    ]
)
