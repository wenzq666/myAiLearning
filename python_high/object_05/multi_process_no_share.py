"""
多进程之间资源不共享
"""
import multiprocessing
import time

my_list = []

def task1():
    for i in range(5):
        my_list.append(i)
        time.sleep(5)
    print("task的my_list--->",my_list)

def task2():
    for i in ['11','22','33','44']:
        my_list.append(i)
    print("task2的my_list--->",my_list)

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=task1)
    p2 = multiprocessing.Process(target=task2)

    # p1.start()
    # p2.start()

    p1.run()
    p2.run()


    my_list.append('主进程')
    print(my_list)
