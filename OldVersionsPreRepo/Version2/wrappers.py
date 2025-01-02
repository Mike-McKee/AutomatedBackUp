import time

def timing_wrapper(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Execute the function
        end_time = time.time()  # Record the end time
        execution_time = end_time - start_time  # Calculate the execution time
        print(f"{func.__name__} executed in {execution_time:.6f} seconds.")
        return result
    return wrapper

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