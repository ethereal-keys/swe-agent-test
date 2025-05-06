def is_palindrome(text):
    """
    Check if the given text is a palindrome.
    A palindrome reads the same forward and backward.
    
    Args:
        text (str): The text to check
        
    Returns:
        bool: True if the text is a palindrome, False otherwise
    """
    # Convert text to lowercase
    text = text.lower()
    
    # Remove spaces
    text = text.replace(" ", "")
    
    # Check if the text is equal to its reverse
    return text == text[::-1]

def main():
    """Example usage of the is_palindrome function"""
    test_cases = [
        "racecar",
        "level",
        "hello",
        "A man, a plan, a canal: Panama",
        "Was it a car or a cat I saw?"
    ]
    
    for test in test_cases:
        result = is_palindrome(test)
        print(f"'{test}' is{' ' if result else ' not '}a palindrome")

if __name__ == "__main__":
    main()
