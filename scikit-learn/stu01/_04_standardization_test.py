"""
标准化
"""

from sklearn.preprocessing import StandardScaler

# 准本数据集
x_train = [[90, 2, 10, 40],[60, 4, 15, 45],[75, 3, 13,46]]

transfer = StandardScaler()


# 进行标准化
x_train_new = transfer.fit_transform(x_train)
print(x_train_new)

# 均值和方差
print(transfer.mean_)
print(transfer.var_)
print(transfer.scale_) # 标准差










