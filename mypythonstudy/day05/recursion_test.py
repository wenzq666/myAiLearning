"""
递归函数
    函数内部调用自身
    1.函数功能 2.寻找递归结束条件 3.找出函数等价关系式
递(传递数据) 归(计算)
"""
num = 1
def fun1():
    global num
    print(f'递归函数 {num}')
    num += 1
    if num == 5:
        return
    fun1()


fun1()


def fun2(n):
    if n == 1:
        return  1
    return fun2(n -1) +n

print(fun2(5))

"""
递
1.  fun(4) + 5
2.  fun(3) + 4
3.  fun(2) + 3
4.  fun(1) + 2
5.  1


归
1.  1
2.  1 + 2 = 3
3.  3 + 3 = 6
4.  6 + 4 = 10
5.  10 + 5 = 15

"""


# 阶乘
def fun3(n):
    if n <= 2:
        return n
    return fun3(n-1) * n


print(fun3(4))

"""
递↓
1. n=5 fun(4) * 5
2. n=4 fun(3) * 4
3. n=3 fun(2) * 3
4. n=2 2

归↑
4. n=2  2
3. n=3  3 * fun(2) = 3 * 2 
4. n=4  4 * fun(3) = 4 * (2 * 3)
5. n=5  5 * fun(4) = 5 * (2 * 3 * 4)
"""










