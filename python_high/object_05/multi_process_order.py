import multiprocessing
import time


def task():
    print("task的进程",multiprocessing.current_process())
    time.sleep(0.2)


if __name__ == '__main__':
    for i in range(10):
        p = multiprocessing.Process(target=task)
        p.start()










