import numpy as np

def is_valid_magic_square(magic_square):
    n = len(magic_square)
    magic_sum = np.sum(magic_square, axis=0)[0]

    # Check the sum of each row, column, and the two diagonals
    return (
        all(np.sum(magic_square, axis=0) == magic_sum) and
        all(np.sum(magic_square, axis=1) == magic_sum) and
        np.sum(np.diag(magic_square)) == magic_sum and
        np.sum(np.diag(np.fliplr(magic_square))) == magic_sum
    )

# Provided magic square
magic_square = np.array([
    [256, 676, 1, 529, 1444, 2704, 1849, 3721],
    [1681, 3969, 1600, 2500, 9, 441, 196, 784],
    [1296, 2916, 2025, 3481, 100, 1024, 49, 289],
    [25, 361, 144, 900, 2209, 3249, 1156, 3136],
    [729, 169, 484, 16, 2401, 1521, 4096, 1764],
    [3844, 1936, 2601, 1369, 576, 4, 625, 225],
    [3025, 1089, 3364, 2304, 841, 121, 400, 36],
    [324, 64, 961, 81, 3600, 2116, 2809, 1225]
])

print(is_valid_magic_square(magic_square))
