# 1. 定义一个函数`celsius_to_fahrenheit`，接收一个参数`celsius`（摄氏度）
# 2. 在函数内部，使用公式`(celsius * 9/5) + 32`将摄氏度转换为华氏度
# 3. 函数返回计算结果
# 4. 通过input()获取用户输入的摄氏度（转换为浮点数）
# 5. 调用函数并打印结果，格式为："XX摄氏度等于XX华氏度"
# 6. 为函数添加必要的注释，说明函数功能
# def celsius_to_fahrenheit(celsius):
#     return (celsius * 9 / 5) + 32
#
# celsius = float(input("输入摄氏度:"))
# fahrenheit = celsius_to_fahrenheit(celsius)
# print(f'{celsius}摄氏度等于{fahrenheit}华氏度')



# 实现一个简单的计数器程序，要求：
#
# 1. 在函数外部定义一个全局变量`counter`，初始值为0
# 2. 定义一个函数`increment_counter`，无参数
# 3. 在函数内部：
#    - 使用global关键字声明要修改全局变量`counter`
#    - 将`counter`的值增加1
#    - 打印"计数器已增加，当前值为：X"
# 4. 定义另一个函数`display_counter`，无参数
# 5. 在`display_counter`函数内部直接访问并打印全局变量`counter`的值（不需要global关键字）
# 6. 按顺序调用函数：先调用`increment_counter`三次，然后调用`display_counter`
# 7. 为代码添加注释，说明全局变量的使用
# counter = 0
# def increment_counter():
#     global counter
#     counter += 1
#     print(f'计数器已增加，当前值为：{counter}')
#
#
# def display_counter():
#     print(f'访问全局计数器：{counter}')
#
# increment_counter()
# increment_counter()
# increment_counter()
# display_counter()




dict1 = {"a":"b","c":"d"}

print(*dict1)
# print(*dict1,**dict1)

def func(**kwargs):
    print(kwargs)

func(**dict1)
