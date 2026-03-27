import matplotlib.pyplot as plt
import csv
from itertools import islice


def plot_liouville_partial(filename, start, end, step=1):
    L_x_values = []
    x_indices = []

    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)

        for i, row in enumerate(islice(csvreader, start - 2, end - 1, step)):
            actual_row_number = start + i * step
            x_indices.append(actual_row_number)
            L_x_values.append(int(row[0]))

    plt.figure(figsize=(16, 9))
    plt.plot(x_indices, L_x_values, linewidth=1, color="#004D81")
    plt.title(f"L(x) from {start} to {end} (every {step}th data)")
    plt.xlabel("n")
    plt.ylabel("L(x)")
    plt.grid(True)
    plt.show()


filename = (
    "/Users/ray/Library/CloudStorage/OneDrive-개인/개인 교육자료/VSCode/python/유튜브/L(x).csv"
)
plot_liouville_partial(filename, 9 * 10**8, 10**9)
