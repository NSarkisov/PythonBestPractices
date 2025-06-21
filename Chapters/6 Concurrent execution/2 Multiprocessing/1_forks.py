import os

pid_list = []

"""
Примечание: модуль os.fork() предназначен только для POSIX подобных систем,
то есть его можно выполнить на Linux, Macos, но не в Windows. Если нужно попробовать
в Windows воспользуйтесь WSL либо другой системой виртуализации.
"""
def main():
    pid_list.append(os.getpid())
    child_pid = os.fork()
    if child_pid == 0:
        pid_list.append(os.getpid())
        print()
        print("CHLD: привет, я дочерний процесс")
        print("CHLD: все PID'ы, которые я знаю: %s" % pid_list)
    else:
        pid_list.append(os.getpid())
        print()
        print("PRNT: привет, я родительский процесс")
        print("PRNT: PID дочернего процесса: %d" % child_pid)
        print("PRNT: все PID'ы, которые я знаю: %s" % pid_list)

if __name__ == '__main__':
    main()
