


def outer_fun(func):
    def inner_func(a, b):
        print("计算结果")
        return func(a,b)
    return inner_func

@outer_fun
def get_sum(a, b):
    return a + b


print(get_sum(10, 99))