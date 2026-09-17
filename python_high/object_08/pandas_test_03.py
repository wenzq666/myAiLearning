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


df1 = pd.DataFrame(dict1,index=['s1','s2','s3'])
print(type(df1))
print(df1)

# print(df1.head(n=1))
# print(df1.tail(n=1))
#
# print(df1.describe())
#
# print('*'*50)
#
# names = df1['name']
# print(type(names))
# print(names)
#
#
# datas = df1[['name','age']]
# print(type(datas))
# print(datas)
# print('*'*50)
#
# # 行索引值  等同于 where
# #df1.loc[s1]
# print(df1.loc['s1'])
print(df1.loc[['s1','s3']])
# print(df1.loc['s1':'s3'])
#
#
# # 行下标值
# #df1.iloc[0,1]
# print(df1.iloc[0])
# print(df1.iloc[[0,2]])
# print(df1.iloc[0:2])

print('*'*50)

#  拿到某个值  iloc[行下标值,列下标值]
print(df1.iloc[0,2])

# 使用iloc方法根据整数位置选择数据
# 选择第2、0、1行和第1、2列的数据
print(df1.iloc[[2, 0 ,1], [1, 2]])

print(df1.iloc[:, [1, 2]])








