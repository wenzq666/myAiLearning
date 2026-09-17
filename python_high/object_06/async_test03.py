import asyncio

result = 0


# 1. 使用 async def 定义协程函数
async def task1():
    global result
    for i in range(10000000):
        result += 1
    print("task1-->", result)


async def task2():
    global result
    for i in range(10000000):
        result += 1
    print("task2-->", result)


async def task3():
    global result
    for i in range(10000000):
        result += 1
    print("task3-->", result)


async def main():
    global result

    # 2. 创建协程任务列表
    tasks = [task1(), task2(), task3()]

    # 3. 使用 asyncio.gather 并发调度执行所有协程，并等待它们全部完成
    await asyncio.gather(*tasks)

    # 4. 所有子协程执行完毕后，主协程再打印最终结果
    print("主协程--> 最终结果:", result)


# 5. 运行事件循环
if __name__ == "__main__":
    asyncio.run(main())
