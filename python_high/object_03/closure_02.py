def outer_fun(num):
    total = num
    def inner_fun(num2):
        nonlocal total
        total += num2
        return total
    return inner_fun


f = outer_fun(100)
print(f.__closure__[0].cell_contents)
print("============")
print(f(1))
print("============")
print(f.__closure__[0].cell_contents)
print("============")
print(f(1))
print(f(1))
print(f(1))


