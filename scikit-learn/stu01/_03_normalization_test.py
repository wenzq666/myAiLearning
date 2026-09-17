"""
归一化
"""

from sklearn.preprocessing import MinMaxScaler

# 准本数据集
x_train = [[90, 2, 10, 40],[60, 4, 15, 45],[75, 3, 13,46]]

# 创建归一化对象
# feature_range 默认区间范围 [0, 1]
transfer = MinMaxScaler(feature_range=(0, 1))

# 进行归一化
x_train_new = transfer.fit_transform(x_train)
print(x_train_new)














