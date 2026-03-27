import os

def count_rows_in_csv(file_path):
    count = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        for _ in file:
            count += 1
    return count

def count_rows_in_multiple_csv(file_list):
    row_counts = {}
    for file_path in file_list:
        row_counts[file_path] = count_rows_in_csv(file_path)
    return row_counts

file_list = ['lambda.csv', 'L(x).csv']

# 여러 파일의 행 수를 계산합니다.
row_counts = count_rows_in_multiple_csv(file_list)

# 결과 출력
for file_path, count in row_counts.items():
    print(f"{file_path}: {count}")
