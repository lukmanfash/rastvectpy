"""Main module."""
import random
import string

def generate_random_string(length):
    """Generate a random string with the specified length."""
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
