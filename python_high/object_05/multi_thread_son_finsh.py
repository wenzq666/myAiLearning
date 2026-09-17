import threading
import time


def task():
    for i in range(10):
        print("task的进程",threading.current_thread())
        time.sleep(0.2)


if __name__ == '__main__':
    # daemon=True  主线程不等子线程结束而结束  （守护主线程）
    p = threading.Thread(target=task,daemon=True)
    p.start()

    time.sleep(1)
    print("主进程结束")










