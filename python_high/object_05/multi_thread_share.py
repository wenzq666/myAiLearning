import threading
import time


my_list = []


def task1():
    for i in range(10):
        my_list.append(i)
        # print("task的进程",threading.current_thread())
        time.sleep(0.2)
    print("task1--->",my_list)

def task2():
    for i in ['11','22','33','44','55']:
        my_list.append(i)
        # print("task的进程",threading.current_thread())
        time.sleep(0.2)
    print("task2--->",my_list)


if __name__ == '__main__':
    # daemon=True  主线程不等子线程结束而结束  （守护主线程）
    t1 = threading.Thread(target=task1)
    t2 = threading.Thread(target=task2)
    t1.start()
    t2.start()


    print("主线程",my_list)












