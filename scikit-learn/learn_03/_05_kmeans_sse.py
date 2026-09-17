"""
k-means
"""

import os
os.environ['OMP_NUM_THREADS'] = '4'

from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import calinski_harabasz_score

# 构造数据


x,y = make_blobs(n_samples=1000,
                 n_features=2,
                 centers=[[-1,-1],[0,0],[1,1],[2,2]],
                 cluster_std=[0.4,0.2,0.2,0.2],
                 random_state=666
                 )

sse_list = []

for i in range(1,100):
    model = KMeans(n_clusters=i, max_iter=100, random_state=666)
    model.fit(x)
    sse_list.append(model.inertia_ ) # 获取sse的值



plt.figure(figsize=(18, 8), dpi=100)
plt.xticks(range(0, 100, 3), labels=range(0, 100, 3))
plt.grid()
plt.title('sse')
plt.plot(range(1, 100), sse_list, '*b-')
plt.show()


















