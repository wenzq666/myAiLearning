# 定义一个简单的函数run，函数的功能是输出"我在跑步" 以及 “管住嘴，迈开腿”，并调用此函数。
def run():
    print("在跑步,管住嘴，迈开腿")

run()

# 在第一题中，我们已经用函数run实现了一些功能，如果我们想run函数做的操作执行1000遍，怎么实现代码？
# for i in range(0,1000):
#     run()

# 现在我们来实现一个有参数有返回值的函数**multiplication**，并实现调用，要求如下 ：
# 我们要用函数来实现7与13两个数字的乘法运算，并返回两个数的计算结果进行输出
def multiplication(x,y):
    return x * y


print(multiplication(7,13))


# 编写程序,给定数N . 使用递归调用函数从 1 到N 求和
# 举例: 用户输入5,输出结果15
def func_recur(n):
    if n == 1:
        return 1
    return func_recur(n - 1) + n


#print(func_recur(int(input("请输入一个整数:"))))


# 使用lambda函数定义一个可以计算两个数字之和的函数。
fn1 = lambda x,y : x + y

# 使用lambda函数定义一个可以将整数转换为字符串并在控制台中打印的函数。
fn2 = lambda n: print(str(n))
fn2(3)

# 使用lambda函数,定义一个函数，该函数可以接受两个字符串作为输入并将其连接起来，
# 然后在控制台中将其打印出 来。
fn3 = lambda s1,s2: print(s1+s2)
fn3('s1','s2')


# 使用lambda定义一个函数，该函数可以接受两个字符串作为输入，
# 并在控制台中打印最大长度的字符串。如果 两个字符串的长度相同，则该函数应逐行打印所有字符串。
fn4 = lambda s1,s2:  print(s1) if len(s1) > len(s2) else ( print(s2) if len(s2) > len(s1) else print(s1 + '\n' +s2))
fn4('qwert','qwer')


# 定义一个函数，该函数可以生成和打印一个列表，其中值是介于1到20之间的数字的平方（均包括 在内）
def func_list():
    list1 = list()
    for i in range(1,21):
        list1.append(i*i)
    return list1


print(func_list())



#定义一个函数，该函数可以生成一个列表，其中值是介于1到20之间的数字的平方（均包括在 内）。
# 然后，该功能需要打印列表中的前5个元素。
print(func_list()[:5])




# 定义一个函数, 使用随机模块和列表推导，输出一个随机数，该随机数可被5和7整除，介于10 和150之间（包括10和150）。
import random

def func_ran():
    list1 = [i for i in range(10,151) if i % 5 == 0 and i % 7 == 0]
    print(list1)
    result = random.choice(list1)
    return result


print(func_ran())


