from threading import Thread

result = 0


def task1():
    global result
    for i in range(10000000):
        result += 1
    print("task1-->",result)



def task2():
    global result
    for i in range(10000000):
        result += 1
    print("task2-->", result)

def task3():
    global result
    for i in range(10000000):
        result += 1
    print("task3-->", result)


t1 = Thread(target=task1)
t2 = Thread(target=task2)
t3 = Thread(target=task3)

t1.start()
t2.start()
t3.start()

print("主线程-->",result)












