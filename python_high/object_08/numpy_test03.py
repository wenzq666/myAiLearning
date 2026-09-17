import numpy as np


arr1 = np.array([[1, 2, 3], [4, 5, 6],[7, 8, 9]])
print(arr1)

# 求和
print(np.sum(arr1)) # 45
print(arr1.sum()) # 45
# 按列
print(arr1.sum(axis=0)) # [12 15 18]
# 按行
print(arr1.sum(axis=1)) # [ 6 15 24]

# 累加和
print(arr1.cumsum()) # [ 1  3  6 10 15 21 28 36 45]


# 平均值
print(np.mean(arr1, axis=0)) # [4. 5. 6.]
print(np.mean(arr1, axis=1)) # [2. 5. 8.]


# 标准差  方差的开发
print(np.std(arr1)) # 2.581988897471611

# 方差:所有元素与平均值的平方求和/元素个数
# 衡量数据的离散程度 ,方差越大,数据越离散
print(np.var(arr1)) # 6.666666666666667
print(arr1.var())

# 最大值
print(np.max(arr1))
print(np.max(arr1, axis=0))

# 最小值
print(np.min(arr1))


#最大值下标
print(np.argmax(arr1)) # 8
print(np.argmax(arr1, axis=0)) # [2 2 2]
print(np.argmax(arr1, axis=1)) # [2 2 2]

# 最小值下标
print(np.argmin(arr1)) # 0
print(np.argmin(arr1, axis=0)) # [0 0 0]
print(np.argmin(arr1, axis=1)) # [0 0 0]
















