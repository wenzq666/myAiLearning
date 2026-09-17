import re

# ^ : 开头([]之外, []之内表示取反), 以哪个字符开始匹配
# 以数字开头
# obj = re.match(pattern='^\\d+', string='a12345')  # 失败
# obj = re.match(pattern='^\\d+', string='123dkf56') # 成功
# 以数字开头, 后边匹配除\n之外的任意字符
# obj = re.match(pattern='^\\d.*', string='123dkf56')  # 成功
# obj = re.search(pattern='^\\d.*', string='abc123dkf56')  # 失败

# $ : 结尾
# 以9位数字结尾
# obj = re.match(pattern=r'1[3-9]\d{9}$', string='133456789108345687745876')  # 失败
# obj = re.match(pattern=r'1[3-9]\d{9}$', string='13345678910')  # 成功
# obj = re.match(pattern=r'1[3-9]\d{9}$', string='1334567891w')  # 失败
# obj = re.match(pattern=r'1[3-9]\d{9}$', string='1334567891')  # 失败

# obj = re.match(pattern=r'[a-zA-Z]\w{5,7}', string='W1234a_%&^$#%')  # 成功
obj = re.match(pattern=r'^[a-zA-Z]\w{5,7}$', string='W1234a_%&^$#%')  # 失败
if obj:
    print('匹配成功...')
    print(obj.group())
else:
    print('匹配失败...')