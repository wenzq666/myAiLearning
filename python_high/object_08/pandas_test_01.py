import pandas as pd


s1 = pd.Series([1, 2, 3, 4, 5,1])
print(type(s1))
print(s1)


# 字典对象
s2 = pd.Series({'a': 1, 'b': 2, 'c': 3})
print(type(s2))
print(s2)


# 手动设置索引
s3 = pd.Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'])
print(type(s3))
print(s3)

print(s3.index)
print(s3.values)

print(s3.shape)
print(s3.size)
print(s3.ndim)
print(s3.dtype)

print('sum-->',s3.sum())
print('mean-->',s3.mean())
print('max-->',s3.max())
print('min-->',s3.min())
print('std-->',s3.std())
print('var-->',s3.var())
print('cumsum-->',s3.cumsum())
print('cumprod-->',s3.cumprod())
print('describe-->',s3.describe())
print('unique-->',s3.unique())









