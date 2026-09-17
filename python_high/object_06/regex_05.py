import re

# 正则表达式1|正则表达式2|正则表达式3 : 匹配任意一个表达式
# obj = re.match(pattern='abc|123', string='abcdefg')  # 成功
# obj = re.match(pattern='abc$|123', string='abcc')  # 失败
# obj = re.match(pattern='abc$|123', string='123djgjhfer')  # 成功
# obj = re.match(pattern='abc$|123$', string='1237846574')  # 失败
# obj = re.match(pattern='abc$|123$|^\\d.*', string='1237846574')  # 成功

# (): 匹配括号内的内容
# 匹配邮箱: @前4-20位的字母汉字数字下划线, 匹配126|qq|163三种邮箱   eg:xxxxx@126.com
# 第1个表达式 ^\\w{4,20}@126
# 第2个表达式 qq
# 第3个表达式 163.com
# obj = re.match(pattern='^\\w{4,20}@126|qq|163.com', string='123456@163.com')  # 失败
# obj = re.match(pattern='^\\w{4,20}@126|qq|163.com', string='123456@126')  # 成功
# obj = re.match(pattern='^\\w{4,20}@126|qq|163.com', string='qq')  # 成功
# obj = re.match(pattern='^\\w{4,20}@126|qq|163.com', string='163.com')  # 成功
# obj = re.match(pattern='^\\w{4,20}@126|qq|163.com', string='1633com')  # 成功

# (): 限制任意表达式的范围  表达式1->126 表达式2->qq  表达式3->163
# obj = re.match(pattern='^\\w{4,20}@(126|qq|163).com', string='123456@163.com')  # 成功
# . -> 匹配除\n之外的任意字符
# obj = re.match(pattern='^\\w{4,20}@(126|qq|163).com', string='wei12345@163@com')  # 成功
# obj = re.match(pattern='^\\w{4,20}@(126|qq|163)\\.com', string='wei12345@163@com')  # 失败
# obj = re.match(pattern='^\\w{4,20}@(126|qq|163)[.]com', string='wei12345@163@com')  # 失败
# obj = re.match(pattern='^\\w{4,20}@(126|qq|163)[.]com', string='wei12345@163.com.com.com')  # 成功
# obj = re.match(pattern='^\\w{4,20}@(126|qq|163)[.]com$', string='wei12345@163.com.com.com')  # 失败
# obj = re.match(pattern='^\\w{4,20}@(126|qq|163)[.]com$', string='wei12345@qq.com')  # 成功

# 获取分组中的内容
# qq:xxxxxx  匹配 :左边内容  :后边内容
# obj = re.match(pattern='(.*):(.*)', string='qq:12345678')
# obj = re.match(pattern='(.*):(.*)', string='wechat:xd123456')
# g1 = obj.group(1)
# g2 = obj.group(2)
#
# obj2 = re.findall(pattern='(.*):(.*)', string='wechat:xd123456')
# print(obj2)
# if obj:
#     print('匹配成功...')
#     print(obj.group())
#     # print(obj.group(0))
#     # print(obj.group(1))  # 获取第1个分组的内容
#     # print(obj.group(2))  # 获取第1个分组的内容
# else:
#     print('匹配失败...')
#
# obj2 = re.findall(pattern='.*:.*', string='wechat:xd123456')
# print(obj2)


# 引用分组
# \num: 引用分组中的内容  num:组号
# obj = re.match(pattern='<([a-zA-Z1-6]{1,4})>(.*)</([a-zA-Z1-6]{1,4})>', string='<html>hhhsjahgfj</html>')
# obj = re.match(pattern='<([a-zA-Z1-6]{1,4})>(.*)</\\1>', string='<html>hhhsjahgfj</html>')
# (?P<name>): 分组起别名  (?P=name): 引用分组别名
obj = re.match(pattern='(<(?P<g1>[a-zA-Z1-6]{1,4})>(.*)</(?P=g1)>)*', string='<html>hhhsjahgfj</html><div>hhhsjahgfj</div>')
if obj:
    print('匹配成功...')
    #print(obj.group())
    # print(obj.group(0))
    print(obj.group(1))  # 获取第1个分组的内容
    print(obj.group(2))  # 获取第1个分组的内容
    print(obj.group(3))  # 获取第1个分组的内容
else:
    print('匹配失败...')












