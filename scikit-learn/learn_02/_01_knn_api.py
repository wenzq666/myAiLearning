"""
knn分类
"""

from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor

# 准备数据
x = [[1],[2],[3],[4]]
y = [0,0,1,1]

# 实例化模型
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(x,y)

print(knn.predict([[5]]))


"""
knn回归
"""

# 准备数据
x = [[0, 0, 1],
     [1, 1, 0],
     [3, 10, 10],
     [4, 11, 12]]

y = [0.1, 0.2, 0.3, 0.4]

model = KNeighborsRegressor(n_neighbors=2)
model.fit(x,y)

print(model.predict([[1, 1, 3]]))











