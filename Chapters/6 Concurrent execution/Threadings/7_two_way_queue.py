import requests
import time
from threading import Thread
from queue import Queue, Empty

THREAD_POOL_SIZE = 5

SYMBOLS = ('USD', 'PLN', 'EUR', 'CZK', 'NOK')
BASES = ('USD', 'PLN', 'EUR', 'CZK', 'NOK')


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

def worker(worker_queue, results_queue):
    while not worker_queue.empty():
        try:
            item = worker_queue.get_nowait()
        except Empty:
            break
        else:
            results_queue.put(fetch_rates(item))
            worker_queue.task_done()


def main():
    work_queue = Queue()
    result_queue = Queue()

    for base in BASES:
        work_queue.put(base)

    threads = [
        Thread(target=worker, args=(work_queue, result_queue))
        for _ in range(THREAD_POOL_SIZE)
    ]
    for thread in threads:
        thread.start()

    work_queue.join()

    while threads:
        threads.pop().join()

    while not result_queue.empty():
        present_result(*result_queue.get())


if __name__ == '__main__':
    started = time.time()
    main()
    elapsed = time.time() - started

    print()
    print("Затраченное время: {:.2f}s".format(elapsed))
