import pandas as pd

"""
DataFrame
"""
# 字典中的key是df对象的列名  value是df对象的列数据值
dict1 = {
    "name": ["迪丽热巴", "古力娜扎", "马儿扎哈"],
    "age": [20, 25, 30],
    "gender": ["女", "♀", "🚺"],
    "height": [165, 170, 175]
}


pd1 = pd.DataFrame(dict1)
print(type(pd1))
print(pd1)

print('*'*50)

# 二维列表
# list1 = [['迪丽热巴', 20, '女', 165], ['古力娜扎', 25, '♀', 170], ['马儿扎哈', 30, '🚺', 175]]
list1 = (['迪丽热巴', 20, '女', 165], ['古力娜扎', 25, '♀', 170], ['马儿扎哈', 30, '🚺', 175])
pd2 = pd.DataFrame(list1, index=['s1','s2','s3'], columns=['name', 'age', 'gender', 'height'])
print(type(pd2))
print(pd2)
























