import asyncio
import random


async def print_number(number):
    await asyncio.sleep(random.random())
    print(number)

async def main():
    await asyncio.gather(*[print_number(number) for number in range(10)])

if __name__ == '__main__':
    """
    Старый метод get_event_loop будет убран в новых версиях python,
    но в целях обучения можно раскомментировать код снизу.
    """
    #loop = asyncio.get_event_loop()

    #loop.run_until_complete(
    #    asyncio.gather(
    #        *[print_number(number) for number in range(10)]
    #    )
    #)
    #loop.close()

    asyncio.run(main())