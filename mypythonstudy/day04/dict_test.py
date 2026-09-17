# dict = {k:v , k:v....}

# dict1 = {'name':'尼古拉斯','age':18,'score':99}

# print(dict1)
# print(type(dict1))
#
#
# dict2 = {}
# print(dict2)
# print(type(dict2))
#
#
# dict3 = dict()
# print(dict3)
# print(type(dict3))



# dict1 = {'name':'尼古拉斯','age':18,'gender':'333'}
# print(dict1)
#
# print(dict1['gender'])
# dict1['gender'] = '男'
# print(dict1)
# dict1['age'] = '22'
# print(dict1)

# 字典嵌套

# scores = {
#     '迪丽热巴':{'yuwen':88,'math':99,'english':95},
#     '古力娜扎':{'yuwen':66,'math':85,'english':62},
#     '尼古拉斯':{'yuwen':77,'math':76,'english':86}
# }
#
# # keys()
# for key in scores.keys():
#     print(key)
#     #print(scores[key])
#
# # values()
# for value in scores.values():
#     print(value)
#
# # items()
# for item in scores.items():
#     print(item)
#
# # 拆包
# for k , v in scores.items():
#     print(f'{k}--{v}')


# print(scores['尼古拉斯'])
# print(scores['尼古拉斯']['english'])
# print(scores['尼古拉斯'].pop('english'))
# print(scores)
#
#
# scores['古力娜扎'].clear()
# print(scores)


dict1 = {'name': 'Alice', 'age': 25, 'city': 'Beijing'} # 这里只是创建

dict2 = {'age': 26, 'desc': '2026'}

print(*dict1) # 拆包  针对于 keys
#print(**dict1)
print(dict1)




#  ** 拆包传给函数（展开为关键字参数）
def f1(name, age, city):
    print(f"f1{name}, {age}, {city}")

def f2(**kwargs):  # 这里定义的时候相当于组包
    print(f'f2{kwargs}')

f1(**dict1)  # 等价于 f(name="Alice", age=25, city="Beijing")
f2(**dict1)  # 拆包

dict_new = {**dict2,**dict1}
dict_new2 = {'name':"Alice", 'age':25, 'city':"Beijing",'age': 26, 'desc': '2026'}
# 先对 dict1 和 dict2 进行拆包  然后重组为新的字典  如果有key重复 则后面的覆盖前面的
print(dict_new)
print(dict_new2)






















