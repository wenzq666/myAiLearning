"""
进程编号
"""
import multiprocessing

import multiprocessing
import random
import time
import os

#获取当前进程
print(os.getpid())
#获取父进程
print(os.getppid())


# os.kill(os.getppid(),9)

# 任务1
def task1(name):
    print("task1父进程",multiprocessing.parent_process())
    print("task1父进程PID", multiprocessing.parent_process().pid)
    print("task1当前进程", multiprocessing.current_process())
    print("task1当前进程PID", multiprocessing.current_process().pid)
    for i in range(5):
        time.sleep(random.randint(0, 5))
        print(f"{name}:coding....{i}")

# 任务2
def drink(name,age):
    print("drink父进程", multiprocessing.parent_process())
    print("drink父进程PID", multiprocessing.parent_process().pid)
    print("drink当前进程", multiprocessing.current_process())
    print("drink当前进程PID", multiprocessing.current_process().pid)
    for i in range(5):
        time.sleep(random.randint(0, 4))
        print(f"{name}:{age}:drink....{i}")



if __name__ == '__main__':
    print(multiprocessing.parent_process().pid)

    # 创建进程
    p1 = multiprocessing.Process(target=task1, name="coding", args=('迪丽热巴',))
    print("p1----->",p1.name)
    p2 = multiprocessing.Process(target=drink, args=('迪丽热巴',), kwargs={'age':18})
    print("p2----->",p2.name)


    # 启动进程
    p1.start()
    p2.start()