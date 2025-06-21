import time
import requests
from threading import Thread, Lock
from queue import Queue, Empty

THREAD_POOL_SIZE = 5

SYMBOLS = ('USD', 'PLN', 'EUR', 'CZK', 'NOK')
BASES = ('USD', 'PLN', 'EUR', 'CZK', 'NOK')


class Throttle:
    """
    Алгоритм маркерной корзины (token bucket):
    Существует «Корзина» с заранее определенным количеством маркеров.
    • Каждый маркер соответствует одному разрешению на обработку одной единицы работы.
    • Каждый раз, когда рабочий поток запрашивает один или несколько маркеров
    (разрешений), алгоритм работает так:
        1. Проверить, сколько времени прошло с момента последнего заполнения корзины.
        2. Если прошло достаточно времени, заполнить корзину количеством маркеров, соответствующим разности во времени.
        3. Если количество хранимых маркеров больше либо равно запрошенному количеству, уменьшить количество хранимых
           маркеров до запрошенной величины и вернуть ее.
        4. Если количество хранимых маркеров меньше запрошенного, вернуть О.
    """

    def __init__(self, rate):
        self._consume_lock = Lock()
        self.rate = rate
        self.tokens = 0
        self.last = None

    def consume(self, amount=1):
        with self._consume_lock:
            now = time.time()

            # Отсчет времени инициализируется при первом запросе
            # маркера, чтобы предотвратить всплеск запросов
            if self.last is None:
                self.last = now

            elapsed = now - self.last

            # Проверяем, что прошедший квант времени
            # достаточно велик для добавления новых маркеров

            if elapsed * self.rate > 1:
                self.tokens += elapsed * self.rate
                self.last = now
            # Корзина никогда не должна переполняться
            self.tokens = min(self.rate, self.tokens)

            # Выдать маркеры, если они доступны
            if self.tokens >= amount:
                self.tokens -= amount
                return amount
            return 0

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

def worker(worker_queue, results_queue, throttle):
    while not worker_queue.empty():
        try:
            item = worker_queue.get_nowait()
        except Empty:
            break
        while not throttle.consume():
            time.sleep(0.1)
        try:
            result = fetch_rates(item)
        except Exception as err:
            results_queue.put(err)
        else:
            results_queue.put(result)
        finally:
            worker_queue.task_done()


def main():
    work_queue = Queue()
    result_queue = Queue()
    throttle = Throttle(10)

    for base in BASES:
        work_queue.put(base)

    threads = [
        Thread(target=worker, args=(work_queue, result_queue, throttle))
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