from tqdm import tqdm
import time

for i in tqdm(range(1, 1001), desc="Processing", unit="item"):
    time.sleep(0.01)  # Simulating a task


# import time

# def print_progress_bar(iteration, total, length=40):
#     percent = ("{0:.2f}").format(100 * (iteration / float(total)))
#     filled_length = int(length * iteration // total)
#     bar = '#' * filled_length + '-' * (length - filled_length)
#     print(f'\rProgress: [{bar}] {percent}% Complete', end='\r')
#     if iteration == total:
#         print()

# total_items = 1000

# for i in range(1, total_items + 1):
#     print_progress_bar(i, total_items)
#     time.sleep(0.3)  # Simulating a task
