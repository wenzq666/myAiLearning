

def outer_fun(num1):
    num2 = 20
    def inner_fun():
        return num1 + num2
    return inner_fun


f = outer_fun(10)
print(f)

print(f.__closure__)
print(f.__closure__[0].cell_contents)
print(f.__closure__[1].cell_contents)

print(f())
























