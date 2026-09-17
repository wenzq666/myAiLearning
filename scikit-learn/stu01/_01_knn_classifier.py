"""
KNN算法分类模型
"""
from sklearn.neighbors import KNeighborsClassifier

# 训练集特征
x_train = [[0],[1],[2],[3]]

# 训练集标签
y_train = [1, 1, 0, 0]

# 测试集特征
x_test = [[5]]

# 创建模型对象
estimator = KNeighborsClassifier(n_neighbors=4)

# 模型训练
estimator.fit(x_train, y_train)

# 模型预测
y_pred = estimator.predict(x_test)

# 打印预测结果
print(y_pred)


























