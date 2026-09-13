import time
import threading 
import asyncio 

FILES = [
    "file1.pdf",
    "file2.pdf",
    "file3.pdf",
    "file4.pdf",
    "file5.pdf",
]

## 1. Sequential Version 
def download_sequential(file_name):
    print (f"Starting {file_name}")
    # simulate waiting for network
    time.sleep(2)
    print (f"Finished {file_name}")

def run_sequential():
    print (f"\n ---- SEQUNTIAL ----")
    start = time.perf_counter()
    for file in FILES:
        download_sequential(file)
    end = time.perf_counter()
    print(f"\n Sequential time: {end - start:.2f} seconds")

## 2. Multi-threading Version
def download_thread(file_name):
    print(f"Starting {file_name}")
    time.sleep(2)
    print(f"Finished {file_name}")

def run_threading():
    print (f"\n--- Multithreading ---")
    start = time.perf_counter()
    threads = []
    for file in FILES:
        thread = threading.Thread(
            target=download_thread,
            args=(file,)
        )
        thread.start()
        threads.append(thread)

    # wait for all the threads
    for thread in threads:
        thread.join()

    end = time.perf_counter()
    print(f"\n Threading time: {end - start:.2f} seconds")

## Asyncio version 
async def download_async(file_name):
    print (f"Starting {file_name}")
    # Below statement says: "I'm waiting. Go work on something else."
    await asyncio.sleep(2)

    # change the await statement to below.. and run 
    # time.sleep(2) 
    # then this behaves like a sequential one ... just the mechanism is different. 
    
    print (f"Finished {file_name}")

async def run_asyncio():
    print (f"\n --- Asyncio ---")
    start = time.perf_counter()
    await asyncio.gather(
        *(download_async(file) for file in FILES)
    )

    end = time.perf_counter()
    print (f"\n Asyncio time: {end-start:.2f}seconds")

## main
if __name__ == "__main__":
    run_sequential()

    run_threading()

    asyncio.run(run_asyncio())
    