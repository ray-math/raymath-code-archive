import numpy as np
from multiprocessing import Pool

# 홀수 차수의 마방진 생성
def generate_odd_magic_square(n):
    magic_square = np.zeros((n,n), dtype=int)
    num = 1
    i, j = 0, n//2

    while num <= n*n:
        magic_square[i, j] = num
        num += 1
        newi, newj = (i-1) % n, (j+1) % n
        if magic_square[newi, newj]:
            i += 1
        else:
            i, j = newi, newj

    return magic_square

# 4n차수의 마방진 생성
def generate_doubly_even_magic_square(n):
    arr = [[(n*y)+x+1 for x in range(n)]for y in range(n)] 
    for i in range(0,n//4): 
        for j in range(0,n//4): 
            arr[i][j] = (n*n + 1) - arr[i][j]; 
    for i in range(0,n//4): 
        for j in range(3 * (n//4),n): 
            arr[i][j] = (n*n + 1) - arr[i][j]; 
    for i in range(3 * (n//4),n): 
        for j in range(0,n//4): 
            arr[i][j] = (n*n + 1) - arr[i][j]; 
    for i in range(3 * (n//4),n): 
        for j in range(3 * (n//4),n): 
            arr[i][j] = (n*n + 1) - arr[i][j]; 
    for i in range(n//4,3 * (n//4)): 
        for j in range(n//4,3 * (n//4)): 
            arr[i][j] = (n*n + 1) - arr[i][j]; 
    return np.array(arr)

# 4n+2차수의 마방진 생성
def generate_singly_even_magic_square(s):
    if s % 2 == 1:
        s += 1
    while s % 4 == 0:
        s += 2
    q = [[0 for j in range(s)] for i in range(s)]
    z = s // 2
    b = z * z
    c = 2 * b
    d = 3 * b
    o = generate_odd_magic_square(z)
    for j in range(0, z):
        for i in range(0, z):
            a = o[i][j]
            q[i][j] = a
            q[i + z][j + z] = a + b
            q[i + z][j] = a + c
            q[i][j + z] = a + d
    lc = z // 2
    rc = lc
    for j in range(0, z):
        for i in range(0, s):
            if i < lc or i > s - rc or (i == lc and j == lc):
                if not (i == 0 and j == lc):
                    t = q[i][j]
                    q[i][j] = q[i][j + z]
                    q[i][j + z] = t
    return np.array(q)

def generate_magic_square(n):
    if n % 2 == 1:
        return generate_odd_magic_square(n)
    elif n % 4 == 0:
        return generate_doubly_even_magic_square(n)
    else:
        return generate_singly_even_magic_square(n)

def is_valid_magic_square(magic_square):
    n = len(magic_square)
    magic_sum = np.sum(magic_square, axis=0)[0]
    return (
        all(np.sum(magic_square, axis=0) == magic_sum) and
        all(np.sum(magic_square, axis=1) == magic_sum) and
        np.sum(np.diag(magic_square)) == magic_sum and
        np.sum(np.diag(np.fliplr(magic_square))) == magic_sum
    )

def worker(n):
    magic_square = generate_magic_square(n)
    result_str = f'Magic Square of order {n}x{n}:\n'
    result_str += str(magic_square) + '\n'
    result_str += f'Magic sum: {np.sum(magic_square, axis=0)[0]}\n'
    result_str += f'Is valid magic square: {is_valid_magic_square(magic_square)}\n'
    return result_str

if __name__ == "__main__":
    orders = list(range(3, 30))
    with Pool() as pool:
        results = pool.map(worker, orders)
    for result in results:
        print(result)
