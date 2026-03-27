import csv

def calculate_cumulative_sum(input_file, output_file):
    cumulative_sum = 0
    
    with open(input_file, 'r') as input_csv, open(output_file, 'w', newline='') as output_csv:
        reader = csv.reader(input_csv)
        writer = csv.writer(output_csv)
        
        header = next(reader)
        writer.writerow(['L(x)'])
        
        for row in reader:
            liouville_value = int(row[0])
            cumulative_sum += liouville_value
            writer.writerow([cumulative_sum])

def main():
    input_filename = 'lambda.csv'
    output_filename = 'L(x).csv'
    calculate_cumulative_sum(input_filename, output_filename)

if __name__ == "__main__":
    main()
