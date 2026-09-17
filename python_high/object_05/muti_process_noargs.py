import multiprocessing
import random
import time

# 任务1
def task1():
    for i in range(5):
        time.sleep(random.randint(1, 20))
        print(f"coding....{i}")

# 任务2
def drink():
    for i in range(5):
        time.sleep(random.randint(0, 4))
        print(f"drink....{i}")



if __name__ == '__main__':

    # 创建进程
    p1 = multiprocessing.Process(target=task1, name="coding")
    print("p1----->",p1.name)
    p2 = multiprocessing.Process(target=drink)
    print("p2----->",p2.name)


    # 启动进程
    p1.start()
    p2.start()