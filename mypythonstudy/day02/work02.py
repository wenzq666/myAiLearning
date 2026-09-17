# 使用while循环打印'hello python'50次
# i = 1
# while i < 51:
#     print("hello python",i)
#     i += 1

# 使用while循环打印1-100
# i = 1
# while i < 101:
#     print(i)
#     i += 1

# 使用while循环计算1 - 100 之间的累加和
# i = 1
# sum = 0
# while i < 101:
#     sum += i
#     i += 1
# print(sum)

# 使用for循环计算1 - 100 之间的累加和
# sum = 0
# for item in range(101):
#     sum += item
# print(sum)

# 要求用户输入一个字符串，遍历当前字符串并打印，如果遇见“q”,则终止循环
# for item in 'sjhagfhvbdsopiqjwhbfsnqioui':
#     print(item)
#     if item == 'q':
#         break

# 使用for循环计算100 - 999 之间的偶数的个数
# sum = 0
# for item in range(100,1000):
#     if item % 2 == 0 :
#         sum += 1
# print(sum)

# 要求用户输入一个字符串，遍历当前字符串并打印，如果遇见“e”,则终止循环。如果遇见` ' '`（空格）则跳过当前输出。
# for item in 'sjhag fhvbdsopiqjwhbfesnqioui':
#     if item == 'e':
#         break
#     elif item == ' ':
#         continue
#     print(item)

# 编写代码模拟用户登陆。要求：用户名为 binzi，密码 123456，
# 如果输入正确，打印“欢迎光临”，程序结束，如果输入错误，提示用户输入错误并重新输入
# name = 'binzi'
# password = '123456'
# while True:
#     user_name = input("user_name:")
#     if user_name == name:
#         user_pass = input("user_pass:")
#         if user_pass == password:
#             print("欢迎光临")
#             break
#         else:
#             print('密码不对')
#     else:
#         print("无此用户")


# 编写程序,分别统计字母和数字的个数,具体效果如下:
# 请输入字符串:abc123def
# 结果如下:
# LETTERS:6
# DIGITS:3
# LETTERS = 0
# DIGITS = 0
# for item in input("word:"):
#     if ('a' <= item <= 'z') or ('A' <= item <= 'Z'):
#         LETTERS += 1
#     if '0' <= item <= '9':
#         DIGITS += 1
# print(LETTERS)
# print(DIGITS)

# 编写一个接受句子的程序，并计算大写字母和小写字母的数量。 假设将以下输入提供给程序：
# 请输入字符串:ABC123DEF
# LETTERSUPPER = 0
# LETTERLOWER = 0
# for item in input("words:"):
#     if item.isupper() :
#         LETTERSUPPER += 1
#     if item.islower() :
#         LETTERLOWER += 1
# print(LETTERSUPPER)
# print(LETTERLOWER)

# 设计"过7 游戏” 程序,即在 1- 99 之间的数字中,
# 如果数字 包含 7 或者是 7 的倍数,则输出"过...",
# 否则输出 具体的数字.
# for item in range(100):
#     if (item % 7 == 0 or item % 10 == 7 or item // 10 == 7):
#         print("过")
#     else:
#         print(item)






