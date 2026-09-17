
#
dict = {'name' :'liming','age':18}

dict2 = {'age':20,'desc':'12325465'}



# print(dict)
# print(*dict) # 针对key进行拆包

# def f(**kwargs): # 组包
#     print(kwargs)

# def f2(name,age):
#     print(name,age)
#
# f2(**dict)  # --> 拆包  f(name ='liming' , age=18)
#f(name ='liming' , age=18)

dict_new = {**dict,**dict2}  # -->  {name ='liming' , age=20,desc='12325465' }
print(dict_new)






















