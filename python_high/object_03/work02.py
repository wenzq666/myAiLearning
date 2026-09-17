


def outer_fun(func):
    def inner_func(*args):
        res = func(*args)
        length = len(args)
        return f"相加后的结果{res}，还需要得到参数个数{length}"
    return inner_func



@outer_fun
def func(*args):
    return sum(args)


print(func(1, 2, 3, 4))








