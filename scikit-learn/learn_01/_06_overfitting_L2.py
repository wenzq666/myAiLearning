import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error  # 计算均方误差
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge


def dm01_overfiting():
    # 1. 准备数据 x, y (增加噪声)
    np.random.seed(666)
    x = np.random.uniform(-3, 3, size=100)
    # 真实关系是一个二次函数: y = 0.5x^2 + x + 2
    y = 0.5 * x ** 2 + x + 2 + np.random.normal(0, 1, size=100)

    # 2. 实例化线性回归模型 (一次模型)
    estimator = Ridge(alpha=5)

    # 3. 训练模型
    X = x.reshape(-1, 1)
    # 增加二次项特征
    X = np.hstack([X, X ** 2,  X ** 3,  X ** 4,  X ** 5, X ** 10, X ** 15, X ** 20, X ** 25, X ** 30])

    estimator.fit(X, y)

    # 4. 模型预测
    y_predict = estimator.predict(X)

    # 5. 计算均方误差
    myret = mean_squared_error(y, y_predict)
    print('均方误差-->', myret)

    # 6. 画图
    # 注意：因为 x 是随机生成的，如果不按顺序排列直接画折线图，线条会来回交错混乱
    # 解决方法：对 x 进行排序，并按照排序后的索引获取对应的预测值

    plt.scatter(x, y)
    plt.plot(np.sort(x), y_predict[np.argsort(x)], color='r')
    plt.show()


# 运行函数
if __name__ == '__main__':
    dm01_overfiting()