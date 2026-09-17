# 简答介绍下python中异常的通用格式?
# try:
#     # 执行的业务逻辑
# except:
#     # 捕获异常的逻辑
# else:
#     # 没有异常的时候执行的逻辑
# finally:
#     # 无论是否有异常，都会执行的逻辑



# 简答介绍下python中模块和包的区别?
# 一个.py文件就是一个模块(单个文件),一个包(文件夹)目录中有 __init__.py


# 已知文件:a.txt,要求复制一份新的文件名:a[备份].txt
# old_file_name = './data/a.txt'
#
# with open(old_file_name,'r',encoding='utf-8') as f_old:
#     data = f_old.read()
#     point_index = old_file_name.rfind('.')
#     new_file_name = old_file_name[:point_index] + '[备份]' + old_file_name[point_index:]
#     print(new_file_name)
#
# with open(new_file_name,'w',encoding='utf-8') as f_dest:
#     f_dest.write(data)


# 编写一个函数以计算5/0并使用try / except捕获异常。
# try:
#     print(5 / 0)
# except:
#     print('执行有异常')

# 提示用户输入已经存在的文件名/图片名/视频名,获取到用户输入的文件名,去完成复制功能
# 要求:如果用户输入的是b.jpg,复制完后的名字为b[备份].jpg
# import os
#
# print(f'现有文件列表:{os.listdir('./data')}')
# os.chdir('./data')
# print(os.getcwd())
# in_str = input('输入要赋值的文件名:')
# str_point = in_str.rfind('.')
# new_fine_name = in_str[:str_point]+'[备份]'+in_str[str_point:]
# with open(in_str,'rb') as old_file , open(new_fine_name,'wb') as new_file:
#     while True:
#         data = old_file.read(1024)
#         if len(data) == 0:
#             break
#         new_file.write(data)
#         print('复制成功')



# 请编写程序,利用时间模块计算1加到100 0000,经历的时间是多少?
# import time
#
# start = time.time()
# sum = 0
# for i in range(1,10000001):
#     sum += i
# end = time.time()
# print(end - start)
# print(sum)



# 编写程序,利用os模块实现以下两个功能:
# 1.获取当前目录下文件列表信息
# 2.判断指定文件是否在当前目录下
# import os
#
# print(os.listdir())
#
# if '1.txt' in os.listdir():
#     print('存在该文件')
# else:
#     print('不存在该文件')



#给您一个字符串S和宽度W。您的任务是将字符串包装成一段宽度。 如果给出以下字符串作为程序的输入：
#请您输入一串字符: ABCDEFGHIJKLIMNOQRSTUVWXYZ
#请您输入展示宽度: 4

# 拓展: `textwrap`模块是Python的标准库模块，用于实现文本的自动换行和缩进。
# 它提供了一种简单的方式来格式化文本，以便它们适合在特定的宽度限制内显示,
# 其中`wrap()`方法：此方法用于将一个很长的字符串分割成多个小字符串，每个小字符串都适合于指定的宽度。
import textwrap

s = 'ABCDEFGHIJKLIMNOQRSTUVWXYZ'
w = 4

for i in range(0, len(s), w):
    print(i,w)
    print(s[i:i + w])

for i in textwrap.wrap(s, w):
    print(i)






