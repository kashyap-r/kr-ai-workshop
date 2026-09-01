import asyncio 
import time 

async def call_api(name, delay):
    print(f" {name} : Sending request to API...")
    await asyncio.sleep(delay)
    print(f" {name} : Received response from API!")
    return f"{name} : Response data"

async def countdown():
    for i in range(5, 0, -1):
        print(f"Countdown: {i}")
        await asyncio.sleep(1)
    print("Countdown complete!")

async def main():
    start = time.perf_counter()

    result = await asyncio.gather(
        call_api("OpenAI API 1", 3),
        call_api("Database", 5),        
        call_api("Weather API", 4),
        countdown()
    )
    end = time.perf_counter()
    print(f"All API calls completed in {end - start:.2f} seconds.")
    print("Results:")
    for res in result:
        print(res)  

if __name__ == "__main__":
    asyncio.run(main())
    