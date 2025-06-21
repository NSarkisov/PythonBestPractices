import time
from threading import Thread
from threading import Lock

threads_visits = 0
threads_visits_lock = Lock()

def visit_counter():
    global threads_visits
    for i in range(100_000):
        with threads_visits_lock:
            time.sleep(0)
            threads_visits += 1

if __name__ == '__main__':
    """
    Что бы не было гонки используем lock и результат всегда:
    threads_count=100, 10000000
    """
    start = time.perf_counter()
    threads_count = 100
    threads = [
        Thread(target=visit_counter)
        for i in range(threads_count)
    ]
    for t in threads:
        t.start()

    for t in threads:
        t.join()
    end = time.perf_counter()
    print(f"{threads_count=}, {threads_visits}, time={(end-start):2f}s")