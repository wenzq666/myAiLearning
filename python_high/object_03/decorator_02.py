import time


def time_decorator(func):
    def inner_func():
        start_time = time.time()
        func()
        end_time = time.time()
        print(f"函数执行时间{end_time - start_time}")
    return inner_func


@time_decorator
def get_sum():
    result = 0
    for i in range(1000000000):
        result += i
    return result

get_sum()





