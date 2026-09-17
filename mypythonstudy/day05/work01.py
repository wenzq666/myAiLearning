# 案例：使用列表推导式生成平方数集合
# 例如, 用户输入10, 表示要生成 1~10的每一个数字的2平方的集合
list1 = [i*i for i in range(1 , 10)]
print(list1)

# 请定义一个函数, 在函数中3 + 5的计算操作, 并且将累加后的结果直接打印出来即可
def func_sum():
    print(3+5)


func_sum()

# 请定义一个函数, 要求函数传入二个任意的数字,
# 在函数体中完成这二个数字的累加计算操作, 并且将累加后的结果直接打印出来即可
def func_sum2(x,y):
    print(x+y)

func_sum2(4,6)

# 请定义一个函数, 要求函数传入二个任意的数字,
# 在函数体中完成这二个数字的累加计算操作, 并且将累加后的结果 返回 然后调用函数 接收返回值, 并且将返回值输出打印
def func_sum3(x,y):
    return x+y

total = func_sum3(4,6)
print(total)


"""
需求: 奇偶求和.
    编写一个程序，求出一个列表中偶数和奇数的和。

    定义函数calculate_sum()，参数为一个数字列表numbers_list, 分别求出偶数和奇数的和。
    最后，返回一个列表(元组)，第一个元素为偶数的和，第二个元素为奇数的和。
"""
def calculate_sum(numbers_list):
    # 偶数和
    even_total = 0
    # 奇数和
    odd_total = 0
    for i in numbers_list:
        if i % 2 == 0:
            even_total += i
        else:
            odd_total += i
    return even_total,odd_total


print(calculate_sum([5, 8, 7, 6, 3, 2, 14, 2]))


# 需求: 完成一个累加计算的操作功能
# # 不定长元组(位置) : 在调用函数的时候, 只需要使用位置传参即可
def func_tuple(*args):
    total = 0
    for i in args:
        total += i
    return total


print(func_tuple(1, 2, 3, 4, 5))

# 不定长的字典: 传递参数的时候 需要使用关键词传参
# 定义一个函数, 支持可以保存一个用户的信息, 但是用户的信息属性不确定有多少个
def func_dict(**kwargs):
    print(kwargs)

func_dict(name = "迪丽热巴",age = 20,phone = '113',addr = '12x.xx.xx')


# 组合应用:  将不定长的元组 和 不定长字典 组合在一起


# 如何调用呢?
# 调用方式一: 分别定义一个元组 和 字典 , 然后再传递参数的时候, 在变量的前面使用*或** 来表示给谁传递
def func_all(*args,**kwargs):
    print(args,kwargs)


t1 = (1,5,6,89,7,2)
d1 = {"AA":"bb","vv":"CC"}
func_all(*t1,**d1)


# 调用方式二:
func_all(1,5,4,2,name = 'ss',age = 33)




