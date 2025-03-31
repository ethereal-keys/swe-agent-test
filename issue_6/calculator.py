from math_ops import add_numbers, multiply_numbers

def compute_result(x, y):
    sum_result = add_numbers(x, y)
    product_result = multiply_numbers(x, y)
    return sum_result, product_result

# Test case
x, y = 3, 4
sum_val, prod_val = compute_result(x, y)
print(f"Sum: {sum_val}, Product: {prod_val}")
