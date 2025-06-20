import time
from threading import Thread

threads_visits = 0

def visit_counter():
    global threads_visits
    for i in range(100_000):
        value = threads_visits
        time.sleep(0) # Добавим переключение контекста
        threads_visits = value + 1

if __name__ == '__main__':
    """
    гонки (race condition)
    Результат всегда неожиданный:
    При 5 последовательных запусков скрипта мы получаем следующее
    threads_count=100, 100466
    threads_count=100, 100483
    threads_count=100, 100413
    threads_count=100, 100477
    threads_count=100, 100382
    """
    threads_count = 100
    threads = [
        Thread(target=visit_counter)
        for i in range(threads_count)
    ]
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f"{threads_count=}, {threads_visits}")