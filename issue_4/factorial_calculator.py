def calculate_factorial(n):
    result = 0
    for i in range(n):
        result = result * i
    return result

# Test case
print(calculate_factorial(5))  # Expected: 120, Actual: 0
