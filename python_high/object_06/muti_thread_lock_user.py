import threading
from threading import Thread

result = 0


lock = threading.Lock()


def task1():
    global result
    lock.acquire()
    for i in range(10000000):
        result += 1
    lock.release()
    print("task1-->",result)



def task2():
    global result
    with lock:
        for i in range(10000000):
            result += 1
    print("task2-->", result)


t1 = Thread(target=task1)
t2 = Thread(target=task2)

t1.start()
t2.start()

with lock:
    print("主线程-->",result)












