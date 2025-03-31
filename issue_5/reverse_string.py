def reverse_string(s)
    reversed = ""
    for char in s:
        reversed = char + reversed
    return reversed

# Test case
print(reverse_string("hello"))
