import csv
from itertools import islice

def find_max_min_in_range(filename, start, end):
    max_value = float('-inf')
    min_value = float('inf')
    max_rows = []
    min_rows = []
    zero_rows = []
    one_rows = []

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)

        for i, row in enumerate(islice(csvreader, start - 2, end - 1), start - 1):
            value = int(row[0])
            if value > max_value:
                max_value = value
                max_rows = [i + 1]
            elif value == max_value:
                max_rows.append(i + 1)

            if value < min_value:
                min_value = value
                min_rows = [i + 1] 
            elif value == min_value:
                min_rows.append(i + 1)

            if value == 0:
                zero_rows.append(i)
            elif value == 1:
                one_rows.append(i)

    return max_rows, max_value, min_rows, min_value, zero_rows, one_rows

filename = '/Users/ray/Library/CloudStorage/OneDrive-개인/개인 교육자료/VSCode/python/유튜브/L(x).csv'
start_range = 9*10**8
end_range = 10**9

max_rows, max_value, min_rows, min_value, zero_rows, one_rows = find_max_min_in_range(filename, start_range, end_range)

print(f"Max value: {max_value} at rows {max_rows}")
print(f"Min value: {min_value} at rows {min_rows}")
print(f"Rows with value 0: {zero_rows}")
print(f"Rows with value 1: {one_rows}")
