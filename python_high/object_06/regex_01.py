"""
match(pattern, string, flags)
    从string的第一个字符开始匹配 如果第一个字符匹配不成功则为 None
====================================================================
search(pattern, string, flags)
    匹配第一次出现的字符串
====================================================================
findall(pattern, string, flags)
    匹配所有符合规则的字串 返回列表   匹配失败返回空列表
====================================================================
re.sub(pattern, repl, string, count, flags)
    用新字串repl替换匹配到的字串  count默认为0替换所有
"""
import re

#obj = re.match(pattern='abc',string='abcjhefgiabc')

#obj = re.search(pattern='abc',string='abcabcabc')

# if obj:
#     print("匹配成功")
#     print(obj)
#     print(obj.group())
# else:
#     print("匹配失败")


# obj = re.findall(pattern='abc',string='abcjhefgiabc')
# print(type(obj))
# print(obj)


obj = re.sub(pattern='abc',repl='***',string='abcjhefgiabc',count=0)
print(obj)





















