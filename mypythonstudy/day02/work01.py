
"""
# 用户输入年龄，如果年龄超过60岁，输出：可以退休了。
age = int(input("age:"))
if age > 60 :
    print("可以退休了")

# 用户输入年龄，如果年龄超过60岁，输出："可以退休了"， 否则，输出："小伙子，加油干！"
age = int(input("age:"))
if age > 60 :
    print("可以退休了")
else:
    print("小伙子，加油干！")

# 用户输入年龄，按照如下标准书写程序，判断用户处于哪个年龄阶段，并提示：您的年龄是xx: 青少年/青年/中年/老年。
# 年龄段划分标准：0-17岁为青少年；18-35岁为青年；36-59为中年，60-99岁为老年。
age = int(input("age:"))
if  0 <= age <= 17 :
    print("您的年龄是青少年")
elif 18 <= age <= 35 :
    print("您的年龄是青年")
elif 36 <= age <= 59 :
    print("您的年龄是中年")
elif 60 <= age <= 99 :
    print("您的年龄是老年")

# 用户登录输入验证码，已知验证码是`axyz`,  验证码正确可以登录，否则输出：验证码错误。
code = input("code:")
if code == 'axyz' :
    print('验证码正确可以登录')
else:
    print('验证码错误')


# 制作用户登录系统：已知A用户注册的用户名为`binzi`，密码是`123456`。具体要求如下：
# 登录时需要验证用户名、密码、验证码(固定验证码为`qwer`)。
# 提示：系统先验证验证码是否正确，正确后再验证用户名和密码。
code = input("code:")
if code == 'qwer' :
    print('验证码正确可以登录')
    user_name = input("user_name:")
    if user_name == 'binzi' :
        password = input("password:")
        if password == '123456' :
            print('success!')
        else:
            print('fail!')
    else:
        print('无此用户')
else:
    print('验证码错误')
"""

#编写程序，运行后用户输入4位整数作为年份，判断其是否为闰年。
#如果年份能被400整除，则为闰 年；如果年份能被4整除但不能被100整除也为闰年
year = int(input("year:"))
if year % 400 == 0:
    print(f'{year}为闰年')
elif year % 4 == 0:
    if year % 100 != 0:
        print(f'{year}为闰年')
else:
    print(f'{year}不是闰年')




