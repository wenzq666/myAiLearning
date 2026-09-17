import multiprocessing
import time


def task():
    for i in range(10):
        print("task的进程",multiprocessing.current_process())
        time.sleep(0.2)


if __name__ == '__main__':
    # daemon=True  主进程不等子进程结束而结束  （守护主进程）
    p = multiprocessing.Process(target=task,daemon=True)
    p.start()

    time.sleep(2)
    print("主进程结束")










