import time
import threading
import multiprocessing


def heavy_calculation(n):
    total = 0
    for i in range(n):
        total += i * i
    return total

WORK = 15_000_000
# SEQUENTIAL

def sequential():
    print("\n--- SEQUENTIAL CPU ---")
    start = time.perf_counter()
    for _ in range(4):
        heavy_calculation(WORK)
    end = time.perf_counter()

    print(f"Sequential: {end - start:.2f} sec")

# THREADING
def threading_version():
    print("\n--- THREADING CPU ---")
    start = time.perf_counter()
    threads = []
    for _ in range(4):
        thread = threading.Thread(
            target=heavy_calculation,
            args=(WORK,)
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    end = time.perf_counter()
    print(f"Threading: {end - start:.2f} sec")

# MULTIPROCESSING
def multiprocessing_version():
    print("\n--- MULTIPROCESSING CPU ---")
    start = time.perf_counter()
    processes = []
    for _ in range(4):
        process = multiprocessing.Process(
            target=heavy_calculation,
            args=(WORK,)
        )
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    end = time.perf_counter()
    print(f"Multiprocessing: {end - start:.2f} sec")

# MAIN
if __name__ == "__main__":
    sequential()
    threading_version()
    multiprocessing_version()