# 闭包

# def fun_outer(num1):
#     def fun_inner(num2):
#         print(num1 + num2)
#     return fun_inner
#
#
# print(fun_outer(10)(20))



def fun_outer():
    num1 = 10
    def fun_inner(num2):
        nonlocal num1
        num1 += num2
        print(f'num1:{num1}')
        return num1
    return fun_inner

fun_inner = fun_outer()
fun_inner(1)
fun_inner(1)
print(fun_inner(1))









