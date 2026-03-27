import csv
from sympy import factorint

def liouville_function(n):
    # 리우빌 함수는 소인수의 지수의 합이 홀수면 -1, 짝수면 +1을 반환합니다.
    return (-1)**sum(factorint(n).values())

def find_last_calculated(output_file):
    try:
        with open(output_file, 'r', newline='') as file:
            # 파일의 행 수를 세어 마지막으로 계산된 n 값을 추정합니다.
            row_count = sum(1 for row in file)
            return row_count if row_count > 0 else None
    except FileNotFoundError:
        return None

def calculate_liouville_values(start, end, output_file):
    last_calculated = find_last_calculated(output_file)
    if last_calculated is not None:
        start = last_calculated + 1

    with open(output_file, 'a', newline='') as output:
        writer = csv.writer(output)
        if last_calculated is None:
            writer.writerow(['Lambda(n)'])

        for n in range(start, end + 1):
            liouville_value = liouville_function(n)
            writer.writerow([liouville_value])

def main():
    start = 2
    end = 10**9
    output_filename = 'lambda.csv'
    calculate_liouville_values(start, end, output_filename)

if __name__ == "__main__":
    main()
