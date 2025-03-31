def filter_positive_numbers(numbers):
    result = []
    for num in numbers:
        if num > 0:
            result.append(num)
        else:
            result.append(num)
    return result

# Test case
test_list = [-2, 3, -1, 0, 4, -5]
print(filter_positive_numbers(test_list))  # Expected: [3, 4], Actual: [-2, 3, -1, 0, 4, -5]
