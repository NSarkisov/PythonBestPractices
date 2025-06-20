import requests
import time

SYMBOLS = ('USD', 'PLN', 'EUR', 'CZK', 'NOK')
BASES = ('USD', 'PLN', 'EUR', 'CZK', 'NOK')

def fetch_rates(base):
    response = requests.get(
        f"https://api.vatcomply.com/rates?base={base}"
    )
    response.raise_for_status()
    rates = response.json()
    rates[base] = 1

    rates_line = ", ".join(
        [f"{rates["rates"][symbol]:7.03} {symbol}" for symbol in SYMBOLS]
    )

    print(f"1 {base} = {rates_line}")

def main():
    for base in BASES:
        fetch_rates(base)


if __name__ == '__main__':
    started = time.time()
    main()
    elapsed = time.time() - started

    print()
    print("Затраченное время: {:.2f}s".format(elapsed))