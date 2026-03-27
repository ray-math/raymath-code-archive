import pandas as pd
import math
from collections import Counter

def find_pairs(n):
    pairs = {i: [] for i in range(1, n + 1)}
    for i in range(1, int(math.sqrt(2*n)) + 1):
        square = i * i
        for num in range(1, n+1):
            for j in range(1, num):
                if j + (square-j) == square and square-j > j and square-j <= num:
                    pairs[num].append((j, square-j))
    return pairs

n = 1000
pairs = find_pairs(n)

# convert the pairs to a DataFrame
df = pd.DataFrame(dict([ (k, pd.Series(v)) for k, v in pairs.items() ]))

# replace empty lists with None for cleaner output
df = df.applymap(lambda x: None if isinstance(x, list) and not x else x)

# Prepend a row with 1-n at the top
df = pd.concat([pd.DataFrame([list(range(1, n + 1))]), df]).reset_index(drop=True)

# Calculate the minimum occurrence for each column
min_occurrence = df.iloc[1:].apply(lambda x: min(Counter([i for sublist in x.dropna().values for i in sublist]).values()) if not x.dropna().empty else None)

# Add the min_occurrence row to the DataFrame at the second row
df.loc[-1] = min_occurrence
df.index = df.index + 1  # shifting index
df.sort_index(inplace=True)

# Count the number of valid pairs for each column (ignore None values)
pair_counts = df.iloc[2:].count()

# Add the pair_counts row to the DataFrame at the third row
df.loc[-2] = pair_counts
df.index = df.index + 1  # shifting index
df.sort_index(inplace=True) 

# Remove the third row
df = df.drop(df.index[2])

# write the DataFrame to CSV
df.to_csv('output.csv', index=False)
