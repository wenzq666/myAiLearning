userName = "雷霆嘎巴"
age = 66
haveMoney = 999.5556

"""占位符
%s 字符串
%d 整数
%f 浮点
%.2f 保留两位小数
"""

print("姓名%s,年龄%d,剩余金额%f" % (userName, age, haveMoney))

# 浮点精度问题处理
print("姓名%s,年龄%d,剩余金额%.2f" % (userName, age, haveMoney))

print(f"姓名{userName},年龄{age},余额{haveMoney}")
# 浮点精度问题处理
print(f"姓名{userName},年龄{age},余额{haveMoney:.2f}")

print("111\t222")
print("111\n222")

print(111, end="____")
print(222)

