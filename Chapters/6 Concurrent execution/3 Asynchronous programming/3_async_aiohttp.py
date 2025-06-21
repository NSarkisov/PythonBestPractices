import asyncio
import aiohttp
import time

from async_rates import get_rates


SYMBOLS = ('USD', 'PLN', 'EUR', 'CZK', 'NOK')
BASES = ('USD', 'PLN', 'EUR', 'CZK', 'NOK')

def present_result(base, rates):

    rates_line = ", ".join(
        [f"{rates[symbol]:7.03} {symbol}" for symbol in SYMBOLS]
    )
    print(f"1 {base} = {rates_line}")

async def main():
    async with aiohttp.ClientSession() as session:
        for result in await asyncio.gather(
            *[get_rates(session, base) for base in BASES]
        ):
            present_result(*result)

if __name__ == '__main__':
    start = time.time()
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
    asyncio.run(main())
    elapsed = time.time() - start

    print()
    print("Затраченное время: {:.2f}s".format(elapsed))
