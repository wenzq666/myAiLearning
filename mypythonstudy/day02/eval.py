# 转int
age = int(input("age:"))
print(age)
print(type(age))

# 转浮点
price = float(input("price:"))
print(price)
print(type(price))
# 转字符串
num = 100.5
print(num)
print("转换前类型",type(num))

str1 = str(num)
print("转换位字符串："+str1)
print(f'转换后类型：{type(str1)}')


# 用来计算在字符串中的有效Python表达式,并返回一个对象
ss = eval(input(":"))
print(ss)
print(type(ss))

