"""
flags: 修饰符, 给正则添加了额外的要求
"""
import re

# re.S: .匹配包括\n在内的任意字符
# obj = re.match(pattern='.', string='\nabc', flags=re.S)

# re.I: 忽略大小写
# obj = re.match(pattern='abc', string='aBcdef', flags=re.I)

# re.I|re.S: 忽略大小写和.匹配包括\n在内的任意字符
obj = re.match(pattern='abc.', string='ABC\nefg', flags=re.I | re.S)
print(obj)
print(obj.group())
