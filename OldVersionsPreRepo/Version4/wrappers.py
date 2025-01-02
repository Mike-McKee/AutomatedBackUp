import time
from colorama import Fore, Style, init

def timing_wrapper(Message=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()  # Record the start time
            result = func(*args, **kwargs)  # Execute the function
            end_time = time.time()  # Record the end time
            execution_time = end_time - start_time  # Calculate the execution time
            if Message:
                print(f"{Fore.MAGENTA}{Message} executed in {execution_time:.6f} seconds.")
            else:
                print(f"{Fore.MAGENTA}{func.__name__} executed in {execution_time:.6f} seconds.")
            return result
        return wrapper
    return decorator

"""
# Example usage with a sample function
@timing_wrapper
def sample_function(n):
    # Simulate a function that takes some time to execute
    total = 0
    for i in range(n):
        total += i
    return total

# Test the wrapper
print(sample_function(1000000))
"""