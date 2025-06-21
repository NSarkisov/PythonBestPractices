from multiprocessing import Process
import os
import time

def work(identifier):
    time.sleep(10)
    print(
        f'Дочерний процесс '
        f'{identifier}, pid: {os.getpid()}'
    )


def main():
    print(
        f'Родительский процесс: {os.getpid()}'
    )
    processes = [
        Process(target=work, args=(number,))
        for number in range(5)
    ]
    for process in processes:
        process.start()

    while processes:
        processes.pop().join()

if __name__ == '__main__':
    main()
