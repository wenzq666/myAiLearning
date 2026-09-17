"""
贪婪模式(多多益善): 在匹配成功的前提下, 匹配更多的内容  .* .+
非贪婪模式(适可而止): 在匹配成功的前提下, 匹配更少的内容  .*?  .+?

抽取想要的内容一般都是 (.*) 或 (.*?)
"""
import re

str1 = '<h1>Python+AI顺义5期</h1>AI行情大好, 均薪很高, 赶紧学起来<h1>智能应用开发顺义20期</h1>'
# 贪婪模式, 匹配所有内容
# obj = re.match(pattern='<h1>(.*)</h1>', string=str1)
# print(obj)
# print(obj.group())
# print(obj.group(1))
#
# print('=' * 80)
# # 非贪婪模式, 匹配更少的内容
# obj = re.match(pattern='<h1>(.*?)</h1>', string=str1)
# print(obj)
# print(obj.group())
# print(obj.group(1))
#
# print('=' * 80)

# 获取满足正则表达式的所有内容\
# obj = re.findall(pattern='<h1>(.*)</h1>', string=str1)  # 贪婪模式
# obj = re.findall(pattern='<h1>(.*?)</h1>', string=str1)  # 非贪婪模式
obj = re.findall(pattern='<h1>(.*?)</h1>(.*)<h1>(.*?)</h1>', string=str1)  # 非贪婪模式
print(obj)
