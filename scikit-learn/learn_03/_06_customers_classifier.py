"""
k-means
"""



import os
os.environ['OMP_NUM_THREADS'] = '1'


import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import calinski_harabasz_score, silhouette_score

# 加载数据
customer_data = pd.read_csv("./data/customers.csv")
print(customer_data.head())
customer_data.info()

# 获取训练数据
x = customer_data.iloc[:, [3, 4]]

def dm01_see_sc():
    # 肘方法 轮廓系数选择K值
    sse = []

    sc = []

    # 遍历[2,11)k值 计算see sc
    for k in range(2,11):
        km = KMeans(n_clusters=k)
        km.fit(x)
        sse.append(km.inertia_)
        pred = km.predict(x)
        sc.append(silhouette_score(x,pred))


    # 绘制肘方法 轮廓系数 分析图
    fig = plt.figure(figsize=(20,10))
    # 序号 行数 列数
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.plot(range(2,11),sse)
    ax1.set_xlabel("clusters")
    ax1.set_ylabel("SEE")
    ax1.grid()

    ax2 = fig.add_subplot(2, 2, 1)
    ax2.plot(range(2,11),sc)
    ax2.set_xlabel("clusters")
    ax2.set_ylabel("SC")
    ax2.grid()

    plt.show()


def dm_02_show():
    km = KMeans(n_clusters=5)
    km.fit(x)
    y_kmeans = km.predict(x)

    # 把类别是0的, 第0类数据,第1列数据, 作为x/y, 传给plt.scatter函数
    plt.scatter(x.values[y_kmeans == 0, 0], x.values[y_kmeans == 0, 1], s=100, c='red', label='Standard')
    # 把类别是1的, 第0类数据,第1列数据, 作为x/y, 传给plt.scatter函数
    plt.scatter(x.values[y_kmeans == 1, 0], x.values[y_kmeans == 1, 1], s=100, c='blue', label='Traditional')
    # 把类别是2的, 第0类数据,第1列数据, 作为x/y, 传给plt.scatter函数
    plt.scatter(x.values[y_kmeans == 2, 0], x.values[y_kmeans == 2, 1], s=100, c='green', label='Normal')
    plt.scatter(x.values[y_kmeans == 3, 0], x.values[y_kmeans == 3, 1], s=100, c='cyan', label='Youth')
    plt.scatter(x.values[y_kmeans == 4, 0], x.values[y_kmeans == 4, 1], s=100, c='magenta', label='TA')
    plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1], s=300, c='black', label='Centroids')
    plt.title('Clusters of customers')
    plt.xlabel('Annual Income (k$)')
    plt.ylabel('Spending Score (1-100)')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    dm_02_show()





