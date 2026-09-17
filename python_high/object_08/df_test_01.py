import pandas as pd


# 加载csv文件
df = pd.read_csv('./data/清洗数据.csv',sep=',')
print(df)

# 判断缺失值 缺失值返回True
print(df.isnull())

# 取反 是缺失值返回False
print(df.notnull())

# 统计缺失值
print(df.isnull().sum())
# 按行统计
print(df.isnull().sum(axis=1))

df.info()


print('*'*50)
# 缺失值处理
# 1.删除 大量的缺失值
# inplace=True 修改原数据
# 默认按行删除  有缺失值删除整行
# how='all' 全部行都为缺失值才删除
# how='any' 只要有缺失值就删除
# df.dropna(axis=0,  inplace=True ,how='all')
# print(df)
# print('*'*50)
# 2.填充 少量缺失值
# df.fillna(value=df.mean(),inplace=True)
# print(df)
print('*'*50)
df['A'] = df['A'].fillna(value=df['A'].mean())
print(df)

