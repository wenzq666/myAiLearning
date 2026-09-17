# 函数说明
def get_res(x , y):
    """
    sum(x+y)
    :param x:num1
    :param y:num2
    :return:num1+num2
    """
    return x + y


get_res(6,4)

# 函数嵌套
def get_sum():
    print(f'总价:{10+20+30}')
    return 10+20+30


def get_avg():
    print(f'平均价 begin')
    sum_num = get_sum() / 3
    print(f'平均价:{sum_num}')
    print(f'平均价 end')

get_avg()


# 变量作用域
x = 1

def get_x():
    y = 2
    print(f'函数中调用函数外的变量x:{x}')
    print(f'函数中调用函数内的变量y:{y}')


#print(f'函数外调用函数内的变量y:{y}')
get_x()


def set_x():
    global x
    x = 2
    print(f'函数中调用函数外的变量x:{x}')

print(f'函数外调用函数外的变量x:{x}')
set_x()
print(f'函数外调用函数外的变量x:{x}')


def fun_mutire():
    return (([[10, {"A":20}],20],20),(30,40))


print(fun_mutire())



def fun2(name,age,gender='塑料袋'):
    print(f'name:{name},age:{age},gender={gender}')

fun2(age= 20 , name= 'dilireba')
fun2(age= 22 , name= 'alibaba',gender='女')


def fun3(name,age,*args):
    print(f'name:{name},age:{age}')
    print(*args)
    for arg in args:
        print(arg)


fun3('aaa',11,'ss',54,{"A":"b"})



def fun4(name,age,*args,**kwargs):
    print(f'name:{name},age:{age}')
    print(args)
    print(kwargs)

fun4('xx',20,phone=1245,addr='xx.xx.xx')




