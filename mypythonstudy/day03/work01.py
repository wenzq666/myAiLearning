# 定义一个简单的函数run，函数的功能是输出"我在跑步" 以及 “管住嘴，迈开腿”，并调用此函数。
def run():
    print('我在跑步')
    print('管住嘴，迈开腿')


run()

# 在第一题中，我们已经用函数run实现了一些功能，如果我们想run函数做的操作执行1000遍，怎么实现代码？
for i in range(1000):
    run()


# 现在我们来实现一个有参数有返回值的函数**multiplication**，并实现调用，要求如下 ：
# 我们要用函数来实现7与13两个数字的乘法运算，并返回两个数的计算结果进行输出

def multiplication(num1 , num2):
    return num1 * num2


print(multiplication(7 , 13))

