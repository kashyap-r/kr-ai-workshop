import asyncio 
import time 

async def make_coffee():
    print("Start making coffee...")
    await asyncio.sleep(6)
    print("Coffee is ready!")

async def make_toast():
    print("Start making toast...")
    await asyncio.sleep(4)
    print("Toast is ready!")

async def boil_eggs():
    print("Start boiling eggs...")
    await asyncio.sleep(8)
    print("Eggs are ready!")

async def main():
    start_time = time.time()
    
    # Run tasks concurrently
    await asyncio.gather(
        make_coffee(),
        make_toast(),
        boil_eggs()
    )
    
    end_time = time.time()
    print(f"All tasks completed in {end_time - start_time:.2f} seconds.")   

async def sync_tasks():
    start_time = time.time()
    
    # Run tasks sequentially
    await make_coffee()
    await make_toast()
    await boil_eggs()
    
    end_time = time.time()
    print(f"All tasks completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())

    print ("All async tasks completed!")
    print ("Now let us try sync")
    asyncio.run(sync_tasks())
    


