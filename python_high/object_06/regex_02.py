import re

# . 匹配任意一个字符  /n除外
obj = re.match(pattern='.',string='asdasd')



if obj:
    print("匹配成功")
    print(obj.group())













