import asyncio
import requests
import time

from concurrent.futures import ThreadPoolExecutor

SYMBOLS = ('USD', 'PLN', 'EUR', 'CZK', 'NOK')
BASES = ('USD', 'PLN', 'EUR', 'CZK', 'NOK')

async def fetch_rates(base):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        ThreadPoolExecutor(20),
        requests.get,
        f"https://api.vatcomply.com/rates?base={base}"
    )

    response.raise_for_status()
    rates = response.json()["rates"]
    # Курс валюты no отношению к самой себе равен 1:1
    rates[base] = 1.
    print(base, rates)

async def main():
    await asyncio.gather(*[fetch_rates(base) for base in BASES])


if __name__ == '__main__':
    start = time.time()
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
    asyncio.run(main())
    elapsed = time.time() - start

    print()
    print("Затраченное время: {:.2f}s".format(elapsed))