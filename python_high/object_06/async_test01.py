"""
实现方法:
1.定义异步函数  async def 函数名():
2.await 手动挂起任务, 释放空闲资源
3.asyncio.run(main()) 运行异步任务
"""
import asyncio
import time

async def task(name, delay):
    print(f"{name}--开始执行....")
    await asyncio.sleep(delay)
    return name , delay

async def main():
    start_time = time.time()

    tasks = [task("任务1",6),task("任务2",2),task("任务3",4)]

    result = await asyncio.gather(*tasks)

    print("result--->",result)

    print("总耗时",time.time() - start_time)


# 运行
asyncio.run(main())


















