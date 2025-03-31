def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers) - 1):  # Possible off-by-one error
        total += numbers[i]
    return total

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    print("Sum:", calculate_sum(numbers))
