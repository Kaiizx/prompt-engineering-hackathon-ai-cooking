import csv

# Memoization dictionary
memo = {}

def ackermann(m, n):
    # Check if the result is already memoized
    if (m, n) in memo:
        return memo[(m, n)]

    # Base cases
    if m == 0:
        result = n + 1
    elif m > 0 and n == 0:
        result = ackermann(m - 1, 1)
    else:
        result = ackermann(m - 1, ackermann(m, n - 1))

    # Memoize the result
    memo[(m, n)] = result
    return result

def save_to_csv(file_path, result):
    # Prepare data for CSV
    data = [{'id': 1, 'answer': result}]

    # Write to CSV
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['id', 'answer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Test Ackermann's function for A(3, 8)
m = 3
n = 8
result = ackermann(m, n)

# Save the result to a CSV file
csv_file_path = 'ackermann_result.csv'
save_to_csv(csv_file_path, result)

print(f"A({m}, {n}) = {result} saved to '{csv_file_path}'.")