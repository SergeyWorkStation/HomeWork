import asyncio

counter = 0
lock = asyncio.Lock()


async def plus_1():
    global counter
    for _ in range(10000):
        async with lock:
            counter += 1

async def multiply_by_2():
    global counter
    for _ in range(10):
        async with lock:
            counter *= 2

async def main():
    tasks = [plus_1() for _ in range(3)] + [multiply_by_2() for _ in range(3)]
    await asyncio.gather(*tasks)


asyncio.run(main())

print(f"Final counter value: {counter}")