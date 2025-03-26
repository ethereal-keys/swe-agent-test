def calculate_average(numbers)
    if not numbers:
        return None
    
    total = sum(numbers)
    return total / len(numbers)

# Example usage
sample_data = [10, 20, 30, 40, 50]
result = calculate_average(sample_data)
print(f"The average is: {result}")
