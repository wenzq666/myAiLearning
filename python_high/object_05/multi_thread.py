import threading
import time
import os


def task1(name):
    print(os.getpid())
    for i in range(5):
        print(f"{name}:coding......{i}")
        time.sleep(0.2)
    os.getppid()


def task2(name,age):
    print(os.getpid())
    for i in range(5):
        print(f"{name}:{age}:drink......{i}")
        time.sleep(0.2)


t1 = threading.Thread(target=task1,args=("迪丽热巴",))
t2 = threading.Thread(target=task2,args=("古力娜扎",),kwargs={'age':18})

print(t1)
print(t2)

t1.start()
t2.start()











