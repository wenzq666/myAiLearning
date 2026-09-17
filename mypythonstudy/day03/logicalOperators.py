# 逻辑运算符
num1 = 10
num2 = 20
num3 = 30

#and
print(num1 < num2 < num3)
print(num1 < num2 > num3)
print(num1 < num2 and num2 > num3)


#or
print(num1 < num2 or num2 > num3)
print(num1 < num2 or num2 < num3)

#not
print(not (num1 < num2))


for i in range(2):
    print(i)
    for j in range(5):
        print(j)



for j in range (1 , 10) :
    for i in range(1, j + 1):
        print(f'{i} * 9 = {i * 9}',end='\t')
    print()


for i in range(5):
    if i == 2:
        #break
        continue
    print(i)
else:
    print('正常结束则执行')
