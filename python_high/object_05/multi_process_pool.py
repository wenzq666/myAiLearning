"""
进程池自动管理
"""
import multiprocessing
import os
import time


def task(n):
    pid = os.getpid()

    return n * n


if __name__ == '__main__':
    with multiprocessing.Pool(processes=4) as pool:
        results = [pool.apply_async(task,(i,)) for i in range(10)]

        for i,res in enumerate(results):
            print(f"任务{i}的结果是：{res.get()}")










