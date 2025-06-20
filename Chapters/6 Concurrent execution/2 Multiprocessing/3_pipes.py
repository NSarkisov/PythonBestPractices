from multiprocessing import Process, Pipe

class CustomClass():
    pass

def worker(connection):
    while True:
        instance = connection.recv()
        if instance:
            print(f"Дочерний процесс: получил: {instance}")
        if instance is None:
            break

def main():
    parent_conn, child_conn = Pipe()

    child = Process(target=worker, args=(child_conn,))

    for item in (
        42,
        'some string',
        {'one': 1},
        CustomClass(),
        None,
    ):
        print(
            "Родительский процесс: отправил: {}".format(item)
        )
        parent_conn.send(item)
    child.start()
    child.join()

if __name__ == '__main__':
    main()