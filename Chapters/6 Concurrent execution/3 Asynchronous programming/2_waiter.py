import time
import random
import asyncio

async def waiter(name):
    """Для наглядности стоит раскомментировать разницу между синхронным исполнением и асинхронным."""
    for _ in range(4):
        time_to_sleep = random.randint(1,3) / 4
        #time.sleep(time_to_sleep) # Проверяем поведение корутины с синхронным методом sleep.
        await asyncio.sleep(time_to_sleep) # Проверяем поведение корутины с асинхронным методом asyncio.sleep
        print(f"{name} ждал {time_to_sleep} сек.")

async def main():
    await asyncio.gather(waiter("Первый"), waiter("Второй"))

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(
    #     asyncio.gather(waiter("Первый"), waiter("Второй"))
    # )
    # loop.close()
    asyncio.run(main())