"""
正则 匹配多个字符
"""
import re

# * :匹配前1个字符出现0次或无数次
#obj = re.match(pattern='a*',string='baaaabbbb')

#obj = re.match(pattern='\\d*',string='*baaaabbbb')

# + :匹配前1个字符只少出现一次
#obj = re.match(pattern='a+',string='aaaabbbbaaa')

#obj = re.match(pattern='\\d+',string='6+5baaaabbbb')

# ? :匹配前1个字符出现0次或1次
#obj = re.match(pattern='a?',string='aaaabbbbaaa')


# {m}: 匹配前1个字符出现m次
# 匹配手机号: 第1个数字是1开头 第2个数字不能是012 剩余9位数字是任意数字
# obj = re.match(pattern=r'1[3-9]\d{9}', string='13345678910')  # 成功
# obj = re.match(pattern=r'1[3-9]\d{9}', string='133456789108345687745876')  # 成功

# {m,n}: 匹配前1个字符出现m到n次  ,后边不能加空格
# 密码: 要求首字符是字母, 剩余的是 数字字母_汉字, 字符位数是6-8位
# obj = re.match(pattern=r'[a-zA-Z]\w{5,7}', string='a12345678')  # 成功
# obj = re.match(pattern=r'[a-zA-Z]\w{5,7}', string='W1234')  # 失败  5位
# obj = re.match(pattern=r'[a-zA-Z]\w{5,7}', string='W1234a')  # 成功  6位
# obj = re.match(pattern=r'[a-zA-Z]\w{5,7}', string='W1234a_好')  # 成功  8位
obj = re.match(pattern=r'[a-zA-Z]\w{5,7}', string='W1234a_%&^$#%')  # 成功


if obj:
    print("匹配成功")
    print(obj.group())
else:
    print("匹配失败")

