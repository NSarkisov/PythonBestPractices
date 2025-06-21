import time
import requests

from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool


SYMBOLS = ('USD', 'PLN', 'EUR', 'CZK', 'NOK')
BASES = ('USD', 'PLN', 'EUR', 'CZK', 'NOK')

POOL_SIZE = 5

def fetch_rates(base):
    response = requests.get(
        f"https://api.vatcomply.com/rates?base={base}"
    )
    response.raise_for_status()
    rates = response.json()
    rates[base] = 1
    return base, rates

def present_result(base, rates):
    rates_line = ", ".join(
        [f"{rates["rates"][symbol]:7.03} {symbol}" for symbol in SYMBOLS]
    )
    print(f"1 {base} = {rates_line}")

def main(use_threads=False):
    if use_threads:
        pool_cls = ThreadPool
    else:
        pool_cls = ProcessPool

    with pool_cls(POOL_SIZE) as pool:
        results = pool.map(fetch_rates, BASES)

    for result in results:
        present_result(*result)

if __name__ == '__main__':
    started = time.time()
    main(use_threads=False)
    elapsed = time.time() - started

    print()
    print("Затраченное время: {:.2f}s".format(elapsed))