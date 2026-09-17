"""
归一化
"""
from sklearn.preprocessing import MinMaxScaler,StandardScaler

data = [[90, 2, 10, 40],
        [60, 4, 15, 45],
        [75, 3, 13, 46]]

# 实例化
mmScaler = MinMaxScaler(feature_range=(0, 1))

data = mmScaler.fit_transform(data)

print(data)


"""
标准化
"""
stdScaler = StandardScaler()
data = stdScaler.fit_transform(data)
print(data)





