import matplotlib.pyplot as plt
import csv

def plot_liouville_graph(filename, n):
    L_x_values = []

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for i, row in enumerate(csvreader, start=2):
            if i > n:
                break
            L_x_values.append(int(row[0]))

    plt.figure(figsize=(16, 9))
    plt.plot(range(2, n+1), L_x_values, linewidth=1, color='#004D81')
    plt.title('Graph of L(x) up to n={}'.format(n))
    plt.xlabel('n')
    plt.ylabel('L(x)')
    plt.grid(True)
    plt.show()

filename = '/Users/ray/Library/CloudStorage/OneDrive-개인/개인 교육자료/VSCode/python/유튜브/L(x).csv'
plot_liouville_graph(filename, n=10**5)