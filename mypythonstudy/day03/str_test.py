# str
#str1 = '0123456'

#print(str1[7])
#print(str1[-1])
#print(len(str1))



# str2 = 'itheima and itcast'
# print(str2.index('and'))
# #print(str2.index('is'))
#
# print(str2.find('is'))
#
# print(str2.count('it'))
#
#
# str3 = 'hello world'
# str4 = str3.replace('hello', 'hi')
#
# print(str2.split())
#
# str5 = '   ss ss  '
# print(str5.strip())
#
#
# str6 = '0123456789'
# #[开始:结束:步长]
# print(str6[::])
# print(str6[:])
# print(str6[2:])
# print(str6[:5])
# print(str6[99:-99:-1])
# print(str6[-99:99:1])



# str7 = '294uruiewbf'
#
# for i in str7:
#     print(i)
#
# i = 0
#
# while i < len(str7):
#     print(str7[i])
#     i += 1

str8 = 'hello world'

# 旋转的位数
rotate_num = 29
rotate_num %= len(str8)

print(str8[-rotate_num:] + str8[:-rotate_num])


print(256 is 256)
print(257 is 257)













