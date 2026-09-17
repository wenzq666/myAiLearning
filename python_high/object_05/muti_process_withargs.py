import multiprocessing
import random
import time

# 任务1
def task1(name):
    for i in range(5):
        time.sleep(random.randint(0, 5))
        print(f"{name}:coding....{i}")

# 任务2
def drink(name,age):
    for i in range(5):
        time.sleep(random.randint(0, 4))
        print(f"{name}:{age}:drink....{i}")



if __name__ == '__main__':

    # 创建进程
    p1 = multiprocessing.Process(target=task1, name="coding", args=('迪丽热巴',))
    print("p1----->",p1.name)
    p2 = multiprocessing.Process(target=drink, args=('迪丽热巴',), kwargs={'age':18})
    print("p2----->",p2.name)


    # 启动进程
    p1.start()
    p2.start()