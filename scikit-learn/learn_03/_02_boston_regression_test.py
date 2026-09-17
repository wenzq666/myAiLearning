"""
CART树回归任务
"""
# 导入必要的库和模块
# from sklearn.datasets import load_boston  # 数据  # 注意：此数据集在新版scikit-learn中已被移除
from sklearn.preprocessing import StandardScaler        # 特征处理：标准化
from sklearn.model_selection import train_test_split    # 数据集划分：将数据集分为训练集和测试集
from sklearn.linear_model import LinearRegression       # 正规方程的回归模型：线性回归
from sklearn.linear_model import SGDRegressor           # 梯度下降的回归模型：随机梯度下降回归
from sklearn.metrics import mean_squared_error          # 均方误差评估：用于评估模型性能
from sklearn.linear_model import Ridge, RidgeCV         # 岭回归和交叉验证岭回归

# 数据集相关库
import pandas as pd    # 用于数据处理和分析
import numpy as np     # 用于数值计算
from sklearn.tree import DecisionTreeRegressor

# 加载波士顿房价数据集
data_url = "http://lib.stat.cmu.edu/datasets/boston"  # 数据集URL
raw_df = pd.read_csv(data_url, sep="\\s+", skiprows=22, header=None)  # 读取原始数据，跳过前22行，无列名
# print(raw_df)  # 打印原始数据


# 数据预处理：将原始数据整理为特征矩阵和目标变量
data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])  # 特征矩阵
target = raw_df.values[1::2, 2]  # 目标变量（房价）
# print(data)  # 打印特征数据



# 使用train_test_split函数将数据集划分为训练集和测试集
# x_train: 训练集特征数据
# x_test: 测试集特征数据
# y_train: 训练集标签数据
# y_test: 测试集标签数据
# data: 原始特征数据集
# target: 原始目标数据集
# random_state=66: 设置随机种子，确保每次划分结果一致，便于复现实验结果
x_train, x_test, y_train, y_test = train_test_split(data,target,random_state=66)

#标准化
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

#模型训练
# 默认训练偏置
model = LinearRegression()
model.fit(x_train,y_train)
print("权重",model.coef_)
print("偏置",model.intercept_)

y_pred = model.predict(x_test)

#sgd = SGDRegressor(max_iter=20, loss="squared_error", learning_rate="constant",eta0=0.01)
sgd = DecisionTreeRegressor(criterion='squared_error',max_depth=5)

sgd.fit(x_train,y_train)
y_sgd_pred = sgd.predict(x_test)

#模型评估
loss = mean_squared_error(y_test,y_pred)
print("回归损失",loss)

loss_sgd = mean_squared_error(y_test,y_sgd_pred)
print("梯度损失",loss_sgd)



