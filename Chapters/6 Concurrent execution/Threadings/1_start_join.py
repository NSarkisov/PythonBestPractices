from threading import Thread

def my_func():
    print("Printing from thread")

if __name__ == '__main__':
    threads = [Thread(target=my_func) for _ in range(10)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()