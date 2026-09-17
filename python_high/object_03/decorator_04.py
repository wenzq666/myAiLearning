
def outer_fun(func):
    def inner_fun(*args,**kwargs):

        return func(*args,**kwargs)
    return inner_fun




@outer_fun
def get_sum(*args,**kwargs):
    result = 0
    for i in args:
        result += i

    for v in kwargs.values():
        result += v

    return result

list1 = [1,2,3,4]
dict1 = {'num1':9,'num2':10}

print(*list1)


print(get_sum(*list1, **dict1))