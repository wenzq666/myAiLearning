"""
k-means
"""
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import calinski_harabasz_score

# 构造数据


x,y = make_blobs(n_samples=1000,
                 n_features=2,
                 centers=[[-1,-1],[0,0],[1,1],[2,2]],
                 cluster_std=[0.9,0.5,0.35,0.8],
                 random_state=666
                 )
# print(x,y)

# 绘制数据分布
plt.figure()
# plt.scatter(x[:, 0], x[:, 1], marker='o')
# plt.show()

# 3 使用k-means进行聚类, 并使用CH方法评估
y_pred = KMeans(n_clusters=1000, random_state=666).fit_predict(x)
plt.scatter(x[:, 0], x[:, 1], c=y_pred,marker='1')
plt.show()
# 4 模型评估
print(calinski_harabasz_score(x, y_pred))

























