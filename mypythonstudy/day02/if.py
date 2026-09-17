import random
# bool
# bool1 = True
# bool2 = False
# print(bool1)
# print(bool2)
# print(type(bool1))
# print(type(bool2))

# if
# num = eval(input("输入:"))
# if num >= 20 :
#     print(num)
# elif num >= 10 :
#     print(num)
# else:
#     print('wrong')
"""
age = eval(input("请输入年龄:"))
if age >= 90 :
    print("old man")
elif age >= 60 :
    print("middle man")
elif age >= 18 :
    print("young man")
else:
    print("little man")
 """

"""
username = input("请输入用户名:")
if username == "admin" :
    password = input("请输入密码")
    if password == "123123" :
        print("success")
    else:
        print("fail")
else:
    print("用户名不存在")
"""


num = random.randint(1,10)
print(num)


user_num = int(input('输入1-10之间的数字:'))
if num > user_num :
    print('小了')
elif num < user_num :
    print('大了')
else:
    print('yeah!')