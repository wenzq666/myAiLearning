










def outer_fun(func):
    def inner_func():
        return func()+".txt"
    return inner_func


@outer_fun
def content():
    return "helloworld"


print(content())














