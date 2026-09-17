# 循环

'''
i = 0;
while i < 3 :
    print(i)
    i += 1
'''

# 输出 1-100
'''
i = 1
while i < 101 :
    print(i)
    i += 1
'''

# 输出 1-100 的偶数
'''
i = 1
while i < 101 :
    if i % 2 == 0 :
        print(i)
    i += 1
'''

# 1-100的累加
'''
i = 1
result = 0

while i < 101 :
    result += i
    i += 1

print(result)
'''


# break
'''
i = 1

while i < 6 :
    if i == 3:
        break
    print(i)
    i += 1
'''

# continue
'''
j = 1

while j < 6 :
    if j == 3:
        j += 1
        continue
    print(j)
    j += 1
'''

# 猜数字
'''
import random
snum = random.randint(1, 100)

while True:
    num = int(input("请输入1-100的数字:"))
    if num > snum:
        print("猜大了")
    elif num < snum:
        print("猜小了")
    else:
        print("bingo!")
        break
'''

# 嵌套循环
'''
j = 1

while j < 4 :
    i = 1
    while i < 4:
        print(i)
        i += 1
    j += 1
'''


# 九九乘法表
'''
i = 1
while i < 10 :
    print(f'{i}*9={i*9}' , end='\t')
    i += 1
'''

j = 1
while j < 10 :
    i = 1
    while i <= j:
        print(f'{i}*{j}={i * j}', end='\t')
        i += 1
    print()
    j += 1







